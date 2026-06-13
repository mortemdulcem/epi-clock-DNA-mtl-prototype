### Tarayıcıyı Çalıştırma

Hem eklentinizi hem de onu kullanan ana programı oluşturduğunuza göre, derlenmiş paylaşılan nesnenizi tarayıcının `plug-ins` dizinine yönlendirmek için `-o` seçeneğini kullanarak eklentinizi derleyin:

```bash
$ go build -buildmode=plugin -o /path/to/plugins/tomcat.so
```

Sonra tarayıcınızı (`cmd/scanner/main.go`) çalıştırarak eklentiyi tespit ettiğini, yüklediğini ve eklentinin `Check()` metodunu yürüttüğünü doğrulayın:

```bash
$ go run main.go
Found plugin: tomcat.so
2020/01/15 15:45:18 Checking for Tomcat Manager...
2020/01/15 15:45:18 Host responded to /manager/html request
2020/01/15 15:45:18 Host requires authentication. Proceeding with password guessing...
2020/01/15 15:45:18 Host is vulnerable: Valid credentials found - tomcat:tomcat
```

Şuna bakın! Çalışıyor! Tarayıcınız, eklentinizin içindeki kodu çağırabiliyor. `plug-ins` dizinine istediğiniz sayıda başka eklenti bırakabilirsiniz. Tarayıcınız her birini okumaya çalışacak ve zafiyet kontrolü işlevlerini tetikleyecektir.

Geliştirdiğimiz kod bir dizi iyileştirmeden faydalanabilir. Bu iyileştirmeleri size egzersiz olarak bırakıyoruz. Şunları denemenizi teşvik ediyoruz:

- Farklı bir zafiyeti kontrol eden bir eklenti oluşturun.
- Daha kapsamlı testler için ana programın dinamik olarak bir hedef listesi ve bu hedeflerin açık portlarını almasını sağlayın.
- Kodu yalnızca ilgili eklentileri çağıracak şekilde geliştirin. Şu anda kod, verilen hedef ve port için tüm eklentileri çağırıyor. Bu ideal değil. Örneğin, hedef port HTTP veya HTTPS değilse Tomcat denetleyicisini çağırmak istemezsiniz.
- Eklenti sisteminizi Windows üzerinde çalışacak şekilde dönüştürün ve eklenti tipi olarak DLL kullanın.

Sonraki bölümde, aynı zafiyet kontrolü eklentisini farklı, resmi olmayan bir eklenti sistemi olan Lua ile inşa edeceksiniz.

### Lua ile Eklenti İnşa Etmek

Go ile eklenti yapılabilir programlar oluştururken Go'nun yerleşik `-buildmode` özelliğini kullanmanın sınırlamaları vardır; özellikle de çok taşınabilir olmaması, yani eklentilerin güzelce çapraz derlenememesi gibi. Bu bölümde, bu eksikliği Lua ile eklentiler oluşturarak aşmanın bir yoluna bakacağız. Lua, çeşitli araçları genişletmek için kullanılan bir betik (script) dilidir. Dilin kendisi gömülebilir (embeddable), güçlü, hızlı ve iyi belgelenmiştir. Nmap ve Wireshark gibi güvenlik araçları, tam da şimdi yapacağınız gibi, eklentiler oluşturmak için Lua kullanır. Daha fazla bilgi için resmi siteye, `https://www.lua.org` adresine bakın.

Lua'yı Go içinde kullanmak için, Lua betiklerini doğrudan Go içinde derleyip çalıştırabilen üçüncü taraf `gopher-lua` paketini kullanacaksınız. Sisteminize aşağıdaki komutla kurun:

```bash
$ go get github.com/yuin/gopher-lua
```

