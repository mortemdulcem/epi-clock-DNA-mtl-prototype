Unauthorized
```bash
$ curl -i http://localhost:8000/hello?username=admin&password=password
HTTP/1.1 200 OK
Date: Thu, 16 Jan 2020 20:41:05 GMT
Content-Length: 9
Content-Type: text/plain; charset=utf-8

Hi admin
```

Kimlik bilgileri olmadan istek göndermek, `middleware`'inizin 401 Unauthorized hatası döndürmesiyle sonuçlanır. Aynı isteği geçerli bir kimlik bilgisi setiyle göndermek ise yalnızca kimliği doğrulanmış kullanıcıların erişebileceği, süper gizli bir karşılama mesajı üretir.

Sindirilmesi gereken epey şey vardı. Buraya kadar `handler` fonksiyonlarınız yalnızca `fmt.Fprintf()` kullanarak yanıtınızı `http.ResponseWriter` örneğine yazdı. Bir sonraki bölümde, Go'nun şablon (templating) paketini kullanarak HTML döndürmenin daha dinamik bir yoluna bakacaksınız.

## HTML Yanıtlar Üretmek için Şablonların Kullanılması

Şablonlar, Go programlarındaki değişkenleri kullanarak HTML de dahil olmak üzere içeriği dinamik olarak üretmenizi sağlar. Birçok dilde, şablon üretimini sağlayan üçüncü taraf paketler bulunur. Go'da ise `text/template` ve `html/template` olmak üzere iki şablon paketi vardır. Bu bölümde, ihtiyacınız olan bağlamsal kodlamayı (contextual encoding) sağladığı için HTML paketini kullanacaksınız.

Go'nun paketinin harika özelliklerinden biri bağlamsal farkındalığa sahip olmasıdır: değişkeninizi şablonda yerleştirildiği yere göre farklı şekilde kodlayacaktır. Örneğin, bir `href` özniteliğine bir URL olarak bir string sağlarsanız, string URL olarak kodlanır; ama aynı string bir HTML öğesinin içinde render edilirse HTML olarak kodlanır.

Şablonlar oluşturmak ve kullanmak için önce, render edilecek dinamik bağlamsal veriyi göstermek amacıyla yer tutucu (placeholder) içeren şablonunuzu tanımlarsınız. Sözdizimi, Python ile Jinja kullanmış okuyuculara tanıdık gelecektir. Şablonu render ettiğinizde, bağlam (context) olarak kullanılacak bir değişken geçirirsiniz. Bu değişken, birden çok alana sahip karmaşık bir yapı (struct) olabileceği gibi, ilkel (primitive) bir değişken de olabilir.

Liste 4-6'da gösterilen bir örnek üzerinden ilerleyelim; bu örnek basit bir şablon oluşturuyor ve bir yer tutucuyu JavaScript ile dolduruyor. Bu, tarayıcıya döndürülen içeriği dinamik olarak nasıl doldurabileceğinizi gösteren, yapay bir örnektir.

```go
package main

import (
    "html/template"
    "os"
)

var x = `
<html>
  <body>
    Hello {{.}}
  </body>
</html>
`

func main() {
    t, err := template.New("hello").Parse(x)
    if err != nil {
        panic(err)
    }

    t.Execute(os.Stdout, "<script>alert('world')</script>")
}
```

**Liste 4-6: HTML şablonlama (`ch-4/template_example/main.go`)**

Yaptığınız ilk şey, HTML şablonunuzu saklamak için `x` adında bir değişken oluşturmak ❶. Burada, şablonunuzu tanımlamak için kodunuzun içine gömülü bir string kullanıyorsunuz; ancak çoğu zaman şablonlarınızı ayrı dosyalar olarak saklamak isteyeceksiniz. Şablonun basit bir HTML sayfasından ibaret olduğuna dikkat edin. Şablon içerisinde, yer tutucuları `{‌{variable-name}}` söz dizimiyle tanımlarsınız; burada `variable-name`, bağlam veriniz içinde render etmek istediğiniz veri öğesidir ❷. Bunun bir `struct` ya da başka bir ilkel değer olabileceğini hatırlayın. Bu örnekte tek bir nokta (.) kullanıyorsunuz; bu, pakete burada tüm bağlamı render etmek istediğinizi söyler. Tek bir string ile çalışacağınız için bu yeterlidir; fakat bir `struct` gibi daha büyük ve karmaşık bir veri yapınız olsaydı, bu noktadan sonra devam ederek yalnızca istediğiniz alanları alabilirdiniz. Örneğin, şablona `username` alanına sahip bir `struct` geçirirseniz, bu alanı `{{.Username}}` kullanarak render edebilirsiniz.

Sonra, `main()` fonksiyonunuzda `template.New(string)` çağırarak yeni bir şablon oluşturursunuz ❸. Ardından, şablonun doğru biçimlendirildiğinden emin olmak ve onu ayrıştırmak için `Parse(string)` çağırırsınız. Bu iki fonksiyon birlikte yeni bir `Template` işaretçisi (pointer) döndürür.

Bu örnek yalnızca tek bir şablon kullanıyor olsa da, şablonları başka şablonların içine gömmek mümkündür. Birden fazla şablon kullanırken, onları çağırabilmek için mutlaka adlandırmak önemlidir. Son olarak `Execute(io.Writer, interface{})` ❹ çağırırsınız; bu, ikinci argüman olarak geçirilen değişkeni kullanarak şablonu işler (process) ve sonucu sağlanan `io.Writer`'a yazar. Gösterim amaçlı olarak `os.Stdout` kullanacaksınız. `Execute()` metoduna ilettiğiniz ikinci değişken, şablonun render edilmesi için kullanılacak bağlamdır.

Bunu çalıştırmak HTML üretir ve bağlamınızın bir parçası olarak sağlanan script etiketlerinin ve diğer kötü niyetli karakterlerin doğru şekilde kodlandığını fark etmelisiniz. Süper!

```bash
$ go build -o template_example
$ ./template_example

<html>
  <body>
    Hello &lt;script&gt;alert(&#39;world&#39;)&lt;/script&gt;
  </body>
</html>
```

Şablonlar hakkında daha söyleyebileceğimiz çok şey var. Onlarla mantıksal operatörler kullanabilir; döngüler ve diğer kontrol yapılarıyla birlikte kullanabilirsiniz. Yerleşik fonksiyonları çağırabilir, hatta şablonlama yeteneklerini büyük ölçüde genişletmek için keyfi yardımcı fonksiyonlar tanımlayıp ortaya çıkarabilirsiniz. Çifte süper! Bu olanaklara dalmanızı ve araştırmanızı öneririz. Bunlar bu kitabın kapsamı dışında, ancak oldukça güçlüler.

Şimdi sunucu oluşturma ve istek işleme temellerinden biraz uzaklaşıp daha kötü niyetli bir şeye odaklanalım. Hadi bir kimlik bilgisi (credential) toplayıcı yazalım!
