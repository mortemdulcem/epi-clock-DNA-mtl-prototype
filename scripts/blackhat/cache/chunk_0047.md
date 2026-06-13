```go
func lookup(fqdn, serverAddr string) []result {
    var results []result
    var cfqdn = fqdn // Orijinali değiştirme.
    for {
        cnames, err := lookupCNAME(cfqdn, serverAddr)
        if err == nil && len(cnames) > 0 {
            cfqdn = cnames[0]
            continue // Bir sonraki CNAME'i işlememiz gerekiyor.
        }

        ips, err := lookupA(cfqdn, serverAddr)
        if err != nil {
            break // Bu ana makine adı için A kaydı yok.
        }

        for _, ip := range ips {
            results = append(results, result{IPAddress: ip, Hostname: fqdn})
        }

        break // Tüm sonuçları işledik.
    }

    return results
}

func worker(tracker chan empty, fqdns chan string, gather chan []result, serverAddr string) {
    for fqdn := range fqdns {
        results := lookup(fqdn, serverAddr)
        if len(results) > 0 {
            gather <- results
        }
    }
    var e empty
    tracker <- e
}

type empty struct{}

type result struct {
    IPAddress string
    Hostname  string
}

func main() {
    var (
        flDomain      = flag.String("domain", "", "The domain to perform guessing against.")
        flWordlist    = flag.String("wordlist", "", "The wordlist to use for guessing.")
        flWorkerCount = flag.Int("c", 100, "The amount of workers to use.")
        flServerAddr  = flag.String("server", "8.8.8.8:53", "The DNS server to use.")
    )

    flag.Parse()

    if *flDomain == "" || *flWordlist == "" {
        fmt.Println("-domain and -wordlist are required")
        os.Exit(1)
    }

    var results []result

    fqdns := make(chan string, *flWorkerCount)
    gather := make(chan []result)
    tracker := make(chan empty)

    fh, err := os.Open(*flWordlist)
    if err != nil {
        panic(err)
    }
    defer fh.Close()
    scanner := bufio.NewScanner(fh)

    for i := 0; i < *flWorkerCount; i++ {
        go worker(tracker, fqdns, gather, *flServerAddr)
    }

    go func() {
        for r := range gather {
            results = append(results, r...)
        }

        var e empty
        tracker <- e
    }()

    for scanner.Scan() {
        fqdns <- fmt.Sprintf("%s.%s", scanner.Text(), *flDomain)
    }

    // Note: We could check scanner.Err() here.

    close(fqdns)
    for i := 0; i < *flWorkerCount; i++ {
        <-tracker
    }
    close(gather)
    <-tracker

    w := tabwriter.NewWriter(os.Stdout, 0, 8, 0, '\t', 0)
    for _, r := range results {
        fmt.Fprintf(w, "%s\t%s\n", r.Hostname, r.IPAddress)
    }

    w.Flush()
}
```

**Liste 5-4:** Tam alt alan adı tahmin programı `gch-5/subdomain_guesser/main.go`

Alt alan adı tahmin programın tamamlandı. Artık yepyeni alt alan adı tahmin aracını derleyip çalıştırabilmelisin. Açık kaynak depolardaki kelime listeleri veya sözlük dosyalarıyla dene (bunlardan bir sürüsünü Google aramasıyla bulabilirsin). İşçi (worker) sayısıyla oyna; çok hızlanırsan, farklı sonuçlar elde edebileceğini görebilirsin. İşte yazarların sisteminde 1000 işçi ile yapılmış bir çalıştırma:

```bash
$ wc -l namelist.txt
1909 namelist.txt
$ time ./subdomain_guesser -domain microsoft.com -wordlist namelist.txt -c 1000
ajax.microsoft.com            72.21.81.200
buy.microsoft.com             157.56.65.82
news.microsoft.com            192.230.67.121
applications.microsoft.com    168.62.185.179
sc.microsoft.com              157.55.99.181
open.microsoft.com            23.99.65.65
ra.microsoft.com              131.107.98.31
ris.microsoft.com             213.199.139.250
smtp.microsoft.com            205.248.106.64
wallet.microsoft.com          40.86.87.229
jp.microsoft.com              134.170.185.46
ftp.microsoft.com             134.170.188.232
develop.microsoft.com         104.43.195.251
./subdomain_guesser -domain microsoft.com -wordlist namelist.txt -c 1000 0.235
user 0.675 system 22% cpu 4.040 total
```

Çıktının birkaç FQDN ve bunların IP adreslerini gösterdiğini göreceksin. Verilen kelime listesine (word list) dayalı olarak her sonuç için alt alan adı değerlerini tahmin edebildik.

Artık kendi alt alan adı tahmin aracını geliştirdiğine ve farklı DNS kayıtlarını numaralandırmak için ana makine adlarını ve IP adreslerini çözmeyi öğrendiğine göre, kendi DNS sunucunu ve vekil sunucunu (proxy) yazmaya hazırsın.

## DNS Sunucuları Yazmak

Yoda’nın dediği gibi, “İki tane her zaman vardır, daha fazla değil, daha az değil.” Elbette burada istemci-sunucu ilişkisini kastediyordu ve artık istemci tarafında ustalaştığına göre, sunucu tarafında da usta olma zamanı. Bu bölümde, temel bir sunucu ve bir proxy yazmak için Go DNS paketini kullanacaksın. DNS sunucularını, kısıtlayıcı ağlardan tünelleme yapmak ve sahte kablosuz erişim noktaları kullanarak sahtekarlık (spoofing) saldırıları gerçekleştirmek gibi çeşitli kötü niyetli faaliyetler (bunlarla sınırlı olmamak üzere) için kullanabilirsin.

Başlamadan önce, bir laboratuvar ortamı kurman gerekecek. Bu laboratuvar ortamı, gerçek alan adlarına sahip olmak ve maliyetli altyapılar kullanmak zorunda kalmadan gerçekçi senaryoları taklit etmene olanak tanıyacak; ancak istersen alan adı kaydedip gerçek bir sunucu da kullanabilirsin.

## Laboratuvar Kurulumu ve Sunucuya Giriş

Laboratuvar ortamın iki sanal makineden (VM) oluşur: istemci olarak görev yapacak bir Microsoft Windows VM ve sunucu olarak görev yapacak bir Ubuntu VM. Bu örnek, her makine için Bridged ağ moduyla birlikte VMWare Workstation kullanıyor; özel bir sanal ağ da kullanabilirsin, ama her iki makinenin de aynı ağda olduğundan emin ol. Sunucun, resmi Java Docker imajından oluşturulmuş iki Cobalt Strike Docker örneği çalıştıracak (Cobalt Strike için Java önkoşuldur). Laboratuvar ortamının nasıl görüneceği Şekil 5-1’de gösteriliyor.

| İstemci                 | Sunucu          |
|-------------------------|-----------------|
| Microsoft Windows       | Ubuntu Linux    |
|                         |                 |
|                         | DNS             |
|                         | Java            |
|                         | Cobalt Strike 1 |
|                         | Cobalt Strike 2 |
|                         | Docker          |

**Şekil 5-1:** DNS sunucunu oluşturmak için laboratuvar kurulumu
