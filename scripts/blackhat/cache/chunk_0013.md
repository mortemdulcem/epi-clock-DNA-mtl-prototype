Artık elinde bir `int` var, ancak unutma, `Dial` fonksiyonuna ikinci argüman olarak bir `string` vermen gerekiyor (`Dial(network, address string)`). Tam sayıdan `string` üretmenin en az iki yolu var. Bunlardan biri `string` dönüştürme paketi `strconv` kullanmaktır. Diğeri ise `fmt` paketindeki, C'deki muadiliyle benzer şekilde, bir format `string`inden `string` üreten `Sprintf(format string, a ...interface{})` fonksiyonunu kullanmaktır.

Liste 2-2'deki kodu içeren yeni bir dosya oluştur ve hem döngünün hem de `string` üretiminin çalıştığından emin ol. Bu kodu çalıştırdığında 1024 satır yazdırması gerekir; ama bunları saymak zorunda değilsin.

```go
package main

import (
    "fmt"
)

func main() {
    for i := 1; i <= 1024; i++ {
        address := fmt.Sprintf("scanme.nmap.org:%d", i)
        fmt.Println(address)
    }
}
```

**Liste 2-2: `scanme.nmap.org` üzerinde 1024 portun taranması (/ch-2/tcp-scanner-slow/main.go)**

Geriye kalan tek şey, önceki kod örneğinde ürettiğin `address` değişkenini `Dial(network, address string)` içine yerleştirmek ve port kullanılabilirliğini test etmek için önceki bölümde kullandığın hatayı kontrol etme mantığının aynısını uygulamak. Ayrıca, bağlantı başarılı olduğunda onu kapatacak bir mantık da eklemelisin; böylece bağlantılar açık kalmaz. Bağlantılarını FIN’leyip düzgün kapatmak nezakettendir. Bunu yapmak için `Conn` üzerindeki `Close()` metodunu çağıracaksın. Liste 2-3’te tamamlanmış port tarayıcı gösteriliyor.

```go
package main

import (
    "fmt"
    "net"
)

func main() {
    for i := 1; i <= 1024; i++ {
        address := fmt.Sprintf("scanme.nmap.org:%d", i)
        conn, err := net.Dial("tcp", address)
        if err != nil {
            // port kapalı veya filtrelenmiş
            continue
        }
        conn.Close()
        fmt.Printf("%d open\n", i)
    }
}
```

**Liste 2-3: Tamamlanmış port tarayıcı (/ch-2/tcp-scanner-slow/main.go)**

Bu kodu derleyip çalıştırarak hedef üzerinde hafif bir tarama gerçekleştir. Birkaç açık port gördüğünü fark etmelisin.

## Eşzamanlı (concurrent) Tarama Gerçekleştirmek

Önceki tarayıcı, tek bir çalıştırmada (pun kasıtlı) birden fazla port tarıyordu. Ancak artık amacın, portları eşzamanlı (concurrently) taramak; bu da port tarayıcını daha hızlı hale getirecek. Bunu yapmak için goroutine’lerin gücünden yararlanacaksın. Go, sisteminin kaldırabildiği kadar çok goroutine oluşturmanı sağlar; tek sınır mevcut bellektir.

### “Çok Hızlı” Tarayıcı Sürümü

Eşzamanlı çalışan bir port tarayıcı oluşturmanın en saf (naive) yolu, `Dial(network, address string)` çağrısını bir goroutine içine sarmalamaktır. Doğal sonuçlardan ders çıkarma adına, `scan-too-fast.go` adında yeni bir dosya oluştur, Liste 2-4’teki kodu içine koy ve çalıştır.

```go
package main

import (
    "fmt"
    "net"
)

func main() {
    for i := 1; i <= 1024; i++ {
        go func(j int) {
            address := fmt.Sprintf("scanme.nmap.org:%d", j)
            conn, err := net.Dial("tcp", address)
            if err != nil {
                return
            }
            conn.Close()
            fmt.Printf("%d open\n", j)
        }(i)
    }
}
```

**Liste 2-4: Fazla hızlı çalışan bir tarayıcı (/ch-2/tcp-scanner-too-fast/main.go)**

Bu kodu çalıştırdığında, programın neredeyse anında çıktığını görmelisin:

```bash
$ time ./tcp-scanner-too-fast
./tcp-scanner-too-fast  0.005s user 0.00s system 90% cpu 0.004s total
```

Yeni çalıştırdığın kod, her bağlantı için bir goroutine başlatıyor ve ana goroutine, bağlantının gerçekleşmesini beklemesi gerektiğini bilmiyor. Bu nedenle, `for` döngüsü turları biter bitmez kod tamamlanıp çıkıyor; bu da, senin kodun ve hedef portlar arasındaki paket alışverişinden daha hızlı olabilir. Böylece, paketleri hâlâ yolda (in-flight) olan portlar için doğru sonuçlar alamayabilirsin.

Bunu düzeltmenin birkaç yolu var. Bunlardan biri, `sync` paketindeki `WaitGroup` kullanmaktır; bu, eşzamanlılığı kontrol etmenin iş parçacığı (thread)/goroutine güvenli bir yoludur. `WaitGroup` bir `struct` tipidir ve şu şekilde oluşturulabilir:

```go
var wg sync.WaitGroup
```

`WaitGroup` oluşturduktan sonra, bu `struct` üzerinde birkaç metod çağırabilirsin. İlki `Add(int)` metodudur; verilen sayı kadar dahili sayacı artırır. Sonra `Done()` çağrısı, sayacı bir azaltır. Son olarak, `Wait()` çağrıldığı goroutine’in yürütülmesini bloke eder ve dahili sayaç sıfıra ulaşana kadar yürütmeye devam edilmesine izin vermez. Bu çağrıları birleştirerek ana goroutine’in tüm bağlantıların tamamlanmasını beklemesini sağlayabilirsin.

## WaitGroup Kullanarak Eşzamanlı Tarama

Liste 2-5’te, goroutine’ler için farklı bir uygulama ile aynı port tarama programı gösterilmektedir.

```go
package main

import (
    "fmt"
    "net"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 1024; i++ {
        wg.Add(1)
        go func(j int) {
            defer wg.Done()
            address := fmt.Sprintf("scanme.nmap.org:%d", j)
            conn, err := net.Dial("tcp", address)
            if err != nil {
                return
            }
            conn.Close()
            fmt.Printf("%d open\n", j)
        }(i)
    }
    wg.Wait()
}
```
