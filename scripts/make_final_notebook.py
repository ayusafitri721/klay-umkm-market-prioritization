"""Generate the executed-ready Final Project notebook."""
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "FinalProject_DS_Kelompok13.ipynb"

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip()))


md("""
# Final Project — Market Prioritization UMKM
**Kelay: POS + AI Sales Analytics untuk UMKM | Kelompok 13**

Notebook ini melanjutkan Milestone 1 (Tugas 2) menjadi analisis final: segmentasi wilayah
dengan K-Means, skor prioritas per **sektor × wilayah**, Top 5 segmen, baseline volume,
uji sensitivitas bobot, tabel legalitas scraping, dan strategi SDR.

**Anggota**
1. Ayu Safitri (2610501106) — data collection & data understanding
2. Carissa Zia W. F (2610514008) — data preparation & merging
3. Gerard Harjuno N (2610512189) — EDA, visualisasi & rancangan bobot ICP
""")

md("""
## 1. Setup dan pemuatan data
Dataset final berisi 30 kabupaten/kota yang lolos filter kualitas dan 90 segmen
(30 wilayah × 3 sektor: Ritel, F&B, Jasa).
""")

code("""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.stats import spearmanr

sns.set_theme(style="whitegrid", palette="deep", font_scale=0.9)
plt.rcParams["figure.dpi"] = 120

ROOT = Path.cwd()
DATA = ROOT / "data" / "processed"
FIG = ROOT / "figures"

master = pd.read_csv(DATA / "master_final.csv")
segments = pd.read_csv(DATA / "segments_final.csv")
sektor = pd.read_csv(DATA / "umkm_sektor_clean.csv")
scraping = pd.read_csv(DATA / "scraping_legality.csv")
sdr = pd.read_csv(DATA / "sdr_strategy.csv")

print("master_final:", master.shape)
print("segments_final:", segments.shape)
print("umkm_sektor_clean:", sektor.shape)
display(master[["kode_wilayah", "wilayah", "tipe", "total_target_unit", "label_klaster"]].head())
""")

md("""
## 2. Cakupan data dan sumber
Empat sumber publik dipakai: BPS JatengDalamAngka 2025, data penduduk 2024, IPM 2024,
dan Dinkop Jateng 2024 untuk komposisi sektor. Dataset sektor memberi dimensi yang tidak
tersedia di Tugas 2: jumlah unit Ritel, F&B, dan Jasa per kabupaten/kota.
""")

code("""
print("Wilayah:", master["wilayah"].nunique())
print("Segmen:", len(segments))
print("\\nTotal unit per sektor:")
print(segments.groupby("sektor")["unit_sektor"].sum().sort_values(ascending=False).to_string())
print("\\nJumlah segmen per sektor:")
print(segments.groupby("sektor").size().to_string())
""")

md("""
## 3. Komponen ICP dan bobot
Lima komponen dinormalisasi Min-Max pada 30 wilayah. Skor segmen memakai komponen wilayah
yang sama, ditambah normalisasi volume dan kepadatan sektor pada 90 segmen.
""")

code("""
bobot = pd.DataFrame(
    [
        ("Ukuran Pasar", "Total unit Ritel + F&B + Jasa", 0.25),
        ("Kepadatan Sektor", "Unit target per 100.000 penduduk", 0.25),
        ("Kesiapan Digital", "IPM dan pengeluaran per kapita", 0.20),
        ("Adopsi Digital", "Simpanan dan tabungan per kapita", 0.15),
        ("Aktivitas Ekonomi", "PDRB per kapita 2024", 0.15),
    ],
    columns=["Komponen", "Indikator", "Bobot"],
)
bobot["Bobot"] = bobot["Bobot"].map(lambda x: f"{x:.0%}")
display(bobot)
print("Total bobot:", "100%")
""")

md("""
## 4. Segmentasi wilayah dengan K-Means
Rentang k yang diwajibkan adalah 3–5. k=3 dipilih karena silhouette tertinggi di dalam
rentang tersebut; k=2 memiliki silhouette lebih tinggi tetapi berada di luar rentang.
""")

code("""
COMP_COLS = [
    "komp_ukuran_pasar",
    "komp_kepadatan_sektor",
    "komp_kesiapan_digital",
    "komp_adopsi_digital",
    "komp_aktivitas_ekonomi",
]
X = master[COMP_COLS].to_numpy()

rows = []
for k in range(2, 7):
    model = KMeans(n_clusters=k, random_state=42, n_init=50)
    labels = model.fit_predict(X)
    rows.append(
        {
            "k": k,
            "inertia": round(model.inertia_, 6),
            "silhouette": round(silhouette_score(X, labels), 6),
        }
    )
evaluasi = pd.DataFrame(rows)
display(evaluasi)
print("k optimal (3-5):", int(evaluasi[evaluasi.k.between(3, 5)].sort_values("silhouette").iloc[-1]["k"]))
""")

code("""
from IPython.display import Image, display as show

show(Image(filename=str(FIG / "final_elbow_silhouette.png"), width=820))
""")

md("""
## 5. Profil klaster
Tiga tipe wilayah yang terbentuk:
- **Hub Digital Matang** — IPM, adopsi digital, dan PDRB tinggi (Kota Semarang, Kota Surakarta, Kudus).
- **Sentra Perdagangan Padat** — volume dan kepadatan sektor tinggi, adopsi digital rendah.
- **Wilayah Rintisan** — volume dan kesiapan digital rendah, tetapi menjadi pasar edukasi.
""")

code("""
profil = pd.read_csv(DATA / "cluster_profile.csv")
display(profil.round(3))
show(Image(filename=str(FIG / "final_clusters_pca.png"), width=820))
show(Image(filename=str(FIG / "final_cluster_profile.png"), width=820))
""")

