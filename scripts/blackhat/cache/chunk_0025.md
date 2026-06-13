58   Bölüm 3

Bu projeye hata işleme ve veri doğrulama eklemek isteyeceksiniz, ancak bu haliyle bile yeni API’nizle Shodan verilerini çekmek ve göstermek için iyi bir örnek işlevi görüyor. Artık kolayca genişletilerek diğer Shodan fonksiyonlarını destekleyip test edecek şekilde kullanılabilecek çalışan bir kod tabanınız var.

## Metasploit ile Etkileşim

Metasploit, keşif (reconnaissance), sömürü (exploitation), komuta ve kontrol (command and control), kalıcılık (persistence), yatay ağ hareketi (lateral network movement), yük/faydalı yük (payload) oluşturma ve teslim etme, ayrıcalık yükseltme (privilege escalation) ve daha birçok saldırgan tekniği gerçekleştirmek için kullanılan bir çerçevedir (framework). Daha da güzeli, ürünün topluluk sürümü ücretsizdir, Linux ve macOS üzerinde çalışır ve aktif olarak bakım görmektedir. Her türlü saldırgan angajman (adversarial engagement) için temel olan Metasploit, sızma testçileri tarafından kullanılan temel bir araçtır ve işlevselliğiyle uzaktan etkileşime izin vermek için bir uzak yordam çağrısı (RPC, remote procedure call) API’si sunar.

Bu bölümde, uzak bir Metasploit örneğiyle etkileşime giren bir istemci oluşturacaksınız. Geliştireceğiniz Metasploit istemcisi, inşa ettiğiniz Shodan koduna oldukça benzer şekilde, mevcut tüm işlevselliğin kapsamlı bir implementasyonunu içermeyecek. Bunun yerine, ihtiyaç duydukça ek işlevler ekleyebileceğiniz bir temel oluşturacak. Uygulamanın Shodan örneğine göre daha karmaşık olduğunu göreceksiniz; bu da Metasploit ile etkileşimi daha zorlayıcı bir ilerleme haline getiriyor.

### Ortamınızı Hazırlama

Bu bölüme devam etmeden önce, hala yapmadıysanız Metasploit topluluk sürümünü indirin ve kurun. Metasploit konsolunu ve `msgrpc` modülü aracılığıyla RPC dinleyicisini başlatın. Ardından, RPC sunucusunun dinleyeceği IP adresi olan sunucu host’unu (`ServerHost`) ve bir parola belirleyin; bu, Liste 3-12’de gösterilmektedir.

```bash
$ msfconsole
msf > load msgrpc Pass=s3cr3t ServerHost=10.0.1.6
[*] MSGRPC Service: 10.0.1.6:55552
[*] MSGRPC Username: msf
[*] MSGRPC Password: s3cr3t
[*] Successfully loaded plugin: msgrpc
```

**Liste 3-12: Metasploit ve `msgrpc` sunucusunu başlatma**

Kodu daha taşınabilir yapmak ve sabit değerler (hardcode) kullanmaktan kaçınmak için, RPC örneğiniz için tanımladığınız değerleri aşağıdaki ortam değişkenlerine atayın. Bu, 58. sayfadaki “Creating a Client (Bir İstemci Oluşturma)” bölümünde Shodan ile etkileşim için kullanılan Shodan API anahtarı için yaptığınıza benzer.

```bash
$ export MSFHOST=10.0.1.6:55552
$ export MSFPASS=s3cr3t
```

Şu anda Metasploit ve RPC sunucusunun çalışıyor olması gerekir.

---

Metasploit sömürme (exploitation) ayrıntıları ve kullanımına ilişkin detaylar bu kitabın kapsamı dışında olduğundan, saf kurnazlık ve hileyle uzak bir Windows sistemini halihazırda ele geçirdiğinizi ve gelişmiş sömürü sonrası (post-exploitation) faaliyetler için Metasploit’in Meterpreter yükünü (payload) kullandığınızı varsayalım. Burada çabalarınızı, kurulmuş Meterpreter oturumlarını listelemek ve onlarla etkileşime geçmek için Metasploit ile uzaktan nasıl iletişim kurabileceğinize odaklayacaksınız. Daha önce belirttiğimiz gibi, bu kod biraz daha zahmetli; bu yüzden kodu kasıtlı olarak asgari seviyeye indireceğiz—sizin kodu alıp özgül ihtiyaçlarınıza göre genişletebilmeniz için yeterli olacak kadar.

