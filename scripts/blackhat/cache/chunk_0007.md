Dikkat edersen `go` yolu ve içe aktarılan package adı, aynı adı birden çok package'a atamaktan kaçınacak şekilde oluşturulmuştur. `github.com/stacktitan` ifadesini gerçek package adı olan `ldapauth` önüne eklemek, package adının benzersiz kalmasını sağlar.

Go geliştiricileri geleneksel olarak bağımlılıkları `go get` ile kurmalarına rağmen, bu bağımlı package'lar geriye dönük uyumluluğu (backward compatibility) bozan güncellemeler aldığında sorunlar ortaya çıkabilir. Go, geriye dönük uyumluluk sorunlarını önlemek için bağımlılıkları kilitlemeye yarayan iki ayrı araç — `dep` ve `mod` — tanıttı. Ancak, bu kitap neredeyse tamamen bağımlılıkları indirmek için `go get` kullanır. Bu, bağımlılık yönetimi araçlarındaki devam eden değişikliklerden kaynaklanan tutarsızlıklardan kaçınmaya ve umarız örnekleri çalışır hale getirmenizi kolaylaştırmaya yardımcı olacaktır.

## `go fmt` Komutu

`go fmt` komutu kaynak kodunuzu otomatik olarak biçimlendirir. Örneğin, `go fmt /path/to/your/package` çalıştırmak; uygun satır sonlarını, girintileme ve süslü parantez hizalamasını zorunlu kılarak kodunuzu biçimlendirir.

Keyfi görünen stil tercihlerine uymak, özellikle de alışkanlıklarınızdan farklıysa, başlangıçta garip gelebilir. Ancak zamanla bu tutarlılığı ferahlatıcı bulacaksınız; çünkü kodunuz diğer üçüncü taraf package'lar ile benzer görünecek ve daha düzenli hissedilecektir. Çoğu IDE, dosyanızı kaydettiğinizde otomatik olarak `go fmt` çalıştıracak kancalar (hook) içerir, bu sayede komutu ayrıca çalıştırmanız gerekmez.

## `golint` ve `go vet` Komutları

`go fmt` kodunuzun sözdizimsel stilini değiştirirken, `golint` yorum eksikliği, kurallara uymayan değişken adlandırma, gereksiz tür belirtimleri ve daha fazlası gibi stil hatalarını raporlar. `golint` aracının, ana `go` ikili dosyasının (binary) bir alt komutu olmadığını, bağımsız bir araç olduğunu unutmayın. `go get -u golang.org/x/lint/golint` kullanarak ayrı olarak kurmanız gerekir.

Benzer şekilde `go vet`, kodunuzu inceler ve sezgisel yöntemler (heuristics) kullanarak, örneğin `Printf()` fonksiyonunu yanlış biçimlendirme (format) dizesi türleriyle çağırmak gibi, şüpheli yapıları tespit eder. `go vet` komutu, derleyicinin kaçırabileceği, bazıları gerçek hatalar (bug) olabilecek sorunları belirlemeye çalışır.

## Go Playground

Go Playground, https://play.golang.org/ adresinde barındırılan ve geliştiricilere Go kod parçacıklarını hızlıca geliştirme, test etme, çalıştırma ve paylaşma imkânı sağlayan bir çalışma ortamıdır. Site, Go'yu yerel sisteminize kurup çalıştırmanıza gerek kalmadan çeşitli Go özelliklerini denemenizi kolaylaştırır. Bu, kod parçacıklarını projelerinize entegre etmeden önce test etmenin harika bir yoludur.

Ayrıca, önceden yapılandırılmış bir ortamda dilin çeşitli ince noktalarıyla oynamanıza da olanak tanır. Go Playground'un, örneğin işletim sistemi komutları çalıştırmak veya üçüncü taraf web siteleriyle etkileşime girmek gibi işlemleri engellemek amacıyla, belirli tehlikeli fonksiyonları çağırmanızı kısıtladığını unutmamak gerekir.

## Diğer Komutlar ve Araçlar

Bu kitapta diğer araç ve komutları açıkça ele almayacak olsak da, kendi araştırmanızı yapmanızı teşvik ediyoruz. Daha karmaşık projeler oluşturdukça, örneğin birim testleri ve benchmark'ları çalıştırmak için `go test` aracını, test kapsamını (coverage) kontrol etmek için `cover` aracını, `import` ifadelerini düzeltmek için `imports` aracını ve benzerlerini kullanma ihtiyacı duyma olasılığınız yüksektir.

## Go Sözdizimini Anlamak

Go dilinin tamamına dair kapsamlı bir inceleme, birkaç bölüm, hatta başlı başına bir kitap gerektirirdi. Bu bölüm, özellikle veri tipleri, kontrol yapıları ve genel kalıplar bağlamında Go sözdizimine kısa bir genel bakış sunar. Bu bölüm, Go'yu ara sıra kullanan geliştiriciler için bir tazeleme ve dile yeni başlayanlar için bir giriş niteliğinde olmalıdır.

Dilin daha derinlemesine ve kademeli bir incelemesi için, mükemmel *A Tour of Go* (https://tour.golang.org/) öğreticisini adım adım takip etmenizi öneririz. Bu, gömülü bir playground kullanarak her bir konsepti denemenizi sağlayan, dilin kapsamlı ve uygulamalı bir anlatımıdır.

Dil, C'nin çok daha temiz bir sürümü olup, pek çok düşük seviye nüansı ortadan kaldırır; bu da daha iyi okunabilirlik ve daha kolay benimsenme ile sonuçlanır.

## Veri Tipleri

Çoğu modern programlama dili gibi Go da çeşitli ilkel (primitive) ve karmaşık veri tipleri sağlar. İlkel tipler; diğer dillerde alışık olduğunuz, dizgeler (string), sayılar ve boolean'lar gibi temel yapı taşlarından oluşur. İlkel tipler, bir programda kullanılan tüm bilginin temelini oluşturur. Karmaşık veri tipleri ise bir veya daha fazla ilkel ya da diğer karmaşık tiplerin birleşiminden oluşan, kullanıcı tanımlı yapılardır.

### İlkel (Primitive) Veri Tipleri

İlkel tipler şunları içerir: `bool`, `string`, `int`, `int8`, `int16`, `int32`, `int64`, `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`, `byte`, `rune`, `float32`, `float64`, `complex64` ve `complex128`.

Genellikle bir değişkenin tipini onu tanımlarken belirtirsiniz. Belirtmezseniz, sistem değişkenin veri tipini otomatik olarak çıkarır (infer). Aşağıdaki örnekleri ele alalım:

```go
var x = "Hello World"
z := int(42)
```

İlk örnekte, `var` anahtar kelimesini kullanarak `x` adlı bir değişken tanımlıyor ve ona `"Hello World"` değerini atıyorsunuz. Go, `x`'in bir `string` olduğunu örtük olarak çıkarır, bu yüzden tipi ayrıca belirtmeniz gerekmez. İkinci örnekte, `:=` operatörünü kullanarak `z` adlı yeni bir değişken tanımlar ve ona `42` tam sayı değerini atarsınız. Aslında bu iki operatör arasında gerçek bir fark yoktur. Bu kitap boyunca her ikisini de kullanacağız, ancak bazı insanlar `:=` operatörünün okunabilirliği azaltan çirkin bir sembol olduğunu düşünür. Sizin için en iyi çalışanı seçin.

Yukarıdaki örnekte, `42` değerini `int` fonksiyon çağrısı içinde açıkça sarmalayarak ona bir tür zorluyorsunuz. `int` çağrısını atlayabilirsiniz, ancak bu durumda sistemin bu değer için otomatik olarak kullandığı tipi kabul etmek zorunda kalırsınız. Bazı durumlarda bu, kullanmayı amaçladığınız tip olmayabilir. Örneğin, `42` değerinin bir `int` tipi yerine işaretsiz tam sayı (`unsigned integer`) olarak temsil edilmesini istiyor olabilirsiniz; bu durumda değeri açıkça sarmalamanız gerekir.

### Dilimler (Slices) ve Haritalar (Maps)
