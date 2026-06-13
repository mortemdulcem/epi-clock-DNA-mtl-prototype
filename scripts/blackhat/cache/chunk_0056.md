### Meta Verileri ve Referans Alanları Anlama

SMB spesifikasyonuna biraz daha derinlemesine bakarsanız, bazı mesajların aynı mesaj içindeki diğer alanlara referans veren alanlar içerdiğini görürsünüz. Örneğin, Negotiate yanıt mesajından alınan şu alanlar, asıl değeri içeren, değişken uzunluklu bir bayt diliminin (byte slice) ofsetini ve uzunluğunu referans alır:

- **SecurityBufferOffset (2 bayt)**: SMB2 başlığının başlangıcından güvenlik arabelleğine (security buffer) kadar olan ofset (bayt cinsinden).
- **SecurityBufferLength (2 bayt)**: Güvenlik arabelleğinin uzunluğu (bayt cinsinden).

Bu alanlar özünde birer meta veri gibi davranır. Mesaj spesifikasyonunda, daha ileride, verinizin gerçekten yer aldığı değişken uzunluklu alanı bulursunuz:

- **Buffer (değişken)**: `SecurityBufferOffset` ve `SecurityBufferLength` alanlarıyla belirtilen, yanıt için güvenlik arabelleğini içeren değişken uzunluklu arabellek (buffer). Arabellek, bölüm 3.3.5.4’te belirtilen GSS protokolü tarafından üretilen bir `token` içermelidir (`SHOULD`). `SecurityBufferLength` 0 ise, bu alan boştur ve sunucu tarafından başlatılan SPNEGO kimlik doğrulaması yerine, [MS-AUTHSOD] bölüm 2.1.2.2’de açıklandığı şekilde, istemci tarafından başlatılan ve kimlik doğrulama protokolü istemcinin seçimine bırakılan bir kimlik doğrulama kullanılacaktır.

Genel olarak SMB spesifikasyonu, değişken uzunluklu verileri hep bu şekilde ele alır: verinin kendisinin boyutunu ve konumunu gösteren, sabit konumlu uzunluk ve ofset alanları. Bu durum sadece yanıt mesajlarına veya Negotiate mesajına özgü değildir; çoğu zaman tek bir mesaj içinde bu deseni kullanan birden fazla alan bulursunuz. Aslında, değişken uzunluklu bir alan gördüğünüz her seferinde bu deseni görürsünüz. Meta veriler, mesajı alan tarafa verinin nasıl bulunacağını ve çıkarılacağını açıkça tarif eder.

Bu faydalıdır, ancak kodlama (encoding) stratejinizi karmaşıklaştırır çünkü artık bir struct içindeki farklı alanlar arasında bir ilişkiyi korumanız gerekir. Örneğin, tüm mesajı tek seferde marshal edemezsiniz; çünkü bazı meta veri alanları — örneğin uzunluk ve ofset — verinin kendisi marshal edilene kadar veya ofset örneğinde olduğu gibi veriden önce gelen tüm alanlar marshal edilene kadar bilinmeyecektir.

### SMB Uygulamasını Anlama

Bu alt bölümün geri kalanı, geliştirdiğimiz SMB uygulamasıyla ilgili bazı çirkin ayrıntıları ele alır. Paketi kullanmak için bu bilgileri anlamanız gerekmez.

Referans verileri ele almak için çeşitli yaklaşımlar denedik ve sonunda struct alan etiketleri (field tags) ile reflection kombinasyonunu kullanan bir çözümde karar kıldık. Reflection, bir programın kendisini incelemesini sağlayan bir tekniktir; özellikle kendi veri tiplerine bakmasına olanak tanır. Alan etiketleri ise reflection ile bağlantılıdır; çünkü bir struct alanı hakkında keyfî meta veri tanımlarlar. Bunları önceki XML, MSGPACK veya JSON kodlama örneklerinden hatırlıyor olabilirsiniz. Örneğin, Liste 6-5, JSON alan adlarını tanımlamak için struct etiketleri kullanır.

```go
type Foo struct {
    A int    'json:"a"'
    B string 'json:"b"'
```

**Liste 6-5: JSON alan adlarını tanımlayan bir struct**

Go’nun `reflect` paketi, veri tiplerini incelemek ve alan etiketlerini çıkarmak için kullandığımız fonksiyonları içerir. Bu noktadan sonra etiketleri ayrıştırmak (parse) ve değerleriyle anlamlı bir şeyler yapmak söz konusuydu. Liste 6-6’da, SMB paketinde tanımlı bir struct görebilirsiniz.

```go
type NegotiateRes struct {
    Header
    StructureSize        uint16
    SecurityMode         uinti6
    DialectRevision      uinti6
    Reserved             uinti6
    ServerGuid           []byte ' smb:"fixed:16"" 0
    Capabilities         uint32
    MaxTransactSize      uint32
    MaxReadSize          uint32
    MaxWriteSize         uint32
    SystemTime           uint64
    ServerStartTime      uint64
    SecurityBufferOffset uint16 'smb:"offset:SecurityBlob""
    SecurityBufferLength uinti6 'smb:"len:SecurityBlob" - 0
    Reserved2            uint32
    SecurityBlob         *gss.NegTokenInit
```

**Liste 6-6: Alan meta verilerini tanımlamak için SMB alan etiketlerinin kullanımı (`ch-6/smb/smb.go`)**

Bu tip, SMB anahtarıyla tanımlanan üç alan etiketi kullanır: `fixed`, `offset` ve `len`. Tüm bu adları keyfî olarak seçtiğimizi aklınızda bulundurun; belirli bir adı kullanmak zorunda değilsiniz. Her bir etiketin amacı şu şekildedir:

- **fixed** bir `[]byte` alanını, verilen boyutta sabit uzunluklu bir alan olarak tanımlar. Bu durumda `ServerGuid` 16 bayt uzunluğundadır.
- **offset**, struct’ın başlangıcından, değişken uzunluklu veri arabelleğinin ilk konumuna kadar olan bayt sayısını tanımlar. Etiket, ofsetin ilişkili olduğu alanın adını belirtir — bu örnekte `SecurityBlob`. Bu adla anılan bir alanın aynı struct içinde mevcut olması beklenir.
- **len**, değişken uzunluklu veri arabelleğinin uzunluğunu tanımlar. Etiket, uzunluğun ilişkili olduğu alanın adını belirtir — yine bu örnekte `SecurityBlob`. Bu adla anılan bir alanın aynı struct içinde mevcut olması gerekir.

Fark etmiş olabileceğiniz gibi, etiketlerimiz sadece farklı alanlar arasında keyfî meta veriler yoluyla ilişkiler kurmamıza izin vermekle kalmaz; sabit uzunluklu bayt dilimlerini (byte slice) değişken uzunluklu veriden ayırt etmemize de yardımcı olur. Ne yazık ki bu struct etiketlerini eklemek sorunu sihirli bir şekilde çözmez. Kodun, bu etiketleri arayacak ve marshal/unmarshal sırasında onlar üzerinde belirli işlemler yapacak mantığa sahip olması gerekir.

### Etiketleri Ayrıştırma ve Saklama

Liste 6-7’de, `parseTags()` adlı yardımcı fonksiyon, etiket ayrıştırma mantığını gerçekleştirir ve verileri `TagMap` tipinde bir yardımcı struct içinde saklar.
