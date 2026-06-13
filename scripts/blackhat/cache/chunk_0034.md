## Negroni ile Middleware Oluşturma

Daha önce gösterdiğimiz basit middleware, bir isteğin işlenmesinin başlangıç ve bitiş zamanlarını kaydediyor ve yanıtı döndürüyordu. Middleware her gelen istek üzerinde çalışmak zorunda değildir, ancak çoğu zaman böyle olur. Middleware kullanmak için birçok neden vardır; bunlar arasında istekleri loglama, kullanıcıları kimlik doğrulama ve yetkilendirme, kaynak eşleme (resource mapping) sayılabilir.

Örneğin, basit kimlik doğrulama (basic authentication) yapmak için bir middleware yazabilirsiniz. Bu middleware, her istek için bir `authorization` başlığını ayrıştırabilir, sağlanan kullanıcı adı ve parolayı doğrulayabilir ve kimlik bilgileri (credentials) geçersizse 401 yanıtı dönebilir. Ayrıca birden fazla middleware fonksiyonunu öyle bir zincir halinde bağlayabilirsiniz ki, bir tanesi çalıştıktan sonra tanımlanan bir sonraki middleware çalışsın.

Bu bölümün başlarında oluşturduğunuz logging middleware için yalnızca tek bir fonksiyonu sarmalamıştınız. Pratikte bu pek kullanışlı değildir, çünkü birden fazla middleware kullanmak istersiniz ve bunu yapmak için bunları bir zincir halinde, art arda çalıştırabilecek bir mantığa ihtiyacınız vardır. Bunu sıfırdan yazmak aşırı zor değildir, ama yeniden tekerleği icat etmeyelim. Burada, bunu zaten yapabilen, olgun bir paket kullanacaksınız: `negroni`.

`negroni` paketini `https://github.com/urfave/negroni` adresinde bulabilirsiniz; güzel tarafı, sizi daha büyük bir çatı (framework) yapıya bağlamamasıdır. Kolayca başka framework’lere eklenebilir ve oldukça esnektir.

Negroni ayrıca birçok uygulama için faydalı olan varsayılan middleware’lerle birlikte gelir. Başlamadan önce `negroni`yi indirmeniz gerekir:

```bash
$ go get github.com/urfave/negroni
```

Teknik olarak `negroni`yi tüm uygulama mantığınız için kullanabilirsiniz, ancak bunu yapmak ideal değildir; çünkü `negroni`, middleware olarak kullanılmak üzere özel olarak tasarlanmıştır ve bir router içermez. Bunun yerine `negroni`yi `gorilla/mux` veya `net/http` gibi başka bir paketle birlikte kullanmak en iyisidir. `negroni` ile tanışmanızı sağlayacak ve middleware zinciri boyunca işlem sırasını görselleştirmenize imkân verecek bir programı `gorilla/mux` kullanarak yazalım.

Öncelikle, `github.com/blackhat-go/bhg/ch-4/negroni_example/` gibi bir dizin isim alanı (namespace) içinde `main.go` adında yeni bir dosya oluşturun. (Bu isim alanı, BHG Github deposunu klonladıysanız zaten oluşturulmuş olacaktır.) Şimdi `main.go` dosyanızı aşağıdaki kodu içerecek şekilde değiştirin.

```go
package main

import (
    "net/http"

    "github.com/gorilla/mux"
    "github.com/urfave/negroni"
)

func main() {
    r := mux.NewRouter()
    n := negroni.Classic()
    n.UseHandler(r)
    http.ListenAndServe(":8000", n)
}
```

**Liste 4-4: Negroni örneği (`/ch-4/negroni_example/main.go`)**

İlk olarak, bu bölümün başlarında yaptığınız gibi `mux.NewRouter()` çağırarak bir router oluşturursunuz ➊. Sonra `negroni` paketiyle ilk etkileşiminiz gelir: `negroni.Classic()` ➋ fonksiyonunu çağırırsınız. Bu, bir Negroni örneğine işaretçi (pointer) oluşturur.

Bunu yapmanın farklı yolları vardır. `negroni.Classic()` kullanabilir veya `negroni.New()` çağırabilirsiniz. İlk seçenek olan `negroni.Classic()`, varsayılan middleware’leri ayarlar; bunlar arasında bir istek logger’ı, `panic`leri yakalayıp kurtaran (recovery) middleware ve aynı dizindeki `public` klasöründen dosya servis eden middleware bulunur. `negroni.New()` fonksiyonu ise herhangi bir varsayılan middleware oluşturmaz.

Her bir middleware türü `negroni` paketi içinde mevcuttur. Örneğin, recovery paketini şu şekilde kullanabilirsiniz:

```go
n.Use(negroni.NewRecovery())
```

Sonraki adımda, `n.UseHandler(r)` ➌ çağrısı yaparak router’ınızı middleware yığınına (stack) eklersiniz. Middleware’lerinizi tasarlamaya ve inşa etmeye devam ederken, çalıştırılma sırasını göz önünde bulundurun. Örneğin, kimlik doğrulama denetimi yapan middleware’inizin, kimlik doğrulaması gerektiren handler fonksiyonlarından önce çalışmasını isteyeceksiniz. Router’dan önce eklenen tüm middleware’ler handler fonksiyonlarınızdan önce; router’dan sonra eklenenler ise handler fonksiyonlarınızdan sonra çalışır. Sıra (order) önemlidir. Bu durumda, henüz özel bir middleware tanımlamadınız, ama az sonra yapacaksınız.

Liste 4-4’te oluşturduğunuz sunucuyu derleyin ve çalıştırın. Ardından `http://localhost:8000` adresine web istekleri gönderin. `negroni` logging middleware’inin `stdout`a bilgi yazdığını görmelisiniz; aşağıda gösterildiği gibi. Çıktı; zaman damgasını, yanıt kodunu, işlem süresini, host’u ve HTTP metodunu gösterir:

```bash
$ go build -o negroni_example
$ ./negroni_example
[negroni] 2020-01-19T11:49:33-07:00 | 404 | 1.0002ms | localhost:8000 | GET
```

Varsayılan middleware’lere sahip olmak güzel, ancak asıl güç kendi middleware’inizi oluşturduğunuzda ortaya çıkar. `negroni` ile, yığına middleware eklemek için birkaç yöntem kullanabilirsiniz. Aşağıdaki koda bakın. Bu kod, bir mesaj yazdıran ve zincirdeki bir sonraki middleware’e çalışmayı devreden önemsiz (trivial) bir middleware oluşturur:

```go
type trivial struct {
}

func (t *trivial) ServeHTTP(w http.ResponseWriter, r *http.Request, next http.HandlerFunc) {
    fmt.Println("Executing trivial middleware")
    next(w, r)
}
```
