Bu örnekte port 80 olarak ayarlanmıştır, ancak DNS yükünüz (payload) hâlâ
port 53 kullanmaktadır, bu yüzden endişelenmeyin. Port 80 özellikle hibrit
(hybrid) yükler için kullanılır. Şekil 5-2, Yeni Listener penceresini ve girmeniz
gereken bilgileri göstermektedir.

Şekil 5-2: Yeni bir listener ekleme

Sonraki adımda, Şekil 5-3’te gösterildiği gibi beaconing için kullanılacak
alan adlarını girmeniz istenir.
DNS beacon olarak `attacker1.com` alan adını girin; bu, payload’unuzun
beacon gönderdiği alan adı olmalıdır. Yeni bir listener’ın başlatıldığına dair bir
mesaj görmelisiniz. Aynı işlemi diğer teamserver üzerinde, `DNS 2` ve
`attacker2.com` kullanarak tekrarlayın. Bu iki listener’ı kullanmaya başlamadan
önce, DNS mesajlarını inceleyip uygun şekilde yönlendiren bir ara sunucu
(intermediary server) yazmanız gerekir. Esasen, bu sizin proxy’nizdir.

Şekil 5-3: DNS beacon’ın alan adını ekleme

## Bir DNS Proxy’si Oluşturma

Bu bölüm boyunca kullandığınız DNS paketi, bir ara fonksiyon (intermediary
function) yazmayı kolaylaştırır ve daha önceki kısımlarda bu fonksiyonlardan
bazılarını zaten kullandınız. Proxy’nizin aşağıdakileri yapabilmesi gerekir:

- Gelen bir sorguyu almak için bir handler fonksiyonu oluşturmak
- Sorgudaki soruyu (question) inceleyerek alan adını çıkarmak
- Alan adına karşılık gelen üst (upstream) DNS sunucusunu belirlemek
- Soruyu üst DNS sunucusuyla değiş tokuş etmek ve yanıtı istemciye yazmak

Handler fonksiyonunuzu `attacker1.com` ve `attacker2.com` için statik
değerler kullanacak şekilde yazabilirsiniz, ancak bu sürdürülebilir değildir.
Bunun yerine, programın dışındaki bir kaynaktan, örneğin bir veritabanından
veya bir yapılandırma (configuration) dosyasından kayıtları okumalısınız.
Aşağıdaki kod, `domain,server` biçimini kullanarak bunu yapar; burada
gelen alan adı ve üst sunucu virgülle ayrılmıştır. Programınızı başlatmak için
bu formattaki kayıtları içeren bir dosyayı ayrıştıran (parse eden) bir fonksiyon
oluşturun. Liste 5-6’daki kod, `main.go` adlı yeni bir dosyaya yazılmalıdır.

```go
package main

import (
        "bufio"
        "fiat"

        "strings"
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
        return records, scanner.Err()
}

func main() {
        records, err := parse("proxy.config")
        if err != nil {
                panic(err)
        }

        fmt.Printf("%v\n", records)
}
```

**Liste 5-6: Bir DNS proxy yazmak (`ch-5/dns_proxy/main.go`)**

Bu kodla, yapılandırma bilgilerini içeren bir dosyayı ayrıştıran `parse`
fonksiyonunu tanımlıyor ve bir `map[string]string` döndürüyorsunuz. Bu
`map`’i gelen alan adını bulmak ve ilgili üst sunucuyu almak için
kullanacaksınız.

Aşağıdaki kodda ilk komutu terminal pencerinize girin; bu komut, `echo`
sonrasındaki string’i `proxy.config` adlı bir dosyaya yazar. Sonrasında
`dns_proxy.go` dosyasını derleyip çalıştırmalısınız.

```bash
$ echo 'attacker1.com,127.0.0.1:2020\nattacker2.com,127.0.0.1:2021' > proxy.config
$ go build
$ ./dns_proxy
map[attacker1.com:127.0.0.1:2020 attacker2.com:127.0.0.1:2021]
```
