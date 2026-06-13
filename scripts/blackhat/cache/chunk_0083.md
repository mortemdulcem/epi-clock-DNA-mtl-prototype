Go Plugins and Extendable Tools
================================

`cmd/scanner/main.go` adlı dosya komut satırı aracınızdır. Eklentileri (plug-in) yükleyecek ve bir taramayı başlatacaktır. `plugins` dizini, çeşitli zafiyet imza kontrollerini çağırmak için dinamik olarak yükleyeceğiniz tüm paylaşımlı nesneleri (shared object) içerecektir. `scanner/scanner.go` adlı dosyayı, eklentilerinizin ve ana tarayıcınızın kullanacağı veri tiplerini tanımlamak için kullanacaksınız. Bu veriyi, kullanımı biraz daha kolay olsun diye kendi package’ine koyuyorsunuz.

Liste 10-1, `scanner.go` dosyanızın nasıl göründüğünü gösterir. (Kök konum `/` altındaki tüm kod listeleri, verilen GitHub deposunda yer almaktadır: `https://github.com/blackhat-go/bhg/`.)

```go
package scanner

// Scanner defines an interface to which all checks adhere
type Checker interface {
	Check(host string, port uint64) *Result
}

// Result defines the outcome of a check
type Result struct {
	Vulnerable bool
	Details    string
}
```

Liste 10-1: Temel tarayıcı tiplerinin tanımlanması (`/ch-10/plugin-core/scanner/scanner.go`)

Bu `scanner` adlı package içinde iki tip tanımlıyorsunuz. İlki, `Checker` 0 adlı bir arayüz (interface). Bu arayüz, `Check()` 6 adlı tek bir metot tanımlar; bu metot bir `host` ve `port` değeri alır ve bir `Result` işaretçisi (pointer) döndürür. `Result` tipiniz bir `struct` 0 olarak tanımlanmıştır. Amacı, yapılan kontrolün sonucunu takip etmektir. Servis zafiyetli mi? Açığın dokümantasyonu, doğrulanması veya sömürülmesi (exploit edilmesi) için hangi detaylar önemlidir?

Arayüzü bir tür sözleşme veya plan (blueprint) gibi ele alacaksınız; bir eklenti (plug-in), `Check()` fonksiyonunu dilediği gibi gerçekleştirmekte özgürdür, yeter ki bir `Result` işaretçisi döndürsün. Eklentinin uygulama mantığı, her eklentinin zafiyet kontrol mantığına göre değişecektir. Örneğin, bir Java deserialization sorununu kontrol eden bir eklenti uygun HTTP çağrılarını gerçekleştirebilirken, varsayılan SSH kimlik bilgilerini kontrol eden bir eklenti SSH servisine karşı bir parola tahmin saldırısı gerçekleştirebilir. Soyutlamanın (abstraction) gücü!

Şimdi de eklentilerinizi tüketecek (consume edecek) `cmd/scanner/main.go` dosyasına bakalım (Liste 10-2).

```go
const PluginsDir = "../../pluginsr 0

func main() {
    var (
        files []os.FileInfo
        err error
               *plugin.Plugin
               plugin.Symbol
        check scanner.Checker

        res *scanner.Result

    if files, err = ioutil.ReadDir(PluginsDir)0; err != nil {
          log.Fatalln(err)

    for idx := range files {
        fet.Println("Found plugin: " + files[idx].Name())
        if p, err = plugin.Open(PluginsDir + "/" + files[idx].Name())0; err != nil {
             log.Fatalln(err)

        if n, err = p.Lookup("New")0; err != nil {
             log.Fatalln(err)

        newFunc, ok := n.(func() scanner.Checker)
        if lok {
            log.Fatalln("Plugin entry point is no good. Expecting: func New() scanner.Checker{                }")

        check = newFunc()0
        res = check.Check("10.0.1.20", 8080)
        if res.Vulnerable { 0
             log.Println("Host is vulnerable: " + res.Details)
           else {
             log.Println("Host is NOT vulnerable")
```

Liste 10-2: Eklentileri çalıştıran tarayıcı istemcisi (`/ch-10/plugin-core/cmd/scanner/main.go`)

Kod, eklentilerinizin konumunu tanımlayarak başlar 0. Bu durumda yolu sabit kodlamışsınız; elbette, bu değeri bir argüman veya ortam değişkeni (environment variable) olarak okuyan şekilde geliştirilebilir. Bu değişkeni kullanarak `ioutil.ReadDir(PluginsDir)` çağrısıyla bir dizin listelemesi alırsınız 0 ve sonra bu eklenti dosyalarının her biri üzerinde döngü kurarsınız 0. Her dosya için, Go’nun `plugin` package’ini kullanarak `plugin.Open()` çağrısıyla eklentiyi okursunuz 0. Bu çağrı başarıyla sonuçlanırsa, size bir `*plugin.Plugin` örneği (instance) verilir ve bunu `p` adlı değişkene atarsınız. Eklentinizde `New` adlı bir sembolü aramak için `p.Lookup("New")` çağrısını yaparsınız 0.

Yüksek seviyeli genel bakışta daha önce de belirttiğimiz gibi, bu sembol arama kuralı, ana programınızın sembolün adını açıkça argüman olarak sağlamasını gerektirir; yani eklentinizin aynı ada sahip dışa aktarılan (exported) bir sembole sahip olmasını beklersiniz — bu durumda, ana programımız `New` adlı sembolü arıyor. Ayrıca, birazdan göreceğiniz gibi, kod bu sembolün, `scanner.Checker` arayüzünüzün somut bir uygulamasını döndürecek bir fonksiyon olmasını bekliyor; bunu bir önceki bölümde tartışmıştık.

Eklentinizin `New` adlı bir sembol içerdiğini varsayarsak, sembolü `func() scanner.Checker` tipine dönüştürmeye çalışırken bir tür yaklaştırma (type assertion) yaparsınız 0. Yani, sembolün, `scanner.Checker` uygulayan (implement eden) bir nesne döndüren bir fonksiyon olmasını bekliyorsunuz. Bu fonksiyonu atarsınız
