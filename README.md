# Boyner Kategori Sayfası: Brief ve İçerik

boyner.com.tr kategori (listeleme) sayfaları için **içerik briefi** ve **SEO + GEO uyumlu kategori içeriği**
üreten Claude Code skill'i, referansları, betikleri ve örnek çıktıları.

Boyner'de 34 binin üzerinde listeleme sayfası var: kategori, cinsiyet + kategori, marka, marka + cinsiyet +
kategori, filtre ve arama sayfaları. Bu depo, o sayfalara içerik yazılırken üç şeyi güvenceye alan süreci
tutar:

- **Bir kelime, bir sahip.** Her kelime hangi Boyner sayfasına aitse orada hedeflenir; içerik başka sayfanın
  kelimesine başlık açmaz, o sayfaya link verir (cannibalization kontrolü).
- **Başlıklar araştırmadan çıkar.** Sabit şablon yoktur; her kategorinin iskeleti ilk 5 rakibin başlıkları,
  PAA soruları, uzun kuyruk kelime kümeleri ve arama eğiliminden kurulur.
- **İçerik sayfadaki gerçek ürün gamına dayanır.** Türler, markalar ve malzemeler sayfanın canlı filtre
  verisinden gelir.

## İçindekiler

```
SKILL.md                              Çalışma akışı (7 faz) ve değişmeyen kurallar
references/
  sahiplik-ve-cannibalization.md      Hedef URL teyidi, dört kova, GSC çapraz kontrolü
  arastirma-ve-dogrulama.md           Kaynak sırası, ilk 5 SERP okuma, mevsimsellik, bilinen tuzaklar
  icerik-kurallari.md                 Ton ("siz"), başlık iskeleti kurma, yapı taşı havuzu, GEO yazımı, SSS
  ic-link-kurallari.md                5-8 link: roller, anchor kuralları, hedef teyidi
  brief-kurallari.md                  Brief Excel'inin on iki sütunu
  kontrol-listesi.md                  Teslim öncesi denetim
scripts/
  envanter.py                         Altı sitemap'ten sayfa envanteri; kelime sahibi ve ilişkili sayfa sorguları
  kategori.py                         Sayfanın canlı kaydı: meta, mevcut içerik, alt kategoriler, markalar, filtreler
  arastirma.py                        SERP + PAA + AI Overview, kelime kümesi, öneriler, ilk 5 rakip içeriği, Boyner haritası
  sahiplik.py                         Kelime sahipliği tablosu: HEDEF / SERBEST / BAŞKA SAYFA / KAPSAM DIŞI
  baslik_adaylari.py                  Başlık adayları (rakip, PAA, kelime kümeleri), sahiplik süzgeciyle
  brief_satiri.py                     Brief Excel'ine kategori satırı ekler
  icerik_denetim.py                   Yapı, link, sahiplik, biçim ve SSS denetimi
  icerik_docx.py                      İçerik JSON'undan Word dosyası
  cms_html.py                         CMS'e girilecek temiz HTML (+ isteğe bağlı FAQPage JSON-LD)
  ortak.py                            Ortak yardımcılar
assets/brief-sablonu.xlsx             Boş brief Excel'i
examples/                             "Kadın Mont" örneği: brief satırı, içerik JSON'u, Word, HTML
```

## Hızlı kullanım

```bash
python3 scripts/envanter.py yenile                                   # 7 günde bir
python3 scripts/kategori.py URL --cikti kayit.json                   # canlı kayıt
python3 scripts/arastirma.py "kadın mont" --url URL --cikti arastirma.json
python3 scripts/sahiplik.py --arastirma arastirma.json --url URL --kayit kayit.json --teyit --cikti sahiplik.json
python3 scripts/baslik_adaylari.py --arastirma arastirma.json --sahiplik sahiplik.json --kayit kayit.json
python3 scripts/brief_satiri.py --xlsx "Boyner kategori içerik briefleri.xlsx" --json satir.json
python3 scripts/icerik_denetim.py --json icerik.json --sahiplik sahiplik.json --arastirma arastirma.json --canli
python3 scripts/icerik_docx.py --json icerik.json --out kadin-mont-icerik.docx
python3 scripts/cms_html.py --json icerik.json --out kadin-mont-icerik.html
```

`arastirma.py`, DataForSEO kimliğini `~/.claude.json` içindeki `dfs-mcp` yapılandırmasından okur; depoda
kimlik bilgisi tutulmaz. GSC verisi `gsc` MCP sunucusuyla (OAuth) çekilir.

## Sürecin özeti

- Hedef URL dört sinyalle teyit edilir: Boyner'de aynı ada sahip birden çok kategori kimliği bulunur.
- İçerik başlıksız girişle açılır (sayfada H1 var), araştırmadan kurulan H2/H3'lerle ilerler, 6-10 soruluk
  SSS ile kapanır. Hitap "siz".
- Uzunlukta sınır yoktur; tabanı içerikli rakiplerin medyanı, tavanı kapsam belirler.
- İçerik başına 5-8 iç link: üst kategori, alt kategoriler, kardeş kategori, marka + kategori, tamamlayıcı
  kategori. Anchor hedef sayfanın ana kelimesidir.
- Fiyat, indirim, kampanya, yıl, ürün sayısı ve canlı kayıtta olmayan ürün bilgisi yazılmaz.

## Kurulum

```bash
git clone https://github.com/erdogan1ozdemir/boyner-category-content-skill.git \
  ~/.claude/skills/boyner-kategori-brief-icerik
```

Gereken Python paketleri: `openpyxl`, `python-docx`. İstekler `curl` ile atılır.
