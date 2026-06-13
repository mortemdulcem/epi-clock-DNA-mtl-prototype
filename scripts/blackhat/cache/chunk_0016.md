Liste 2-9: Bir reader ve writer gösterimi (`/ch-2/io-example/main.go`)

Kod iki özel tür tanımlar: `FooReader` ve `FooWriter`. Her bir tür üzerinde, `FooReader` için `Read([]byte)` fonksiyonunun ve `FooWriter` için `Write([]byte)` fonksiyonunun somut (concrete) bir uygulamasını tanımlarsınız. Bu durumda, her iki fonksiyon da `stdin` üzerinden okuma ve `stdout` üzerinde yazma işlemi yapmaktadır.

`FooReader` ve `os.Stdin` üzerindeki `Read` fonksiyonlarının, veri uzunluğunu ve olası hataları döndürdüğüne dikkat edin. Verinin kendisi, fonksiyona geçirilen byte slice’ına kopyalanır. Bu, bu bölümde daha önce verilen `Reader` arayüzü (interface) prototip tanımıyla tutarlıdır. `main()` fonksiyonu bu slice’ı (adı `input`) oluşturur ve ardından `FooReader.Read([]byte)` ve `FooWriter.Write([]byte)` çağrılarında kullanır.

Programın örnek bir çalıştırması aşağıdaki çıktıyı üretir:

```bash
$ go run main.go
in > hello world!!!
Read 15 bytes from stdin
out> hello world!!!
Wrote 4096 bytes to stdout
```

Bir `Reader`’dan bir `Writer`’a veri kopyalamak oldukça yaygın bir desendir; o kadar ki Go’nun `io` paketinde, `main()` fonksiyonunu basitleştirmek için kullanılabilecek bir `Copy()` fonksiyonu bulunur. Fonksiyon prototipi aşağıdaki gibidir:

```go
func Copy(dst io.Writer, src io.Reader) (written int64, err error)
```

Bu yardımcı (convenience) fonksiyon, öncekiyle aynı programatik davranışı, `main()` fonksiyonunuzu Liste 2-10’daki kodla değiştirerek elde etmenizi sağlar.

```go
func main() {
    var (
        reader FooReader
        writer FooWriter
    )

    if _, err := io.Copy(writer, reader); err != nil {
        log.Fatalln("Unable to read/write data")
    }
}
```

Liste 2-10: `io.Copy` kullanımı (`/ch-2/copy-example/main.go`)

`reader.Read([]byte)` ve `writer.Write([]byte)` için yapılan açık (explicit) çağrıların, `io.Copy(writer, reader)` fonksiyonuna yapılan tek bir çağrı ile değiştirildiğine dikkat edin. Arka planda `io.Copy(writer, reader)`, verilen reader üzerinde `Read([]byte)` fonksiyonunu çağırır ve böylece `FooReader`’ın `stdin` üzerinden okuma yapmasını tetikler. Ardından `io.Copy(writer, reader)`, verilen writer üzerinde `Write([]byte)` fonksiyonunu çağırır ve bu da `FooWriter`’ınızın veriyi `stdout`’a yazmasına yol açar. Özetle `io.Copy(writer, reader)`, tüm küçük ayrıntılarla uğraşmadan sıralı okuma-sonra-yazma sürecini yönetir.

Bu giriş bölümü, Go’nun G/Ç (I/O) ve arayüzlerine (interfaces) kapsamlı bir bakış sunmaktan uzaktır. Standart Go paketlerinin bir parçası olarak pek çok yardımcı fonksiyon ve özel (custom) reader ve writer mevcuttur. Çoğu durumda, Go’nun standart paketleri, en yaygın görevleri gerçekleştirmek için gerekli tüm temel uygulamaları içerir. Sonraki bölümde, bu temelleri TCP haberleşmesine nasıl uygulayacağınızı, sonunda size bahşedilen gücü kullanarak gerçek hayatta kullanılabilir araçlar geliştirmeyi inceleyeceğiz.

## Echo Sunucusunu Oluşturma

Çoğu programlama dilinde olduğu gibi, bir soketten (socket) veri okumayı ve yazmayı öğrenmek için bir echo sunucusu inşa ederek başlayacaksınız. Bunu yapmak için, bir port tarayıcı (port scanner) inşa ederken tanıttığımız, Go’nun akış yönelimli (stream-oriented) ağ bağlantısı `net.Conn`’u kullanacaksınız. Go’nun bu veri türüne ilişkin dokümantasyonuna göre, `Conn`, `Reader` ve `Writer` arayüzleri için tanımlandığı şekilde `Read([]byte)` ve `Write([]byte)` fonksiyonlarını uygular. Dolayısıyla `Conn`, hem bir `Reader` hem de bir `Writer`’dır (evet, bu mümkündür). Bu mantıksal olarak anlamlıdır; çünkü TCP bağlantıları çift yönlüdür (bidirectional) ve veri göndermek (write) ya da almak (read) için kullanılabilirler.

Bir `Conn` örneği (instance) oluşturduktan sonra, bir TCP soketi üzerinden veri gönderip alabileceksiniz. Ancak bir TCP sunucusu, bağlantıyı kendiliğinden üretemez; bir istemci (client) bir bağlantı kurmak zorundadır. Go’da, belirli bir portta TCP listener açmak için önce `net.Listen(network, address string)` fonksiyonunu kullanabilirsiniz. Bir istemci bağlandığında, `Accept()` metodu bir `Conn` nesnesi oluşturur ve döndürür; bu nesneyi veri almak ve göndermek için kullanabilirsiniz.

Liste 2-11, sunucu uygulamasının eksiksiz bir örneğini göstermektedir. Açıklık için satır içi yorumlar ekledik. Kodun tamamını şu anda anlamak için endişelenmeyin, çünkü kısa süre içinde parçalarına ayıracağız.

```go
package main

import (
    "log"
    "net"
)
```

```go
// echo is a handler function that simply echoes received data.
func echo(conn net.Conn) {
    defer conn.Close()

    // Create a buffer to store received data.
    b := make([]byte, 512)
    for {
        // Receive data via conn.Read into a buffer.
        size, err := conn.Read(b[0:])
        if err == io.EOF {
            log.Println("Client disconnected")
            break
        }
        if err != nil {
            log.Println("Unexpected error")
            break
        }
        log.Printf("Received %d bytes: %s\n", size, string(b))

        // Send data via conn.Write.
        log.Println("Writing data")
        if _, err := conn.Write(b[0:size]); err != nil {
            log.Fatalln("Unable to write data")
        }
    }
}
```

```go
func main() {
    // Bind to TCP port 20080 on all interfaces.
    listener, err := net.Listen("tcp", ":20080")
    if err != nil {
        log.Fatalln("Unable to bind to port")
    }
    log.Println("Listening on 0.0.0.0:20080")
    for {
        // Wait for connection. Create net.Conn on connection established.
        conn, err := listener.Accept()
        log.Println("Received connection")
        if err != nil {
            log.Fatalln("Unable to accept connection")
        }

        // Handle the connection. Using goroutine for concurrency.
        go echo(conn)
    }
}
```

Liste 2-11: Temel bir echo sunucusu (`/ch-2/echo-server/main.go`)
