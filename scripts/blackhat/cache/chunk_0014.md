Liste 2-5: WaitGroup kullanan eşzamanlı bir tarayıcı (/ch-2/tcp-scanner-wg-too-foo
Anain.go)

Bu sürüm, kodun ilk sürümüne büyük ölçüde benzer kalır. Ancak, kalan işi açıkça izleyen kod eklediniz. Programın bu sürümünde, senkronize bir sayaç olarak görev alan bir `sync.WaitGroup` oluşturursunuz. Bir port `p` taramak için her goroutine oluşturduğunuzda `wg.Add(1)` ile bu sayacı artırırsınız ve ertelenmiş (deferred) bir `wg.Done()` çağrısı, her bir iş birimi tamamlandığında sayacı azaltır. `main()` fonksiyonunuz `wg.Wait()` çağrısı yapar; bu çağrı, tüm işler tamamlanıp sayacınız tekrar sıfıra dönene kadar bloklar.

Programın bu sürümü daha iyi, ancak hâlâ hatalıdır. Bunu birden fazla kez ve birden fazla hedefe karşı çalıştırırsanız tutarsız sonuçlar görebilirsiniz. Aynı anda aşırı sayıda hedef veya port taramak, ağ ya da sistem sınırlamalarının sonuçlarınızı bozmasına neden olabilir. Koddaki `1024` değerini `65535` ile ve hedef sunucuyu da `127.0.0.1` (localhost) ile değiştirin. İsterseniz, bu bağlantıların ne kadar hızlı açıldığını görmek için Wireshark veya `tcpdump` kullanabilirsiniz.

## İşçi Havuzu (Worker Pool) Kullanarak Port Tarama

Tutarsızlıkları önlemek için yürütülen eşzamanlı (concurrent) işi yönetmek üzere bir goroutine havuzu kullanacaksınız. Bir `for` döngüsü kullanarak, kaynak havuzu olarak belirli sayıda işçi (worker) goroutine oluşturacaksınız. Ardından, ana "iş parçacığınızda" (`main()` fonksiyonunda), iş sağlamak için bir kanal (channel) kullanacaksınız.

Başlamak için, 100 işçiye sahip, `int` türünde bir kanal tüketen ve kanaldan okuduğu değerleri ekrana yazdıran yeni bir program oluşturun. Yine yürütmeyi bloklamak için `WaitGroup` kullanacaksınız. `main` fonksiyonunuz için bir iskelet kod oluşturun. Bunun üstüne, Liste 2-6'da gösterilen fonksiyonu yazın.

```go
func worker(ports chan int, wg *sync.WaitGroup) {
    for p := range ports {
        fmt.Println(p)
        wg.Done()
    }
}
```

**Liste 2-6: İşi işlemek için bir worker fonksiyonu**

`worker(int, *sync.WaitGroup)` fonksiyonu iki argüman alır: `int` türünde bir kanal ve bir `WaitGroup` işaretçisi (pointer). Kanal, iş almak için kullanılacak; `WaitGroup` ise tek bir iş öğesi tamamlandığında bunu takip etmek için kullanılacaktır.

Şimdi, iş yükünü yönetecek ve `worker(int, *sync.WaitGroup)` fonksiyonunuza iş sağlayacak Liste 2-7'deki `main()` fonksiyonunu ekleyin.

```go
package main

import (
    "fmt"
    "sync"
)

func worker(ports chan int, wg *sync.WaitGroup) {
    for p := range ports {
        fmt.Println(p)
        wg.Done()
    }
}

func main() {
    ports := make(chan int, 100)
    var wg sync.WaitGroup
    for i := 0; i < cap(ports); i++ {
        go worker(ports, &wg)
    }

    for i := 1; i <= 1024; i++ {
        wg.Add(1)
        ports <- i
    }
    wg.Wait()
    close(ports)
}
```

**Liste 2-7: Basit bir worker pool (/ch-2/tcp-sync-scanner/main.go)**

İlk olarak `make()` kullanarak bir kanal oluşturursunuz. Burada `make()` fonksiyonuna ikinci parametre olarak bir `int` değeri olan `100` verilir. Bu, kanalın arabellekli (buffered) olmasını sağlar; yani, bir alıcı (receiver) öğeyi okumadan da kanala öğe gönderebilirsiniz. Arabellekli kanallar, birden fazla üretici (producer) ve tüketici (consumer) için işi sürdürmek ve izlemek açısından idealdir. Kanal kapasitesini 100'de sınırlandırdınız; yani gönderici bloklanmadan önce kanal 100 öğe tutabilir.

Bu, hafif bir performans artışı sağlar; çünkü tüm worker'ların hemen başlamasına izin verir.

Sonra, istenen sayıdaki worker'ı başlatmak için bir `for` döngüsü kullanırsınız — bu örnekte 100. `worker(int, *sync.WaitGroup)` fonksiyonunda, `ports` kanalından sürekli veri almak için `range` kullanırsınız; kanal kapanana kadar döngü devam eder. Dikkat edin, worker içinde henüz gerçek bir iş yapmıyorsunuz — bu kısmı birazdan ekleyeceksiniz. `main()` fonksiyonunda portları sıralı olarak yineleyerek, her portu `ports` kanalına gönderirsiniz; yani worker'a aktarırsınız. Tüm işler tamamlandıktan sonra kanalı kapatırsınız.

Bu programı derleyip çalıştırdığınızda, sayıların ekrana yazdırıldığını görürsünüz. Burada ilginç bir şey fark edebilirsiniz: sayılar belirli bir sıraya göre yazdırılmıyor. Paralellik (parallelism) dünyasına hoş geldiniz.

## Çok Kanallı (Multichannel) İletişim

Port tarayıcıyı tamamlamak için, önceki bölümdeki kodunuzu buraya entegre edebilirsiniz ve gayet iyi çalışır. Ancak, yazdırılan portlar sıralı olmaz; çünkü tarayıcı portları sırayla kontrol etmez. Bu problemi çözmek için, port tarama sonuçlarını ana iş parçacığınıza geri iletmek ve yazdırmadan önce portları sıralamak için ayrı bir iş parçacığı (goroutine) kullanmanız gerekir. Bu değişikliğin bir diğer faydası, `WaitGroup` bağımlılığını tamamen kaldırabilmenizdir; çünkü tamamlanmayı izlemenin başka bir yoluna sahip olursunuz. Örneğin, 1024 port tararsanız, worker kanalına 1024 kez iş gönderirsiniz ve bu işlerin sonucunu ana iş parçacığına 1024 kez geri göndermeniz gerekir. Gönderilen iş birimi sayısı ile alınan sonuç sayısı aynı olduğundan, programınız kanalları ne zaman kapatacağını ve dolayısıyla worker'ları ne zaman durduracağını bilebilir.

Bu değişiklik, port tarayıcıyı tamamlayan Liste 2-8'de gösterilmektedir.

```go
package main

import (
    "fmt"
    "net"
    "sort"
)

func worker(ports, results chan int) {
    for p := range ports {
        address := fmt.Sprintf("scanme.nmap.org:%d", p)
        conn, err := net.Dial("tcp", address)
        if err != nil {
            results <- 0
            continue
        }
        conn.Close()
        results <- p
    }
}
```

```go
func main() {
    ports := make(chan int, 100)
    results := make(chan int)
    var openports []int

    for i := 0; i < cap(ports); i++ {
        go worker(ports, results)
    }

    go func() {
        for i := 1; i <= 1024; i++ {
            ports <- i
        }
    }()
}
```
