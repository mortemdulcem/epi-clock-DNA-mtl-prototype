### Arabellek Taşması (Buffer Overflow) Fuzzing

Arabellek taşmaları (buffer overflow), bir kullanıcı bir girdiye, uygulamanın ayırdığı bellek alanından daha fazla veri gönderdiğinde meydana gelir. Örneğin, uygulama yalnızca 5 karakter almayı beklerken bir kullanıcı 5.000 karakter gönderebilir. Bir program yanlış teknikler kullanıyorsa, bu durum kullanıcının bu fazla veriyi amaçlanmayan bellek bölgelerine yazmasına izin verebilir. Bu "taşma", bitişik bellek konumlarında saklanan verileri bozar ve kötü niyetli bir kullanıcının programı çökertmesine veya programın mantıksal akışını değiştirmesine olanak tanır.

Arabellek taşmaları, istemcilerden veri alan ağ tabanlı programlar için özellikle etkilidir. Bir istemci, arabellek taşmalarını kullanarak sunucu kullanılabilirliğini bozabilir veya muhtemelen uzaktan kod çalıştırma (remote code execution) elde edebilir. Tekrar vurgulamak gerekir: izin verilmedikçe sistemleri veya uygulamaları fuzz etmeyin. Ayrıca, sistemi veya servisi çökertmenin sonuçlarını tamamen anladığınızdan emin olun.

### Arabellek Taşması Fuzzing Nasıl Çalışır?

Bir arabellek taşması oluşturmak için fuzzing genellikle, her bir ardışık isteğin, önceki denemeden bir karakter daha uzun bir girdi içerdiği şekilde, gittikçe daha uzun girdiler göndermeyi içerir. Girdi olarak `A` karakterinin kullanıldığı yapay bir örnek, Tablo 9-1'de gösterilen desene göre çalışır.

Zafiyetli bir fonksiyona çok sayıda girdi göndererek, sonunda girdinizin uzunluğunun fonksiyonun tanımlı arabellek boyutunu aştığı bir noktaya ulaşırsınız; bu durum, dönüş işaretçileri ve komut işaretçileri (instruction pointer) gibi programın kontrol elemanlarını bozar. Bu noktada uygulama veya sistem çöker.

Her denemede kademeli olarak daha büyük istekler göndererek, beklenen girdi boyutunu hassas biçimde belirleyebilirsiniz; bu, uygulamayı daha sonra sömürmek (exploit) için önemlidir. Ardından, zafiyeti daha iyi anlamak ve çalışır bir exploit geliştirmeye çalışmak için çökme durumunu veya ortaya çıkan core dump dosyasını inceleyebilirsiniz. Burada hata ayıklayıcı (debugger) kullanımı ve exploit geliştirme konularına girmeyeceğiz; bunun yerine fuzzer yazmaya odaklanalım.

**Tablo 9-1: Bir Arabellek Taşması Testindeki Girdi Değerleri**

| Deneme | Girdi değeri        |
|--------|---------------------|
| 1      | A                   |
| 2      | AA                  |
| 3      | AAA                 |
| 4      | AAAA                |
| …      | A karakterinin N kez tekrarı |

Modern, yorumlamalı dillerle el ile fuzzing yaptıysanız, muhtemelen belirli uzunluklarda stringler oluşturmak için bir yapı kullanmışsınızdır. Örneğin, yorumlayıcı konsolda çalıştırılan aşağıdaki Python kodu, 25 adet `A` karakterinden oluşan bir string oluşturmanın ne kadar basit olduğunu gösterir:

```python
>>> x = "A" * 25
>>> x
'AAAAAAAAAAAAAAAAAAAAAAAAA'
```

Ne yazık ki Go'da, keyfi uzunlukta stringleri rahatça oluşturmak için böyle bir yapı yoktur. Bunu eski usul bir şekilde—bir döngü kullanarak—yapmanız gerekir; bu da aşağıdakine benzer görünecektir:

```go
var (
    n int
    s string
)

for n = 0; n < 25; n++ {
    s += "A"
}
```

Python alternatifine göre biraz daha ayrıntılı olsa da abartılacak kadar değil.

Dikkate almanız gereken diğer nokta, yük/faydalı yükünüzü (payload) iletme mekanizmasıdır. Bu, hedef uygulamaya veya sisteme bağlı olacaktır. Bazı durumlarda bu, diske bir dosya yazmayı içerebilir. Diğer durumlarda, HTTP, SMTP, SNMP, FTP, Telnet veya başka bir ağ servisiyle TCP/UDP üzerinden iletişim kurmanız gerekebilir.

Aşağıdaki örnekte, uzak bir FTP sunucusuna karşı fuzzing yapacaksınız. Sunulan mantığın önemli bir kısmını, diğer protokollere karşı çalışacak şekilde hızlıca uyarlayabilirsiniz; dolayısıyla bu, diğer servisler için özelleştirilmiş fuzzer'lar geliştirmeniz açısından iyi bir temel işlevi görmelidir.

Go'nun standart paketleri HTTP ve SMTP gibi bazı yaygın protokoller için destek içerse de, istemci-sunucu FTP etkileşimleri için destek içermez. Bunun yerine, tekerleği yeniden icat etmek zorunda kalmamak ve her şeyi sıfırdan yazmamak için FTP iletişimini halihazırda gerçekleştiren üçüncü taraf bir paket kullanabilirsiniz. Ancak, maksimum kontrol için (ve protokolü takdir etmek adına), temel FTP işlevselliğini ham TCP iletişimi kullanarak oluşturacaksınız. Bunun nasıl çalıştığına dair bir hatırlatmaya ihtiyacınız varsa Bölüm 2'ye bakın.

### Arabellek Taşması Fuzzer'ını Oluşturma

Liste 9-1 fuzzer kodunu göstermektedir. (Kök dizindeki tüm kod listeleri, sağlanan GitHub deposu `https://github.com/blackhat-go/bhg` altında `/` konumu altında bulunur.) Hedef IP ve port gibi bazı değerleri, ayrıca girdinizin maksimum uzunluğunu kodun içine sabit olarak yazdık (hardcode). Kodun kendisi `USER` özelliğini fuzz eder. Bu özellik bir kullanıcı kimlik doğrulanmadan önce kullanıldığından, saldırı yüzeyinde genellikle test edilebilir bir nokta temsil eder. Elbette bu kodu `PASS` gibi diğer kimlik doğrulama öncesi komutları test edecek şekilde genişletebilirsiniz; ancak geçerli bir kullanıcı adı sağlarsanız ve ardından `PASS` için girdi göndermeye devam ederseniz, sonunda kilitlenebileceğinizi (lock out) unutmayın.

```go
func main() {
    for i := 0; i < 2500; i++ {
        conn, err := net.Dial("tcp", "10.0.1.20:21")
        if err != nil {
            log.Fatalf("[!] Error at offset %d: %s\n", i, err)
        }

        bufio.NewReader(conn).ReadString('\n')

        user := ""
        for n := 0; n <= i; n++ {
            user += "A"
        }

        raw := "USER %s\n"
        fmt.Fprintf(conn, raw, user)
        bufio.NewReader(conn).ReadString('\n')

        raw = "PASS password\n"
        fmt.Fprint(conn, raw)
        bufio.NewReader(conn).ReadString('\n')

        if err := conn.Close(); err != nil {
            log.Printf("[!] Error at offset %d: %s\n", i, err)
        }
    }
}
```

**Liste 9-1: Bir arabellek taşması fuzzer'ı (`/ch-9/ftp-fuzz/main.go`)**
