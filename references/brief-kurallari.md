# Brief Excel'i: sütunlar ve kurallar

Brief, kategori başına **tek satır**dır. Dosya adı `Boyner kategori içerik briefleri.xlsx`. Excel, içerik
yazılacak tüm kategori sayfalarını **kategori tipine göre sekmelerde** taşır: `Kategori` (cinsiyetsiz kategori
sayfaları), `Kadın`, `Erkek`, `Çocuk`, `Bebek` (cinsiyet + kategori sayfaları). `brief_satiri.py --kur`
sekmeleri sitemap envanterinden kurar; her sayfa `Bekliyor` durumunda bir satırdır. Brief hazırlandığında
satır URL'ye göre bulunup doldurulur ve `Hazır` olur. Envanterde olmayan bir sayfa (sitemap ana ağaçtaki bazı
sayfaları taşımıyor) ilgili sekmenin sonuna eklenir.

## Düzen

Tablo başlığı 1. satırda, veri 2. satırdan başlar; üstte not bloğu ve birleştirilmiş hücre yoktur.
Başlık Calibri 11 kalın beyaz, `#434343` dolgulu; gövde Calibri 10 `#10332F`, sola ve dikeyde ortalı,
kaydırmalı. `scripts/brief_satiri.py` biçimi kendisi kurar.

## Sütunlar

**Kategori** - sayfanın adı ("Kadın Mont").

**URL** - teyit edilmiş hedef adres (bkz. `sahiplik-ve-cannibalization.md`, Adım 1).

**Brief** - `Bekliyor` ya da `Hazır`; betik doldurur. Kurulumda Kategori sütunu slug'dan üretilir (Türkçe
karaktersiz); brief hazırlanınca sayfanın gerçek adıyla değişir.

**Main KW** - sayfanın ana kelimesi, küçük harfle. Kategori sorgusunun en hacimli doğal biçimi
("kadın mont"; "mont kadın" ya da "bayan mont" değil).

**Main KW Hacim** - 12 aylık ortalama aylık arama, sayı olarak. Mevsimsel kategorilerde ortalama yanıltır:
zirve ayı ve son üç ay ortalaması DİKKAT satırına yazılır.

**İkincil ve Uzun Kuyruk Kelimeler** - aynı hücrede alt alta `kelime (hacim)`, hacme göre azalan. Yalnız
HEDEF ve SERBEST kovasındaki kelimeler. Hacmi olmayan ama otomatik tamamlamadan gelen hedefli ifade `(-)`
ile yazılır. 15-25 kelime yeter; aynı kök kümesinin varyantları ("kapitone mont kadın", "kapitoneli mont
kadın") tek satırda birleştirilir.

**Alt Başlıklar** - `H2: Başlık`, `H3: Başlık` satırları. Sabit iskelet yoktur: başlıklar o kategorinin
araştırmasından (rakip başlıkları, PAA, SERBEST kelime kümeleri, arama eğilimi) kurulur ve sahiplik
süzgecinden geçer (bkz. `icerik-kurallari.md`, bölüm 3-4; `scripts/baslik_adaylari.py`). Başlıkların yanına
kelime sayısı yazılmaz.

**İçerik Kurgusu** - şu sırayla:

```
TON: Hitap "siz"; bilgili mağaza danışmanı sesi; sıfat yerine özellik.

AÇILIŞ: Başlıksız 1-2 paragraf. İlk cümle ana kelimeyle tanım; ikinci paragraf Boyner'deki gam (türler, kalıplar, markalar: ...).

H2 · Başlık: Bu bölümde ne anlatılır, hangi kelime karşılanır, hangi biçim (liste / tablo / H3). [dayanak: 3 rakip + PAA]
H2 · Başlık: ...

SSS: Ayrı modül; gövde kelime sayısına dahil değil.

BİÇİM: "•" satırları ve numaralı adımlar (tablo ve liste biçimi yok), kalın vurgu, link sayısı.
UZUNLUK: Hedef 1.500-2.500 kelime gövde; rakip medyanı ... kelime (tekrar yok, yeni bilgi).
DİKKAT: Yazılmayacaklar, sahiplik uyarıları, mevsimsellik, teyit edilecekler.
```

Her H2 satırının sonunda başlığın **dayanağı** köşeli parantezle yazılır (`[dayanak: 3 rakip]`,
`[dayanak: PAA]`, `[dayanak: "kışlık" kümesi 2.780]`, `[dayanak: filtre ekseni]`); dayanağı yazılamayan başlık
açılmaz. Kurgu satırları telgraf üslubuyla yazılır ve yaklaşık 30 ekran satırına sığar (Excel satır yüksekliği
sınırı 409 punto). Sayfanın canlı kaydından gelen somut adlar (alt kategoriler, markalar, filtre değerleri)
ilgili H2 satırına yazılır; içerik ekibi olmayan ürünü uydurmasın.

**Link Verilecek Sayfalar** - numaralı liste, her link iki satır:

```
1. anchor metni : https://www.boyner.com.tr/...
   H2 · Bölüm adı bölümünde, hangi cümlede.
```

5-8 link; seçim ve dağılım `ic-link-kurallari.md`'de.

**Kapsam Dışı Kelimeler (Sahibi Başka Sayfa)** - BAŞKA SAYFA kovasının hacme göre ilk 10-15 kelimesi:

```
kadın şişme mont (6.600) -> /kadin-sisme-mont-x-g3731-c23896555
columbia kadın mont (18.100) -> /columbia-kadin-mont-x-b596-g3731-c23896554
```

Bu sütun brief'in cannibalization sigortasıdır: içerik ekibi hangi kelimeye başlık açmayacağını buradan okur.
Site düzeyinde çakışma tespit edildiyse (aynı kelimede iki sayfa) sütunun sonuna not düşülür.

**SSS'ler** - numaralı soru, altında `Yanıtta:` satırı. 6-10 soru. Kaynak PAA, bilgi niyetli SERP,
otomatik tamamlama ve SERBEST soru kelimeleri; soru uydurulmaz. Brief yalnız soruyu ve yanıtta geçmesi
gerekeni verir.

**Yanıt Biçimi** - kategoriler arasında değişmeyen metin, olduğu gibi kopyalanır:

```
• Her yanıt 30-70 kelimedir (en fazla 80).
• İlk cümle soruyu doğrudan yanıtlar (evet, hayır ya da net bilgi); gerekçe ikinci cümlede verilir.
• Yanıt kendi başına okunur; "yukarıda belirtildiği gibi" türünde gönderme yapılmaz.
• Kategori adı yanıtta en az bir kez tam haliyle geçer.
• Hitap "siz"dir; fiyat, indirim ve tarih yazılmaz.
• Gövdedeki cümleler birebir tekrarlanmaz; SSS daha kısa ve doğrudan yazılır.
• Doğrulanamayan bilgi yazılmaz; yanıtlanamayan soru listeden çıkarılır.
```

**Mevcut Durum** - sayfanın bugünkü hâli, 4-6 satır:

```
Sayfa tipi: BrandCategoryGender · ürün: 2.431 · canonical: kendisi
Mevcut içerik: yok (ya da: 607 kelime, 12 H3, 12 link, SSS yok)
Google (mobil, 02.10.2026): "kadın mont" 1. sıra
GSC 90 gün: 41.200 click · 1.2M impression · ort. pozisyon 4.1
İlk 5 rakip içerik medyanı: 1.054 kelime
```

## Briefe girmeyenler

Fiyat aralığı, ürün sayısı hedefi, kampanya bilgisi, KAPSAM DIŞI kovası (rakip perakendeci kelimeleri).