md("""
## 6. Skor prioritas dan Top 5 segmen
Skor tinggi tidak otomatis berarti volume terbesar. Kota Semarang dan Kota Surakarta
unggul karena kombinasi volume, kepadatan, kesiapan digital, dan aktivitas ekonomi.
""")

code("""
top10 = (
    segments.sort_values("skor_icp", ascending=False)
    .head(10)[["peringkat", "sektor", "wilayah", "unit_sektor", "kepadatan_sektor", "skor_icp", "label_klaster"]]
    .copy()
)
top10["skor_icp"] = top10["skor_icp"].round(4)
top10["kepadatan_sektor"] = top10["kepadatan_sektor"].round(0)
display(top10)

top5 = pd.read_csv(DATA / "top5_segments.csv")
display(top5)
show(Image(filename=str(FIG / "final_top5_segments.png"), width=820))
""")

md("""
## 7. Baseline volume vs skor ICP
Baseline hanya mengurutkan segmen berdasarkan jumlah unit. Hasilnya berbeda total:
Top 5 ICP tidak beririsan dengan Top 5 volume (overlap 0/5). Ini menunjukkan pentingnya
kesiapan digital dan kepadatan, bukan sekadar ukuran pasar.
""")

code("""
baseline = pd.read_csv(DATA / "baseline_comparison.csv")
display(baseline)
overlap = len(
    set(zip(segments.nsmallest(5, "peringkat")["sektor"], segments.nsmallest(5, "peringkat")["wilayah"]))
    & set(zip(segments.nsmallest(5, "baseline_rank")["sektor"], segments.nsmallest(5, "baseline_rank")["wilayah"]))
)
rho = spearmanr(segments["skor_icp"], segments["unit_sektor"]).statistic
print(f"Overlap Top 5: {overlap}/5 | Spearman rho: {rho:.3f}")
show(Image(filename=str(FIG / "final_baseline.png"), width=820))
""")

md("""
## 8. Uji sensitivitas bobot
Perubahan bobot digital, adopsi, dan PDRB sebesar ±5–10 poin persentase menggeser
peringkat banyak segmen, tetapi Top 5 relatif stabil pada skenario kenaikan. Skenario
penurunan membuat 3 dari 5 segmen tetap. Artinya rekomendasi tidak bergantung pada satu
bobot saja, namun tetap perlu diuji saat data baru masuk.
""")

code("""
sens = pd.read_csv(DATA / "sensitivity_scenarios.csv")
display(sens)
show(Image(filename=str(FIG / "final_sensitivity.png"), width=860))
""")

md("""
## 9. Analisis legalitas dan etika sumber leads
Tabel berikut merangkum robots.txt dan ketentuan layanan calon sumber. Sumber yang
melarang scraping tidak dipakai; untuk data peta, gunakan API atau bulk data resmi.
""")

code("""
display(
    scraping[
        ["Sumber", "Status_Robots", "Status_ToS", "Status_Kelayakan", "Rekomendasi", "Tanggal_Akses"]
    ]
)
""")

md("""
## 10. Strategi SDR berbasis segmen
Prioritas tidak diberikan rata ke semua wilayah. Tier A fokus pada Top 5 segmen di Hub
Digital Matang; Tier B pada sentra perdagangan padat dengan volume besar; Tier C pada
wilayah rintisan dengan pendekatan edukasi.
""")

code("""
display(
    sdr[
        ["Prioritas", "Tier", "Segmen_Prioritas", "Profil_Wilayah", "Penawaran_Utama", "Channel_Akuisisi"]
    ]
)
""")

md("""
## 11. Rekomendasi dan limitasi
**Rekomendasi**
1. Prioritaskan Ritel dan F&B Kota Semarang serta Kota Surakarta untuk pilot berbayar.
2. Gunakan Sentra Perdagangan Padat sebagai pasar volume dengan paket POS basic dan onboarding.
3. Jadikan Wilayah Rintisan sebagai pipeline edukasi, bukan target volume jangka pendek.
4. Jangan scrape Google Maps, LinkedIn, Tokopedia, atau Shopee; gunakan API/data partner.
5. Ulangi skor setiap kuartal karena data sektor dan adopsi digital berubah.

**Limitasi**
- Dataset sektor 2024 adalah cross-section; belum ada panel antarwaktu.
- Kepadatan dihitung dari penduduk, bukan jumlah usaha aktif per sektor.
- Komponen digital memakai proxy IPM, pengeluaran, simpanan, dan tabungan.
- Data Dinkop mencakup pelaku usaha hasil pendataan, bukan seluruh UMKM.
- Scraping tidak dilakukan; tabel legalitas adalah hasil kajian dokumen publik.
""")

md("""
## 12. Reproduksibilitas
Jalankan ulang dari akar proyek:

```bash
python3 scripts/build_final_dataset.py
python3 scripts/final_analysis.py
python3 scripts/make_final_notebook.py
jupyter nbconvert --to notebook --execute --inplace FinalProject_DS_Kelompok13.ipynb
python3 scripts/make_final_report.py
python3 scripts/make_final_slides.py
```
""")

code("""
for path in [
    DATA / "master_final.csv",
    DATA / "segments_final.csv",
    DATA / "top5_segments.csv",
    DATA / "scraping_legality.csv",
    DATA / "sdr_strategy.csv",
    FIG / "final_top5_segments.png",
]:
    print(("OK " if path.exists() else "MISSING "), path)
""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12"},
}
nbf.write(nb, OUT)
print("Wrote", OUT)
