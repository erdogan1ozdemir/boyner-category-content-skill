---
name: boyner-kategori-brief-icerik
description: boyner.com.tr kategori ve marka (listeleme) sayfaları için içerik briefi ve SEO + GEO uyumlu kategori içeriği üretir. Hedef kategoride ilk 5 SERP'i ve rakip içeriklerini inceler, kelime kümesini ve soru kalıplarını çıkarır, 34 bin sayfalık Boyner envanterine karşı kelime sahipliği (cannibalization) tablosu kurar, 5-8 çapraz iç link seçer; ardından "siz" diliyle, başlık iskeleti o kategorinin araştırmasından (rakip başlıkları, PAA, uzun kuyruk kümeleri, arama eğilimi) kurulan gövde metni ve answer-first SSS yanıtları yazar. Çıktılar - kategori tipine göre sekmeli ortak brief Excel'inde ilgili satır ve içerik Word dosyası; içerik teslimden önce bağımsız içerik değerlendirmesinden geçer. Şu durumlarda mutlaka kullan - kullanıcı bir Boyner kategori URL'si ya da kategori adı verip "kategori içeriği yaz", "kategori briefi", "bu kategoriye içerik", "SEO metni", "kategori açıklaması", "SSS yaz", "içeriği revize et" dediğinde · Boyner için uzun kuyruk kelime, alt başlık planı, iç link planı ya da cannibalization kontrolü istendiğinde · "hangi sayfa bu kelimenin sahibi", "bu kelimeye hangi Boyner sayfası oynuyor" diye sorulduğunda · içeriği zayıf ya da boş Boyner kategorileri aranırken · kullanıcı yalnız bir boyner.com.tr listeleme adresi yapıştırıp içerik beklediğinde. Boyner teknik SEO audit dosyaları ve müşteriye giden rapor/sunumlar bu skill'in işi değildir.
---

# Boyner Kategori Sayfası: Brief ve İçerik

Bu skill bir Boyner kategori sayfası için **iki çıktı** üretir:

1. **Brief satırı** - ortak Excel'de o sayfanın satırı. Excel, içerik yazılacak tüm kategori sayfalarını
   kategori tipine göre sekmelerde taşır (Kategori, Kadın, Erkek, Çocuk, Bebek, Marka); brief hazırlandıkça ilgili
   satır doldurulur.
2. **Kategori içeriği** - Word dosyası: başlıksız giriş, H2/H3 bölümleri ve SSS. Belge adı
   `{slug}: {tam URL}` biçimindedir (ör. `kadin-mont: https://www.boyner.com.tr/kadin-mont-x-g3731-c23896554`).

HTML çıktısı varsayılan akışta üretilmez (kullanıcı kararı, 02.10.2026); `scripts/cms_html.py` yalnız
kullanıcı açıkça isterse çalıştırılır.

Kullanıcı yalnız "brief" derse içerik yazılmaz; yalnız "içerik" derse brief satırı atlanır ama araştırma ve
sahiplik fazları yine yürütülür, çünkü içerik onlara dayanır.

## İşin özü

Boyner'de 34 binin üzerinde listeleme sayfası var (kategori, cinsiyet + kategori, marka, marka + cinsiyet +
kategori, filtre ve arama sayfaları) ve örneklenen kategori sayfalarının yaklaşık %6'sında içerik bulunuyor.
İki şey bu işi sıradan bir "SEO metni" işinden ayırır:

- **Her kelimenin tek bir sahibi vardır.** İçerik yalnız kendi sayfasının kelimelerini hedefler; başka
  sayfanın kelimesi başlığa çıkmaz, o sayfaya link olur. Bunu atlayan içerik sıralama kazandırmaz, iki
  sayfayı birbirine düşürür.
- **İçerik sayfadaki gerçek ürün gamına dayanır.** Türler, markalar, kalıplar ve malzemeler sayfanın canlı
  filtre verisinden gelir; satılmayan şey yazılmaz.

- **Başlık iskeleti sabit değildir.** Boyner giyimden kozmetiğe, evden spora uzanır; her kategorinin
  başlıkları kendi araştırmasından çıkar: ilk 5 rakibin başlıkları, PAA, uzun kuyruk kelime kümeleri ve
  kategorinin arama eğilimi.

Mevcut Boyner içeriklerinden yalnız **"siz" hitabı** alınır; yapıları ve üslupları örnek alınmaz
(kullanıcı kararı, 02.10.2026).

## Çalışma akışı

Fazları sırayla yürüt. Betikler `scripts/` altındadır ve bu klasörden çalıştırılır. Ara dosyalar için
oturumun geçici dizinini kullan (aşağıda `$T`).

### Faz 0 - Envanter

```bash
python3 scripts/envanter.py ozet        # "Envanter yok" derse ya da 7 günden eskiyse: envanter.py yenile
```

Altı sitemap'ten kurulan sayfa envanteri `~/.cache/boyner-kategori-brief/envanter.json` içinde durur.

### Faz 1 - Hedef sayfayı teyit et ve canlı kaydı oku

Kullanıcı URL verdiyse onu, kategori adı verdiyse adayları bul:

```bash
python3 scripts/envanter.py sahip "kadın mont"
python3 scripts/kategori.py {URL} --cikti $T/kayit.json
```

Boyner'de aynı ada sahip birden çok kategori kimliği bulunur; yanlış kimliğe yazılan içerik boşa gider.
Hedef dört sinyalle teyit edilir (aday listesi, ürün sayısı ve breadcrumb, Google'da sıralanan URL, GSC);
ayrıntı `references/sahiplik-ve-cannibalization.md` Adım 1'de. Canonical başka sayfayı gösteriyorsa, sayfa
noindex ise ya da sinyaller ayrışıyorsa yazmadan önce kullanıcıya sor.

`kategori.py` çıktısı içeriğin gerçeklik zeminidir: alt kategoriler, markalar, filtre değerleri (ürün çeşidi,
kalıp, materyal, renk), mevcut içerik ve link bulutu. Mevcut içerik varsa `--icerik` ile okunur; işe yarar
bilgi taşıyorsa yeni metne alınır, yapısı alınmaz.

### Faz 2 - Araştır

```bash
python3 scripts/arastirma.py "kadın mont" --url {URL} --cikti $T/arastirma.json [--ek "kadın kaban"]
```

Tek çağrıda toplar: Google SERP (mobil, Türkiye) ilk 10 ve Boyner'in sıralanan sayfası · bilgi niyetli SERP
("... nasıl seçilir") ile PAA ve AI Overview · kelime kümesi (hacim, zirve ayı, son üç ay) · otomatik
tamamlama soru ve uzun kuyruk önerileri · ilk 5 rakibin içerik iskeleti (başlık, kelime sayısı, soru) ·
ana kelimeyi taşıyan sorgularda sıralanan Boyner sayfaları.

Ardından GSC'den iki sorgu (`gsc` MCP, site `sc-domain:boyner.com.tr`, 90 gün): hedef sayfanın sorguları
(`get_search_by_page_query`) ve ana kelimeyi taşıyan sorgularda sayfa dağılımı
(`get_advanced_search_analytics`, `dimensions: "query,page"`). GSC'ye erişilemezse bu adım atlanır ve
atlandığı söylenir.

Rakip sayfalar nasıl okunur, hangi bilgi hangi kaynaktan doğrulanır: `references/arastirma-ve-dogrulama.md`.
Ürün bilgisi (malzeme, dolgu, bakım) yazılacaksa bu fazda kaynağından doğrulanır; gerekiyorsa web araması
yapılır.

### Faz 3 - Kelime sahipliğini çıkar

```bash
python3 scripts/sahiplik.py --arastirma $T/arastirma.json --url {URL} --kayit $T/kayit.json --teyit --cikti $T/sahiplik.json
```

`--kayit` sayfanın canlı alt kategori ve marka kırılımlarını sahip olarak öne alır: sitemap eski kategori
kimliklerini de taşıdığı için doğru adres canlı kayıttan gelir. Her kelime dört kovadan birine düşer: **HEDEF** (bu sayfanın), **SERBEST** (kendi sayfası olmayan uzun
kuyruk; bu sayfada karşılanır), **BAŞKA SAYFA** (sahibi belli; hedeflenmez, linklenir), **KAPSAM DIŞI**.
Betik biçime bakar, niyete bakamaz: tablo bir kez elle gözden geçirilir (SERBEST'teki marka ve renk
kelimeleri, çok adaylı sahipler). Nasıl yapılacağı `references/sahiplik-ve-cannibalization.md`'de.

Site düzeyinde çakışma görülürse (aynı kelimede iki Boyner sayfası sıralanıyor, arama sayfası kategori
sayfasının önünde) içerikle çözülmeye çalışılmaz; teslim notunda kullanıcıya bildirilir.

### Faz 4 - Başlık iskeletini ve briefi kur

```bash
python3 scripts/baslik_adaylari.py --arastirma $T/arastirma.json --sahiplik $T/sahiplik.json --kayit $T/kayit.json
```

Başlık adaylarını dört kaynaktan toplar (rakip başlıkları konuya göre kümelenmiş, PAA, SERBEST uzun kuyruk
kümeleri hacimleriyle, otomatik tamamlama) ve her adayı sahiplik tablosuna karşı işaretler: `[SAHİPLİ]` aday
başlık olamaz. İskelet bu listeden, kategorinin doğasına göre kurulur; kurma yöntemi ve yapı taşı havuzu
`references/icerik-kurallari.md` bölüm 3-4'te. Rakiplerin üçünden azı okunabildiyse ilk 5 sayfa tarayıcı
araçlarıyla da açılıp başlıklarına bakılır.


`references/brief-kurallari.md` sütunların biçimini anlatır. Özet:

- **Main KW** kategori sorgusunun en hacimli doğal biçimi; hacim 12 aylık ortalama, mevsimsellik DİKKAT'te.
- **İkincil ve uzun kuyruk** yalnız HEDEF ve SERBEST kovasından.
- **Alt başlıklar** araştırmadan kurulur ve her H2'nin dayanağı kurguda yazılır (`[dayanak: 3 rakip + PAA]`).
  Sıra okuyucunun karar yolunu izler: ne var → hangisi uyar → nasıl kullanılır/bakılır → hangi marka.
  Başka kategorinin iskeleti taşınmaz.
- **Linkler** 5-8 adet, rolleriyle (üst, alt, kardeş, marka + kategori, tamamlayıcı), yerleşeceği cümleyle.
  Kurallar `references/ic-link-kurallari.md`'de.
- **Kapsam Dışı Kelimeler** BAŞKA SAYFA kovasının ilk 10-15 satırı, sahibiyle.
- **SSS** 6-10 soru; PAA, otomatik tamamlama ve SERBEST sorulardan.

```bash
python3 scripts/brief_satiri.py --xlsx "Boyner kategori içerik briefleri.xlsx" --json $T/satir.json
```

Excel yoksa önce `--kur` ile kurulur (tüm kategori sayfaları sekmelere `Bekliyor` olarak eklenir); `--ozet`
sekme başına hazır ve bekleyen sayısını verir. Satır URL'ye göre bulunup doldurulur ve `Hazır` olur.

### Faz 5 - İçeriği yaz

`references/icerik-kurallari.md` yazmadan önce okunur. Özet:

- **Hitap baştan sona "siz".** Ses bilgili bir mağaza danışmanınınki: sıfat yerine özellik, süs yerine karar
  verdiren bilgi.
- Gövde **başlıksız 1-2 paragraflık girişle** açılır (sayfada H1 var); ilk cümle ana kelimeyle tanım, ikinci
  paragraf Boyner'deki gam. Ardından brief'teki iskeletle H2'ler; H3 yalnız H2 altında.
- **Her H2'nin ilk cümlesi başlığın sorusunu doğrudan yanıtlar**; bölüm kendi başına okunur. AI Overview ve
  diğer yapay zeka yanıtlarında alıntılanan birim budur.
- **Uzunlukta sınır yok;** tabanı içerikli rakiplerin medyanı, tavanı kapsam belirler. Bilgi taşımayan
  paragraf eklenmez.
- **Başlıklar arama diliyle yazılır** ve ana kelimeyi ya da ürün adını taşır ("Kadın Montlarda Boy, Kalıp ve
  Beden Seçimi", "Mevsimlik Kadın Mont Modelleri"); biçim hacme göre seçilir.
- **Kipler uygun yerlerde değişir** (tanım geniş zaman, katalog şimdiki zaman, tasarım `-mıştır`, öneri
  `-ebilirsiniz`; `-mektedir` kullanılmaz); özne ile yüklem uyuşur, ana kelime cümle içinde çekimlenir ("kadın montu").
- **Ticari kelimeler karşılanır:** "fiyatları" başlığı ve "uygun", "ekonomik", "kaliteli", "şık" gibi
  niteleyiciler kullanılır; net fiyat ve fiyat aralığı verilmez.
- **Sayılabilir şeyler listeyle, karşılaştırmalar tabloyla** verilir; içerikte en az bir tablo ya da liste
  bulunur.
- **BAŞKA SAYFA kelimesi başlık ya da SSS olmaz;** bir kez, tanım cümlesi içinde ve sahibine link veren
  anchor olarak geçer. SERBEST kelimeler H3, madde ya da SSS ile karşılanır.
- **İç link metnin içinden çıkar:** anchor silindiğinde cümle anlamlı kalır; anchor hedef sayfanın ana
  kelimesidir; bu sayfanın ana kelimesi başka sayfaya anchor olmaz.
- **İçerik mevcut ürün gamını anlatır:** yazılan her tür, marka, seri, kalıp ve malzeme canlı kayıtta vardır;
  gamda ağırlığı olan öne alınır. Taslak bitince kayıt bir kez daha okunur.
- **Tutarlılık:** tek tanım, gövde-SSS uyumu, genel adım / özel istisna ayrımı, kendi başına okunur maddeler
  (`icerik-kurallari.md`, Tutarlılık kuralları). En az iki tablo (ihtiyaca göre tür + iki seçenek
  karşılaştırması) ve numaralı karar adımları bulunur.
- **SSS yanıtları 30-70 kelime,** ilk cümle doğrudan yanıt, gövdeyi tekrar etmez.

İçerik şu JSON biçiminde yazılır (alanlar `scripts/icerik_docx.py` başında): `kategori`, `url`, `main_kw`,
`linkler` (`{"LINK1": [anchor, url]}`), `govde` (`["p" | "H2" | "H3" | "mad" | "li" | "tablo", içerik]`
listesi; köprüler `[LINK1]`, vurgu `**kalın**`), `sss` (`[soru, yanıt]`).

### Faz 6 - Denetle, üret, teslim et

```bash
python3 scripts/icerik_denetim.py --json $T/icerik.json --sahiplik $T/sahiplik.json --arastirma $T/arastirma.json --canli
python3 scripts/icerik_docx.py --json $T/icerik.json --klasor "Kategori İçerik"      # -> "kadin-mont: https://...docx"
```

Denetim bulgu verirse çıktı üretilmez; önce metin düzeltilir. `NOT:` satırları okunarak karar verilir.
Ardından `references/kontrol-listesi.md`'deki okuyarak yapılan kontroller geçilir.

**Ardından içerik bağımsız bir değerlendirmeden geçirilir.** Betik biçime bakar; özne-yüklem uyumu, anlam,
bilgi doğruluğu ve iç çelişki ancak okuyarak yakalanır. `seo-content` ajanına (yoksa `seo-content` skill'i
ile satır içi) içerik JSON'u verilir ve şunlar istenir: dil ve anlam (özne-yüklem, kayan özne, mantık), kip
kullanımı, başlıkların arama diline uygunluğu, bilgi doğruluğu, iç çelişki, SEO/GEO ve 100 üzerinden puan.
Ajana bilinçli kısıtlar (rakam yok, sahipli kelimelere başlık yok, link sayısı) söylenir ki bunları eksik
saymasın. Bulgular körü körüne uygulanmaz: skill kurallarıyla çelişen öneri (sayısal eşik ekleme, sahipli
kelimeye başlık) alınmaz. Düzeltmelerden sonra denetim betiği yeniden çalıştırılır ve Word dosyası üretilir.

Çıktılar çalışma klasörüne kaydedilir ve kullanıcıya gönderilir. Teslim notunda üç şey söylenir: hangi bilgi
hangi kaynaktan alındı · ne yazılmadı ve neden (sahibi başka sayfa olan kelimeler, teyit edilemeyen
bilgiler) · hangi konuda karar bekleniyor.

## Değişmeyen kurallar

- **Hedef URL teyit edilmeden içerik yazılmaz.** Aynı adlı kimliklerden hangisinin canlı, dolu ve sıralanan
  sayfa olduğu bilinmelidir.
- **Bir kelime, bir sahip.** Sahibi başka sayfa olan kelime için başlık, SSS ya da ayrı paragraf açılmaz.
- **Bu sayfanın ana kelimesi başka sayfaya anchor olmaz;** sayfa kendine link vermez; aynı hedefe iki kez
  link verilmez.
- **Link sayısı 5-8;** her hedef canlı, canonical ve ürünlü olmalıdır. Arama (`/search?q=`), kampanya ve
  outlet sayfalarına link verilmez.
- **Hitap "siz";** "sen", birinci çoğul ve "bayan" kullanılmaz.
- **Net fiyat, fiyat aralığı, indirim oranı, kampanya adı, yıl ve "bu sezon" yazılmaz** ("uygun", "ekonomik"
  gibi niteleyiciler ve rakamsız "Fiyatları" başlığı serbesttir). Sayfa bir yıl sonra da düzeltme
  istemeden doğru kalmalıdır. Ürün sayısı da yazılmaz.
- **Canlı kayıtta olmayan ürün bilgisi yazılmaz.** Boyner'de satılmayan marka, sitede filtrelenmeyen tür
  metne girmez. Rakip perakendeci adı geçmez.
- **Doğrulanamayan sayı ve iddia yazılmaz.** Sıcaklık değeri, dolgu gücü, "en çok tercih edilen" gibi
  ifadeler ancak kaynakla. Kozmetikte sağlık iddiası kurulmaz.
- **Boyner hizmetleri** (teslimat, iade, Boyner Now) yalnız sitenin kendi sayfasından teyit edilerek ve
  süre/tutar rakamı verilmeden anılır.
- **Sabit başlık şablonu kullanılmaz;** her başlığın araştırmada bir dayanağı vardır ve başlık aranabilir bir
  ifadedir.
- **Mevcut içeriklerin yapısı örnek alınmaz;** yalnız "siz" hitabı sürdürülür.
- İçerik Dili Rehberi bu çıktıya uygulanmaz (tüketiciye dönük metin). Uzun tire, emoji ve marka sembolü
  yine de kullanılmaz.

## Toplu çalışma ve aday seçimi

Birden fazla kategori istenirse her kategori için fazlar ayrı yürütülür; kardeş kategoriler (kadın mont,
kadın kaban, kadın şişme mont) aynı partide yazılıyorsa önce hepsinin sahiplik tablosu çıkarılır, sonra
yazılır: bir sayfanın SERBEST kelimesi, yanındaki sayfanın HEDEF kelimesi olabilir.

İçeriği zayıf kategori aranıyorsa: GSC'den gösterimi yüksek kategori sayfaları alınır, `kategori.py` ile
içerik durumu okunur (kelime sayısı, başlık, SSS). Boş ya da kısa içerikli, ürünü çok ve pozisyonu 4-15
arasında olan sayfalar ilk adaylardır.

## Referanslar

| Dosya | Ne zaman okunur |
|---|---|
| `references/sahiplik-ve-cannibalization.md` | Faz 1 ve 3'te. Hedef teyidi, dört kova, elle gözden geçirme, GSC çapraz kontrolü. |
| `references/arastirma-ve-dogrulama.md` | Faz 2'de. Kaynak sırası, ilk 5 SERP okuma, mevsimsellik, bilinen tuzaklar. |
| `references/brief-kurallari.md` | Faz 4'te, brief satırını kurarken. |
| `references/icerik-kurallari.md` | Faz 4'te iskeleti kurarken (bölüm 3-4) ve Faz 5'te yazmadan önce. Yapı taşı havuzu, GEO yazımı, SSS. |
| `references/ic-link-kurallari.md` | Link seçerken ve yerleştirirken. |
| `references/marka-sayfasi.md` | Hedef bir marka sayfasıysa (`-x-b...`): kelime sahipliği, yapı taşları, link kuralları. |
| `references/kontrol-listesi.md` | Faz 6'da, teslimden önce. |
| `examples/` | Örnek brief satırı ve içerik JSON'u; biçim referansı. |

Betikler DataForSEO kimliğini `~/.claude.json` içindeki `dfs-mcp` yapılandırmasından okur. Gereken Python
paketleri: `openpyxl`, `python-docx`. İstekler `curl` ile atılır.
