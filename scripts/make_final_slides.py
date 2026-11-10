"""Build the Final Project slide deck (16:9)."""
from pathlib import Path

import pandas as pd
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
FIG = ROOT / "figures"
OUT = ROOT / "report" / "FinalProject_DS_Kelompok13.pptx"

top5 = pd.read_csv(DATA / "top5_segments.csv")
profile = pd.read_csv(DATA / "cluster_profile.csv")
sens = pd.read_csv(DATA / "sensitivity_scenarios.csv")
scraping = pd.read_csv(DATA / "scraping_legality.csv")

NAVY = RGBColor(0x17, 0x3A, 0x5E)
TEAL = RGBColor(0x2C, 0x7A, 0x8C)
ORANGE = RGBColor(0xE0, 0xA4, 0x3A)
DARK = RGBColor(0x1F, 0x29, 0x33)
GRAY = RGBColor(0x5F, 0x6B, 0x76)
LIGHT = RGBColor(0xEE, 0xF4, 0xF8)
CREAM = RGBColor(0xFF, 0xF6, 0xE5)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xC9, 0xD3, 0xDC)
GREEN = RGBColor(0x2E, 0x7D, 0x5B)
RED = RGBColor(0xA8, 0x45, 0x3E)
FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL = 12


def add_text(slide, x, y, w, h, text, size=18, bold=False, italic=False, color=DARK, align=PP_ALIGN.LEFT, font=FONT, spacing=1.0, anchor=MSO_ANCHOR.TOP, margin=0.02):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = anchor
    lines = str(text).split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        p.line_spacing = spacing
        for run in p.runs:
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = color
    return box


def add_bullets(slide, x, y, w, h, items, size=14, color=DARK, gap=8, bullet_color=TEAL):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "•  " + item
        p.space_before = Pt(0)
        p.space_after = Pt(gap)
        p.line_spacing = 1.08
        for run in p.runs:
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.color.rgb = color
    return box


def add_card(slide, x, y, w, h, fill=LIGHT, line=None, radius=True):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line:
        shape.line.color.rgb = line
        shape.line.width = Pt(0.8)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def add_rule(slide, x, y, w, color=LINE, width=0.8):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Pt(width))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_header(slide, kicker, title, subtitle=None):
    add_text(slide, 0.62, 0.36, 12.0, 0.25, kicker.upper(), size=10, bold=True, color=TEAL)
    add_text(slide, 0.62, 0.62, 12.1, 0.62, title, size=27, bold=True, color=NAVY)
    add_rule(slide, 0.62, 1.28, 12.1, TEAL, 1.2)
    if subtitle:
        add_text(slide, 0.62, 1.38, 12.0, 0.32, subtitle, size=12.5, color=GRAY)


def add_footer(slide, number):
    add_text(slide, 0.62, 7.12, 8.0, 0.22, "Klay × Kelompok 13  |  Final Project Data Science", size=8.5, color=GRAY)
    add_text(slide, 12.05, 7.12, 0.65, 0.22, f"{number:02d}", size=8.5, bold=True, color=NAVY, align=PP_ALIGN.RIGHT)


def add_image_fit(slide, path, x, y, max_w, max_h):
    img = Image.open(path)
    iw, ih = img.size
    scale = min(max_w / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    left = x + (max_w - w) / 2
    top = y + (max_h - h) / 2
    slide.shapes.add_picture(str(path), Inches(left), Inches(top), width=Inches(w), height=Inches(h))


def add_table(slide, x, y, w, h, headers, rows, col_widths, font_size=10, header_size=9.5, row_h=0.33, header_fill=NAVY, align=None):
    shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(x), Inches(y), Inches(w), Inches(h))
    table = shape.table
    for i, width in enumerate(col_widths):
        table.columns[i].width = Inches(width)
    table.rows[0].height = Inches(0.36)
    for i in range(1, len(rows) + 1):
        table.rows[i].height = Inches(row_h)
    for c, header in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        cell.margin_left = Inches(0.07)
        cell.margin_right = Inches(0.05)
        cell.margin_top = Inches(0.02)
        cell.margin_bottom = Inches(0.02)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = header
        p.alignment = PP_ALIGN.LEFT if align is None else align[c]
        for run in p.runs:
            run.font.name = FONT
            run.font.size = Pt(header_size)
            run.font.bold = True
            run.font.color.rgb = WHITE
    for r, row in enumerate(rows, 1):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 else LIGHT
            cell.margin_left = Inches(0.07)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(value)
            p.alignment = PP_ALIGN.LEFT if align is None else align[c]
            for run in p.runs:
                run.font.name = FONT
                run.font.size = Pt(font_size)
                run.font.color.rgb = DARK
    return table


