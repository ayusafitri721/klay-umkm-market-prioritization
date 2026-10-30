# Tugas 2 - Milestone 1 Final Project
## Market Prioritization UMKM: Wilayah Target Sourcing Leads B2B SaaS

**Studi kasus:** Skalar Solutions - Klay (POS + AI Sales Analytics)
**Kelompok:** 13
**Anggota:**
1. [Nama 1] - Data collection & data understanding
2. [Nama 2] - Data preparation & merging
3. [Nama 3] - EDA, visualisasi & rancangan bobot ICP

> Lengkapi nama anggota sebelum submit. ZIP akhir: `Tugas2_DS_Kelompok13.zip`.

## Ringkasan

Analisis mencakup 35 kabupaten/kota Provinsi Jawa Tengah. Setelah pembersihan dan filter
kualitas data, 30 wilayah dianalisis untuk menyusun kerangka Indeks Calon Pelanggan (ICP)
Klay. Ruang lingkup berhenti pada perancangan bobot ICP; K-Means, skor akhir, Top 5, dan
uji sensitivitas bobot dikerjakan pada milestone berikutnya.

## Sumber data

| No | Sumber | Link | Level |
|---|---|---|---|
| 1 | BPS Jateng, *Provinsi Jawa Tengah Dalam Angka 2025* | https://jateng.bps.go.id/id/publication/2025/02/28/6f9ad30e8755ed2b706cb979/provinsi-jawa-tengah-dalam-angka-2025.html | Kab/kota |
| 2 | BPS Jateng, Penduduk menurut Kabupaten/Kota 2024 | https://data.jatengprov.go.id/dataset/79a-penduduk-laju-pertumbuhan-penduduk-distribusi-persentase-penduduk-kepadatan-penduduk-rasio-jenis | Kab/kota |
| 3 | BPS Jateng, IPM menurut Kabupaten/Kota 2024 | https://data.jatengprov.go.id/dataset/6c4-indeks-pembangunan-manusia-ipm-menurut-kabupaten-kota | Kab/kota |
| 4 | Dinkop Jateng, Jumlah UMKM Binaan 2019-2024 | https://data.jatengprov.go.id/dataset/7e5-jumlah-umkm-binaan-jawa-tengah | Provinsi |

Tabel PDF yang dipakai dari sumber 1: 7.2.2 (IMK 2023), 13.2.5 (PDRB per kapita 2024),
10.2.23 (sarana perdagangan 2024), 10.3.2/10.3.3 (simpanan/tabungan 2024).

## Struktur file

```
.
├── Tugas2_DS_Kelompok13.ipynb       # notebook utama, sudah tereksekusi
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                         # PDF BPS dan XLSX sumber
│   └── processed/
│       ├── master_raw.csv           # 35 wilayah, sebelum filter
│       ├── master_clean.csv         # 30 wilayah, setelah filter + normalisasi
│       ├── wilayah_tereliminasi.csv # 5 wilayah gugur + alasan
│       └── provinsi_umkm_series.csv # time series UMKM binaan 2019-2024
├── figures/                         # 9 figur EDA dan bobot ICP
├── report/
│   └── Tugas2_DS_Kelompok13.pdf     # laporan ringkas
└── scripts/
    ├── build_dataset.py             # ekstraksi PDF/XLSX -> dataset
    ├── make_notebook.py             # generator notebook
    └── make_report.py               # generator laporan PDF
```

## Cara menjalankan

1. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```

2. Pastikan raw data tersedia di `data/raw/`:

   - `jtg2025.pdf` (Provinsi Jawa Tengah Dalam Angka 2025)
   - `penduduk_2024.xlsx`
   - `ipm_2024.xlsx`
   - `umkm_binaan_2023.xlsx`
   - `umkm_binaan_2024.xlsx`

3. Bentuk ulang dataset:

   ```bash
   python scripts/build_dataset.py
   ```

4. Jalankan notebook:

   ```bash
   jupyter nbconvert --to notebook --execute --inplace Tugas2_DS_Kelompok13.ipynb
   ```

5. Buat ulang laporan:

   ```bash
   python scripts/make_report.py
   ```

## Keputusan analisis penting

- **Nama wilayah kanonik** diambil dari file penduduk berdasarkan urutan 35 wilayah dan
  `kode_wilayah` (3301-3329 kabupaten, 3371-3376 kota), karena PDF BPS tidak membedakan
  Kabupaten vs Kota.
- **En dash** pada tabel sarana perdagangan diisi 0, bukan missing.
- **Merging lintas level**: data provinsi tidak dijumlahkan dengan data kab/kota. Hanya
  pertumbuhan UMKM binaan provinsi 2023 (3,02%) yang di-broadcast sebagai kolom konteks.
  Total UMKM binaan provinsi (186.024) dan total IMK (862.926) mengukur populasi berbeda.
- **Filter penggugur**: IMK < 10.000 unit dan IMK/100k > Q3 + 1,5 IQR. Hasil: 5 wilayah
  gugur, 30 wilayah lolos.
- **Normalisasi**: Min-Max pada 30 wilayah yang lolos. Catatan: simpanan per kapita masih
  sangat miring karena didominasi Kota Semarang; perlu log-transform/winsorization pada
  milestone berikutnya.

## Wilayah yang gugur

| Wilayah | Alasan |
|---|---|
| Kabupaten Pekalongan | IMK/100k > 5.298 (outlier) |
| Kota Magelang | IMK < 10.000 unit |
| Kota Salatiga | IMK < 10.000 unit |
| Kota Pekalongan | IMK < 10.000 unit |
| Kota Tegal | IMK < 10.000 unit |

## Rancangan bobot ICP

| Komponen | Indikator | Arah | Bobot |
|---|---|---|---|
| Ukuran Pasar | Penduduk; pedagang pasar | + | 25% |
| Kepadatan Sektor Target | IMK/100k; pedagang/100k | + | 25% |
| Kesiapan Digital | IPM; pengeluaran per kapita | + | 20% |
| Adopsi Pembayaran Digital | Simpanan/kapita; tabungan/kapita | + | 15% |
| Aktivitas Ekonomi | PDRB per kapita | + | 15% |

Total bobot = 100%. Skor akhir dan Top 5 tidak dihitung di Tugas 2.

## Keterbatasan

- IMK adalah proxy manufaktur mikro/kecil, bukan seluruh UMKM.
- Pedagang pasar adalah proxy retail tradisional, bukan seluruh retail.
- QRIS merchant per kabupaten/kota tidak tersedia publik.
- UMKM binaan hanya level provinsi dan hanya mencakup UMKM yang difasilitasi Dinkop.
- Filter mengeluarkan 4 dari 6 kota, sehingga hasil lebih representatif untuk kabupaten.
- Data cross-sectional 2023-2024 tidak mendukung inferensi kausal.
