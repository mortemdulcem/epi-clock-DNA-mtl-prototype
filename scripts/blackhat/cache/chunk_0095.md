## Şifreleme ve İmza Doğrulama

Bu ilk örnekte, bir mesajı şifrelemek ve şifresini çözmek için açık anahtarlı kripto (public-key crypto) kullanacaksın. Ayrıca, bir mesajı imzalamak ve bu imzayı doğrulamak için gerekli mantığı da oluşturacaksın. Basitlik adına, tüm bu mantığı tek bir `main()` fonksiyonu içinde toplayacaksın. Bu, asıl amaç olan çekirdek işlevsellik ve mantığı göstermek için; böylece sen bunu istediğin şekilde uygulayabilirsin. Gerçek dünyada süreç biraz daha karmaşıktır, çünkü muhtemelen birbirleriyle iletişim kuran iki uzak düğüm (node) olacaktır. Bu düğümlerin açık anahtarları birbirleriyle paylaşması gerekir. Neyse ki, bu değiş-tokuş süreci, aşağıdakiyle aynı güvenlik güvencelerini gerektirmez.  

1. Galois/Counter Mode (GCM) gibi bazı çalışma kipleri, bütünlük güvencesi sağlar.

---

Şifre: 68941bf95bbc12edc12be369f3fd0463497a1220d9a6ab741cf9223c6793  
--snip--  
İmza doğrulandı

Sırada, açık anahtarlı kriptografinin başka bir uygulamasına bakalım: karşılıklı kimlik doğrulama.

## Karşılıklı Kimlik Doğrulama (Mutual Authentication)

Karşılıklı kimlik doğrulama, bir istemci ve sunucunun birbirlerini doğruladığı süreçtir. Bunu açık anahtarlı kriptografi ile yaparlar; hem istemci hem sunucu birer açık/özel anahtar çifti üretir, açık anahtarlarını değiş tokuş eder ve diğer uç noktanın kimliğinin ve özgünlüğünün (authenticity) doğruluğunu test etmek için bu açık anahtarları kullanırlar.  

Bu işi başarabilmek için, hem istemci hem sunucunun yetkilendirmeyi kurmak adına biraz hazırlık yapması gerekir; diğerini doğrulamak için kullanmayı planladıkları açık anahtar değerini açıkça tanımlamalıdırlar. Bu sürecin dezavantajı, her bir düğüm için benzersiz anahtar çiftleri oluşturma zorunluluğunun ve sunucu ile istemci düğümlerin düzgün çalışmak için ihtiyaç duydukları verilerin uygun şekilde sağlandığından emin olma işinin getirdiği idari (administrative) ek yüktür.  

Başlamak için, anahtar çiftleri oluşturma gibi idari görevleri aradan çıkaracaksın. Açık anahtarları, kendinden imzalı (self-signed), PEM kodlu sertifikalar olarak saklayacaksın. Bu dosyaları oluşturmak için `openssl` aracını kullanalım. Sunucunda, aşağıdaki komutu girerek sunucunun özel anahtarını ve sertifikasını oluşturacaksın:

```bash
$ openssl req -nodes -x509 -newkey rsa:4096 -keyout serverKey.pem -out serverCrt.pem -days 365
```

`openssl` komutu senden çeşitli girdiler isteyecek; bu örnek için bunlara rastgele değerler verebilirsin. Komut, `serverKey.pem` ve `serverCrt.pem` olmak üzere iki dosya oluşturur. `serverKey.pem` dosyası özel anahtarını içerir ve bunu korumalısın. `serverCrt.pem` dosyası ise sunucunun açık anahtarını içerir; bu dosyayı bağlanan her bir istemciye dağıtacaksın.  

Bağlanan her istemci için, yukarıdaki komuta benzer bir komut çalıştıracaksın:

```bash
$ openssl req -nodes -X509 -newkey rsa:4096 -keyout clientKey.pem -out clientCrt.pem -days 365
```

Bu komut da `clientKey.pem` ve `clientCrt.pem` olmak üzere iki dosya üretir. Sunucu çıktısında olduğu gibi, istemcinin özel anahtarını korumalısın. `clientCrt.pem` sertifika dosyası sunucuna aktarılacak ve programın tarafından yüklenecektir. Bu, istemciyi yetkili bir uç nokta (endpoint) olarak yapılandırmanı ve tanımlamanı sağlar. Sunucunun her bir ek istemciyi tanıyabilmesi ve açıkça yetkilendirebilmesi için, her istemciye ait sertifikayı oluşturman, aktarman ve yapılandırman gerekir.  

Liste 11-6'da, bir istemcinin geçerli ve yetkilendirilmiş bir sertifika sağlamasını gerektiren bir HTTPS sunucusu kuruyorsun.

```go
func helloHandler(w http.ResponseWriter, r *http.Request)     0
    fmt.Printf("Hello: Zs\n", r.TB.PeerCertificates[0].Subject.CommonName) 0
    fmt.Fprint(w, "Authentication successful")
```

```go
func main()
    var (
        err        error
        clientCert []byte
        pool       *x509.CertPool
        tlsConf    *tls.Config
        server     *http.Server

    http.HandleFunc("/hello", helloHandler)

    if clientCert, err = ioutil.ReadFile("../client/clientCrt.pem")0; err != nil
         log.Fatalln(err)

    pool = x509.NewCertPool()
    pool.AppendCertsFromPEM(clientCert) 0

    tIsConf = kls.Config{ 0
        ClientCAs: pool,
        ClientAuth: tls.RequireAndVerifyClientCert,

    tlsConf.BuildNameToCertificate()

    server = &http.Serverf
        Addr:      ":9443",
        TL5Config: tlsConf,
    1
    log.Fatalln(server.ListenAndServeTLS("serverCrt.pem", "serverKey.pem")0)
```

**Liste 11-6** Karşılıklı kimlik doğrulama sunucusunun kurulması (`ich-11/mutual-auth/cmd/server/main.go`)

`main()` fonksiyonu dışında, program bir `helloHandler()` fonksiyonu tanımlar 0. Bölüm 3 ve 4'te çok daha önce tartıştığımız gibi, bu handler fonksiyonu bir `http.ResponseWriter` örneği ve `http.Request` nesnesinin kendisini alır. Bu handler oldukça sıkıcıdır. Alınan istemci sertifikasının ortak adını (common name) loglar 0. Ortak ada, `http.Request` nesnesinin `TLS` alanını inceleyip sertifikadaki `PeerCertificates` verisine inerek erişilir. Handler fonksiyonu ayrıca istemciye kimlik doğrulamasının başarılı olduğunu belirten bir mesaj gönderir.  

Peki hangi istemcilerin yetkili olduğunu nasıl tanımlarsın ve onları nasıl doğrularsın? Süreç oldukça ağrısızdır. Önce, istemcinin sertifikasını daha önce istemci tarafından oluşturulmuş PEM dosyasından okursun 0. Birden fazla yetkili istemci sertifikasının olması mümkün olduğu için, bir sertifika havuzu (certificate pool) oluşturur ve `pool.AppendCertsFromPEM(clientCert)` çağrısı ile istemci sertifikasını havuzuna eklersin 0. Kimlik doğrulamak istediğin her ek istemci için bu adımı tekrar edersin.  

Sonraki adımda, TLS yapılandırmanı oluşturursun. `ClientCAs` alanını açıkça havuzuna ayarlarsın ve `ClientAuth` alanını `tls.RequireAndVerifyClientCert` olarak yapılandırırsın 0.
