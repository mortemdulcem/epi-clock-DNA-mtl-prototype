XOR bölümünü okurken, `XorDecode0` fonksiyonunun çözümlenmiş bir chunk parçası ürettiğini, ancak CRC sağlama toplamını (checksum) hiç güncellemediğini fark etmiş olabilirsiniz. Bu sorunu düzeltebilir misiniz?

`WriteData()` fonksiyonu, rastgele chunk parçaları enjekte etme yeteneği sağlar. Mevcut yardımcı (ancillary) chunk parçalarını üzerine yazmak (overwrite) isteseydiniz hangi kod değişikliklerini yapmanız gerekirdi? Yardıma ihtiyaç duyarsanız, bayt kaydırma (byte shifting) ve `Seek()` fonksiyonu hakkındaki açıklamamız bu sorunu çözmenize yardımcı olabilir.

Burada daha zorlayıcı bir problem var: PNG `DATA` bayt chunk’ını, yani yükü (payload), çeşitli yardımcı chunk parçalarına dağıtarak enjekte etmeyi deneyin. Bunu her seferinde bir bayt olacak şekilde yapabilir veya birden fazla bayt gruplarıyla çalışabilirsiniz; yaratıcılığınızı kullanın. Ek bir bonus olarak, tam yük bayt ofset konumlarını okuyan bir decoder oluşturun; böylece yükü çıkarmak daha kolay hale gelir.

Bu bölüm, XOR’u bir gizlilik tekniği olarak nasıl kullanacağınızı — gömülü yükü karartma (obfuscation) yöntemi olarak — açıkladı. AES şifreleme gibi farklı bir teknik uygulamayı deneyin. Go çekirdek paketleri birçok olasılık sağlar (tazeleme ihtiyacınız olursa Bölüm 11’e bakın). Çözümün yeni görüntüyü nasıl etkilediğini gözlemleyin. Toplam boyutu artırıyor mu, artırıyorsa ne kadar?

Bu bölümdeki kod fikirlerini kullanarak diğer görüntü dosya formatlarına da destek ekleyin. Diğer görüntü tanımları PNG kadar düzenli olmayabilir. Kanıt mı istiyorsunuz? Oldukça göz korkutucu olabilen PDF tanımını (specification) okuyun. Bu yeni görüntü formatında veri okuma ve yazma zorluklarını nasıl çözerdiniz?

## BUILDING A COMMAND-AND-CONTROL RAT

Bu bölümde, önceki bölümlerden birkaç dersi bir araya getirerek temel bir komuta-kontrol (command and control, C2) uzaktan erişim Truva atı (remote access Trojan, RAT) inşa edeceğiz. RAT, saldırganların ele geçirilmiş kurban makinesinde dosya sistemine erişme, kod yürütme ve ağ trafiğini dinleme gibi işlemleri uzaktan gerçekleştirmek için kullandıkları bir araçtır.

Bu RAT’ı inşa etmek için üç ayrı araç oluşturmamız gerekiyor: bir istemci implant, bir sunucu ve bir yönetim (admin) bileşeni. İstemci implant, RAT’ın ele geçirilmiş iş istasyonunda çalışan kısmıdır. Sunucu, istemci implant ile etkileşime giren kısımdır; tıpkı yaygın kullanılan bir C2 aracı olan Cobalt Strike’ın sunucu bileşeni (team server) gibi, ele geçirilmiş sistemlere komutlar gönderir. Tek bir servisin hem sunucu hem de yönetim işlevlerini kolaylaştırdığı team server’ın aksine, komutları gerçekten göndermek için kullanılan ayrı, bağımsız bir admin bileşeni oluşturacağız. Bu sunucu, araya giren bir aracı gibi davranarak ele geçirilmiş sistemler ile admin bileşenini kullanan saldırgan arasındaki haberleşmeyi koordine edecek.

RAT tasarlamanın sonsuz sayıda yolu vardır. Bu bölümde, uzak erişim için istemci ve sunucu haberleşmesini nasıl ele alacağınızı vurgulamayı amaçlıyoruz. Bu nedenle, size basit ve cilasız bir şey nasıl inşa edilir gösterecek, ardından belirli sürümünüzü daha sağlam kılmak için önemli iyileştirmeler yapmanız için sizi teşvik edeceğiz. Bu iyileştirmeler, birçok durumda, önceki bölümlerden içerik ve kod örneklerini yeniden kullanmanızı gerektirecek. Uygulamanızı geliştirmek için bilginizi, yaratıcılığınızı ve problem çözme yeteneğinizi kullanacaksınız.

## Başlarken

Başlamak için neler yapacağımızı gözden geçirelim: Yönetim bileşeninden (onu da biz oluşturacağız) işletim sistemi komutları şeklinde iş alan bir sunucu oluşturacağız. Sunucudan periyodik olarak yeni komutlar olup olmadığını kontrol eden ve ardından komut çıktısını tekrar sunucuya yükleyen (publish) bir implant oluşturacağız. Sunucu daha sonra bu sonucu yönetim istemcisine geri verecek, böylece operatör (siz) çıktıyı görebileceksiniz.

Hadi, tüm bu ağ etkileşimlerini yönetmemize yardımcı olacak bir aracı yüklemekle ve bu proje için dizin yapısını gözden geçirmekle başlayalım.

## gRPC API Tanımlamak için Protocol Buffers’ı Kurmak

Tüm ağ etkileşimlerini, Google tarafından oluşturulmuş yüksek performanslı bir uzak prosedür çağrısı (remote procedure call, RPC) framework’ü olan gRPC kullanarak inşa edeceğiz. RPC framework’leri, istemcilerin, alttaki detayların hiçbirini anlamak zorunda kalmadan, standart ve tanımlı protokoller üzerinden sunucularla iletişim kurmasına izin verir. gRPC framework’ü HTTP/2 üzerinden çalışır ve mesajları oldukça verimli, ikili (binary) bir yapıda iletir.

Diğer RPC mekanizmalarında (REST veya SOAP gibi) olduğu gibi, veri yapılarımızın serileştirme (serialize) ve tersine serileştirme (deserialize) işlemlerini kolaylaştırmak için tanımlanması gerekir. Neyse ki, verilerimizi ve API fonksiyonlarımızı gRPC ile kullanabilmemiz için tanımlamamızı sağlayan bir mekanizma var. Protocol Buffers (kısaca Protobuf) adı verilen bu mekanizma, `.proto` dosyası biçiminde API ve karmaşık veri tanımları için standart bir sözdizimi sunar. Bu tanım dosyasını Go ile uyumlu arayüz (interface) iskeletleri (stub) ve veri tiplerine derlemek için araçlar mevcuttur. Aslında, bu araçlar çeşitli dillerde çıktı üretebilir; yani aynı `.proto` dosyasını kullanarak C# stub’ları ve tipleri de üretebilirsiniz.

İlk iş olarak sisteminize Protobuf derleyicisini kurmalısınız. Kurulum adımlarını tek tek anlatmak bu kitabın kapsamı dışında, ancak resmi Go Protobuf deposunun https://github.com/golang/protobuf/ adresindeki "Installation" bölümünde tüm ayrıntıları bulabilirsiniz. Bu arada, aşağıdaki komutla gRPC paketini de kurun:

```bash
> go get -u google.golang.org/grpc
```
