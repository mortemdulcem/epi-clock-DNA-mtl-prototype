96   Bölüm 4

WebSocket işleyicinizi (handler) oluştururken tartışmasız olarak bulmacanın en zor parçasını hallettiniz. Sırada `serveFile()` adlı başka bir handler fonksiyonu oluşturmak var. Bu fonksiyon, JavaScript şablonunuzun içeriğini, bağlamsal verilerle birlikte alıp döndürecek. Bunu yapmak için `Content-Type` başlığını `application/javascript` olarak ayarlıyorsunuz. Bu, bağlanan tarayıcılara HTTP yanıt gövdesinin içeriğinin JavaScript olarak ele alınması gerektiğini söyler. Handler fonksiyonunun ikinci ve son satırında `jsTemplate.Execute(w, wsAddr)` çağrısını yapıyorsunuz. Sunucunuzu `init()` fonksiyonunda başlatırken (`bootstrap`) `logger.js` dosyasını nasıl parse ettiğinizi hatırlıyor musunuz? Sonucu `jsTemplate` adlı değişkende saklamıştınız. Bu satır söz konusu şablonu işler. Ona bir `io.Writer` (bu örnekte `http.ResponseWriter` olan `w`) ve `interface{}` tipinde bağlamsal verinizin referansını geçiriyorsunuz. `interface{}` tipi, ister string, ister struct ya da başka bir şey olsun, herhangi bir tipte değişken geçirmenize izin verir. Bu durumda `wsAddr` adlı bir string değişkeni geçiriyorsunuz. `init()` fonksiyonuna geri dönerseniz, bu değişkenin WebSocket sunucunuzun adresini içerdiğini ve komut satırı argümanı üzerinden ayarlandığını görürsünüz. Kısaca, bu satır şablonu verilerle doldurur ve HTTP yanıtı olarak yazar. Oldukça şık!

Handler fonksiyonlarınızı, `serveFile()` ve `serveWS()` fonksiyonlarını uyguladınız. Şimdi sadece, yürütmeyi (execution) uygun handler’a aktarabilmek için router’ınızı desen eşleştirme (pattern matching) yapacak şekilde yapılandırmanız gerekiyor. Bunu, daha önce yaptığınıza çok benzer biçimde, `main()` fonksiyonunuzda yapıyorsunuz. İki handler fonksiyonunuzdan ilki `/ws` URL desenini eşleştirir ve WebSocket bağlantılarını yükseltmek (upgrade) ve işlemek için `serveWS` fonksiyonunu çalıştırır. İkinci rota `/k.js` desenini eşleştirir ve bunun sonucu olarak `serveFile` fonksiyonunu çalıştırır. Sunucunuz, işlenmiş (rendered) JavaScript şablonunu istemciye bu şekilde gönderir.

Şimdi sunucuyu ayağa kaldıralım. HTML dosyasını açarsanız, `connection established` yazan bir mesaj görmelisiniz. Bu mesaj, JavaScript dosyanız tarayıcıda render edilip bir WebSocket bağlantısı talebinde bulunduğu için loglanır. Form elemanlarına kimlik bilgileriniz (credential) girerseniz, bunların sunucuda `stdout`’a yazdırıldığını görmelisiniz:

```bash
$ go run main.go -listen-addr.127.0.0.1:8080 -ws-addr.127.0.0.1:8080
Connection from 127.0.0.1:58438
From 127.0.0.1:58438: u
From 127.0.0.1:58438: s
From 127.0.0.1:58438: e
From 127.0.0.1:58438: r
From 127.0.0.1:58438:
From 127.0.0.1:58438: p
From 127.0.0.1:58438: @
From 127.0.0.1:58438: s
From 127.0.0.1:58438: s
From 127.0.0.1:58438: w
From 127.0.0.1:58438: o
From 127.0.0.1:58438: r
From 127.0.0.1:58438: d
```

HTTP Sunucuları, Yönlendirme (Routing) ve Ara Katman (Middleware)   97

Bunu başardınız! Çalışıyor! Çıktınız, giriş formunu doldururken basılan her bir tuş vuruşunu ayrı ayrı listeliyor. Bu örnekte, bir kullanıcı kimlik bilgileri seti söz konusu. Sorun yaşıyorsanız, komut satırı argümanları olarak doğru adresleri verdiğinizden emin olun. Ayrıca, `logger.js` dosyasını `localhost:8080` dışındaki bir sunucudan çağırmaya çalışıyorsanız, HTML dosyasının kendisini de biraz ayarlamanız gerekebilir.

