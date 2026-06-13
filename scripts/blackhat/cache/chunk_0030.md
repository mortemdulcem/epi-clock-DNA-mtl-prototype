Bing ile Dosya Arama ve Alma
Artık Office Open XML belgelerini açmak, okumak, ayrıştırmak ve çıkarmak için gerekli tüm koda sahipsiniz ve dosyayla ne yapmanız gerektiğini biliyorsunuz. Şimdi Bing kullanarak dosyaları nasıl arayacağınızı ve alacağınızı bulmanız gerekiyor. İzlemeniz gereken eylem planı şöyle:

1. Hedeflenmiş sonuçları almak için uygun filtrelerle Bing'e bir arama isteği gönderin.
2. HTML yanıtını kazıyın (scrape) ve HREF (link) verisini çıkararak belgelerin doğrudan URL'lerini elde edin.
3. Her bir doğrudan belge URL'si için bir HTTP isteği gönderin.
4. Yanıt gövdesini ayrıştırarak bir `zip.Reader` oluşturun.
5. `zip.Reader` nesnesini, meta veri çıkarmak için önceden geliştirdiğiniz koda aktarın.

Aşağıdaki bölümlerde bu adımların her biri sırayla ele alınmaktadır.

İlk iş olarak bir arama sorgu şablonu oluşturmak gerekiyor. Google'da olduğu gibi, Bing de arama sonuçlarını birçok değişkene göre filtrelemek için kullanabileceğiniz gelişmiş sorgu parametreleri içerir. Bu filtrelerin çoğu `filter type:value` biçiminde gönderilir. Tüm mevcut filtre türlerini açıklamak yerine, amacınıza ulaşmanıza yardımcı olanlara odaklanalım. Aşağıdaki liste, ihtiyaç duyduğunuz üç filtreyi içerir. Ek filtreler de kullanabilirsiniz, ancak bu kitabın yazıldığı tarihte bunlar biraz öngörülemez davranmaktaydı.

- `site` Sonuçları belirli bir alan adıyla (domain) sınırlamak için kullanılır.
- `filetype` Sonuçları kaynak dosya türüne göre filtrelemek için kullanılır.
- `instreamset` Sonuçları sadece belirli dosya uzantılarını içerecek şekilde filtrelemek için kullanılır.

`nytimes.com` alan adından `docx` dosyalarını almak için örnek bir sorgu şöyle görünür:

`site:nytimes.com && filetype:docx && instreamset:(url title):docx`

Tarayıcınızda bu sorguyu gönderdikten sonra ortaya çıkan URL'ye bir göz atın. Şekil 3-1'e benzemelidir. Bu URL'den sonra ek parametreler de görünebilir, ancak bu örnek için önemsizdirler; bu yüzden yok sayabilirsiniz.

Artık URL ve parametre formatını bildiğinize göre, HTML yanıtını da görebilirsiniz; ancak önce Belge Nesne Modeli'nde (DOM) belge linklerinin nerede yer aldığını belirlemeniz gerekir. Bunu doğrudan kaynak kodunu görüntüleyerek yapabilir veya tahmin sürecini kısaltmak için tarayıcınızın geliştirici araçlarını kullanabilirsiniz. Aşağıdaki görsel, hedef HREF'e giden tam HTML öğe yolunu göstermektedir. Şekil 3-1'de olduğu gibi öğe denetleyicisini (element inspector) kullanarak linki hızlıca seçip tam yolunu ortaya çıkarabilirsiniz.

```
site:nytimes.com && filetype:docx && instreamset:(url title):docx

Web         Images          Videos   Maps        News         Explore

5 RESULTS            Any time -

world increase in HIV infections on a Navajo reservation in New ...
World/abc8radio/healthanddiseases/pdf2012N/HHSAnnualHIVReportD41713.docx Web site
Apr 11, 2013 The mean CD4 count among new cases was 461, a dramatic increase from the 2011
mean of 340, reflecting improved success in diagnosing cases early in field

Etc [5]   Elements Console Sources Network Timeline Profiles Application Security Audits
    <script type="text/javascript" ...></script>
    <div id="b_content" role="main" aria-label="Search Results">

        <ol class="b_results">
            <li class="b_algo">
                <div class="b_title">
                    <h2>
                        <a href="https://graphics.nytimes.com/packages/pdf/2012/HHSAnnualHIVReport-41713.docx">
                            DESCRIPTIVE: World increase in HIV infections on a Navajo reservation in New ...
                        </a>
                    </h2>
                </div>
            </li>
        </ol>
    </div>
```

Şekil 3-1: Tarayıcı geliştirici aracıyla gösterilen tam öğe yolu

Bu yol bilgisiyle, goquery kullanarak belirli bir HTML yoluyla eşleşen tüm veri öğelerini sistematik biçimde çekebilirsiniz. Yeterince konuştuk! Liste 3-22 her şeyi bir araya getiriyor: alma, kazıma (scraping), ayrıştırma ve çıkarma. Bu kodu `main.go` dosyasına kaydedin.

```go
func handler(i int, s *goquery.Selection) {
    url, ok := s.Find("a").Attr("href")
    if !ok {
        return
    }

    fmt.Printf("%d: %s\n", i, url)
    res, err := http.Get(url)
    if err != nil {
        return
    }

    buf, err := ioutil.ReadAll(res.Body)
    if err != nil {
        return
    }

    defer res.Body.Close()

    r, err := zip.NewReader(bytes.NewReader(buf), int64(len(buf)))
    if err != nil {
        return
    }

    cp, ap, err := metadata.NewProperties(r)
    if err != nil {
        return
    }

    log.Printf(
        "%25s %25s - %s %s\n",
        cp.Creator,
        cp.LastModifiedBy,
        ap.Application,
        ap.GetMajorVersion())
}

func main() {
    if len(os.Args) != 3 {
        log.Fatalln("Missing required argument. Usage: main.go domain ext")
    }

    domain := os.Args[1]
    filetype := os.Args[2]

    q := fmt.Sprintf(
        "site:%s && filetype:%s && instreamset:(url title):%s",
        domain,
        filetype,
        filetype)
    search := fmt.Sprintf("http://www.bing.com/search?q=%s", url.QueryEscape(q))
    doc, err := goquery.NewDocument(search)
    if err != nil {
        log.Panicln(err)
    }

    s := "html body div#b_content ol#b_results li.b_algo div.b_title h2"
    doc.Find(s).Each(handler)
}
```

**Liste 3-22: Bing sonuçlarını kazıma ve belge meta verisini ayrıştırma (`/ch-3/bing-metadata/client/main.go`)**

İki fonksiyon oluşturuyorsunuz. İlki, `handler()`, bir `goquery.Selection` örneğini (`s`) alır (bu örnek, bu durumda bir `anchor` HTML öğesiyle doldurulacaktır) ve `href` özniteliğini bulup çıkarır. Bu öznitelik, Bing aramasından dönen belgeye doğrudan bir bağlantı içerir. Bu URL kullanılarak kod, belgeyi almak için bir GET isteği gönderir. Herhangi bir sorun olmadığı varsayıldığında...
