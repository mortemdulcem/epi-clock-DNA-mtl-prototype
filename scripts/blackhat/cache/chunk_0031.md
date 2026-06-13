HTTP istemciler ve araçlarla uzaktan etkileşim sırasında hatalar oluştuğunda, yanıt gövdesini ❶ okur ve bunu kullanarak bir `zip.Reader` ❷ oluşturursunuz. Metadata paketinizde daha önce oluşturduğunuz `NewProperties()` fonksiyonunun bir `zip.Reader` beklediğini hatırlayın. Artık uygun veri tipine sahip olduğunuza göre, bunu o fonksiyona ❸ geçirir ve özellikler (properties) dosyadan okunarak doldurulur ve ekranınıza yazdırılır.

`main()` fonksiyonu tüm süreci başlatır ve kontrol eder; alan adını (domain) ve dosya türünü komut satırı argümanları olarak ona verirsiniz. Fonksiyon sonra bu girdi verilerini kullanarak uygun filtrelerle ❹ Bing sorgusunu oluşturur. Filtre dizesi (filter string) kodlanır ve tam Bing arama URL’sini ❺ oluşturmak için kullanılır. Arama isteği, örtük olarak bir HTTP GET isteği yapan ve HTML yanıt belgesinin goquery-uyumlu bir temsili ❻ olan bir nesne döndüren `goquery.NewDocument()` fonksiyonu kullanılarak gönderilir. Bu belge goquery ile incelenebilir. Son olarak, tarayıcınızın geliştirici araçlarıyla belirlediğiniz HTML eleman seçici dizesini kullanarak eşleşen HTML elemanlarını bulun ve bunlar üzerinde yineleme yapın ❼. Her bir eşleşen eleman için `handler()` fonksiyonunuza çağrı yapılır.

Kodun örnek bir çalıştırması aşağıdakine benzer bir çıktı üretir:

```bash
$ go run main.go nytimes.com docx
0: http://graphics8.nytimes.com/packages/pdf/2012NAINSAnnualHIVReport041713.docx
2020/12/21 11:53:50       Jonathan V. Iralu    Dan Frosch - Microsoft Macintosh Word 2010
   http://www.nytimes.com/packages/pdf/business/Announcement.docx
2020/12/21 11:53:51       agouser              agouser - Microsoft Office Outlook 2007
   http://www.nytimes.com/packages/pdf/business/DOCXIndictment.docx
2020/12/21 11:53:51       AGO                  Gonder, Nanci - Microsoft Office Word 2007
   http://www.nytimes.com/packages/pdf/business/BrownIndictment.docx
2020/12/21 11:53:51       AGO                  Gonder, Nanci - Microsoft Office Word 2007
   http://graphics8.nytimes.com/packages/pdf/health/Introduction.docx
2020/12/21 11:53:51       Oberg, Amanda M      Karen Barrow - Microsoft Macintosh Word 2010
```

Artık belirli bir alan adını hedeflerken tüm Open XML dosyalarının belge metadata’sını arayabilir ve çıkarabilirsiniz. Bu örneği genişleterek, çok sayfalı Bing arama sonuçları arasında gezinme mantığını eklemenizi, Open XML dışındaki diğer dosya türlerini de dahil etmenizi ve tespit edilen dosyaları eşzamanlı (concurrent) olarak indirmek için kodu geliştirmeyi denemenizi öneririm.

## Özet

Bu bölümde Go ile temel HTTP kavramlarıyla tanıştınız; bunları uzak API’lerle etkileşime giren ve rastgele HTML verilerini toplayan (scrape) kullanılabilir araçlar oluşturmak için kullandınız. Sonraki bölümde, istemciler yerine sunucular oluşturmayı öğrenerek HTTP temasına devam edeceksiniz.

---

# HTTP SUNUCULARI, YÖNLENDİRME VE MIDDLEWARE

Eğer sıfırdan HTTP sunucuları yazmayı biliyorsanız, sosyal mühendislik, komuta-kontrol (command-and-control, C2) taşımaları (transports) veya kendi araçlarınız için API’ler ve ön yüzler (frontend’ler) gibi şeyler için özelleştirilmiş mantık oluşturabilirsiniz. Neyse ki Go, HTTP sunucuları kurmak için mükemmel bir standart paket olan `net/http`'ya sahiptir; yalnızca basit sunucuları değil, aynı zamanda karmaşık, tam özellikli web uygulamalarını etkili bir şekilde yazmak için de gerçekten ihtiyacınız olan tek şey budur.

Standart pakete ek olarak, desen eşleştirme (pattern matching) gibi bazı zahmetli süreçleri ortadan kaldırarak geliştirmeyi hızlandırmak için üçüncü taraf paketlerden yararlanabilirsiniz. Bu paketler size yönlendirme (routing), middleware inşa etme, istekleri doğrulama ve diğer görevlerde yardımcı olur.

Bu bölümde önce basit uygulamalar kullanarak HTTP sunucuları oluşturmak için gereken birçok tekniği inceleyeceksiniz. Ardından bu teknikleri kullanarak iki sosyal mühendislik uygulaması—bir kimlik bilgisi toplama (credential-harvesting) sunucusu ve bir tuş kaydı (keylogging) sunucusu—ve çoklu C2 kanalları (multiplex C2 channels) oluşturacaksınız.

## HTTP Sunucusu Temelleri

Bu bölümde, basit sunucular, yönlendiriciler (routers) ve middleware oluşturarak `net/http` paketini ve kullanışlı üçüncü taraf paketleri inceleyeceksiniz. Bölümün ilerleyen kısımlarında bu temelleri daha kötü niyetli örnekleri kapsayacak şekilde genişleteceğiz.

### Basit Bir Sunucu Oluşturma

Liste 4-1’deki kod, tek bir path’e gelen istekleri işleyen bir sunucu başlatır. (`/` kök konumundaki tüm kod listeleri, verilen GitHub deposu `https://github.com/blackhat-go/bhg` altında bulunmaktadır.) Sunucu, bir kullanıcının adını içeren `name` URL parametresini bulmalı ve özelleştirilmiş bir selamlama ile yanıt vermelidir.

```go
package main

import (
   "fmt"
   "net/http"
)

func hello(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello %s\n", r.URL.Query().Get("name"))
}

func main() {
    http.HandleFunc("/hello", hello)
    http.ListenAndServe(":8000", nil)
}
```
