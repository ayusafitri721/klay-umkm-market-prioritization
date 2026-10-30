from pathlib import Path

import pandas as pd
from fpdf import FPDF, XPos, YPos
from PIL import Image

ROOT = Path(".")
FIG = ROOT / "figures"
OUT = ROOT / "report" / "Tugas2_DS_Kelompok13.pdf"

clean = pd.read_csv(ROOT / "data/processed/master_clean.csv")
elim = pd.read_csv(ROOT / "data/processed/wilayah_tereliminasi.csv")
umkm = pd.read_csv(ROOT / "data/processed/provinsi_umkm_series.csv")

NAVY = (22, 58, 92)
GREY = (90, 90, 90)
LIGHT = (235, 242, 248)


class Report(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*GREY)
        self.cell(0, 5, "Tugas 2 - Milestone 1 Final Project | Klay - Market Prioritization UMKM",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        self.set_draw_color(200, 210, 220)
        self.line(15, 18, 195, 18)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_font("DejaVu", "", 7.5)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Halaman {self.page_no()}", align="C")


pdf = Report(format="A4")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.set_margins(15, 15, 15)


def h1(text):
    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 13.5)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 7.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def h2(text):
    pdf.set_font("DejaVu", "B", 10.5)
    pdf.set_text_color(40, 70, 100)
    pdf.multi_cell(0, 6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(0.5)


def para(text, size=9.3, color=(0, 0, 0)):
    pdf.set_font("DejaVu", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, 5.2, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, wrapmode="WORD")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(0.8)


def bullet(text, size=9.3):
    pdf.set_font("DejaVu", "", size)
    pdf.multi_cell(0, 5.2, "-  " + text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, wrapmode="WORD")
    pdf.ln(0.2)


def note(text):
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 4.6, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, wrapmode="CHAR")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)


def table(headers, rows, widths, font_size=7.6, align="LEFT"):
    pdf.set_font("DejaVu", "", font_size)
    with pdf.table(col_widths=widths, text_align=align, line_height=4.6,
                   borders_layout="ALL", first_row_as_headings=True) as t:
        r = t.row()
        for h in headers:
            r.cell(h)
        for row in rows:
            r = t.row()
            for c in row:
                r.cell(str(c))
    pdf.ln(2)


