Liste 4-1: Bir Hello World sunucusu (`/ch-4/hello_world/main.go`)

Bu basit örnek `/hello` altında bir kaynak sunar. Bu kaynak, parametreyi alır ve değerini istemciye geri yansıtır. `main()` fonksiyonu içinde `http.HandleFunc()` 0 iki argüman alır: İlki, sunucunuza izlemesini söylediğiniz URL yolu desenini temsil eden bir string; ikincisi ise isteği gerçekten işleyecek fonksiyondur. İsterseniz fonksiyon tanımını anonim bir satır içi (inline) fonksiyon olarak da verebilirsiniz. Bu örnekte ise, daha önce tanımladığınız `hello()` adlı fonksiyonu geçiriyorsunuz.

`hello()` fonksiyonu istekleri işler ve istemciye bir selamlama (hello) mesajı döner. Kendisi iki argüman alır. İlki, isteğe verilen yanıtları yazmak için kullanılan `http.ResponseWriter`’dır. İkinci argüman ise, gelen istekteki bilgileri okumanızı sağlayacak olan `http.Request`’e işaretçi (pointer)’dir. Dikkat edin, `main` 0 fonksiyonundan `hello()` fonksiyonunu çağırmıyorsunuz. Yalnızca HTTP sunucunuza `/hello` için gelen tüm isteklerin `hello` adlı bir fonksiyon tarafından ele alınması gerektiğini söylüyorsunuz.

Peki, arka planda `http.HandleFunc()` gerçekte ne yapar? Go dokümantasyonu, bu fonksiyonun işleyiciyi (handler) `DefaultServerMux` üzerine yerleştirdiğini söyler. `ServerMux`, server multiplexer’ın kısaltmasıdır; bu da alttaki kodun birden fazla HTTP isteğini desenler ve fonksiyonlar için işleyebildiğini söylemenin süslü bir yoludur. Bunu, her gelen istek için bir goroutine kullanarak yapar.

`net/http` paketini içe aktarmak (import etmek) bir `ServerMux` oluşturur ve onu bu paketin isim alanına (namespace) bağlar; bu da `DefaultServerMux`’tur.

Sonraki satır, `http.ListenAndServe()` 49 çağrısıdır; string ve `http.Handler` türünde iki argüman alır. İlk argümanı adres olarak kullanarak bir HTTP sunucusu başlatır. Bu durumda bu değer `:8000`’dır; bu da sunucunun tüm arayüzlerde (interfaces) 8000 numaralı portu dinlemesi gerektiği anlamına gelir. İkinci argüman olan `http.Handler` için `nil` geçiriyorsunuz. Sonuç olarak, paket alttaki işleyici olarak `DefaultServerMux`’u kullanır. Birazdan kendi `http.Handler` implementasyonunuzu yazacak ve onu geçireceksiniz ama şimdilik varsayılanı kullanacaksınız. Ayrıca, açıklamasının da belirttiği gibi HTTPS ve TLS kullanarak bir sunucu başlatacak olan `http.ListenAndServeTLS()`’i de kullanabilirsiniz; ancak bu ek parametreler gerektirir.

`http.Handler` arayüzünü (interface) uygulamak (implement etmek) için tek bir metoda ihtiyaç vardır: `ServeHTTP(http.ResponseWriter, *http.Request)`. Bu harikadır, çünkü kendi özel HTTP sunucularınızı oluşturmayı basitleştirir. `net/http` fonksiyonelliğini genişleterek middleware, kimlik doğrulama (authentication), yanıt kodlama (response encoding) ve daha fazlası gibi özellikler ekleyen sayısız üçüncü taraf implementasyon bulacaksınız.

Bu sunucuyu `curl` kullanarak test edebilirsiniz:

```bash
$ curl -i http://localhost:8000/hello?name=alice
HTTP/1.1 200 OK
Date: Sun, 12 Jan 2020 01:18:26 GMT
Content-Length: 12
Content-Type: text/plain; charset=utf-8

Hello alice
```

Mükemmel! Kurduğunuz sunucu, `name` URL parametresini okuyor ve bir selamlama ile yanıt veriyor.

## Basit Bir Router (yönlendirici) Oluşturma

Şimdi, URL yolunu inceleyerek gelen istekleri dinamik olarak nasıl işleyeceğinizi gösteren, Liste 4-2’deki basit bir router’ı oluşturacaksınız. URL yolu `/a`, `/b` veya `/c` içeriyorsa, sırasıyla `Executing /a`, `Executing /b` veya `Executing /c` mesajını yazdıracaksınız. Diğer her şey için ise `404 Not Found` hatası döndüreceksiniz.

```go
package main

import (

    "net/http"

type router struct {

func (r *router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    switch req.URL.Path {
    case "/a":
        fmt.Fprint(w, "Executing /a")
    case "/b":
        fmt.Fprint(w, "Executing /b")
    case "/c":
        fmt.Fprint(w, "Executing /c")
    default:
        http.Error(w, "404 Not Found", 404)
    }
}

func main() {
    var r router
    http.ListenAndServe(":8000", &r)
}
```

Liste 4-2: Basit bir router (`/ch-4/simple_router/main.go`)

İlk olarak, herhangi bir alanı (field) olmayan `router` adında yeni bir type tanımlıyorsunuz 0. Bunu `http.Handler` arayüzünü uygulamak için kullanacaksınız. Bunu yapmak için `ServeHTTP()` metodunu tanımlamalısınız 0. Metot, isteğin URL yolu üzerinde bir `switch` ifadesi kullanır 0 ve yola bağlı olarak farklı mantık yürütür. Varsayılan olarak bir `404 Not Found` yanıtı döner. `main()` içinde yeni bir router oluşturur ve ilgili işaretçisini `http.ListenAndServe()` fonksiyonuna geçirirsiniz 0.

Şimdi bunu terminalde bir deneyelim:

```bash
$ curl http://localhost:8000/a
Executing /a
$ curl http://localhost:8000/d
404 Not Found
```

Her şey beklendiği gibi çalışıyor; program, `/a` yolunu içeren bir URL için `Executing /a` mesajını döndürüyor ve var olmayan bir yol için 404 yanıtı veriyor. Bu önemsiz (trivial) bir örnek. Kullanacağınız üçüncü taraf router’lar çok daha karmaşık mantığa sahip olacak ancak bu örnek, nasıl çalıştıklarına dair temel bir fikir vermeli.

## Basit Middleware Oluşturma

Şimdi, hedef fonksiyon ne olursa olsun tüm gelen istekler üzerinde çalışacak bir tür sarmalayıcı (wrapper) olan middleware yazalım. Liste 4-3’teki örnekte, isteğin işlenmeye başlama ve bitiş zamanını gösteren bir logger oluşturacaksınız.

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "time"
)

type logger struct {
    Inner http.Handler
}

func (l *logger) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    log.Println("start")
    l.Inner.ServeHTTP(w, r)
    log.Println("finish")
}

func hello(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello\n")
}

func main() {
    f := http.HandlerFunc(hello)
    l := logger{Inner: f}
    http.ListenAndServe(":8000", &l)
}
```

Liste 4-3: Basit middleware (`/ch-4/simple_middleware/main.go`)
