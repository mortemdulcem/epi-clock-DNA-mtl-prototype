DNS'i Sömürmek 109

Bu kod tanıdık görünmelidir, çünkü bu bölümün ilk kısmında yazdığınız koda neredeyse birebir benzerdir. İlk fonksiyon olan `lookupA`, bir IP adresi listesi döndürür ve `lookupCNAME` ise bir hostname listesi döndürür.

CNAME, yani canonical name (kanonik ad) kayıtları, bir FQDN'den diğerine işaret eder ve ilkine bir takma ad (alias) görevi görür. Örneğin, `example.com` organizasyonunun sahibi, bir WordPress barındırma servisi kullanarak bir WordPress sitesi barındırmak istesin. Bu servis, tüm kullanıcılarının sitelerini dengelemek için yüzlerce IP adresine sahip olabilir, bu nedenle tekil bir sitenin IP adresini sağlamak pratik değildir. WordPress barındırma servisi bunun yerine, `example.com` sahibinin referans verebileceği kanonik bir ad (bir CNAME) sağlayabilir. Böylece `www.example.com`, `someserver.hostingcompany.org` adresine işaret eden bir CNAME'e sahip olabilir; bu adresin de bir IP adresine işaret eden bir A kaydı vardır. Bu, `example.com` sahibinin, IP bilgisine sahip olmadığı bir sunucuda sitesini barındırmasına olanak tanır.

Çoğu zaman, geçerli bir A kaydına ulaşmak için CNAME zincirini takip etmeniz gerekir. Buna zincir diyoruz, çünkü sonsuza kadar sürebilen bir CNAME zinciriniz olabilir. Aşağıdaki fonksiyonu `main()` fonksiyonunun dışına yerleştirerek CNAME zincirini kullanarak geçerli A kaydının nasıl bulunacağını görebilirsiniz:

```go
func lookup(fqdn, serverAddr string) []result {
    var results []result
    var cfqdn = fqdn // Don't modify the original.
    for {
        cnames, err := lookupCNAME(cfqdn, serverAddr)
        if err == nil && len(cnames) > 0 {
            cfqdn = cnames[0]
            continue // We have to process the next CNAME.
        }

        ips, err := lookupA(cfqdn, serverAddr)
        if err != nil {
            break // There are no A records for this hostname.
        }

        for _, ip := range ips {
            results = append(results, result{IPAddress: ip, Hostname: fqdn})
        }

        break // We have processed all the results.
    }

    return results
}
```

Öncelikle, sonuçları saklamak için bir `slice` tanımlayın ➊. Ardından, birinci argüman olarak geçirilen FQDN'nin bir kopyasını oluşturun ➋; bunu yalnızca tahmin edilen orijinal FQDN'yi kaybetmemek için değil, aynı zamanda ilk sorgu denemesinde kullanabilmek için yaparsınız. Sonsuz bir döngü başlattıktan sonra, FQDN için CNAME'leri çözmeye çalışın ➌. Hata oluşmazsa ve en az bir CNAME dönerse ➍, dönen CNAME'i kullanarak `cfqdn` değerini ayarlayın ➎ ve `continue` kullanarak döngünün başına dönün ➏. Bu süreç, bir hata oluşana kadar CNAME zincirini takip etmenizi sağlar. Bir hata oluşursa, bu zincirin sonuna geldiğinizi gösterir ve bu noktada A kayıtlarını arayabilirsiniz ➐; ancak bir hata varsa, bu kayıt çözümlemede bir sorun olduğunu gösterir ve döngüden erken çıkarsınız. Geçerli A kayıtları varsa, dönen her IP adresini `results` slice'ına ekleyin ➑ ve döngüden çıkın ➒. Son olarak, sonuçları çağırana döndürürsünüz.

İsim çözümlemesine ilişkin mantığımız yerinde görünüyor. Ancak, performansı dikkate almadınız. Örneğimizi goroutine dostu hale getirerek eşzamanlılık (concurrency) ekleyelim.

## Worker Fonksiyonuna İş Aktarmak

Bir *unit of work* (iş birimi) gerçekleştiren bir worker fonksiyonuna iş aktaran bir goroutine havuzu (pool) oluşturacaksınız. Bunu, iş dağıtımını ve sonuçların toplanmasını koordine etmek için kanallar (channels) kullanarak yapacaksınız. 2. Bölüm’de, eşzamanlı bir port tarayıcı (port scanner) inşa ederken benzer bir şey yaptığınızı hatırlayın.

Liste 5-3’teki kodu genişletmeye devam edin. Önce `worker()` fonksiyonunu oluşturun ve `main()` fonksiyonunun dışına yerleştirin. Bu fonksiyon üç kanal argümanı alır: worker’ın işinin bittiğini sinyallemek için kullanılan bir kanal, üzerinde iş (domain) alacağı bir kanal ve sonuçları göndereceği bir kanal. Fonksiyon ayrıca hangi DNS sunucusunun kullanılacağını belirtmek için son bir `string` argümanına ihtiyaç duyar. Aşağıdaki kod, `worker()` fonksiyonumuzun bir örneğini gösterir:

```go
type empty struct{} // ➊

func worker(tracker chan empty, fqdns chan string, gather chan []result, serverAddr string) {
    for fqdn := range fqdns { // ➋
        results := lookup(fqdn, serverAddr)
        if len(results) > 0 {
            gather <- results // ➌
        }
    }

    var e empty
    tracker <- e // ➍
}
```

`worker()` fonksiyonunu tanıtmadan önce, worker’ın ne zaman tamamlandığını takip etmek için `empty` tipini tanımlayın ➊. Bu, alanı olmayan bir `struct`’tır; boş bir `struct` kullanırsınız çünkü boyutu 0 bayttır ve kullanıldığında neredeyse hiç etkisi veya ek yükü (overhead) olmaz. Daha sonra `worker()` fonksiyonunda, FQDN’lerin iletildiği domain kanalını döngüyle okuyun ➋. `lookup()` fonksiyonunuzdan sonuçları aldıktan ve en az bir sonuç olduğundan emin olduktan sonra, sonuçları `gather` kanalı üzerinden gönderin ➌; bu kanal sonuçların `main()` fonksiyonunda yeniden toplanmasını sağlar. İş döngüsü, kanal kapatıldığı için sona erdiğinde, çağırana tüm işlerin tamamlandığını bildirmek için `tracker` kanalı üzerinden boş bir `struct` gönderilir ➍. Boş `struct`’ı `tracker` kanalı üzerinden göndermek önemli bir son adımdır. Bunu yapmazsanız, bir yarış durumu (race condition) oluşur, çünkü çağıran, `gather` kanalı sonuçları almadan önce çıkış yapabilir.

Gereken tüm altyapı şu noktada hazır olduğuna göre, dikkatimizi Liste 5-3’te başladığımız programı tamamlamak için yeniden `main()` fonksiyonuna verelim.

DNS'i Sömürmek 111

Sonuçları ve `worker` fonksiyonuna iletilecek kanalları tutacak bazı değişkenler tanımlayın ➎. Sonra `main()` içine aşağıdaki kodu ekleyin:
