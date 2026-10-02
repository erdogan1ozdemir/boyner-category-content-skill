#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bir boyner.com.tr listeleme sayfasının canlı kaydını okur: meta, mevcut içerik, ürün gamı.

Sayfa Next.js ile sunulur; her şey HTML içindeki __NEXT_DATA__ JSON'unda durur:
  filters.resolvedPage      -> Title, Description, H1, CanonicalUrl, PageType, Content (mevcut SEO metni)
  getProducts(...)          -> Breadcrumbs, TotalCount, ilk sayfadaki ürünler
  getFilters(...)           -> alt kategoriler, markalar, ürün çeşidi, renk, materyal, kalıp... (gerçek ürün gamı)
  getCloudLinking(...)      -> sayfanın altındaki link bulutu

Bu kayıt içeriğin zeminidir: metinde anılan alt kategori, marka, renk, materyal ve kalıp, sayfada gerçekten
filtrelenebilen değerlerden seçilir. Sayfada olmayan ürün tipi yazılmaz.

Kullanım:
    python3 kategori.py URL                       # özet (insan okur)
    python3 kategori.py URL --cikti kayit.json    # tam kayıt (içerik HTML'i dahil)
    python3 kategori.py URL --icerik              # mevcut içeriği düz metin olarak basar
"""
import argparse, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import getir, url_coz, SITE, CINSIYET

ATLA = {"categories", "marka", "satici", "priceFilter", "urunPuani", "trueFalseFilter", "cinsiyet"}
KIRLI = {"", "-", "belirtilmemis", "belirtilmemiş", "diger", "diğer"}


def metne(h):
    h = re.sub(r"<(br|/p|/div|/h\d|/li)[^>]*>", "\n", h or "", flags=re.I)
    return re.sub(r"[ \t\xa0]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def icerik_analizi(c):
    c = c or ""
    duz_ = metne(c)
    basliklar = [(t.upper(), metne(x)) for t, x in re.findall(r"<(h[1-6])[^>]*>(.*?)</\1>", c, re.S | re.I)]
    linkler = [(metne(a), html.unescape(u)) for u, a in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', c, re.S | re.I)]
    linkler = [(a, u) for a, u in linkler if a]
    return {"kelime": len(duz_.split()), "basliklar": basliklar, "linkler": linkler,
            "liste": len(re.findall(r"<(ul|ol)\b", c, re.I)), "tablo": len(re.findall(r"<table\b", c, re.I)),
            "soru_baslik": sum(1 for _, b in basliklar if b.rstrip().endswith("?")),
            "sss": bool(re.search(r"sık\w* sorulan|sıkça sorulan|\bSSS\b", duz_, re.I)),
            "siz": len(re.findall(r"\w+(?:abilirsiniz|ebilirsiniz|ınız|iniz|unuz|ünüz)\b", duz_)),
            "sen": len(re.findall(r"\w+(?:abilirsin|ebilirsin)\b", duz_)),
            "metin": duz_}


def oku(url):
    p = url_coz(url)
    tam = p["url"] if p else url
    h = getir(tam)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
    if not m:
        return {"url": tam, "hata": "sayfa okunamadı (Cloudflare doğrulaması ya da farklı sayfa tipi)"}
    st = json.loads(m.group(1))["props"]["pageProps"]["initialState"]
    rp = st["filters"]["resolvedPage"] or {}
    k = {"url": tam, "sayfa_tipi": rp.get("PageType"), "durum": rp.get("StatusCode"),
         "yonlendirme": rp.get("RedirectUrl"), "title": rp.get("Title"), "description": rp.get("Description"),
         "h1": rp.get("H1"), "canonical": rp.get("CanonicalUrl"), "index": rp.get("MetaRobots"),
         "html_title": (re.search(r"<title[^>]*>(.*?)</title>", h, re.S) or [None, None])[1],
         "icerik_html": rp.get("Content") or ""}
    k["canonical_kendisi"] = (not k["canonical"]) or k["canonical"].rstrip("/") == tam.split("?")[0].rstrip("/")
    k["icerik"] = icerik_analizi(k["icerik_html"])
    if p and p.get("g"):
        k["cinsiyet"] = CINSIYET.get(p["g"], p["g"])
    for anahtar, v in (st.get("dsListingSearchService", {}).get("queries") or {}).items():
        d = v.get("data") or {}
        if anahtar.startswith("getProducts"):
            k["breadcrumb"] = [(b["Title"], SITE + b["Url"]) for b in d.get("Breadcrumbs") or []]
            k["urun_sayisi"] = d.get("TotalCount")
            urun = d.get("Products") or []
            k["ornek_urunler"] = [f"{u.get('Brand')} · {u.get('Title')}" for u in urun[:12]]
        elif anahtar.startswith("getFilters"):
            k["urun_sayisi"] = k.get("urun_sayisi") or d.get("TotalCount")
            k["filtreler"] = {}
            for f in d.get("Filters") or []:
                deger = [(a.get("DisplayName"), a.get("SpecialLink")) for a in f.get("Attributes") or []]
                if f["Name"] == "categories":
                    k["alt_kategoriler"] = [(ad, SITE + l) for ad, l in deger if l]
                elif f["Name"] == "marka":
                    k["markalar"] = [(ad, SITE + l) for ad, l in deger if l]
                elif f["Name"] == "cinsiyet":
                    k["cinsiyetler"] = [ad for ad, _ in deger]
                elif f["Name"] == "priceFilter":
                    k["fiyat_filtresi"] = True          # içerikte "fiyat aralığı filtresi" yalnız bu True ise anılır
                elif f["Name"] == "trueFalseFilter":
                    k["secenek_filtreleri"] = [ad for ad, _ in deger]      # Kargo Bedava, Yarın Kargoda...
                elif f["Name"] not in ATLA:
                    k["filtreler"][f.get("DisplayName")] = [ad for ad, _ in deger
                                                             if (ad or "").strip().lower() not in KIRLI][:40]
            k["hizli_filtreler"] = [a.get("DisplayName") for a in d.get("FastFilterAttributes") or []]
            k["siralama"] = [o.get("DisplayName") or o.get("Name") for o in d.get("OrderOptions") or [] if isinstance(o, dict)]
    for anahtar, v in (st.get("dsSharedService", {}).get("queries") or {}).items():
        if anahtar.startswith("getCloudLinking") and v.get("data"):
            k["link_bulutu"] = [(c["Title"], SITE + c["Link"]) for grup in v["data"] for c in grup.get("CloudLinking") or []]
    return k


def gam(k, n=12):
    """Ürün gamı özeti: en çok ürünü olan kırılımları (marka sayfasında alt kategoriler, kategori sayfasında
    markalar) tek tek okuyup ürün sayısını ve örnek ürün adlarını toplar. İçerik mevcut gamı anlatır;
    gamda ağırlığı olan öne alınır. Cloudflare'e takılmamak için istekler arasında beklenir."""
    import time
    liste = (k.get("alt_kategoriler") if k.get("sayfa_tipi") == "Brand" else k.get("markalar")) or []
    out = []
    for ad, u in liste[:n]:
        time.sleep(1.5)
        c = oku(u)
        if c.get("hata"):
            out.append({"ad": ad, "url": u, "hata": c["hata"]}); continue
        out.append({"ad": ad, "url": u, "urun": c.get("urun_sayisi"), "index": c.get("index"),
                    "canonical_kendisi": c.get("canonical_kendisi"), "ornek": c.get("ornek_urunler")})
    return sorted(out, key=lambda x: -(x.get("urun") or 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--gam", type=int, nargs="?", const=12, default=0,
                    help="ilk N kırılımın (marka ya da alt kategori) ürün sayısını ve örnek ürünlerini topla (yavaş)")
    ap.add_argument("--cikti")
    ap.add_argument("--icerik", action="store_true")
    a = ap.parse_args()
    k = oku(a.url)
    if a.gam and not k.get("hata"):
        k["gam"] = gam(k, a.gam)
    if a.cikti:
        json.dump(k, open(a.cikti, "w"), ensure_ascii=False, indent=2)
    if k.get("hata"):
        sys.exit(k["hata"])
    if a.icerik:
        print(k["icerik"]["metin"] or "(sayfada içerik yok)"); return
    i = k["icerik"]
    print(f"URL        : {k['url']}")
    print(f"Tip/durum  : {k['sayfa_tipi']} · {k['durum']} · index={k['index']} · ürün: {k.get('urun_sayisi')}")
    print(f"Canonical  : {k['canonical'] or '(kendisi)'}" + ("" if k["canonical_kendisi"] else "   <-- BAŞKA SAYFAYA İŞARET EDİYOR"))
    print(f"H1         : {k['h1']}\nTitle      : {k['title']}  | html: {k['html_title']}\nDescription: {k['description']}")
    print("Breadcrumb : " + " > ".join(b for b, _ in k.get("breadcrumb", [])))
    print(f"İçerik     : {i['kelime']} kelime · {len(i['basliklar'])} başlık ({', '.join(sorted({t for t, _ in i['basliklar']})) or '-'})"
          f" · {len(i['linkler'])} link · liste {i['liste']} · tablo {i['tablo']} · soru başlık {i['soru_baslik']} · SSS {'var' if i['sss'] else 'yok'}")
    for t, b in i["basliklar"]:
        print(f"   {t}: {b}")
    for a_, u in i["linkler"]:
        print(f"   link: {a_} -> {u}")
    print(f"Fiyat filtresi: {'var' if k.get('fiyat_filtresi') else 'yok'} · seçenek filtreleri: {', '.join(k.get('secenek_filtreleri') or []) or '-'}"
          f" · sıralama: {', '.join(x for x in (k.get('siralama') or []) if x) or '-'}")
    for x in k.get("gam") or []:
        print(f"Gam · {x['ad']}: {x.get('urun')} ürün · " + " | ".join((x.get('ornek') or [])[:4]))
    print("Alt kategoriler: " + ", ".join(ad for ad, _ in k.get("alt_kategoriler", [])))
    print("Markalar (ilk 25): " + ", ".join(ad for ad, _ in k.get("markalar", [])[:25]) + f"  (toplam {len(k.get('markalar', []))})")
    for ad, deger in (k.get("filtreler") or {}).items():
        print(f"Filtre · {ad}: " + ", ".join(deger[:18]))
    if k.get("link_bulutu"):
        print("Link bulutu: " + ", ".join(t for t, _ in k["link_bulutu"][:30]))


if __name__ == "__main__":
    main()
