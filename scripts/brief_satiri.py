#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brief Excel'ini kurar ve kategori satırlarını doldurur.

Excel, içerik yazılacak tüm kategori sayfalarını kategori tipine göre sekmelere ayrılmış olarak taşır
(Kategori, Kadın, Erkek, Çocuk, Bebek, Marka). Her sayfa bir satırdır; "Brief" sütunu başlangıçta "Bekliyor"dur.
Bir kategorinin briefi hazırlandığında ilgili satır doldurulur ve "Hazır" olur.

Kullanım:
    python3 brief_satiri.py --xlsx "Boyner kategori içerik briefleri.xlsx" --kur          # sekmeleri envanterden kur
    python3 brief_satiri.py --xlsx "Boyner kategori içerik briefleri.xlsx" --json satir.json
    python3 brief_satiri.py --xlsx "..." --ozet                                          # sekme başına hazır / bekleyen

--kur var olan dosyada doldurulmuş satırları korur; yalnız eksik sayfaları ekler. Envanterde bulunmayan bir
URL'nin briefi gelirse (sitemap ana ağaçtaki bazı sayfaları taşımıyor) satır ilgili sekmenin sonuna eklenir.

satir.json biçimi (çok satırlı metinler "\\n" ile):
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import url_coz

INK, HEAD, FN = "FF10332F", "434343", "Calibri"
SEKMELER = ["Kategori", "Kadın", "Erkek", "Çocuk", "Bebek", "Marka"]
CINS_SEKME = {"3731": "Kadın", "25462663": "Kadın", "3730": "Erkek", "3733": "Çocuk", "3734": "Çocuk",
              "214747": "Bebek", "214763": "Bebek"}
BASLIK = ["Kategori", "URL", "Brief", "Main KW", "Main KW Hacim", "İkincil ve Uzun Kuyruk Kelimeler", "Alt Başlıklar",
          "İçerik Kurgusu", "Link Verilecek Sayfalar", "Kapsam Dışı Kelimeler (Sahibi Başka Sayfa)", "SSS'ler",
          "Yanıt Biçimi", "Mevcut Durum"]
GENISLIK = [26, 44, 11, 18, 12, 38, 48, 130, 72, 62, 66, 56, 44]
ANAHTAR = ["kategori", "url", "brief", "main_kw", "hacim", "ikincil", "basliklar", "kurgu", "link", "kapsam_disi",
           "sss", "yanit", "durum"]
ZORUNLU = [k for k in ANAHTAR if k != "brief"]
ORTALI = {"hacim", "brief"}


def sekme_adi(url):
    p = url_coz(url) or {}
    if p.get("b"):
        return "Marka"          # marka sayfaları envanterden toplu eklenmez; brief hazırlandıkça satır açılır
    return CINS_SEKME.get(p.get("g"), "Kategori")


def satir_sayisi(metin, genislik):
    kap = max(1, int(genislik * 1.15))
    return sum(max(1, math.ceil(len(p) / kap)) for p in str(metin).split("\n"))


def sekme_kur(wb, ad):
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
    ws = wb.create_sheet(ad)
    for c, b in enumerate(BASLIK, start=1):
        h = ws.cell(row=1, column=c, value=b)
        h.font = Font(name=FN, size=11, bold=True, color="FFFFFF")
        h.fill = PatternFill("solid", fgColor=HEAD)
        h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = GENISLIK[c - 1]
    ws.row_dimensions[1].height = 36
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(BASLIK))}1"
    return ws


def hucre(ws, r, c, deger, k):
    from openpyxl.styles import Font, Alignment
    cell = ws.cell(row=r, column=c, value=deger)
    cell.font = Font(name=FN, size=10, color=INK)
    cell.alignment = Alignment(horizontal="center" if k in ORTALI else "left", vertical="center", wrap_text=True)
    return cell


def ac(yol):
    from openpyxl import Workbook, load_workbook
    if os.path.exists(yol):
        wb = load_workbook(yol, rich_text=True)
    else:
        wb = Workbook(); wb.remove(wb.active)
    for ad in SEKMELER:
        if ad not in wb.sheetnames:
            sekme_kur(wb, ad)
    return wb


def url_satiri(wb, url):
    for ws in wb.worksheets:
        for r in range(2, ws.max_row + 1):
            if str(ws.cell(row=r, column=2).value or "").strip() == url:
                return ws, r
    return None, None


