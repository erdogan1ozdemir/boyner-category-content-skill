#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kelime sahipliği (cannibalization) tablosu: araştırmadaki her kelime hangi Boyner sayfasına ait?

Boyner'de 34 binin üzerinde listeleme sayfası var ve bir kelimeye çoğu zaman birden fazla sayfa aday.
İçerik yazılmadan önce her kelime dört kovadan birine düşer:

  HEDEF        Bu sayfanın kelimesi. Title, H1, giriş ve H2'lerde işlenir.
  BAŞKA SAYFA  Kelimenin Boyner'de kendi sayfası var (alt kategori, marka+kategori, renk araması...).
               Bu içerikte hedeflenmez: başlığa çıkmaz, SSS sorusu olmaz. Geçerse bir kez ve o sayfaya
               link veren anchor olarak geçer.
  SERBEST      Hedefin kapsamında, kendi sayfası olmayan uzun kuyruk. H2/H3, madde ya da SSS ile bu
               sayfada karşılanır; trafik kazancı buradan gelir.
  KAPSAM DIŞI  Boyner'de satılmayan marka ya da perakendeci kelimesi (zara, lcw...), başka cinsiyet. Yazılmaz.

Sahip belirleme sırası: (1) Boyner'in o kelimede Google'da sıralanan sayfası (arastirma.py haritası),
(2) envanterde kök kümesi kelimeyle birebir eşleşen sayfa. Aynı ada sahip birden çok kategori kimliği
varsa (Boyner'de sık) --teyit canlı kayıttan ürün sayısı en yüksek ve canonical'ı kendisi olanı seçer.

Kullanım:
    python3 sahiplik.py --arastirma /tmp/kadin-mont.json --url https://www.boyner.com.tr/kadin-mont-x-g3731-c23896554 \
        --kayit /tmp/kayit.json [--teyit] [--min-hacim 50] [--cikti /tmp/kadin-mont-sahiplik.json]
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import kumeler, url_coz, duz, CINSIYET
import envanter

# Boyner'de satılmayan perakendeci ve özel markalar: kelime bunlardan birini taşıyorsa ve envanterde
# o marka sayfası yoksa kapsam dışıdır. Liste envanterle çapraz kontrol edilir, tek başına karar vermez.
RAKIP = ["zara", "lcw", "lc waikiki", "waikiki", "koton", "mango", "h&m", "hm", "bershka", "stradivarius",
         "pull and bear", "pull bear", "massimo dutti", "trendyol", "trendyolmilla", "milla", "hepsiburada",
         "decathlon", "flo", "morhipo", "n11", "amazon", "ipekyol", "oxxo", "addax", "modanisa", "sefamerve",
         "bim", "a101", "migros", "tchibo", "lufian", "loft", "collezione", "kigili", "damat", "altinyildiz",
         "vakko", "beymen", "network", "sarar", "hatemoglu", "superstep", "sportive", "intersport", "korayspor"]


MARKA_EK = frozenset({"the", "jeans", "jean", "assn", "by", "of", "club", "sport", "kids", "home"})


def siniflandir(kw, hedef, sayfalar, harita, marka_kumeleri, cins_kok, markali, canli):
    k = kumeler(kw["kelime"])
    hk = hedef["kume"]
    if not k:
        return None
    h_url = harita.get(kw["kelime"])
    sahipler = [s for s in envanter.sahip(kw["kelime"], sayfalar)]
    if k in canli and k != hk:
        # sayfanın kendi filtresinde listelenen alt kategori ya da marka kırılımı: en güvenilir sahip.
        # Sitemap eski kategori kimliklerini de taşır; canlı kayıttaki adres doğru kimliktir.
        return {"kelime": kw["kelime"], "hacim": kw.get("hacim"), "kova": "BAŞKA SAYFA", "sahip": canli[k],
                "not": "canlı kayıt: sayfanın kendi alt kırılımı", "adaylar": []}
    if not sahipler and k != hk:
        # marka sayfaları slug'da fazladan bir kelime taşıyabilir ("the north face" / "north face")
        sahipler = envanter.sirala([s for s in markali if k < s["kume"] and len(s["kume"] - k) == 1
                                    and (s["kume"] - k) <= MARKA_EK])
    # aynı ada sahip birden çok kategori kimliği varsa hedefin kategori ailesindeki aday öne alınır
    sahipler.sort(key=lambda s: 0 if s["c"] == hedef["c"] else 1)
    s_url = [s["url"] for s in sahipler]
    hedef_aile = lambda u: bool(u) and (url_coz(u) or {}).get("c") == hedef["c"] and not (url_coz(u) or {}).get("b") \
        and (url_coz(u) or {}).get("g") in (hedef["g"], None) and not (url_coz(u) or {}).get("q")
    baska_cins = (k & cins_kok) - hk
    if k == hk or (h_url and h_url["url"].split("?")[0] == hedef["url"] and not sahipler):
        kova, sahip, not_ = "HEDEF", hedef["url"], ("sıralanıyor: %s." % h_url["sira"] if h_url else "")
        if k != hk:
            kova, not_ = "SERBEST", f"Boyner'de bu sayfa sıralanıyor ({h_url['sira']}.), kendi sayfası yok"
    elif hedef["url"] in s_url:
        kova, sahip, not_ = "HEDEF", hedef["url"], ""
    elif baska_cins and not (hk & cins_kok and hk & cins_kok <= k and len(k & cins_kok) == len(hk & cins_kok)):
        kova, sahip, not_ = "KAPSAM DIŞI", (s_url or [h_url and h_url["url"]])[0], "başka cinsiyet"
    elif sahipler:
        kova, sahip = "BAŞKA SAYFA", s_url[0]
        not_ = f"{len(s_url)} aday sayfa" if len(s_url) > 1 else sahipler[0]["tip"]
        if h_url and h_url["sira"] and h_url["sira"] <= 20 and "-p-" not in h_url["url"] and h_url["url"] != hedef["url"]:
            sahip, not_ = h_url["url"], f"Google'da bu sayfa sıralanıyor ({h_url['sira']}.)"
    elif h_url and not hedef_aile(h_url["url"]) and h_url["sira"] and h_url["sira"] <= 20 and "-p-" not in h_url["url"]:
        kova, sahip, not_ = "BAŞKA SAYFA", h_url["url"], f"Google'da bu sayfa sıralanıyor ({h_url['sira']}.)"
    else:
        ek = duz(kw["kelime"])
        rakip = next((r for r in RAKIP if f" {r} " in f" {ek} "), None)
        if rakip and kumeler(rakip) not in marka_kumeleri:
            kova, sahip, not_ = "KAPSAM DIŞI", None, f"Boyner'de satılmayan marka/perakendeci: {rakip}"
        elif hk <= k or (hk - cins_kok) <= k:
            kova, sahip, not_ = "SERBEST", None, ("soru" if kw.get("soru") else "uzun kuyruk")
            if h_url:
                not_ += f" · Boyner {h_url['sira']}. sırada: {h_url['url'].replace('https://www.boyner.com.tr', '')}"
        else:
            kova, sahip, not_ = "KAPSAM DIŞI", None, "hedefin ürün çekirdeğini taşımıyor"
    return {"kelime": kw["kelime"], "hacim": kw.get("hacim"), "kova": kova, "sahip": sahip, "not": not_,
            "adaylar": s_url[:8] if len(s_url) > 1 else []}


def teyit_et(satirlar, hedef_c):
    """Çok adaylı sahiplerde canlı kaydı okuyup ürün sayısı en yüksek, canonical'ı kendisi olan sayfayı seçer."""
    import kategori, time
    onbellek = {}
    for s in satirlar:
        if s["kova"] != "BAŞKA SAYFA" or not s["adaylar"]:
            continue
        en_iyi, en_cok = None, -1
        for u in s["adaylar"][:6]:
            if "search?q=" in u:
                continue
            if u not in onbellek:
                k = kategori.oku(u); time.sleep(0.6)
                # H1'i kelimeyle örtüşmeyen sayfa (ör. "Mont & Şişme Mont") aynı ada sahip görünse de sahip değildir
                uyum = kumeler(k.get("h1") or "") <= kumeler(s["kelime"]) | kumeler(k.get("cinsiyet") or "")
                onbellek[u] = ((k.get("urun_sayisi") or 0) if uyum else 0, k.get("canonical_kendisi"), k.get("durum"))
            n, kendi, durum = onbellek[u]
            puan = n + (10 ** 6 if (url_coz(u) or {}).get("c") == hedef_c else 0)   # hedefin kategori ailesi önde
            if durum == 200 and kendi and n > 0 and puan > en_cok:
                en_iyi, en_cok = u, puan
        if en_iyi:
            s["sahip"] = en_iyi
            s["not"] = f"teyitli: {onbellek[en_iyi][0]} ürün · {len(s['adaylar'])} aday arasından"
    return satirlar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arastirma", required=True)
    ap.add_argument("--url", required=True, help="hedef sayfa")
    ap.add_argument("--min-hacim", type=int, default=50)
    ap.add_argument("--kayit", help="kategori.py --cikti dosyası; sayfanın canlı alt kategori ve marka kırılımları "
                                    "sahip olarak öncelik alır (önerilir)")
    ap.add_argument("--teyit", action="store_true", help="çok adaylı sahipleri canlı kayıttan teyit et (yavaş)")
    ap.add_argument("--cikti")
    a = ap.parse_args()

    d = json.load(open(a.arastirma, encoding="utf-8"))
    sayfalar = envanter.yukle()
    hedef = url_coz(a.url)
    if not hedef:
        sys.exit("Hedef URL çözülemedi")
    hedef["kume"] = kumeler(hedef["slug"])
    harita = {}
    for x in (d.get("boyner_haritasi") or {}).get("liste") or []:
        harita.setdefault(x["kelime"], {"url": x["url"].split("?srsltid")[0], "sira": x["sira"]})
    marka_kumeleri = {s["kume"] for s in sayfalar if s["tip"] == "marka"}
    markali = [s for s in sayfalar if s["b"] and s["c"]]
    cins_kok = frozenset(k for g in CINSIYET.values() for k in kumeler(g)) | kumeler("bebek çocuk kız")

    canli = {}
    if a.kayit:
        kayit = json.load(open(a.kayit, encoding="utf-8"))
        cins = kumeler(kayit.get("cinsiyet") or "")
        for ad, u in (kayit.get("alt_kategoriler") or []) + (kayit.get("markalar") or []):
            p = url_coz(u)
            if p and not p["q"]:
                canli.setdefault(kumeler(p["slug"]), p["url"])
    kelimeler = [k for k in d["kelimeler"]["liste"] if (k.get("hacim") or 0) >= a.min_hacim]
    gorulen, satirlar = set(), []
    for kw in kelimeler:
        k = kumeler(kw["kelime"])
        if k in gorulen:          # "kadın mont" / "mont kadın" / "kadın mont modelleri" aynı niyet: en hacimlisi kalır
            continue
        gorulen.add(k)
        r = siniflandir(kw, hedef, sayfalar, harita, marka_kumeleri, cins_kok, markali, canli)
        if r:
            satirlar.append(r)
    if a.teyit:
        satirlar = teyit_et(satirlar, hedef["c"])

    for kova in ("HEDEF", "SERBEST", "BAŞKA SAYFA", "KAPSAM DIŞI"):
        grup = [s for s in satirlar if s["kova"] == kova]
        print(f"\n== {kova} ({len(grup)}) ==")
        for s in grup[:45]:
            sahip = (s["sahip"] or "").replace("https://www.boyner.com.tr", "")
            print(f"  {s['hacim'] or 0:>6}  {s['kelime']:<38} {sahip[:70]:<70} {s['not']}")
        if len(grup) > 45:
            print(f"  ... +{len(grup) - 45} kelime (tam liste JSON çıktısında)")
    # aynı kelimede iki Boyner sayfası sıralanıyorsa site düzeyinde çakışma vardır; içerikle çözülmez, bildirilir
    if a.cikti:
        json.dump({"hedef": hedef["url"], "satirlar": satirlar}, open(a.cikti, "w"), ensure_ascii=False, indent=2)
        print(f"\nyazıldı: {a.cikti}")


if __name__ == "__main__":
    main()
