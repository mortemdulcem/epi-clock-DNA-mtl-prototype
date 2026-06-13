Ne yapmış olduğunuz şey, her istekte sunucuda bazı bilgileri loglayan ve `hello()` fonksiyonunuzu çağıran dış bir handler (işleyici) oluşturmak. Bu loglama mantığını fonksiyonunuzun etrafına sarıyorsunuz.

Yönlendirme (routing) örneğinde olduğu gibi, `logger` adlı yeni bir tür (type) tanımlıyorsunuz; ancak bu kez `Inner` adlı ve kendisi de bir `http.Handler` olan bir alanınız (field) var. `ServeHTTP()` tanımınızda 0, isteğin başlangıç ve bitiş zamanlarını yazdırmak için `log()` kullanıyor, bu sırada iç handler'ın `ServeHTTP()` metodunu çağırıyorsunuz 0. İstemci açısından istek, iç handler'ın içinde tamamlanıyor. `main()` fonksiyonu içinde bir fonksiyondan `http.Handler` oluşturmak için `http.HandlerFunc()` kullanıyorsunuz 0. `logger` nesnesini oluşturuyor ve `Inner` alanını yeni oluşturduğunuz handler'a atıyorsunuz 0. Son olarak, sunucuyu, bir `logger` örneğine işaretçi (pointer) kullanarak başlatıyorsunuz.

Bunu çalıştırıp bir istek gönderdiğinizde, isteğin başlangıç ve bitiş zamanlarını içeren iki mesaj çıktısı alırsınız:

```bash
$ go build -o simple_middleware
$ ./simple_middleware
2020/01/16 06:23:14 start
2020/01/16 06:23:14 finish
```

İzleyen bölümlerde, middleware ve routing konularına daha derinlemesine girecek ve bazı favori üçüncü taraf paketlerimizi kullanacağız. Bu paketler, daha dinamik rotalar oluşturmanıza ve middleware’i bir zincir içinde çalıştırmanıza olanak tanır. Ayrıca, middleware’in daha karmaşık senaryolara uzanan kullanım alanlarını da tartışacağız.

## gorilla/mux Paketi ile Routing

Liste 4-2’de gösterildiği gibi, bir isteğin yolunu (path) bir fonksiyonla eşleştirmek için routing kullanabilirsiniz. Fakat routing’i, HTTP verb veya host header gibi diğer özellikleri bir fonksiyonla eşleştirmek için de kullanabilirsiniz. Go ekosisteminde birkaç üçüncü taraf router mevcuttur. Bu bölümde, bunlardan biri olan `gorilla/mux` paketini tanıtacağız. Ancak her konuda olduğu gibi, karşılaştıkça başka paketleri de araştırarak bilginizi genişletmenizi öneririz.

`gorilla/mux` paketi, hem basit hem karmaşık kalıplara (pattern) göre routing yapmanıza izin veren olgun bir üçüncü taraf routing paketidir. Düzenli ifadeler (regular expressions), parametre eşleştirme, verb eşleştirme ve alt routing (sub routing) gibi özellikler içerir.

Router’ı nasıl kullanabileceğinize dair birkaç örnek üzerinden geçelim. Bunları çalıştırmanıza gerek yok; yakında gerçek bir programda kullanacaksınız, ancak denemek ve kurcalamak isterseniz elbette deneyebilirsiniz.

`gorilla/mux` kullanmadan önce, paketi `go get` ile indirmeniz gerekir:

```bash
$ go get github.com/gorilla/mux
```

Artık routing’e başlayabilirsiniz. Router’ınızı `mux.NewRouter()` kullanarak oluşturun:

```go
r := mux.NewRouter()
```

Dönen tür `http.Handler` arayüzünü uygular ancak buna ek olarak birçok ilişkili metoda da sahiptir. En sık kullanacağınız metot `HandleFunc()` olacaktır. Örneğin, `/foo` kalıbına gelen GET isteklerini işlemek için yeni bir route tanımlamak isterseniz, şunu kullanabilirsiniz:

```go
r.HandleFunc("/foo", func(w http.ResponseWriter, req *http.Request) {
    fmt.Fprint(w, "hi foo")
}).Methods("GET")
```

Burada `Methods()` 0 çağrısı sayesinde yalnızca GET istekleri bu route ile eşleşecektir. Diğer tüm HTTP metodları için 404 yanıtı dönecektir. Bunun üzerine `Host(string)` gibi başka niteleyiciler de zincirleyebilirsiniz; bu, belirli bir host header değerini eşleştirir. Örneğin, aşağıdaki kod yalnızca host header’ı `www.foo.com` olan isteklerle eşleşir:

```go
r.HandleFunc("/foo", func(w http.ResponseWriter, req *http.Request) {
    fmt.Fprint(w, "hi foo")
}).Methods("GET").Host("www.foo.com")
```

Bazen istek yolunun (request path) içinde parametreleri eşleştirmek ve aktarmak faydalıdır (örneğin bir RESTful API uygularken). `gorilla/mux` ile bu oldukça kolaydır. Aşağıdaki örnek, isteğin yolunda `/users/` ifadesini takip eden her şeyi ekrana basar:

```go
r.HandleFunc("/users/{user}", func(w http.ResponseWriter, req *http.Request) {
    user := mux.Vars(req)["user"]
    fmt.Fprintf(w, "hi %s\n", user)
}).Methods("GET")
```

Yol tanımında, istek parametresini tanımlamak için süslü parantezler kullanıyorsunuz. Bunu isimlendirilmiş bir yer tutucu (placeholder) olarak düşünebilirsiniz. Ardından, handler fonksiyonunun içinde, istek nesnesini (request object) vererek `mux.Vars()` fonksiyonunu çağırıyorsunuz; bu fonksiyon `map[string]string` türünde, istek parametresi adlarını ilgili değerlerine eşleyen bir `map` döndürür. Anahtar olarak isimlendirilmiş yer tutucu `user`’ı verirsiniz. Böylece `/users/bob` isteği, Bob için bir selamlama üretir:

```bash
$ curl http://localhost:8000/users/bob
hi bob
```

Bunu bir adım daha ileri götürerek, aktarılan kalıpları nitelemek için bir düzenli ifade kullanabilirsiniz. Örneğin, `user` parametresinin yalnızca küçük harflerden oluşması gerektiğini belirtebilirsiniz:

```go
r.HandleFunc("/users/{user:[a-z]+}", func(w http.ResponseWriter, req *http.Request) {
    user := mux.Vars(req)["user"]
    fmt.Fprintf(w, "hi %s\n", user)
}).Methods("GET")
```

Artık bu kalıpla eşleşmeyen tüm istekler 404 yanıtı döndürecektir:

```bash
$ curl -i http://localhost:8000/users/bob1
HTTP/1.1 404 Not Found
```

Bir sonraki bölümde, routing kavramını genişleterek başka kütüphaneler kullanarak middleware uygulamalarını da dahil edeceğiz. Bu, HTTP isteklerini ele alırken size daha fazla esneklik sağlayacak.
