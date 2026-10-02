#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""boyner.com.tr listeleme sayfası envanteri: altı sitemap'ten kurulur, önbelleğe alınır, sorgulanır.

Neden var: Boyner'de aynı ürün ailesi için kategori, cinsiyet+kategori, marka, marka+cinsiyet,
marka+cinsiyet+kategori ve filtre (renk, materyal...) sayfaları ayrı ayrı yayında. İçerik yazarken
her kelimenin "sahibi" olan sayfayı bilmek gerekir; yoksa iki sayfa aynı kelimeye oynar. Bu betik
hem cannibalization kontrolünün hem de iç link seçiminin veri kaynağıdır.

Kullanım:
    python3 envanter.py yenile                       # sitemap'leri indir, envanteri kur (7 günde bir yeter)
    python3 envanter.py ozet                         # tip bazında sayfa sayıları
    python3 envanter.py ara "kadın mont"             # kelimeyi taşıyan sayfalar, tipe göre
    python3 envanter.py sahip "kadın şişme mont"     # kelimenin sahibi olan sayfa(lar)
    python3 envanter.py iliskili URL                 # üst, alt, kardeş, cinsiyet, marka ve filtre sayfaları
"""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import getir, onbellek, url_coz, kumeler, duz, CINSIYET

KOK = "https://sitemap.boyner.com.tr/bynsitemap/"
SITEMAPLER = ["category.xml", "gender_category.xml", "brand.xml", "brand_gender.xml",
              "brand_gender_category.xml", "custom_sitemap.xml"]
DOSYA = onbellek("envanter.json")
# Sahiplik sırası: aynı kelimeye iki sayfa uyuyorsa üstteki tip sahibidir.
TIP_SIRA = ["cinsiyet_kategori", "kategori", "marka_cinsiyet_kategori", "marka_kategori", "marka_cinsiyet",
            "marka", "arama", "cinsiyet_kategori_filtre", "kategori_filtre", "marka_cinsiyet_kategori_filtre",
            "marka_filtre", "marka_cinsiyet_filtre"]


def loclar(xml):
    return [u.replace("&amp;", "&").strip() for u in re.findall(r"<loc>(.*?)</loc>", xml)]


def yenile():
    kayit, gorulen = [], set()
    for sm in SITEMAPLER:
        urller = loclar(getir(KOK + sm))
        alt = [u for u in urller if u.endswith(".xml")]
        for a in alt:                                   # sitemap index ise alt dosyalar
            urller += loclar(getir(a)); time.sleep(1)
        n = 0
        for u in urller:
            if u.endswith(".xml") or u in gorulen:
                continue
            p = url_coz(u)
            if not p:
                continue
            gorulen.add(u)
            p["kaynak"] = sm[:-4]
            p["kume"] = sorted(kumeler(p["slug"] + " " + filtre_metni(p["q"])))
            kayit.append(p); n += 1
        print(f"{sm}: {n} sayfa", flush=True)
        time.sleep(1)
    json.dump({"tarih": time.strftime("%Y-%m-%d"), "sayfalar": kayit}, open(DOSYA, "w"), ensure_ascii=False)
    print(f"toplam {len(kayit)} sayfa -> {DOSYA}")


def filtre_metni(q):
    """?renk=nude&materyal=deri -> 'nude deri' (filtre değeri kelimenin parçasıdır: nude ruj)."""
    return " ".join(v.replace("-", " ").replace(",", " ") for kv in q.split("&") if "=" in kv
                    for v in [kv.split("=", 1)[1]])


def yukle():
    if not os.path.exists(DOSYA):
        sys.exit("Envanter yok. Önce: python3 envanter.py yenile")
    d = json.load(open(DOSYA))
    yas = (time.time() - os.path.getmtime(DOSYA)) / 86400
    if yas > 7:
        print(f"UYARI: envanter {yas:.0f} günlük; 'envanter.py yenile' ile güncellenmeli.", file=sys.stderr)
    for s in d["sayfalar"]:
        s["kume"] = frozenset(s["kume"])
    return d["sayfalar"]


def sirala(sayfalar):
    return sorted(sayfalar, key=lambda s: (TIP_SIRA.index(s["tip"]) if s["tip"] in TIP_SIRA else 99, len(s["url"])))


def sahip(kelime, sayfalar):
    """Kelimenin kök kümesiyle birebir eşleşen sayfalar; sahiplik sırasına göre."""
    k = kumeler(kelime)
    return sirala([s for s in sayfalar if s["kume"] == k]) if k else []


def ara(kelime, sayfalar):
    k = kumeler(kelime)
    return sirala([s for s in sayfalar if k and k <= s["kume"]])


def iliskili(url, sayfalar):
    p = url_coz(url)
    if not p:
        sys.exit("URL çözülemedi: " + url)
    ben = next((s for s in sayfalar if s["url"] == p["url"]), None)
    kume = ben["kume"] if ben else kumeler(p["slug"])
    cins = {kok for g in CINSIYET.values() for kok in kumeler(g)}
    cekirdek = frozenset(kume - cins) or kume                 # cinsiyet kelimesi atılmış ürün çekirdeği
    out = {"hedef": p["url"], "envanterde": bool(ben), "cekirdek": sorted(cekirdek)}
    diger = [s for s in sayfalar if s["url"] != p["url"]]
    ayni_c = [s for s in diger if p["c"] and s["c"] == p["c"]]
    out["ayni_kategori_cinsiyetler"] = [s["url"] for s in ayni_c if not s["b"] and not s["q"]]
    out["ayni_kategori_filtreler"] = [s["url"] for s in ayni_c if s["q"] and not s["b"]
                                      and (s["g"] == p["g"] or not s["g"] or not p["g"])][:60]
    out["ayni_kategori_markalar"] = [s["url"] for s in ayni_c if s["b"] and not s["q"]
                                     and (s["g"] == p["g"] or not p["g"])][:60]
    kat = [s for s in diger if not s["b"] and not s["q"] and s["c"] != p["c"]]
    # alt: hedefin kümesini kapsayan daha dar sayfalar (kadın mont -> kadın şişme mont)
    out["alt_sayfalar"] = [s["url"] for s in sirala([s for s in kat if kume < s["kume"]])][:80]
    # üst: hedefin kümesinin alt kümesi olan daha geniş sayfalar (kadın şişme mont -> kadın mont, mont)
    out["ust_sayfalar"] = [s["url"] for s in sirala([s for s in kat if s["kume"] and s["kume"] < kume])][:20]
    # akraba: aynı ürün çekirdeğini başka cinsiyetle taşıyanlar (erkek mont, kız çocuk mont)
    out["akraba_sayfalar"] = [s["url"] for s in sirala([s for s in kat if cekirdek <= s["kume"]
                              and not kume <= s["kume"]])][:40]
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    komut = sys.argv[1]
    if komut == "yenile":
        return yenile()
    sayfalar = yukle()
    if komut == "ozet":
        from collections import Counter
        for t, n in Counter(s["tip"] for s in sayfalar).most_common():
            print(f"{n:6d}  {t}")
    elif komut in ("ara", "sahip"):
        kelime = " ".join(sys.argv[2:])
        liste = (sahip if komut == "sahip" else ara)(kelime, sayfalar)
        print(f"'{kelime}' -> kök kümesi {sorted(kumeler(kelime))} · {len(liste)} sayfa")
        for s in liste[:80]:
            print(f"  {s['tip']:32s} {s['url']}")
    elif komut == "iliskili":
        print(json.dumps(iliskili(sys.argv[2], sayfalar), ensure_ascii=False, indent=2))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
