İstemci sunucuya bir Negotiate Protocol isteği gönderir. Bu mesaj, istemcinin desteklediği diyalektlerin bir listesini içerir.  
Sunucu, seçtiği diyalekti belirten bir Negotiate Protocol yanıt mesajı ile cevap verir. Sonraki mesajlar bu diyalekti kullanacaktır. Yanıtın içinde, sunucunun desteklediği kimlik doğrulama mekanizmalarının bir listesi bulunur.  

İstemci, NTLMSSP gibi desteklenen bir kimlik doğrulama türü seçer ve bu bilgiyi kullanarak sunucuya bir Session Setup istek mesajı oluşturup gönderir. Mesaj, bunun bir NTLMSSP Negotiate isteği olduğunu belirten kapsüllenmiş bir güvenlik yapısı (security structure) içerir.  

Sunucu bir Session Setup yanıt mesajı ile cevap verir. Bu mesaj, daha fazla işlem gerektiğini belirtir ve bir sunucu challenge (meydan okuma) belirteci (token) içerir.  

İstemci, domain, kullanıcı ve parolayı girdi olarak kullanan kullanıcının NTLM karmasını (hash) hesaplar ve bunu, sunucu challenge’ı, rastgele istemci challenge’ı ve diğer veriler ile birlikte kullanarak challenge yanıtını üretir. Bu yanıtı, sunucuya gönderdiği yeni bir Session Setup istek mesajına dahil eder. 3. adımda gönderilen mesajdan farklı olarak, kapsüllenmiş güvenlik yapısı bunun bir NTLMSSP Authenticate isteği olduğunu belirtir. Böylece sunucu, iki farklı Session Setup SMB isteği arasında ayrım yapabilir.  

Sunucu, domain kimlik bilgilerini kullanarak kimlik doğrulaması için bir domain denetleyicisi (domain controller) gibi yetkili bir kaynakla etkileşime girer ve istemcinin sağladığı challenge–response bilgisini, yetkili kaynağın hesapladığı değerle karşılaştırır. Eğer eşleşirlerse, istemci kimliği doğrulanmış olur. Sunucu, oturum açmanın başarılı olduğunu belirten bir Session Setup yanıt mesajını istemciye gönderir. Bu mesaj, istemcinin oturum durumunu izlemek için kullanabileceği benzersiz bir oturum tanımlayıcısı (session identifier) içerir.  

İstemci, paylaşılan dosya alanlarına (file shares), adlandırılmış borulara (named pipes), yazıcılara vb. erişmek için ek mesajlar gönderir; her mesaj, sunucunun istemcinin kimlik doğrulama durumunu doğrulayabildiği bir referans olarak oturum tanımlayıcısını içerir.  

Burada SMB’nin ne kadar karmaşık olduğunu ve neden SMB spesifikasyonunu uygulayan ne standart bir Go paketi ne de üçüncü taraf bir paket bulunduğunu anlamaya başlayabilirsiniz. Kapsamlı bir yaklaşım benimseyip oluşturduğumuz kütüphanelerin her nüansını tartışmak yerine, iyi tanımlanmış ağ protokollerinin kendi sürümlerinizi uygulamanıza yardımcı olabilecek birkaç yapı, mesaj veya benzersiz yön üzerinde odaklanalım. Uzun uzun kod listeleri yerine, bu bölüm yalnızca işe yarar kısımları ele alacak ve sizi bilgi fazlalığından kurtaracak.  

Aşağıdaki ilgili spesifikasyonları referans olarak kullanabilirsiniz, ancak her birini okuma zorunluluğu hissetmeyin. Bir Google araması, en güncel sürümleri bulmanızı sağlayacaktır.

- **MS-SMB2**  
  Uymaya çalıştığımız SMB2 spesifikasyonu. Bu, esas dikkate alınan spesifikasyon olup kimlik doğrulama gerçekleştirmek için bir Generic Security Service Application Programming Interface (GSS-API) yapısını kapsüller.
- **MS-SPNG ve RFC 4178**  
  MS-NLMP verilerinin kapsüllendiği GSS-API spesifikasyonu. Yapı ASN.1 ile kodlanır.
- **MS-NLMP**  
  NTLMSSP kimlik doğrulama belirteci (token) yapısını ve challenge–response formatını anlamak için kullanılan spesifikasyon. NTLM karması (hash) ve kimlik doğrulama yanıt belirteci gibi şeylerin nasıl hesaplanacağına dair formüller ve ayrıntılar içerir. Dıştaki GSS-API konteynerinin aksine, NTLMSSP verisi ASN.1 ile kodlanmış değildir.
- **ASN.1**  
  Verinin ASN.1 biçimi kullanılarak kodlanmasına ilişkin spesifikasyon.

Paketten ilginç kod parçacıklarını tartışmadan önce, çalışan SMB iletişimi kurabilmek için aşmanız gereken bazı zorlukları anlamalısınız.

## Struct Alanlarının Karma (Mixed) Kodlanmasının Kullanılması

Daha önce ima ettiğimiz gibi, SMB spesifikasyonu mesaj verisinin büyük kısmı için konumsal, ikili (binary), little-endian, sabit ve değişken uzunluklu kodlama gerektirir. Ancak bazı alanların ASN.1 ile kodlanması gerekir; ASN.1, alan indeksi, türü ve uzunluğu için açıkça etiketlenmiş tanımlayıcılar kullanır. Bu durumda, kodlanacak ASN.1 alt alanlarının çoğu isteğe bağlıdır ve mesaj alanı içinde belirli bir konuma veya sıraya bağlı değildir. Bu örnek, zorluğu biraz daha somutlaştırmaya yardımcı olabilir.  

Liste 6-1’de, bu zorlukları barındıran varsayımsal bir `Message` struct’ı görebilirsiniz.

```go
type Foo struct {
    X int
      []byte

type Message struct {
    A int    // Binary, positional encoding
      Foo    // A94.1 encoding as required by spec
    C bool // Binary, positional encoding
1
```

**Liste 6-1: Değişken alan kodlamaları gerektiren varsayımsal bir struct örneği**

Buradaki temel sorun, `Message` struct’ı içindeki tüm türleri aynı kodlama şeması ile kodlayamamanızdır; çünkü `Foo` türündeki `B` alanının ASN.1 ile kodlanması beklenirken diğer alanlar için bu geçerli değildir.

## Özel Marshaling ve Unmarshaling Arayüzü Yazmak

Önceki bölümleri hatırlarsanız, JSON veya XML gibi kodlama şemaları, struct’ı ve tüm alanlarını aynı kodlama formatını kullanarak özyinelemeli (recursive) olarak kodlar. Bu yöntem temiz ve basitti. Burada aynı lükse sahip değilsiniz; çünkü Go’nun `binary` paketi de aynı şekilde davranır — tüm struct’ları ve struct alanlarını, umursamadan, özyinelemeli olarak kodlar; fakat mesaj, karma (mixed) kodlama gerektirdiği için bu yaklaşım sizin için işe yaramaz:

```go
binary.Write(someWriter, binary.LittleEndian, message)
```

Çözüm, keyfi türlerin özel marshaling ve unmarshaling mantığını tanımlamasına izin veren bir arayüz (interface) oluşturmaktır (Liste 6-2).

```go
0 type BinaryMarshallable interface f
      MarshalBinary(*Metadata) ([]byte, error)
      UnmarshalBinary([]byte, *Metadata) error
```

**Liste 6-2: Özel marshaling ve unmarshaling metodları gerektiren arayüz tanımı**
