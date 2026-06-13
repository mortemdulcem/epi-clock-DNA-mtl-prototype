Bölüm 2'de, kullanılabilir istemciler ve sunucular oluşturmak için çeşitli tekniklerle TCP'nin gücünden nasıl yararlanılacağını öğrendiniz. Bu, OSI modelinin üst katmanlarındaki çeşitli protokolleri inceleyen bir dizi bölümün ilkidir. Ağlarda çok yaygın olması, gevşek çıkış (egress) kontrolleriyle ilişkilendirilmesi ve genel esnekliği nedeniyle HTTP ile başlayalım.

Bu bölüm istemci tarafına odaklanır. Önce HTTP isteklerinin nasıl oluşturulup özelleştirileceğinin ve bu isteklere verilen yanıtların alınmasının temellerini göreceksiniz. Ardından, istemcinin harekete geçirilebilir veya ilgili verileri belirlemek için bilgiyi sorgulayabilmesi amacıyla, yapılandırılmış yanıt verilerini nasıl ayrıştıracağınızı (parse) öğreneceksiniz. Son olarak, bu temel bilgileri, çeşitli güvenlik araçları ve kaynaklarıyla etkileşime giren HTTP istemcileri inşa ederek nasıl uygulayacağınızı göreceksiniz. Geliştireceğiniz istemciler Shodan, Bing ve Metasploit API'lerini sorgulayıp tüketecek ve FOCA adlı meta veri arama aracına benzer bir şekilde doküman meta verilerini arayıp ayrıştıracaktır.

## Go ile HTTP Temelleri

HTTP hakkında kapsamlı bir bilgiye ihtiyaç duymasanız da başlamadan önce bazı temel kavramları bilmelisiniz.

İlk olarak, HTTP durum bilgisiz (stateless) bir protokoldür: sunucu, her istek için durumu ve statüyü içkin olarak takip etmez. Bunun yerine, durum; oturum tanımlayıcıları (session identifiers), çerezler (cookies), HTTP başlıkları ve daha fazlasını içerebilen çeşitli yollarla takip edilir. İstemci ve sunucular, bu durumu doğru şekilde müzakere etmek ve doğrulamakla yükümlüdür.

İkinci olarak, istemciler ve sunucular arasındaki iletişimler eşzamanlı (synchronous) veya eşzamansız (asynchronous) olabilir, ancak bir istek/yanıt döngüsü üzerinde çalışırlar. Sunucu davranışını etkilemek ve kullanılabilir web uygulamaları oluşturmak için isteğe çeşitli seçenekler ve başlıklar ekleyebilirsiniz. En yaygın olarak sunucular, bir web tarayıcısının verinin grafiksel, düzenli ve şık bir temsilini üretmek için işlediği dosyaları barındırır. Ancak uç nokta (endpoint) keyfi veri türlerini de sunabilir. API'ler genellikle XML, JSON veya MSGRPC gibi daha yapılandırılmış veri kodlamaları üzerinden iletişim kurar. Bazı durumlarda, alınan veri indirilecek keyfi bir dosya türünü temsil eden ikili (binary) formatta olabilir.

Son olarak, Go içinde, bir sunucuya HTTP isteklerini hızlı ve kolay bir şekilde oluşturup gönderebilmeniz ve sonrasında yanıtı alıp işleyebilmeniz için kolaylık sağlayan fonksiyonlar bulunur. Önceki bölümlerde öğrendiğiniz bazı mekanizmalar aracılığıyla, yapılandırılmış verileri ele almak için kullanılan konvansiyonların HTTP API'leriyle etkileşimde son derece kullanışlı olduğunu göreceksiniz.

## HTTP API'lerini Çağırmak

HTTP tartışmasına temel istekleri inceleyerek başlayalım. Go'nun `net/http` standart paketi, muhtemelen en sık kullanacağınız HTTP fiilleri olan POST, GET ve HEAD isteklerini hızlı ve kolay bir şekilde göndermek için birkaç kolaylık (convenience) fonksiyonu içerir. Bu fonksiyonların biçimleri şöyledir:

```go
Get(url string) (resp *Response, err error)
Head(url string) (resp *Response, err error)
Post(url string, bodyType string, body io.Reader) (resp *Response, err error)
```

Her fonksiyon, parametre olarak URL'yi bir `string` değer olarak alır ve bu değeri isteğin hedefi için kullanır. `Post()` fonksiyonu, `Get()` ve `Head()` fonksiyonlarından biraz daha karmaşıktır. `Post()`, iki ek parametre alır: `bodyType`, istek gövdesinin `Content-Type` HTTP başlığı için kullandığınız bir `string` değerdir (çoğunlukla `application/x-www-form-urlencoded`), ve Bölüm 2'de hakkında bilgi edindiğiniz bir `io.Reader`.

Bu fonksiyonların her birinin örnek bir uygulamasını Liste 3-1'de görebilirsiniz. (Kök konum `/` altındaki tüm kod listeleri, sağlanan GitHub deposu `https://github.com/blackhat-go/bhg/` altında bulunur.) Dikkat edin, POST isteği istek gövdesini form değerlerinden oluşturur ve `Content-Type` başlığını ayarlar. Her durumda, yanıt gövdesinden veri okumayı bitirdiğinizde gövdeyi kapatmanız gerekir.

```go
r1, err := http.Get("http://www.google.com/robots.txt")
// Read response body. Not shown.
defer r1.Body.Close()

r2, err := http.Head("http://www.google.com/robots.txt")
// Read response body. Not shown.
defer r2.Body.Close()

form := url.Values{}
form.Add("foo", "bar")
r3, err := http.Post(
     "https://www.google.com/robots.txt",
     "application/x-www-form-urlencoded",
     strings.NewReader(form.Encode()),
)
// Read response body. Not shown.
defer r3.Body.Close()
```

**Liste 3-1:** `Get()`, `Head()` ve `Post()` fonksiyonlarının örnek uygulamaları (`/ch-3/basic/main.go`)

`Post()` fonksiyon çağrısı, `Content-Type`'ı `application/x-www-form-urlencoded` olarak ayarlamak ve form verilerini URL-encode etmek gibi oldukça yaygın bir modeli izler.

Go'da `PostForm()` adlı ek bir POST istek kolaylık fonksiyonu daha vardır; bu fonksiyon, bu değerleri ayarlama ve her isteği elle encode etme zahmetini ortadan kaldırır. Sözdizimini burada görebilirsiniz:

```go
func PostForm(url string, data url.Values) (resp *Response, err error)
```

`PostForm()` fonksiyonunu, Liste 3-1'deki `Post()` uygulamasının yerine kullanmak isterseniz, Liste 3-2'de kalın gösterilen koddaki gibi bir şey kullanırsınız.

```go
form := url.Values{}
form.Add("foo", "bar")
r3, err := http.PostForm("https://www.google.com/robots.txt", form)
// Read response body and close.
```

**Liste 3-2:** `Post()` yerine `PostForm()` fonksiyonunun kullanılması (`/ch-3/basic/main.go`)

Ne yazık ki, PATCH, PUT veya DELETE gibi diğer HTTP fiilleri için kolaylık fonksiyonları yoktur. Bu fiilleri çoğunlukla RESTful API'lerle etkileşim kurmak için kullanırsınız; bu API'ler, bir sunucunun bu fiilleri nasıl ve neden kullanması gerektiğine dair genel kılavuzlar uygular; ancak hiçbir şey taşla yazılı değildir ve HTTP fiiller söz konusu olduğunda Vahşi Batı gibidir. Aslında, her şey için yalnızca DELETE kullanan yeni bir web çatısı (framework) oluşturma fikriyle sık sık oynadık. Adını DELETEjs koyarız ve kesinlikle Hacker News'te en üst sıralarda olur. Bunu okuyarak, bu fikri çalmayacağınıza dair şimdiden anlaşmış sayılıyorsunuz!