def figure(path, caption, width=170):
    img = Image.open(path)
    w, h = img.size
    display_h = width * h / w
    if pdf.get_y() + display_h + 10 > 270:
        pdf.add_page()
    pdf.image(str(path), x=(210 - width) / 2, w=width)
    pdf.set_font("DejaVu", "", 7.8)
    pdf.set_text_color(*GREY)
    pdf.multi_cell(0, 4.5, caption, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


# ------------------------------------------------------------------ cover
pdf.add_page()
pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, 210, 52, "F")
pdf.set_y(18)
pdf.set_font("DejaVu", "B", 19)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 9, "Tugas 2 - Milestone 1 Final Project", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("DejaVu", "", 11)
pdf.cell(0, 7, "Market Prioritization UMKM", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 7, "Wilayah Target Sourcing Leads B2B SaaS", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_y(72)
pdf.set_text_color(0, 0, 0)
pdf.set_font("DejaVu", "B", 13)
pdf.cell(0, 8, "Skalar Solutions - Klay", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("DejaVu", "", 10)
pdf.cell(0, 6, "POS + AI Sales Analytics untuk UMKM", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_y(100)
pdf.set_font("DejaVu", "", 10)
pdf.cell(0, 6, "Kelompok: 13", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)
pdf.set_font("DejaVu", "B", 9.5)
pdf.cell(0, 5, "Anggota dan pembagian tugas", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("DejaVu", "", 9.5)
for line in [
    "1. [Nama 1] - Data collection & data understanding",
    "2. [Nama 2] - Data preparation & merging",
    "3. [Nama 3] - EDA, visualisasi & rancangan bobot ICP",
]:
    pdf.cell(0, 5.5, line, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_y(160)
pdf.set_font("DejaVu", "", 9)
pdf.set_text_color(*GREY)
pdf.multi_cell(0, 5, "Studi kasus: 35 kabupaten/kota Provinsi Jawa Tengah\n"
                     "Periode data: 2023-2024 (time series UMKM 2019-2024)\n"
                     "Tanggal: 30 Oktober 2026",
               align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(0, 0, 0)

pdf.set_y(205)
pdf.set_fill_color(*LIGHT)
pdf.rect(25, 205, 160, 42, "F")
pdf.set_y(211)
pdf.set_font("DejaVu", "", 8.5)
pdf.multi_cell(150, 4.8,
               "Dokumen ini merangkum proses data collection, data preparation, EDA, "
               "dan rancangan bobot ICP. Notebook pendukung dieksekusi tanpa error dan "
               "seluruh figur dihasilkan ulang dari notebook tersebut.",
               align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ------------------------------------------------------------- executive
pdf.add_page()
h1("1. Ringkasan Eksekutif")
para("Klay menjual POS + AI Sales Analytics ke UMKM. Untuk memprioritaskan wilayah sourcing "
     "leads, kami menyusun kerangka Indeks Calon Pelanggan (ICP) pada 35 kabupaten/kota "
     "Jawa Tengah. Data berasal dari empat sumber publik BPS dan Dinkop Jateng (2023-2024). "
     "Setelah pembersihan dan filter kualitas data, 30 wilayah lolos dan siap dianalisis.")
bullet("Kabupaten Banyumas, Cilacap, Kebumen, Purbalingga, dan Pemalang memimpin jumlah unit IMK, "
       "tetapi kepadatan IMK tidak otomatis sejalan dengan PDRB per kapita (korelasi -0,30).")
bullet("Kota Surakarta dan Kota Semarang unggul pada kepadatan pedagang pasar, IPM, PDRB, dan "
       "simpanan per kapita. Keduanya adalah segmen siap digital dengan daya beli tinggi.")
bullet("Kabupaten dengan IMK padat tetapi PDRB/IPM menengah (Kebumen, Wonosobo, Banjarnegara) "
       "adalah pasar volume besar dengan gap digitalisasi yang justru menjadi peluang Klay.")
bullet("Rancangan bobot ICP: Ukuran Pasar 25%, Kepadatan Sektor Target 25%, Kesiapan Digital 20%, "
       "Adopsi Pembayaran Digital 15%, Aktivitas Ekonomi 15%.")

h2("1.1 Ruang lingkup")
para("Sesuai instruksi Tugas 2, pekerjaan berhenti pada perancangan bobot ICP. K-Means, skor "
     "indeks akhir, penentuan Top 5, dan uji sensitivitas bobot tidak dihitung di sini; "
     "bagian tersebut menjadi rencana milestone berikutnya.")
para("Output utama: notebook Tugas2_DS_Kelompok13.ipynb yang tereksekusi, dataset mentah dan "
     "bersih di data/processed, sembilan figur EDA di figures, dan laporan ini.")

# ------------------------------------------------------------- collection
h1("2. Data Collection & Data Understanding")
h2("2.1 Sumber data")
table(
    ["No", "Sumber", "Level", "Kolom kunci", "Keterbatasan"],
    [
        ["1", "BPS Jateng, Provinsi Jawa Tengah Dalam Angka 2025",
         "Kab/kota (35)", "IMK 2023; PDRB 2024; sarana perdagangan 2024; simpanan/tabungan 2024",
         "PDF; nama wilayah tidak membedakan kabupaten/kota; watermark dan sel en dash"],
        ["2", "BPS Jateng, Penduduk menurut Kabupaten/Kota 2024",
         "Kab/kota (35)", "kode wilayah, jumlah penduduk, kepadatan",
         "Satu tahun; proyeksi penduduk"],
        ["3", "BPS Jateng, IPM menurut Kabupaten/Kota 2024",
         "Kab/kota (35)", "IPM, pengeluaran per kapita, indikator pendidikan/kesehatan",
         "IPM agregat; bukan literasi digital langsung"],
        ["4", "Dinkop Jateng, Jumlah UMKM Binaan 2019-2024",
         "Provinsi", "tahun, jumlah UMKM binaan",
         "Hanya UMKM binaan; 2024 baru s.d. TW II"],
    ],
    [8, 47, 23, 52, 50],
)
note("Link akses: BPS Jateng - https://jateng.bps.go.id/id/publication/2025/02/28/"
     "6f9ad30e8755ed2b706cb979/provinsi-jawa-tengah-dalam-angka-2025.html ; "
     "Penduduk - https://data.jatengprov.go.id/dataset/79a-penduduk-laju-pertumbuhan-penduduk-"
     "distribusi-persentase-penduduk-kepadatan-penduduk-rasio-jenis ; "
     "IPM - https://data.jatengprov.go.id/dataset/6c4-indeks-pembangunan-manusia-ipm-menurut-"
     "kabupaten-kota ; UMKM - https://data.jatengprov.go.id/dataset/7e5-jumlah-umkm-binaan-jawa-tengah")

h2("2.2 Definisi operasional dan limitasi")
para("IMK adalah Industri Mikro dan Kecil, yaitu unit usaha manufaktur berskala mikro/kecil. "
     "IMK dipakai sebagai proxy kepadatan sektor target, bukan total UMKM. Pedagang pasar adalah "
     "pedagang yang berjualan di pasar rakyat, proxy retail/F&B tradisional. Sarana perdagangan "
     "mencakup pasar, supermarket, dan pedagang pasar, bukan seluruh kanal retail modern. "
     "UMKM binaan adalah UMKM yang difasilitasi Dinkop Jateng, bukan populasi seluruh UMKM.")
para("Keterbatasan utama: total UMKM per kabupaten/kota tidak tersedia seragam; QRIS merchant per "
     "kabupaten/kota tidak tersedia publik; data UMKM binaan hanya level provinsi; dan sebagian "
     "tabel BPS hanya tersedia dalam PDF sehingga memerlukan ekstraksi dan validasi manual.")

# ------------------------------------------------------------- preparation
h1("3. Data Preparation")
h2("3.1 Pembersihan data")
para("Tahapan pembersihan yang dilakukan:")
bullet("Ekstraksi tabel PDF dengan pdfplumber, lalu membersihkan angka dari watermark dan pemisah ribuan.")
bullet("Mengganti nama wilayah hasil ekstraksi dengan nama kanonik dari file penduduk berdasarkan "
       "urutan 35 wilayah dan kode wilayah (3301-3329 kabupaten, 3371-3376 kota).")
bullet("Mengisi sel en dash pada tabel sarana perdagangan dengan 0, karena tanda tersebut berarti "
       "tidak ada outlet, bukan data hilang.")
bullet("Memeriksa duplikat dan missing pada level kode dan nama wilayah; memastikan seluruh kolom "
       "numerik bertipe angka.")
para("Hasil validasi: 35 baris, 35 wilayah unik, 0 duplikat, 0 missing. Tidak ada nilai negatif "
     "yang tidak wajar.")

h2("3.2 Merging lintas level")
para("Data kabupaten/kota digabung dengan kode wilayah dan nama wilayah sebagai kunci. Data provinsi "
     "(time series UMKM binaan) tidak di-join secara aditif karena level agregasinya berbeda. "
     "Yang dilakukan adalah broadcast satu kolom konteks, yaitu pertumbuhan UMKM binaan 2023 "
     "(3,02%), ke seluruh kabupaten/kota. Kolom ini dipakai sebagai konteks, bukan tambahan kuantitas.")
para("Mengapa tidak dijumlahkan: total UMKM binaan provinsi 2023 adalah 186.024, sedangkan total "
     "unit IMK 35 kabupaten/kota adalah 862.926. Keduanya mengukur populasi berbeda, sehingga "
     "penjumlahan akan menyesatkan. Perbedaan definisi ini dicatat sebagai limitasi.")

h2("3.3 Kriteria penggugur")
para("Filter dipakai untuk membuang wilayah yang terlalu kecil atau ekstrem agar segmentasi tidak "
     "didominasi outlier. Kriteria: (1) data kunci kosong; (2) skala terlalu kecil, yaitu IMK < "
     "10.000 unit; (3) outlier kepadatan, yaitu IMK per 100.000 penduduk > Q3 + 1,5 x IQR. "
     "Ambang 10.000 dipilih agar kota-kota kecil dengan basis manufaktur tipis keluar, tetapi "
     "wilayah dengan basis memadai tetap lolos.")
para(f"Hasil: {len(elim)} wilayah gugur dan {len(clean)} wilayah lolos (di atas syarat minimal 20). "
     "Daftar wilayah gugur:")
table(
    ["Wilayah", "Tipe", "IMK (unit)", "IMK/100k", "Alasan"],
    [[r.wilayah, r.tipe, f"{r.imk_unit:,.0f}", f"{r.imk_per_100k:,.0f}", r.alasan_gugur]
     for r in elim.itertuples()],
    [48, 27, 25, 25, 55],
)
para("Filter ini secara tidak proporsional mengeluarkan kota-kota kecil. Dari enam kota, hanya Kota "
     "Semarang dan Kota Surakarta yang lolos. Ini adalah trade-off yang disadari: fokus pada wilayah "
     "dengan basis sektor cukup besar, sementara analisis kota kecil perlu dilakukan terpisah.")

h2("3.4 Normalisasi Min-Max")
para("Normalisasi dilakukan pada 30 wilayah yang lolos dengan rumus x' = (x - min) / (max - min). "
     "Fitur yang dinormalisasi mewakili lima komponen ICP: penduduk, IMK per 100k, pedagang per 100k, "
     "IPM, pengeluaran per kapita, simpanan per kapita, tabungan per kapita, dan PDRB per kapita. "
     "Seluruh hasil berada pada rentang 0-1.")
para("Catatan: Min-Max sensitif terhadap outlier. Setelah filter, simpanan per kapita masih sangat "
     "miring karena didominasi Kota Semarang. Pada milestone berikutnya perlu dipertimbangkan "
     "log-transform atau winsorization sebelum scoring.")

# ------------------------------------------------------------- EDA
pdf.add_page()
h1("4. Exploratory Data Analysis")
para("EDA dilakukan pada 30 wilayah yang lolos. Fokusnya memetakan variasi antarwilayah dan mencari "
     "kombinasi indikator yang relevan untuk ICP Klay, bukan inferensi kausal.")

h2("4.1 Sebaran jumlah unit IMK")
figure(FIG / "fig1_imk_distribution.png",
       "Gambar 1. Sebaran jumlah unit IMK 2023 pada 30 wilayah yang lolos filter.")
para("Distribusi jumlah IMK sangat timpang. Banyumas, Cilacap, Kebumen, Purbalingga, dan Pemalang "
     "masing-masing memiliki lebih dari 42 ribu unit, sedangkan wilayah lain jauh lebih kecil. "
     "Lima wilayah ini adalah pasar volume untuk paket dasar POS, tetapi belum tentu paling siap "
     "digital. Prioritas sebaiknya mempertimbangkan kepadatan relatif dan kesiapan digital, bukan "
     "hanya jumlah absolut.")

h2("4.2 Kepadatan IMK menurut tipe wilayah")
figure(FIG / "fig2_boxplot_imk_density.png",
       "Gambar 2. Kepadatan IMK per 100.000 penduduk menurut tipe wilayah (n=28 kabupaten, n=2 kota).")
para("Kabupaten memiliki rata-rata unit IMK jauh lebih besar (26.892 vs 13.612), tetapi kepadatan "
     "per 100 ribu penduduk juga lebih tinggi (2.307 vs 1.510). Kota yang lolos justru unggul pada "
     "kepadatan pedagang pasar, PDRB, dan IPM. Profil risiko dan pendekatan akuisisi berbeda: "
     "kabupaten cocok untuk penetrasi volume manufaktur/retail tradisional, kota cocok untuk merchant "
     "yang sudah siap digital dan bertransaksi lebih tinggi.")

pdf.add_page()
h2("4.3 PDRB per kapita vs kepadatan pedagang pasar")
figure(FIG / "fig3_pdrb_vs_pedagang.png",
       "Gambar 3. Hubungan PDRB per kapita 2024 dan pedagang pasar per 100.000 penduduk.")
para("Korelasi positif sedang (r = 0,42). Wilayah dengan aktivitas ekonomi tinggi cenderung memiliki "
     "ekosistem pedagang pasar yang padat. Kota Surakarta adalah outlier positif: PDRB tinggi dan "
     "kepadatan pedagang sangat tinggi. Sebaliknya, beberapa kabupaten berpendapatan rendah tetap "
     "memiliki kepadatan pedagang tinggi (Kebumen, Temanggung, Purworejo), menandakan aktivitas retail "
     "tradisional besar tetapi daya beli belum tinggi. Wilayah seperti ini cocok untuk paket hemat dan "
     "edukasi digital.")

h2("4.4 IPM vs kepadatan IMK")
figure(FIG / "fig4_ipm_vs_imk.png",
       "Gambar 4. Hubungan IPM 2024 dan kepadatan IMK per 100.000 penduduk.")
para("Korelasinya negatif lemah (r = -0,30). Kabupaten dengan IMK padat (Purbalingga, Temanggung, "
     "Kebumen, Batang) justru memiliki IPM menengah, bukan tertinggi. Ini adalah gap yang menarik: "
     "basis usaha besar, tetapi kesiapan digital belum matang. Klay dapat memposisikan diri sebagai "
     "alat bantu adopsi digital, bukan sekadar POS. Sebaliknya, kota dengan IPM tinggi tetapi IMK "
     "rendah lebih cocok untuk produk analytics yang sudah advanced.")

pdf.add_page()
h2("4.5 Peta prioritas awal (multivariat)")
figure(FIG / "fig5_multivariate_bubble.png",
       "Gambar 5. PDRB vs kepadatan IMK; ukuran gelembung = populasi, warna = IPM 2024.")
para("Empat kuadran memberi arah strategi. Kanan atas (PDRB tinggi, IMK padat) adalah wilayah siap "
     "scale untuk paket lengkap. Kiri atas (PDRB rendah, IMK padat) adalah volume besar dengan daya "
     "beli terbatas, cocok untuk paket hemat dan onboarding intensif. Kanan bawah (PDRB tinggi, IMK "
     "rendah) adalah ekonomi jasa/perdagangan, prospek merchant retail. Kiri bawah (keduanya rendah) "
     "menjadi prioritas rendah untuk sourcing awal. Kota Semarang dan Surakarta berada di kanan dengan "
     "IPM tinggi, sedangkan Kebumen, Wonosobo, dan Banjarnegara berada di kiri atas dengan populasi "
     "besar dan IPM menengah.")

pdf.add_page()
h2("4.6 Profil komponen ICP")
figure(FIG / "fig6_heatmap_komponen.png",
       "Gambar 6. Z-score lima komponen ICP pada 15 wilayah dengan kepadatan sektor tertinggi.")
para("Wilayah dengan kepadatan sektor tinggi tidak seragam pada komponen lain. Sebagian unggul di "
     "ukuran pasar tetapi lemah di adopsi digital; sebagian lain seimbang. Untuk Klay, kombinasi "
     "kepadatan sektor tinggi dan kesiapan digital menengah adalah target paling efisien: kebutuhan "
     "nyata, tetapi belum terlalu matang sehingga masih ada ruang untuk value proposition POS/AI.")

pdf.add_page()
h2("4.7 Tren UMKM binaan provinsi")
figure(FIG / "fig7_umkm_series.png",
       "Gambar 7. Jumlah UMKM binaan Provinsi Jawa Tengah, 2019-2024 (2024 s.d. TW II).")
para("Populasi UMKM binaan tumbuh konsisten 3-4% per tahun (CAGR 2019-2023 = 3,6%). Angka 2024 baru "
     "mencakup TW II, jadi tidak sebanding dengan tahun penuh. Pertumbuhan yang stabil menandakan "
     "pasar sourcing yang terus bertambah, tetapi Klay perlu prioritas berbasis kualitas wilayah, "
     "bukan hanya mengejar volume.")

pdf.add_page()
h2("4.8 Komposisi sarana perdagangan")
figure(FIG / "fig8_retail_mix.png",
       "Gambar 8. Komposisi pasar dan supermarket pada 15 wilayah dengan pedagang pasar terbanyak.")
para("Hampir seluruh ekosistem retail di wilayah terpilih berbasis pasar rakyat; supermarket hanya "
     "sebagian kecil. Ini memperkuat tesis bahwa pasar tradisional dan pedagangnya adalah segmen utama "
     "Klay, bukan hanya retail modern. Wilayah dengan pedagang pasar banyak tetapi supermarket sedikit "
     "(mis. Kebumen, Kendal) memiliki ketergantungan tinggi pada transaksi tunai, sehingga menjadi "
     "peluang untuk edukasi pembayaran digital dan pencatatan penjualan.")

# ------------------------------------------------------------- ICP
pdf.add_page()
h1("5. Rancangan Bobot Indeks Calon Pelanggan (ICP)")
para("Bobot disusun dari lima komponen yang mencerminkan kesesuaian produk, kemampuan bayar, dan "
     "kemudahan akuisisi. Total bobot = 100%.")
table(
    ["Komponen", "Indikator", "Arah", "Bobot", "Justifikasi"],
    [
        ["Ukuran Pasar", "Jumlah penduduk; jumlah pedagang pasar", "+", "25%",
         "Volume merchant dan transaksi menentukan potensi revenue; Klay memonetisasi per outlet."],
        ["Kepadatan Sektor Target", "IMK/100k; pedagang pasar/100k", "+", "25%",
         "F&B, retail, dan jasa adalah pengguna utama POS; kepadatan tinggi menurunkan biaya akuisisi."],
        ["Kesiapan Digital", "IPM; pengeluaran per kapita", "+", "20%",
         "Literasi dan daya beli menurunkan biaya onboarding serta churn."],
        ["Adopsi Pembayaran Digital", "Simpanan per kapita; tabungan per kapita", "+", "15%",
         "Proxy kebiasaan nontunai dan akses keuangan; QRIS ideal tetapi belum tersedia per kab/kota."],
        ["Aktivitas Ekonomi", "PDRB per kapita", "+", "15%",
         "Intensitas bisnis dan kemampuan bayar menentukan kesediaan berlangganan."],
    ],
    [32, 52, 10, 13, 73],
    font_size=7.2,
)
figure(FIG / "fig9_bobot_icp.png",
       "Gambar 9. Rancangan bobot ICP Klay; total 100%.", width=150)

h2("5.1 Formula skor (rancangan, belum dihitung)")
para("ICP(i) = 0,25 U(i) + 0,25 K(i) + 0,20 D(i) + 0,15 A(i) + 0,15 E(i), dengan U = Ukuran Pasar, "
     "K = Kepadatan Sektor Target, D = Kesiapan Digital, A = Adopsi Pembayaran Digital, dan "
     "E = Aktivitas Ekonomi. Semua komponen berada pada 0-1, sehingga ICP juga 0-1. Skor akhir, "
     "peringkat, Top 5, dan uji sensitivitas bobot tidak dihitung di Tugas 2.")

h2("5.2 Rasional pembobotan")
bullet("Ukuran Pasar (25%) dan Kepadatan Sektor Target (25%) mendapat bobot terbesar karena keduanya "
       "paling langsung menentukan jumlah leads dan potensi revenue.")
bullet("Kesiapan Digital (20%) lebih tinggi dari adopsi/aktivitas karena Klay adalah produk software: "
       "wilayah dengan literasi dan daya beli lebih baik lebih murah di-onboard dan lebih kecil churn.")
bullet("Adopsi Pembayaran Digital (15%) penting, tetapi datanya hanya proxy simpanan/tabungan, bukan "
       "QRIS merchant. Bobotnya dibatasi agar tidak mendominasi.")
bullet("Aktivitas Ekonomi (15%) memberi sinyal daya beli, tetapi PDRB per kapita tidak secara langsung "
       "mengukur kesiapan adopsi software.")

# ------------------------------------------------------------- conclusion
pdf.add_page()
h1("6. Kesimpulan dan Keterbatasan")
h2("6.1 Kesimpulan")
bullet("Data 35 kabupaten/kota berhasil digabung dari empat sumber publik dengan kunci wilayah yang "
       "konsisten; tidak ada missing atau duplikat pada data mentah.")
bullet("Setelah filter transparan, 30 wilayah siap dianalisis. Lima wilayah gugur: Kabupaten Pekalongan "
       "(outlier kepadatan IMK) serta Kota Magelang, Kota Salatiga, Kota Pekalongan, dan Kota Tegal "
       "(basis IMK < 10.000 unit).")
bullet("EDA menunjukkan dua klaster besar: kabupaten berbasis manufaktur/retail tradisional dengan "
       "volume besar tetapi IPM/PDRB menengah, dan kota berbasis jasa/perdagangan dengan IPM/PDRB "
       "tinggi tetapi basis IMK lebih kecil.")
bullet("Rancangan bobot ICP memberi prioritas seimbang pada ukuran pasar dan kepadatan sektor (50% "
       "gabungan), dengan kesiapan digital sebagai faktor kualitas (20%), serta adopsi pembayaran dan "
       "aktivitas ekonomi sebagai pelengkap (30%).")
bullet("Wilayah dengan kepadatan sektor tinggi dan kesiapan digital menengah (mis. Kebumen, "
       "Purbalingga, Temanggung, Batang) adalah kandidat menarik untuk ekspansi berbasis volume dan "
       "edukasi digital; kota besar (Semarang, Surakarta) lebih cocok untuk paket advanced.")

h2("6.2 Keterbatasan")
bullet("Proxy sektor: IMK hanya mencakup industri manufaktur mikro/kecil, bukan seluruh UMKM. Pedagang "
       "pasar hanya mencakup pedagang di pasar rakyat, bukan seluruh retail.")
bullet("Data adopsi digital: QRIS merchant per kabupaten/kota tidak tersedia publik; simpanan/tabungan "
       "per kapita hanya proxy tidak langsung.")
bullet("Level agregasi: UMKM binaan hanya tersedia di level provinsi dan hanya mencakup UMKM yang "
       "difasilitasi Dinkop, bukan total UMKM.")
bullet("Filter: ambang 10.000 unit IMK mengeluarkan empat dari enam kota, sehingga hasil lebih "
       "representatif untuk kabupaten. Analisis kota kecil perlu dilakukan terpisah.")
bullet("Desain cross-sectional: data 2023-2024 tidak memungkinkan inferensi kausal atau tren jangka "
       "panjang per wilayah.")
bullet("Normalisasi: Min-Max sensitif terhadap outlier. Simpanan per kapita masih sangat miring "
       "(didominasi Kota Semarang), sehingga perlu log-transform atau winsorization pada milestone "
       "berikutnya.")

h2("6.3 Rencana milestone berikutnya")
bullet("Finalisasi fitur dan uji sensitivitas bobot ICP.")
bullet("Segmentasi wilayah dengan K-Means (jumlah klaster diuji dengan elbow/silhouette).")
bullet("Perhitungan skor akhir dan penentuan Top 5 wilayah.")
bullet("Validasi eksternal (mis. data QRIS atau survei lapangan) bila tersedia.")

# ------------------------------------------------------------- appendix
pdf.add_page()
h1("Lampiran")
h2("A. Struktur deliverable")
table(
    ["Path", "Isi"],
    [
        ["Tugas2_DS_Kelompok13.ipynb", "Notebook utama, tereksekusi tanpa error"],
        ["data/raw/", "PDF BPS, XLSX penduduk/IPM/UMKM"],
        ["data/processed/master_raw.csv", "Dataset gabungan 35 wilayah sebelum filter"],
        ["data/processed/master_clean.csv", "Dataset 30 wilayah setelah filter + normalisasi"],
        ["data/processed/wilayah_tereliminasi.csv", "Daftar 5 wilayah gugur dan alasannya"],
        ["data/processed/provinsi_umkm_series.csv", "Time series UMKM binaan 2019-2024"],
        ["figures/", "Sembilan figur EDA dan bobot ICP"],
        ["scripts/build_dataset.py", "Skrip ekstraksi dan pembentukan dataset"],
        ["scripts/make_notebook.py", "Generator notebook"],
        ["scripts/make_report.py", "Generator laporan PDF"],
    ],
    [78, 102],
    font_size=7.6,
)
h2("B. Cara menjalankan ulang")
para("1. Install dependensi: pandas, numpy, matplotlib, seaborn, scikit-learn, pdfplumber, "
     "nbformat, nbconvert, fpdf2.")
para("2. Letakkan raw data di data/raw (lihat README).")
para("3. Jalankan python scripts/build_dataset.py untuk membentuk ulang dataset.")
para("4. Jalankan jupyter nbconvert --to notebook --execute --inplace Tugas2_DS_Kelompok13.ipynb.")
para("5. Jalankan python scripts/make_report.py untuk menghasilkan laporan PDF.")
note("Catatan: lengkapi nama anggota sebelum submit. ZIP akhir: "
     "Tugas2_DS_Kelompok13.zip")

pdf.output(str(OUT))
print("Laporan ditulis:", OUT)
