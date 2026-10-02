# Marka sayfası içeriği

Marka sayfaları (`/skechers-x-b545`) kategori sayfalarıyla aynı akıştan geçer; farklar aşağıda. Bu dosya yalnız
hedef bir marka sayfasıysa okunur.

## Hedef ve kelime

- **Ana kelime marka adıdır** ("skechers"). Marka sorgusu çoğu zaman gezinme niyetlidir ve markanın kendi
  sitesi ilk sıradadır; Boyner sayfasının işi "skechers + ürün" ve "skechers modelleri" sorgularında ve
  marka hakkındaki bilgi sorgularında görünmektir.
- `arastirma.py` marka adıyla çalıştırılır; ek tohum olarak "{marka} modelleri" ve markanın Boyner'deki en
  büyük ürün ailesi ("skechers ayakkabı") verilir (`--ek`).
- SERP'te markanın kendi sitesi, pazar yerleri ve Wikipedia bulunur; rakip içerik olarak **diğer
  perakendecilerin marka sayfaları** okunur, markanın kendi sitesi başlık kaynağı değil bilgi kaynağıdır.

## Kelime sahipliği

Marka sayfasının çevresi kalabalıktır: marka + cinsiyet (`/skechers-kadin-x-b545-g3731`), marka + kategori
ve marka + cinsiyet + kategori (`/skechers-kadin-sneaker-x-b545-g3731-c...`) sayfaları ayrı ayrı yayındadır.

| Kelime | Sahibi | Bu içerikte |
|---|---|---|
| skechers, skechers modelleri, skechers türkiye | marka sayfası | HEDEF |
| skechers kadın, skechers erkek, skechers çocuk | marka + cinsiyet sayfası | başlık olmaz; bir kez, link olarak |
| skechers ayakkabı, skechers bot, skechers terlik | marka + kategori sayfası (varsa) | başlık olmaz; ürün aileleri listesinde link olarak |
| skechers kadın yürüyüş ayakkabısı | marka + cinsiyet + kategori sayfası | başlık olmaz; link olarak ya da hiç |
| skechers memory foam, skechers go walk, skechers arch fit (seri ve teknoloji adları) | çoğu zaman sahipsiz ya da arama sayfası | SERBEST: seri/teknoloji bölümünde karşılanır |
| skechers hangi ülkenin, skechers orijinal nasıl anlaşılır, skechers kalıbı dar mı | sahipsiz | SERBEST: H2/H3 ya da SSS |

`sahiplik.py --kayit` marka sayfasının canlı kategori kırılımlarını sahip olarak öne alır. Marka + kategori
sayfası olmayan ürün ailesi (SERBEST) gövdede bir paragraf alabilir.

## İçerik

- **Giriş:** marka kimdir (kuruluş yeri ve yılı, neyle bilinir; kaynak: markanın kendi kurumsal sayfası) ve
  Boyner'de hangi ürün aileleri bulunur (canlı kayıttaki kategoriler).
- **Yapı taşları** (araştırma hangilerini destekliyorsa):

| Blok | İçerik |
|---|---|
| {Marka} Modelleri / Ürünleri | Boyner'deki ürün aileleri; marka + kategori ve marka + cinsiyet linkleri burada |
| {Marka} Serileri / Teknolojileri | Markanın kendi adlandırdığı seriler ve teknolojiler; her biri ne işe yarar (kaynak: marka) |
| {Marka} Kalıp ve Numara / Beden | "kalıbı dar mı", "numara büyük mü alınır" aramaları; markanın kendi beden rehberine dayanır |
| {Marka} Kimler İçin / Hangi Kullanım | yürüyüş, koşu, günlük, iş; ürün ailesiyle eşleştirilir |
| {Marka} Orijinal Ürün Nasıl Anlaşılır? | aranıyorsa; yetkili satıcı vurgusu, abartısız |
| {Marka} Fiyatları | fiyatı belirleyen etkenler (seri, teknoloji, malzeme); rakam yok |
| {Marka} Bakım | markanın bakım talimatına dayanır |
| Boyner {Marka} Modelleri | filtreler, cinsiyet ve kategori kırılımları |

- **Marka bilgisi kaynakla yazılır.** Kuruluş yılı, ülke, teknoloji adları ve işlevleri markanın resmi
  sitesinden ya da kurumsal sayfasından doğrulanır; doğrulanamayan tarih ve iddia ("dünyanın en çok satan")
  yazılmaz. Teknoloji adları markanın yazımıyla geçer (Memory Foam, Arch Fit).
- **Karşılaştırma yapılmaz:** başka markalarla kıyas, üstünlük iddiası ve rakip marka adı yazılmaz.
- **Linkler (5-8):** marka + cinsiyet sayfaları (2-3), marka + kategori ya da marka + cinsiyet + kategori
  sayfaları (2-4; Google'da sıralananlar öncelikli), 0-1 genel kategori sayfası (markanın ana ürün ailesi).
  Anchor her zaman marka adını taşır ("Skechers kadın ayakkabı"); çıplak "kadın ayakkabı" anchor'ı genel
  kategori sayfasına aittir.
- Brief satırı Excel'de `Marka` sekmesine yazılır; Word belge adı yine `{slug}: {tam URL}` (`skechers: https://...`).
