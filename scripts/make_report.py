from pathlib import Path

import pandas as pd
from fpdf import FPDF, XPos, YPos
from fpdf.enums import TableCellFillMode
from fpdf.fonts import FontFace
from PIL import Image

ROOT = Path(".")
FIG = ROOT / "figures"
OUT = ROOT / "report" / "Tugas2_DS_Kelompok13.pdf"

clean = pd.read_csv(ROOT / "data/processed/master_clean.csv")
elim = pd.read_csv(ROOT / "data/processed/wilayah_tereliminasi.csv")
umkm = pd.read_csv(ROOT / "data/processed/provinsi_umkm_series.csv")

NAVY = (23, 58, 94)
TEAL = (44, 122, 140)
TEXT = (31, 41, 51)
CAPTION = (95, 107, 118)
LINE = (201, 211, 220)
LIGHT = (238, 244, 248)
CREAM = (255, 246, 229)
ORANGE = (224, 164, 58)

CONTENT_W = 210 - 44
LINE_H = 5.3
PARA_GAP = 2.5

HEADER = "Tugas 2 – Milestone 1 Final Project | Klay: Market Prioritization UMKM"

URLS = [
    "https://jateng.bps.go.id/id/publication/2025/02/28/6f9ad30e8755ed2b706cb979/provinsi-jawa-tengah-dalam-angka-2025.html",
    "https://data.jatengprov.go.id/dataset/79a-penduduk-laju-pertumbuhan-penduduk-distribusi-persentase-penduduk-kepadatan-penduduk-rasio-jenis",
    "https://data.jatengprov.go.id/dataset/6c4-indeks-pembangunan-manusia-ipm-menurut-kabupaten-kota",
    "https://data.jatengprov.go.id/dataset/7e5-jumlah-umkm-binaan-jawa-tengah",
]