Shodan örneğindekiyle aynı proje yol haritasını izleyin: Metasploit API’sini inceleyin, projeyi bir kütüphane (library) formatında düzenleyin, veri tiplerini tanımlayın, istemci API fonksiyonlarını implemente edin ve son olarak kütüphaneyi kullanan bir test düzeneği (test rig) inşa edin.

İlk olarak, Rapid7’nin resmi sitesindeki Metasploit API geliştirici dokümantasyonunu inceleyin (`https://metasploithelp.rapid7.com/docs/rpc-api`). Sunulan işlevsellik oldukça geniş kapsamlıdır; yerel etkileşimle yapabildiğiniz hemen hemen her şeyi uzaktan yapmanıza olanak tanır. JSON kullanan Shodan’ın aksine Metasploit, kompakt ve verimli bir ikili (binary) format olan MessagePack’i kullanır. Go, standart bir MessagePack paketi içermediğinden, tam özellikli bir topluluk implementasyonu kullanacaksınız. Bunu komut satırından aşağıdaki komutu çalıştırarak yükleyin:

```bash
$ go get gopkg.in/vmihailenco/msgpack.v2
```

Kod içinde bu implementasyona `msgpack` olarak atıfta bulunacaksınız. MessagePack spesifikasyonunun ayrıntıları hakkında fazla endişelenmeyin. Kısa süre içinde göreceğiniz gibi, çalışan bir istemci oluşturmak için MessagePack hakkında bilmeniz gereken şey oldukça az. Go bu konudaki birçok ayrıntıyı gizleyerek, sizin iş mantığına (business logic) odaklanmanızı sağlar. Bilmeniz gereken, tip tanımlarınızı MessagePack dostu (“MessagePack-friendly”) hale getirmek için bunları nasıl anotasyonlayacağınıza dair temel bilgiler. Bunun ötesinde, kodda kodlama (encoding) ve kod çözme (decoding) başlatmaya yönelik kısım, JSON ve XML gibi diğer formatlarla aynıdır.

Sonra, dizin yapınızı oluşturun. Bu örnek için yalnızca iki Go dosyası kullanacaksınız:

```bash
$ tree github.com/blackhat-go/bhg/ch-3/metasploit-minimal
github.com/blackhat-go/bhg/ch-3/metasploit-minimal
├── client
└── rpc
    └── msf.go
```

`msf.go` dosyası `rpc` package’i içinde yer alır ve oluşturduğunuz kütüphaneyi implemente etmek ve test etmek için `client/main.go` dosyasını kullanacaksınız.

> 1. Sömürme (exploitation) konusunda yardım ve pratik için, eğitim amaçlı bir dizi sömürülebilir zafiyet içeren Metasploitable sanal imajını indirip çalıştırmayı düşünebilirsiniz.

60   Bölüm 3

## Amacınızı Tanımlama

Şimdi amacınızı tanımlamanız gerekiyor. Kısalık adına, mevcut Meterpreter oturumlarının listesini alan bir RPC çağrısı yapan ve onunla etkileşime giren kodu implemente edin; yani Metasploit geliştirici dokümantasyonundaki `session.list` metodunu kullanın. İstek formatı şu şekilde tanımlanmıştır:

```text
["session.list", "token"]
```

Bu oldukça minimaldir; implemente edilecek metodun adını ve bir `token` almayı bekler. `token` değeri bir yer tutucudur (placeholder). Dokümantasyonu incelerseniz bunun, RPC sunucusuna başarılı girişten sonra verilen bir kimlik doğrulama jetonu (authentication token) olduğunu göreceksiniz. Metasploit’in `session.list` metodu için döndürdüğü yanıt ise şu formattadır:
