# Kelime sahipliği ve cannibalization

Boyner'de 34 binin üzerinde indekslenebilir listeleme sayfası var. Aynı ürün ailesi için şu sayfa tipleri
ayrı ayrı yayında:

| Tip | Örnek | Adet (02.10.2026) |
|---|---|---|
| kategori | `/mont-x-c1531` | ~2.500 |
| cinsiyet + kategori | `/kadin-mont-x-g3731-c23896554` | ~2.150 |
| marka | `/columbia-x-b596` | ~2.900 |
| marka + cinsiyet | `/adidas-kadin-x-b3-g3731` | ~2.350 |
| marka + cinsiyet + kategori | `/columbia-kadin-mont-x-b596-g3731-c23896554` | ~19.400 |
| kategori + filtre | `/ruj-x-c12037604?renk=nude` | ~100 |
| arama sayfası | `/search?q=beyaz+çanta` | ~4.600 |

Bir kategori içeriği bu sayfalardan herhangi birinin kelimesine oynarsa iki Boyner sayfası aynı sorguda
yarışır. Bu yüzden içerik yazılmadan önce **her kelimenin sahibi belirlenir** ve içerik yalnız kendi
kelimelerini hedefler.

## Adım 1 - Doğru hedef URL

Boyner'de aynı ada sahip birden fazla kategori kimliği bulunur. "Kadın mont" için envanterde
`/kadin-mont-x-g3731-c1531` (çocuk ağacında, 13 ürün), `/kadin-mont-x-g3731-c200102` ve
`/kadin-mont-x-g3731-c23896554` (Google'da sıralanan, ana ağaçtaki sayfa) vardır. Yanlış kimliğe yazılan
içerik boşa gider.

**Önce Google ve GSC'ye bakılır, sonra envantere.** Sitemap ana ağaçtaki sayfaların bir kısmını taşımaz (erkek
gömlek `c23896609`, kadın şişme mont `c23896555` sitemap'te yoktur) ve cinsiyetsiz marka + kategori sayfalarını
hiç içermez. Envanterde aday çıkması doğru sayfanın orada olduğunu göstermez; sıralanan adres envanterde yoksa
üst kategorinin canlı kaydındaki (`kategori.py`) alt kategori adresi kullanılır.

Hedef şu dört sinyalle teyit edilir; dördü aynı sayfayı göstermeli:

1. `envanter.py sahip "{ana kelime}"` - adaylar
2. `kategori.py {aday}` - ürün sayısı en yüksek, breadcrumb doğru ağaçta, canonical kendisi, index açık
3. `arastirma.py` SERP çıktısı - Google'da ana kelimede sıralanan Boyner URL'si
4. GSC - ana kelimede en çok tıklama alan sayfa (`get_advanced_search_analytics`, `dimensions: "page"`,
   `filter_dimension: "query"`, `filter_operator: "equals"`)

Sinyaller ayrışıyorsa (Google bir kimliği, menü başka kimliği gösteriyor) içerik yazılmaz; durum kullanıcıya
iki URL ve verileriyle bildirilir. Bu site düzeyinde bir çakışmadır, içerikle çözülmez.

Ayrışmanın üç sık biçimi ve yapılacak olan:

| Ayrışma | Yapılacak |
|---|---|
| Ana kelimede **blog yazısı** (`/mag/...`) ya da **marka içerik sayfası** (`/content/{marka}`) sıralanıyor | İçerik yazılır; çakışma teslim notunda GSC verisiyle bildirilir. Blog ve içerik sayfaları **zayıf sahiptir** (aşağıda). `/content/{marka}` görselli kampanya / karosel sayfasıdır, listeleme değildir: marka sorgusunun esas sayfası her zaman marka listeleme sayfasıdır (`/{marka}-x-b...`; kullanıcı kararı, 02.10.2026) |
| Cinsiyetli sayfa ile **cinsiyetsiz çatı sayfa** aynı sorguda dönüşümlü sıralanıyor (`/erkek-gomlek` ve `/gomlek`) | Cinsiyetli kelimenin içeriği cinsiyetli sayfaya yazılır ("erkek gömlek" -> `/erkek-gomlek`); cinsiyetsiz kelimenin içeriği ayrıca, cinsiyetsiz çatı sayfaya yazılır ("gömlek" -> `/gomlek`). Bkz. aşağıda "Cinsiyetli ve cinsiyetsiz sayfa ailesi" |
| **Eş sesli kategori**: aynı ad iki farklı ürünü karşılıyor (kulaklık: elektronik ve kışlık aksesuar) | Breadcrumb ve ürünlere bakılır; kullanıcının kastettiği ağaçtaki sayfa seçilir, öteki not edilir |

**Cinsiyet + kategori sayfasının canonical'ı kategori sayfasını gösterebilir** (`/kadin-elbise-x-g3731-c23896624`
-> `/elbise-x-c23896624`). Bu durumda içerik canonical adrese yazılır ve kullanıcıya not düşülür.

## Adım 2 - Dört kova

`sahiplik.py` araştırmadaki her kelimeyi şu kovalardan birine koyar:

- **HEDEF:** kök kümesi hedefin kök kümesine eşit ("kadın mont", "mont kadın", "kadın mont modelleri",
  "bayan mont").
- **BAŞKA SAYFA:** kelimenin kök kümesiyle birebir eşleşen başka bir sayfa var, ya da Google o kelimede
  başka bir Boyner sayfasını ilk 20'de sıralıyor.
- **SERBEST:** hedefin ürün çekirdeğini taşıyan, kendi sayfası olmayan uzun kuyruk ("kışlık kadın mont",
  "su geçirmez kadın mont", "kadın mont beden tablosu").
- **KAPSAM DIŞI:** Boyner'de satılmayan marka/perakendeci, başka cinsiyet, başka ürün çekirdeği.

Kök kümesi nedir: kelime ASCII'ye katlanır, dolgu ekleri ("modelleri", "fiyatları", "çeşitleri") atılır,
çoğul ve iyelik ekleri kırpılır, "bayan" -> "kadın" eşlenir. "Kadın Mont Modelleri ve Fiyatları" ile
"mont kadın" aynı kümedir: {kadin, mont}.

Sahip belirlenirken öncelik sırası: (1) hedef sayfanın canlı kaydındaki alt kategori ve marka kırılımı
(`--kayit`), (2) Google'da o kelimede ilk 20'de sıralanan Boyner sayfası, (3) envanterde kök kümesi eşleşen
sayfa. Sitemap eski kategori kimliklerini de taşır: "kadın şişme mont" için envanterde beş aday vardır ama
ana ağaçtaki sayfa (`c23896555`) sitemap'te bulunmaz, yalnız canlı kayıtta görünür.

## Adım 3 - Kovaları elle gözden geçir

Betik kelime biçimine bakar, niyete bakamaz. Tablonun üzerinden bir kez geçilir:

- **SERBEST'teki marka kelimeleri:** betik envanterde marka sayfası olan markaları tanır; olmayanları tanıyamaz ("moncler kadın mont", "lacoste kadın
  mont"). Marka Boyner'de satılıyorsa (`envanter.py ara "{marka}"`) sahibi marka sayfasıdır -> BAŞKA SAYFA.
  Satılmıyorsa KAPSAM DIŞI.
- **SERBEST'teki renk kelimeleri:** "siyah kadın mont" için arama sayfası (`/search?q=...`) ya da renk
  filtresi sayfası var mı bakılır. Varsa BAŞKA SAYFA; yoksa metinde renk bir cümlede anılır, H3 açılmaz
  (renk başına bölüm içeriği şişirir, bilgi katmaz).
- **BAŞKA SAYFA'da "N aday sayfa" notu:** aynı ada sahip birden çok kimlik var demektir. `--teyit` ile ya da
  elle `kategori.py` çalıştırılarak ürünü olan, canonical'ı kendisi olan kimlik seçilir.
- **Eş anlamlı sahipler:** "kadın kaban" ile "kadın mont" ayrı sayfalardır ve ayrı kalır; ama "kadın mont
  kaban" sorgusunda Google kaban sayfasını sıralıyorsa bu kelime kabanındır.
- **Arama sayfasına sahip kelime:** `/search?q=kaz+tüyü+mont` sıralanıyorsa kelimenin sahibi odur. Arama
  sayfaları zayıf sahiplerdir (içerik taşımaz); yine de aynı kelimeye H2 açılmaz. Metinde tanım cümlesi içinde
  bir kez geçer. Link verilip verilmeyeceği `ic-link-kurallari.md`'de.

## Adım 4 - GSC ile çapraz kontrol

SERP haritası tek gün ve tek konum içindir; GSC 3 aylık gerçeği gösterir. İki sorgu yeter:

1. **Hedef sayfa hangi sorgulardan gösterim alıyor?** `get_search_by_page_query` (site
   `sc-domain:boyner.com.tr`, 90 gün). Pozisyonu 5-20 arasında, gösterimi yüksek sorgular içeriğin ilk
   karşılaması gereken kelimelerdir; SERBEST kovasına eklenir.
2. **Ana kelimeyi taşıyan sorgularda hangi sayfalar gösterim alıyor?** `get_advanced_search_analytics`,
   `dimensions: "query,page"`, `filter_dimension: "query"`, `filter_operator: "contains"`,
   `filter_expression: "{ana kelime}"`. Aynı sorguda iki farklı Boyner sayfası kayda değer gösterim
   alıyorsa mevcut çakışmadır: brief'in DİKKAT satırına ve teslim notuna yazılır.

GSC'ye erişilemiyorsa bu adım atlanır ve atlandığı kullanıcıya söylenir; SERP haritası tek başına kullanılır.

## Sahiplik metne nasıl yansır

| | HEDEF | SERBEST | BAŞKA SAYFA | KAPSAM DIŞI |
|---|---|---|---|---|
| Giriş, kapanış | evet | doğal geçerse | hayır | hayır |
| H2 / H3 | evet | evet | **hayır** | hayır |
| Madde, tanım cümlesi | evet | evet | bir kez, anchor olarak | hayır |
| SSS sorusu | evet | evet | **hayır** | hayır |
| Anchor metni (başka sayfaya) | **hayır** | hayır | evet (sahibine) | hayır |
| Brief sütunu | Main KW / İkincil | İkincil ve Uzun Kuyruk | Kapsam Dışı Kelimeler | yazılmaz |

