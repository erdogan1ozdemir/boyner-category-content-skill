# Teslim öncesi kontrol listesi

## Hedef ve sahiplik

- [ ] Hedef URL dört sinyalle teyit edildi mi (envanter, canlı kayıt, SERP, GSC)? Canonical kendisi mi, index açık mı?
- [ ] `sahiplik.py` tablosu elle gözden geçirildi mi? SERBEST'teki marka ve renk kelimeleri ayıklandı mı?
- [ ] "N aday sayfa" notu taşıyan sahipler `--teyit` ya da `kategori.py` ile tek kimliğe indirildi mi?
- [ ] GSC'de aynı sorguda iki Boyner sayfası görünüyorsa kullanıcıya bildirildi mi?

## Brief

- [ ] Main KW hacmi 12 aylık ortalama mı? Mevsimsel kategoride zirve ayı ve son üç ay DİKKAT'te mi?
- [ ] İkincil kelimelerde BAŞKA SAYFA ya da KAPSAM DIŞI kelimesi var mı? (olmamalı)
- [ ] Her H2'nin araştırmada bir dayanağı var mı (rakip kapsamı, PAA, kelime kümesi, arama eğilimi) ve kurguda yazılı mı?
- [ ] İskelet bu kategorinin doğasına mı göre kuruldu, yoksa başka bir kategorinin başlıkları mı taşındı?
- [ ] Üç ya da daha fazla rakipte geçen konular karşılandı mı? Başlıklardan biri başka sayfanın kelimesi mi? (olmamalı)
- [ ] Kurgu satırlarında canlı kayıttan gelen somut adlar (alt türler, markalar, filtre değerleri) var mı?
- [ ] Link sayısı 5-8 mi, her link bölümü ve cümlesiyle yazılı mı, roller dağılmış mı?
- [ ] "Kapsam Dışı Kelimeler" sütunu dolu mu, sahipler tam yol olarak yazılı mı?
- [ ] SSS soruları PAA / otomatik tamamlama / SERBEST sorulardan mı? Başka sayfanın kelimesini taşıyan soru var mı?
- [ ] Yanıt biçimi metni olduğu gibi kopyalandı mı? Mevcut Durum sütunu dolu mu?

## İçerik

- [ ] Gövde başlıksız girişle açılıyor mu, ilk cümle ana kelimeyle tanım mı? Belgede H1 var mı? (olmamalı)
- [ ] Her H2'nin ilk cümlesi başlığın sorusunu doğrudan yanıtlıyor mu?
- [ ] Hitap baştan sona "siz" mi? "Sen", "biz", "tavsiye ederiz" var mı?
- [ ] Yazılan her tür, marka, malzeme ve kalıp `kategori.py` çıktısında var mı?
- [ ] Taslak bittikten sonra canlı kayıt bir kez daha okundu mu: sayfada olup içerikte olmayan ne var?
- [ ] BAŞKA SAYFA kelimeleri metinde en fazla bir kez ve anchor olarak mı geçiyor?
- [ ] **Anchor'ı sil, cümle hâlâ anlamlı mı?** "...göz atabilirsiniz" biçiminde link cümlesi var mı?
- [ ] Bu sayfanın ana kelimesi başka sayfaya anchor olmuş mu? (olmamalı)
- [ ] "•" satırları var mı? İlk cümleleri özneyi kuruyor ve bilgi ekliyor mu?
- [ ] Sayısal değerlerin kaynağı var mı? Ürün sayısı, fiyat, indirim, yıl, "bu sezon" geçiyor mu? (geçmemeli)
- [ ] Dayanaksız üstünlük iddiası ("en iyi", "en kaliteli") var mı?
- [ ] Bilgi taşımayan paragraf var mı? Her paragraf "okuyucu ne öğrendi" sorusundan geçti mi?
- [ ] Boyner hizmet cümleleri siteden teyit edildi mi, rakam içeriyor mu? (içermemeli)
- [ ] SSS yanıtları 30-70 kelime, ilk cümle doğrudan yanıt, gövdeyi tekrar etmiyor mu?
- [ ] Gövde uzunluğu içerikli rakiplerin medyanının üzerinde mi; altındaysa gerekçesi var mı?

- [ ] Başlıklar aranabilir ifadeler mi, ana kelimeyi ya da ürün adını taşıyor mu? ("Boy, Kalıp ve Beden" değil "Kadın Montlarda Boy, Kalıp ve Beden Seçimi")
- [ ] Yüklem dağılımı tek kipe mi kilitlenmiş? Özne ile yüklem uyuşuyor mu, ana kelime cümlede çekimli mi?
- [ ] Tanımlar ve sayımlar metin boyunca tutarlı mı? Gövde ile SSS aynı soruya aynı yanıtı mı veriyor? Genel adımlar tür maddeleriyle çelişiyor mu?
- [ ] Kalın etiketli maddelerin ilk cümlesi etiket silinince de anlamlı mı?
- [ ] Tablo ya da liste biçimi kalmış mı? (olmamalı; "•  " satırları ve "1. " önekli adımlar kullanılır)
- [ ] İhtiyaca göre tür eşleştirmesi, iki seçenek karşılaştırması ve numaralı karar adımları var mı?
- [ ] "Kategoride / kategorisinde" geçiyor mu? (geçmemeli) Madde etiketleri ürün adını ve cinsiyeti taşıyor mu?
- [ ] Kesin yargılar yumuşatıldı mı (genellikle, -abilir, önerilir)? Uzun cümleler noktalı virgülle mi uzatılmış?
- [ ] Gövde 1.500-2.500 kelime bandında mı; uzunluk tekrarla değil yeni bilgiyle mi kuruldu?
- [ ] Ticari kelimeler (fiyatları, uygun, ekonomik, kaliteli, şık) karşılandı mı? Net fiyat ya da aralık var mı? (olmamalı)
- [ ] Bağımsız içerik değerlendirmesi (`seo-content`) yapıldı mı, bulgular işlendi mi?
- [ ] Word belgesinin adı `{slug}: {tam URL}` mi?

## Otomatik denetim

```bash
python3 scripts/icerik_denetim.py --json icerik.json --sahiplik sahiplik.json --arastirma arastirma.json --canli
```

Betik bulgu bulursa 1 koduyla çıkar; bulgular giderilmeden çıktı üretilmez. `NOT:` satırları okunarak karar
verilecek adaylardır (kalıp ifade, zamana bağlı söz, karşılanmayan SERBEST kelime).

## Teslim

Çıktılar çalışma klasörüne kaydedilir: brief Excel'i ve içerik Word dosyası (HTML yalnız istenirse). Kullanıcıya üç şey
söylenir: hangi bilgi hangi kaynaktan alındı; ne yazılmadı ve neden (özellikle sahibi başka sayfa olan
kelimeler); hangi konuda karar ya da teyit bekleniyor (site düzeyinde çakışma, canonical, CMS'te SSS modülü).
