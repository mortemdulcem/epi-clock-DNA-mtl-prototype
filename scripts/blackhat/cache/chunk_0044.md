### Alt Alan Adlarını (Subdomain) Numaralandırma

Artık Go’yu bir DNS istemcisi olarak nasıl kullanacağınızı bildiğinize göre, işe yarar araçlar oluşturabilirsiniz. Bu bölümde bir alt alan adı tahmin (subdomain guessing) aracı yazacaksınız. Bir hedefin alt alan adlarını ve diğer DNS kayıtlarını tahmin etmek keşif (reconnaissance) aşamasının temel adımlarından biridir; çünkü ne kadar çok alt alan adı biliyorsanız, o kadar çok hedefe saldırmayı deneyebilirsiniz. Bu aracımıza, alt alan adlarını tahmin etmek için kullanılacak aday bir kelime listesi (dictionary dosyası) vereceksiniz.

DNS ile, işletim sisteminizin paket verisi işlemeyi kaldırabildiği hızda istek gönderebilirsiniz. Dil ve çalışma zamanı (runtime) bir darboğaz olmayacak olsa da, hedef sunucu buna dönüşecektir. Programınızın eşzamanlılığını (concurrency) kontrol etmek burada da önemli olacak; tıpkı önceki bölümlerde olduğu gibi.

Önce GOPATH’iniz içinde `subdomain_guesser` adlı yeni bir dizin oluşturun ve `main.go` adlı yeni bir dosya oluşturun. Ardından, yeni bir araç yazmaya başlarken, programın hangi argümanları alacağına karar vermelisiniz. Bu alt alan adı tahmin programı; hedef alan adı (domain), tahmin edilecek alt alan adlarını içeren dosya adı, kullanılacak hedef DNS sunucusu ve başlatılacak worker sayısı gibi birkaç argüman alacak. Go, komut satırı seçeneklerini ayrıştırmak (parse) için `flag` adlı kullanışlı bir paket sağlar ve siz de komut satırı argümanlarınızı yönetmek için bunu kullanacaksınız. `flag` paketini tüm örnek kodlarımızda kullanmasak da, daha sağlam ve zarif bir argüman ayrıştırma yöntemi göstermek için bu durumda kullanmayı seçtik. Liste 5-3’te argüman ayrıştırma kodumuz yer alıyor.

```go
package main

import (
   "flag"

func main() {
    var (
        flDomain        flag.String(domain", "", "The domain to perform guessing against.") 0
        flWordlist    = flag.String("wordlist", "", "The wordlist to use for guessing.")
        flWorkerCount = flag.Int("c", lop, "The amount of workers to use.") 0
        flServerAddr = flag.String("server", "8.8.8.8:53", "The DNS server to use.")

      flag.Parse()
```

**Liste 5-3: Bir alt alan adı tahmin aracı oluşturma (`/ch-5/subdomain_guesser/main.go`)**

Öncelikle, `flDomain` değişkenini tanımlayan satır, `String` argümanı alır ve `domain` seçeneği olarak ayrıştırılacak değer için varsayılan boş bir string tanımlar. Sonraki ilgili satır `flWorkerCount` değişkeninin tanımıdır. `-c` komut satırı seçeneği için bir `Integer` değer sağlamanız gerekir. Bu durumda, varsayılan worker sayısını 100 olarak ayarlıyoruz. Ancak bu değer muhtemelen fazla muhafazakâr; test ederken bu sayıyı artırmaktan çekinmeyin. Son olarak, `flag.Parse()` çağrısı, kullanıcıdan gelen girdiyi kullanarak değişkenlerinizi doldurur.

> **NOT**  
> Örneğin, Unix yasasına aykırı bir şey yaptığını fark etmiş olabilirsiniz: Zorunlu argümanlar olmasına rağmen, bunları isteğe bağlı (optional) argümanlar olarak tanımladık. Bu noktada `os.Args` kullanmakta kendinizi özgür hissedebilirsiniz. Biz sadece `flag` paketinin tüm işi yapmasını daha kolay ve hızlı bulduk.

Bu programı derlemeyi denerseniz, kullanılmayan değişkenler hakkında bir hata almanız gerekir. `flag.Parse()` çağrınızın hemen ardından aşağıdaki kodu ekleyin. Bu ekleme, kullanıcı `-domain` ve `-wordlist` seçeneklerini verdiğinden emin olmak için değişkenleri stdout’a yazdırır ve kontrol eder:

```go
if *f1Domain == "" II *flWordlist =. "" {
     fmt.Println("-domain and -wordlist are required")
     os.Exit(i)
}
fmt.Println(*flWorkerCount, *f1ServerAddr)
```

Aracınızın, çözümlenebilen (resolvable) adları ve bunlara karşılık gelen IP adreslerini raporlamasını sağlamak için, bu bilgiyi saklayacak bir `struct` tipi oluşturacaksınız. Bunu `main()` fonksiyonunun üzerinde tanımlayın:

```go
type result struct {
    IPAddress string
    Hostname  string
}
```

İki temel kayıt tipini sorgulayacaksınız: bu araç için A ve CNAME. Her sorguyu ayrı bir fonksiyonda gerçekleştireceksiniz. Fonksiyonlarınızı olabildiğince küçük tutmak ve her birinin tek bir işi iyi yapmasını sağlamak iyi bir pratiktir. Bu tarz bir geliştirme yaklaşımı, gelecekte daha küçük testler yazmanıza olanak tanır.

### A ve CNAME Kayıtlarını Sorgulama

İki fonksiyon oluşturacaksınız: biri A kayıtları, diğeri CNAME kayıtları için. Her iki fonksiyon da ilk argüman olarak tam nitelikli alan adı (FQDN — fully qualified domain name), ikinci argüman olarak DNS sunucu adresini alır. Her biri bir `[]string` (string slice’ı) ve bir `error` döndürmelidir. Bu fonksiyonları Liste 5-3’te yazmaya başladığınız koda ekleyin. Bu fonksiyonlar `main` fonksiyonunun dışında tanımlanmalıdır.

```go
func lookupA(fqdn, serverAddr string) ([]string, error) f
    var in dns.Msg
    var ips []string
    m.SetOuestion(dns.Fqdn(fqdn), dns.TypeA)
    in, err := dns.Exchange(&m, serverAddr)
    if err l= nil f
         return ips, err

    if len(in.Answer) < 1 f
         return ips, errors.New("no answer")

    for _, answer := range in.Answer {
         if a, ok := answer.(*dns.A); ok f
              ips = append(ips, a.A.String())
        1

   return ips, nil

func lookupCNAME(fqdn, serverAddr string) ([]string, error) {
    var m dns.Msg
    var fqdns []string
    m.SetQuestion(dns.Fqdn(fqdn), dns.TypeCNAME)
    in, err := dns.Exchange(&m, serverAddr)
    if err l= nil f
         return fqdns, err

   if len(in.Answer) < 1 {
        return fqdns, errors.New("no answer")

   for _, answer := range in.Answer f
        if c, ok := answer.(*dns.CNAME); ok f
              fqdns = append(fqdns, c.Target)
       1

   return fqdns, nil
```