`icerik_denetim.py --sahiplik` başlıkları, SSS sorularını ve anchor'ları bu tabloyla karşılaştırır.

## Zayıf sahipler ve sınır durumlar

- **Blog (`/mag/`) ve içerik (`/content/`) sayfaları zayıf sahiptir.** Bilgi niyetli kelimeyi ("fondöten nedir",
  "en iyi fondöten") alabilirler, ama kategori niyetli kelimeyi ("fondöten markaları", "fondöten çeşitleri")
  kategori sayfasından alamazlar: kategori sayfası bu başlıkları açabilir. "En iyi ..." listesi blogundur,
  kategori içeriğinde açılmaz. Bu sayfalara link verilmez (kullanıcı isterse istisna).
- **Arama sayfası (`/search?q=`) sahibi olan alt tür** (keten gömlek, oduncu gömlek; kullanıcı kararı,
  02.10.2026): kendi H3'ünü alabilir, ama arama sayfasıyla yarışmayacak ölçüde: tek paragraf (60-100 kelime),
  türü tanımlar ve hangi ihtiyaca uyduğunu söyler; renk, kalıp, kombin gibi alt kırılımlara inmez. Paragrafın
  bir cümlesinde arama sayfasına link verilir (anchor: aramanın kendisi, "keten gömlek"). Aynı türün ayrıca
  çeşitler listesinde maddesi olmaz. Arama sayfası renk sorgusunun sahibiyse ("siyah kadın mont") başlık
  açılmaz; renk girişte ve kombin bölümünde tek cümleyle geçer.
- **Sahibi 8 üründen az olan kelime** (oyuncu kulaklığı: 7 ürün): başlık açılmaz, link de verilmez; düz metinle
  bir kez geçer.
- **Cinsiyetli ve cinsiyetsiz sayfa ailesi.** Giyim, ayakkabı ve aksesuarda aynı ürünün çoğu zaman cinsiyetsiz
  (`/gomlek`), kadın (`/kadin-gomlek`), erkek (`/erkek-gomlek`) ve çocuk sürümleri vardır. Her sürüm kendi
  kelimesini hedefler: cinsiyetli sayfa cinsiyetli kelimeyi (başlıklar ve madde etiketleri cinsiyeti taşır),
  cinsiyetsiz sayfa cinsiyetsiz kelimeyi ve ürünün genel bilgisini ("gömlek nedir", "gömlek nasıl ütülenir").
  Cinsiyetli içerikte cinsiyetsiz bilgi anlatılabilir ama başlığa çıkmaz; ileride cinsiyetsiz sayfaya içerik
  yazılırsa aynı bilgi oraya genel biçimiyle girer. İki sürüm birbirine link verebilir (cinsiyetsiz sayfa
  cinsiyetli sürümlere, cinsiyetli sayfa üst ağaca).
- **Cinsiyetsiz bilgi sorusu** ("sneaker ne demek", "sneaker nasıl temizlenir"): doğal sahibi cinsiyetsiz çatı
  sayfadır. Çatı sayfada içerik yoksa ve yazılması planlanmıyorsa cinsiyetli sayfada karşılanabilir; brief'in
  DİKKAT satırına "çatı sayfaya içerik yazılırsa taşınır" notu düşülür.
- **Kardeş kategori:** "tek kişilik nevresim takımı" kelimesinin sahibi `/tek-kisilik-nevresim` sayfasıdır;
  betik "takım" kelimesi yüzünden eşleştiremez. Hedefin breadcrumb'ındaki üst kategorinin alt kategorileri
  elle sahip adayı olarak gözden geçirilir.
- **Alt marka:** bir markanın alt çizgisi ayrı marka sayfasına sahipse (Calvin Klein Jeans `b559`), o çizginin
  kelimeleri ("calvin klein jeans", "calvin klein jean") alt marka sayfasınındır.
- **Marka kelimesi:** kelime Boyner'de sayfası olan bir markanın adını taşıyorsa betik sahibi marka tarafına
  verir. Canlı kırılımdaki adres ile Google'da sıralanan adres farklıysa **Google'da sıralanan adres** sahip ve
  link hedefi sayılır; ikisi de teslim notunda yazılır. (Kesin tercih kullanıcı kararını bekliyor, 02.10.2026.)

## İçerikle çözülmeyenler

Şunlar içerik işi değildir; fark edilirse yazılmaz, kullanıcıya bildirilir:

- Aynı ada sahip iki kategori kimliğinin ikisinin de indekste olması
- Cinsiyet + kategori sayfası ile kategori sayfasının aynı sorguda dönüşümlü sıralanması
- Arama sayfasının (`/search?q=`) kategori sayfasının önünde sıralanması
- Hedef sayfanın canonical'ının başka sayfayı göstermesi ya da noindex olması
