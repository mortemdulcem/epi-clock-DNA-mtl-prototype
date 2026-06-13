50   Bölüm 3

yaparak `Status` struct'ını normalde yaptığınız gibi, dışa açılmış `Status` ve `Messages` veri tiplerine erişerek sorgulayabilirsiniz.

Bu tür yapılandırılmış veri tiplerini ayrıştırma (parse) süreci, XML veya hatta ikili (binary) temsiller gibi diğer kodlama (encoding) formatları için de tutarlıdır. Sürece, beklenen yanıt verisini temsil eden bir `struct` tanımlayarak başlarsınız ve ardından veriyi bu `struct` içine decode edersiniz. Diğer formatları ayrıştırmanın ayrıntıları ve gerçek uygulaması size bırakılmıştır.

Sonraki bölümlerde, üçüncü taraf API'lerle etkileşime giren araçlar oluşturmanıza yardımcı olmak için bu temel kavramlar uygulanacak; amaç, saldırgan teknikleri ve keşif (reconnaissance) faaliyetlerini geliştirmektir.

## Shodan ile Etkileşen Bir HTTP İstemcisi Oluşturma

Herhangi bir kuruluş üzerinde yetkili saldırgan faaliyetlere başlamadan önce, iyi bir saldırgan mutlaka keşifle başlar. Genellikle bu, hedefe paket göndermeyen pasif tekniklerle başlar; böylece etkinliğin tespiti neredeyse imkânsız hale gelir. Saldırganlar, hedef hakkında potansiyel olarak faydalı bilgi elde etmek için sosyal ağlar, kamuya açık kayıtlar ve arama motorları da dahil olmak üzere çeşitli kaynak ve hizmetlerden yararlanır.

Görünüşte zararsız görünen bilgilerin, zincirli bir saldırı senaryosunda ortama ait bağlam (context) uygulandığında nasıl kritik hale geldiği inanılmazdır. Örneğin, ayrıntılı (verbose) hata mesajları gösteren bir web uygulaması tek başına düşük önem derecesine sahip sayılabilir. Ancak, bu hata mesajları kurumsal kullanıcı adı formatını açığa çıkarıyorsa ve kurum VPN'i için tek faktörlü kimlik doğrulaması kullanıyorsa, bu hata mesajları, parola tahminine dayalı saldırılar üzerinden iç ağın ele geçirilme olasılığını artırabilir.

Bilgi toplarken düşük profil sürdürmek, hedefin farkındalık ve güvenlik duruşunun (security posture) nötr kalmasını sağlayarak saldırınızın başarılı olma olasılığını artırır.

Shodan (`https://www.shodan.io`), kendisini “internet bağlantılı cihazlar için dünyanın ilk arama motoru” olarak tanımlayan ve ürün adları, sürümler, yerel ayar (locale) ve daha fazlası gibi metadata dâhil, ağ cihazları ve hizmetlerine ait aranabilir bir veritabanı tutarak pasif keşfi kolaylaştıran bir servistir. Shodan’ı, çok daha fazlasını yapıyor olsa bile, tarama verilerinin (scan data) bir deposu olarak düşünebilirsiniz.

### Bir API İstemcisi Oluşturmanın Adımlarını Gözden Geçirme

Sonraki birkaç bölümde, Shodan API’siyle etkileşen, sonuçları ayrıştıran ve ilgili bilgileri gösteren bir HTTP istemcisi oluşturacaksınız. Öncelikle, Shodan API anahtarına (API key) ihtiyacınız var; bunu Shodan’ın sitesine kayıt olduğunuzda alırsınız. Bu satırlar yazılırken, en düşük seviye için ücret oldukça cüzi ve bireysel kullanım için yeterli kredi sunuyor, dolayısıyla buna kaydolun. Shodan zaman zaman indirimli fiyatlar da sunuyor; birkaç dolar tasarruf etmek istiyorsanız dikkatle takip edin.

