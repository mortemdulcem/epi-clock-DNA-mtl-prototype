### API Çağrılarını Temizlemek

Shodan API dokümantasyonunu incelediğinizde, açığa çıkan her fonksiyonun API anahtarınızı (`API key`) göndermenizi gerektirdiğini fark etmiş olabilirsiniz. Elbette, yazacağınız her tüketici fonksiyona bu değeri parametre olarak iletebilirsiniz; ancak bu tekrarlayan iş oldukça sıkıcı hale gelir. Aynı durum, temel URL'yi (`https://api.shodan.io`) sabitlemek (hardcode etmek) veya her seferinde ayrıca ele almak için de geçerlidir. Örneğin, API fonksiyonlarınızı aşağıdaki parçadaki gibi tanımlamak, her fonksiyona token ve URL geçirmenizi gerektirir; bu da pek zarif değildir:

```go
func APIInfo(token, url string) { --snip-- }
func HostSearch(token, url string) { --snip-- }
```

Bunun yerine, daha idiomatik bir çözümü tercih ederek hem tuş vuruşlarından tasarruf edebilir hem de argümanlı olarak kodunuzu daha okunabilir hale getirebilirsiniz. Bunu yapmak için bir `shodan.go` dosyası oluşturun ve Liste 3-7’deki kodu girin.

```go
package shodan

const BaseURL = "https://api.shodan.io"

type Client struct {
    apiKey string
}

func New(apiKey string) *Client {
    return &Client{apiKey: apiKey}
}
```

**Liste 3-7** Shodan `Client` tanımı (`/ch-3/shodan/shodan/shodan.go`)

Shodan URL'si sabit (`const`) bir değer olarak tanımlanmıştır; böylece uygulayıcı fonksiyonlarınız içinde bu değere kolayca erişip tekrar kullanabilirsiniz. Shodan bir gün API'sinin URL'sini değiştirirse, tüm kod tabanınızı düzeltmek için yalnızca bu tek konumda değişiklik yapmanız yeterli olur. Sonraki adımda, istekler arasında API token’ınızı korumak için kullanılan bir `Client` struct tanımlarsınız. Son olarak, girdi olarak API token’ını alan ve başlatılmış bir `Client` örneği oluşturarak döndüren bir `New()` yardımcı fonksiyon tanımlarsınız. Artık API kodunuzu rastgele fonksiyonlar olarak yazmak yerine, `Client` struct’ı üzerinde metodlar olarak oluşturursunuz; bu da örneği sorgulamanıza (interrogate) olanak tanır.

Fonksiyon parametrelerine gereğinden fazla veri yüklemek yerine doğrudan `Client` örneği üzerinden çalışabilirsiniz. API fonksiyon çağrılarınızı, birazdan ayrıntılı olarak ele alacağımız şekilde, aşağıdaki biçime dönüştürebilirsiniz:

```go
func (s *Client) APIInfo() { --snip-- }
func (s *Client) HostSearch() { --snip-- }
```

Bunlar `Client` struct’ı üzerinde metodlar olduğundan, API anahtarını `s.apiKey` ile, URL’yi ise `BaseURL` üzerinden alabilirsiniz. Bu metodları çağırmadan önce gereken tek şey, `Client` struct’ından bir örnek yaratmanızdır. Bunu da `shodan.go` içindeki `New()` yardımcı fonksiyonu ile yapabilirsiniz.

### Shodan Aboneliğinizi Sorgulamak

Şimdi Shodan ile etkileşime başlamaya hazırsınız. Shodan API dokümantasyonuna göre, abonelik planı bilgilerinizi sorgulamak için yapılacak çağrı aşağıdaki gibidir:

```
https://api.shodan.io/api-info?key={YOUR API KEY}
```

Dönen yanıt aşağıdaki yapıya benzer olacaktır. Elbette, değerler abonelik planı detaylarınıza ve kalan abonelik kredilerinize göre değişecektir.

```json
"query_credits": 56,
"scan_credits": 0,
"telnet": true,
"plan": "developer",
"https": true,
"unlocked": true,
```

Öncelikle, `api.go` içinde JSON yanıtını bir Go struct’a unmarshalle etmek için kullanılacak bir tip tanımlamanız gerekir. Bu olmadan, yanıt gövdesini işleyemez veya sorgulayamazsınız. Bu örnekte tipe `APIInfo` adını verin:

```go
type APIInfo struct {
    QueryCredits int    `json:"query_credits"`
    ScanCredits  int    `json:"scan_credits"`
    Telnet       bool   `json:"telnet"`
    Plan         string `json:"plan"`
    HTTPS        bool   `json:"https"`
    Unlocked     bool   `json:"unlocked"`
}
```

Go’nun harikalığı, bu struct ile JSON hizalamasını tam bir keyif haline getirir. Bölüm 1’de gösterildiği gibi, alanları sizin yerinize dolduracak “otomatik” JSON ayrıştırma araçlarını kullanabilirsiniz. Struct üzerinde dışa açık (exported) olan her tip için, veri doğru şekilde eşlenip ayrıştırılsın diye struct tag’leri ile JSON eleman adını açıkça tanımlarsınız.

Sonraki adımda, Liste 3-8’deki fonksiyonu uygulamanız gerekir; bu fonksiyon Shodan’a bir HTTP GET isteği yapar ve yanıtı `APIInfo` struct’ınıza decode eder:

```go
func (s *Client) APIInfo() (*APIInfo, error) {
    res, err := http.Get(fmt.Sprintf("%s/api-info?key=%s", BaseURL, s.apiKey))
    if err != nil {
        return nil, err
    }
    defer res.Body.Close()

    var ret APIInfo
    if err := json.NewDecoder(res.Body).Decode(&ret); err != nil {
        return nil, err
    }

    return &ret, nil
}
```

**Liste 3-8**: HTTP GET isteği yapma ve yanıtı decode etme (`/ch-3/shodan/shodan/api.go`)

Uygulama kısa ve nettir. Önce `/api-info` kaynağına bir HTTP GET isteği yaparsınız. Tam URL, `BaseURL` küresel sabiti ve `s.apiKey` kullanılarak oluşturulur. Ardından yanıtı `APIInfo` struct’ınıza decode eder ve çağırana döndürürsünüz.

Bu yeni parlak mantığı kullanan kodu yazmadan önce, ikinci ve daha kullanışlı bir API çağrısı—host araması—oluşturun; bunu `host.go` dosyasına ekleyeceksiniz. API dokümantasyonuna göre istek ve yanıt aşağıdaki gibidir:

```
https://api.shodan.io/shodan/host/search?key={YOUR API KEY}&query={query}&facets={facets}
```

```json
"matches": [
    {
        "os": null,
        "timestamp": "2014-01-15T05:49:56.283713",
        "isp": "Vivacom",
        "asn": "AS8866",
        "hostnames": [],
        "location": {
            "city": null,
            "region_code": null,
            "area_code": null,
            "longitude": 25,
            "country_code3": "BGR",
            "country_name": "Bulgaria",
            "postal_code": null,
            "dma_code": null,
            "country_code": "BG",
            "latitude": 43
        },
        "ip": 3579573318,
        "domains": [],
        "org": "Vivacom",
        "data": "PJL INFO STATUS CODE=35078 DISPLAY=\"Power Saver\" ONLINE=TRUE",
        "port": 9100,
        "ip_str": "213.91.244.70"
    }

    --snip--
],
"facets": {
    "org": [
        {
            "count": 286,
            "value": "Korea Telecom"
        }

        --snip--
    ]
},
"total": 12039
```
