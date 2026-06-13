Bu yapılandırma, yetkili istemci havuzunuzu tanımlar ve istemcilerin, devam etmelerine izin verilmeden önce kendilerini düzgün şekilde tanımlamalarını zorunlu kılar. `tlsConf.BuildNameToCertificate()` çağrısı yaparsınız; böylece istemcinin common name ve subject alternative name alanları—sertifikanın üretildiği alan adları—doğru şekilde ilgili sertifikaya eşlenir ➀. HTTP sunucunuzu tanımlar, özel olarak kendi yapılandırmanızı ➁ ayarlarsınız ve daha önce oluşturduğunuz sunucu sertifikası ile özel anahtar dosyalarını ➂ `server.ListenAndServeTLS()` fonksiyonuna geçirerek sunucuyu başlatırsınız. Sunucu kodunda istemcinin özel anahtar dosyasını hiçbir yerde kullanmadığınıza dikkat edin. Daha önce söylediğimiz gibi, özel anahtar özel kalır; sunucunuz, istemciyi yalnızca istemcinin genel anahtarını kullanarak tanımlayabilir ve yetkilendirebilir. Bu, açık anahtar kriptografisinin parlak tarafıdır.

Sunucunuzu `curl` kullanarak doğrulayabilirsiniz. Eğer sahte ve yetkisiz bir istemci sertifikası ve anahtarı üretip sağlarsanız, size bunu söyleyen ayrıntılı bir mesajla karşılanırsınız:

```bash
$ curl -ik -X GET --cert badCrt.pem --key badKey.pem \
  https://server.blackhat-go.local:9443/hello
curl: (35) gnutls_handshake() failed: Certificate is bad
```

Sunucu tarafında da buna benzer daha ayrıntılı bir mesaj alırsınız:

```text
http: TLS handshake error from 127.0.0.1:61682: remote error: tls: unknown certificate authority
```

Öte yandan, sunucu havuzunda yapılandırılmış sertifikayla eşleşen geçerli sertifika ve anahtarı sağlarsanız, başarılı biçimde kimlik doğrulandığında küçük bir zafer anı yaşarsınız:

```bash
$ curl -ik -X GET --cert clientCrt.pem --key clientKey.pem \
  https://server.blackhat-go.local:9443/hello
HTTP/1.1 200 OK
Date: Fri, 09 Oct 2020 16:55:52 GMT
Content-Length: 25
Content-Type: text/plain; charset=utf-8

Authentication successful
```

Bu mesaj, sunucunun beklendiği gibi çalıştığını söyler.

Şimdi bir de istemciye bakalım (Liste 11-7). İstemciyi sunucuyla aynı sistemde ya da farklı bir sistemde çalıştırabilirsiniz. Farklı bir sistemdeyse, `clientCrt.pem` dosyasını sunucuya ve `serverCrt.pem` dosyasını istemciye aktarmanız gerekir.

```go
func main() {
    var (
        err              error
        cert             tls.Certificate
        serverCert, body []byte
        pool             *x509.CertPool
        tlsConf          *tls.Config
        transport        *http.Transport
        client           *http.Client
        resp             *http.Response
    )

    if cert, err = tls.LoadX509KeyPair("clientCrt.pem", "clientKey.pem"); err != nil { // istemci sertifikası ve anahtarını yükle
        log.Fatalln(err)
    }

    if serverCert, err = ioutil.ReadFile("../server/serverCrt.pem"); err != nil { // sunucu sertifikasını oku
        log.Fatalln(err)
    }

    pool = x509.NewCertPool()
    pool.AppendCertsFromPEM(serverCert)

    tlsConf = &tls.Config{
        Certificates: []tls.Certificate{cert},
        RootCAs:      pool,
    }

    tlsConf.BuildNameToCertificate()

    transport = &http.Transport{
        TLSClientConfig: tlsConf,
    }

    client = &http.Client{
        Transport: transport,
    }

    if resp, err = client.Get("https://server.blackhat-go.local:9443/hello"); err != nil { // GET isteği gönder
        log.Fatalln(err)
    }

    if body, err = ioutil.ReadAll(resp.Body); err != nil {
        log.Fatalln(err)
    }

    defer resp.Body.Close()

    fmt.Printf("Success: %s\n", body)
}
```

**Liste 11-7** Karşılıklı kimlik doğrulama istemcisi (`ch-11/mutual-auth/cmd/client/main.go`)

Sertifika hazırlama ve yapılandırmanın büyük kısmı, sunucu kodunda yaptıklarınıza benzeyecek: sertifika havuzu oluşturma ve subject/common name alanlarını hazırlama. İstemci sertifikası ve anahtarını bir sunucu olarak kullanmayacağınız için, bunun yerine `tls.LoadX509KeyPair("clientCrt.pem", "clientKey.pem")` çağrısıyla bunları daha sonra kullanılmak üzere yüklersiniz ➀. Sunucu sertifikasını da okur, izin vermek istediğiniz sertifikalar havuzuna eklersiniz ➁. Ardından TLS yapılandırmanızı oluşturmak için sertifika havuzunu ve istemci sertifikalarını ➂ kullanır ➃ ve alan adlarını ilgili sertifikalarına bağlamak için `tlsConf.BuildNameToCertificate()` çağrısı yaparsınız ➄.

Bir HTTP istemcisi oluşturduğunuzdan, TLS yapılandırmanızla ilişkili bir `transport` ➅ tanımlamanız gerekir. Bu `transport` örneğini kullanarak bir `http.Client` struct’ı ➆ oluşturabilirsiniz. Bölüm 3 ve 4’te tartıştığımız gibi, bu istemciyi `client.Get("https://server.blackhat-go.local:9443/hello")` ➇ çağrısı ile bir HTTP GET isteği göndermek için kullanabilirsiniz.

Buradan sonra tüm sihir perde arkasında gerçekleşir. Karşılıklı kimlik doğrulama yapılır—istemci ve sunucu birbirlerini karşılıklı olarak doğrular. Kimlik doğrulama başarısız olursa, program bir hata döndürür ve çıkar. Aksi halde, HTTP yanıt gövdesini okur ve `stdout`’a yazdırırsınız ➈. İstemci kodunuzu çalıştırmak, beklendiği sonucu üretir; özellikle, hiçbir hata atılmadığını ve kimlik doğrulamanın başarılı olduğunu gösterir:

```bash
$ go run main.go
Success: Authentication successful
```

Sunucu çıktısı aşağıda gösterilmiştir. Sunucuyu, standart çıktıya bir selam (hello) mesajı yazacak şekilde yapılandırdığınızı hatırlayın. Bu mesaj, sertifikadan çıkarılan bağlanan istemcinin common name değerini içerir:

```bash
$ go run main.go
Hello: client.blackhat-go.local
```
