```go
var results []result
fqdns := make(chan string, *flWorkerCount)
gather := make(chan []result)
tracker := make(chan empty)
```

Kullanıcı tarafından sağlanan işçi (worker) sayısını kullanarak `fqdns` kanalını arabellekli (buffered) kanal olarak oluştur. Bu, kanal bloklamadan önce birden fazla mesaj tutabildiği için işçilerin biraz daha hızlı başlamasını sağlar.

## `bufio` ile Tarayıcı (Scanner) Oluşturma

Sonraki adımda, kullanıcı tarafından sağlanan ve kelime listesi olarak kullanılacak dosyayı aç. Dosya açıldıktan sonra `bufio` paketini kullanarak yeni bir scanner oluştur. Scanner, dosyayı satır satır okumana olanak tanır. Aşağıdaki kodu `main()` fonksiyonuna ekle:

```go
fh, err := os.Open(*flWordlist)
if err != nil {
    panic(err)
}

defer fh.Close()
scanner := bufio.NewScanner(fh)
```

Burada, dönen hata `nil` değilse yerleşik `panic()` fonksiyonu kullanılıyor. Başkalarının kullanacağı bir package veya program yazarken, bu bilgiyi daha temiz bir formatta sunmayı düşünmelisin.

Yeni scanner'ı, verilen kelime listesinden bir satır metin almak ve bunu kullanıcı tarafından sağlanan alan adıyla (domain) birleştirerek bir FQDN oluşturmak için kullanacaksın. Elde edilen sonucu `fqdns` kanalı üzerinden göndereceksin. Ancak önce işçileri başlatman gerekiyor. Bu işlemin sırası önemli. İşçileri başlatmadan işi `fqdns` kanalına gönderirsen, arabellekli kanal sonunda dolar ve üreticilerin (producers) gönderimi bloklanır. Aşağıdaki kodu `main()` fonksiyonuna ekleyeceksin. Bu kodun amacı, worker goroutine'lerini başlatmak, girdi dosyanı okumak ve işi `fqdns` kanalı üzerinden göndermek.

```go
for i := 0; i < *flWorkerCount; i++ {
    go worker(tracker, fqdns, gather, *flServerAddr)
}

for scanner.Scan() {
    fqdns <- fmt.Sprintf("%s.%s", scanner.Text(), *flDomain)
}
```

Bu desenle worker'ları oluşturmak, eşzamanlı port tarayıcısını inşa ederken yaptıklarına benzemeli: Kullanıcının sağladığı sayıya ulaşana kadar bir `for` döngüsü kullandın. Dosyadaki her satırı almak için, bir döngü içinde `scanner.Scan()` kullanılır. Dosyada okunacak satır kalmadığında bu döngü sona erer. Tara (scan) edilen satırdan metnin string gösterimini almak için `scanner.Text()` kullan.

İş artık başlatıldı! Bir an durup bu harika anın tadını çıkar. Sonraki kodu okumadan önce, programda şu anda nerede olduğunu ve bu kitapta şimdiye kadar neler yaptığını düşün. Programı kendin tamamlamaya çalış ve ardından, geri kalanını adım adım açıklayacağımız bir sonraki bölüme devam et.

## Sonuçları Toplama ve Gösterme

Bitirmek için, önce worker'lardan gelen sonuçları toplayacak anonim bir goroutine başlat. Aşağıdaki kodu `main()` fonksiyonuna ekle:

```go
go func() {
    for r := range gather {
        results = append(results, r...)
    }
    var e empty
    tracker <- e
}()
```

`gather` kanalı üzerinde döngü yaparak, alınan sonuçları `results` slice'ına ekliyorsun. Bir slice'ı başka bir slice'a eklediğin için `...` söz dizimini kullanman gerekiyor. `gather` kanalı kapatıldıktan ve döngü sona erdikten sonra, daha önce yaptığın gibi `tracker` kanalına boş bir `struct` gönder. Bu, `append()` işlemi sonuçları kullanıcıya sunmaya başlamadan önce bitmezse oluşabilecek bir yarış durumunu (race condition) engellemek için yapılıyor.

Geriye sadece kanalları kapatmak ve sonuçları sunmak kaldı. Kanalları kapatmak ve sonuçları kullanıcıya göstermek için aşağıdaki kodu `main()` fonksiyonunun sonuna ekle:

```go
close(fqdns)
for i := 0; i < *flWorkerCount; i++ {
    <-tracker
}
close(gather)
<-tracker
```

İlk kapatılabilecek kanal `fqdns` çünkü bu kanal üzerinden gönderilecek tüm işleri zaten gönderdin. Sonraki adımda, her bir worker için bir kez `tracker` kanalından alman gerekiyor; böylece worker'ların tamamen çıktığını (tamamlandığını) sinyal etmelerine izin veriyorsun. Tüm worker'lar hesaba katıldıktan sonra artık `gather` kanalını kapatabilirsin çünkü alınacak başka sonuç yok. Son olarak, toplama (gathering) goroutine'inin tamamen bitmesine izin vermek için `tracker` kanalından bir kez daha al.

Sonuçlar henüz kullanıcıya sunulmadı. Bunu düzeltelim. İstersen `results` slice'ı üzerinde döngü yaparak `Hostname` ve `IPAddress` alanlarını `fmt.Printf()` kullanarak yazdırabilirsin. Biz bunun yerine, veriyi sunmak için Go'nun yerleşik harika paketlerinden birini kullanmayı tercih ediyoruz; `tabwriter` favorilerimizden biri. Tab'lerle ayrılmış düzgün hizalanmış sütunlarla veri sunmana olanak tanır. Sonuçlarını yazdırmak için `tabwriter` kullanmak amacıyla `main()` fonksiyonunun sonuna aşağıdaki kodu ekle:

```go
w := tabwriter.NewWriter(os.Stdout, 0, 8, 4, ' ', 0)
for _, r := range results {
    fmt.Fprintf(w, "%s\t%s\n", r.Hostname, r.IPAddress)
}
w.Flush()
```

Programın tam hali Liste 5-4'te gösterilmektedir.

```go
package main

import (
    "bufio"
    "errors"
    "flag"
    "fmt"
    "os"
    "text/tabwriter"

    "github.com/miekg/dns"
)

func lookupA(fqdn, serverAddr string) ([]string, error) {
    var m dns.Msg
    var ips []string
    m.SetQuestion(dns.Fqdn(fqdn), dns.TypeA)
    in, err := dns.Exchange(&m, serverAddr)
    if err != nil {
        return ips, err
    }

    if len(in.Answer) < 1 {
        return ips, errors.New("no answer")
    }

    for _, answer := range in.Answer {
        if a, ok := answer.(*dns.A); ok {
            ips = append(ips, a.A.String())
        }
    }

    return ips, nil
}

func lookupCNAME(fqdn, serverAddr string) ([]string, error) {
    var m dns.Msg
    var fqdns []string
    m.SetQuestion(dns.Fqdn(fqdn), dns.TypeCNAME)
    in, err := dns.Exchange(&m, serverAddr)
    if err != nil {
        return fqdns, err
    }

    if len(in.Answer) < 1 {
        return fqdns, errors.New("no answer")
    }

    for _, answer := range in.Answer {
        if c, ok := answer.(*dns.CNAME); ok {
            fqdns = append(fqdns, c.Target)
        }
    }

    return fqdns, nil
}
```
