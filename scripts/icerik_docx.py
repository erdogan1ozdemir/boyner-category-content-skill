#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kategori içeriğini Word dosyasına basar (okuma ve onay kopyası).

Kullanım:
    python3 icerik_docx.py --json icerik.json --klasor "Kategori İçerik"     

Belge adı "{slug}: {tam URL}" biçimindedir (ör. "kadin-mont: https://www.boyner.com.tr/kadin-mont-x-g3731-c23896554");
başlık satırına, belge özelliklerine ve dosya adına yazılır (dosya adında ":" ve "/" yerine görünüşü aynı olan
∶ ve ∕ karakterleri kullanılır).

icerik.json biçimi:
{
  "kategori": "Kadın Mont",
  "url": "https://www.boyner.com.tr/kadin-mont-x-g3731-c23896554",
  "main_kw": "kadın mont",
  "meta": "İç künye; belgeye BASILMAZ",
  "linkler": {"LINK1": ["anchor metni", "https://www.boyner.com.tr/..."]},
  "govde": [["p","Başlıksız giriş paragrafı, içinde [LINK1] geçebilir"],
            ["H2","Başlık"], ["H3","Alt başlık"], ["mad","Madde imli madde"], ["li","Numaralı adım"],
            ["p","Vurgu için **kalın metin**"], ["tablo", [["Sütun","Sütun"],["hücre","hücre"]]]],
  "sss": [["Soru?","Yanıt"]]
}
Sayfada H1 kategori adı olarak bulunduğu için belgeye H1 yazılmaz; gövde başlıksız girişle açılır.
Kaynak notu ve künye belgeye basılmaz; kullanıcıya sohbette söylenir.
"""
import argparse, json, re

INK, LINK, FN = "1A1A1A", "0B5FB0", "Calibri"


def renk(run, hex_kod):
    from docx.shared import RGBColor
    run.font.color.rgb = RGBColor.from_string(hex_kod)


def kopru(p, metin, url, boyut):
    from docx.oxml.shared import OxmlElement, qn
    r_id = p.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                            is_external=True)
    h = OxmlElement("w:hyperlink"); h.set(qn("r:id"), r_id)
    r = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    for etiket, deger in (("w:color", LINK), ("w:u", "single")):
        e = OxmlElement(etiket); e.set(qn("w:val"), deger); rPr.append(e)
    rf = OxmlElement("w:rFonts"); rf.set(qn("w:ascii"), FN); rf.set(qn("w:hAnsi"), FN); rPr.append(rf)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(boyut * 2))); rPr.append(sz)
    r.append(rPr)
    t = OxmlElement("w:t"); t.text = metin; t.set(qn("xml:space"), "preserve"); r.append(t)
    h.append(r); p._p.append(h)


def metni_bas(p, metin, linkler, boyut=10.5):
    from docx.shared import Pt
    for parca in re.split(r"(\[LINK\d+\]|\*\*[^*]+\*\*)", metin):
        m = re.fullmatch(r"\[(LINK\d+)\]", parca)
        if m and m.group(1) in linkler:
            kopru(p, linkler[m.group(1)][0], linkler[m.group(1)][1], boyut)
        elif parca.startswith("**") and parca.endswith("**") and len(parca) > 4:
            r = p.add_run(parca[2:-2]); r.bold = True; r.font.name = FN; r.font.size = Pt(boyut); renk(r, INK)
        elif parca:
            r = p.add_run(parca); r.font.name = FN; r.font.size = Pt(boyut); renk(r, INK)


def belge_adi(url):
    m = re.search(r"boyner\.com\.tr/(?:.*/)?(.+?)-x-[bgc0-9-]+", url)
    return m.group(1) if m else re.sub(r"\W+", "-", url).strip("-")


def dosya_adi(url):
    """Dosya adı da belge adıyla aynı görünür: "kadin-mont: https://www.boyner.com.tr/...".
    Dosya sistemleri adında ":" ve "/" kabul etmediği için görünüşü aynı olan Unicode karakterleri
    kullanılır: ∶ (U+2236) ve ∕ (U+2215). Belgenin içindeki başlık satırı ve belge özellikleri gerçek
    karakterleri taşır."""
    return f"{belge_adi(url)}: {url}".replace(":", "\u2236").replace("/", "\u2215") + ".docx"


def main():
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.shared import OxmlElement, qn

    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--out", help="çıktı yolu; verilmezse çalışma klasörüne {slug}.docx")
    ap.add_argument("--klasor", default=".", help="--out verilmediğinde dosyanın yazılacağı klasör")
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    import os
    a.out = a.out or os.path.join(a.klasor, dosya_adi(d["url"]))
    linkler = {k: tuple(v) for k, v in (d.get("linkler") or {}).items()}

    doc = Document()
    st = doc.styles["Normal"]; st.font.name = FN; st.font.size = Pt(10.5)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2); s.left_margin = s.right_margin = Cm(2)

    # Belge adı: "{slug}: {tam URL}" (kullanıcı kararı 02.10.2026). Dosya adında ":" ve "/" kullanılamadığı için
    # dosya "{slug}.docx" olarak kaydedilir; belge adı başlık satırında ve belge özelliklerinde tam haliyle durur.
    ad = belge_adi(d["url"])
    doc.core_properties.title = f"{ad}: {d['url']}"
    p = doc.add_paragraph(); r = p.add_run(f"{ad}: "); r.bold = True; r.font.size = Pt(13); r.font.name = FN; renk(r, INK)
    kopru(p, d["url"], d["url"], 13)

    def baslik(metin, seviye):
        p = doc.add_paragraph(style="Heading 1" if seviye == 2 else "Heading 2")
        p.paragraph_format.space_before = Pt(14 if seviye == 2 else 11); p.paragraph_format.space_after = Pt(5)
        r = p.add_run(metin); r.bold = True; r.font.name = FN; r.font.size = Pt(13 if seviye == 2 else 11.5); renk(r, INK)

    for tip, icerik in d["govde"]:
        if tip in ("H2", "H3"):
            baslik(icerik, int(tip[1]))
        elif tip == "tablo":
            t = doc.add_table(rows=0, cols=len(icerik[0])); t.style = "Table Grid"
            for i, satir in enumerate(icerik):
                hucreler = t.add_row().cells
                for j, deger in enumerate(satir):
                    hucreler[j].text = ""
                    par = hucreler[j].paragraphs[0]
                    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    if i == 0:
                        rr = par.add_run(str(deger)); rr.font.name = FN; rr.font.size = Pt(9.5); rr.bold = True
                        renk(rr, "FFFFFF")
                        sh = OxmlElement("w:shd"); sh.set(qn("w:fill"), "434343"); sh.set(qn("w:val"), "clear")
                        hucreler[j]._tc.get_or_add_tcPr().append(sh)
                    else:
                        metni_bas(par, str(deger), linkler, 9.5)
            doc.add_paragraph()
        elif tip in ("li", "mad"):
            p = doc.add_paragraph(style="List Number" if tip == "li" else "List Bullet")
            p.paragraph_format.space_after = Pt(3); metni_bas(p, icerik, linkler)
        else:
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(7); metni_bas(p, icerik, linkler)

    if d.get("sss"):
        baslik(d.get("sss_baslik") or f"{d['kategori']} Hakkında Sık Sorulan Sorular", 2)
        for soru, yanit in d["sss"]:
            baslik(soru, 3)
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4); metni_bas(p, yanit, linkler)

    doc.save(a.out)
    duz = lambda i: re.sub(r"\*\*", "", re.sub(r"\[LINK\d+\]", "x", i))
    kelime = sum(len(duz(i).split()) for t, i in d["govde"] if t in ("p", "li", "mad"))
    sss_k = sum(len(duz(c).split()) for _, c in d.get("sss", []))
    print(f"yazıldı: {a.out} · gövde {kelime} kelime + SSS {sss_k} kelime · "
          f"{sum(1 for t, _ in d['govde'] if t == 'H2')} H2 · {sum(1 for t, _ in d['govde'] if t == 'H3')} H3 · "
          f"{len(linkler)} link · {len(d.get('sss', []))} SSS")


if __name__ == "__main__":
    main()
