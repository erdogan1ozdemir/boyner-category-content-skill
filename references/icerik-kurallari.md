# İçerik yazımı: yapı, ton ve bölüm kalıpları

## İçindekiler

1. Ton ve hitap
2. Zaman kipi
3. Yapı: iskelet araştırmadan çıkar
4. Yapı taşı havuzu
5. Uzunluk
6. SEO, GEO ve AI Overview için yazım
7. Kelime sahipliği metne nasıl yansır
8. İç link metnin içinden çıkar
9. Madde listesi, tablo ve kalın vurgu
10. Bölüm bölüm ne yazılır
11. SSS yanıtları
12. Cümle kurgusu
13. Yazarken kaçınılacaklar

## 1. Ton ve hitap

Bu metin tüketiciye dönük kategori içeriğidir, rapor değil; İçerik Dili Rehberi bu çıktıya uygulanmaz.

**Hitap baştan sona "siz"dir.** Boyner'in kategori metinleri çoğunlukla ikinci çoğul konuşur
("tamamlayabilirsiniz", "tercih edebilirsiniz"); mevcut içeriklerden alınan tek şey budur. Sitede "sen" diliyle
yazılmış sayfalar da vardır (bazı marka içerikleri, `/content/boyner-now`); onlar örnek alınmaz. "Sen" dili,
birinci çoğul ("öneriyoruz", "tavsiye ederiz") ve "biz" kullanılmaz; marka kendinden "Boyner" diye söz eder.

Mevcut kategori içeriklerinin **yapısı ve üslubu örnek alınmaz** (kullanıcı kararı, 02.10.2026). O metinler
başlık hiyerarşisi tutmuyor (H3 ile başlıyor), liste ve tablo kullanmıyor, SSS taşımıyor ve "eşsiz bir
yolculuğa davet ediyor", "ışıltınızı ortaya çıkaran parçalar" gibi bilgi taşımayan cümlelerle dolu.
Yapı her kategoride araştırmadan kurulur.

Ses: **bilgili bir mağaza danışmanı.** Okuyucu ya ne alacağını biliyor ve seçenekleri görmek istiyor, ya da
iki tip arasında kararsız ve farkı öğrenmek istiyor. İkisi de süslü cümle değil, karar verdiren bilgi
bekliyor. Bu yüzden:

- **Sıfatla değil özellikle anlatılır.** "Göz alıcı montlar" yerine "kaz tüyü dolgulu, bel hizasında biten
  montlar". "Kaliteli kumaş" yerine "su itici dış yüzey".
- Moda dili serbesttir ama somut kalır: kalıp, boy, yaka, kumaş, renk, kombin. "Zahmetsiz şıklık",
  "stil yolculuğu", "tarzınızı konuşturun" gibi içi boş kalıplar yazılmaz.
- Ünlem en fazla bir yerde, kapanışta kullanılabilir.
- **Ticari niteleyiciler kullanılır:** "uygun fiyatlı", "en uygun", "ekonomik", "bütçeye uygun" ile "kaliteli",
  "şık", "premium" gibi kelimeler metinde doğal yerlerinde geçer (kullanıcı kararı, 02.10.2026); bunlar
  kategori aramalarının ticari niyetini karşılar. Net fiyat ve fiyat aralığı verilmez. Niteleyici bir özelliğe
  bağlanır: "kaliteli" tek başına değil, "kaliteli dolgusu ve sağlam fermuarı olan".

## 2. Zaman kipi

Tek kipe kilitlenen metin makine çıktısı gibi okunur; **uygun yerlerde farklı kipler kullanılır** (kullanıcı
kararı, 02.10.2026). Kip cümlenin işine göre değişir:

| Cümle ne yapıyor | Kip | Örnek |
|---|---|---|
| Tanım, her zaman geçerli bilgi | Geniş zaman | "Şişme mont, dolgulu kanallarıyla ısıyı gövdede tutar." |
| Boyner'deki ürün gamı, katalog | Şimdiki zaman | "Kategoride kapüşonlu, uzun ve kısa modeller yer alıyor." |
| Tasarım amacı | `-mıştır` | "Kayak montu pist için tasarlanmıştır." |
| Okuyucuya öneri | İkinci çoğul, olasılık | "Bel hizasında biten bir model tercih edebilirsiniz." |
| Ölçüt | İsim cümlesi | "Belirleyici olan dolgu miktarıdır." |
| Sıralı adım | İkinci çoğul emir | "Fermuarları kapatın." |

