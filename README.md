# Final Project - Market Prioritization UMKM
## Dari Volume ke Kesiapan: Segmentasi Wilayah dan Prioritisasi Leads UMKM

**Studi kasus:** Skalar Solutions - Klay (POS + AI Sales Analytics)
**Kelompok:** 13
**Anggota:**
1. Ayu Safitri (2610501106) - Data collection & data understanding
2. Carissa Zia W. F (2610514008) - Data preparation & merging
3. Gerard Harjuno N (2610512189) - EDA, visualisasi, segmentasi & prioritisasi

## Ringkasan

Analisis mencakup 35 kabupaten/kota Provinsi Jawa Tengah. Setelah filter kualitas data,
30 wilayah dianalisis dan dipecah menjadi 90 segmen sektor x wilayah (Ritel, F&B, Jasa).
Lima komponen ICP dinormalisasi Min-Max, lalu wilayah disegmentasi dengan K-Means k=3.
Skor prioritas segmen dipakai untuk menyusun Top 5, dibandingkan dengan baseline volume,
diuji sensitivitasnya, dan diterjemahkan menjadi strategi SDR per tier.

Temuan utama: Top 5 ICP seluruhnya berada di Kota Semarang dan Kota Surakarta, sementara
Top 5 volume seluruhnya Ritel kabupaten. Overlap keduanya 0/5 (Spearman rho = 0,738).
Prioritas tidak sama dengan ukuran pasar.

## Sumber data

| No | Sumber | Link | Level |
|---|---|---|---|
| 1 | BPS Jateng, *Provinsi Jawa Tengah Dalam Angka 2025* | https://jateng.bps.go.id/id/publication/2025/02/28/6f9ad30e8755ed2b706cb979/provinsi-jawa-tengah-dalam-angka-2025.html | Kab/kota |
| 2 | BPS Jateng, Penduduk menurut Kabupaten/Kota 2024 | https://data.jatengprov.go.id/dataset/79a-penduduk-laju-pertumbuhan-penduduk-distribusi-persentase-penduduk-kepadatan-penduduk-rasio-jenis | Kab/kota |
| 3 | BPS Jateng, IPM menurut Kabupaten/Kota 2024 | https://data.jatengprov.go.id/dataset/6c4-indeks-pembangunan-manusia-ipm-menurut-kabupaten-kota | Kab/kota |
| 4 | Dinkop Jateng, Pelaku Usaha per Lapangan Usaha 2024 | https://data.jatengprov.go.id/dataset/f23725ac-b792-4e7d-9506-0d16f392f6a4/resource/4e820490-c1fc-4b8e-b398-d9ff49caad45/download/jumlah-pelaku-usaha-berdasarkan-lapangan-usaha-hasil-pendataan-lengkap-koperasi-usaha-mikro-kec.xlsx | Kab/kota x 17 KBLI |

Sumber 4 dipakai untuk mendapatkan jumlah unit Ritel, F&B, dan Jasa per kabupaten/kota.
Tiga kategori KBLI dipetakan: perdagangan besar/eceran -> Ritel; akomodasi dan makan/minum
-> F&B; aktivitas jasa lainnya -> Jasa.

## Struktur file

```
.
├── FinalProject_DS_Kelompok13.ipynb       # notebook utama, sudah tereksekusi
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── umkm_sektor_2024.xlsx          # sumber sektor Dinkop
│   └── processed/
│       ├── master_clean.csv               # 30 wilayah hasil Tugas 2
│       ├── umkm_sektor_clean.csv          # 35 wilayah x 17 KBLI
│       ├── master_final.csv               # 30 wilayah + komponen + klaster
│       ├── segments_final.csv             # 90 segmen + skor + peringkat
│       ├── top5_segments.csv              # tabel Top 5
│       ├── baseline_comparison.csv        # Top 5 ICP vs Top 5 volume
│       ├── sensitivity_scenarios.csv      # uji sensitivitas bobot
│       ├── cluster_profile.csv            # profil rata-rata klaster
│       ├── kmeans_evaluation.csv          # elbow dan silhouette
│       ├── cluster_score_summary.csv      # ringkasan skor per klaster
│       ├── scraping_legality.csv          # tabel legalitas sumber leads
│       └── sdr_strategy.csv               # strategi SDR per tier
├── figures/
│   ├── final_elbow_silhouette.png
│   ├── final_clusters_pca.png
│   ├── final_cluster_profile.png
│   ├── final_top5_segments.png
│   ├── final_baseline.png
│   ├── final_sensitivity.png
│   └── final_cluster_score.png
├── report/
│   ├── FinalProject_DS_Kelompok13.pdf     # laporan final
│   ├── FinalProject_DS_Kelompok13.pptx    # slide 12 halaman 16:9
│   └── FinalProject_DS_Kelompok13_Slides.pdf
└── scripts/
    ├── build_final_dataset.py             # bangun dataset final
    ├── final_analysis.py                  # K-Means, skor, baseline, sensitivitas
    ├── make_final_notebook.py             # generator notebook
    ├── make_final_report.py               # generator laporan PDF
    └── make_final_slides.py               # generator slide PPTX
```

## Cara menjalankan

1. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```

2. Bentuk ulang dataset final:

   ```bash
   python3 scripts/build_final_dataset.py
   ```

3. Jalankan analisis dan buat ulang figur/tabel:

   ```bash
   python3 scripts/final_analysis.py
   ```

4. Tulis ulang dan eksekusi notebook:

   ```bash
   python3 scripts/make_final_notebook.py
   jupyter nbconvert --to notebook --execute --inplace FinalProject_DS_Kelompok13.ipynb
   ```

5. Buat ulang laporan dan slide:

   ```bash
   python3 scripts/make_final_report.py
   python3 scripts/make_final_slides.py
   ```

## Keputusan analisis penting

- **Kode wilayah** diparse dari format desimal (`33.10` -> `3310`). Tanpa pembulatan ini,
  Klaten dan Jepara hilang dari dataset.
- **Unit sektor** adalah jumlah pelaku usaha hasil pendataan Dinkop, bukan seluruh UMKM.
  Angka ini dipakai sebagai proxy populasi sektor.
- **Bobot ICP** ditetapkan sebelum melihat hasil: Ukuran Pasar 25%, Kepadatan Sektor 25%,
  Kesiapan Digital 20%, Adopsi Digital 15%, Aktivitas Ekonomi 15%.
- **K-Means** dijalankan pada lima komponen wilayah. k=3 dipilih karena silhouette tertinggi
  dalam rentang wajib 3-5 (0,390); k=2 lebih tinggi (0,578) tetapi di luar rentang.
- **Skor segmen** memakai komponen wilayah yang sama, ditambah normalisasi volume dan
  kepadatan sektor pada 90 segmen.
- **Baseline** hanya mengurutkan jumlah unit sektor, tanpa komponen kesiapan.
- **Sensitivitas** menggeser bobot digital, adopsi, dan PDRB sebesar +/-5-10 poin persentase.

## Hasil utama

### Klaster wilayah

| Tipe wilayah | Jumlah | Ukuran | Kepadatan | Digital | Adopsi | Ekonomi |
|---|---:|---:|---:|---:|---:|---:|
| Hub Digital Matang | 3 | 0,271 | 0,318 | 0,789 | 0,694 | 0,888 |
| Sentra Perdagangan Padat | 14 | 0,641 | 0,512 | 0,223 | 0,040 | 0,103 |
| Wilayah Rintisan | 13 | 0,209 | 0,222 | 0,318 | 0,058 | 0,134 |

### Top 5 segmen

| # | Sektor | Wilayah | Skor | Unit |
|---|---|---|---:|---:|
| 1 | Ritel | Kota Semarang | 0,657 | 20.547 |
| 2 | F&B | Kota Semarang | 0,610 | 15.600 |
| 3 | Ritel | Kota Surakarta | 0,594 | 9.871 |
| 4 | F&B | Kota Surakarta | 0,532 | 6.269 |
| 5 | Jasa | Kota Semarang | 0,530 | 6.925 |

Baseline Top 5: Ritel Banyumas (44.960), Ritel Tegal (39.767), Ritel Grobogan (39.264),
Ritel Purbalingga (37.960), Ritel Cilacap (35.905). Overlap dengan Top 5 ICP = 0/5.

### Sensitivitas

Spearman rho terhadap baseline tetap di atas 0,97 pada semua skenario, tetapi overlap Top 5
turun ke 3/5 saat bobot adopsi, PDRB, atau digital diturunkan. Tiga nama teratas relatif
stabil; posisi keempat dan kelima perlu divalidasi dengan data pipeline.

## Legalitas sumber leads

Tabel lengkap ada di `data/processed/scraping_legality.csv`. Ringkasnya:

- **Google Maps/Places:** robots.txt membatasi; ToS melarang scraping. Gunakan Places API.
- **OpenStreetMap:** gunakan planet.osm/ekstrak resmi dengan atribusi ODbL; jangan crawl situs.
- **LinkedIn, Tokopedia, Shopee:** ToS melarang crawling/scraping. Jangan dipakai.
- **Portal Satu Data Dinkop Jateng:** robots.txt mengizinkan; tidak ada izin scraping eksplisit.
  Gunakan unduhan resmi/API dan batasi laju permintaan.

Pemeriksaan dokumen dilakukan pada 2 November 2026. Kebijakan dapat berubah.

## Limitasi

- Data cross-section 2023-2024 tidak mendukung inferensi kausal.
- IPM, pengeluaran, simpanan, dan tabungan adalah proxy, bukan ukuran langsung literasi digital.
- Dataset Dinkop mencakup pelaku usaha hasil pendataan, bukan seluruh UMKM.
- Kepadatan memakai denominator penduduk, bukan jumlah usaha aktif.
- Silhouette K-Means moderat (0,390); label klaster adalah alat strategi, bukan taksonomi kaku.
- Tidak ada scraping yang dijalankan; tabel legalitas adalah kajian dokumen, bukan nasihat hukum.

## Arsip Tugas 2

Laporan Milestone 1 tetap tersedia di `report/Tugas2_DS_Kelompok13.pdf` dan
`Tugas2_DS_Kelompok13.zip`. Final Project memakai `data/processed/master_clean.csv` sebagai
titik sambung dari Tugas 2, lalu menambahkan dataset sektor 2024.
