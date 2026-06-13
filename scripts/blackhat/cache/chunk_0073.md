Kod temelde, 0’dan başlayarak tek büyük döngüden oluşur. Program her döngüye girdiğinde, sağlayacağınız kullanıcı adına (username) bir karakter daha ekler. Bu örnekte 1 ile 2.500 karakter uzunluğu arasında kullanıcı adları göndereceksiniz.

Döngünün her yinelemesinde hedef FTP sunucusuna 0 üzerinde bir TCP bağlantısı kurarsınız. FTP servisiyle ne zaman etkileşime girerseniz (ister ilk bağlantı olsun ister sonraki komutlar), sunucudan gelen yanıtı açıkça tek satır olarak okursunuz 0. Bu, TCP yanıtlarını beklerken kodun bloklanmasını sağlar; böylece komutlarınızı, paketler gidiş-dönüş yolculuklarını tamamlamadan, erken göndermemiş olursunuz.

Daha sonra, önce gösterdiğimiz şekilde `A` karakterlerinden oluşan dizeyi oluşturmak için başka bir `for` döngüsü kullanırsınız 0. Dize uzunluğunu, döngünün o anki yinelemesine bağlı olarak oluşturmak için dış döngünün `i` indeksini kullanırsınız; böylece program her başa sardığında uzunluk bir artar. Bu değeri kullanarak `fmt.Fprintf(conn, raw, user)` ile `USER` komutunu yazarsınız 0.

FTP sunucusuyla etkileşiminizi bu noktada sonlandırabilmenize rağmen (sonuçta yalnızca `USER` komutunu fuzz ediyorsunuz), işlemi tamamlamak için `PASS` komutunu da göndermeye devam edersiniz. Son olarak, bağlantınızı düzgün bir şekilde kapatırsınız 0.

Dikkate değer olan, anormal bağlantı davranışının bir hizmet kesintisini gösterebileceği iki nokta olmasıdır, 0 ve 0; bu da olası bir arabellek taşmasına (buffer overflow) işaret eder: bağlantının ilk kurulduğu an ve bağlantının kapandığı an. Program bir sonraki döngüye girdiğinde bağlantı kuramıyorsanız, muhtemelen bir şeyler ters gitmiştir. Ardından, hizmetin bir arabellek taşması sonucu çöküp çökmediğini kontrol etmek isteyeceksiniz.

Kurulmuş bir bağlantıyı kapatamıyorsanız bu, uzak FTP servisinin ani şekilde bağlantıyı kesmesinden kaynaklanan anormal bir davranışa işaret ediyor olabilir; ancak büyük ihtimalle bir arabellek taşmasından kaynaklanmamaktadır. Bu anomal durum kayda geçirilir, fakat program çalışmaya devam eder.

Şekil 9-1’de gösterilen paket yakalama (capture), her bir ardışık `USER` komutunun uzunluğunun arttığını gösterir ve kodunuzun istenildiği gibi çalıştığını doğrular.

> Şekil 9-1: Program her döngüye girdiğinde bir harf artan `USER` komutunu gösteren bir Wireshark kaydı

Kodu esneklik ve kullanım kolaylığı açısından çeşitli şekillerde geliştirebilirsiniz. Örneğin, muhtemelen IP, port ve yineleme (iteration) değerlerini kod içine sabitlenmiş (hardcoded) olmaktan çıkarıp, bunları komut satırı argümanları veya bir yapılandırma (configuration) dosyası üzerinden almak istersiniz. Bu kullanılabilirlik (usability) güncellemelerini bir alıştırma olarak yapmanızı öneriyoruz. Ayrıca, kodu kimlik doğrulama (authentication) sonrası komutları da fuzz edecek şekilde genişletebilirsiniz. Özellikle, aracı `CWD/CD` komutunu fuzz edecek şekilde güncelleyebilirsiniz. Çeşitli araçlar tarihsel olarak bu komuta karşı hassas olmuştur.

---

`username=someuser&password=somepass`

Giriş (login) formu, `http://10.0.1.20:8080/WebApplication/login.jsp` adresine bir POST isteği gönderir. İki form parametresi vardır: `username` ve `password`. Bu örnekte, kısalık açısından fuzz etmeyi `username` alanıyla sınırlayacağız. Kodun kendisi oldukça derli topludur; birkaç döngüden, bazı düzenli ifadelerden (regular expressions) ve bir HTTP isteği oluşturmaktan oluşur. Kod, Liste 9-2’de gösterilmiştir.

```go
func main() {
    payloads := []string{
        "baseline",

    sqlErrors := °string{
        "SQL",
        "MySQL",

        "syntax",

    errRegexes := H*regexp.Regexp{}
    for _, e := range sqlErrors {
        re := regexp.MustCompile(fmt.Sprintf(". *%s.*", e))
        errRegexes = append(errRegexes, re)
```
