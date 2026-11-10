"""Build the Final Project report PDF."""
from pathlib import Path

import pandas as pd
from fpdf import FPDF, XPos, YPos
from fpdf.enums import TableCellFillMode
from fpdf.fonts import FontFace
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
FIG = ROOT / "figures"
OUT = ROOT / "report" / "FinalProject_DS_Kelompok13.pdf"

master = pd.read_csv(DATA / "master_final.csv")
segments = pd.read_csv(DATA / "segments_final.csv")
top5 = pd.read_csv(DATA / "top5_segments.csv")
profile = pd.read_csv(DATA / "cluster_profile.csv")
baseline = pd.read_csv(DATA / "baseline_comparison.csv")
sens = pd.read_csv(DATA / "sensitivity_scenarios.csv")
scraping = pd.read_csv(DATA / "scraping_legality.csv")
sdr = pd.read_csv(DATA / "sdr_strategy.csv")
evaluation = pd.read_csv(DATA / "kmeans_evaluation.csv")

NAVY = (23, 58, 94)
TEAL = (44, 122, 140)
TEXT = (31, 41, 51)
CAPTION = (95, 107, 118)
LINE = (201, 211, 220)
LIGHT = (238, 244, 248)
CREAM = (255, 246, 229)
ORANGE = (224, 164, 58)
RED = (170, 70, 60)

CONTENT_W = 210 - 44
LINE_H = 5.3
PARA_GAP = 2.4
HEADER = "Final Project – Market Prioritization UMKM | Klay | Kelompok 13"


def fmt_int(value):
    return f"{value:,.0f}".replace(",", ".")


def fmt_dec(value, digits=2):
    return f"{value:.{digits}f}".replace(".", ",")


class Report(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVuSans", "", 7.2)
        self.set_text_color(*CAPTION)
        self.set_xy(self.l_margin, 11)
        self.cell(0, 4, HEADER, align="L")
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, 17, self.w - self.r_margin, 17)
        self.set_xy(self.l_margin, self.t_margin)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-11)
        self.set_font("DejaVuSans", "", 7.2)
        self.set_text_color(*CAPTION)
        self.set_x(self.l_margin)
        self.cell(0, 4, "Kelompok 13", align="L")
        self.set_xy(self.w - self.r_margin - 30, self.h - 11)
        self.cell(30, 4, f"Halaman {self.page_no()}", align="R")


