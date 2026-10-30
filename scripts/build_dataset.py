"""Build the Milestone 1 dataset from official BPS Jawa Tengah and Dinkop Jateng sources.

Raw inputs (downloaded separately, see README):
- data/raw/jtg2025.pdf          : BPS, Provinsi Jawa Tengah Dalam Angka 2025
- data/raw/penduduk_2024.xlsx   : BPS Jateng, Penduduk menurut Kabupaten/Kota 2024
- data/raw/ipm_2024.xlsx        : BPS Jateng, IPM menurut Kabupaten/Kota 2024
- data/raw/umkm_binaan_2023.xlsx: Dinkop Jateng, Jumlah UMKM Binaan 2023
- data/raw/umkm_binaan_2024.xlsx: Dinkop Jateng, Statistik UKM Binaan s.d. TW II 2024
"""
import re
import numpy as np
import pandas as pd
import pdfplumber

RAW = "data/raw"
OUT = "data/processed"


def clean_num(x):
    if x is None:
        return np.nan
    s = re.sub(r"[^0-9,.\-]", "", str(x))
    if s in ("", "-", ".", ","):
        return np.nan
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return np.nan


def table_rows(page_no):
    with pdfplumber.open(f"{RAW}/jtg2025.pdf") as pdf:
        table = pdf.pages[page_no - 1].extract_tables()[0]
    rows = []
    for row in table:
        if row and re.fullmatch(r"\d+\.", str(row[0]).strip()):
            rows.append(row)
    return rows


def extract_by_order(page_no, value_idx, columns, regions):
    rows = table_rows(page_no)
    assert len(rows) == len(regions), f"page {page_no}: {len(rows)} rows != {len(regions)} regions"
    out = []
    for region, row in zip(regions, rows):
        rec = {"wilayah": region}
        for col, idx in zip(columns, value_idx):
            rec[col] = clean_num(row[idx]) if idx < len(row) else np.nan
        out.append(rec)
    return pd.DataFrame(out)


pop = pd.read_excel(f"{RAW}/penduduk_2024.xlsx")
pop = pop.rename(columns={
    "kod_wil": "kode_wilayah",
    "kab_ko": "wilayah",
    "jumlah_penduduk": "penduduk_ribu",
    "kepadatan_penduduk": "kepadatan_per_km2",
})[["kode_wilayah", "wilayah", "penduduk_ribu", "kepadatan_per_km2"]]
pop["tipe"] = np.where(pop["wilayah"].str.startswith("Kota"), "Kota", "Kabupaten")
regions = pop["wilayah"].tolist()

imk = extract_by_order(845, [2, 3, 4], ["imk_unit", "imk_tenaga_kerja", "imk_nilai_produksi"], regions)
pdrb = extract_by_order(1200, [6], ["pdrb_per_kapita_2024"], regions)
sarana = extract_by_order(1037, [2, 3, 4], ["supermarket", "pasar", "pedagang_pasar"], regions)
simpanan = extract_by_order(1040, [4], ["simpanan_2024"], regions)
tabungan = extract_by_order(1042, [4], ["tabungan_2024"], regions)

# En dash means zero outlets in the BPS trading-facility table.
for col in ["supermarket", "pasar", "pedagang_pasar"]:
    sarana[col] = sarana[col].fillna(0)

ipm_raw = pd.read_excel(f"{RAW}/ipm_2024.xlsx").rename(columns={"kod_wil": "kode_wilayah"})
ipm = (ipm_raw.pivot_table(index="kode_wilayah", columns="indikator", values="indeks", aggfunc="first")
       .reset_index())
ipm = ipm.rename(columns={
    "Indeks Pembangunan Manusia": "ipm",
    "Pengeluaran per kapita Disesuaikan (ribu rupiah/orang/tahun)": "pengeluaran_per_kapita",
    "Harapan Lama Sekolah (tahun)": "harapan_lama_sekolah",
    "Rata-rata Lama Sekolah (tahun)": "rata_rata_lama_sekolah",
    "Usia Harapan Hidup saat Lahir (tahun)": "usia_harapan_hidup",
})[["kode_wilayah", "ipm", "pengeluaran_per_kapita", "harapan_lama_sekolah",
    "rata_rata_lama_sekolah", "usia_harapan_hidup"]]

master = (pop.merge(ipm, on="kode_wilayah", how="left")
             .merge(imk, on="wilayah", how="left")
             .merge(pdrb, on="wilayah", how="left")
             .merge(sarana, on="wilayah", how="left")
             .merge(simpanan, on="wilayah", how="left")
             .merge(tabungan, on="wilayah", how="left"))

# Province-level UMKM series (fostered UMKM, not the universe of all UMKM).
umkm_series = pd.DataFrame({
    "tahun": [2019, 2020, 2021, 2022, 2023, 2024],
    "umkm_binaan": [161458, 167391, 173431, 180579, 186024, 191689],
    "catatan": ["penuh"] * 5 + ["s.d. TW II 2024"],
})
umkm_series["pertumbuhan_yoy_persen"] = umkm_series["umkm_binaan"].pct_change() * 100

# Broadcast a province-level contextual feature. This is a hierarchy-aware merge:
# the province value is a context column, never added to kab/kota counts.
growth_2023 = float(umkm_series.loc[umkm_series.tahun == 2023, "pertumbuhan_yoy_persen"].iloc[0])
master["prov_umkm_growth_2023"] = growth_2023
master["prov_umkm_binaan_2023"] = int(umkm_series.loc[umkm_series.tahun == 2023, "umkm_binaan"].iloc[0])

# Derived density features (population is in thousands).
master["imk_per_100k"] = master["imk_unit"] / master["penduduk_ribu"] * 100
master["pedagang_per_100k"] = master["pedagang_pasar"] / master["penduduk_ribu"] * 100
master["pasar_per_100k"] = master["pasar"] / master["penduduk_ribu"] * 100
master["simpanan_per_kapita_juta"] = master["simpanan_2024"] / (master["penduduk_ribu"] * 1000)
master["tabungan_per_kapita_juta"] = master["tabungan_2024"] / (master["penduduk_ribu"] * 1000)
master["sektor_target_per_100k"] = master["imk_per_100k"] + master["pedagang_per_100k"]

master.to_csv(f"{OUT}/master_raw.csv", index=False)
umkm_series.to_csv(f"{OUT}/provinsi_umkm_series.csv", index=False)

print("master", master.shape)
print(master[["wilayah", "imk_unit", "pdrb_per_kapita_2024", "ipm",
              "imk_per_100k", "pedagang_per_100k"]].head().to_string(index=False))
print("\nmissing:\n", master.isna().sum()[master.isna().sum() > 0])
print("\nprovince growth 2023: %.2f%%" % growth_2023)
