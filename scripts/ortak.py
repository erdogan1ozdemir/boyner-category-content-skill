#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Betiklerin ortak yardımcıları: curl ile istek, önbellek dizini, Türkçe normalizasyon, URL çözümleme.

İstekler curl ile atılır: bu makinede Python'un urllib'i kurumsal sertifika zinciri yüzünden SSL
hatası veriyor; curl çalışıyor. boyner.com.tr Cloudflare arkasında; art arda hızlı istekte "Just a
moment..." sayfası dönebiliyor, bu yüzden getir() kısa bekleme ve yeniden deneme yapar.
"""
import os, re, subprocess, time, unicodedata

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")
ONBELLEK = os.path.expanduser("~/.cache/boyner-kategori-brief")
SITE = "https://www.boyner.com.tr/"

CINSIYET = {"3731": "Kadın", "3730": "Erkek", "3733": "Kız Çocuk", "3734": "Erkek Çocuk",
            "214747": "Kız Bebek", "214763": "Erkek Bebek", "25462663": "Kadın"}   # 25462663: ikinci "kadın" kimliği

# Kelimenin niyetini değiştirmeyen ekler: "kadın mont modelleri" ile "kadın mont" aynı sayfanın kelimesidir.
DOLGU = {"model", "modelleri", "modeli", "modeller", "cesitleri", "cesit", "cesidi", "fiyatlari", "fiyat",
         "fiyati", "urunleri", "urun", "urunler", "ve", "ile", "icin", "x", "boyner", "online", "satin", "al"}
# Sahiplik dışı bırakılacak kalıplar: kampanya, gezinme ve konu dışı sorgular
KAPSAM_DISI_KALIP = (r"\b(1 alana|2 al|bedava|defolu|toptan|indirim|outlet|kampanya|ikinci el|2 el|sahibinden|"
                     r"ruyada|eksi|kadinlar kulubu|sikayet|guvenilir mi|com tr|nerede satilir|magazalari?)\b")
RENKLER = {"siyah", "beyaz", "kirmiz", "mavi", "lacivert", "yesil", "sar", "pembe", "mor", "gri", "bej", "kahvereng",
           "bordo", "turuncu", "haki", "ekru", "krem", "fume", "antrasit", "vizon", "lila", "gumus", "altin"}


def onbellek(*parca):
    yol = os.path.join(ONBELLEK, *parca)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    return yol


def getir(url, saniye=40, deneme=3, bekle=4):
    """URL'yi curl ile indirir. Cloudflare doğrulama sayfası gelirse bekleyip yeniden dener."""
    govde = ""
    for i in range(deneme):
        r = subprocess.run(["curl", "-sSL", "--compressed", "-m", str(saniye), "-A", UA,
                            "-H", "Accept-Language: tr-TR,tr;q=0.9", url], capture_output=True, text=True)
        govde = r.stdout or ""
        if govde and "Just a moment..." not in govde[:600]:
            return govde
        time.sleep(bekle * (i + 1))
    return govde


def durum_kodu(url, saniye=25):
    r = subprocess.run(["curl", "-sSL", "-o", "/dev/null", "-m", str(saniye), "-A", UA,
                        "-w", "%{http_code}", url], capture_output=True, text=True)
    return r.stdout.strip()


def duz(s):
    """Türkçe harfleri ASCII'ye katlar, küçültür; slug ile kelimeyi aynı zemine indirir."""
    s = (s or "").replace("İ", "i").replace("I", "i").lower()
    s = s.translate(str.maketrans("çğıöşüâîû", "cgiosuaiu"))
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def kok(w):
    """Çok hafif gövdeleme: çoğul ve iyelik eklerini atar, ünsüz yumuşamasını geri alır
    (montlar, montu, montlari -> mont · ayakkabisi, ayakkabi -> ayakkab · kulakligi -> kulaklik)."""
    for ek in ("lari", "leri", "lar", "ler"):
        if w.endswith(ek) and len(w) - len(ek) >= 3:
            w = w[:-len(ek)]
            break
    if len(w) >= 6 and w[-2:] in ("si", "su") and w[-3] in "aeiou":
        w = w[:-2]                                   # ayakkabi-si, corab-i gibi 3. tekil iyelik
    if len(w) >= 6 and w[-2:] in ("gi", "gu"):
        return w[:-2] + "k"                          # kulaklig-i -> kulaklik, gozlug-u -> gozluk
    if len(w) >= 5 and w[-2:] in ("bi", "bu"):
        return w[:-2] + "p"                          # corab-i -> corap; ayakkabi -> ayakkap (tutarlı kalır)
    if len(w) >= 5 and w[-1] == "b":
        return w[:-1] + "p"
    if len(w) >= 5 and w[-1] in "iu" and w[-2] not in "aeiou":
        w = w[:-1]
    return w


ES_ANLAM = {"bayan": "kadin", "bay": "erkek", "kiz": "kiz", "tisort": "t shirt", "tshirt": "t shirt",
            "sneakers": "sneaker", "jean": "jean", "kot": "jean"}


def kumeler(metin):
    """Kelime ya da slug -> niyet taşıyan kök kümesi (dolgu ekleri atılmış, eş anlamlılar birleştirilmiş)."""
    out = set()
    for t in duz(metin).split():
        if t in DOLGU or kok(t) in DOLGU:
            continue
        k = kok(t)
        out.update(ES_ANLAM.get(k, ES_ANLAM.get(t, k)).split())
    return frozenset(out)


URL_DESEN = re.compile(r"^(?:https?://www\.boyner\.com\.tr)?/?(?P<slug>[^?#]*?)-x-(?P<ids>[bgc0-9-]+)(?:\?(?P<q>[^#]*))?$")


ARAMA_DESEN = re.compile(r"^(?:https?://www\.boyner\.com\.tr)?/?search\?q=(?P<q>[^&#]+)$")


def url_coz(url):
    """boyner.com.tr listeleme URL'sini parçalar: slug, marka/cinsiyet/kategori kimlikleri, filtre, tip."""
    url = url.strip()
    a = ARAMA_DESEN.match(url)
    if a:   # custom_sitemap'teki indekslenebilir arama sayfaları: /search?q=beyaz+çanta
        from urllib.parse import unquote_plus
        q = unquote_plus(a["q"]).strip()
        return {"url": SITE + "search?q=" + a["q"], "slug": q, "b": None, "g": None, "c": None,
                "q": "", "tip": "arama"}
    m = URL_DESEN.match(url)
    if not m:
        return None
    b = re.search(r"(?:^|-)b(\d+)", m["ids"]); g = re.search(r"(?:^|-)g(\d+)", m["ids"])
    c = re.search(r"(?:^|-)c(\d+)", m["ids"])
    q = m["q"] or ""
    parca = [x for x, v in (("marka", b), ("cinsiyet", g), ("kategori", c)) if v]
    tip = "_".join(parca) + ("_filtre" if q else "")
    return {"url": SITE + m["slug"] + "-x-" + m["ids"] + ("?" + q if q else ""),
            "slug": m["slug"], "b": b and b.group(1), "g": g and g.group(1), "c": c and c.group(1),
            "q": q, "tip": tip}
