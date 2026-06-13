### Bir TCP İstemcisini Proxy’lemek

Artık sağlam bir temele sahip olduğunuza göre, bu noktaya kadar öğrendiklerinizi kullanarak, bir ara servis veya konak (host) üzerinden bağlantıyı proxy’leyen basit bir port yönlendirici (port forwarder) oluşturabilirsiniz. Bu, bu bölümün başlarında da belirtildiği gibi, kısıtlayıcı çıkış (egress) kontrollerini aşmaya çalışırken veya ağ segmentasyonunu atlatmak için bir sistemi kullanmak istediğinizde faydalıdır.

Koda geçmeden önce, hayali ama gerçekçi bir problemi düşünün: Joe, ACME Inc.'de iş analisti olarak çalışan, performansı düşük bir çalışan; özgeçmişine eklediği hafif abartılar sayesinde gayet iyi bir maaş almaktadır. (Gerçekten Ivy League bir okulda mı okudu? Joe, bu pek etik değil.) Joe’nun motivasyon eksikliği, kedilere olan sevgisiyle yarışır durumda — o kadar ki, evine kedi kameraları kurmuş ve evdeki tüy yuvalarını uzaktan izleyebilmek için `joescatcam.website` adlı bir site barındırmaktadır. Ancak bir sorun vardır: ACME durumu fark etmiştir. Joe’nun 7/24 4K ultra yüksek çözünürlükte kedi kamerası yayını yaparak ACME’nin değerli ağ bant genişliğini tüketmesinden hoşlanmamaktadır. Hatta ACME, çalışanlarının Joe’nun kedi kamerası sitesine erişmesini engellemiştir.

Joe’nun aklına bir fikir gelir. “Kontrol ettiğim internet tabanlı bir sistemde bir port forwarder kurup,” der Joe, “o konaktan gelen tüm trafiği `joescatcam.website` adresine zorla yönlendirsem nasıl olur?” Joe, ertesi gün işteyken kontrol eder ve `joesproxy.com` alan adında barındırılan kişisel sitesine erişebildiğini doğrular. Öğleden sonraki toplantılarını eker, bir kahveciye gider ve sorununa hızlıca bir çözüm kodlar. `http://joesproxy.com` üzerinde alınan tüm trafiği `http://joescatcam.website` adresine iletecektir.

İşte Joe’nun `joesproxy.com` sunucusunda çalıştırdığı kod:

```go
func handle(src net.Conn) {
    dst, err := net.Dial("tcp", "joescatcam.website:80")
    if err != nil {
        log.Fatalln("Unable to connect to our unreachable host")
    }
    defer dst.Close()

    // io.Copy'nin bloklamasını önlemek için goroutine içinde çalıştır
    go func() {
        // Kaynağın çıktısını hedefe kopyala
        if _, err := io.Copy(dst, src); err != nil {
            log.Fatalln(err)
        }
    }()

    // Hedefin çıktısını tekrar kaynağa kopyala
    if _, err := io.Copy(src, dst); err != nil {
        log.Fatalln(err)
    }
}
```

```go
func main() {
    // Yerel 80 portunda dinle
    listener, err := net.Listen("tcp", ":80")
    if err != nil {
        log.Fatalln("Unable to bind to port")
    }

    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Fatalln("Unable to accept connection")
        }

        go handle(conn)
    }
}
```

Önce Joe’nun `handle(net.Conn)` fonksiyonunu inceleyin. Joe, `joescatcam.website` adresine bağlanır (bu erişilemeyen hedefin, Joe’nun kurumsal iş istasyonundan doğrudan erişilebilir olmadığını hatırlayın). Joe daha sonra `Copy(Writer, Reader)` fonksiyonunu iki kez kullanır. İlk kullanım, gelen bağlantıdan gelen verilerin `joescatcam.website` bağlantısına kopyalanmasını sağlar. İkinci kullanım, `joescatcam.website` üzerinden okunan verilerin, bağlanan istemcinin bağlantısına geri yazılmasını sağlar. `Copy(Writer, Reader)` fonksiyonu bloklayıcıdır ve ağ bağlantısı kapanana kadar yürütmeyi bloklamaya devam eder; bu nedenle Joe, ilk `Copy(Writer, Reader)` çağrısını yeni bir goroutine içinde çalıştırarak akıllıca davranır. Bu, `handle(net.Conn)` fonksiyonu içindeki yürütmenin devam etmesini ve ikinci `Copy(Writer, Reader)` çağrısının yapılabilmesini sağlar.