Ölçü dağılımdır: gövdede yüklemlerin %70'inden fazlası geniş zamandaysa metin ansiklopedi maddesine döner;
`icerik_denetim.py` yüklem dağılımını raporlar. **Çeşitlilik bu eşleşmenin dışına çıkılarak sağlanmaz:**
genel geçer bir bilgi ya da sınıflama şimdiki zamanla ("montlar ikiye ayrılıyor") yazılmaz, katalog bilgisi
geniş zamanla donuklaşmaz. Resmi `-mektedir / -maktadır` tüketici metninde ayrışır, kullanılmaz. Geniş zaman
ağır basıyorsa çözüm kipi zorlamak değil, metne katalog cümlesi (Boyner'de ne var), öneri cümlesi ve isim
cümlesi eklemektir.

**Bir paragrafta edilgen ile "siz" arasında gidip gelinmez.** "Üç ölçüte bakılır... belirlediğinizde" yerine
"üç ölçüte bakabilirsiniz... belirlediğinizde". Gereklilik kipi ("-malıdır") kategori metninde sert durur;
yalnız gerçek gereklilikte (bakım, güvenlik) kullanılır.

**Kipler arası sert geçiş yumuşatılır:** edilgen bir giriş cümlesinden emir kipli adımlara geçilecekse giriş
"şu adımları izleyebilirsiniz" diye okuyucuya döner.

## 3. Yapı: iskelet araştırmadan çıkar

Sayfada H1 kategori adı olarak zaten bulunur ("Kadın Mont Modelleri"). Gövdeye H1 yazılmaz; metin
**başlıksız kısa bir girişle** açılır, ardından H2'ler gelir. H3 yalnız bir H2'nin altında açılır.

**Sabit bir başlık iskeleti yoktur** (kullanıcı kararı, 02.10.2026). Boyner giyimden kozmetiğe, ev
tekstilinden spor ekipmanına uzanır; mont için doğru olan iskelet parfüm, nevresim ya da koşu bandı için
doğru değildir. Her kategorinin başlıkları **o kategorinin araştırmasından** kurulur. Dört kaynak vardır ve
`scripts/baslik_adaylari.py` dördünü sahiplik süzgecinden geçirerek tek listede verir:

1. **İlk 5 rakibin başlıkları.** Üç ya da daha fazla rakipte geçen konu, Google'ın o sorguda beklediği
   kapsamdır ve iskelette karşılanır. Tek rakipte geçen iyi bir başlık fikir olarak alınabilir; başlık metni
   kopyalanmaz, konu alınır.
2. **PAA soruları** (kategori SERP'i ve bilgi niyetli SERP). Hacimli ve kategorinin özüne dokunan soru H2
   olur ("Parfüm Nasıl Seçilir?"); dar soru SSS'ye gider.
3. **SERBEST uzun kuyruk kümeleri.** Aynı niteleyeni paylaşan kelimeler (kışlık, kaz tüyü, su geçirmez;
   kuru cilt için, kalıcı; çift kişilik, pamuk saten) bir H2 ya da H3'ün konusudur. Küme hacmi başlığın
   önceliğini belirler.
4. **Kategorinin arama eğilimi.** Mevsimsellik, yükselen niteleyenler ve otomatik tamamlama önerileri;
   "insanlar bu kategoride en çok neyi soruyor" sorusunun cevabı.

Sayfanın canlı kırılımları (alt kategoriler, filtre adları) başlık kaynağı değil, başlıkların altını
dolduran malzemedir; ama filtre adları kategorinin hangi eksenlerde ayrıştığını gösterir (parfümde "koku
ailesi" ve "konsantrasyon", nevresimde "ölçü" ve "kumaş") ve çoğu zaman en doğru H2'leri işaret eder.

### İskeleti kurarken

- **Her başlığın bir dayanağı olur:** rakip kapsamı, PAA, kelime kümesi ya da arama eğilimi. Dayanağı
  olmayan başlık ("... ile Tarzınızı Yansıtın") açılmaz. Brief'te her H2'nin yanında dayanağı yazılır.
- **Başlık başka sayfanın kelimesi olamaz.** `baslik_adaylari.py` çıktısında `[SAHİPLİ]` işaretli aday
  başlık olmaz; o tür metinde bir kez, sahibine link veren anchor olarak geçer (bkz. bölüm 7). Rakipte
  "Kadın Şişme Mont Modelleri" başlığının olması, bizde de olacağı anlamına gelmez: rakibin ayrı sayfası
  yoktur, Boyner'in vardır.
- **Sıra okuyucunun karar yolunu izler:** önce "ne var / nedir", sonra "hangisi bana uyar", sonra "nasıl
  kullanırım / bakarım", sonda "nereden, hangi markadan". En çok aranan konu yukarıda durur.
- **Sayı kapsama göre:** uç kategoride 3-5, ana kategoride 5-8 H2. Bir H2'nin altı iki paragrafı
  dolduramıyorsa H3'e iner ya da SSS'ye gider.
- **Başlık, kullanıcının arama diliyle yazılır** (kullanıcı kararı, 02.10.2026). Ölçü: bu başlık Google'a
  yazılabilecek bir ifade mi? "Boy, Kalıp ve Beden" kimsenin aramadığı bir etikettir; "Kadın Montlarda Boy,
  Kalıp ve Beden Seçimi" aranabilir. "Dolgu ve Astar" yerine "Kaz Tüyü Mont ile Elyaf Dolgulu Mont Arasındaki
  Fark"; "Mont Bakımı ve Temizliği" yerine "Mont Nasıl Yıkanır?".
- **Ana kelime ya da ürün çekirdeği başlıkta geçer.** H2 ve H3'lerin çoğu kategori adını ("Kadın Mont") ya da
  ürün adını ("Mont") taşır; bağlamı başlıktan düşürülmüş genel etiketler ("Markalar", "Seçenekler")
  kullanılmaz. "Mevsime ve Kullanıma Göre Kadın Mont Modelleri", "Uzun, Kısa ve Kapüşonlu Kadın Mont
  Modelleri".
- **Biçim hacme göre seçilir.** Aynı konunun iki yazımı varsa hacmi yüksek olan başlığa çıkar: "modelleri"
  mi "çeşitleri" mi, "nasıl seçilir" mi "alırken nelere dikkat edilmeli" mi; kelime kümesi ve PAA karar
  verir. "... Modelleri" eki Türkçe kategori aramalarının en yaygın kalıbıdır ve H3'lerde de kullanılır.
- Başlık en fazla iki konu taşır (aynı eksenin değerleri tek konu sayılır: "Uzun, Kısa ve Kapüşonlu").
- **Ticari kelimeler karşılanır, rakam verilmez.** "{Kategori} Fiyatları" başlığı açılabilir ("fiyatları",
  "modelleri ve fiyatları" kategori aramalarının büyük kısmını oluşturur): altında fiyatı belirleyen etkenler,
  hangi türlerin ekonomik, hangilerinin üst fiyat grubunda olduğu ve sayfadaki fiyat filtresi anlatılır. Net
  fiyat, fiyat aralığı, indirim oranı ve kampanya yazılmaz.
- Kapanış H2'si ilk H2'nin eş anlamlısı olmaz; sayfadaki işlevi adlandırır (filtreleme, seçim, alışveriş).
- Kapanış bölümü ("Boyner'de {Kategori} Alışverişi") isteğe bağlıdır; söylenecek somut şey (filtreler,
  teyitli hizmet) varsa açılır, yoksa son bölümün sonuna iki cümlelik çağrı yeter.

## 4. Yapı taşı havuzu

Aşağıdaki bloklar **şablon değil havuzdur**: araştırma hangilerini destekliyorsa onlar, desteklediği sırayla
kullanılır; araştırmanın gösterdiği ama havuzda olmayan konu da başlık olur.

| Blok | Ne zaman açılır | Tipik biçim |
|---|---|---|
| {Kategori} Nedir? / Ne İşe Yarar? | Ürün herkesçe bilinmiyorsa, "nedir" sorgusu varsa (serum, softshell, espadril) | 2-3 cümlelik tanım |
| Çeşitleri / Modelleri | Kategorinin alt türleri varsa (hemen her kategoride) | tür başına tanım maddesi; alt kategori linkleri |
| Nasıl Seçilir? / Alırken Nelere Dikkat Edilmeli? | Seçim sorusu PAA'da ya da rakiplerde varsa | ölçüt H3'leri + karşılaştırma tablosu |
| İhtiyaç ekseni (mevsim, kullanım yeri, cilt tipi, yaş, ölçü, seviye) | SERBEST kümeleri bir eksende toplanıyorsa | eksen değerleri H3 |
| Malzeme / İçerik / Teknoloji | Kumaş, dolgu, aktif madde, taban teknolojisi aranıyorsa | karşılaştırma tablosu |
| Beden / Ölçü / Numara | Ölçü sorusu varsa (giyim, ayakkabı, nevresim, valiz) | marka-bağımsız ölçüt; tablo yalnız doğrulanabiliyorsa |
| Nasıl Kombinlenir? | Giyim, ayakkabı, çanta, aksesuar | tür başına eşleşme maddesi; tamamlayıcı kategori linki |
| Nasıl Kullanılır? / Nasıl Uygulanır? | Kozmetik, bakım, spor ekipmanı, ev aletleri | numaralı adımlar |
| Hangi Aktivitede / Nerede Kullanılır? | Spor, outdoor, valiz, çanta | aktiviteye göre tip tablosu |
| Fiyatları | Hemen her kategoride ("fiyatları" kelimesi aranıyorsa) | fiyatı belirleyen etkenler; rakam yok |
| Markaları | Kategoride birden çok marka varsa ve marka sorusu aranıyorsa | kullanım amacına göre gruplar; marka + kategori linkleri |
| Bakımı / Temizliği / Saklanması | Bakım sorusu varsa ve ürün bakım istiyorsa | numaralı adımlar |
| Hediye olarak / Özel gün | Hediye niyeti aranıyorsa (parfüm, saat, takı, cüzdan) | kısa bölüm |
| Boyner'de {Kategori} Alışverişi | Söylenecek somut şey varsa | filtreler, teyitli hizmet, çağrı |

Aileye göre seçim ölçütleri değişir; bunlar da araştırmayla teyit edilir:

| Aile | Sık çıkan eksenler ve ölçütler |
|---|---|
| Giyim | mevsim, kumaş ve dolgu, kalıp ve boy, beden, kombin, bakım |
| Ayakkabı | kullanım (günlük, koşu, yürüyüş), taban ve malzeme, numara ve kalıp, zemin |
| Çanta, aksesuar, saat, takı | kullanım, boyut/hacim, malzeme, mekanizma/kapama, hediye |
| Kozmetik, cilt ve saç bakımı, parfüm | cilt/saç tipi, içerik, form, uygulama sırası, kalıcılık, koku ailesi |
| Ev, tekstil, mutfak | ölçü, malzeme, kullanım alanı, set içeriği, yıkama |
| Spor, outdoor | branş, zemin/koşul, teknoloji, seviye, bakım |
| Elektronik | bağlantı ve uyumluluk, kullanım amacı, pil/şarj, koruma derecesi (IP), garanti, temizlik |
| Çocuk, bebek | yaş/beden, malzeme ve güvenlik, mevsim, pratiklik |

Kozmetikte sağlık iddiası kurulmaz ("lekeleri yok eder" değil; "leke görünümünü azaltmaya yardımcı
içerikler"). Çocuk ve bebek ürünlerinde güvenlik bilgisi kaynağa dayanmadan yazılmaz.

## 5. Uzunluk

Sınır yoktur; uzunluğu iki şey belirler:

1. **Rakip tabanı:** içerik taşıyan ilk 5 rakibin medyan kelime sayısı (`arastirma.py` çıktısı). Bunun altında
   kalmak için bir gerekçe olmalı.
2. **Kapsam:** HEDEF ve SERBEST kovasındaki kelime kümelerinin tamamı bir başlık, madde ya da SSS ile
   karşılanana kadar yazılır.

Pratikte uç kategori (ör. kadın peluş mont) 700-1.100, ana kategori (kadın mont) 1.200-2.000, üst kategori
(kadın dış giyim) 1.800 ve üzeri kelimeye çıkar; SSS buna dahil değildir. Uzunluk hedef değil sonuçtur:
**bilgi taşımayan paragraf uzunluk için eklenmez.** Her paragraf şu sorudan geçer: okuyucu bunu okuyunca
bir şey öğrendi mi ya da bir karar verdi mi?

Paragraf 3-4 cümleyi, 110 kelimeyi geçmez. Bir H2'nin altında 250 kelimeden fazla düz metin varsa H3'e ya da
listeye bölünür.

## 6. SEO, GEO ve AI Overview için yazım

Kategori sorgusunda ("kadın mont") Google çoğunlukla AI Overview göstermez; bilgi sorgusunda ("kadın mont
nasıl seçilir") gösterir. İçerik iki işi birlikte yapar: kategori kelimesinde sayfayı konu olarak
derinleştirir, bilgi sorgularında alıntılanabilir yanıt üretir.

- **Giriş tanımla açılır.** İlk cümle ana kelimeyi taşır ve kategorinin ne olduğunu söyler; 2-3 cümlede
  (40-60 kelime) kendi başına okunabilir bir tanım oluşur. Yapay zeka yanıtlarında alıntılanan şey bu bloktur.
- **Her H2'nin ilk cümlesi başlığın sorusunu doğrudan yanıtlar** (en fazla 30 kelime). Gerekçe ve ayrıntı
  sonra gelir. "Kadın mont seçerken üç şeye bakılır: kullanılacağı mevsim, dolgu malzemesi ve kalıp."
- **Bölüm kendi başına anlamlıdır.** "Yukarıda bahsedildiği gibi", "bu modeller" gibi öncesine yaslanan
  ifadeler yerine özne açık yazılır; AI motorları bölümü bağlamından koparıp alır.
- **Varlıklar adıyla geçer:** malzeme (kaz tüyü, polyester elyaf, softshell), kalıp (oversize, regular fit),
  marka, ürün tipi. "Çeşitli malzemeler" yazılmaz, malzemeler sayılır.
- **Karşılaştırma tabloyla, sayılabilir şeyler listeyle** verilir (bkz. bölüm 9). Liste ve tablo hem
  featured snippet hem AI Overview için en çok alınan biçimdir.
- **Tarihsel yıl ve yaygın standart serbesttir, kaynağıyla.** Marka kuruluş yılı, standart adı (IP68, EN ISO
  12312-1), yaygın ölçü (160x220 nevresim) kaynağı varsa yazılır; markaya göre değişen değer "çoğunlukla" ile
  verilir ya da yazılmaz. Yasak olan, güncel yıl ("2026 modası") ve kaynağı gösterilemeyen eşiktir.
- **Sayı doğrulanmadan yazılmaz.** "Kaz tüyü 800 dolgu gücünde", "-20 dereceye kadar korur" gibi değerler
  ancak kaynağı varsa (üretici, standart) yazılır. Ürün sayısı ("11.000 model") yazılmaz; yarın değişir.
- **Uzun kuyruk doğal cümlede geçer.** "Kışlık kadın mont" H3 olabilir; "kışlık mont bayan" gibi devrik
  arama ifadesi metne olduğu gibi yazılmaz, doğal sırasıyla ("kışlık kadın mont") karşılanır. "Bayan"
  kelimesi kullanılmaz; "kadın" yazılır.
- Ana kelime giriş, bir iki H2 ve kapanışta geçer; yoğunluk %3'ü geçmez (tek kelimelik ana kelimede ve marka
  sayfasında %4-5'e çıkabilir; başlık ve anchor'lar bunu doğal olarak yükseltir).
- Rakip kelime sayısı yanıltabilir: `arastirma.py` ürün kartı metinlerini de sayar. Medyana değil, rakibin
  gerçekten yazılmış metnine bakılır; ürün adı başlıkları (H3'te ürün listesi) konu başlığı sayılmaz. Çoğul, iyelik ve eş anlamlı
  biçimler ("montlar", "kadın mont modelleri", "dış giyim") tekrarın yerini alır.

## 7. Kelime sahipliği metne nasıl yansır

`sahiplik.py` her kelimeyi bir kovaya koyar. Metindeki karşılığı:

| Kova | Metinde |
|---|---|
| HEDEF | Giriş, H2'ler, kapanış. Sayfanın konusu. |
| SERBEST | H2/H3 başlığı, madde ya da SSS sorusu. Bu sayfanın uzun kuyruk trafiği buradan gelir. |
| BAŞKA SAYFA | Başlığa çıkmaz, SSS sorusu olmaz, ayrı paragraf almaz. Geçecekse **bir kez**, tanım cümlesi ya da madde içinde ve o sayfaya link veren anchor olarak geçer. |
| KAPSAM DIŞI | Yazılmaz. |

Örnek: "kadın şişme mont" kendi sayfasına sahipken kadın mont içeriğinde şöyle geçer:

> **Şişme mont:** Dolgulu kanalları sayesinde hafif kalırken ısıyı gövdede tutar; soğuk ve kuru havalar için
> [kadın şişme mont] modelleri öne çıkar.

Şöyle geçmez: "Kadın Şişme Mont Modelleri" başlığı altında üç paragraf ve "Şişme mont nasıl yıkanır?" SSS'si.
O içerik şişme mont sayfasına aittir; burada yazılırsa iki sayfa aynı sorguda yarışır ve ikisi de zayıflar.

Bir alt türün kendi sayfası **yoksa** (SERBEST) durum tersine döner: o tür bu sayfada H3 ile işlenir, çünkü
arayanı karşılayabilecek tek sayfa burasıdır.

## 8. İç link metnin içinden çıkar

Ayrıntı `ic-link-kurallari.md`'de. Yazarken akılda tutulacak üç şey:

- **Anchor'ı sil, cümle hâlâ anlamlı mı?** "Kadın kaban modellerine göz atabilirsiniz" link taşımak için
  kurulmuş cümledir. Doğrusu: "Diz altına inen, yün karışımlı modeller mont değil [kadın kaban] sınıfına girer."
- Anchor, hedef sayfanın ana kelimesidir; bu sayfanın ana kelimesi asla başka sayfaya anchor olmaz.
- Linkler bölümlere yayılır: tek paragrafta en fazla iki, tek H2'de en fazla dört.

## 9. Madde listesi, tablo ve kalın vurgu

**Madde listesi:** türler, ölçütler, adımlar gibi sayılabilir ve paralel şeyler paragrafa gömülmez. Biçim
`**Etiket:** tek ya da iki cümlelik tanım.` İlk cümle özneyi yeniden kurar ve bilgi ekler ("**Parka:** Parkalar
kalçayı örten boyu ve kapüşonuyla rüzgârlı havalarda gövdeyi korur."); etiket silindiğinde cümle anlamlı kalır. Liste öncesinde onu tanıtan bir cümle bulunur.
İki maddelik liste yapılmaz; sekizi geçen liste bölünür. Numaralı liste yalnız sıralı adımlar içindir
(uygulama adımları, yıkama sırası).

**Tablo:** iki ya da daha fazla şey birden çok ölçütte karşılaştırılıyorsa. En fazla dört sütun (mobilde
okunmalı), 3-7 satır. Tipik tablolar: "kullanıma göre hangi tip", "malzeme karşılaştırması", "beden/ölçü".
Tablo hücresinde link en fazla bir sütunda bulunur. Beden tablosu ancak marka-bağımsız ve doğrulanabilir
ise verilir; markaya göre değişen ölçü tablosu uydurulmaz, "ürün sayfasındaki beden tablosu" işaret edilir.

**Asgari yapı öğeleri.** Her kategori içeriğinde şunlar bulunur (değerlendirmede 90 üstünü ayıran öğeler):

- İhtiyaca göre tür tablosu **ve** okuyucunun en sık ikilemde kaldığı iki seçeneği karşılaştıran nitel bir
  tablo (kaz tüyü / elyaf dolgu; mat / parlak bitiş; pamuk saten / ranforce). Hücreler sayı değil nitelik
  taşır ("daha hafif", "ıslandığında azalır").
- Seçim ölçütleri cümle içinde sayılmaz; **numaralı karar adımları** olarak verilir (her adım tek cümle).
- Ürün sayfasında hangi bilginin nerede olduğu (materyal, beden tablosu, içerik listesi) bir cümleyle
  söylenir; okuyucu etiketi ve ürün sayfasını okumayı öğrenir.
- Filtre adları dışında **doğrulanmış bir mağaza bilgisi**, teyit edilebiliyorsa (bkz. bölüm 10, kapanış).
  Zorunlu değildir: teyit edilemeyen hizmet cümlesi yazılmaz.
- Karşılaştırma tablosunun konusu gamda olmalıdır (pamuk saten / ranforce tablosu, ranforce satılmıyorsa
  yazılmaz). Tablo sütun adında sahipli bir kelimenin geçmesi ("Kablosuz") serbesttir; başlık ve SSS olamaz.

**Kalın vurgu:** bölüm başına iki üç yerde, okuyucunun aradığı net bilgi için (malzeme adı, ölçüt, karar
cümlesi). Tam cümle, bölümün ilk kelimeleri ve başlıkta geçen ifade kalın yazılmaz.

## 10. Bölüm bölüm ne yazılır

**Yazmadan önce canlı kayıt okunur** (`kategori.py`): alt kategoriler, markalar, filtre değerleri (ürün
çeşidi, kalıp, materyal, renk...) ve örnek ürün adları metnin gerçeklik zeminidir. **İçerik mevcut ürün
gamını anlatır** (kullanıcı kararı, 02.10.2026): sayfada filtrelenemeyen bir tür, sitede satılmayan bir marka,
seri ya da malzeme yazılmaz; gamda ağırlığı olan türler ve markalar metinde de öne alınır, tek tük ürünü
olan tür bir cümleyle geçer. Gam darsa içerik de dar tutulur; rakipte var diye sayfada olmayan konu açılmaz. Taslak bittikten sonra aynı kayıt bir kez daha okunur: "sayfada olup içerikte
olmayan ne var?"

**Giriş (başlıksız).** Birinci paragraf: kategori nedir, hangi ihtiyacı karşılar (tanım; ana kelime ilk
cümlede). İkinci paragraf: Boyner'deki gam; hangi türler, hangi kalıp ve malzemeler, hangi markalar
(üç dört somut ad). Üst kategori linkinin doğal yeri burasıdır. "Günümüzde...", "Moda dünyasında..." gibi
açılışlar yazılmaz.

Aşağıdakiler havuzdaki blokların nasıl yazılacağını anlatır; iskelette olmayan blok yazılmaz.

**Çeşitleri / Modelleri.** İlk cümle türleri sayar. Ardından madde listesi: her tür bir tanım cümlesi alır.
Kendi sayfası olan türler anchor ile, olmayanlar düz metinle geçer. Alt kategori linklerinin (2-4) evi
burasıdır.

**Nasıl Seçilir?** İlk cümle ölçütleri sayar; her ölçüt bir H3 ya da madde. Karşılaştırma tablosunun doğal
yeri ve sayfanın bilgi sorgularında alıntılanan bölümü.

**İhtiyaç ekseni.** SERBEST kümeleri burada H3 olur ("Kışlık Kadın Mont", "Kuru Ciltler İçin Fondöten",
"Çift Kişilik Nevresim Takımı"). Her H3 o ihtiyaç için hangi özelliğe bakılacağını söyler; yalnız
"seçenekler Boyner'de" demek için H3 açılmaz. H2 eksene göre adlandırılır.

**Malzeme / İçerik / Teknoloji.** Malzemeler adıyla ve farkıyla anlatılır; iki üç seçenek varsa tablo.
Sayısal değer yalnız kaynakla.

**Nasıl Kombinlenir? / Kullanılır? / Uygulanır?** Somut eşleşme ya da adım. Tamamlayıcı kategori linkleri
(1-2) burada. Genel nasihat yazılmaz.

**Markaları.** İlk cümle markaları ya da grupları sayar. Her marka neyle ayrıştığını bir cümleyle alır;
bilgi markanın kendi tanımına ya da sayfadaki ürün gamına dayanır. Marka + kategori sayfası olanlardan
1-2'sine link verilir. Yalnız Boyner'de o kategoride ürünü olan markalar yazılır.

**Bakımı / Temizliği.** Malzemeye göre kısa yönerge; numaralı adım olabilir. "Etiketteki talimat esastır"
bir kez geçer. Alt türe özgü bakım, o türün kendi sayfası varsa burada ayrıntılanmaz.

**Boyner'de {Kategori} Alışverişi.** Sayfadaki filtrelerle seçimin nasıl daraltılacağı ve teyitli Boyner
hizmetleri. Hizmet bilgisi (Boyner Now, mağazadan teslim, iade) yalnız `boyner.com.tr/content/...`
sayfasından teyit edilerek ve süre/koşul rakamı verilmeden yazılır. Teyitli örnek (02.10.2026,
`/content/boyner-now`): Boyner Now ile ürünler teslimat adresinde denenip beğenilenler satın alınabiliyor.
Bu hizmet giyim ve ayakkabıda anılır; kozmetik, elektronik ve ev tekstilinde
geçerliliği teyit edilmeden yazılmaz. Diğer teyit kaynakları: canlı kayıttaki seçenek filtreleri (Kargo
Bedava, Yarın Kargoda), fiyat filtresi ve sıralama (`kategori.py` "Fiyat filtresi: var" diyorsa), ürün
sayfasındaki alanlar (elektronikte "Garanti Süresi"). "Ürün sayfasındaki beden tablosu" her üründe teyit
edilemedi; "markanın beden bilgisi" ya da "ürün sayfasındaki beden bilgisi" yazılır.
Satıcıya göre değişen koşullar (iade süresi, mağazadan iade) genelleme olarak yazılmaz. Fiyat, indirim oranı,
kampanya adı ve tarihi yazılmaz. Bir iki cümlelik çağrıyla biter.

## 11. SSS yanıtları

- 6-10 soru. Kaynak: PAA, bilgi niyetli SERP'in PAA'sı, otomatik tamamlama önerileri ve SERBEST kovasındaki
  soru kalıpları. Soru uydurulmaz.
- Gövdede bir H2 ile zaten yanıtlanan soru SSS'de tekrarlanmaz; SSS gövdenin giremediği uzun kuyruğu toplar.
- Başka sayfanın kelimesini taşıyan soru alınmaz ("şişme mont nasıl yıkanır" şişme mont sayfasınındır).
- Yanıt 30-70 kelime (en fazla 80). İlk cümle doğrudan yanıt: evet/hayır ya da net bilgi. Gerekçe ikinci
  cümlede.
- Yanıt kendi başına okunur, gövdeye gönderme yapmaz, kategori adını bir kez tam haliyle taşır.
- Soru kullanıcının arama diliyle ama düzgün Türkçeyle yazılır: "kadın mont beden" değil "Kadın mont bedeni
  nasıl seçilir?".
- Fiyat sorusu rakamla yanıtlanmaz; fiyatı belirleyen etkenlerle (dolgu, marka, uzunluk) yanıtlanır. Gövdede
  "Fiyatları" başlığı varsa SSS'de tekrarlanmaz.

## 12. Cümle kurgusu

- **Özne ile yüklem uyuşur; yüklemin işi öznenin yapabileceği bir iştir.** "Kısa montlar araç kullanırken
  rahat eder" cümlesinde rahat eden mont değil, giyen kişidir: "kısa montlar hareketi kısıtlamaz". Her cümle
  "kim / ne yapıyor" diye okunur.
- Yan cümlede özne açık olur; bilgi doğru özneye bağlanır (montu sıcak tutan dolgu ve astardır, renk değil).
- **Ana kelime cümle içinde çekimlenir.** Arama ifadesi "kadın mont"tur ama Türkçe cümlede özne "kadın
  montu / kadın montları" olur. Yalın biçim başlıklarda ve "kadın mont modelleri" gibi zincirlerde kalır;
  cümle öznesi olarak "Kadın mont, ... korur" yazılmaz.
- **Tanımlar metin boyunca tutarlı kalır.** Bir yerde "bel ile kalça arasında biter" denen ürün başka yerde
  "diz üstüne iner" diye tanımlanmaz; sayı verilen sayım ("üç ölçüt", "yedi tür") listeyle birebir tutar.
- İki ayrı iş tek yükleme bağlanmaz: "rüzgârı keser ve ıslandığında silinerek temizlenir" yerine "rüzgârı
  keser, yüzeyi su emmez; lekeler nemli bezle silinir".
- Aynı cümlede aynı kök iki kez geçmez; art arda iki cümle aynı kalıpla açılmaz.
- Olumsuzla koşul kurulmaz: "çok dar olmayan" yerine "omuzdan bir parmak boşluk bırakan".
- Mecaz yerine düz anlatım: "soğuğa meydan okuyan" değil "astarlı ve rüzgâr geçirmeyen".
- "Hem ... hem de", "sadece ... değil aynı zamanda" kalıpları sayfada en fazla bir kez.
- Üçlü sıfat dizisi ("şık, rahat ve fonksiyonel") yazılmaz; bir özellik seçilip açıklanır.

### Tutarlılık kuralları (değerlendirmelerde tekrar eden kusurlardan)

Kadın Mont içeriği üç tur bağımsız değerlendirmeden geçti (74 → 86 → 89/100; aynı sürüme ikinci bir
değerlendirici 84 verdi). Turlar boyunca tekrar eden
kusurlar bilgi eksikliği değil tutarsızlıktı; aşağıdakiler her içerikte kontrol edilir:

- **Tek tanım.** Ürünün boyu, malzemesi ve komşu kategoriden farkı bir kez tanımlanır; giriş, gövde, tablo
  ve SSS aynı ölçülerle konuşur. Teslimden önce her ölçü ifadesi ("diz üstü", "bel ile kalça arası") metin
  genelinde taranır.
- **Gövde ile SSS çelişmez.** Aynı soruya iki yerde iki ayrı yanıt verilmez; aynı tavsiye en fazla bir kez
  gövdede, bir kez SSS'de geçer.
- **Genel adım, özel istisna.** Numaralı adımlar yalnız tüm ürün türleri için geçerli işlemleri içerir; türe
  göre değişen talimat ayrı maddelerde verilir ve hiçbir genel adım bir tür maddesiyle çelişmez ("montu
  yıkayın" adımı ile "suni deri yıkanmaz" maddesi).
- **Geniş genelleme testi.** "X'ler Y olur" kalıbındaki her cümle metnin kendi anlattığı türlerle sınanır
  ("kışlık montlar uzun olur" genellemesi "kısa şişme mont" ile çelişir). Tür sayısı kesin sınıflama gibi
  sunulmaz ("başlıca ... tür").
- **Dayanaksız üstünlük ve kesinlik yok.** "En sık", "en çok", "her zaman", "yıllarca" veriyle
  desteklenmiyorsa "çoğunlukla", "öne çıkan", "... biri", "birkaç sezon" biçimine çevrilir.
- **Tablo ve gövde aynı sözlüğü kullanır.** Tabloda geçen her tür ve özellik gövdede tanımlıdır; aynı parça
  için iki ad kullanılmaz ("kar eteği" / "etek bandı").
- **Kendi başına okunur madde.** Kalın etiketli maddede ilk cümle özneyi yeniden kurar (yalnız ilk cümle;
  sonraki cümlelerde ve anchor'da aynı kelime üçüncü kez tekrarlanmaz, zamir ya da "bu modeller" yeter): "**Suni deri mont:**
  Suni deri montlar rüzgârı keser..." Etiket silindiğinde cümle anlamını korumalıdır; AI motorları cümleyi
  etiketsiz alıntılar.
- **Başlık sorusuna ilk cümlede yanıt, sorulan birimle.** "Hangi aylarda" sorusunun yanıtı ay adı, "hangisi"
  sorusunun yanıtı tür adı içerir. Paragrafta başlığın sorusuyla ilgisiz cümle bulunmaz.
- **Anchor cümleye oturur.** Anchor yerine yazıldığında cümle dil bilgisi açısından doğru okunmalı ("bir
  [kadın bot] ile" değil "[kadın bot] modelleriyle"); küçük harfli anchor cümle başına gelmez.
- **Açılış ve bitiş çeşitliliği.** Ardışık bölümler aynı kalıpla (ana kelime + "modellerinde") açılmaz;
  ardışık iki madde aynı yüklemle bitmez; aynı kök bir bölümde üçten fazla, aynı niteleyici ("uygun")
  metinde bir düzineden fazla tekrarlanmaz.
- **Marka nitelemesi doğrulanır.** "... ile tanınır", "... için öne çıkar" markanın bilinen ürün çizgisi ve
  canlı kategori listesiyle teyit edilir; teyit edilemiyorsa yalnız varlık bildirilir ("kategoride ...
  montlarıyla yer alıyor").
- **Tanım her alt tür için doğru kalır.** "X ile Y farkı" ayrımı metindeki bütün alt türlerle sınanır ("montu
  kabandan ayıran dolgudur" cümlesi dolgusuz mevsimlik montla çelişir); bir tür başka bir türün alt kümesiyse
  (kaz tüyü, şişmenin dolgu türüdür) ekseni açıkça söylenir.
- **H2 vaadini tutar.** Bir H2 altındaki her H3 o H2'nin eksenine girer; H2'nin giriş cümlesi alt başlıkların
  tümünü sayar.
- **Tek yerde anlatım.** Bir özellik (boy, kapüşon, beden tablosu) bir bölümde açıklanır; diğer bölümlerde
  yalnız o bölüme özgü sonucu yazılır.
- **Terim tekliği.** Aynı kavram için tek terim (elyaf / sentetik, bantlı / bantlanmış, kapitone /
  kapitoneli).
- **Girişte sayılan gövdede işlenir;** giriş, kombin ve kapanıştaki listeler (tür, renk, filtre) aynı kümeyi
  kullanır.
- **Sayfa işlevi teyitli adıyla ve fiili işleviyle anılır:** filtre adı canlı kayıttaki gibi yazılır
  ("Peluş/Kürk"), filtre "daraltır", sıralama "üste alır".
- **Ürün, sayfanın kategori adıyla anılır** (mont sayfasında "ceket" yazılmaz).
- **Nedensellik sınanır.** "-dığı için", "çünkü", "sağlar" ile kurulan her bağ cümledeki özellikten doğrudan
  çıkmalıdır; çıkmıyorsa bağ kaldırılır.
- **Sayı taraması.** Teslimden önce metindeki her rakam aranır (`icerik_denetim.py` listeler); kaynağı
  gösterilemeyen eşik "etikette belirtilen" gibi rakamsız ifadeye çevrilir.
- **Düzeltme sonrası yeniden tarama.** Bir cümle düzeltildiğinde aynı kalıp ve aynı konu (bakım, beden, boy)
  metnin tamamında yeniden taranır; düzeltme yeni bir çelişki doğurmamalıdır.

## 13. Yazarken kaçınılacaklar

- Net fiyat, fiyat aralığı, indirim oranı, kampanya adı ve tarihi ("uygun", "ekonomik" gibi niteleyiciler
  serbesttir); yıl ("2026 modası"), "bu sezon", "yeni sezon trendi" gibi
  zamanla eskiyen ifadeler. Sayfa bir yıl sonra da düzeltme istemeden doğru kalmalı.
- Rakip perakendeci adı. Boyner'de satılmayan marka.
- Sitede karşılığı olmayan tür, renk, malzeme (canlı kayıtla teyit edilmeden yazılan her ürün bilgisi).
- "En iyi", "en kaliteli", "1 numara" gibi dayanağı olmayan üstünlük iddiası. "En çok tercih edilen" de
  veriye dayanmıyorsa yazılmaz.
- "Bayan" kelimesi; "kadın" kullanılır.
- Link taşımak için kurulan cümle ("...modellerine göz atabilirsiniz", "...sayfamızı inceleyebilirsiniz").
- Kaynak notu, künye, kelime sayısı gibi iç bilgiler belgeye basılmaz; sohbette söylenir.
- Uzun tire, emoji, marka sembolü (® ™), çift boşluk.
