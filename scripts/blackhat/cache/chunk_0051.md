Burada neye bakıyorsunuz? Çıktı, teamserver alan adları ile Cobalt Strike DNS sunucusunun dinlediği port arasındaki eşlemedir. İki ayrı Docker konteynerinizde port 2020 ve 2021'i port 53'e eşlediğinizi hatırlayın. Bu, aracınız için temel yapılandırmayı oluşturmanın hızlı ve kirli bir yoludur; böylece bunu bir veritabanında veya başka bir kalıcı depolama mekanizmasında saklamak zorunda kalmazsınız.

Bir kayıt haritasını (map) tanımladıktan sonra, artık handler fonksiyonunu yazabilirsiniz. Kodu rafine edelim ve `main()` fonksiyonunuza aşağıdakileri ekleyelim. Bu kod, yapılandırma dosyanızın ayrıştırılmasını takiben gelmelidir.

```go
dns.HandleFunc(".", func(w dns.ResponseWriter, req *dns.Msg) {
    if len(req.Question) < 1 {
        dns.HandleFailed(w, req)
        return
    }

    name := req.Question[0].Name
    parts := strings.Split(name, ".")
    if len(parts) > 1 {
        name = strings.Join(parts[len(parts)-2:], ".")
    }

    match, ok := records[name]
    if !ok {
        dns.HandleFailed(w, req)
        return
    }

    resp, err := dns.Exchange(req, match)
    if err != nil {
        dns.HandleFailed(w, req)
        return
    }

    if err := w.WriteMsg(resp); err != nil {
        dns.HandleFailed(w, req)
        return
    }
})

log.Fatal(dns.ListenAndServe(":53", "udp", nil))
```

Önce, tüm gelen istekleri ele almak için `HandleFunc()` fonksiyonunu bir nokta ile çağırın ve anonim bir fonksiyon tanımlayın; bu, yeniden kullanmayı düşünmediğiniz (adı olmayan) bir fonksiyondur. Bir kod bloğunu yeniden kullanmayı düşünmüyorsanız bu iyi bir tasarımdır. Yeniden kullanmayı düşünüyorsanız, onu isimli bir fonksiyon olarak bildirip öyle çağırmalısınız. Sonra, gelen `questions` slice'ını inceleyip en az bir soru sağlandığından emin olun ve eğer sağlanmadıysa `HandleFailed()` çağırıp fonksiyondan erken çıkmak için `return` edin. Bu, handler boyunca kullanılan bir kalıptır. En az bir soru varsa, ilk sorudan istenen adı güvenle alabilirsiniz. Adı bir nokta ile bölmek, alan adını çıkarmak için gereklidir. Adı bölmek hiçbir zaman 1'den küçük bir değere yol açmamalıdır ama yine de güvenlik için kontrol etmelisiniz. Slice operatörünü kullanarak slice'ın kuyruğunu—yani slice'ın sonundaki elemanları—alabilirsiniz. Şimdi, `records` map'inden upstream sunucuyu almanız gerekiyor.

Bir map'ten değer almak, bir veya iki değişken döndürebilir. Anahtar (bizim durumumuzda bir alan adı) map'te varsa, karşılık gelen değeri döndürür. Alan adı yoksa, boş bir string döndürür. Dönen değerin boş string olup olmadığını kontrol edebilirsiniz ama daha karmaşık tiplerle çalışmaya başladığınızda bu verimsiz olur. Bunun yerine iki değişken atayın: ilki anahtar için değer, ikincisi ise anahtar bulunduğunda `true` döndüren bir Boolean'dır. Eşleşmeyi garantiledikten sonra, isteği upstream sunucu ile değiş tokuş (exchange) edebilirsiniz. Burada yalnızca, istek aldığınız alan adının kalıcı depolamanızda yapılandırıldığından emin oluyorsunuz. Sonraki adımda, upstream sunucudan gelen yanıtı istemciye yazın. Handler fonksiyonu tanımlandıktan sonra, sunucuyu başlatabilirsiniz. Son olarak, artık proxy'yi derleyip (build) başlatabilirsiniz.

Proxy çalışırken, iki Cobalt Strike listener kullanarak onu test edebilirsiniz. Bunu yapmak için önce iki stageless çalıştırılabilir (executable) oluşturun. Cobalt Strike'ın üst menüsünden, dişli gibi görünen simgeye tıklayın ve çıktıyı Windows Exe olarak değiştirin. Bu işlemi her bir teamserver'dan tekrarlayın. Bu çalıştırılabilir dosyaların her birini Windows sanal makinenize kopyalayın ve çalıştırın. Windows sanal makinenizin DNS sunucusu, Linux ana makinenizin IP adresi olmalıdır. Aksi takdirde test çalışmaz.

Bir iki an sürebilir ama sonunda her bir teamserver'da yeni bir beacon görmelisiniz. Görev tamamlandı!

## Son Rötuşlar

Bu harika, ancak teamserver'ınızın veya redirector'ınızın IP adresini değiştirmeniz, ya da yeni bir kayıt eklemeniz gerektiğinde, sunucuyu da yeniden başlatmanız gerekecek. Beacon'lar muhtemelen böyle bir işlemi atlatacaktır, ama çok daha iyi bir seçenek varken neden risk alasınız? Çalışan programınıza yapılandırma dosyasını yeniden yüklemesi gerektiğini söylemek için süreç sinyallerini (process signals) kullanabilirsiniz. Bu numarayı ilk kez, bunu harika Caddy Server'da uygulayan Matt Holt'tan öğrendim. Liste 5-7, süreç sinyal mantığı da dahil olmak üzere programın tamamını gösteriyor:

```go
package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "os/signal"
    "strings"
    "sync"
    "syscall"

    "github.com/miekg/dns"
)

func parse(filename string) (map[string]string, error) {
    records := make(map[string]string)
    fh, err := os.Open(filename)
    if err != nil {
        return records, err
    }
    defer fh.Close()
    scanner := bufio.NewScanner(fh)
    for scanner.Scan() {
        line := scanner.Text()
        parts := strings.SplitN(line, ",", 2)
        if len(parts) < 2 {
            return records, fmt.Errorf("%s is not a valid line", line)
        }
        records[parts[0]] = parts[1]
    }
    log.Println("records set to:")
    for k, v := range records {
        fmt.Printf("%s -> %s\n", k, v)
    }
    return records, scanner.Err()
}

func main() {
    var recordLock sync.RWMutex
```
