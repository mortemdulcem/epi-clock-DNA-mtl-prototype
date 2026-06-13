Jen’e, tüm desteği, cesareti ve ben ofisime kapanıp gecelerimi ve hafta sonlarımı bitmek bilmeyen bu kitap üzerinde çalışarak geçirirken hayatı ileriye taşımaya devam ettiği için teşekkür etmek istiyorum. Jen, bana sandığından çok daha fazla yardım ettin.

## Önsöz

Programlama dilleri her zaman bilgi güvenliği üzerinde etkili olmuştur. Her bir dilde mevcut olan tasarım kısıtları, standart kütüphaneler ve protokol implementasyonları, o dil üzerinde inşa edilen herhangi bir uygulamanın saldırı yüzeyini fiilen tanımlar. Güvenlik araçları da farklı değildir; doğru dil, karmaşık görevleri basitleştirebilir ve son derece zor işleri önemsiz hale getirebilir. Go’nun çapraz platform desteği, tek binary çıktısı, eşzamanlılık (concurrency) özellikleri ve devasa ekosistemi, onu güvenlik aracı geliştirme için harika bir tercih haline getiriyor. Go, hem güvenli uygulama geliştirme hem de güvenlik araçları yazımı için oyunun kurallarını yeniden yazıyor; daha hızlı, daha güvenli ve daha taşınabilir araçlar geliştirmeye imkân veriyor.

Metasploit Framework üzerinde çalıştığım 15 yıl boyunca, proje iki tam yeniden yazım geçirdi, diller Perl’den Ruby’ye değişti ve şu anda çok dilli modüller, eklentiler ve yükler/faydalı yükler (payload) yelpazesini destekliyor. Bu değişiklikler, yazılım geliştirmenin sürekli evrilen doğasını yansıtıyor; güvenlik alanında ayakta kalmak istiyorsanız, araçlarınızın uyum sağlaması gerekir ve doğru dili kullanmak devasa miktarda zamanı kurtarabilir. Ancak tıpkı Ruby gibi, Go da bir gecede her yerde karşımıza çıkan bir dil haline gelmedi. Ekosistemin belirsizlikleri ve standart kütüphaneler olgunlaşmadan önce yaygın görevleri yerine getirmek için gerekli muazzam efor düşünüldüğünde, yeni bir dil kullanarak değerli bir şey inşa etmek belli bir inanç sıçraması gerektirir.

*Black Hat Go*’nun yazarları, Go güvenlik araçları geliştirme alanında öncüdür; BlackSheepWall, Lair Framework ve sipbrute gibi — ve daha niceleri — en erken açık kaynak Go projelerinden bazılarından sorumludurlar. Bu projeler, dille neler inşa edilebileceğine dair mükemmel örnekler sunar. Yazarlar, yazılımı inşa etmekte ne kadar rahatsa onu parçalamakta da o kadar rahattır ve bu kitap, bu becerileri birleştirme yeteneklerinin harika bir örneğidir.

*Black Hat Go*, güvenlik alanında Go geliştirmeye başlarken nadiren kullanılan dil özelliklerine takılıp kalmadan ihtiyaç duyacağınız her şeyi sağlar. Aşırı hızlı bir ağ tarayıcı, şeytani bir HTTP proxy veya çapraz platform bir komuta-denetim (command-and-control) çerçevesi (framework) mi yazmak istiyorsunuz? Bu kitap sizin için. Güvenlik aracı geliştirme konusunda içgörü arayan tecrübeli bir programcıysanız, bu kitap, saldırı aracı yazarken her türden hacker’ın göz önünde bulundurduğu kavramları ve ödünleşimleri (trade-off) tanıtacaktır. Güvenlikle ilgilenen deneyimli Go geliştiricileri, burada kullanılan yaklaşımlardan çok şey öğrenebilir; zira başka yazılımlara saldırmak için araçlar yazmak, tipik uygulama geliştirmeden farklı bir zihniyet gerektirir. Güvenlik kontrollerini atlatma ve tespitten kaçınma gibi hedefleriniz olduğunda tasarım ödünleşimleriniz muhtemelen önemli ölçüde farklı olacaktır.

Halihazırda saldırı güvenliği (offensive security) alanında çalışıyorsanız, bu kitap mevcut çözümlerden ışık yılı daha hızlı yardımcı programlar (utility) geliştirmenize yardımcı olacaktır. Savunma tarafında veya olay müdahalesinde (incident response) çalışıyorsanız, bu kitap size Go dilinde yazılmış zararlı yazılımları analiz etme ve bunlara karşı savunma konusunda fikir verecektir.

Keyifli hack’lemeler!

HD Moore  
Metasploit Project ve Critical Research Corporation Kurucusu  
Atredis Partners’ta Araştırma ve Geliştirmeden Sorumlu Başkan Yardımcısı

## Giriş

### Neden Hack’lemek için Go Kullanılmalı?

Go’dan önce, kullanım kolaylığını önceliklendirmek isterseniz Python, Ruby veya PHP gibi dinamik tür denetimli dilleri kullanır, bunun karşılığında performans ve güvenlikten ödün verirdiniz. Alternatif olarak, C veya C++ gibi, yüksek performans ve güvenlik sunan ancak çok kullanıcı dostu olmayan statik tür denetimli bir dil seçebilirdiniz. Go, birincil atası olan C’nin büyük kısmındaki çirkinliklerden arındırılmıştır; bu da geliştirmeyi çok daha kullanıcı dostu kılar. Aynı zamanda, derleme (compile) anında sözdizimi (syntax) hataları üreten statik tür denetimli bir dildir; bu da kodunuzun gerçekten güvenli bir şekilde çalışacağına dair güveninizi artırır. Derlenen bir dil olduğundan yorumlamalı dillere kıyasla daha optimal çalışır ve çok çekirdekli işlem (multicore computing) göz önünde bulundurularak tasarlanmıştır; bu da eşzamanlı programlamayı çocuk oyuncağı haline getirir.

Go kullanmak için bu nedenler, güvenlik uzmanlarını özel olarak hedeflemiyor. Ancak dilin pek çok özelliği, özellikle hacker’lar ve saldırganlar için oldukça kullanışlıdır:

- **Temiz package yönetim sistemi** Go’nun package yönetim çözümü zariftir ve doğrudan Go’nun araç setiyle entegredir. `go` binary’sini kullanarak paketleri ve bağımlılıkları kolayca indirebilir, derleyebilir ve kurabilirsiniz; bu da üçüncü taraf kütüphaneleri kullanmayı basit ve genellikle çakışmalardan uzak kılar.
- **Çapraz derleme (cross-compilation)** Go’daki en iyi özelliklerden biri, yürütülebilir dosyaları çapraz derleyebilmesidir. Kodunuz ham C ile etkileşime girmediği sürece, Linux veya Mac sisteminizde kolayca kod yazıp bunu Windows dostu Portable Executable formatında derleyebilirsiniz.
- **Zengin standart kütüphane** Diğer dillerde geliştirme yaparken harcanan zaman, Go’nun standart kütüphanesinin kapsamını takdir etmemizi sağladı. Pek çok modern dil, kriptografi (crypto), ağ haberleşmesi, veritabanı bağlantısı ve veri kodlama (JSON, XML, Base64, hex) gibi yaygın görevleri yerine getirmek için gereken standart kütüphanelerden yoksundur. Go, bu kritik işlevlerin ve kütüphanelerin çoğunu dilin standart paketlemesinin bir parçası olarak içerir; bu da geliştirme ortamınızı doğru şekilde kurmak veya fonksiyonları çağırmak için gerekli çabayı azaltır.
- **Eşzamanlılık (concurrency)** Daha uzun süredir var olan dillerin aksine, Go ilk yaygın çok çekirdekli işlemcilerin piyasaya çıkmasıyla aşağı yukarı aynı dönemde yayımlandı. Bu nedenle, Go’nun eşzamanlılık kalıpları (pattern) ve performans optimizasyonları özellikle bu modele göre ince ayar yapılmıştır.
