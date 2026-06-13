66   Bölüm 3

`New()` isimli, önyükleme (bootstrapping) amacıyla kullanılmak üzere tasarlanmış bir fonksiyon zaten yazmıştınız; şimdi bu fonksiyonu yamalayarak, kimlik doğrulamanın sürecin bir parçası olarak dahil edildiği yeni bir uygulamanın nasıl göründüğüne bakalım (Liste 3-18’e bakın).

```go
func New(host, user, pass string) (*Metasploit, error)0 {
    msf := &Metasploit{
        host: host,
        user: user,
        pass: pass,
    }
    if err :=
            msf.Login()0; err 1= nil {
         return nil, err
    }
    return msf, nil
```

Liste 3-18: Metasploit oturum açma işlemini gömerek istemciyi başlatmak (/ch-3/metasploit-minimal/rpc/msf.go)

Yamalı kod artık dönüş değer kümesine 0 bir hata nesnesi de ekliyor. Bu, olası kimlik doğrulama hatalarına dikkat çekmek için. Ayrıca, mantığa `Login()` metoduna 0 açık bir çağrı eklendi. Metasploit struct’ı bu `New()` fonksiyonu kullanılarak örneklendirildiği sürece, kimlik doğrulanmış metot çağrıları geçerli bir kimlik doğrulama belirtecine (token) erişime sahip olacaktır.

## Bir Yardımcı Program Oluşturma

Bu örneğin sonuna yaklaşırken, son çabanız yeni parlak kütüphanenizi kullanan yardımcı (utility) programı oluşturmak. Liste 3-19’daki kodu `client/main.go` dosyasına girin, çalıştırın ve sihrin gerçekleşmesini izleyin.

```go
package main

import (
   "fmt"
   "log"

    "github.com/blackhat-go/bhg/ch-3/metasploit-minimal/rpc "
```

```go
func main() {
    host := os.Getenv("MSFHOST")
    pass := os.Getenv("MSFPASS")
    user := "msf"

    if host == "" 11 Pass "
        log.Fatalln("Missing required environment variable MSFHOST or MSFPASS")
```

```go
                    msf, err := rpc.New(host, user, pass)0
                    if err != nil {
                        log.Panicln(err)
                    1
                    defer msf.Logout()

                    sessions, err := msf.SessionList()0
                    if err != nil
                        log.Panicln(err)
                    1
                    fmt.Println("Sessions:")
                    for _, session := range sessions {
                        fmt.Printf("W %s\n", session.ID, session.Info)
```

Liste 3-19: `msfrpc` paketimizi tüketmek (/ch-3/metasploit-minimal/client/main.go)

İlk olarak, RPC istemcisini önyükleyin ve yeni bir Metasploit struct’ı başlatın 0. Bu fonksiyonu, başlatma sırasında kimlik doğrulama gerçekleştirecek şekilde az önce güncellediğinizi unutmayın. Sonra, `Logout()` metoduna 0 ertelenmiş (deferred) bir çağrı yaparak uygun temizlik işlemini gerçekleştirdiğinizden emin olun. Bu, `main` fonksiyonu döndüğünde veya çıktığında çalışacaktır. Daha sonra `SessionList()` metoduna 0 bir çağrı yapar ve yanıt üzerinde yineleme (iterate) ederek kullanılabilir Meterpreter oturumlarını listelersiniz 0.

Epeyce kod yazdınız, ancak neyse ki diğer API çağrılarını uygulamak çok daha az iş gerektirecektir; çünkü yalnızca istek ve yanıt tiplerini tanımlayıp, uzak çağrıyı yapan kütüphane metodunu inşa edeceksiniz. İşte istemci yardımcı programımızdan doğrudan üretilen, kurulmuş bir Meterpreter oturumunu gösteren örnek çıktı:

```bash
$ go run main.go
Sessions:
    1. WIN-HOME\jsmith @ WIN-HOME
```

İşte bu kadar. Uzak bir Metasploit örneğiyle etkileşime girip kullanılabilir Meterpreter oturumlarını almak için bir kütüphane ve istemci yardımcı programı oluşturmayı başarıyla tamamladınız. Sırada arama motoru yanıt kazıma (scraping) ve doküman meta verisi ayrıştırma var.

