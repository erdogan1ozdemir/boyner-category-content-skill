#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İçerik JSON'unu teslimden önce denetler: yapı, link, kelime sahipliği, biçim, hitap ve SSS.

Neden betik: çok kategorili bir sitede en pahalı hata içeriğin başka bir sayfanın kelimesine oynamasıdır
ve bu, okuyarak en zor yakalanan hatadır. Betik başlıkları, anchor'ları ve SSS sorularını sahiplik
tablosuyla (sahiplik.py çıktısı) ve envanterle karşılaştırır; biçim ve hitap hatalarını da aynı turda toplar.

Kullanım:
    python3 icerik_denetim.py --json icerik.json
    python3 icerik_denetim.py --json icerik.json --sahiplik sahiplik.json --arastirma arastirma.json --canli

    --sahiplik    başlık / SSS / anchor'ları BAŞKA SAYFA kelimeleriyle karşılaştırır
    --arastirma   gövde uzunluğunu ilk 5 rakibin medyanıyla karşılaştırır
    --canli       her link hedefini canlı okur: 200, canonical kendisi, ürün sayısı > 0

Bulgu varsa çıkış kodu 1 olur; çıktı dosyaları üretilmeden önce çalıştırılır. "NOT:" satırları hata
değil, okuyarak karar verilecek adaylardır.
"""
import argparse, json, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortak import kumeler, url_coz, duz as duzle

BICIM = [("—", "uzun tire"), ("–", "en tire"), (r"(?<=\S)  +(?=\S)", "çift boşluk"), ("®|™", "marka sembolü"),
         (r"[\U0001F300-\U0001FAFF☀-➿]", "emoji"), (r"\.\.(?!\.)", "çift nokta"), (r" ,| \.(?!\w)", "boşluk-noktalama"),
         (r"(?i)\b\d[\d.,]*\s*(TL|lira)\b|₺", "fiyat"), (r"(?i)%\s?\d+\s*(?:'?[ea]? varan )?indirim|\d+\s?%\s*indirim", "indirim oranı"),
         (r"\b20[2-3]\d\b", "yıl (zamana bağlı ifade)"),
         (r"(?i)\bkategori(?:de|sinde|deki|sindeki|nin|si)\b|\bbu kategori", "'kategori' kelimesi (ürün grubu / Boyner ... modelleri arasında)"), 
         (r"(?i)\b\w+(?:abilirsin|ebilirsin|malısın|melisin)\b|\bsenin\b|\bsana\b", "'sen' hitabı (Boyner dili 'siz')"),
         (r"(?i)\btrendyol|hepsiburada|\bn11\b|amazon|morhipo|\bzara\b|\blcw\b|lc waikiki|\bkoton\b|\bbeymen\b|\bflo\b(?! [a-z])",
          "rakip perakendeci adı")]
UYARI_DESEN = [
    (r"(?i)\bbu sezon\b|\bbu yıl\b|\bgeçtiğimiz\b|\bson yıllarda\b|\byakında\b|\bşu sıralar\b", "zamana bağlı ifade"),
    (r"(?i)vazgeçilmez|olmazsa olmaz|\badeta\b|göz kamaştır|büyüleyici|eşsiz|kusursuz|benzersiz|mükemmel|harika|"
     r"yolculuğa|kapılarını aral|bir tık öte|sizi bekliyor", "kalıp pazarlama ifadesi (somut bilgiyle değiştirilebilir mi?)"),
    (r"(?i)sadece [^.]{3,60} değil,? aynı zamanda|hem de öyle|tabii ki|elbette ki|unutmayın ki|şüphesiz", "yapay geçiş kalıbı"),
    (r"(?i)tedavi ed|iyileştir|kesin çözüm|garanti(?! süre)|yüzde yüz|%\s?100 (?:etkili|sonuç)", "sağlık / kesinlik iddiası"),
    (r"(?i)\b\w+(?:ıyoruz|iyoruz|uyoruz|üyoruz|acağız|eceğiz)\b|\btavsiye ederiz\b", "birinci çoğul (yalnız liste girişlerinde 'sizin için grupladık' gibi kalıplarda serbest)"),
    (r"[^.!?]{140,};", "noktalı virgülle uzatılmış uzun cümle (iki cümleye bölünebilir)"),
    (r"(?i)tıklayın|buraya tıkla|göz atabilirsiniz|inceleyebilirsiniz", "link taşımak için kurulmuş cümle olabilir"),
]
JENERIK_ANCHOR = {"buraya", "tiklayin", "burada", "bu sayfa", "link", "sayfa", "detaylar", "incele", "urunler", "tumu"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--sahiplik")
    ap.add_argument("--arastirma")
    ap.add_argument("--canli", action="store_true")
    ap.add_argument("--kayit", help="kategori.py çıktısı; sayfada satılan markalar rakip adı taramasından muaf tutulur")
    a = ap.parse_args()

    d = json.load(open(a.json, encoding="utf-8"))
    g, linkler = d["govde"], d.get("linkler") or {}
    hedef = url_coz(d["url"]) or {}
    hk = kumeler(d["main_kw"])
    duz = lambda i: re.sub(r"\*\*", "", re.sub(r"\[LINK(\d+)\]", lambda m: linkler.get("LINK" + m.group(1), ["?"])[0], i))
    govde_metin = " ".join(duz(i) for t, i in g if t in ("p", "li", "mad"))
    sss = d.get("sss") or []
    tum = govde_metin + " " + " ".join(q + " " + duz(c) for q, c in sss) + " " + " ".join(v for t, v in g if t in ("H2", "H3"))
    sorun, uyari = [], []

    # --- yapı
    tablo_metin = " ".join(str(h) for t, i in g if t == "tablo" for s_ in i for h in s_)
    kelime = len(govde_metin.split())           # tablolar hariç; icerik_docx.py ile aynı sayım
    h2 = [v for t, v in g if t == "H2"]; h3 = [v for t, v in g if t == "H3"]
    if not g or g[0][0] != "p":
        sorun.append("gövde başlıksız girişle açılmıyor (sayfada H1 var; ilk öğe paragraf olmalı)")
    if any(t == "H1" for t, _ in g):
        sorun.append("gövdede H1 var; sayfanın H1'i kategori adıdır")
    if kelime < 1500:
        uyari.append(f"gövde {kelime} kelime; hedef 1.500-2.500 (gam darsa gerekçesiyle kısa kalabilir, tekrarla uzatılmaz)")
    if len(h2) < 4:
        uyari.append(f"{len(h2)} H2 var; konu kapsamı için genellikle en az 4-5 bölüm gerekir")
    ilk_h = next((t for t, _ in g if t in ("H2", "H3")), None)
    if ilk_h == "H3":
        sorun.append("ilk başlık H3; H3 yalnız bir H2'nin altında açılır")
    for b in h2 + h3:
        if b.count(",") >= 2:
            uyari.append(f"başlık üç konuyu virgülle diziyor: {b}")
        if len(b) > 70:
            uyari.append(f"başlık {len(b)} karakter: {b}")
    for b in {b for b in h2 + h3 if (h2 + h3).count(b) > 1}:
        sorun.append(f"aynı başlık iki kez: {b}")
    giris = " ".join(duz(i) for t, i in g[:next((k for k, (t, _) in enumerate(g) if t in ("H2", "H3")), len(g))])
    if hk and not hk <= kumeler(giris):
        sorun.append(f"ana kelime ('{d['main_kw']}') başlıksız girişte geçmiyor")
    if any(t == "tablo" for t, _ in g):
        sorun.append("içerikte tablo var; içerik alanına tablo eklenemiyor, bilgi '•' satırlarına çevrilir")
    if not any(t in ("mad", "li") for t, _ in g):
        uyari.append("gövdede '•' satırı ya da numaralı adım yok; taranabilirlik ve AI alıntılanabilirliği için beklenir")
    for t, i in g:
        if t in ("p", "mad", "li") and re.match(r"\s*(?:[•\-*]|\d+[.)])\s", i):
            sorun.append(f"madde imi ya da numara metne elle yazılmış (betik ekler): {i[:50]}")
    for t, i in g:
        if t == "p" and len(duz(i).split()) > 110:
            uyari.append(f"paragraf {len(duz(i).split())} kelime (bölünebilir): {duz(i)[:70]}…")
    # H2'den sonraki ilk cümle doğrudan yanıt olmalı; çok uzun ilk cümle çoğu zaman girizgâhtır
    for k, (t, v) in enumerate(g[:-1]):
        if t == "H2" and g[k + 1][0] == "p":
            ilk = re.split(r"(?<=[.!?])\s+", duz(g[k + 1][1]))[0]
            if len(ilk.split()) > 32:
                uyari.append(f"'{v}' bölümünün ilk cümlesi {len(ilk.split())} kelime; ilk cümle başlığı kısa ve doğrudan yanıtlar")
        if t == "H2" and g[k + 1][0] in ("H2",):
            sorun.append(f"'{v}' başlığının altı boş")

    # --- ana kelime yoğunluğu
    ana = duzle(d["main_kw"])
    # yoğunluk madde etiketleri ve anchor'lar dışında sayılır (etiketler kural gereği ana kelimeyi taşır)
    ciplak = " ".join(re.sub(r"\*\*", "", re.sub(r"\[LINK\d+\]", " ", re.sub(r"^\*\*[^*]+\*\*", " ", i)))
                      for t, i in g if t in ("p", "li", "mad"))
    gecis = len(re.findall(r"\b" + re.escape(ana) + r"\w*", duzle(ciplak)))
    yogunluk = gecis * len(ana.split()) / max(1, kelime) * 100
    if yogunluk > (4 if (hedef.get("b") or len(d["main_kw"].split()) == 1) else 3):
        uyari.append(f"ana kelime {gecis} kez geçiyor (%{yogunluk:.1f}); eş anlamlı ve ürün adlarıyla çeşitlendirilebilir")
    if gecis < 3:
        uyari.append(f"ana kelime gövdede {gecis} kez geçiyor")

    # --- linkler
    kull = re.findall(r"\[(LINK\d+)\]", " ".join(str(i) for t, i in g if t != "tablo") + " " +
                      " ".join(str(h) for t, i in g if t == "tablo" for s in i for h in s) + " " + " ".join(c for _, c in sss))
    for k in linkler:
        n = kull.count(k)
        if n != 1:
            sorun.append(f"{k} {n} kez kullanılmış (her link bir kez)")
    for k in set(kull):
        if k not in linkler:
            sorun.append(f"[{k}] tanımsız")
    n = len(linkler)
    if n < 4 or n > 10:
        sorun.append(f"{n} iç link var; hedef 5-8")
    elif not 5 <= n <= 8:
        uyari.append(f"{n} iç link var; hedef 5-8")
    hedefler, cids = {}, {}
    try:
        import envanter
        sayfalar = {s["url"]: s for s in envanter.yukle()}
    except SystemExit:
        sayfalar = None
        uyari.append("envanter yok; link hedefleri envanterle karşılaştırılmadı")
    for k, (anchor, url) in linkler.items():
        p = url_coz(url)
        if "boyner.com.tr" not in url:
            sorun.append(f"{k}: site dışı link ({url})"); continue
        if not p:
            uyari.append(f"{k}: listeleme sayfası değil ya da URL çözülemedi ({url})"); continue
        if p["url"].split("?")[0] == (hedef.get("url") or "").split("?")[0]:
            sorun.append(f"{k}: sayfa kendine link veriyor")
        if p["url"] in hedefler:
            sorun.append(f"{k} ve {hedefler[p['url']]} aynı sayfaya gidiyor")
        hedefler[p["url"]] = k
        ak, sk = kumeler(anchor), kumeler(p["slug"])
        if ak == hk:
            sorun.append(f"{k}: anchor ('{anchor}') bu sayfanın ana kelimesi; başka sayfaya bu anchor'la link verilirse "
                         "iki sayfa aynı kelimede yarışır")
        if duzle(anchor) in JENERIK_ANCHOR or len(anchor.split()) > 6:
            sorun.append(f"{k}: anchor aranan terim değil ('{anchor}')")
        if ak and sk and not (ak & sk):
            uyari.append(f"{k}: anchor ('{anchor}') hedef sayfanın kelimesiyle örtüşmüyor ({p['slug']})")
        aile = (p["c"], p["g"], p["b"], p["q"])
        if p["c"] and aile in cids:
            sorun.append(f"{k} ve {cids[aile]} aynı kategori kimliğine gidiyor")
        cids[aile] = k
        if sayfalar is not None and p["url"] not in sayfalar and not a.canli:
            uyari.append(f"{k}: hedef sitemap envanterinde yok, canlı olduğu teyit edilmeli ({url})")
        ayni_ad = [u for u, s in (sayfalar or {}).items() if s["kume"] == sk and u != p["url"] and not s["b"] and not p["b"]]
        if ayni_ad and not a.canli:
            uyari.append(f"{k}: aynı ada sahip {len(ayni_ad)} sayfa daha var; doğru (ürünü olan, canonical) kimlik --canli ile teyit edilmeli")
    link_bolum, bolum = {}, "Giriş"
    for t, v in g:
        if t == "H2":
            bolum = v
        elif t != "tablo":
            for k in re.findall(r"\[(LINK\d+)\]", str(v)):
                link_bolum.setdefault(bolum, []).append(k)
    for b, ks in link_bolum.items():
        if len(ks) > (6 if hedef.get("b") else 4):
            uyari.append(f"'{b}' bölümünde {len(ks)} link var; linkler bölümlere yayılır")
    for t, v in g:
        if t == "p" and len(re.findall(r"\[LINK\d+\]", v)) > 2:
            uyari.append(f"tek paragrafta {len(re.findall(r'\[LINK\d+\]', v))} link: {duz(v)[:60]}…")
    if a.canli:
        import kategori, time
        for k, (anchor, url) in linkler.items():
            c = kategori.oku(url); time.sleep(0.6)
            if c.get("hata"):
                uyari.append(f"{k}: canlı okunamadı ({url})"); continue
            if c.get("durum") != 200 or c.get("yonlendirme"):
                sorun.append(f"{k}: hedef {c.get('durum')} / yönlendirme {c.get('yonlendirme')}")
            if not c.get("canonical_kendisi"):
                sorun.append(f"{k}: hedefin canonical'ı başka sayfa ({c.get('canonical')}); link canonical adrese verilir")
            if c.get("index") is False:
                sorun.append(f"{k}: hedef noindex ({url}); noindex sayfaya link verilmez")
            if not (c.get("urun_sayisi") or 0):
                sorun.append(f"{k}: hedefte ürün yok ({url})")
            elif c["urun_sayisi"] < 8:
                uyari.append(f"{k}: hedefte yalnız {c['urun_sayisi']} ürün var ({url})")

    # --- kelime sahipliği
    if a.sahiplik:
        s = json.load(open(a.sahiplik, encoding="utf-8"))
        baska = [(x, kumeler(x["kelime"])) for x in s["satirlar"] if x["kova"] == "BAŞKA SAYFA"]
        baska = [(x, k) for x, k in baska if k - hk and all(len(t) > 2 for t in k - hk)]
        cins = kumeler("kadin erkek cocuk bebek kiz")
        link_url = {url_coz(u)["url"] for _, u in linkler.values() if url_coz(u)}
        for b in h2 + h3:
            bk = kumeler(b)
            for x, k in baska:
                if k <= bk:
                    msg = f"başlık başka sayfanın kelimesini hedefliyor: '{b}' -> '{x['kelime']}' ({x['sahip']})"
                    zayif = any(z in (x["sahip"] or "") for z in ("/mag/", "/content/", "/search?q=")) or \
                        (hk & cins and not k & cins)      # cinsiyetli hedefte cinsiyetsiz sahip: çatı sayfa
                    (uyari if zayif else sorun).append(msg + (" [zayıf sahip: okuyarak karar ver]" if zayif else ""))
                    break
        for q, _ in sss:
            qk = kumeler(q)
            for x, k in baska:
                if k <= qk:
                    uyari.append(f"SSS sorusu başka sayfanın kelimesini taşıyor: '{q}' -> '{x['kelime']}' ({x['sahip']})")
                    break
        # başka sayfanın kelimesi gövdede linksiz ve tekrar tekrar geçiyorsa sayfa o kelimeye de oynuyor demektir
        gd = duzle(ciplak + " " + " ".join(a_ for a_, _ in linkler.values()))     # etiketler hariç, anchor'lar dahil
        for x, k in baska[:60]:
            ifade = duzle(x["kelime"])
            n_ = len(re.findall(r"\b" + re.escape(ifade), gd))
            if n_ >= 2:
                uyari.append(f"'{x['kelime']}' gövdede {n_} kez geçiyor (sahipli kelime en fazla bir kez, anchor olarak); sahibi {x['sahip']}")
        serbest = [x for x in s["satirlar"] if x["kova"] == "SERBEST"][:25]
        td = duzle(tum)
        eksik = [x for x in serbest if not (kumeler(x["kelime"]) - hk) <= kumeler(td)]
        if eksik:
            uyari.append("karşılanmayan SERBEST kelimeler (bilinçli dışarıda bırakıldıysa sorun değil): " +
                         ", ".join(f"{x['kelime']} ({x['hacim']})" for x in eksik[:12]))

    # --- uzunluk: rakip medyanı
    if a.arastirma:
        r = json.load(open(a.arastirma, encoding="utf-8"))
        rk = [x.get("kelime") for x in r.get("rakip_icerik") or [] if (x.get("kelime") or 0) >= 300]
        if rk:
            med = statistics.median(rk)
            if kelime + len(duz(tablo_metin).split()) < med:
                uyari.append(f"gövde {kelime} kelime; içerikli rakiplerin medyanı {med:.0f} ({', '.join(map(str, rk))})")

    # --- biçim ve dil
    canli_marka = ""
    if a.kayit:
        kk = json.load(open(a.kayit, encoding="utf-8"))
        canli_marka = duzle(" ".join(ad for ad, _ in kk.get("markalar") or []))
    for pat, ad in BICIM:
        for m in re.finditer(pat, tum):
            if ad == "rakip perakendeci adı" and duzle(m.group(0)).strip() in canli_marka:
                continue            # sayfada satılan marka (ör. Beymen Business), rakip değil
            sorun.append(f"{ad}: …{tum[max(0, m.start() - 40):m.end() + 40]}…")
    for pat, ad in UYARI_DESEN:
        bul = [tum[max(0, m.start() - 30):m.end() + 25] for m in re.finditer(pat, tum)]
        if bul:
            uyari.append(f"{ad} ({len(bul)}): " + " | ".join(f"…{b}…" for b in bul[:4]))
    kalin = sum(len(re.findall(r"\*\*[^*]+\*\*", re.sub(r"^\*\*[^*]+\*\*", "", i))) for t, i in g if t in ("p", "mad", "li"))
    if kalin > max(8, len(h2) * 3):
        uyari.append(f"{kalin} kalın vurgu var; bölüm başına iki üç vurgu yeterli")
    # Kalın etiketli maddede ilk cümle özneyi yeniden kurmalı: etiket silinince cümle anlamını korur.
    for t, i in g:
        m = re.match(r"\*\*(.+?):\*\*\s*(.+)", i) if t == "mad" else None
        if m:
            et = {w[:4] for w in duzle(m.group(1)).split() if len(w) >= 4}
            ilk = re.split(r"(?<=[.!?;])\s+", duz(m.group(2)))[0]
            bas = {w[:4] for w in duzle(ilk).split()[:4]}
            if et and not (et & bas):
                uyari.append(f"madde ilk cümlesi özneyi kurmuyor (etiket silinince anlamsız kalabilir): {duz(i)[:90]}")
    sayilar = sorted({m.group(0).strip() for m in re.finditer(
        r"%\s?\d[\d.,]*|\bIP[X\d]\d?\b|(?<![\w%])\d[\d.,x]*\s?(?:derece|°C?|cm|mm|gr|kg|ml|saat|gün|yıl|kat|tel)?", govde_metin + " " + " ".join(duz(c) for _, c in sss))})
    if sayilar:
        uyari.append("metindeki rakamlar (her birinin kaynağı var mı?): " + ", ".join(sayilar[:25]))

    # --- SSS
    if not sss:
        sorun.append("SSS yok")
    elif not 5 <= len(sss) <= 12:
        uyari.append(f"{len(sss)} SSS var; 6-10 arası hedeflenir")
    h_kume = [kumeler(b) for b in h2 + h3]
    for q, c in sss:
        n_ = len(duz(c).split())
        if not q.strip().endswith("?"):
            sorun.append(f"SSS sorusu soru işaretiyle bitmiyor: {q}")
        if n_ > 80:
            sorun.append(f"SSS yanıtı {n_} kelime (en fazla 80): {q}")
        elif n_ < 20:
            uyari.append(f"SSS yanıtı {n_} kelime, soruyu karşıladığı kontrol edilsin: {q}")
        if kumeler(q) in h_kume:
            uyari.append(f"SSS sorusu bir başlıkla aynı; gövdede yanıtlanan soru SSS'de tekrarlanmaz: {q}")
        if re.match(r"(?i)\s*(yukarıda|daha önce|belirtildiği)", duz(c)):
            sorun.append(f"SSS yanıtı gövdeye gönderme yapıyor: {q}")

    # kip dağılımı: cümlelerin yüklemine (son kelimesine) bakılır
    yuklem = [re.sub(r"\W+$", "", c).split()[-1].lower() for t, i in g if t in ("p", "mad", "li")
              for c in re.split(r"(?<=[.!?;:])\s+", duz(i)) if re.sub(r"\W+$", "", c).split()]
    kip = {"-iyor": 0, "-ir/-ar": 0, "-ebilirsiniz": 0, "-malı": 0, "-mıştır": 0, "-mektedir": 0, "isim/-dır": 0, "emir": 0}
    for y in yuklem:
        if re.search(r"(?:ıyor|iyor|uyor|üyor)$", y): kip["-iyor"] += 1
        elif re.search(r"(?:abilirsiniz|ebilirsiniz)$", y): kip["-ebilirsiniz"] += 1
        elif re.search(r"(?:malıdır|melidir|malı|meli|gerekir)$", y): kip["-malı"] += 1
        elif re.search(r"(?:mıştır|miştir|muştur|müştür)$", y): kip["-mıştır"] += 1
        elif re.search(r"(?:maktadır|mektedir)$", y): kip["-mektedir"] += 1
        elif re.search(r"(?:[ıiuü]n|[ae]y[ıi]n)$", y) and re.search(r"(?:yın|yin|ın|in|un|ün)$", y): kip["emir"] += 1
        elif re.search(r"(?:[dt][ıiuü]r)$", y): kip["isim/-dır"] += 1
        elif re.search(r"(?:[ıiuü]r|[ae]r|maz|mez|l[ıi]r|n[ıi]r)$", y): kip["-ir/-ar"] += 1
    # tek kipe kilitlenen metin makine çıktısı gibi okunur
    top = sum(kip.values()) or 1
    if kip["-ir/-ar"] / top > 0.7:
        uyari.append(f"gövde geniş zamana kilitlenmiş (%{kip['-ir/-ar'] / top * 100:.0f}); ürün gamı ve anlatı cümleleri "
                     "şimdiki zamanla, öneriler '-ebilirsiniz' ile çeşitlendirilebilir")
    eksiz = len(re.findall(r"(?:^|[.!?]\s+)(?:[A-ZÇĞİÖŞÜ]\w+ )?" + re.escape(d["main_kw"]) + r"[, ]", ciplak, re.I))
    # yalnız çok kelimeli ve iyelik eki almamış kategori adlarında anlamlı ("kadın mont" -> "kadın montu");
    # "nevresim takımı", "güneş gözlüğü", tek kelimelik adlar ve marka adları zaten doğal biçimdedir
    son = duzle(d["main_kw"]).split()[-1]
    if eksiz >= 4 and len(d["main_kw"].split()) >= 2 and son[-1] not in "iu" and not hedef.get("b"):
        uyari.append(f"ana kelime {eksiz} cümlede yalın (eksiz) biçimde özne konumunda; cümle içinde çekimli biçim "
                     "doğal olur ('kadın montu', 'kadın montları')")
    print(f"{d['kategori']}: gövde {kelime} kelime · {len(h2)} H2 · {len(h3)} H3 · {len(linkler)} link · {len(sss)} SSS "
          f"(SSS {sum(len(duz(c).split()) for _, c in sss)} kelime) · ana kelime {gecis} kez (%{yogunluk:.1f}) · "
          "kip: " + ", ".join(f"{k} {v}" for k, v in kip.items()))
    for u in uyari:
        print("NOT:", u)
    print("SORUN YOK" if not sorun else "SORUNLAR:\n  " + "\n  ".join(sorun))
    sys.exit(1 if sorun else 0)


if __name__ == "__main__":
    main()
