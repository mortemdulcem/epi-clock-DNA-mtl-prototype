Karşılaştırıldığında, uyguladığınız ilk API çağrısına göre bu çağrı oldukça daha karmaşıktır. İstek yalnızca birden fazla parametre almakla kalmaz, aynı zamanda JSON yanıtı iç içe geçmiş veriler ve diziler içerir. Aşağıdaki uygulamada, `facets` seçeneğini ve verisini yok sayacak, bunun yerine yalnızca yanıtın `matches` elemanını işlemek için dize tabanlı bir host araması gerçekleştirmeye odaklanacaksınız.

Daha önce yaptığınız gibi, yanıt verisini işlemek için Go `struct`larını oluşturarak başlayın; Liste 3-9’daki tipleri `host.go` dosyanıza girin.

```go
type HostLocation struct {
    City         string  `json:"city"`
    RegionCode   string  `json:"region_code"`
    AreaCode     int     `json:"area_code"`
    Longitude    float32 `json:"longitude"`
    CountryCode3 string  `json:"country_code3"`
    CountryName  string  `json:"country_name"`
    PostalCode   string  `json:"postal_code"`
    DMACode      int     `json:"dma_code"`
    CountryCode  string  `json:"country_code"`
    Latitude     float32 `json:"latitude"`
}

type Host struct {
    OS        string       `json:"os"`
    Timestamp string       `json:"timestamp"`
    ISP       string       `json:"isp"`
    ASN       string       `json:"asn"`
    Hostnames []string     `json:"hostnames"`
    Location  HostLocation `json:"location"`
    IP        int64        `json:"ip"`
    Domains   []string     `json:"domains"`
    Org       string       `json:"org"`
    Data      string       `json:"data"`
    Port      int          `json:"port"`
    IPString  string       `json:"ip_str"`
}

type HostSearch struct {
    Matches []Host `json:"matches"`
}
```

**Liste 3-9: Host araması yanıt veri tipleri (`/ch-3/shodan/shodan/host.go`)**

Kod üç tip tanımlar:

- **HostSearch** `matches` dizisini ayrıştırmak için kullanılır.
- **Host** tek bir `matches` elemanını temsil eder.
- **HostLocation** host içindeki `location` elemanını temsil eder.

Tiplerin tüm yanıt alanlarını tanımlamadığına dikkat edin. Go bunu oldukça şık bir şekilde ele alır; yalnızca önemsediğiniz JSON alanlarını içeren yapılar tanımlamanıza izin verir. Dolayısıyla, kodumuz JSON’u gayet güzel ayrıştırırken, örnek için en alakalı alanları dahil ederek kodunuzun uzunluğunu azaltır. `struct`ı ilklendirmek ve doldurmak için, Liste 3-8’de oluşturduğunuz `APIInfo()` metoduna benzer bir fonksiyon tanımlayacaksınız; bu fonksiyon Liste 3-10’da verilmiştir.

```go
func (s *Client) HostSearch(q string) (*HostSearch, error) {
    res, err := http.Get(
        fmt.Sprintf("%s/shodan/host/search?key=%s&query=%s", BaseURL, s.apiKey, q),
    )
    if err != nil {
        return nil, err
    }

    defer res.Body.Close()

    var ret HostSearch
    if err := json.NewDecoder(res.Body).Decode(&ret); err != nil {
        return nil, err
    }

    return &ret, nil
}
```

**Liste 3-10: Host arama yanıt gövdesinin çözümlenmesi (`/ch-3/shodan/shodan/host.go`)**

Akış ve mantık, `APIInfo()` yöntemiyle tamamen aynıdır; tek fark, arama sorgusu dizgesini bir parametre olarak almanız, `/shodan/host/search` uç noktasına arama terimini de geçirerek çağrı yapmanız ve yanıtı `HostSearch` `struct`ına çözümlendirmenizdir.

Etkileşimde bulunmak istediğiniz her API servisi için bu yapı tanımlama ve fonksiyon uygulama sürecini tekrar edersiniz. Burada sayfaları israf etmek yerine, sürecin son adımına atlayıp, API kodunuzu kullanan istemciyi nasıl oluşturacağınızı göstereceğiz.

## İstemci Oluşturma

İstemcinizi oluştururken minimalist bir yaklaşım kullanacaksınız: bir arama terimini komut satırı argümanı olarak alacak ve ardından Liste 3-11’de olduğu gibi `APIInfo()` ve `HostSearch()` metodlarını çağıracaksınız.

```go
func main() {
    if len(os.Args) != 2 {
        log.Fatalln("Usage: shodan searchterm")
    }

    apiKey := os.Getenv("SHODAN_API_KEY")
    s := shodan.New(apiKey)
    info, err := s.APIInfo()
    if err != nil {
        log.Panicln(err)
    }

    fmt.Printf(
        "Query Credits: %d\nScan Credits: %d\n\n",
        info.QueryCredits,
        info.ScanCredits,
    )

    hostSearch, err := s.HostSearch(os.Args[1])
    if err != nil {
        log.Panicln(err)
    }

    for _, host := range hostSearch.Matches {
        fmt.Printf("%18s%8d\n", host.IPString, host.Port)
    }
}
```

**Liste 3-11: `shodan` paketinin tüketilmesi ve kullanılması (`/ch-3/shodan/cmd/shodan/main.go`)**

Öncelikle API anahtarınızı `SHODAN_API_KEY` ortam değişkeninden okuyun. Ardından bu değeri kullanarak yeni bir `Client` `struct`ı (`s`) ilklendirin ve bunu `APIInfo()` metodunuzu çağırmak için kullanın. Sonra `HostSearch()` metodunu çağırın ve komut satırı argümanı olarak yakalanan bir arama dizgesini parametre olarak geçin. Son olarak, sonuçlar üzerinde döngü kurarak, sorgu dizesiyle eşleşen servislerin IP ve port değerlerini gösterin. Aşağıdaki çıktı, `tomcat` dizesi için yapılan örnek bir çalıştırmayı göstermektedir:

```bash
$ SHODAN_API_KEY=YOUR-KEY go run main.go tomcat
Query Credits: 100
Scan Credits: 160

    185.23.138.141     8081
    218.103.124.239     8080
      123.59.14.169     8081
       177.6.80.213     8181
     142.165.84.160    10000
--snip--
```
