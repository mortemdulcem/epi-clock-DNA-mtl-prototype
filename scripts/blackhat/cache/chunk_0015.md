```go
for i :=o; I < 1024; 1++ {
   port := <-results
   If port I= 0 {
       openports = append(openports, port)

1
close(ports)
close(results)
sort.Ints(openports)
for _, port := range openports f
     fmt.Printf("%d open\n", port)
```

**Liste 2-8: Birden fazla kanal ile port tarama (`ch-2/tcp-scanner-final/main.go`)**

`worker(ports, results chan int)` fonksiyonu iki kanal kabul edecek şekilde değiştirilmiştir; geri kalan mantık büyük ölçüde aynıdır, yalnızca port kapalıysa `0` gönderecek, açıksa portun kendisini göndereceksiniz. Ayrıca, işçiden (worker) ana iş parçacığına/goroutine’e sonuçları iletmek için ayrı bir kanal oluşturursunuz. Daha sonra sonuçları daha sonra sıralayabilmek için bir `slice`’ta saklarsınız. Sonraki adımda, işçilere göndermeyi ayrı bir goroutine içinde yapmanız gerekir; çünkü sonuç toplama döngüsünün, 100’den fazla iş devam edemeden önce başlaması gerekir.

Sonuç toplama döngüsü `results` kanalından 1024 kez alım yapar. Port `0`’a eşit değilse `slice`’a eklenir. Kanalları kapattıktan sonra, açık portlardan oluşan `slice`’ı sıralamak için `sort` kullanırsınız. Geriye kalan tek şey, `slice` üzerinde döngü kurup açık portları ekrana yazdırmaktır.

Böylece, oldukça verimli bir port tarayıcı elde etmiş oldunuz. Özellikle işçi (worker) sayısıyla oynayarak kodla biraz vakit geçirin. Sayı arttıkça, programınız daha hızlı çalışmalıdır. Ancak çok fazla işçi eklerseniz sonuçlar güvenilmez hale gelebilir. Başkalarının kullanması için araçlar yazarken, hızdan çok güvenilirliğe öncelik veren, makul bir varsayılan değer kullanmak isteyeceksiniz. Bununla birlikte, kullanıcıların işçi sayısını bir seçenek olarak belirleyebilmesine de izin vermelisiniz.

TCP, Scanners, and Proxies   31

Bu programa birkaç iyileştirme ekleyebilirsiniz. İlk olarak, taranan her port için `results` kanalına gönderim yapıyorsunuz ve bu her zaman gerekli değil. Alternatif çözüm, yalnızca işçileri takip etmek için değil, aynı zamanda toplanan tüm sonuçların tamamlandığından emin olarak bir yarış durumunu (race condition) engellemek için ek bir kanal kullandığından, biraz daha karmaşık bir kod gerektirir. Bu giriş niteliğindeki bölümde bunu bilerek dışarıda bıraktık; ama merak etmeyin! Bu deseni Bölüm 3’te tanıtacağız. İkinci olarak, tarayıcınızın port dizgelerini (port-strings) ayrıştırabilmesini isteyebilirsiniz; örneğin Nmap’e verilebilen `80,443,8080,21-25` gibi. Bunun bir uygulamasını görmek istiyorsanız `https://github.com/blackhat-go/bhg/blob/master/ch-2/scanner-portformat` adresine bakın. Bunu keşfetmeyi size bir alıştırma olarak bırakıyoruz.

## Bir TCP Proxy’si Oluşturmak

Tüm TCP tabanlı haberleşmeleri Go’nun yerleşik `net` paketini kullanarak gerçekleştirebilirsiniz. Bir önceki bölüm, `net` paketini esas olarak bir istemci bakış açısından kullanmaya odaklanıyordu; bu bölümde ise TCP sunucuları oluşturmak ve veri aktarmak için kullanacaksınız. Bu yolculuğa gerekli `echo` sunucusunu inşa ederek başlayacaksınız — istemciye verilen yanıtı olduğu gibi geri yansıtan bir sunucu — ve bunu, çok daha genel amaçlı iki program takip edecek: Bir TCP port yönlendirici (port forwarder) ve Netcat’in uzak komut çalıştırma için kullanılan “gaping security hole” özelliğinin yeniden yaratılması.