def pill(slide, x, y, w, h, text, fill=LIGHT, color=NAVY, size=10.5):
    add_card(slide, x, y, w, h, fill=fill)
    add_text(slide, x, y - 0.01, w, h, text, size=size, bold=True, color=color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ 1. cover
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, 0.16, prs.slide_height)
accent.fill.solid()
accent.fill.fore_color.rgb = TEAL
accent.line.fill.background()

add_text(s, 0.85, 0.75, 5.0, 0.3, "FINAL PROJECT  ·  DATA SCIENCE", size=11, bold=True, color=RGBColor(0x9F, 0xC5, 0xD3))
add_text(s, 0.85, 1.55, 8.2, 0.8, "DARI VOLUME\nKE KESIAPAN", size=42, bold=True, color=WHITE, spacing=0.92)
add_text(s, 0.85, 3.42, 8.0, 0.9, "Segmentasi Wilayah dan\nPrioritisasi Leads UMKM", size=21, color=RGBColor(0xD9, 0xE6, 0xEF), spacing=1.12)
add_text(s, 0.85, 4.62, 7.8, 0.5, "Klay (Skalar Solutions) — POS + AI Sales Analytics", size=13, color=RGBColor(0xB8, 0xCD, 0xDB))
add_rule(s, 0.85, 5.25, 3.0, ORANGE, 2.0)
add_text(s, 0.85, 5.5, 6.4, 0.35, "Kelompok 13  ·  Ayu Safitri  ·  Carissa Zia  ·  Gerard Harjuno", size=11.5, color=WHITE)

