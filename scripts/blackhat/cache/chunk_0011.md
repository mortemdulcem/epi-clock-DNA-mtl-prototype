Son olarak, aynı byte `slice` `b` değerini alıp `json.Unmarshal(b, &f)` çağrısıyla decode edersiniz. Bu, bir `Foo` struct örneği `f` üretir. XML ile çalışmak da bu sürece neredeyse birebir benzer.

JSON ve XML ile çalışırken, sıkça alan etiketleri (field tags) kullanırsınız. Bunlar, `struct` alanlarına atadığınız, marshal/unmarshal mantığının ilgili elemanları nasıl bulacağını ve nasıl işleyeceğini tanımlayan meta veri öğeleridir. Bu alan etiketlerinin sayısız varyasyonu vardır, ancak XML ile çalışmak için kullanımlarını gösteren kısa bir örnek aşağıdadır:

```go
type Foo struct {
    Bar     string     `xml:"id,attr"`
    Bar     string     `xml:"parent>child"`
}
```

Struct alanlarını takip eden ve ters tırnaklar (backticks) içine alınmış string değerleri alan etiketleridir (field tags). Alan etiketleri her zaman etiket adıyla (bu durumda `xml`) başlar, ardından iki nokta üst üste gelir ve çift tırnak içine alınmış yönerge (directive) bulunur. Bu yönerge, alanların nasıl ele alınacağını tanımlar. Bu örnekte, `Bar` alanının bir element değil, `id` adında bir öznitelik (attribute) olarak ele alınması gerektiğini ve `Bar` alanının `parent` isimli bir üst elementin `child` adlı bir alt elementinde bulunması gerektiğini belirten yönergeler veriyorsunuz. Önceki JSON örneğini yapıyı XML olarak encode edecek şekilde değiştirirseniz, aşağıdaki çıktıyı görürsünüz:

```xml
<Foo id="Joe Junior"><parent><child>Hello Shabado</child></parent></Foo>
```

XML encoder, eleman adlarını, tag yönergelerini kullanarak yansıtmalı (reflective) biçimde belirler; böylece her alan ihtiyaçlarınıza göre ele alınır.

Bu kitap boyunca, ASN.1 ve MessagePack dâhil olmak üzere diğer veri serileştirme (serialization) formatlarıyla çalışırken bu alan etiketlerinin kullanıldığını göreceksiniz. Ayrıca, özellikle Server Message Block (SMB) protokolünü nasıl ele alacağınızı öğrenirken, kendi özel etiketlerinizi tanımlamaya ilişkin bazı ilgili örnekleri de tartışacağız.

## Özet

Bu bölümde, Go ortamınızı kurdunuz ve Go dilinin temel yönlerini öğrendiniz. Bunlar, Go’nun tüm özelliklerinin kapsamlı bir listesi değildir; dil, tek bir bölüme sığdırılamayacak kadar ince ayrıntılı ve geniştir. Bunun yerine, takip eden bölümlerde en faydalı olacak yönleri seçtik. Şimdi dikkatimiz, dilin güvenlik uzmanları ve saldırganlar (hackers) için pratik uygulamalarına yönelecek. Haydi başlayalım!

## TCP, Tarayıcılar ve Proxy’ler

Go’nun pratik uygulamalarına, bağlantı odaklı (connection-oriented), güvenilir iletişimler için baskın standart ve modern ağların temeli olan Transmission Control Protocol (TCP) ile başlayalım. TCP her yerdedir; iyi belgelenmiş kütüphaneleri, kod örnekleri ve genel olarak kolay anlaşılır paket akışları vardır. Ağ trafiğini tam olarak değerlendirmek, analiz etmek, sorgulamak ve manipüle etmek için TCP’yi anlamak zorundasınız.

Bir saldırgan olarak, TCP’nin nasıl çalıştığını anlamalı ve kullanılabilir TCP yapıları geliştirebilmelisiniz ki açık/kapalı portları tespit edebilin, syn-flood korumaları gibi yanlış-pozitif (false-positive) olabilecek sonuçları tanıyabilin ve port yönlendirme (port forwarding) yoluyla dışa giden (egress) kısıtlamaları aşabilesiniz. Bu bölümde, Go ile temel TCP haberleşmesini öğrenecek; eşzamanlı (concurrent), uygun şekilde kısıtlanmış (throttled) bir port tarayıcı (port scanner) inşa edecek; port yönlendirme için kullanılabilecek bir TCP proxy oluşturacak ve Netcat’in “gaping security hole” özelliğini yeniden gerçekleştireceksiniz.

TCP’nin paket yapısı ve akışı, güvenilirlik, iletişim yeniden birleştirme (reassembly) ve daha fazlası dâhil tüm inceliklerini ele alan kitaplar başlı başına yazılmıştır. Bu ayrıntı seviyesi, bu kitabın kapsamının ötesindedir. Daha fazla ayrıntı için Charles M. Kozierok’un *The TCP/IP Guide* (No Starch Press, 2005) kitabını okumalısınız.

## TCP El Sıkışmasını (Handshake) Anlamak

Tazeleme ihtiyacı olanlar için temelleri gözden geçirelim. Şekil 2-1, bir portun açık, kapalı veya filtrelenmiş olup olmadığını belirlemek için TCP’nin bir el sıkışma (handshake) süreci kullandığını göstermektedir.

**Şekil 2-1: TCP el sıkışmasının temelleri**

Port açıksa, üç aşamalı bir el sıkışma gerçekleşir. Önce istemci, bir iletişimin başlangıcını işaret eden bir `syn` paketi gönderir. Sunucu daha sonra aldığı `syn` paketini onaylayan bir `syn-ack` (syn acknowledgment) ile yanıt verir ve bu da istemcinin sunucunun yanıtını onaylayan bir `ack` (acknowledgment) paketiyle el sıkışmayı tamamlamasını tetikler. Bundan sonra veri aktarımı gerçekleşebilir. Port kapalıysa, sunucu `syn-ack` yerine bir `rst` paketiyle yanıt verir. Trafik bir güvenlik duvarı (firewall) tarafından filtreleniyorsa, istemci genellikle sunucudan hiç yanıt almaz.

Bu yanıtları anlamak, ağ tabanlı araçlar yazarken önemlidir. Araçlarınızın çıktısını, bu düşük seviyeli paket akışlarıyla ilişkilendirmek, bir ağ bağlantısını doğru şekilde kurduğunuzu doğrulamanıza ve olası sorunları gidermenize yardımcı olur. Bu bölümün ilerleyen kısımlarında göreceğiniz gibi, istemci-sunucu TCP bağlantı el sıkışmalarının tam olarak tamamlanmasına izin vermezseniz, kodunuza kolaylıkla hatalar sokabilir, bunun sonucunda yanlış veya yanıltıcı sonuçlar üretebilirsiniz.