Şimdi, siteden API anahtarınızı alın ve bir ortam değişkeni (environment variable) olarak ayarlayın. Aşağıdaki örnekler, yalnızca API anahtarınızı `SHODAN_API_KEY` değişkeni olarak kaydederseniz aynen çalışacaktır. Değişkeni ayarlama konusunda yardıma ihtiyacınız varsa, işletim sisteminizin kullanıcı kılavuzuna bakın veya daha iyisi, Bölüm 1’e göz atın.

---

Bu bölümdeki koda geçmeden önce, burada gösterilenin tam özellikli, kapsamlı bir istemci değil, temel (bare-bones) bir istemci uygulaması olduğunu anlayın. Ancak, şimdi oluşturacağınız temel iskelet (scaffolding), gerektiğinde diğer API çağrılarını da uygulayabilmeniz için gösterilen kodu kolayca genişletmenizi sağlar.

Oluşturacağınız istemci iki API çağrısı uygulayacak: biri abonelik kredi bilgilerini sorgulamak, diğeri ise belirli bir string içeren host’ları aramak için. İkinci çağrıyı, örneğin belirli bir ürüne uyan portlara veya işletim sistemlerine sahip host’ları tespit etmek için kullanabilirsiniz.

Neyse ki, Shodan API’si oldukça yalın ve güzel yapılandırılmış JSON yanıtları üretiyor. Bu da API etkileşimini öğrenmek için iyi bir başlangıç noktası yapıyor. Bir API istemcisi hazırlayıp inşa ederken tipik adımların üst düzey bir özeti şöyle:

- Servisin API dokümantasyonunu inceleyin.
- Karmaşıklığı ve tekrarları azaltmak için kod için mantıklı bir yapı tasarlayın.
- Gerektiğinde Go içinde istek (request) veya yanıt (response) tiplerini tanımlayın.
- Ayrıntılı veya tekrarlı mantığı azaltmak amacıyla basit başlatma (initialization), kimlik doğrulama (authentication) ve iletişimi kolaylaştıracak yardımcı fonksiyonlar ve tipler oluşturun.
- API tüketici fonksiyonları ve tipleriyle etkileşen istemciyi inşa edin.

Bu bölümde her adımı tek tek işaret etmeyeceğiz, ancak geliştirme sürecinizde bu listeyi bir yol haritası olarak kullanmalısınız. Shodan’ın sitesindeki API dokümantasyonunu hızlıca gözden geçirerek başlayın. Dokümantasyon minimal olsa da bir istemci programı oluşturmak için gereken her şeyi sağlıyor.

## Proje Yapısını Tasarlama

Bir API istemcisi oluştururken, fonksiyon çağrıları ve mantığın başlı başına ayakta durabileceği şekilde yapılandırmalısınız. Bu, uygulamayı başka projelerde bir kütüphane (library) olarak yeniden kullanmanıza olanak sağlar. Böylece gelecekte tekerleği yeniden icat etmek zorunda kalmazsınız. Yeniden kullanılabilirlik için inşa etmek, bir projenin yapısını biraz değiştirir. Shodan örneği için proje yapısı şöyle:

```bash
$ tree github.com/blackhat-go/bhg/ch-3/shodan
github.com/blackhat-go/bhg/ch-3/shodan
|---cmd
|   |---shodan
|        |---main.go
|---shodan
     |---api.go
     |---host.go
     |---shodan.go
```

`main.go` dosyası `package main` tanımlar ve esas olarak oluşturacağınız API’nin bir tüketicisi olarak kullanılır; bu durumda, ağırlıklı olarak istemci uygulamanızla etkileşim kurmak için kullanacaksınız.

`shodan` dizinindeki `api.go`, `host.go` ve `shodan.go` dosyaları `package shodan` tanımlar; bu paket, Shodan ile giriş çıkış (I/O) iletişimi için gerekli tip ve fonksiyonları içerir. Bu paket, çeşitli projelere import edebileceğiniz bağımsız bir kütüphaneniz haline gelecektir.