for i, (num, label) in enumerate([("30", "wilayah"), ("90", "segmen"), ("4", "sumber"), ("3", "klaster")]):
    x = 9.15 + (i % 2) * 1.75
    y = 1.75 + (i // 2) * 1.72
    add_card(s, x, y, 1.55, 1.45, fill=RGBColor(0x21, 0x4A, 0x70))
    add_text(s, x, y + 0.18, 1.55, 0.55, num, size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, x, y + 0.78, 1.55, 0.25, label, size=9.5, color=RGBColor(0xB8, 0xCD, 0xDB), align=PP_ALIGN.CENTER)

# ------------------------------------------------------------------ 2. problem
s = prs.slides.add_slide(BLANK)
add_header(s, "01  ·  Masalah", "Volume bukan prioritas", "Pasar terbesar belum tentu paling siap membeli dan mengadopsi.")
add_text(s, 0.62, 1.82, 5.15, 1.55, "Top 5 volume", size=12, bold=True, color=GRAY)
add_text(s, 0.62, 2.15, 5.15, 0.6, "Semua Ritel. Semua kabupaten.", size=18, bold=True, color=NAVY)
add_text(s, 0.62, 2.62, 5.15, 1.25, "Banyumas 44.960  ·  Tegal 39.767\nGrobogan 39.264  ·  Purbalingga 37.960\nCilacap 35.905", size=13, color=DARK, spacing=1.25)
add_text(s, 0.62, 4.08, 5.15, 0.5, "Skor ICP", size=12, bold=True, color=ORANGE)

add_text(s, 6.0, 1.82, 6.3, 1.55, "Top 5 ICP", size=12, bold=True, color=GRAY)
add_text(s, 6.0, 2.15, 6.3, 0.6, "Semua Hub Digital Matang.", size=18, bold=True, color=NAVY)
add_text(s, 6.0, 2.62, 6.3, 1.3, "Ritel & F&B Kota Semarang\nRitel & F&B Kota Surakarta\nJasa Kota Semarang", size=13, color=DARK, spacing=1.25)
add_text(s, 6.0, 4.08, 6.3, 0.5, "Siap pilot berbayar", size=12, bold=True, color=TEAL)

add_card(s, 0.62, 5.35, 3.55, 1.18, fill=CREAM, line=ORANGE)
add_text(s, 0.85, 5.55, 3.1, 0.3, "OVERLAP TOP 5", size=9.5, bold=True, color=ORANGE)
add_text(s, 0.85, 5.8, 3.1, 0.5, "0 / 5", size=26, bold=True, color=NAVY)
add_text(s, 4.55, 5.55, 7.5, 0.65, "ρ = 0,738  ·  arah sama, tetapi ujung distribusi berbeda", size=13, color=GRAY)
add_text(s, 4.55, 6.12, 8.0, 0.35, "Keputusan sourcing tidak boleh hanya memakai peringkat jumlah usaha.", size=11.5, italic=True, color=TEAL)
add_footer(s, 2)

# ------------------------------------------------------------------ 3. data
s = prs.slides.add_slide(BLANK)
add_header(s, "02  ·  Data", "Empat sumber, satu dataset segmen", "Data publik 2023–2024, 30 kabupaten/kota, 90 segmen sektor × wilayah.")
sources = [
    ("BPS Jateng", "Jateng Dalam Angka 2025", "PDRB, simpanan, sarana"),
    ("BPS Jateng", "Penduduk 2024", "Denominator kepadatan"),
    ("BPS Jateng", "IPM 2024", "Kesiapan digital"),
    ("Dinkop Jateng", "Pelaku usaha per KBLI 2024", "Ritel, F&B, Jasa"),
]
for i, (org, title, desc) in enumerate(sources):
    x = 0.62 + i * 3.1
    add_card(s, x, 1.88, 2.82, 1.92, fill=LIGHT)
    add_text(s, x + 0.2, 2.04, 2.4, 0.25, org.upper(), size=8.8, bold=True, color=TEAL)
    add_text(s, x + 0.2, 2.34, 2.45, 0.62, title, size=11.4, bold=True, color=NAVY)
    add_text(s, x + 0.2, 3.02, 2.45, 0.42, desc, size=9.8, color=GRAY)

add_text(s, 0.62, 4.15, 12.0, 0.3, "ALUR ANALISIS", size=9.5, bold=True, color=GRAY)
steps = [("4 sumber", "BPS + Dinkop"), ("30 wilayah", "lolos filter"), ("90 segmen", "3 sektor × 30"), ("Skor ICP", "5 komponen")]
for i, (big, small) in enumerate(steps):
    x = 0.62 + i * 3.08
    add_card(s, x, 4.5, 2.7, 0.95, fill=NAVY if i == 3 else LIGHT)
    add_text(s, x, 4.6, 2.7, 0.38, big, size=16, bold=True, color=WHITE if i == 3 else NAVY, align=PP_ALIGN.CENTER)
    add_text(s, x, 5.0, 2.7, 0.24, small, size=9.5, color=RGBColor(0xC9, 0xD9, 0xE5) if i == 3 else GRAY, align=PP_ALIGN.CENTER)
    if i < 3:
        add_text(s, x + 2.72, 4.78, 0.3, 0.3, "›", size=22, bold=True, color=TEAL)

add_text(s, 0.62, 5.86, 12.0, 0.33, "Total unit target: 1.021.062  ·  Ritel 68,9%  ·  F&B 22,4%  ·  Jasa 8,8%", size=13, bold=True, color=NAVY)
add_text(s, 0.62, 6.28, 12.0, 0.5, "Dataset sektor memberi dimensi yang tidak ada di Tugas 2: jumlah unit Ritel, F&B, dan Jasa per kabupaten/kota.", size=10.5, color=GRAY)
add_footer(s, 3)

# ------------------------------------------------------------------ 4. ICP
s = prs.slides.add_slide(BLANK)
add_header(s, "03  ·  Metodologi", "Lima komponen, bobot tetap", "Bobot ditetapkan sebelum melihat hasil agar skor tidak disesuaikan ke kesimpulan.")
rows = [
    ("Ukuran Pasar", "Total unit Ritel + F&B + Jasa", "25%"),
    ("Kepadatan Sektor", "Unit target per 100.000 penduduk", "25%"),
    ("Kesiapan Digital", "IPM + pengeluaran per kapita", "20%"),
    ("Adopsi Digital", "Simpanan + tabungan per kapita", "15%"),
    ("Aktivitas Ekonomi", "PDRB per kapita 2024", "15%"),
]
add_table(s, 0.62, 1.85, 7.45, 3.7, ["Komponen", "Indikator", "Bobot"], rows, [2.45, 3.65, 1.35], font_size=10.2, header_size=9.5, row_h=0.6)
add_text(s, 0.62, 5.82, 7.4, 0.3, "Skor = Σ (bobot × komponen ternormalisasi)", size=12, bold=True, color=TEAL)
add_text(s, 0.62, 6.16, 7.4, 0.5, "Normalisasi Min-Max pada 30 wilayah; volume dan kepadatan sektor dinormalisasi ulang pada 90 segmen.", size=10, color=GRAY)

add_card(s, 8.45, 1.85, 4.25, 3.7, fill=LIGHT)
add_text(s, 8.72, 2.05, 3.7, 0.3, "PRINSIP", size=9.5, bold=True, color=TEAL)
add_bullets(s, 8.72, 2.4, 3.75, 2.9, [
    "Bobot tidak diubah setelah hasil keluar.",
    "Volume dan kepadatan dipisahkan dari kesiapan.",
    "Semua komponen diskalakan 0–1.",
    "Uji sensitivitas menjadi pengaman.",
], size=10.6, gap=5)
add_footer(s, 4)

# ------------------------------------------------------------------ 5. clusters
s = prs.slides.add_slide(BLANK)
add_header(s, "04  ·  Segmentasi", "Tiga tipe wilayah", "K-Means k=3 dipilih karena silhouette tertinggi dalam rentang wajib 3–5.")
clusters = [
    ("Hub Digital Matang", "3 wilayah", "Kota Semarang, Kota Surakarta, Kudus", "Digital 0,79 · Adopsi 0,69", TEAL),
    ("Sentra Perdagangan Padat", "14 wilayah", "Banyumas, Purbalingga, Rembang, dst.", "Ukuran 0,64 · Kepadatan 0,51", ORANGE),
    ("Wilayah Rintisan", "13 wilayah", "Banjarnegara, Kebumen, Wonosobo, dst.", "Digital 0,32 · Ukuran 0,21", GRAY),
]
for i, (name, count, areas, metric, color) in enumerate(clusters):
    y = 1.82 + i * 1.55
    add_card(s, 0.62, y, 6.6, 1.35, fill=LIGHT)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.62), Inches(y), Inches(0.08), Inches(1.35))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    add_text(s, 0.85, y + 0.13, 2.6, 0.28, name, size=11.5, bold=True, color=NAVY)
    add_text(s, 3.55, y + 0.11, 1.15, 0.3, count, size=10, bold=True, color=color, align=PP_ALIGN.RIGHT)
    add_text(s, 0.85, y + 0.48, 4.4, 0.3, areas, size=8.8, color=GRAY)
    add_text(s, 0.85, y + 0.88, 5.9, 0.3, metric, size=9.2, bold=True, color=DARK)

