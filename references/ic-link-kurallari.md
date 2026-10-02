# İç link seçimi ve yerleşimi

İçerik başına **5-8 iç link** kullanılır. Daha azı sayfayı kategori ağacından kopuk bırakır; daha fazlası
gövdeyi link tarlasına çevirir ve her linkin taşıdığı değeri böler.

## Link metne sonradan eklenmez

Önce anchor'ın geçtiği cümlenin metinde zaten var olması gerekir. Ölçü: **anchor'ı sil, cümle hâlâ anlamlı
mı?** Değilse cümle linki taşımak için kurulmuştur, yeniden yazılır.

| Yerine | Böyle |
|---|---|
| "[Kadın kaban] modellerine de göz atabilirsiniz." | "Diz altına inen, yün karışımlı modeller mont değil [kadın kaban] sınıfına girer." |
| "Markalar arasında [Columbia kadın mont] da bulunuyor." | "Yağmurlu havalar için su geçirmez membranlı [Columbia kadın mont] modelleri öne çıkar." |
| "Ayakkabı için [kadın bot] kategorisini inceleyebilirsiniz." | "Uzun bir parka, bilekte biten düz tabanlı bir [kadın bot] ile dengelenir." |

## Dağılım

5-8 link şu rollere dağılır. Her rol dolmak zorunda değildir, ama dağılım tek role yığılmaz:

| Rol | Adet | Hedef | Metindeki yeri |
|---|---|---|---|
| Üst kategori | 1 | bir üst seviye (kadın dış giyim) | giriş |
| Alt kategori (hub -> spoke) | 2-4 | bu sayfanın alt türleri (kadın şişme mont, kadın peluş mont) | Çeşitleri listesi |
| Kardeş / komşu kategori | 0-1 | aynı seviyede karıştırılan tür (kadın kaban, kadın trençkot) | Çeşitleri ya da Nasıl Seçilir |
| Marka + kategori | 1-2 | Google'da sıralanan marka+kategori sayfası | Markaları |
| Tamamlayıcı kategori (çapraz) | 1-2 | birlikte kullanılan ürün (kadın bot, atkı) | Kombin / Kullanım |
| Öteki cinsiyet | 0-1 | erkek mont | kapanış ya da SSS, yalnız doğal bağlam varsa |

Alt kategori linkleri önceliklidir: üst sayfa ile alt sayfalar arasındaki bağ hem kullanıcının yolunu hem de
hangi sayfanın hangi kelimeye ait olduğunu arama motoruna anlatır.

## Kurallar

- **Anchor, hedef sayfanın ana kelimesidir** ("kadın şişme mont", "Columbia kadın mont"): insanların arattığı
  terim. "Buraya", "tıklayın", "bu modeller", çıplak URL kullanılmaz. Anchor en fazla 4-5 kelime.
- **Bu sayfanın ana kelimesi hiçbir linkin anchor'ı olamaz.** "Kadın mont" anchor'ıyla başka bir sayfaya
  (ör. marka sayfasına) link verilirse arama motoruna o kelimenin sahibi olarak öteki sayfa gösterilmiş olur.
- **Sayfa kendine link vermez.**
- **Aynı hedefe iki kez link verilmez;** aynı ada sahip iki kategori kimliğinden yalnız biri (teyitli olan)
  kullanılır.
- **Benzer niyetli iki sayfadan birine link verilir.** `/kadin-sisme-mont` ile `/kadin-mont-sisme-mont`
  ikisi birden linklenmez.
- **Hedef canlı ve dolu olmalı:** 200 döner, canonical'ı kendisidir, en az 8 ürünü vardır (daha azı olan alt
  tür linklenmez, metinde düz geçer). Sitemap eski kategori kimliklerini de taşıdığı için bir adresin envanterde
  olması canlı ve dolu olduğunu göstermez; sayfanın canlı kaydındaki alt kategori adresleri esastır.
  `icerik_denetim.py --canli` bunu her link için kontrol eder. Canonical'ı başka sayfayı gösteren adrese
  değil, canonical adresin kendisine link verilir.
- **Marka linki yalnız marka + kategori sayfasına verilir** (`/columbia-kadin-mont-x-b596-g3731-c23896554`),
  markanın ana sayfasına (`/columbia-x-b596`) değil: bağlam kategoriyse hedef de kategori kırılımıdır.
  Seçim ölçütü: `arastirma.py` Boyner haritasında o kelimede sıralanan sayfa.
- **Arama sayfasına (`/search?q=...`) link verilmez.** Bu sayfalar Cloudflare doğrulaması arkasında ve
  içerik taşımıyor; durumları betikle teyit edilemiyor. Kullanıcı açıkça isterse istisna yapılır.
- **Filtre sayfasına (`?renk=`, `?materyal=`) link** yalnız o adres sitemap envanterinde varsa verilir.
- **Kampanya, outlet ve tarihli sayfalara** (`/kampanya/...`, `/outlet-...`) link verilmez; içerik kalıcıdır,
  o sayfalar değil.
- Tek paragrafta en fazla 2, tek H2'de en fazla 4 link (alt kategori linklerinin toplandığı Çeşitleri bölümü
  dışında 2'yi geçmemesi iyi olur). Giriş paragrafında en fazla 1.
- SSS yanıtlarında link en fazla 1 kez kullanılır; SSS modülü şemaya girerse link düz metne döner.

## Adayları bulmak

```bash
python3 scripts/envanter.py iliskili {hedef URL}     # üst, alt, akraba, marka ve filtre sayfaları
python3 scripts/kategori.py {hedef URL}              # sayfadaki alt kategori ve marka filtreleri (canlı)
python3 scripts/envanter.py sahip "kadın bot"        # tamamlayıcı kategori için sahibi bul
```

Alt kategori adayları için öncelik `kategori.py` çıktısındaki "Alt kategoriler" listesidir: sitenin o
sayfada gerçekten gösterdiği alt kırılımlar bunlardır ve kimlikleri doğrudur. `envanter.py iliskili` daha
geniş ama aynı adlı eski kimlikleri de getirir.

Brief'te her link, yerleşeceği bölüm ve cümleyle birlikte yazılır:

```
1. kadın şişme mont : https://www.boyner.com.tr/kadin-sisme-mont-x-g3731-c23896555
   H2 · Kadın Mont Çeşitleri bölümünde, "Şişme mont" maddesinin tanım cümlesinde.
```
