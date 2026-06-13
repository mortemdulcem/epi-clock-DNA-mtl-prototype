Liste 2-11, parametre olarak bir Conn örneği kabul eden `echo(net.Conn)` adlı bir fonksiyon tanımlayarak başlar. Bu fonksiyon, gerekli tüm G/Ç işlemlerini gerçekleştiren bir bağlantı işleyicisi (handler) gibi davranır. Fonksiyon, bağlantıdan veri okuyup yazmak için bir arabellek (buffer) kullanarak sonsuz döngü içinde çalışır; veriler `b` adlı bir değişkene okunur ve ardından tekrar bağlantıya yazılır.

Artık işleyicini çağıracak bir dinleyici (listener) kurman gerekiyor. Daha önce bahsedildiği gibi, bir sunucu bağlantıyı kendiliğinden oluşturamaz; bunun yerine bir istemcinin bağlanmasını beklemek üzere dinleme yapmalıdır. Bu nedenle, `net.Listen(network, address string)` fonksiyonu kullanılarak, tüm arayüzlerde 20080 portuna bağlı TCP olarak tanımlanan bir dinleyici başlatılır.

Sonraki adımda, sonsuz bir döngü 0, bir bağlantı alındıktan sonra bile sunucunun bağlantı dinlemeye devam etmesini sağlar. Bu döngü içinde `listener.Accept()` 0 fonksiyonunu çağırırsın; bu fonksiyon istemci bağlantılarını beklerken yürütmeyi bloke eder. Bir istemci bağlandığında, bu fonksiyon bir Conn örneği döndürür. Bu bölümde daha önceki tartışmalardan hatırlarsan, Conn hem bir Reader hem de bir Writer’dır (Read([]byte) ve Write([]byte) arayüz fonksiyonlarını uygular).

Conn örneği daha sonra `echo(net.Conn)` işleyici fonksiyonuna 0 aktarılır. Bu çağrının başına `go` anahtar sözcüğü getirilmiştir; bu sayede fonksiyon çağrısı eşzamanlı (concurrent) hale gelir ve işleyici fonksiyonunun tamamlanmasını beklerken diğer bağlantılar bloke olmaz. Bu kadar basit bir sunucu için muhtemelen gereğinden fazla, fakat Go’nun eşzamanlılık (concurrency) modelinin ne kadar basit olduğunu göstermek için tekrar dahil ettik; hâlâ net değilse bile burada açıkça görülüyor. Bu noktada, eşzamanlı çalışan iki hafif iş parçacığın (lightweight thread/goroutine) olur:

- Ana iş parçacığı, başka bir bağlantı beklerken `listener.Accept()` üzerinde tekrar döngüye girer ve bloklanır.
- Çalışması `echo(net.Conn)` fonksiyonuna devredilmiş olan işleyici goroutine, çalışmaya devam eder ve veriyi işler.

Aşağıda, bağlanan istemci olarak Telnet kullanıldığında oluşan örnek bir çıktı gösterilmiştir:

```bash
$ telnet localhost 20080
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
test of the echo server
test of the echo server
```

Sunucu ise aşağıdaki standart çıktıyı üretir:

```bash
$ go run main.go
2020/01/01 06:22:09 Listening on 0.0.0.0:20080
2020/01/01 06:22:14 Received connection
2020/01/01 06:22:18 Received 25 bytes: test of the echo server
2020/01/01 06:22:18 Writing data
```

Devrim niteliğinde, değil mi? İstemcinin sunucuya gönderdiği veriyi, sunucunun bire bir aynen istemciye geri yolladığı bir sunucu. Ne kadar kullanışlı ve heyecan verici bir örnek! Yaşamak için gerçekten harika bir zaman.

## Kodu Geliştirerek Tamponlu (Buffered) Bir Dinleyici Oluşturmak

Liste 2-11’deki örnek gayet iyi çalışıyor, ancak oldukça düşük seviyeli fonksiyon çağrılarına, arabellek takibine ve tekrarlayan okuma/yazma işlemlerine dayanıyor. Bu, bir ölçüde sıkıcı ve hataya açık bir süreç. Neyse ki Go, bu süreci basitleştirecek ve kodun karmaşıklığını azaltacak başka paketler içeriyor.

Özellikle `bufio` paketi, Reader ve Writer’ı sarmalayarak tamponlu bir G/Ç (buffered I/O) mekanizması oluşturur. Güncellenmiş `echo(net.Conn)` fonksiyonu aşağıda verilmiştir; ardından değişikliklerin açıklaması yer almaktadır:

```go
func echo(conn net.Conn) {
    defer conn.Close()

    reader := bufio.NewReader(conn)
    s, err := reader.ReadString('\n')
    if err != nil {
        log.Fatalln("Unable to read data")
    }

    log.Printf("Read %d bytes: %s", len(s), s)

    log.Println("Writing data")
    writer := bufio.NewWriter(conn)
    if err := writer.WriteString(s); err != nil {
        log.Fatalln("Unable to write data")
    }

    writer.Flush()
}
```

Artık Conn örneği üzerinde doğrudan `Read([]byte)` ve `Write([]byte)` fonksiyonlarını çağırmıyorsun; bunun yerine, `NewReader(io.Reader)` 0 ve `NewWriter(io.Writer)` 0 aracılığıyla yeni bir tamponlu Reader ve Writer başlatıyorsun. Bu çağrıların her ikisi de parametre olarak mevcut bir Reader ve Writer alır (unutma, Conn tipi hem Reader hem de Writer olarak kabul edilmek için gerekli fonksiyonları uygular).

Her iki tamponlu örnek (buffered instance), string veriyi okumak ve yazmak için tamamlayıcı fonksiyonlar içerir. `ReadString(byte)` 0, ne kadar okunacağını belirlemek için bir ayırıcı (delimiter) karakter alır; `WriteString(byte)` 0 ise string’i sokete (socket) yazar. Veri yazarken, alttaki writer’a (bu örnekte bir Conn örneği) tüm veriyi yazdığından emin olmak için `writer.Flush()` 0 fonksiyonunu açıkça çağırman gerekir.

Önceki örnek tamponlu G/Ç kullanarak süreci basitleştiriyor olsa da, bunu `Copy(Writer, Reader)` yardımcı (convenience) fonksiyonunu kullanacak şekilde yeniden çerçeveleyebilirsin. Bu fonksiyonun girdi olarak bir hedef Writer ve bir kaynak Reader aldığını ve sadece kaynaktan hedefe veri kopyaladığını hatırla.

Bu örnekte, kurulmuş bağlantı üzerinden içeriği geri yankılayacağın için `conn` değişkenini hem kaynak hem de hedef olarak ileteceksin:

```go
func echo(conn net.Conn) {
    defer conn.Close()
    // Copy data from io.Reader to io.Writer via io.Copy().
    if _, err := io.Copy(conn, conn); err != nil {
        log.Fatalln("Unable to read/write data")
    }
}
```

G/Ç temellerini inceledin ve bunu TCP sunucularına uyguladın. Şimdi sırada daha kullanışlı ve ilgili örneklere geçmek var.