add_image_fit(s, FIG / "final_clusters_pca.png", 7.45, 1.72, 5.35, 4.55)
add_text(s, 7.45, 6.38, 5.35, 0.3, "Sebaran wilayah pada dua komponen utama (PCA).", size=8.5, color=GRAY, align=PP_ALIGN.CENTER)
add_footer(s, 5)

# ------------------------------------------------------------------ 6. profile
s = prs.slides.add_slide(BLANK)
add_header(s, "05  ·  Profil", "Kesiapan dan volume tidak berkorelasi sempurna", "Sentra perdagangan punya volume; hub digital punya daya beli dan adopsi.")
add_image_fit(s, FIG / "final_cluster_profile.png", 0.55, 1.55, 8.05, 4.75)
add_text(s, 0.55, 6.35, 8.05, 0.3, "Rata-rata komponen per tipe wilayah (skala 0–1).", size=8.5, color=GRAY, align=PP_ALIGN.CENTER)

add_card(s, 8.85, 1.65, 3.85, 4.6, fill=LIGHT)
add_text(s, 9.05, 1.83, 3.4, 0.3, "BACA CEPAT", size=9.2, bold=True, color=TEAL)
add_bullets(s, 9.05, 2.18, 3.4, 3.8, [
    "Hub digital: digital 0,79; adopsi 0,69; ekonomi 0,89.",
    "Sentra: ukuran 0,64; kepadatan 0,51; adopsi hanya 0,04.",
    "Rintisan: semua komponen rendah–menengah.",
    "Tiga motion SDR, bukan satu kampanye massal.",
], size=9.8, gap=6)
add_footer(s, 6)

# ------------------------------------------------------------------ 7. top5
s = prs.slides.add_slide(BLANK)
add_header(s, "06  ·  Prioritas", "Top 5 segmen", "Semua berada di Hub Digital Matang; konsentrasi tinggi, gelombang berikutnya sudah terlihat.")
rows = []
for _, r in top5.iterrows():
    rows.append([
        str(int(r["Peringkat"])),
        r["Sektor"],
        r["Wilayah"],
        f"{r['Skor Prioritas']:.3f}".replace(".", ","),
        f"{int(r['Estimasi Jumlah UMKM']):,}".replace(",", "."),
    ])
add_table(s, 0.62, 1.78, 8.0, 3.5, ["#", "Sektor", "Wilayah", "Skor", "Unit"], rows, [0.55, 1.25, 3.2, 1.2, 1.8], font_size=11, header_size=9.5, row_h=0.55)
add_text(s, 0.62, 5.55, 8.0, 0.3, "Kepadatan per 100k:", size=9.5, bold=True, color=GRAY)
add_text(s, 0.62, 5.86, 8.0, 0.55, "Ritel Semarang 1.202  ·  F&B Semarang 913  ·  Ritel Surakarta 1.870  ·  F&B Surakarta 1.187  ·  Jasa Semarang 405", size=9.3, color=DARK)

add_card(s, 8.95, 1.78, 3.75, 3.45, fill=CREAM, line=ORANGE)
add_text(s, 9.15, 1.97, 3.35, 0.3, "IMPLIKASI", size=9.2, bold=True, color=ORANGE)
add_bullets(s, 9.15, 2.3, 3.35, 2.75, [
    "Semarang: akuisisi volume.",
    "Surakarta: kepadatan merchant.",
    "Konsentrasi 3 wilayah = risiko.",
    "Banyumas, Purbalingga, Rembang: next wave.",
], size=9.6, gap=5)
add_footer(s, 7)

# ------------------------------------------------------------------ 8. baseline
s = prs.slides.add_slide(BLANK)
add_header(s, "07  ·  Baseline", "Volume vs kesiapan", "Top 5 ICP tidak beririsan dengan Top 5 volume: 0/5.")
add_image_fit(s, FIG / "final_baseline.png", 0.55, 1.78, 8.3, 4.55)
add_card(s, 9.1, 1.68, 3.55, 1.2, fill=LIGHT)
add_text(s, 9.3, 1.82, 3.1, 0.25, "OVERLAP TOP 5", size=8.8, bold=True, color=GRAY)
add_text(s, 9.3, 2.05, 3.1, 0.55, "0 / 5", size=27, bold=True, color=ORANGE)
add_card(s, 9.1, 3.02, 3.55, 1.3, fill=LIGHT)
add_text(s, 9.3, 3.16, 3.1, 0.25, "SPEARMAN ρ", size=8.8, bold=True, color=GRAY)
add_text(s, 9.3, 3.4, 3.1, 0.55, "0,738", size=24, bold=True, color=NAVY)
add_text(s, 9.1, 4.62, 3.55, 1.4, "Arah peringkat sama, tetapi ujung distribusi berbeda. Baseline mengabaikan kesiapan digital dan kepadatan.", size=9.5, color=GRAY)
add_footer(s, 8)

# ------------------------------------------------------------------ 9. sensitivity
s = prs.slides.add_slide(BLANK)
add_header(s, "08  ·  Ketahanan", "Skor stabil, posisi 4–5 sensitif", "ρ > 0,97; overlap Top 5 turun ke 3/5 saat bobot digital/adopsi/PDRB diturunkan.")
add_image_fit(s, FIG / "final_sensitivity.png", 0.55, 1.52, 8.35, 4.85)
add_card(s, 9.15, 1.7, 3.5, 1.35, fill=LIGHT)
add_text(s, 9.35, 1.84, 3.05, 0.25, "PALING RENTAN", size=8.8, bold=True, color=GRAY)
add_text(s, 9.35, 2.08, 3.05, 0.45, "3/5", size=25, bold=True, color=ORANGE)
add_text(s, 9.35, 2.55, 3.05, 0.3, "saat bobot diturunkan", size=9, color=GRAY)
add_text(s, 9.15, 3.35, 3.5, 2.0, "Tiga nama teratas relatif aman untuk keputusan kuartalan. Posisi keempat dan kelima perlu divalidasi dengan data pipeline.", size=9.5, color=DARK)
add_footer(s, 9)

# ------------------------------------------------------------------ 10. scraping
s = prs.slides.add_slide(BLANK)
add_header(s, "09  ·  Legalitas", "Tidak semua data publik boleh di-scrape", "Robots.txt dan ToS diperiksa 2 November 2026.")
rows = []
for _, r in scraping.iterrows():
    rows.append([r["Sumber"], r["Status_Robots"], r["Status_ToS"], r["Status_Kelayakan"], r["Rekomendasi"]])
add_table(s, 0.55, 1.68, 12.2, 4.55, ["Sumber", "robots.txt", "ToS", "Status", "Jalur"], rows, [3.05, 1.65, 1.65, 1.35, 4.5], font_size=8.6, header_size=8.4, row_h=0.62)
add_text(s, 0.55, 6.4, 12.2, 0.3, "Google Maps/LinkedIn/Tokopedia/Shopee: jangan scrape. OSM: planet.osm/ekstrak. Dinkop: unduhan resmi + atribusi.", size=9.3, bold=True, color=TEAL)
add_footer(s, 10)

