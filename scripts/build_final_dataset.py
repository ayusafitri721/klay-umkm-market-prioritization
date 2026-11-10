"""Build the Final Project region-level and segment-level datasets.

Inputs:
- data/processed/master_clean.csv          : 30 filtered regions from Tugas 2
- data/raw/umkm_sektor_2024.xlsx           : Dinkop Jateng, pelaku usaha per KBLI/kab-kota 2024

Outputs:
- data/processed/umkm_sektor_clean.csv     : 35 regions x 17 KBLI categories
- data/processed/master_final.csv          : 30 regions + final ICP components
- data/processed/segments_final.csv        : 90 sector x region segments + scores
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

TARGET_SECTORS = {
    "PERDAGANGAN BESAR DAN ECERAN; REPARASI DAN PERAWATAN MOBIL DAN SEPEDA MOTOR": "Ritel",
    "PENYEDIAAN AKOMODASI DAN PENYEDIAAN MAKAN MINUM": "F&B",
    "AKTIVITAS JASA LAINNYA": "Jasa",
}

WEIGHTS = {
    "ukuran": 0.25,
    "kepadatan": 0.25,
    "digital": 0.20,
    "adopsi": 0.15,
    "ekonomi": 0.15,
}


def minmax(series):
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    return (series - lo) / (hi - lo)


def main():
    master = pd.read_csv(OUT / "master_clean.csv")
    sector = pd.read_excel(RAW / "umkm_sektor_2024.xlsx")

    sector["kode_wilayah"] = (
        sector["kd_wilayah"].astype(float).mul(100).round().astype(int)
    )
    sector["sektor"] = sector["jenis_usaha"].map(TARGET_SECTORS)

    sector_clean = (
        sector.pivot_table(
            index="kode_wilayah",
            columns="jenis_usaha",
            values="jumlah",
            aggfunc="sum",
        )
        .reset_index()
    )
    sector_clean.columns.name = None
    sector_clean.to_csv(OUT / "umkm_sektor_clean.csv", index=False)

    target = sector.dropna(subset=["sektor"])
    wide = (
        target.pivot_table(
            index="kode_wilayah",
            columns="sektor",
            values="jumlah",
            aggfunc="sum",
        )
        .reset_index()
    )
    wide.columns.name = None
    wide = wide.rename(
        columns={"Ritel": "unit_ritel", "F&B": "unit_fnb", "Jasa": "unit_jasa"}
    )

    missing = sorted(set(master["kode_wilayah"]) - set(wide["kode_wilayah"]))
    if missing:
        raise ValueError(f"Region sector data missing for: {missing}")

    df = master.merge(wide, on="kode_wilayah", how="left", validate="one_to_one")
    if df[["unit_ritel", "unit_fnb", "unit_jasa"]].isna().any().any():
        raise ValueError("Missing sector counts after merge")

    df["total_target_unit"] = df[["unit_ritel", "unit_fnb", "unit_jasa"]].sum(axis=1)
    df["target_per_100k"] = df["total_target_unit"] / df["penduduk_ribu"] * 100

    df["komp_ukuran_pasar"] = minmax(df["total_target_unit"])
    df["komp_kepadatan_sektor"] = minmax(df["target_per_100k"])
    df["komp_kesiapan_digital"] = (
        minmax(df["ipm"]) + minmax(df["pengeluaran_per_kapita"])
    ) / 2
    df["komp_adopsi_digital"] = (
        minmax(df["simpanan_per_kapita_juta"])
        + minmax(df["tabungan_per_kapita_juta"])
    ) / 2
    df["komp_aktivitas_ekonomi"] = minmax(df["pdrb_per_kapita_2024"])

    comp_cols = [
        "komp_ukuran_pasar",
        "komp_kepadatan_sektor",
        "komp_kesiapan_digital",
        "komp_adopsi_digital",
        "komp_aktivitas_ekonomi",
    ]
    df[comp_cols] = df[comp_cols].clip(0, 1)

    id_cols = [
        "kode_wilayah",
        "wilayah",
        "tipe",
        "penduduk_ribu",
        "ipm",
        "pengeluaran_per_kapita",
        "pdrb_per_kapita_2024",
        "simpanan_per_kapita_juta",
        "tabungan_per_kapita_juta",
        "komp_ukuran_pasar",
        "komp_kepadatan_sektor",
        "komp_kesiapan_digital",
        "komp_adopsi_digital",
        "komp_aktivitas_ekonomi",
    ]

    seg = df[id_cols + ["unit_ritel", "unit_fnb", "unit_jasa"]].melt(
        id_vars=id_cols,
        value_vars=["unit_ritel", "unit_fnb", "unit_jasa"],
        var_name="sektor",
        value_name="unit_sektor",
    )
    seg["sektor"] = seg["sektor"].map(
        {"unit_ritel": "Ritel", "unit_fnb": "F&B", "unit_jasa": "Jasa"}
    )
    seg["kepadatan_sektor"] = seg["unit_sektor"] / seg["penduduk_ribu"] * 100
    seg["ukuran_n"] = minmax(seg["unit_sektor"])
    seg["kepadatan_n"] = minmax(seg["kepadatan_sektor"])

    seg["skor_icp"] = (
        WEIGHTS["ukuran"] * seg["ukuran_n"]
        + WEIGHTS["kepadatan"] * seg["kepadatan_n"]
        + WEIGHTS["digital"] * seg["komp_kesiapan_digital"]
        + WEIGHTS["adopsi"] * seg["komp_adopsi_digital"]
        + WEIGHTS["ekonomi"] * seg["komp_aktivitas_ekonomi"]
    )
    seg["peringkat"] = seg["skor_icp"].rank(ascending=False, method="min").astype(int)
    seg = seg.sort_values(["peringkat", "sektor", "wilayah"]).reset_index(drop=True)

    df.to_csv(OUT / "master_final.csv", index=False)
    seg.to_csv(OUT / "segments_final.csv", index=False)

    print(f"master_final : {df.shape[0]} regions x {df.shape[1]} columns")
    print(f"segments     : {seg.shape[0]} segments")
    print("\nTop 10 segments:")
    print(
        seg.head(10)[
            ["peringkat", "sektor", "wilayah", "unit_sektor", "skor_icp"]
        ].to_string(index=False)
    )
    print("\nSector totals:")
    print(df[["unit_ritel", "unit_fnb", "unit_jasa"]].sum().to_string())


if __name__ == "__main__":
    main()