## Bing Kazıma ile Doküman Meta Verisi Ayrıştırma

Shodan bölümünde özellikle vurguladığımız gibi, göreli olarak zararsız görünen bilgi—doğru bağlamda değerlendirildiğinde—kritik hale gelebilir ve bir organizasyona yönelik saldırınızın başarılı olma olasılığını artırabilir. Çalışan isimleri, telefon numaraları, e-posta adresleri ve istemci yazılım sürümleri gibi bilgiler, doğrudan sömürülebilen veya daha etkili ve yüksek hedefli (targeted) saldırılar oluşturmak için kullanılabilen somut ya da uygulanabilir bilgi sağladıkları için genellikle en değerli olanlardır. FOCA isimli araç tarafından popülerleştirilen bu tür bilgi kaynaklarından biri, doküman meta verisidir (metadata).

Uygulamalar, diske kaydedilen bir dosyanın yapısı içine keyfi bilgiler saklar. Bazı durumlarda, bu bilgiler coğrafi koordinatları, uygulama sürümlerini, işletim sistemi bilgilerini ve kullanıcı adlarını içerebilir. Daha da iyisi, arama motorları belirli bir organizasyona ait belirli dosyaları getirmenizi sağlayan gelişmiş sorgu filtrelerine sahiptir. Bu bölümün geri kalanı, hedef organizasyonun Microsoft Office dokümanlarını elde etmek için Bing arama sonuçlarını kazıyan (veya avukatımın dediği gibi, indeksleyen) bir araç inşa etmeye ve sonrasında ilgili meta verileri çıkarmaya odaklanıyor.

### Ortamı Hazırlama ve Planlama

Özel detaylara dalmadan önce, hedefleri ortaya koyarak başlayacağız. Öncelikle yalnızca Office Open XML dokümanlarına—`xlsx`, `docx`, `pptx` gibi uzantılarla bitenlere—odaklanacaksınız. Elbette eski tip Office veri türlerini de dahil edebilirsiniz, ancak ikili (binary) formatlar bunları katlanarak daha karmaşık hale getirir; bu da kod karmaşıklığını artırır ve okunabilirliği azaltır. PDF dosyalarıyla çalışmak için de aynı şey geçerlidir. Ayrıca geliştireceğiniz kod Bing sayfalama (pagination) işlemini ele almayacak; bunun yerine yalnızca ilk sayfa arama sonuçlarını ayrıştıracaktır. Bu işlevi kendi çalışan örneğinize eklemenizi ve Open XML’in ötesindeki dosya türlerini keşfetmenizi teşvik ediyoruz.

Neden HTML kazıma yapmak yerine, bunu inşa ederken Bing Search API’lerini kullanmıyoruz? Çünkü yapılandırılmış API’lerle etkileşime giren istemciler oluşturmayı hâlihazırda biliyorsunuz. HTML sayfalarını kazımanın pratik kullanım alanları var, özellikle de hiçbir API mevcut değilken. Zaten bildiklerinizi tekrar etmek yerine, bunu veri çıkarmanın yeni bir yöntemini tanıtmak için fırsat olarak kullanacağız. `goquery` isimli mükemmel bir paket kullanacaksınız; bu paket, HTML dokümanlarını gezmek ve içlerinden veri seçmek için sezgisel bir sözdizimine sahip olan `jQuery` JavaScript kütüphanesinin işlevselliğini taklit eder. `goquery`’yi kurarak başlayın:

```bash
$ go get github.com/PuerkitoBio/goquery
```

Neyse ki geliştirmeyi tamamlamak için gereken tek önkoşul yazılım bu. Open XML dosyalarıyla etkileşime geçmek için standart Go paketlerini kullanacaksınız. Bu dosyalar, dosya uzantılarına rağmen ZIP arşivleridir; açıldıklarında XML dosyaları içerirler. Meta veri, arşivin `docProps` dizini içinde yer alan iki dosyada saklanır:

```bash
$ unzip test.xlsx
$ tree
--snip--
    ---docProps
I       I ---app.xml
I       I ---core.xml
--snip-
```

`core.xml` dosyası yazar bilgilerini ve değişiklik ayrıntılarını içerir. Yapısı şu şekildedir:
