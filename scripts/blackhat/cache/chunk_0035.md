Bu uygulama, önceki örneklerden biraz farklıdır. Daha önce `http.Handler` arayüzünü (interface) uyguluyordunuz; bu arayüz, iki parametre alan bir `ServeHTTP()` metodu bekliyordu: `http.ResponseWriter` ve `*http.Request`. Bu yeni örnekte, `http.Handler` arayüzü yerine `negroni.Handler` arayüzünü uyguluyorsunuz.

Aradaki küçük fark, `negroni.Handler` arayüzünün sizden iki değil, üç parametre alan bir `ServeHTTP()` metodu uygulamanızı beklemesidir: `http.ResponseWriter`, `*http.Request` ve `http.HandlerFunc`. `http.HandlerFunc` parametresi, zincirdeki bir sonraki middleware fonksiyonunu temsil eder. Bizim amaçlarımız için, ona `next` adını veriyorsunuz. İşlemenizi `ServeHTTP()` içerisinde yapıyor, ardından ilk başta aldığınız `http.ResponseWriter` ve `*http.Request` değerlerini ona geçirerek `next()` çağırıyorsunuz. Bu, yürütmeyi (execution) zincirde aşağıya doğru devretmiş olur.

Ama hâlâ negroni'ye, sizin implementasyonunuzu middleware zincirinin bir parçası olarak kullanmasını söylemeniz gerekir. Bunu, negroni'nin `Use` metodunu çağırıp `negroni.Handler` implementasyonunuzun bir örneğini ona vererek yapabilirsiniz:

```go
n.Use(&trivial{})
```

###  

Bu yöntemi kullanarak middleware yazmak, yürütmeyi bir sonraki middleware'e kolayca devredebileceğiniz için kullanışlıdır. Bunun bir dezavantajı var: yazdığınız her şey negroni kullanmak zorunda kalır. Örneğin, bir yanıta güvenlik başlıkları (security headers) yazan bir middleware paketi yazsaydınız, bunun `http.Handler` implement etmesini isterdiniz; böylece onu diğer uygulama yığınlarında da kullanabilirdiniz, çünkü çoğu yığın `negroni.Handler` beklemez. Yani, middleware'inizin amacından bağımsız olarak, negroni middleware'ini negroni olmayan bir yığında kullanmaya çalışırken (veya tam tersi) uyumluluk sorunları ortaya çıkabilir.

Negroni'ye middleware'inizi kullanmasını söylemenin iki yolu daha vardır. İlki, zaten aşina olduğunuz `UseHandler(handler http.Handler)` çağrısıdır. İkinci yol, `UseHandlerFunc(handlerFunc func(w http.ResponseWriter, r *http.Request))` çağrısını yapmaktır. Bu ikinci yöntem, zincirdeki bir sonraki middleware'in yürütülmesini atlamanıza izin vermediği için, sık kullanmak isteyeceğiniz bir şey değildir. Örneğin, kimlik doğrulama (authentication) yapan bir middleware yazıyor olsaydınız, kimlik bilgileri veya oturum (session) bilgileri geçersizse bir 401 yanıtı döndürmek ve yürütmeyi durdurmak isterdiniz; bu yöntemle bunu yapmanın bir yolu yoktur.

## Negroni ile Kimlik Doğrulama Eklemek

Devam etmeden önce, fonksiyonlar arasında değişkenleri kolayca aktarabilen context kullanımını göstermek için önceki bölümdeki örneğimizi değiştirelim. Liste 4-5'teki örnek, kimlik doğrulama middleware'i eklemek için negroni kullanıyor.

```go
package main

import (
   "context"
   "fmt"
   "net/http"

   "github.com/gorilla/mux"
   "github.com/urfave/negroni"
)

type badAuth struct {
    Username string
    Password string
}

func (b *badAuth) ServeHTTP(w http.ResponseWriter, r *http.Request, next http.HandlerFunc) {
    username := r.URL.Query().Get("username")
    password := r.URL.Query().Get("password")
    if username != b.Username || password != b.Password {
         http.Error(w, "Unauthorized", 401)
         return
     }
     ctx := context.WithValue(r.Context(), "username", username)
     r = r.WithContext(ctx)
     next(w, r)
}

func hello(w http.ResponseWriter, r *http.Request) {
    username := r.Context().Value("username").(string)
    fmt.Fprintf(w, "Hi %s\n", username)
}

func main() {
    r := mux.NewRouter()
    r.HandleFunc("/hello", hello).Methods("GET")
    n := negroni.Classic()
    n.Use(&badAuth{
         Username: "admin",
         Password: "password",
    })
    n.UseHandler(r)
    http.ListenAndServe(":8000", n)
}
```

**Liste 4-5:** Handler'larda context kullanımı (`ch-4/negroni_example/main.go`)

Yeni bir middleware olan `badAuth` eklediniz; bu middleware yalnızca gösterim amacıyla kimlik doğrulamayı taklit edecek. Bu yeni tipin iki alanı var: `Username` ve `Password`. Ayrıca, üç parametre alan `ServeHTTP()` metodunun sürümünü tanımladığı için `negroni.Handler` arayüzünü implement ediyor; bunu önceki kısımda tartışmıştık. `ServeHTTP()` metodunun içinde önce istekten kullanıcı adı ve parolayı alıyor, sonra bunları elinizdeki alanlarla karşılaştırıyorsunuz. Kullanıcı adı ve parola yanlışsa, yürütme durdurulur ve istemciye bir 401 yanıtı yazılır.

`next()` fonksiyonunu çağırmadan önce `return` ettiğinize dikkat edin. Bu, middleware zincirinin geri kalanının yürütülmesini engeller. Kimlik bilgileri doğruysa, kullanıcı adını istek context'ine eklemek için oldukça ayrıntılı bir rutin izliyorsunuz. Önce `context.WithValue()` fonksiyonunu çağırarak context'i isteğin context'inden başlatıyor ve bu context üzerinde `username` adlı bir değişken ayarlıyorsunuz. Ardından `r.WithContext(ctx)` çağrısıyla isteğin yeni context'inizi kullandığından emin oluyorsunuz. Go ile web uygulamaları yazmayı planlıyorsanız, bu desene (pattern) alışmak isteyeceksiniz; çünkü bunu sık sık kullanacaksınız.

`hello()` fonksiyonunda, istek context'inden `Context.Value(interface{})` fonksiyonunu kullanarak kullanıcı adını alıyorsunuz; bu fonksiyon bir `interface{}` döndürür. Bunun bir `string` olduğunu bildiğiniz için burada bir tür iddiası (type assertion) kullanabilirsiniz. Türü garanti edemiyorsanız veya değerin context içinde var olacağını garanti edemiyorsanız, dönüşüm için `switch` yapısı kullanın.

Liste 4-5'teki kodu derleyip çalıştırın ve sunucuya birkaç istek gönderin. Hem doğru hem de yanlış kimlik bilgileriyle bazı istekler gönderin. Aşağıdaki çıktıyı görmelisiniz:

```bash
$ curl -i http://localhost:8000/hello
HTTP/1.1 401 Unauthorized
Content-Type: text/plain; charset=utf-8
X-Content-Type-Options: nosniff
Date: Thu, 16 Jan 2020 20:41:20 GMT
Content-Length: 13
```