Joe’nun proxy’si 80 numaralı portta dinler ve bir bağlantıdan aldığı tüm trafiği `joescatcam.website` üzerindeki 80 numaralı porta iletir ve oradan geri döner. Joe, o çılgın ve müsrif adam, `joesproxy.com` üzerinden `joescatcam.website` adresine `curl` ile bağlanarak erişebildiğini doğrular:

```bash
$ curl -i -X GET http://joesproxy.com
HTTP/1.1 200 OK
Date: Wed, 25 Nov 2020 19:51:54 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Thu, 27 Jun 2019 15:30:43 GMT
ETag: "6d-519594e7f2d25"
Accept-Ranges: bytes
Content-Length: 109
Vary: Accept-Encoding
Content-Type: text/html
--snip--
```

Bu noktada Joe amacına ulaşmıştır. ACME sponsorlu zamanını ve ağ bant genişliğini kedilerini izleyerek boşa harcayarak hayallerini yaşamaktadır. Bugün, kedi günü!

### Komut Çalıştırma için Netcat’i Kopyalamak

Bu bölümde Netcat’in daha ilginç işlevlerinden bazılarını — özellikle de kocaman güvenlik açığını — kopyalayalım.

Netcat, TCP/IP’nin İsviçre çakısıdır; temelde Telnet’in daha esnek ve betiklenebilir bir sürümüdür. Herhangi bir rastgele programın stdin ve stdout’unun TCP üzerinden yeniden yönlendirilmesini sağlayan bir özelliğe sahiptir; bu da bir saldırganın, örneğin, tek bir komut çalıştırma zafiyetini işletim sistemi kabuğu (shell) erişimine dönüştürmesine olanak tanır. Şu komutu düşünün:

```bash
$ nc -lp 13337 -e /bin/bash
```

Bu komut, 13337 portunda dinleyen bir sunucu oluşturur. Uzakta herhangi bir istemci, örneğin Telnet ile bağlanarak, rastgele `bash` komutları çalıştırabilir — bu yüzden buna kocaman bir güvenlik açığı denir. Netcat, program derlemesi (build/compile) sırasında bu özelliği isteğe bağlı olarak eklemenize izin verir. (Haklı sebeplerle, standart Linux dağıtımlarında bulacağınız Netcat ikililerinin çoğu bu özelliği içermez.) Bu özellik o kadar tehlikelidir ki, size bunu Go ile nasıl oluşturacağınızı göstereceğiz!

Önce Go’nun `os/exec` paketine bakın. İşletim sistemi komutlarını çalıştırmak için bunu kullanacaksınız. Bu paket, komut çalıştırmak ve stdin ile stdout’u yönetmek için gerekli metot ve özellikleri içeren `Cmd` adlı bir tür tanımlar. `stdin` (bir `Reader`) ve `stdout` (bir `Writer`) akışlarını, hem `Reader` hem `Writer` olan bir `Conn` örneğine yönlendireceksiniz.

Yeni bir bağlantı aldığınızda, `os/exec` paketindeki `Command(name string, arg ...string)` fonksiyonunu kullanarak yeni bir `Cmd` örneği oluşturabilirsiniz. Bu fonksiyon, parametre olarak işletim sistemi komutunu ve argümanlarını alır. Bu örnekte, komut olarak `/bin/sh` değerini sabit kodlayın ve etkileşimli modda olabilmeniz için `-i` argümanını geçin; böylece stdin ve stdout’u daha güvenilir şekilde yönetebilirsiniz:

```go
cmd := exec.Command("/bin/sh", "-i")
```