Şimdi, taşınabilirlik için ödeyeceğiniz bedelin artan karmaşıklık olacağı konusunda önceden uyaralım. Bunun nedeni, Lua'nın programınızdaki ya da çeşitli Go paketlerindeki fonksiyonları çağırmak için örtük (implicit) bir yönteme sahip olmaması ve veri tipleriniz hakkında hiçbir bilgiye sahip olmamasıdır. Bu problemi çözmek için iki tasarım deseninden birini seçmek zorundasınız:

- Lua eklentinizde tek bir giriş noktası (entry point) çağırın ve eklentinin, (HTTP istekleri göndermek için gerekenler gibi) yardımcı metotları başka Lua paketleri üzerinden çağırmasına izin verin. Bu, ana programınızı basit tutar ama taşınabilirliği azaltır ve bağımlılık yönetimini kabusa çevirebilir. Örneğin, bir Lua eklentisinin çekirdek Lua paketleri arasında yer almayan üçüncü taraf bir bağımlılık gerektirdiğini düşünün. Eklentiniz, onu başka bir sisteme taşıdığınız anda bozulur. Ayrıca, iki ayrı eklentinin aynı paketin farklı sürümlerine ihtiyaç duyması durumunda ne olur?

- Ana programınızda yardımcı fonksiyonları (örneğin `net/http` paketindeki fonksiyonlar) eklentinin etkileşime girebileceği bir dış yüz (facade) ortaya çıkaracak şekilde sarmalayın. Bu elbette tüm Go fonksiyonlarını ve tiplerini ortaya çıkarmak için kapsamlı kod yazmanızı gerektirir. Ancak bir kez bu kodu yazdığınızda, eklentiler bunu tutarlı bir şekilde yeniden kullanabilir. Ayrıca, ilk tasarım desenini kullansaydınız yaşayacağınız Lua bağımlılık sorunları hakkında kısmen de olsa endişelenmek zorunda kalmazsınız (tabii ki, bir eklenti yazarının üçüncü taraf bir kütüphane kullanarak bir şeyleri bozma ihtimali her zaman vardır).

Bu bölümün geri kalanında ikinci tasarım deseni üzerinde çalışacaksınız. Lua eklentilerinizin erişebileceği bir dış yüz (facade) ortaya çıkarmak için Go fonksiyonlarınızı sarmalayacaksınız. İki çözümden daha iyi olanı budur (ve ayrıca *facade* kelimesi, çok havalı bir şey inşa ediyormuşsunuz gibi hissettirir).

Eklentileri yükleyen ve çalıştıran, önyükleme (bootstrapping) amacı taşıyan çekirdek Go kodu, bu alıştırma boyunca tek bir dosyada yer alacaktır. Basitlik uğruna, özellikle `https://github.com/yuin/gopher-lua` adresindeki örneklerde kullanılan bazı kalıpları çıkardık. Kullanıcı tanımlı tipler gibi bazı kalıpların, kodu daha az okunabilir hale getirdiğini düşündük. Gerçek bir uygulamada, daha fazla esneklik için muhtemelen bu kalıplardan bazılarını dahil etmek isteyeceksiniz. Ayrıca daha kapsamlı hata ve tip kontrolü eklemek isteyeceksiniz.

Ana programınız, GET ve HEAD HTTP istekleri göndermek için fonksiyonlar tanımlayacak, bu fonksiyonları Lua sanal makinesine (VM) kaydedecek ve tanımlı bir `plug-ins` dizininden Lua betiklerinizi yükleyip çalıştıracak. Bir önceki bölümdekiyle aynı Tomcat parola tahmin (password guessing) eklentisini inşa edeceksiniz; böylece iki sürümü karşılaştırabileceksiniz.

### head() HTTP Fonksiyonunu Oluşturma

Ana programla başlayalım. Önce, Go'nun `net/http` paketine yapılan çağrıları saran `head()` HTTP fonksiyonuna bakalım (Liste 10-4).

```go
func head(L *lua.LState) int {
    var (
        host string
        port uint64
        path string
        resp *http.Response
        err error
        url string
```
