104    Bölüm 5

Yeni bir `Msg{}` oluşturarak başlayın ve ardından `fqdn(string)` fonksiyonunu çağırarak alan adını bir DNS sunucusu ile değiş tokuş edilebilecek bir FQDN’e dönüştürün. Sonraki adımda, `SetQuestion(string, uint16)` fonksiyonunu çağırarak `Msg`’in iç durumunu değiştirin; burada bir A kaydı bakmak istediğinizi belirtmek için `TypeA` değerini kullanın. (`TypeA`, package içinde tanımlı bir `const`’tur. Desteklenen diğer değerleri package dokümantasyonunda görebilirsiniz.) Son olarak, mesajı verilen sunucu adresine göndermek için `Exchange(*Msg, string)` fonksiyonunu çağırın; bu örnekte bu adres Google tarafından işletilen bir DNS sunucusudur.

Muhtemelen fark ettiğiniz gibi, bu kod şu haliyle çok kullanışlı değil. Bir DNS sunucusuna sorgu gönderiyor ve A kaydı istiyor olsanız da, cevabı işlemiyorsunuz; sonuçla anlamlı hiçbir şey yapmıyorsunuz. Bunu Go ile programatik olarak yapmadan önce, DNS cevabının nasıl göründüğünü gözden geçirelim ki protokolü ve farklı sorgu tiplerini daha derinlemesine anlayabilelim.

Liste 5-1’deki programı çalıştırmadan önce, Wireshark veya `tcpdump` gibi bir paket analizörü çalıştırarak trafiği inceleyin. Bir Linux makinede `tcpdump` kullanımına şöyle bir örnek verilebilir:

```bash
$ sudo tcpdump eth0 -n udp port 53
```

Ayrı bir terminal penceresinde, programınızı şu şekilde derleyip çalıştırın:

```bash
$ go run main.go
```

Kodunuzu çalıştırdığınızda, paket yakalama çıktısında 8.8.8.8 adresine UDP 53 üzerinden bir bağlantı görmelisiniz. Ayrıca DNS protokolüne ait bazı detaylar da şöyle görünecektir:

```bash
$ sudo tcpdump eth0 -n udp port 53
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens33, link-type EN10M13 (Ethernet), capture size 262144 bytes
23:55:16.523741 IP 192.168.7.51.53307 > 8.8.8.8.53: 25147+ A? stacktitan.com. (32)
23:55:16.650905 IP 8.8.8.8.53 > 192.168.7.51.53307: 25147 1/0/0 A 104.131.56.170 (48)
```

Paket yakalama çıktısı, daha fazla açıklama gerektiren birkaç satır üretir. Öncelikle, 192.168.7.51 adresinden 8.8.8.8 adresine UDP 53 kullanılarak bir DNS A kaydı isteği gönderilmektedir. Yanıt, Google’ın 8.8.8.8 DNS sunucusundan dönmekte ve çözümlenmiş IP adresi olarak 104.131.56.170 değerini içermektedir.

`tcpdump` gibi bir paket analizörü kullanarak `stacktitan.com` alan adını bir IP adresine çözümleyebiliyorsunuz. Şimdi, aynı bilgiyi Go kullanarak nasıl çıkaracağımıza bakalım.

---

## Bir Msg struct’ından Cevapları İşlemek

`Exchange(*Msg, string)` fonksiyonunun döndürdüğü değerler `(*Msg, error)` şeklindedir. `error` tipinin döndürülmesi mantıklıdır ve Go idiom’larında yaygındır; peki neden girdi olarak verdiğiniz `*Msg`’i tekrar döndürür? Bunu netleştirmek için, `struct`’ın kaynak kodda nasıl tanımlandığına bakalım:

```go
type Msg struct {
    MsgHdr
    Compress bool       `json:"-"` // Eğer true ise, mesaj sıkıştırılacaktır...
    Question []Question           // Soru bölümündeki RR’leri tutar.
    Answer   []RR                 // Cevap bölümündeki RR’leri tutar.
    Ns       []RR                 // Yetkili bölümdeki RR’leri tutar.
    Extra    []RR                 // Ek bölümdeki RR’leri tutar.
}
```

Gördüğünüz gibi, `Msg` struct’ı hem soruları hem de cevapları tutar. Bu sayede tüm DNS sorularınızı ve cevaplarını tek, birleşik bir yapı içinde toplayabilirsiniz. `Msg` tipi, veriyle çalışmayı kolaylaştıran çeşitli metodlara sahiptir. Örneğin, `Question` slice’ı, kullanım kolaylığı sağlayan `SetQuestion()` metodu ile değiştirilmektedir. Aynı sonuca, `append()` kullanarak bu slice’ı doğrudan değiştirerek de ulaşabilirsiniz. `Answer` slice’ı ise sorguların yanıtlarını tutar ve `RR` tipindedir. Liste 5-2, cevapların nasıl işleneceğini göstermektedir.

```go
package main

import (
    "fmt"

    "github.com/miekg/dns"
)

func main() {
    var msg dns.Msg
    fqdn := dns.Fqdn("stacktitan.com")
    msg.SetQuestion(fqdn, dns.TypeA)
    in, err := dns.Exchange(&msg, "8.8.8.8:53")
    if err != nil {
        panic(err)
    }
    if len(in.Answer) < 1 {
        fmt.Println("No records")
        return
    }

    for _, answer := range in.Answer {
        if a, ok := answer.(*dns.A); ok {
            fmt.Println(a.A)
        }
    }
}
```

Liste 5-2: DNS cevaplarını işleme (`/ch-5/get_all_a/main.go`)

---

Örneğimiz, `Exchange` fonksiyonundan dönen değerleri bir değişkende saklayarak başlıyor, ardından bir hata olup olmadığını kontrol ediyor ve hata varsa programı durdurmak için `panic()` fonksiyonunu çağırıyor. `panic()` fonksiyonu, yığın izini (stack trace) hızla görmenizi ve hatanın nerede oluştuğunu tespit etmenizi sağlar. Sonraki adımda, `Answer` slice’ının uzunluğunun en az 1 olduğunu doğrulayın; değilse, kayıt bulunmadığını belirtin ve hemen `return` edin — sonuçta, alan adının çözümlenemediği meşru durumlar olacaktır.

`RR` tipi yalnızca iki metodu tanımlayan bir arayüz (interface)’tür ve bunların hiçbiri yanıtta saklanan IP adresine erişim sağlamaz. Bu IP adreslerine erişmek için, veriyi istediğiniz tipte bir örneğe dönüştürmek amacıyla tip doğrulaması (type assertion) yapmanız gerekir.

Öncelikle tüm cevaplar üzerinde döngü kurun. Sonrasında, üzerinde çalıştığınızın bir `*dns.A` tipi olduğundan emin olmak için cevap üzerinde tip doğrulaması gerçekleştirin. Bu işlemi yaptığınızda iki değer elde edersiniz: verinin iddia edilen (asserted) tipteki hali ve doğrulamanın başarılı olup olmadığını gösteren bir `bool`. Doğrulamanın başarılı olup olmadığını kontrol ettikten sonra, `a.A` içinde saklanan IP adresini yazdırın. Tip her ne kadar `net.IP` olsa da, bir `String()` metoduna sahiptir, dolayısıyla kolayca yazdırabilirsiniz.

Bu kodla zaman geçirerek, DNS sorgusunu ve `exchange` işlemini değiştirip ek kayıtlar arayacak şekilde uyarlayın. Tip doğrulaması kavramı size yabancı gelebilir; ancak diğer dillere aşinaysanız, tip dönüşümüne (type casting) benzer bir konsept olduğunu fark edeceksiniz.