pdf = Report(format="A4")
pdf.set_margins(22, 22, 22)
pdf.set_auto_page_break(auto=True, margin=19)
pdf.add_font("DejaVuSans", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVuSans", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.add_font("DejaVuSerif", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.add_font("DejaVuSerif", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
pdf.add_font("DejaVuMono", "", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
pdf.set_title("Final Project – Market Prioritization UMKM")
pdf.set_author("Kelompok 13")
pdf.set_subject("Data Science Final Project – Klay")


def ensure_space(height):
    if pdf.get_y() + height > pdf.h - pdf.b_margin:
        pdf.add_page()


def text_height(text, width, family="DejaVuSans", style="", size=9.5, line_h=LINE_H, markdown=False):
    pdf.set_font(family, style, size)
    return pdf.multi_cell(width, line_h, text, dry_run=True, output="HEIGHT", markdown=markdown)


def h1(text, new_page=False):
    if new_page:
        pdf.add_page()
    ensure_space(31)
    pdf.set_font("DejaVuSans", "B", 15.5)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 8, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    y = pdf.get_y() + 1
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.set_line_width(0.3)
    pdf.ln(3.5)


def h2(text):
    ensure_space(23)
    pdf.set_font("DejaVuSans", "B", 11)
    pdf.set_text_color(*TEAL)
    pdf.multi_cell(0, 6, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)


def para(text, size=9.5, color=TEXT, gap=PARA_GAP, markdown=False):
    pdf.set_font("DejaVuSans", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, LINE_H, text, align="L", wrapmode="WORD", new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=markdown)
    pdf.ln(gap)


def bullet_list(items, size=9.5, gap=PARA_GAP):
    for item in items:
        height = text_height(item, CONTENT_W - 5, "DejaVuSans", "", size, LINE_H, markdown=True)
        ensure_space(height + 1)
        y = pdf.get_y()
        pdf.set_font("DejaVuSans", "", size)
        pdf.set_text_color(*TEXT)
        pdf.set_xy(pdf.l_margin, y)
        pdf.cell(5, LINE_H, "•")
        pdf.set_xy(pdf.l_margin + 5, y)
        pdf.multi_cell(CONTENT_W - 5, LINE_H, item, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
    pdf.ln(gap)


def numbered_list(items, size=9.5, gap=PARA_GAP):
    for i, item in enumerate(items, 1):
        height = text_height(item, CONTENT_W - 8, "DejaVuSans", "", size, LINE_H, markdown=True)
        ensure_space(height + 1)
        y = pdf.get_y()
        pdf.set_font("DejaVuSans", "", size)
        pdf.set_text_color(*TEXT)
        pdf.set_xy(pdf.l_margin, y)
        pdf.cell(8, LINE_H, f"{i}.")
        pdf.set_xy(pdf.l_margin + 8, y)
        pdf.multi_cell(CONTENT_W - 8, LINE_H, item, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
    pdf.ln(gap)


def callout(title, items, bg=LIGHT, bar=TEAL, bullet=False, size=9.1):
    pad_x, pad_y = 4.0, 3.2
    inner_w = CONTENT_W - 2 * pad_x
    title_h = 5.2 if title else 0
    item_heights = [
        text_height(item, inner_w - (4 if bullet else 0), "DejaVuSans", "", size, 4.9, markdown=bullet)
        for item in items
    ]
    total = pad_y * 2 + title_h + sum(item_heights) + 1.4 * len(items)
    ensure_space(total + 2)
    x, y = pdf.l_margin, pdf.get_y()
    pdf.set_fill_color(*bg)
    pdf.rect(x, y, CONTENT_W, total, "F")
    pdf.set_fill_color(*bar)
    pdf.rect(x, y, 1.2, total, "F")
    pdf.set_xy(x + pad_x, y + pad_y)
    if title:
        pdf.set_font("DejaVuSans", "B", 9.6)
        pdf.set_text_color(*NAVY)
        pdf.cell(0, title_h, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVuSans", "", size)
    pdf.set_text_color(*TEXT)
    for item in items:
        pdf.set_x(x + pad_x + (4 if bullet else 0))
        if bullet:
            pdf.set_x(x + pad_x)
            pdf.cell(4, 4.9, "•")
            pdf.set_x(x + pad_x + 4)
        pdf.multi_cell(inner_w - (4 if bullet else 0), 4.9, item, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=bullet)
        pdf.ln(1.4)
    pdf.set_y(y + total + 3)


def table(headers, rows, widths, font_size=7.8):
    ensure_space(25)
    pdf.set_font("DejaVuSans", "", font_size)
    pdf.set_text_color(*TEXT)
    with pdf.table(
        col_widths=widths,
        text_align="LEFT",
        line_height=4.0,
        borders_layout="HORIZONTAL_LINES",
        first_row_as_headings=True,
        cell_fill_mode=TableCellFillMode.ROWS,
        cell_fill_color=LIGHT,
        headings_style=FontFace(emphasis="BOLD", size_pt=font_size, color=(255, 255, 255), fill_color=NAVY),
        padding=1.3,
    ) as t:
        r = t.row()
        for header in headers:
            r.cell(header)
        for row in rows:
            r = t.row()
            for cell in row:
                r.cell(str(cell))
    pdf.ln(2.5)


def figure(path, caption, width=148):
    img = Image.open(path)
    w, h = img.size
    display_h = width * h / w
    caption_h = text_height(caption, CONTENT_W, "DejaVuSans", "", 8.1, 4.3)
    ensure_space(display_h + caption_h + 7)
    pdf.image(str(path), x=(pdf.w - width) / 2, w=width)
    pdf.ln(1)
    pdf.set_font("DejaVuSans", "", 8.1)
    pdf.set_text_color(*CAPTION)
    pdf.multi_cell(0, 4.3, caption, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def link_line(text, url):
    pdf.set_font("DejaVuSans", "", 6.3)
    pdf.set_text_color(*TEAL)
    pdf.multi_cell(0, 3.5, text, link=url, align="L", wrapmode="WORD", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ------------------------------------------------------------------ cover
pdf.add_page()
pdf.set_auto_page_break(False)
pdf.set_y(27)
pdf.set_font("DejaVuSerif", "B", 11)
pdf.cell(0, 6, "FINAL PROJECT – DATA SCIENCE", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(35)

pdf.set_font("DejaVuSerif", "B", 19)
pdf.cell(0, 9, "DARI VOLUME KE KESIAPAN", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(10)
pdf.set_font("DejaVuSerif", "", 14)
pdf.cell(0, 7, "Segmentasi Wilayah dan Prioritisasi Leads UMKM", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(11)
pdf.set_font("DejaVuSerif", "", 12)
pdf.cell(0, 6.5, "Klay (Skalar Solutions) – POS + AI Sales Analytics", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(28)

pdf.set_font("DejaVuSerif", "", 10.8)
pdf.cell(0, 5.8, "Studi kasus: 30 kabupaten/kota Provinsi Jawa Tengah", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(5)
pdf.cell(0, 5.8, "Data: 2023–2024 | 90 segmen sektor × wilayah", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(38)

pdf.set_font("DejaVuSerif", "B", 13.5)
pdf.cell(0, 7, "Kelompok 13", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(14)
pdf.set_font("DejaVuSerif", "", 11.5)
for line in [
    "Ayu Safitri (2610501106)",
    "Carissa Zia W. F (2610514008)",
    "Gerard Harjuno N (2610512189)",
]:
    pdf.cell(0, 5.2, line, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
pdf.ln(34)
pdf.set_font("DejaVuSerif", "B", 12.5)
pdf.cell(0, 6.5, "Fakultas Ilmu Komputer", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(4)
pdf.cell(0, 6.5, "Universitas Pembangunan Nasional “Veteran” Jakarta", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ------------------------------------------------------------- executive
pdf.set_auto_page_break(True, margin=19)
h1("1. Ringkasan Eksekutif", new_page=True)
para(
    "Klay menjual POS dan AI Sales Analytics kepada UMKM. Pertanyaan investasi utamanya bukan "
    "“wilayah mana yang paling banyak usahanya?”, tetapi “segmen mana yang paling siap membeli, "
    "mengadopsi, dan bertahan?” Laporan ini menjawab pertanyaan tersebut dengan menyegmentasikan "
    "30 kabupaten/kota di Jawa Tengah dan memberi skor pada 90 segmen sektor × wilayah."
)
callout(
    "Temuan utama",
    [
        "**Top 5 segmen berada di Kota Semarang dan Kota Surakarta.** Kombinasi volume besar, "
        "kepadatan tinggi, IPM tinggi, dan adopsi keuangan digital membuat keduanya paling siap "
        "untuk pilot berbayar.",
        "**Volume bukan prioritas.** Baseline yang hanya mengurutkan jumlah unit menghasilkan Top 5 "
        "yang seluruhnya kabupaten dan seluruhnya Ritel; tidak ada satu pun yang beririsan dengan "
        "Top 5 ICP (overlap 0/5; Spearman ρ = 0,738).",
        "**Tiga tipe wilayah.** Hub Digital Matang (3 wilayah), Sentra Perdagangan Padat (14), dan "
        "Wilayah Rintisan (13). Masing-masing membutuhkan motion dan paket SDR yang berbeda.",
        "**Ritel mendominasi populasi.** Dari 1.021.062 unit target, 68,9% adalah Ritel, 22,4% F&B, "
        "dan 8,8% Jasa. Namun prioritas tetap ditentukan oleh kesiapan, bukan hanya ukuran.",
    ],
    bullet=True,
)
callout(
    "Rekomendasi inti",
    [
        "Jalankan pilot berbayar di Ritel dan F&B Kota Semarang serta Kota Surakarta.",
        "Pakai Sentra Perdagangan Padat sebagai mesin volume dengan POS basic dan onboarding.",
        "Perlakukan Wilayah Rintisan sebagai pipeline edukasi, bukan target volume jangka pendek.",
    ],
    bg=CREAM,
    bar=ORANGE,
    bullet=True,
)

# ------------------------------------------------------------- context
h1("2. Latar, Tujuan, dan Ruang Lingkup")
para(
    "Sebagai produk B2B SaaS, Klay perlu memilih wilayah dan segmen yang memberi rasio konversi "
    "terbaik terhadap biaya akuisisi. Tugas 2 sudah membangun kerangka ICP dan filter kualitas data, "
    "tetapi berhenti pada rancangan bobot. Final Project ini menutup tiga celah: (1) segmentasi "
    "wilayah dengan K-Means, (2) skor prioritas pada level sektor × wilayah, dan (3) uji ketahanan "
    "skor terhadap perubahan bobot."
)
para(
    "Ruang lingkup: 30 kabupaten/kota yang lolos filter kualitas, tiga sektor target (Ritel, F&B, "
    "Jasa), data cross-section 2023–2024, dan horizon rekomendasi satu sampai dua kuartal. Analisis "
    "tidak mengklaim kausalitas; hasil adalah prioritisasi berbasis data publik."
)
h2("2.1 Pertanyaan analisis")
numbered_list(
    [
        "Bagaimana mengelompokkan wilayah berdasarkan ukuran pasar, kepadatan sektor, kesiapan digital, adopsi digital, dan aktivitas ekonomi?",
        "Segmen sektor × wilayah mana yang paling diprioritaskan untuk sourcing leads?",
        "Seberapa berbeda prioritas ICP dibanding baseline volume?",
        "Seberapa sensitif Top 5 terhadap perubahan bobot?",
        "Sumber leads mana yang layak secara hukum dan etika untuk dipakai?",
    ]
)

# ------------------------------------------------------------- data
h1("3. Data dan Metodologi")
h2("3.1 Sumber data")
para(
    "Empat sumber publik dipakai. Tiga sumber pertama membangun konteks wilayah; sumber keempat "
    "memberi dimensi sektor yang tidak tersedia di Tugas 2."
)
table(
    ["Sumber", "Level & isi", "Peran dalam analisis"],
    [
        ["BPS Jateng, Provinsi Jawa Tengah Dalam Angka 2025", "Kab/kota; PDRB per kapita 2024, simpanan/tabungan, sarana perdagangan", "Aktivitas ekonomi, adopsi digital, konteks retail"],
        ["BPS Jateng, Penduduk 2024", "Kab/kota; jumlah penduduk dan kepadatan", "Denominator kepadatan sektor"],
        ["BPS Jateng, IPM 2024", "Kab/kota; IPM dan pengeluaran per kapita", "Kesiapan digital dan daya beli"],
        ["Dinkop Jateng, Pelaku Usaha per Lapangan Usaha 2024", "Kab/kota × 17 KBLI; 595 baris", "Jumlah unit Ritel, F&B, dan Jasa aktual"],
    ],
    [55, 58, 55],
    font_size=7.6,
)
link_line(
    "Sumber sektor: https://data.jatengprov.go.id/dataset/f23725ac-b792-4e7d-9506-0d16f392f6a4/resource/4e820490-c1fc-4b8e-b398-d9ff49caad45/download/jumlah-pelaku-usaha-berdasarkan-lapangan-usaha-hasil-pendataan-lengkap-koperasi-usaha-mikro-kec.xlsx",
    "https://data.jatengprov.go.id/dataset/f23725ac-b792-4e7d-9506-0d16f392f6a4/resource/4e820490-c1fc-4b8e-b398-d9ff49caad45/download/jumlah-pelaku-usaha-berdasarkan-lapangan-usaha-hasil-pendataan-lengkap-koperasi-usaha-mikro-kec.xlsx",
)
para(
    "Tiga kategori KBLI dipetakan ke sektor Klay: perdagangan besar/eceran menjadi Ritel; "
    "akomodasi dan makan/minum menjadi F&B; aktivitas jasa lainnya menjadi Jasa. Dataset ini "
    "mencakup pelaku usaha hasil pendataan Dinkop, bukan seluruh UMKM, sehingga tetap dibaca sebagai "
    "proxy populasi.",
    size=9.1,
)

h2("3.2 Pembersihan dan pembentukan segmen")
bullet_list(
    [
        "35 wilayah dibaca dari dataset sektor; kode wilayah diparse dari format desimal (33.10 → 3310) agar Klaten dan Jepara tidak hilang.",
        "Data sektor di-pivot menjadi tiga kolom sektor dan digabung ke master 30 wilayah yang lolos filter Tugas 2.",
        "Unit sektor dijumlahkan menjadi total target; kepadatan dihitung per 100.000 penduduk.",
        "Setiap wilayah × sektor menjadi satu segmen: 30 × 3 = 90 baris.",
    ]
)
para(
    "Total unit target: Ritel 703.132 (68,9%), F&B 228.270 (22,4%), dan Jasa 89.660 (8,8%). "
    "Ritel adalah pasar terbesar, tetapi F&B dan Jasa tetap dianalisis karena kepadatan dan "
    "kesiapan digitalnya berbeda."
)

h2("3.3 Komponen dan bobot ICP")
para(
    "Lima komponen dinormalisasi Min-Max. Bobot dipilih dari rancangan Tugas 2 dan tidak diubah "
    "setelah melihat hasil: Ukuran Pasar 25%, Kepadatan Sektor 25%, Kesiapan Digital 20%, Adopsi "
    "Digital 15%, dan Aktivitas Ekonomi 15%."
)
table(
    ["Komponen", "Indikator", "Bobot"],
    [
        ["Ukuran Pasar", "Total unit Ritel + F&B + Jasa", "25%"],
        ["Kepadatan Sektor", "Unit target per 100.000 penduduk", "25%"],
        ["Kesiapan Digital", "Rata-rata MinMax IPM dan pengeluaran per kapita", "20%"],
        ["Adopsi Digital", "Rata-rata MinMax simpanan dan tabungan per kapita", "15%"],
        ["Aktivitas Ekonomi", "PDRB per kapita 2024", "15%"],
    ],
    [42, 96, 30],
)

h2("3.4 K-Means dan skor segmen")
para(
    "K-Means dijalankan pada lima komponen wilayah dengan k = 2–6 untuk evaluasi, tetapi pemilihan "
    "dibatasi pada k = 3–5 sesuai ketentuan. k = 3 dipilih karena silhouette tertinggi di dalam "
    "rentang (0,390); k = 2 memang lebih tinggi (0,578) tetapi di luar rentang. Skor segmen "
    "menggabungkan komponen wilayah dengan volume dan kepadatan sektor yang dinormalisasi pada 90 "
    "segmen."
)
para(
    "Baseline hanya mengurutkan 90 segmen berdasarkan jumlah unit sektor. Perbandingan memakai "
    "overlap Top 5 dan Spearman ρ. Sensitivitas menggeser bobot digital, adopsi, dan PDRB sebesar "
    "±5–10 poin persentase, lalu menghitung ulang peringkat."
)

# ------------------------------------------------------------- results
h1("4. Hasil")
h2("4.1 Evaluasi klaster")
table(
    ["k", "Inertia", "Silhouette", "Catatan"],
    [
        ["2", "4,432", "0,578", "Di luar rentang wajib"],
        ["3", "2,540", "0,390", "Dipilih: tertinggi dalam rentang 3–5"],
        ["4", "2,062", "0,365", "Alternatif"],
        ["5", "1,623", "0,362", "Alternatif"],
        ["6", "1,230", "0,350", "Di luar rentang"],
    ],
    [15, 35, 35, 83],
)
para(
    "Tiga klaster cukup untuk memisahkan wilayah berdasarkan kesiapan digital dan ukuran pasar. "
    "Silhouette 0,390 menunjukkan struktur yang moderat, bukan pemisahan sempurna; karena itu label "
    "klaster dibaca sebagai tipe strategi, bukan taksonomi kaku."
)
figure(FIG / "final_elbow_silhouette.png", "Gambar 1. Elbow dan silhouette untuk pemilihan k. Garis putus-putus menandai k = 3.")

h2("4.2 Profil klaster")
table(
    ["Tipe wilayah", "Jumlah", "Ukuran", "Kepadatan", "Digital", "Adopsi", "Ekonomi"],
    [
        ["Hub Digital Matang", "3", "0,271", "0,318", "0,789", "0,694", "0,888"],
        ["Sentra Perdagangan Padat", "14", "0,641", "0,512", "0,223", "0,040", "0,103"],
        ["Wilayah Rintisan", "13", "0,209", "0,222", "0,318", "0,058", "0,134"],
    ],
    [52, 17, 19, 22, 19, 19, 20],
    font_size=7.5,
)
para(
    "Hub Digital Matang hanya berisi tiga wilayah (Kota Semarang, Kota Surakarta, Kudus), tetapi "
    "unggul jauh pada kesiapan digital, adopsi, dan aktivitas ekonomi. Sentra Perdagangan Padat "
    "adalah kutub volume: 14 kabupaten dengan ukuran dan kepadatan tinggi, tetapi adopsi digital "
    "sangat rendah. Wilayah Rintisan adalah pasar edukasi dengan volume dan digital di bawah kedua "
    "klaster lain."
)
figure(FIG / "final_clusters_pca.png", "Gambar 2. Peta klaster wilayah pada dua komponen utama (PCA). Ukuran titik mengikuti aktivitas ekonomi.", width=145)
figure(FIG / "final_cluster_profile.png", "Gambar 3. Profil rata-rata lima komponen per tipe wilayah.", width=150)

h2("4.3 Top 5 segmen")
rows = []
for _, r in top5.iterrows():
    rows.append(
        [
            int(r["Peringkat"]),
            r["Sektor"],
            r["Wilayah"],
            fmt_dec(r["Skor Prioritas"], 3),
            fmt_int(r["Estimasi Jumlah UMKM"]),
            fmt_int(r["Kepadatan per 100k"]),
            r["Tipe Wilayah"],
        ]
    )
table(
    ["#", "Sektor", "Wilayah", "Skor", "Unit", "Kepadatan", "Tipe wilayah"],
    rows,
    [10, 18, 31, 18, 20, 25, 46],
    font_size=7.7,
)
para(
    "Top 5 seluruhnya berada di Hub Digital Matang. Ritel Kota Semarang memimpin dengan skor "
    "0,657 dan 20.547 unit; F&B Kota Semarang mengikuti dengan 15.600 unit. Kota Surakarta masuk "
    "lewat Ritel dan F&B karena kepadatan sektornya lebih tinggi per penduduk, meskipun volume "
    "absolutnya lebih kecil. Jasa Kota Semarang melengkapi Top 5 dengan 6.925 unit."
)
callout(
    "Implikasi komersial",
    [
        "Kota Semarang adalah pasar akuisisi utama: volume besar, kepadatan tinggi, dan daya beli tertinggi.",
        "Kota Surakarta adalah pasar kepadatan: cocok untuk motion berbasis komunitas dan merchant padat.",
        "Konsentrasi Top 5 di tiga wilayah menandakan risiko konsentrasi; Banyumas, Purbalingga, dan Rembang adalah kandidat gelombang berikutnya.",
    ],
    bullet=True,
)
figure(FIG / "final_top5_segments.png", "Gambar 4. Lima segmen prioritas utama berdasarkan skor ICP.", width=150)

h2("4.4 Baseline volume vs skor ICP")
rows = []
for _, r in baseline.iterrows():
    rows.append(
        [
            int(r["Peringkat"]),
            f"{r['ICP_Sektor']} {r['ICP_Wilayah']}",
            fmt_dec(r["ICP_Skor"], 3),
            f"{r['Baseline_Sektor']} {r['Baseline_Wilayah']}",
            fmt_int(r["Baseline_Unit"]),
        ]
    )
table(
    ["#", "Top 5 ICP", "Skor", "Top 5 volume", "Unit"],
    rows,
    [10, 55, 25, 55, 23],
    font_size=7.6,
)
para(
    "Baseline didominasi Ritel di kabupaten: Banyumas (44.960), Tegal (39.767), Grobogan "
    "(39.264), Purbalingga (37.960), dan Cilacap (35.905). Tidak ada satu pun segmen yang sama "
    "dengan Top 5 ICP. Korelasi peringkat keduanya 0,738: arahnya positif, tetapi ujung distribusi "
    "berbeda karena baseline mengabaikan kesiapan digital dan kepadatan."
)
figure(FIG / "final_baseline.png", "Gambar 5. Peringkat ICP vs baseline volume. Titik oranye adalah Top 5 ICP; overlap 0/5.", width=148)

h2("4.5 Sensitivitas bobot")
rows = []
for _, r in sens.iterrows():
    rows.append(
        [
            r["Skenario"],
            f"{int(r['Overlap_Top5'])}/5",
            fmt_dec(r["Spearman_vs_Base"], 3),
            int(r["Segmen_Berubah_Peringkat"]),
        ]
    )
table(
    ["Skenario", "Overlap Top 5", "Spearman vs base", "Segmen berubah"],
    rows,
    [55, 34, 39, 40],
)
para(
    "Spearman ρ tetap di atas 0,97 pada semua skenario, tetapi overlap Top 5 turun dari 5/5 ke 3/5 "
    "saat bobot adopsi, PDRB, atau digital diturunkan. Artinya urutan besar cukup stabil, namun "
    "segmen batas (terutama F&B dan Jasa) sensitif terhadap asumsi bobot. Untuk keputusan kuartalan, "
    "tiga nama teratas relatif aman; posisi keempat dan kelima perlu divalidasi dengan data pipeline."
)
figure(FIG / "final_sensitivity.png", "Gambar 6. Uji sensitivitas bobot: jumlah segmen Top 5 yang tetap dan korelasi peringkat.", width=150)

# ------------------------------------------------------------- discussion
h1("5. Pembahasan dan Strategi Go-to-Market")
para(
    "Hasil menunjukkan bahwa pasar terbesar bukan otomatis pasar terbaik. Kabupaten dengan puluhan "
    "ribu unit Ritel memiliki volume, tetapi kesiapan digital dan daya beli lebih rendah. Klay "
    "menjual alat analitik yang membutuhkan data transaksi dan disiplin operasional; karena itu "
    "wilayah dengan IPM, adopsi simpanan, dan PDRB tinggi lebih mungkin mencapai time-to-value "
    "yang cepat."
)
h2("5.1 Tiga motion SDR")
table(
    ["Tier", "Target", "Profil", "Penawaran", "Channel"],
    [
        ["A", "Top 5: Ritel/F&B/Jasa Kota Semarang & Surakarta", "Adopsi digital tinggi; volume dan kepadatan tinggi", "Demo AI Sales Analytics; pilot 30 hari; integrasi POS", "Direct sales; komunitas merchant; referral"],
        ["B", "Ritel di 14 Sentra Perdagangan Padat", "Volume besar; adopsi rendah", "POS basic + onboarding; literasi digital", "Dinas/koperasi; komunitas pasar; agen lokal"],
        ["C", "Ritel/F&B di 13 Wilayah Rintisan", "Volume dan digital rendah", "Produk ringan; uji coba; edukasi", "Event UMKM; mitra lokal; konten"],
    ],
    [12, 48, 39, 39, 30],
    font_size=7.2,
)
para(
    "Tier A memakai sales-assisted motion karena nilai kontrak dan kompleksitas integrasi lebih "
    "tinggi. Tier B memakai channel partner dan komunitas untuk menekan CAC. Tier C memakai "
    "edukasi dan produk ringan; targetnya bukan revenue jangka pendek, melainkan pipeline dan "
    "brand presence."
)
h2("5.2 Target dan urutan eksekusi")
numbered_list(
    [
        "Kuartal 1: pilot 10–15 merchant Ritel/F&B di Kota Semarang; ukur activation, GMV per merchant, dan retensi 30 hari.",
        "Kuartal 1–2: replikasi pilot di Kota Surakarta dengan motion komunitas merchant padat.",
        "Kuartal 2: uji paket POS basic di 3–5 kabupaten Sentra Perdagangan Padat (Banyumas, Purbalingga, Rembang).",
        "Kuartal 3: bangun pipeline edukasi di Wilayah Rintisan; jangan paksakan target volume.",
        "Setiap kuartal: hitung ulang skor dengan data sektor dan adopsi terbaru; validasi posisi 4–5.",
    ]
)
callout(
    "Metrik yang harus dipantau",
    [
        "Conversion rate dari qualified lead ke pilot.",
        "Activation: merchant menyelesaikan onboarding dan transaksi pertama di POS.",
        "Retensi 30/90 hari dan fitur AI yang benar-benar dipakai.",
        "CAC payback per tier dan waktu ke nilai (time-to-value).",
    ],
    bg=CREAM,
    bar=ORANGE,
    bullet=True,
)

# ------------------------------------------------------------- scraping
h1("6. Legalitas dan Etika Sumber Leads")
para(
    "Sebelum melakukan scraping, kami memeriksa robots.txt dan ketentuan layanan calon sumber. "
    "Prinsipnya: hormati robots.txt, jangan melanggar ToS, jangan mengambil data pribadi tanpa "
    "dasar yang sah, dan gunakan API atau data partner bila tersedia. Pemeriksaan dilakukan pada "
    "2 November 2026; kebijakan dapat berubah."
)
rows = []
for _, r in scraping.iterrows():
    rows.append([r["Sumber"], r["Status_Robots"], r["Status_ToS"], r["Status_Kelayakan"], r["Rekomendasi"]])
table(
    ["Sumber", "robots.txt", "ToS", "Status", "Rekomendasi"],
    rows,
    [37, 24, 24, 22, 61],
    font_size=6.6,
)
para(
    "Google Maps, LinkedIn, Tokopedia, dan Shopee tidak layak di-scrape: ToS melarang, dan untuk "
    "Google Maps jalur yang sah adalah Places API berbayar. OpenStreetMap menyediakan bulk data "
    "planet.osm dengan lisensi ODbL; gunakan ekstrak resmi, bukan crawling situs. Portal Satu Data "
    "Dinkop mengizinkan akses robots.txt, tetapi tidak memberi izin scraping eksplisit; gunakan "
    "unduhan resmi dan batasi laju permintaan."
)
callout(
    "Rekomendasi akuisisi data",
    [
        "Untuk direktori merchant: gunakan Places API, data partner, atau opt-in merchant; jangan scrape.",
        "Untuk data publik sektor: gunakan portal Satu Data dan cantumkan atribusi.",
        "Untuk data sosial/profesional: jangan crawl; gunakan API resmi atau kemitraan.",
        "Simpan log sumber, tanggal akses, dan dasar penggunaan untuk audit internal.",
    ],
    bullet=True,
)

# ------------------------------------------------------------- limitations
h1("7. Limitasi")
bullet_list(
    [
        "**Cross-section.** Data 2023–2024 tidak menangkap perubahan musiman atau dampak kebijakan; hasil adalah potret, bukan ramalan.",
        "**Proxy digital.** IPM, pengeluaran, simpanan, dan tabungan bukan ukuran langsung literasi digital atau penggunaan POS.",
        "**Cakupan sektor.** Dataset Dinkop mencakup pelaku usaha hasil pendataan, bukan seluruh UMKM; unit Ritel/F&B/Jasa adalah proxy populasi.",
        "**Kepadatan.** Denominator memakai penduduk, bukan jumlah usaha aktif; wilayah dengan banyak usaha kecil per penduduk bisa terlihat lebih padat.",
        "**K-Means.** Silhouette moderat (0,390); label klaster adalah alat strategi, bukan kebenaran absolut.",
        "**Bobot.** Bobot dipilih sebelum melihat hasil, tetapi tetap mengandung judgment; sensitivitas menunjukkan posisi 4–5 rentan.",
        "**Scraping.** Tidak ada scraping yang dijalankan; tabel legalitas adalah kajian dokumen, bukan nasihat hukum.",
    ]
)

h1("8. Kesimpulan")
para(
    "Prioritas Klay di Jawa Tengah adalah segmen yang siap mengadopsi, bukan sekadar yang besar. "
    "Ritel dan F&B Kota Semarang serta Kota Surakarta adalah kandidat pilot terkuat; Sentra "
    "Perdagangan Padat adalah mesin volume; Wilayah Rintisan adalah pipeline edukasi. Baseline "
    "volume menghasilkan Top 5 yang sama sekali berbeda, sehingga keputusan sourcing harus memakai "
    "skor ICP, bukan peringkat jumlah usaha."
)
para(
    "Langkah berikutnya: validasi Top 5 dengan data pipeline internal, jalankan pilot 30 hari, "
    "ukur activation dan retensi, lalu kalibrasi bobot setiap kuartal. Sumber leads harus mengikuti "
    "jalur yang sah: API, data partner, atau opt-in merchant."
)
callout(
    "Satu kalimat untuk manajemen",
    [
        "“Jangan cari kota dengan usaha terbanyak; cari kota dan sektor dengan usaha yang paling siap membeli dan memakai Klay.”",
    ],
    bg=CREAM,
    bar=ORANGE,
)

h1("9. Lampiran: Reproduksibilitas")
para("Alur reproduksi dari akar proyek:")
pdf.set_font("DejaVuMono", "", 7.4)
pdf.set_text_color(*NAVY)
for line in [
    "python3 scripts/build_final_dataset.py",
    "python3 scripts/final_analysis.py",
    "python3 scripts/make_final_notebook.py",
    "jupyter nbconvert --to notebook --execute --inplace FinalProject_DS_Kelompok13.ipynb",
    "python3 scripts/make_final_report.py",
    "python3 scripts/make_final_slides.py",
]:
    pdf.multi_cell(0, 4.2, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_text_color(*TEXT)
pdf.ln(3)
table(
    ["Berkas", "Isi"],
    [
        ["FinalProject_DS_Kelompok13.ipynb", "Notebook utama, sudah tereksekusi"],
        ["data/processed/master_final.csv", "30 wilayah, komponen, klaster, centroid"],
        ["data/processed/segments_final.csv", "90 segmen, skor, peringkat, baseline"],
        ["data/processed/top5_segments.csv", "Tabel Top 5 segmen"],
        ["data/processed/scraping_legality.csv", "Tabel legalitas sumber leads"],
        ["data/processed/sdr_strategy.csv", "Strategi SDR per tier"],
        ["figures/final_*.png", "Tujuh figur final"],
        ["report/FinalProject_DS_Kelompok13.pdf", "Laporan ini"],
    ],
    [78, 90],
    font_size=7.8,
)

pdf.output(str(OUT))
print("Wrote", OUT, "pages:", pdf.page_no())