### `io.Reader` ve `io.Writer` Kullanımı

Bu bölümdeki örnekleri oluşturmak için, TCP, HTTP, dosya sistemi ya da başka bir yol kullanıyor olun, hemen hemen tüm girdi/çıktı (I/O) görevleri için kritik olan iki önemli türü kullanmanız gerekir: `io.Reader` ve `io.Writer`. Go’nun yerleşik `io` paketinin parçası olan bu türler, yerel veya ağ üzerinden tüm veri iletiminin temelini oluşturur. Bu türler Go dokümantasyonunda şu şekilde tanımlanır:

```go
type Reader interface {
    Read(p []byte) (n int, err error)

type Writer interface {
    Write(p []byte) (n int, err error)
```

Her iki tür de birer arayüz (interface) olarak tanımlanmıştır; bu, doğrudan örneklenemeyecekleri anlamına gelir. Her tür, tek bir dışa açılmış fonksiyonun tanımını içerir: `Read` veya `Write`. Bölüm 1’de açıklandığı gibi, bu fonksiyonları, bir türün `Reader` veya `Writer` olarak kabul edilebilmesi için üzerinde uygulanması gereken soyut metotlar olarak düşünebilirsiniz. Örneğin, aşağıdaki yapay (contrived) tür bu sözleşmeyi yerine getirir ve bir `Reader` kabul edilen her yerde kullanılabilir:

```go
type FooReader struct {}
func (fooReader *FooReader) Read(p []byte) (int, error) {
    // Read some data from somewhere, anywhere.
    return len(dataReadFromSomewhere), nil
```

Aynı fikir `Writer` arayüzü için de geçerlidir:

```go
type FooWriter struct {}
func (fooWriter *FooWriter) Write(p []byte) (int, error) {
    // Write data somewhere.
    return len(dataWrittenSomewhere), nil
}
```

Şimdi bu bilgiyi alıp yarı kullanışlı bir şey oluşturalım: `stdin` ve `stdout`’u saran özel bir `Reader` ve `Writer`. Bu kod biraz yapay çünkü Go’nun `os.Stdin` ve `os.Stdout` türleri zaten `Reader` ve `Writer` gibi davranır; ama arada sırada tekerleği yeniden icat etmeseydiniz bir şey öğrenemezdiniz, değil mi?

Liste 2-9’da tam bir uygulama gösterilmiştir; ardından bir açıklama gelmektedir.

```go
package main

import (
   "fmt"
   "log"

// FooReader defines an io.Reader to read from stdin.
type FooReader struct{}

// Read reads data from stdin.
func (fooReader *FooReader) Read(b []byte) (int, error) {
    fmt.Print("in > ")
    return os.Stdin.Read(b)0

// FooWriter defines an io.Writer to write to Stdout.
type FooWriter structa

// Write writes data to Stdout.
func (fooWriter *FooWriter) Write(b [}byte) (int, error) {
    fmt.Print("out> ")
    return os.Stdout.Write(b)0

func main() {
    // Instantiate reader and writer.
    var (
        reader FooReader
        writer FooWriter

    // Create buffer to hold input/output.
    input := make([]byte, 4096)
```

TCP, Scanners, and Proxies   33

```go
    // Use reader to read input.
    s, err := reader.Read(input)0
    if err I= nil {
        log.Fatalln("Unable to read data")

    fmt.Printf("Read %d bytes from stdin\n", s)

    // Use writer to write output.
    s, err = writer.Write(input)e
    if err I= nil {
        log.Fatalln("Unable to write data")

    fmt.Printf("Wrote %d bytes to stdout\n", s)
```