class Report(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVuSans", "", 7.5)
        self.set_text_color(*CAPTION)
        self.set_xy(self.l_margin, 12)
        self.cell(0, 4, HEADER, align="L")
        self.set_draw_color(*LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, 18, self.w - self.r_margin, 18)
        self.set_xy(self.l_margin, self.t_margin)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font("DejaVuSans", "", 7.5)
        self.set_text_color(*CAPTION)
        self.set_x(self.l_margin)
        self.cell(0, 4, "Kelompok 13", align="L")
        self.set_xy(self.w - self.r_margin - 30, self.h - 12)
        self.cell(30, 4, f"Halaman {self.page_no()}", align="R")


pdf = Report(format="A4")
pdf.set_margins(22, 23, 22)
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_font("DejaVuSans", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVuSans", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.add_font("DejaVuSerif", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.add_font("DejaVuSerif", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
pdf.add_font("DejaVuMono", "", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
pdf.add_font("DejaVuMono", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")
pdf.set_title("Tugas 2 – Market Prioritization UMKM")
pdf.set_author("Kelompok 13")
pdf.set_subject("Milestone 1 Final Project – Klay")


def ensure_space(height):
    if pdf.get_y() + height > pdf.h - pdf.b_margin:
        pdf.add_page()


def text_height(text, width, family="DejaVuSans", style="", size=9.5,
                line_h=LINE_H, markdown=False):
    pdf.set_font(family, style, size)
    return pdf.multi_cell(width, line_h, text, dry_run=True, output="HEIGHT",
                          markdown=markdown)


def h1(text, new_page=False):
    if new_page:
        pdf.add_page()
    ensure_space(34)
    pdf.set_font("DejaVuSans", "B", 16)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(0, 8, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    y = pdf.get_y() + 1
    pdf.set_draw_color(*TEAL)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.set_line_width(0.3)
    pdf.ln(4)


def h2(text):
    ensure_space(26)
    pdf.set_font("DejaVuSans", "B", 11.5)
    pdf.set_text_color(*TEAL)
    pdf.multi_cell(0, 6.2, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def para(text, size=9.5, color=TEXT, gap=PARA_GAP, markdown=False):
    pdf.set_font("DejaVuSans", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, LINE_H, text, align="L", wrapmode="WORD",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=markdown)
    pdf.ln(gap)


def bold_para(text, size=9.5, gap=PARA_GAP):
    pdf.set_font("DejaVuSans", "B", size)
    pdf.set_text_color(*TEXT)
    pdf.multi_cell(0, LINE_H, text, align="L", wrapmode="WORD",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(gap)


def note(text, size=8.2, gap=2.0):
    ensure_space(8)
    pdf.set_font("DejaVuSans", "", size)
    pdf.set_text_color(*CAPTION)
    pdf.multi_cell(0, 4.4, text, align="L", wrapmode="WORD",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(gap)


def bullet_list(items, size=9.5, gap=PARA_GAP):
    for item in items:
        height = text_height(item, CONTENT_W - 5, "DejaVuSans", "", size,
                             LINE_H, markdown=True)
        ensure_space(height + 1)
        y = pdf.get_y()
        pdf.set_font("DejaVuSans", "", size)
        pdf.set_text_color(*TEXT)
        pdf.set_xy(pdf.l_margin, y)
        pdf.cell(5, LINE_H, "•")
        pdf.set_xy(pdf.l_margin + 5, y)
        pdf.multi_cell(CONTENT_W - 5, LINE_H, item, align="L",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
    pdf.ln(gap)


def numbered_list(items, size=9.5, gap=PARA_GAP):
    for i, item in enumerate(items, 1):
        height = text_height(item, CONTENT_W - 8, "DejaVuSans", "", size,
                             LINE_H, markdown=True)
        ensure_space(height + 1)
        y = pdf.get_y()
        pdf.set_font("DejaVuSans", "", size)
        pdf.set_text_color(*TEXT)
        pdf.set_xy(pdf.l_margin, y)
        pdf.cell(8, LINE_H, f"{i}.")
        pdf.set_xy(pdf.l_margin + 8, y)
        pdf.multi_cell(CONTENT_W - 8, LINE_H, item, align="L",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
    pdf.ln(gap)


def callout(title, items, bg=LIGHT, bar=TEAL, bullet=False, size=9.3):
    pad_x = 4.0
    pad_y = 3.5
    inner_w = CONTENT_W - 2 * pad_x
    title_h = 5.5 if title else 0
    item_heights = [
        text_height(item, inner_w - (4 if bullet else 0), "DejaVuSans", "",
                    size, 5.0, markdown=bullet)
        for item in items
    ]
    total = pad_y * 2 + title_h + sum(item_heights) + 1.5 * len(items)
    ensure_space(total + 2)
    x = pdf.l_margin
    y = pdf.get_y()
    pdf.set_fill_color(*bg)
    pdf.rect(x, y, CONTENT_W, total, "F")
    pdf.set_fill_color(*bar)
    pdf.rect(x, y, 1.2, total, "F")
    pdf.set_xy(x + pad_x, y + pad_y)
    if title:
        pdf.set_font("DejaVuSans", "B", 9.8)
        pdf.set_text_color(*NAVY)
        pdf.cell(0, title_h, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("DejaVuSans", "", size)
    pdf.set_text_color(*TEXT)
    for item in items:
        if bullet:
            pdf.set_x(x + pad_x)
            pdf.cell(4, 5.0, "•")
            pdf.set_x(x + pad_x + 4)
            pdf.multi_cell(inner_w - 4, 5.0, item, align="L",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
        else:
            pdf.set_x(x + pad_x)
            pdf.multi_cell(inner_w, 5.0, item, align="L",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1.5)
    pdf.set_y(y + total + 3)


def formula_box(text):
    pdf.set_font("DejaVuSans", "B", 9.5)
    inner_h = pdf.multi_cell(CONTENT_W - 8, 5.3, text, dry_run=True,
                             output="HEIGHT", align="C")
    total = inner_h + 8
    ensure_space(total + 2)
    x = pdf.l_margin
    y = pdf.get_y()
    pdf.set_fill_color(*LIGHT)
    pdf.rect(x, y, CONTENT_W, total, "F")
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.3)
    pdf.rect(x, y, CONTENT_W, total, "D")
    pdf.set_xy(x + 4, y + 4)
    pdf.set_text_color(*NAVY)
    pdf.multi_cell(CONTENT_W - 8, 5.3, text, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)


def table(headers, rows, widths, font_size=8, align="LEFT"):
    ensure_space(30)
    pdf.set_font("DejaVuSans", "", font_size)
    pdf.set_text_color(*TEXT)
    pdf.set_fill_color(255, 255, 255)
    with pdf.table(
        col_widths=widths,
        text_align=align,
        line_height=4.2,
        borders_layout="HORIZONTAL_LINES",
        first_row_as_headings=True,
        cell_fill_mode=TableCellFillMode.ROWS,
        cell_fill_color=LIGHT,
        headings_style=FontFace(emphasis="BOLD", size_pt=font_size,
                                color=(255, 255, 255), fill_color=NAVY),
        padding=1.5,
    ) as t:
        r = t.row()
        for header in headers:
            r.cell(header)
        for row in rows:
            r = t.row()
            for cell in row:
                r.cell(str(cell))
    pdf.ln(3)


def figure(path, caption, width=135):
    img = Image.open(path)
    img_w, img_h = img.size
    display_h = width * img_h / img_w
    caption_h = text_height(caption, CONTENT_W, "DejaVuSans", "", 8.2, 4.4)
    ensure_space(display_h + caption_h + 8)
    pdf.image(str(path), x=(pdf.w - width) / 2, w=width)
    pdf.ln(1)
    pdf.set_font("DejaVuSans", "", 8.2)
    pdf.set_text_color(*CAPTION)
    pdf.multi_cell(0, 4.4, caption, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def eda_block(title, fig_path, caption, body):
    width = 135
    img = Image.open(fig_path)
    img_w, img_h = img.size
    display_h = width * img_h / img_w
    caption_h = text_height(caption, CONTENT_W, "DejaVuSans", "", 8.2, 4.4)
    body_h = 0
    for kind, payload in body:
        if kind == "p":
            body_h += text_height(payload, CONTENT_W, "DejaVuSans", "", 9.5,
                                  LINE_H) + PARA_GAP
        elif kind == "bullets":
            for item in payload:
                body_h += text_height(item, CONTENT_W - 5, "DejaVuSans", "",
                                      9.5, LINE_H, markdown=True) + 1
            body_h += PARA_GAP
        elif kind == "note":
            body_h += text_height(payload, CONTENT_W, "DejaVuSans", "", 8.2,
                                  4.4) + 2
    required = 8.2 + 2 + display_h + 1 + caption_h + 2 + body_h + 4
    ensure_space(required)
    h2(title)
    pdf.image(str(fig_path), x=(pdf.w - width) / 2, w=width)
    pdf.ln(1)
    pdf.set_font("DejaVuSans", "", 8.2)
    pdf.set_text_color(*CAPTION)
    pdf.multi_cell(0, 4.4, caption, align="C",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)
    for kind, payload in body:
        if kind == "p":
            para(payload)
        elif kind == "bullets":
            bullet_list(payload)
        elif kind == "note":
            note(payload)


def link_line(text, url):
    pdf.set_font("DejaVuSans", "", 6.1)
    pdf.set_text_color(*TEAL)
    pdf.multi_cell(0, 3.4, text, link=url, align="L", wrapmode="WORD",
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def step_list(steps):
    for i, (text, command) in enumerate(steps, 1):
        height = text_height(text, CONTENT_W - 8, "DejaVuSans", "", 9.5,
                             LINE_H, markdown=True)
        command_h = (text_height(command, CONTENT_W - 8, "DejaVuMono", "", 8.0,
                                 4.2) if command else 0)
        ensure_space(height + command_h + 2)
        y = pdf.get_y()
        pdf.set_font("DejaVuSans", "", 9.5)
        pdf.set_text_color(*TEXT)
        pdf.set_xy(pdf.l_margin, y)
        pdf.cell(8, LINE_H, f"{i}.")
        pdf.set_xy(pdf.l_margin + 8, y)
        pdf.multi_cell(CONTENT_W - 8, LINE_H, text, align="L",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
        if command:
            pdf.set_x(pdf.l_margin + 8)
            pdf.set_font("DejaVuMono", "", 8.0)
            pdf.set_text_color(*NAVY)
            pdf.multi_cell(CONTENT_W - 8, 4.2, command, align="L",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(*TEXT)
        pdf.ln(1.0)


# ------------------------------------------------------------------ cover
pdf.add_page()
pdf.set_auto_page_break(False)
pdf.set_text_color(0, 0, 0)
PT = 25.4 / 72
pdf.set_y(23 + 12)

pdf.set_font("DejaVuSerif", "B", 12)
pdf.cell(0, 6, "TUGAS 2 – MILESTONE 1 FINAL PROJECT", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(34 * PT)

pdf.set_font("DejaVuSerif", "B", 20)
pdf.cell(0, 9, "MARKET PRIORITIZATION UMKM", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(16 * PT)

pdf.set_font("DejaVuSerif", "", 14)
pdf.cell(0, 7, "Wilayah Target Sourcing Leads B2B SaaS", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(8 * PT)

pdf.set_font("DejaVuSerif", "", 13)
pdf.cell(0, 7, "Klay (Skalar Solutions) – POS + AI Sales Analytics untuk UMKM",
         align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(30)

pdf.set_font("DejaVuSerif", "", 11.5)
pdf.cell(0, 6, "Studi kasus: 35 kabupaten/kota Provinsi Jawa Tengah", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(6 * PT)
pdf.cell(0, 6, "Periode data: 2023–2024", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(38)

pdf.set_font("DejaVuSerif", "B", 14)
pdf.cell(0, 7, "Kelompok 13", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(16 * PT)

pdf.set_font("DejaVuSerif", "", 12)
for i, line in enumerate([
    "Ayu Safitri (2610501106)",
    "Carissa Zia W. F (2610514008)",
    "Gerard Harjuno N (2610512189)",
]):
    pdf.cell(0, 5.2, line, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if i < 2:
        pdf.ln(8 * PT)
pdf.ln(45)

pdf.set_font("DejaVuSerif", "B", 13)
pdf.cell(0, 7, "Fakultas Ilmu Komputer", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(6 * PT)
pdf.cell(0, 7, "Universitas Pembangunan Nasional “Veteran” Jakarta", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ------------------------------------------------------------- executive
pdf.set_auto_page_break(True, margin=20)
h1("1. Ringkasan Eksekutif", new_page=True)
para("Klay menjual POS + AI Sales Analytics kepada UMKM. Untuk memprioritaskan wilayah "
     "sourcing leads, kami menyusun kerangka Ideal Customer Profile (ICP) pada 35 "
     "kabupaten/kota Provinsi Jawa Tengah. Data berasal dari empat sumber publik BPS dan "
     "Dinkop Jateng (2023–2024). Setelah pembersihan dan filter kualitas data, 30 wilayah "
     "lolos dan siap dianalisis.")

callout("Temuan utama", [
    "**Volume terbesar:** Kabupaten Banyumas, Cilacap, Kebumen, Purbalingga, dan Pemalang "
    "memimpin jumlah unit IMK. Namun, kepadatan IMK tidak otomatis sejalan dengan PDRB per "
    "kapita.",
    "**Segmen siap digital:** Kota Surakarta dan Kota Semarang unggul pada kepadatan "
    "pedagang pasar, IPM, PDRB, dan simpanan per kapita. Keduanya adalah segmen siap digital "
    "dengan daya beli tinggi.",
    "**Peluang digitalisasi:** Kabupaten dengan IMK padat cenderung memiliki IPM lebih "
    "rendah (r = −0,30), sehingga banyaknya usaha belum tentu berarti kesiapan digital "
    "tinggi. Kebumen, Wonosobo, dan Banjarnegara justru menawarkan peluang edukasi digital.",
    "**Rancangan bobot ICP:** Ukuran Pasar 25%, Kepadatan Sektor Target 25%, Kesiapan "
    "Digital 20%, Adopsi Pembayaran Digital 15%, Aktivitas Ekonomi 15%.",
], bullet=True)

h2("1.1 Ruang lingkup")
callout(None, [
    "Sesuai instruksi Tugas 2, pekerjaan berhenti pada perancangan bobot ICP. K-Means, skor "
    "indeks akhir, penentuan Top 5, dan uji sensitivitas bobot tidak dihitung di sini; "
    "bagian tersebut menjadi rencana milestone berikutnya.",
], bg=CREAM, bar=ORANGE)
para("Output utama: notebook Tugas2_DS_Kelompok13.ipynb, dataset mentah dan bersih di "
     "data/processed, sembilan figur (8 EDA + 1 bobot ICP) di figures, dan laporan ini.")

# ------------------------------------------------------------- collection
h1("2. Data Collection & Data Understanding", new_page=True)
h2("2.1 Sumber data")
para("Empat sumber publik dipakai untuk membangun dataset kabupaten/kota dan konteks "
     "provinsi. Ringkasan sumber, kolom kunci, alasan pemilihan, dan keterbatasannya "
     "disajikan pada tabel berikut.")
table(
    ["Sumber", "Level & kolom kunci", "Alasan dipilih", "Keterbatasan"],
    [
        ["1. BPS Jateng, Provinsi Jawa Tengah Dalam Angka 2025",
         "Kab/kota (35); IMK 2023, PDRB 2024, sarana perdagangan 2024, "
         "simpanan/tabungan 2024",
         "Satu publikasi resmi memuat lima indikator utama per kab/kota",
         "PDF; nama wilayah tidak membedakan kabupaten/kota; watermark dan sel en dash"],
        ["2. BPS Jateng, Penduduk menurut Kabupaten/Kota 2024",
         "Kab/kota (35); kode wilayah, jumlah penduduk, kepadatan",
         "Denominator kepadatan sektor dan konteks demografi",
         "Satu tahun; proyeksi penduduk"],
        ["3. BPS Jateng, IPM menurut Kabupaten/Kota 2024",
         "Kab/kota (35); IPM, pengeluaran per kapita, indikator pendidikan/kesehatan",
         "Proxy kesiapan digital dan kualitas sumber daya manusia",
         "IPM agregat; bukan literasi digital langsung"],
        ["4. Dinkop Jateng, Jumlah UMKM Binaan 2019–2024",
         "Provinsi; tahun, jumlah UMKM binaan",
         "Konteks pertumbuhan populasi UMKM di level provinsi",
         "Hanya UMKM binaan; 2024 baru s.d. TW II"],
    ],
    [36, 45, 44, 41],
    font_size=8,
)
ensure_space(30)
for i, url in enumerate(URLS, 1):
    link_line(f"{i}. {url}", url)

h2("2.2 Definisi operasional dan data yang tidak tersedia")
bullet_list([
    "**IMK:** Industri Mikro dan Kecil, yaitu unit usaha manufaktur berskala mikro/kecil; "
    "dipakai sebagai proxy kepadatan sektor target, bukan total UMKM.",
    "**Pedagang pasar:** pedagang yang berjualan di pasar rakyat; proxy retail/F&B "
    "tradisional.",
    "**Sarana perdagangan:** pasar, supermarket, dan pedagang pasar; bukan seluruh kanal "
    "retail modern.",
    "**UMKM binaan:** UMKM yang difasilitasi Dinkop Jateng; bukan populasi seluruh UMKM.",
])
para("Keterbatasan data: total UMKM per kabupaten/kota tidak tersedia seragam; QRIS merchant "
     "per kabupaten/kota tidak tersedia publik; data UMKM binaan hanya level provinsi; dan "
     "sebagian tabel BPS hanya tersedia dalam PDF sehingga memerlukan ekstraksi serta "
     "validasi manual.")

h2("2.3 Pemetaan sektor")
para("Brief ICP Klay menyasar ritel, F&B, dan jasa transaksi kecil berulang. Data publik yang "
     "dipakai tidak menyediakan komposisi sektor per kabupaten/kota. Jumlah unit IMK dipakai "
     "sebagai proxy umum usaha mikro/kecil, sedangkan pedagang pasar sebagai proxy ritel/F&B "
     "tradisional. Komposisi F&B dan jasa per wilayah tidak dapat difilter terpisah; filter "
     "sektor tanpa transaksi harian rutin juga tidak diterapkan pada level ini. Filter hanya "
     "dilakukan pada level wilayah, dan keterbatasan ini dicatat eksplisit.")

# ------------------------------------------------------------- preparation
h1("3. Data Preparation")
h2("3.1 Pembersihan data")
para("Tahapan pembersihan yang dilakukan:")
bullet_list([
    "Ekstraksi tabel PDF dengan pdfplumber, lalu membersihkan angka dari watermark dan "
    "pemisah ribuan.",
    "Mengganti nama wilayah hasil ekstraksi dengan nama kanonik dari file penduduk "
    "berdasarkan urutan 35 wilayah dan kode wilayah (3301–3329 kabupaten, 3371–3376 kota).",
    "Mengisi sel en dash pada tabel sarana perdagangan dengan 0 karena tanda tersebut "
    "berarti tidak ada outlet, bukan data hilang.",
    "Memeriksa duplikat dan missing pada level kode dan nama wilayah; memastikan seluruh "
    "kolom numerik bertipe angka.",
])
bold_para("Hasil validasi: 35 baris, 35 wilayah unik, 0 duplikat, 0 missing. Tidak ada nilai "
          "negatif yang tidak wajar.")

h2("3.2 Merging lintas level")
para("Data kabupaten/kota digabung dengan kode wilayah dan nama wilayah sebagai kunci. Data "
     "provinsi (time series UMKM binaan) tidak di-join secara aditif karena level agregasinya "
     "berbeda. Yang dilakukan adalah broadcast satu kolom konteks, yaitu pertumbuhan UMKM "
     "binaan 2023 (3,02%), ke seluruh kabupaten/kota. Kolom ini dipakai sebagai konteks, "
     "bukan tambahan kuantitas.")
callout("Mengapa tidak dijumlahkan?", [
    "Total UMKM binaan provinsi 2023 adalah 186.024 unit, sedangkan total unit IMK 35 "
    "kabupaten/kota adalah 862.926 unit. Keduanya mengukur populasi berbeda, sehingga "
    "penjumlahan akan menyesatkan. Perbedaan definisi ini dicatat sebagai limitasi.",
])

h2("3.3 Kriteria penggugur")
para("Filter dipakai untuk membuang wilayah yang terlalu kecil atau ekstrem agar segmentasi "
     "tidak didominasi outlier. Tiga kriteria diterapkan:")
numbered_list([
    "Data kunci kosong.",
    "Skala terlalu kecil, yaitu IMK < 10.000 unit.",
    "Outlier kepadatan, yaitu IMK per 100.000 penduduk > Q3 + 1,5 × IQR.",
])
para("Ambang 10.000 dipilih agar kota-kota kecil dengan basis manufaktur tipis keluar, "
     "tetapi wilayah dengan basis memadai tetap lolos.")
ensure_space(85)
para(f"Hasil: {len(elim)} wilayah gugur dan {len(clean)} wilayah lolos (di atas syarat "
     "minimal 20). Daftar wilayah gugur:")
table(
    ["Wilayah", "Tipe", "IMK (unit)", "IMK/100k", "Alasan"],
    [
        [
            r.wilayah if str(r.wilayah).startswith("Kota") else f"Kabupaten {r.wilayah}",
            r.tipe,
            f"{r.imk_unit:,.0f}".replace(",", "."),
            f"{r.imk_per_100k:,.0f}".replace(",", "."),
            r.alasan_gugur.replace("5,298", "5.298"),
        ]
        for r in elim.itertuples()
    ],
    [48, 27, 25, 25, 55],
)
para("Filter ini secara tidak proporsional mengeluarkan kota-kota kecil. Dari enam kota, "
     "hanya Kota Semarang dan Kota Surakarta yang lolos. Ini adalah trade-off yang disadari: "
     "fokus pada wilayah dengan basis sektor cukup besar, sementara analisis kota kecil perlu "
     "dilakukan terpisah.")

h2("3.4 Normalisasi Min-Max")
para("Normalisasi dilakukan pada 30 wilayah yang lolos dengan rumus x′ = (x − min) / "
     "(max − min). Fitur yang dinormalisasi mewakili lima komponen ICP: jumlah unit IMK, "
     "jumlah pedagang pasar, IMK per 100k, pedagang per 100k, IPM, pengeluaran per kapita, "
     "simpanan per kapita, tabungan per kapita, dan PDRB per kapita. Seluruh hasil berada "
     "pada rentang 0–1.")
callout("Catatan Min-Max", [
    "Min-Max sensitif terhadap outlier. Setelah filter, simpanan per kapita masih sangat "
    "miring karena didominasi Kota Semarang. Pada milestone berikutnya perlu dipertimbangkan "
    "log-transform atau winsorization sebelum scoring.",
], bg=CREAM, bar=ORANGE)

# ------------------------------------------------------------- EDA
h1("4. Exploratory Data Analysis", new_page=True)
para("EDA dilakukan pada 30 wilayah yang lolos. Fokusnya memetakan variasi antarwilayah dan "
     "mencari kombinasi indikator yang relevan untuk ICP Klay, bukan inferensi kausal.")

eda_block(
    "4.1 Sebaran jumlah unit IMK",
    FIG / "fig1_imk_distribution.png",
    "Gambar 1. Sebaran jumlah unit IMK 2023 pada 30 wilayah yang lolos filter.",
    [("p", "Distribusi jumlah IMK sangat timpang. Banyumas, Cilacap, Kebumen, Purbalingga, "
           "dan Pemalang masing-masing memiliki lebih dari 42 ribu unit, sedangkan wilayah "
           "lain jauh lebih kecil. Lima wilayah ini adalah pasar volume untuk paket dasar "
           "POS, tetapi belum tentu paling siap digital. Prioritas sebaiknya "
           "mempertimbangkan kepadatan relatif dan kesiapan digital, bukan hanya jumlah "
           "absolut.")],
)

eda_block(
    "4.2 Kepadatan IMK menurut tipe wilayah",
    FIG / "fig2_boxplot_imk_density.png",
    "Gambar 2. Kepadatan IMK per 100.000 penduduk menurut tipe wilayah (n=28 kabupaten, "
    "n=2 kota).",
    [
        ("p", "Kabupaten memiliki rata-rata unit IMK jauh lebih besar (26.892 vs 13.612), "
              "tetapi kepadatan per 100 ribu penduduk juga lebih tinggi (2.307 vs 1.510). "
              "Kota yang lolos justru unggul pada kepadatan pedagang pasar, PDRB, dan IPM. "
              "Profil risiko dan pendekatan akuisisi berbeda: kabupaten cocok untuk "
              "penetrasi volume manufaktur/retail tradisional, kota cocok untuk merchant "
              "yang sudah siap digital dan bertransaksi lebih tinggi."),
        ("note", "Catatan: kelompok kota hanya berisi dua wilayah sehingga perbandingan "
                 "bersifat indikatif."),
    ],
)

eda_block(
    "4.3 PDRB per kapita vs kepadatan pedagang pasar",
    FIG / "fig3_pdrb_vs_pedagang.png",
    "Gambar 3. Hubungan PDRB per kapita 2024 dan pedagang pasar per 100.000 penduduk.",
    [("p", "Korelasi positif sedang (r = 0,42). Wilayah dengan aktivitas ekonomi tinggi "
           "cenderung memiliki ekosistem pedagang pasar yang padat. Kota Surakarta adalah "
           "outlier positif: PDRB tinggi dan kepadatan pedagang sangat tinggi. Sebaliknya, "
           "beberapa kabupaten berpendapatan rendah tetap memiliki kepadatan pedagang tinggi "
           "(Kebumen, Temanggung, Purworejo), menandakan aktivitas retail tradisional besar "
           "tetapi daya beli belum tinggi. Wilayah seperti ini cocok untuk paket hemat dan "
           "edukasi digital.")],
)

eda_block(
    "4.4 IPM vs kepadatan IMK",
    FIG / "fig4_ipm_vs_imk.png",
    "Gambar 4. Hubungan IPM 2024 dan kepadatan IMK per 100.000 penduduk.",
    [("p", "Korelasinya negatif lemah (r = −0,30). Kabupaten dengan IMK padat "
           "(Purbalingga, Temanggung, Kebumen, Batang) justru memiliki IPM menengah, bukan "
           "tertinggi. Ini adalah gap yang menarik: basis usaha besar, tetapi kesiapan "
           "digital belum matang. Klay dapat memposisikan diri sebagai alat bantu adopsi "
           "digital, bukan sekadar POS. Sebaliknya, kota dengan IPM tinggi tetapi IMK rendah "
           "lebih cocok untuk produk analytics yang sudah advanced.")],
)

eda_block(
    "4.5 Peta prioritas awal (multivariat)",
    FIG / "fig5_multivariate_bubble.png",
    "Gambar 5. PDRB vs kepadatan IMK; ukuran gelembung = populasi, warna = IPM 2024.",
    [
        ("p", "Empat kuadran memberi arah strategi, tetapi sebaran aktual tidak rapi. Pada "
              "data ini, kuadran kanan atas nyaris kosong: belum ada wilayah dengan PDRB "
              "tinggi sekaligus kepadatan IMK tinggi."),
        ("bullets", [
            "**Kanan atas** (PDRB tinggi, IMK padat): wilayah “siap scale” untuk paket "
            "lengkap; pada data ini kuadran ini nyaris kosong.",
            "**Kiri atas** (PDRB rendah, IMK padat): volume besar dengan daya beli "
            "terbatas; cocok untuk paket hemat dan onboarding intensif.",
            "**Kanan bawah** (PDRB tinggi, IMK rendah): ekonomi jasa/perdagangan; prospek "
            "merchant retail, bukan manufaktur.",
            "**Kiri bawah** (keduanya rendah): prioritas rendah untuk sourcing awal.",
        ]),
        ("p", "Kota Semarang dan Surakarta berada di sisi kanan (PDRB tinggi, IPM tinggi) "
              "tetapi kepadatan IMK rendah hingga sedang. Kebumen, Wonosobo, dan "
              "Banjarnegara berada di kiri atas dengan populasi besar dan IPM menengah; "
              "kombinasi ini menarik untuk ekspansi berbasis volume."),
    ],
)

eda_block(
    "4.6 Profil komponen ICP",
    FIG / "fig6_heatmap_komponen.png",
    "Gambar 6. Z-score lima komponen ICP pada 15 wilayah dengan kepadatan sektor tertinggi "
    "(z-score dihitung ulang di antara 15 wilayah terpilih).",
    [
        ("p", "Wilayah dengan kepadatan sektor tinggi tidak seragam pada komponen lain. "
              "Sebagian unggul di ukuran pasar tetapi lemah di adopsi digital; sebagian lain "
              "seimbang. Untuk Klay, kombinasi kepadatan sektor tinggi dan kesiapan digital "
              "menengah adalah target paling efisien: kebutuhan nyata, tetapi belum terlalu "
              "matang sehingga masih ada ruang untuk value proposition POS/AI."),
        ("note", "Catatan: nilai pada gambar adalah z-score yang dihitung ulang di antara 15 "
                 "wilayah terpilih, bukan normalisasi Min-Max di Bab 3. Karena itu, sebagian "
                 "baris bawah bernilai negatif; ini bukan berarti kepadatan absolutnya rendah."),
    ],
)

eda_block(
    "4.7 Tren UMKM binaan provinsi",
    FIG / "fig7_umkm_series.png",
    "Gambar 7. Jumlah UMKM binaan Provinsi Jawa Tengah, 2019–2024 (2024 s.d. TW II).",
    [("p", "Populasi UMKM binaan tumbuh konsisten sekitar 3–4% per tahun (CAGR 2019–2023 = "
           "3,6%; pertumbuhan 2022 = 4,12%). Angka 2024 baru mencakup TW II, jadi tidak "
           "sebanding dengan tahun penuh. Pertumbuhan yang stabil menandakan pasar sourcing "
           "yang terus bertambah, tetapi Klay perlu prioritas berbasis kualitas wilayah, "
           "bukan hanya mengejar volume.")],
)

eda_block(
    "4.8 Komposisi sarana perdagangan",
    FIG / "fig8_retail_mix.png",
    "Gambar 8. Jumlah pasar dan supermarket pada 15 wilayah dengan pedagang pasar "
    "terbanyak; wilayah diurutkan berdasarkan jumlah pedagang pasar.",
    [
        ("p", "Hampir seluruh ekosistem retail di wilayah terpilih berbasis pasar rakyat; "
              "supermarket hanya sebagian kecil. Ini memperkuat tesis bahwa pasar "
              "tradisional dan pedagangnya adalah segmen utama Klay, bukan hanya retail "
              "modern. Kota Semarang menjadi pengecualian karena jumlah supermarketnya "
              "hampir menyamai jumlah pasar. Kendal dan Kebumen menunjukkan pola pasar "
              "rakyat dominan dengan supermarket yang relatif sedikit, kemungkinan masih "
              "sangat bergantung pada transaksi tunai; keduanya menjadi peluang untuk "
              "edukasi pembayaran digital dan pencatatan penjualan."),
        ("note", "Catatan: sumbu x menampilkan jumlah sarana (pasar dan supermarket), "
                 "sedangkan urutan wilayah berdasarkan jumlah pedagang pasar."),
    ],
)

# ------------------------------------------------------------- ICP
h1("5. Rancangan Bobot Ideal Customer Profile (ICP)", new_page=True)
para("Bobot disusun dari lima komponen yang mencerminkan kesesuaian produk, kemampuan bayar, "
     "dan kemudahan akuisisi. Total bobot = 100%.")
table(
    ["Komponen", "Indikator", "Arah", "Bobot", "Justifikasi"],
    [
        ["Ukuran Pasar", "Jumlah unit IMK; jumlah pedagang pasar", "+", "25%",
         "Jumlah usaha mikro/kecil dan pedagang pasar menentukan volume merchant dan "
         "transaksi; Klay memonetisasi per outlet."],
        ["Kepadatan Sektor Target", "IMK/100k; pedagang pasar/100k", "+", "25%",
         "F&B, retail, dan jasa adalah pengguna utama POS; kepadatan tinggi menurunkan "
         "biaya akuisisi."],
        ["Kesiapan Digital", "IPM; pengeluaran per kapita (proxy)", "+", "20%",
         "IPM dan daya beli adalah proxy kesiapan digital karena persentase pengguna "
         "internet/ponsel per kab/kota tidak tersedia."],
        ["Adopsi Pembayaran Digital", "Simpanan/kapita; tabungan/kapita (proxy)", "+", "15%",
         "Proxy kebiasaan nontunai dan akses keuangan; QRIS ideal tetapi belum tersedia per "
         "kab/kota."],
        ["Aktivitas Ekonomi", "PDRB per kapita", "+", "15%",
         "Intensitas bisnis dan kemampuan bayar menentukan kesediaan berlangganan."],
    ],
    [31, 35, 11, 13, 76],
    font_size=8,
)
figure(FIG / "fig9_bobot_icp.png",
       "Gambar 9. Rancangan bobot ICP Klay; total 100%.")

h2("5.1 Formula skor (rancangan, belum dihitung)")
formula_box("ICP(i) = 0,25 U(i) + 0,25 K(i) + 0,20 D(i) + 0,15 A(i) + 0,15 E(i)")
para("dengan:")
bullet_list([
    "**U** = rata-rata Min-Max jumlah unit IMK dan pedagang pasar.",
    "**K** = rata-rata Min-Max IMK/100k dan pedagang/100k.",
    "**D** = rata-rata Min-Max IPM dan pengeluaran per kapita.",
    "**A** = rata-rata Min-Max simpanan dan tabungan per kapita.",
    "**E** = Min-Max PDRB per kapita.",
])
ensure_space(14)
para("Semua komponen berada pada rentang 0–1, sehingga ICP juga 0–1. Skor akhir, peringkat, "
     "Top 5, dan uji sensitivitas bobot tidak dihitung di Tugas 2.")

h2("5.2 Rasional pembobotan")
bullet_list([
    "**Ukuran Pasar (25%) dan Kepadatan Sektor Target (25%)** mendapat bobot terbesar "
    "karena keduanya paling langsung menentukan jumlah leads dan potensi revenue.",
    "**Kesiapan Digital (20%)** lebih tinggi dari adopsi/aktivitas karena Klay adalah "
    "produk software: wilayah dengan literasi dan daya beli lebih baik lebih murah "
    "di-onboard dan lebih kecil churn.",
    "**Adopsi Pembayaran Digital (15%)** penting, tetapi datanya hanya proxy "
    "simpanan/tabungan, bukan QRIS merchant. Bobotnya dibatasi agar tidak mendominasi.",
    "**Aktivitas Ekonomi (15%)** memberi sinyal daya beli, tetapi PDRB per kapita tidak "
    "secara langsung mengukur kesiapan adopsi software.",
])

# ------------------------------------------------------------- conclusion
h1("6. Kesimpulan dan Keterbatasan")
h2("6.1 Kesimpulan")
bullet_list([
    "Data 35 kabupaten/kota berhasil digabung dari empat sumber publik tanpa missing atau "
    "duplikat.",
    "Setelah filter, 30 wilayah siap dianalisis; lima gugur karena outlier kepadatan atau "
    "IMK < 10.000 unit.",
    "EDA menunjukkan **dua kelompok besar**: kabupaten berbasis manufaktur/retail "
    "tradisional dan kota berbasis jasa/perdagangan. Ini temuan awal, belum diuji K-Means.",
    "Bobot ICP: ukuran pasar dan kepadatan sektor 50%, kesiapan digital 20%, adopsi "
    "pembayaran dan aktivitas ekonomi 30%.",
    "Kebumen, Purbalingga, Temanggung, dan Batang cocok untuk ekspansi volume; Semarang dan "
    "Surakarta untuk paket advanced.",
])

h2("6.2 Keterbatasan")
bullet_list([
    "**Proxy sektor:** IMK dan pedagang pasar hanya proxy, bukan seluruh UMKM/retail; "
    "komposisi sektor per kabupaten/kota tidak tersedia, sehingga filter sektor tidak "
    "diterapkan.",
    "**Data adopsi digital:** QRIS merchant tidak tersedia publik; simpanan/tabungan per "
    "kapita hanya proxy tidak langsung.",
    "**Level agregasi:** UMKM binaan hanya level provinsi dan hanya UMKM binaan Dinkop, "
    "bukan total UMKM.",
    "**Filter:** ambang 10.000 unit IMK mengeluarkan empat dari enam kota; analisis kota "
    "kecil perlu terpisah.",
    "**Desain cross-sectional:** data 2023–2024 tidak memungkinkan inferensi kausal atau "
    "tren jangka panjang.",
    "**Normalisasi:** Min-Max sensitif outlier; simpanan per kapita didominasi Kota "
    "Semarang, sehingga perlu log-transform atau winsorization.",
])

h2("6.3 Rencana milestone berikutnya")
numbered_list([
    "Finalisasi fitur dan uji sensitivitas bobot ICP.",
    "Segmentasi wilayah dengan K-Means (jumlah klaster diuji dengan elbow/silhouette).",
    "Perhitungan skor akhir dan penentuan Top 5 wilayah.",
    "Validasi eksternal (mis. data QRIS atau survei lapangan) bila tersedia.",
])

# ------------------------------------------------------------- appendix
h1("Lampiran", new_page=True)
h2("A. Struktur deliverable")
para("Output utama: notebook Tugas2_DS_Kelompok13.ipynb yang tereksekusi tanpa error, "
     "dataset mentah dan bersih di data/processed, sembilan figur (8 EDA + 1 bobot ICP) di "
     "figures, dan laporan ini.")
table(
    ["Path", "Isi"],
    [
        ["Tugas2_DS_Kelompok13.ipynb", "Notebook utama, tereksekusi tanpa error"],
        ["data/raw/", "PDF BPS, XLSX penduduk/IPM/UMKM"],
        ["data/processed/master_raw.csv", "Dataset gabungan 35 wilayah sebelum filter"],
        ["data/processed/master_clean.csv", "Dataset 30 wilayah setelah filter + normalisasi"],
        ["data/processed/wilayah_tereliminasi.csv", "Daftar 5 wilayah gugur dan alasannya"],
        ["data/processed/provinsi_umkm_series.csv", "Time series UMKM binaan 2019–2024"],
        ["data/processed/Tugas2_DS_Kelompok13_Data.xlsx",
         "Excel berformat: ringkasan, data, wilayah gugur, UMKM provinsi, bobot ICP"],
        ["figures/", "Sembilan figur EDA dan bobot ICP"],
        ["scripts/build_dataset.py", "Skrip ekstraksi dan pembentukan dataset"],
        ["scripts/make_notebook.py", "Generator notebook"],
        ["scripts/make_report.py", "Generator laporan PDF"],
    ],
    [78, 88],
    font_size=8,
)

h2("B. Cara menjalankan ulang")
step_list([
    ("Install dependensi (pandas, numpy, matplotlib, seaborn, scikit-learn, pdfplumber, "
     "openpyxl, nbformat, nbconvert, fpdf2, Pillow, notebook).",
     "pip install -r requirements.txt"),
    ("Letakkan raw data di data/raw (lihat README).", None),
    ("Bentuk ulang dataset dari raw data.", "python scripts/build_dataset.py"),
    ("Tulis ulang notebook dari sumber.", "python scripts/make_notebook.py"),
    ("Eksekusi notebook tanpa membuka Jupyter.",
     "jupyter nbconvert --to notebook --execute --inplace Tugas2_DS_Kelompok13.ipynb"),
    ("Hasilkan laporan PDF.", "python scripts/make_report.py"),
])

h2("C. Pembagian tugas")
table(
    ["Anggota", "Tugas"],
    [
        ["Ayu Safitri (2610501106)", "Data collection & data understanding"],
        ["Carissa Zia W. F (2610514008)", "Data preparation & merging"],
        ["Gerard Harjuno N (2610512189)", "EDA, visualisasi & rancangan bobot ICP"],
    ],
    [65, 101],
    font_size=8,
)
bold_para("Arsip akhir: Tugas2_DS_Kelompok13.zip")

OUT.parent.mkdir(parents=True, exist_ok=True)
pdf.output(str(OUT))
print("Laporan ditulis:", OUT)
