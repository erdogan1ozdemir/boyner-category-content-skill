# Araştırma ve doğrulama: hangi bilgi hangi kaynaktan

## Kaynak sırası

| Bilgi | Birincil kaynak | İkincil | Not |
|---|---|---|---|
| Sayfadaki ürün gamı (alt türler, markalar, kalıp, materyal, renk) | `kategori.py` (sayfanın canlı filtre verisi) | - | Tek geçerli kaynak. Filtrede olmayan yazılmaz |
| Hedef URL'nin doğruluğu | `kategori.py` + SERP + GSC | `envanter.py sahip` | Dört sinyal örtüşmeli (bkz. sahiplik dosyası) |
| Arama hacmi, mevsimsellik | `arastirma.py` kelime kümesi | Ahrefs / SEOmonitor MCP (bağlıysa) | 12 aylık ortalama + zirve ayı |
| Sorular | SERP PAA, bilgi niyetli SERP PAA, otomatik tamamlama | Rakip SSS'leri | Uydurulmaz |
| Rakip içerik yapısı | `arastirma.py` rakip_icerik | Sayfayı tarayıcıyla açmak | Başlıklar konu kapsamı için okunur, kopyalanmaz |
| Hangi Boyner sayfası hangi kelimede | GSC `query,page` (ücretsiz, 90 gün) | SEOmonitor `get_ranking_pages` (kampanya 84056, Boyner, 4.600 takipli kelime; ücretsiz, yalnız takipli kelimeler; Türkiye için domain araştırma verisi yok) → Ahrefs `site-explorer-organic-keywords` (yalnız `keyword,best_position,best_position_url` sütunları ücretsiz; hacim, KD ve trafik sütunları satır başına 10 birim) → `arastirma.py` Boyner haritası (DataForSEO, ücretli, son çare) | SERP tek gün, GSC 90 gün |
| Malzeme, dolgu, kumaş bilgisi | Üretici / marka sayfası, standart (ör. dolgu gücü tanımı) | Genel başvuru kaynakları | Sayısal değer ancak kaynakla |
| Bakım ve yıkama | Üretici bakım talimatı, tekstil bakım sembolleri | - | "Etiketteki talimat esastır" cümlesi eklenir |
| Kozmetik içerik ve etki | Marka ürün sayfası | Dermatoloji kaynakları | İddia değil işlev: "yardımcı olur" |
| Boyner hizmetleri (teslimat, iade, Boyner Now, Hopi) | `boyner.com.tr/content/...` ilgili sayfa | `boyner.com.tr/yardim` | Süre ve tutar rakamı yazılmaz |

## İlk 5 SERP nasıl okunur

`arastirma.py` ilk 5 rakip sayfanın başlıklarını, kelime sayısını ve sorularını verir. Bakılacaklar:

1. **Ortak konular:** beş rakibin üçünde geçen başlık konusu (seçim ölçütü, kombin, bakım) bizim iskelette de
   karşılanmalı. Bu, Google'ın o sorguda beklediği kapsamdır.
2. **Eksik konular:** hiçbir rakipte olmayan ama soru verisinde çıkan konu (beden seçimi, su geçirmezlik
   farkı) ayrışma fırsatıdır; bir H3 ya da SSS ile karşılanır.
3. **Biçim:** rakiplerde tablo, liste, SSS var mı? Yoksa bunları eklemek tek başına fark yaratır.
4. **Uzunluk tabanı:** içerik taşıyan rakiplerin medyanı.

Rakip sayfa okuma sırası (betikte otomatik; hepsi bağlama token yazmaz):

| Sıra | Yöntem | Maliyet | Not |
|---|---|---|---|
| 1 | doğrudan indirme (`curl`) | ücretsiz, ~1 sn | JavaScript'siz sayfalar |
| 2 | `r.jina.ai` okuyucusu | ücretsiz, ~5 sn | JavaScript'le oluşan sayfalar; kimlik anahtarsız dakikada sınırlı istek kabul eder, 5 rakipte sorun olmaz |
| 3 | yerel Playwright (`scripts/pw_oku.py`) | ücretsiz, ~6-13 sn | bot korumalı sayfalar (Trendyol); headless olmazsa headed denenir |
| 4 | DataForSEO sayfa ayrıştırma | ücretli | son çare |

MCP Playwright'ı (`browser_navigate`) elle kullanmak her sayfada 3-5 bin token bağlama yazar; betiğin
okuyamadığı nadir sayfa için kalır. Pazar yeri kategori sayfalarında H2'ler çoğunlukla ürün adıdır ve
editoryal metin yoktur (Trendyol kadın mont sayfasında yalnız ürün kartları vardı); bu sayfalar başlık kaynağı
sayılmaz. LCW kadın mont sayfası gibi bazı markaların sayfasında zaten ~100 kelimelik kısa metin vardır;
kelime sayısı düşükse bu bir okuma hatası değil sayfanın kendi durumudur.

SERP'te pazar yerleri (Trendyol, Hepsiburada) ile marka siteleri karışıktır. Pazar yerlerinin kategori
metinleri genellikle kısa ve şablondur; marka sitelerininki (Lufian, Oxxo, Mavi) daha uzundur. Taban olarak
içerik taşıyanlar alınır.

## Mevsimsellik

Giyim kelimelerinin çoğu mevsimseldir. "Kadın mont" 12 aylık ortalaması 33.100 iken yaz aylarında ortalama
5.800'e iner, zirvesi Aralık'tadır. Brief'te:

- Main KW Hacim sütununa 12 aylık ortalama yazılır.
- DİKKAT satırına zirve ayı ve son üç ay ortalaması yazılır.
- İçerik zirveden 6-8 hafta önce yayında olmalıysa bu da DİKKAT'e not edilir.

## Bilinen tuzaklar

- **Aynı ada sahip birden çok kategori kimliği.** İlk çıkan adaya yazma; `kategori.py` ile ürün sayısına ve
  breadcrumb'a bak.
- **`g25462663`** ikinci bir "kadın" cinsiyet kimliğidir (plaj giyim, blazer gibi bazı ağaçlarda). `g3731`
  ile aynı kelimeye oynayabilir.
- **Cinsiyet + kategori sayfasının `PageType` değeri `BrandCategoryGender`** görünür; marka içermese de bu
  tip döner. Yanıltmasın.
- **Arama ve filtre adresleri (`/search?q=`, `?renk=`) Cloudflare doğrulamasına takılır;** `kategori.py`
  bunları okuyamaz. Envanterde oldukları bilinir, canlı durumları betikle teyit edilemez.
- **Otomatik tamamlama önerilerinde alakasız sonuçlar çıkar** ("montale en iyi kadın parfümü"); öneriler
  elenerek kullanılır.
- **Boyner haritasında ürün sayfası (`-p-`) sıralanıyorsa** o kelimenin kategori düzeyinde sahibi yoktur;
  kelime SERBEST sayılabilir.
- **Mevcut `Content` alanı Google Docs kalıntısı taşır** (ilk harfi kopmuş başlıklar: "K ız Çocuk Bluz").
  Mevcut içerik revize edilecekse metin `kategori.py --icerik` ile düz okunur, HTML'i taşınmaz.
