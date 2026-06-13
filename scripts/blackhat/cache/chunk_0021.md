HTTP İstemcileri ve Araçlarla Uzaktan Etkileşim   47

## Bir İstek Üretmek

Bu HTTP fiillerinden (verbs) biriyle bir istek üretmek için `NewRequest()` fonksiyonunu kullanarak bir `Request` struct’ı oluşturabilir ve ardından bunu `Client` fonksiyonunun `Do()` metodu ile gönderirsiniz. Kulağa olduğundan daha karmaşık geliyor; aslında oldukça basit. `http.NewRequest()` fonksiyon prototipi şöyledir:

```go
func NewRequest(method, url string, body io.Reader) (req *Request, err error)
```

`NewRequest()` fonksiyonuna ilk iki string parametre olarak HTTP fiilini (`method`) ve hedef URL'yi (`url`) sağlamanız gerekir. Liste 3-1'deki ilk POST örneğine benzer şekilde, üçüncü ve son parametre olarak bir `io.Reader` geçirerek isteğin gövdesini (body) isteğe bağlı olarak sağlayabilirsiniz.

Liste 3-3, HTTP gövdesi olmadan yapılan bir çağrıyı—bir DELETE isteğini—göstermektedir.

```go
req, err := http.NewRequest("DELETE", "https://www.google.com/robots.txt", nil)
var client http.Client
resp, err := client.Do(req)
// Read response body and close.
```

**Liste 3-3: Bir DELETE isteği gönderme (/ch-3/basic/main.go)**

Şimdi, Liste 3-4 bir `io.Reader` gövdesi ile yapılan bir PUT isteğini göstermektedir (bir PATCH isteği de buna benzer görünür).

```go
form := url.Values{}
form.Add("foo", "bar")
var client http.Client
req, err := http.NewRequest(
    "PUT",
    "https://www.google.com/robots.txt",
    strings.NewReader(form.Encode()),
)

resp, err := client.Do(req)
// Read response body and close.
```

**Liste 3-4: Bir PUT isteği gönderme (/ch-3/basic/main.go)**

Standart Go `net/http` kütüphanesi, isteği sunucuya gönderilmeden önce üzerinde değişiklik yapabilmeniz için kullanabileceğiniz birkaç fonksiyon içerir. Bu bölüm boyunca üzerinde çalışacağınız pratik örnekler sayesinde en ilgili ve uygulanabilir varyantlardan bazılarını öğreneceksiniz. Ancak önce, sunucunun aldığı HTTP yanıtı ile anlamlı bir şey nasıl yapılır, onu göstereceğiz.

## Yapılandırılmış Yanıt Ayrıştırma Kullanma

Önceki bölümde, Go'da HTTP istekleri oluşturma ve gönderme mekanizmalarını öğrendiniz. Bu örneklerin her biri, yanıt işlemesini yüzeysel geçti ve şimdilik büyük ölçüde yok saydı. Oysa HTTP yanıtının çeşitli bileşenlerini incelemek—yanıt gövdesini okumak, çerezlere (cookies) ve başlıklara (headers) erişmek ya da sadece HTTP durum kodunu kontrol etmek gibi—HTTP ile ilgili herhangi bir görevin kritik bir parçasıdır.

Liste 3-5, Liste 3-1'deki GET isteğini geliştirerek durum kodunu ve yanıt gövdesini gösterir—bu durumda Google'ın `robots.txt` dosyası. `ioutil.ReadAll()` fonksiyonunu kullanarak yanıt gövdesinden veri okur, hata kontrolü yapar ve HTTP durum kodunu ve yanıt gövdesini `stdout`'a yazdırır.

```go
resp, err := http.Get("https://www.google.com/robots.txt")
if err != nil {
    log.Panicln(err)
}
// Print HTTP Status
fmt.Println(resp.Status)

// Read and display response body
body, err := ioutil.ReadAll(resp.Body)
if err != nil {
    log.Panicln(err)
}
fmt.Println(string(body))
resp.Body.Close()
```

**Liste 3-5: HTTP yanıt gövdesini işleme (/ch-3/basic/main.go)**

Yanıtınızı (yukarıdaki koddaki `resp`) aldıktan sonra, dışa açık `Status` parametresine erişerek (örneğin, `200 OK`) durum string'ini elde edebilirsiniz; örnekte gösterilmemiş olsa da, durum string'inin yalnızca tam sayı kısmına erişen benzer bir `StatusCode` parametresi de vardır.

`Response` tipi, türü `io.ReadCloser` olan dışa açık bir `Body` parametresi içerir. Bir `io.ReadCloser`, hem bir `io.Reader` hem de bir `io.Closer` gibi davranan bir arayüzdür (interface); yani okuyucuyu (reader) kapatmak ve gerekli temizliği yapmak için bir `Close()` fonksiyonunun implement edilmesini gerektirir. Ayrıntılar çok da önemli değil; sadece şunu bilin: Bir `io.ReadCloser`'dan verileri okuduktan sonra yanıt gövdesi üzerinde `Close()` fonksiyonunu çağırmanız gerekir. Yanıt gövdesini kapatmak için `defer` kullanmak yaygın bir uygulamadır; bu, fonksiyondan dönmeden önce gövdenin kapatılmasını garanti eder.

Şimdi, hata durumunu ve yanıt gövdesini görmek için script'i çalıştırın:

```bash
$ go run main.go
200 OK
User-agent: *
Disallow: /search
Allow: /search/about
Disallow: /sdch
Disallow: /groups
Disallow: /index.html?
Disallow: /?
Allow: /?hl=
Disallow: /?hl=*&
Allow: /?hl=*&gws_rd=ssl$
Disallow: /?hl=*&*&gws_rd=ssl
--snip--
```

Daha yapılandırılmış verileri ayrıştırmanız gereken bir durumla karşılaşırsanız—ki muhtemelen karşılaşacaksınız—yanıt gövdesini okuyabilir ve 2. Bölüm'de sunulan kuralları kullanarak decode edebilirsiniz. Örneğin, JSON kullanan bir API ile etkileşimde bulunduğunuzu ve bir uç noktanın (endpoint)—örneğin `/ping`—sunucunun durumunu gösteren aşağıdaki yanıtı döndürdüğünü varsayın:

```text
{"Message":"All is good with the world","Status":"Success"}
```

Bu uç noktayla etkileşime geçebilir ve Liste 3-6'daki programı kullanarak JSON mesajını decode edebilirsiniz.

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Status struct {
    Message string
    Status  string
}

func main() {
    res, err := http.Post(
        "http://IP:PORT/ping",
        "application/json",
        nil,
    )

    if err != nil {
        log.Fatalln(err)
    }

    var status Status
    if err := json.NewDecoder(res.Body).Decode(&status); err != nil {
        log.Fatalln(err)
    }

    defer res.Body.Close()
    log.Printf("%s -> %s\n", status.Status, status.Message)
}
```

**Liste 3-6: Bir JSON yanıt gövdesini decode etme (/ch-3/basic-parsing/main.go)**

Kod, sunucu yanıtından beklenen elemanları içeren `Status` adlı bir struct tanımlayarak başlar. `main()` fonksiyonu önce POST isteğini gönderir ve ardından yanıt gövdesini decode eder.