Bu kodu birkaç şekilde geliştirebilirsiniz. Örneğin, çıktıyı terminal yerine bir dosyaya ya da başka kalıcı bir depolamaya loglamak isteyebilirsiniz. Bu sayede terminal penceresi kapanırsa veya sunucu yeniden başlatılırsa verilerinizi kaybetme olasılığınız azalır. Ayrıca, keylogger’ınız aynı anda birden fazla istemcinin tuş vuruşlarını loglarsa, çıktı verileri karışarak belirli bir kullanıcının kimlik bilgilerinin yeniden birleştirilmesini zorlaştırabilir. Bunu, örneğin, tuş vuruşlarını benzersiz istemci/port kaynağına göre gruplayan daha iyi bir sunum formatı (presentation format) bularak önleyebilirsiniz.

Kimlik bilgisi toplama (credential harvesting) yolculuğunuz tamamlandı. Bu bölümü, HTTP komuta-kontrol (command-and-control, C2) bağlantılarını çoklayarak (multiplexing) sonlandıracağız.

## Komuta-Kontrol Çoklama (Multiplexing Command-and-Control)

HTTP sunucuları bölümünün son kısmına geldiniz. Burada, Meterpreter HTTP bağlantılarını farklı arka uç (backend) kontrol sunucularına nasıl çoklayacağınızı inceleyeceksiniz. Meterpreter, Metasploit exploitation framework’ü içinde yer alan, popüler ve esnek bir komuta-kontrol (C2) paketidir. Metasploit veya Meterpreter hakkında çok fazla ayrıntıya girmeyeceğiz. Eğer bunlara yeniyseniz, mevcut birçok öğretici (tutorial) veya dokümantasyon sitesinden birini okumanızı öneririz.

Bu bölümde, Go ile ters HTTP proxy (reverse HTTP proxy) oluşturmayı adım adım ele alacağız; böylece gelen Meterpreter oturumlarınızı `Host` HTTP başlığına göre dinamik olarak yönlendirebileceksiniz. Bu, sanal web sitesi barındırmanın (virtual hosting) çalışma şeklidir. Ancak bu sefer, farklı yerel dosya ve dizinler sunmak yerine bağlantıyı farklı Meterpreter dinleyicilerine (listener) proxy’leyeceksiniz. Bu birkaç açıdan ilginç bir kullanım senaryosudur.

İlk olarak, proxy’niz bir yönlendirici (redirector) gibi davranır; böylece yalnızca o alan adını (domain name) ve IP adresini dışa açar, Metasploit dinleyicilerinizi açığa çıkarmazsınız. Eğer redirector kara listeye alınırsa, C2 sunucunuzu taşımak zorunda kalmadan yalnızca redirector’u taşıyabilirsiniz. İkinci olarak, buradaki kavramları genişleterek domain fronting yapabilirsiniz; bu, kısıtlayıcı egress kontrollerini atlatmak için güvenilen üçüncü taraf alan adlarından (çoğunlukla bulut sağlayıcıları) yararlanma tekniğidir. Burada tam teşekküllü bir örneğe girmeyeceğiz ama bu konuyu derinlemesine incelemenizi şiddetle tavsiye ederiz; oldukça güçlü olabilir ve kısıtlı ağlardan çıkış (egress) yapmanıza olanak tanır. Son olarak bu kullanım senaryosu, farklı hedef organizasyonlara saldıran bir müttefikler ekibi arasında tek bir host/port kombinasyonunu nasıl paylaşabileceğinizi gösterir. 80 ve 443 portları en muhtemel izin verilen egress portları olduğundan, proxy’nizi bu portlarda dinlemek için kullanabilir ve bağlantıları doğru dinleyiciye akıllıca yönlendirebilirsiniz.

Plan şu: İki ayrı Meterpreter ters HTTP dinleyicisi kuracaksınız. Bu örnekte, bunlar IP adresi `10.0.1.20` olan bir sanal makine üzerinde bulunacak, ancak rahatlıkla ayrı hostlarda da olabilirler. Dinleyicilerinizi sırasıyla 10080 ve 20080 portlarına bağlayacaksınız (`bind`). Gerçek bir durumda, proxy bu portlara erişebildiği sürece bu dinleyiciler herhangi bir yerde çalışabilir. Metasploit’in kurulu olduğundan emin olun (Kali Linux’ta önceden kurulu gelir); ardından dinleyicilerinizi başlatın.