# ------------------------------------------------------------------ 11. SDR
s = prs.slides.add_slide(BLANK)
add_header(s, "10  ·  Eksekusi", "Tiga motion SDR", "Satu kampanye massal tidak cocok untuk tiga tipe wilayah yang berbeda.")
tiers = [
    ("TIER A", "Top 5 segmen", "Kota Semarang & Surakarta", "Demo AI Analytics; pilot 30 hari; integrasi POS", "Direct sales; komunitas merchant; referral", TEAL),
    ("TIER B", "14 Sentra Perdagangan", "Banyumas, Purbalingga, Rembang, dst.", "POS basic; onboarding; literasi digital", "Dinas/koperasi; komunitas pasar; agen lokal", ORANGE),
    ("TIER C", "13 Wilayah Rintisan", "Banjarnegara, Kebumen, Wonosobo, dst.", "Produk ringan; uji coba; edukasi", "Event UMKM; mitra lokal; konten", GRAY),
]
for i, (tier, target, areas, offer, channel, color) in enumerate(tiers):
    x = 0.62 + i * 4.12
    add_card(s, x, 1.72, 3.78, 4.8, fill=LIGHT)
    add_text(s, x + 0.2, 1.88, 1.2, 0.28, tier, size=9.5, bold=True, color=color)
    add_text(s, x + 0.2, 2.18, 3.4, 0.3, target, size=13.5, bold=True, color=NAVY)
    add_text(s, x + 0.2, 2.55, 3.4, 0.55, areas, size=8.8, color=GRAY)
    add_rule(s, x + 0.2, 3.18, 3.35, LINE, 0.8)
    add_text(s, x + 0.2, 3.3, 3.4, 0.25, "PENAWARAN", size=7.8, bold=True, color=GRAY)
    add_text(s, x + 0.2, 3.55, 3.4, 0.8, offer, size=9.2, color=DARK)
    add_text(s, x + 0.2, 4.45, 3.4, 0.25, "CHANNEL", size=7.8, bold=True, color=GRAY)
    add_text(s, x + 0.2, 4.7, 3.4, 0.8, channel, size=9.2, color=DARK)

add_text(s, 0.62, 6.72, 12.0, 0.3, "Metrik: conversion to pilot · activation · retensi 30/90 hari · CAC payback", size=9.5, bold=True, color=TEAL)
add_footer(s, 11)

# ------------------------------------------------------------------ 12. close
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()
accent = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, 0.16, prs.slide_height)
accent.fill.solid()
accent.fill.fore_color.rgb = ORANGE
accent.line.fill.background()

add_text(s, 0.85, 0.72, 5.0, 0.3, "KESIMPULAN", size=10.5, bold=True, color=RGBColor(0x9F, 0xC5, 0xD3))
add_text(s, 0.85, 1.2, 11.5, 1.4, "Cari yang siap,\nbukan yang paling besar.", size=31, bold=True, color=WHITE, spacing=0.95)
add_text(s, 0.85, 2.92, 6.2, 0.8, "Ritel & F&B Kota Semarang dan Kota Surakarta adalah kandidat pilot terkuat.", size=13.5, color=RGBColor(0xD9, 0xE6, 0xEF), spacing=1.12)

actions = [
    ("01", "Pilot 10–15 merchant Ritel/F&B di Kota Semarang."),
    ("02", "Replikasi di Kota Surakarta dengan motion komunitas."),
    ("03", "Uji POS basic di 3–5 kabupaten Sentra Perdagangan."),
    ("04", "Bangun pipeline edukasi di Wilayah Rintisan."),
]
for i, (num, text) in enumerate(actions):
    y = 4.05 + i * 0.56
    add_text(s, 0.85, y, 0.45, 0.3, num, size=10.5, bold=True, color=ORANGE)
    add_text(s, 1.35, y - 0.02, 5.8, 0.45, text, size=10.8, color=WHITE)

add_card(s, 7.55, 3.95, 4.95, 1.75, fill=RGBColor(0x21, 0x4A, 0x70))
add_text(s, 7.78, 4.12, 4.5, 0.3, "NEXT STEP", size=8.8, bold=True, color=RGBColor(0x9F, 0xC5, 0xD3))
add_text(s, 7.78, 4.42, 4.5, 1.0, "Validasi Top 5 dengan data pipeline internal, jalankan pilot 30 hari, lalu kalibrasi bobot setiap kuartal.", size=10.5, color=WHITE, spacing=1.1)

add_text(s, 0.85, 6.75, 8.0, 0.3, "Kelompok 13  ·  Ayu Safitri  ·  Carissa Zia  ·  Gerard Harjuno", size=9.5, color=RGBColor(0xB8, 0xCD, 0xDB))

prs.save(OUT)
print("Wrote", OUT, "slides:", len(prs.slides))