def kur(yol):
    import envanter
    wb = ac(yol)
    var = {str(ws.cell(row=r, column=2).value).strip() for ws in wb.worksheets for r in range(2, ws.max_row + 1)
           if ws.cell(row=r, column=2).value}
    sayfalar = [s for s in envanter.yukle() if s["kaynak"] in ("category", "gender_category")
                and "/kampanya/" not in s["url"] and not s["slug"].startswith("outlet")]
    eklenen = {ad: 0 for ad in SEKMELER}
    for s in sorted(sayfalar, key=lambda s: s["slug"]):
        if s["url"] in var:
            continue
        ws = wb[sekme_adi(s["url"])]
        r = ws.max_row + 1
        # Ad slug'dan üretilir (Türkçe karaktersiz); brief hazırlanınca sayfanın gerçek adıyla değişir.
        hucre(ws, r, 1, s["slug"].replace("-", " ").title(), "kategori")
        hucre(ws, r, 2, s["url"], "url").hyperlink = s["url"]
        hucre(ws, r, 3, "Bekliyor", "brief")
        eklenen[ws.title] += 1
    wb.save(yol)
    print(f"{yol} kuruldu · eklenen: " + ", ".join(f"{k} {v}" for k, v in eklenen.items()))


def ozet(yol):
    wb = ac(yol)
    for ws in wb.worksheets:
        d = [ws.cell(row=r, column=3).value for r in range(2, ws.max_row + 1) if ws.cell(row=r, column=2).value]
        print(f"{ws.title:10s} toplam {len(d):5d} · hazır {d.count('Hazır'):4d} · bekleyen {d.count('Bekliyor'):5d}")
        for r in range(2, ws.max_row + 1):
            if ws.cell(row=r, column=3).value == "Hazır":
                print(f"   hazır: {ws.cell(row=r, column=1).value} · {ws.cell(row=r, column=2).value}")


def main():
    from openpyxl.styles import PatternFill
    from openpyxl.cell.rich_text import CellRichText, TextBlock
    from openpyxl.cell.text import InlineFont

    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--json")
    ap.add_argument("--kur", action="store_true")
    ap.add_argument("--ozet", action="store_true")
    a = ap.parse_args()
    if a.kur:
        return kur(a.xlsx)
    if a.ozet:
        return ozet(a.xlsx)
    if not a.json:
        sys.exit("--json, --kur ya da --ozet gerekli")
    d = json.load(open(a.json, encoding="utf-8"))
    eksik = [k for k in ZORUNLU if k not in d]
    if eksik:
        sys.exit(f"satir.json içinde eksik alan: {', '.join(eksik)}")
    d["brief"] = "Hazır"

    wb = ac(a.xlsx)
    ws, r = url_satiri(wb, d["url"])
    guncelle = ws is not None
    if ws is None:
        ws = wb[sekme_adi(d["url"])]
        r = ws.max_row + 1
    for c, k in enumerate(ANAHTAR, start=1):
        deger = d[k]
        if k == "kurgu" and d.get("kurgu_kalin"):
            kalin = str(d["kurgu_kalin"]).lstrip()
            if not str(d["kurgu"])[-1:].isspace():
                kalin = " " + kalin
            deger = CellRichText([TextBlock(InlineFont(rFont=FN, sz=10, b=False, color=INK), str(d["kurgu"])),
                                  TextBlock(InlineFont(rFont=FN, sz=10, b=True, color=INK), kalin)])
        cell = hucre(ws, r, c, deger, k)
        if k == "hacim":
            cell.number_format = "#,##0"
        if k == "url":
            cell.hyperlink = d["url"]
        if k == "brief":
            cell.fill = PatternFill("solid", fgColor="C8E6C9")
    en = max(satir_sayisi(str(d[k]) + str(d.get("kurgu_kalin", "") if k == "kurgu" else ""), GENISLIK[i])
             for i, k in enumerate(ANAHTAR))
    ws.row_dimensions[r].height = min(409, max(30, round(en * 13.2)))
    wb.save(a.xlsx)
    print(f"{a.xlsx} · sekme '{ws.title}' · {r}. satır · '{d['kategori']}' "
          f"{'dolduruldu' if guncelle else 'eklendi (envanterde yoktu)'}")
    if en * 13.2 > 409:
        print("UYARI: en uzun hücre 409 punto satır sınırını aşıyor (yaklaşık 30 satır); metnin tamamı ekranda "
              "görünmeyebilir. Kurgu satırları telgraf üslubuyla kısaltılabilir.")


if __name__ == "__main__":
    main()
