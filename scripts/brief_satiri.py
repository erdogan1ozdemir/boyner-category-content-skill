#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brief Excel'ine bir kategori satırı ekler (ya da aynı URL'nin satırını günceller). Biçimi kendisi kurar.

Kullanım:
    python3 brief_satiri.py --xlsx "Boyner kategori içerik briefleri.xlsx" --json satir.json

satir.json biçimi (çok satırlı metinler "\\n" ile; ilk on bir alan zorunlu):
{
  "kategori": "Kadın Mont",
  "url": "https://www.boyner.com.tr/kadin-mont-x-g3731-c23896554",
  "main_kw": "kadın mont",
  "hacim": 33100,
  "ikincil": "kelime (hacim)\\nkelime (hacim)",
  "basliklar": "H2: ...\\nH3: ...",
  "kurgu": "TON: ...\\n\\nAÇILIŞ: ...",
  "kurgu_kalin": "(isteğe bağlı) DİKKAT'in sonuna kalın basılacak koşullu uyarı",
  "link": "1. anchor : https://...\\n   yerleşeceği bölüm ve cümle",
  "kapsam_disi": "kelime (hacim) -> sahibi olan sayfa",
  "sss": "1. Soru?\\n   Yanıtta: ...",
  "yanit": "• Her yanıt ...",
  "durum": "Sayfa tipi, ürün sayısı, mevcut içerik, sıralama, GSC özeti"
}
"""
import argparse, json, math, os, sys

INK, HEAD, FN = "FF10332F", "434343", "Calibri"
SEKME = "Kategori Briefleri"
BASLIK = ["Kategori", "URL", "Main KW", "Main KW Hacim", "İkincil ve Uzun Kuyruk Kelimeler", "Alt Başlıklar",
          "İçerik Kurgusu", "Link Verilecek Sayfalar", "Kapsam Dışı Kelimeler (Sahibi Başka Sayfa)", "SSS'ler",
          "Yanıt Biçimi", "Mevcut Durum"]
GENISLIK = [20, 34, 18, 12, 38, 48, 130, 72, 62, 66, 56, 44]
ANAHTAR = ["kategori", "url", "main_kw", "hacim", "ikincil", "basliklar", "kurgu", "link", "kapsam_disi", "sss",
           "yanit", "durum"]


def satir_sayisi(metin, genislik):
    kap = max(1, int(genislik * 1.15))
    return sum(max(1, math.ceil(len(p) / kap)) for p in str(metin).split("\n"))


def main():
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.cell.rich_text import CellRichText, TextBlock
    from openpyxl.cell.text import InlineFont
    from openpyxl.utils import get_column_letter

    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--json", required=True)
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    eksik = [k for k in ANAHTAR if k not in d]
    if eksik:
        sys.exit(f"satir.json içinde eksik alan: {', '.join(eksik)}")

    if os.path.exists(a.xlsx):
        wb = load_workbook(a.xlsx, rich_text=True)
        ws = wb[SEKME] if SEKME in wb.sheetnames else wb.active
    else:
        wb = Workbook(); ws = wb.active; ws.title = SEKME
        for c, b in enumerate(BASLIK, start=1):
            h = ws.cell(row=1, column=c, value=b)
            h.font = Font(name=FN, size=11, bold=True, color="FFFFFF")
            h.fill = PatternFill("solid", fgColor=HEAD)
            h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[1].height = 36
        for i, w in enumerate(GENISLIK, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "C2"

    # aynı URL'nin satırı varsa güncellenir; yoksa ilk boş satıra yazılır
    r = next((i for i in range(2, ws.max_row + 1) if str(ws.cell(row=i, column=2).value or "").strip() == d["url"]), None)
    guncelle = r is not None
    if r is None:
        r = ws.max_row + 1
        if ws.cell(row=ws.max_row, column=1).value in (None, "") and ws.max_row > 1:
            r = ws.max_row
    for c, k in enumerate(ANAHTAR, start=1):
        deger = d[k]
        if k == "kurgu" and d.get("kurgu_kalin"):
            kalin = str(d["kurgu_kalin"]).lstrip()
            if not str(d["kurgu"])[-1:].isspace():
                kalin = " " + kalin
            deger = CellRichText([TextBlock(InlineFont(rFont=FN, sz=10, b=False, color=INK), str(d["kurgu"])),
                                  TextBlock(InlineFont(rFont=FN, sz=10, b=True, color=INK), kalin)])
        cell = ws.cell(row=r, column=c, value=deger)
        cell.font = Font(name=FN, size=10, color=INK)
        cell.alignment = Alignment(horizontal="center" if k == "hacim" else "left", vertical="center", wrap_text=True)
        if k == "hacim":
            cell.number_format = "#,##0"
        if k == "url":
            cell.hyperlink = d["url"]

    en = max(satir_sayisi(str(d[k]) + str(d.get("kurgu_kalin", "") if k == "kurgu" else ""), GENISLIK[i])
             for i, k in enumerate(ANAHTAR))
    ws.row_dimensions[r].height = min(409, max(30, round(en * 13.2)))
    wb.save(a.xlsx)
    print(f"{a.xlsx} · {r}. satır · '{d['kategori']}' {'güncellendi' if guncelle else 'eklendi'}")
    if en * 13.2 > 409:
        print("UYARI: en uzun hücre 409 punto satır sınırını aşıyor (yaklaşık 30 satır); metnin tamamı ekranda "
              "görünmeyebilir. Kurgu satırları telgraf üslubuyla kısaltılabilir.")


if __name__ == "__main__":
    main()
