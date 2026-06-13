Hashlemeyi Keşfetmek
Hashleme, daha önce bahsettiğimiz gibi, değişken uzunluktaki bir girdiye dayanarak sabit uzunlukta, olasılıksal olarak benzersiz bir çıktı üreten tek yönlü bir fonksiyondur. Bu hash değerini tersine çevirerek özgün girdi kaynağını geri elde edemezsiniz. Hash'ler genellikle, özgün, düz metin (cleartext) kaynağının gelecekteki işleme için gerekli olmadığı durumlarda veya verinin bütünlüğünü takip etmek için kullanılır. Örneğin, şifrenin düz metin halini saklamak kötü bir uygulamadır ve genellikle gereksizdir; bunun yerine hash değerini saklarsınız (idealde, tekrar eden değerler arasında rastgelelik sağlamak için tuz (salt) kullanarak).

Hashlemeyi Go'da göstermek için iki örneğe bakacağız. İlk örnek, çevrimdışı bir sözlük saldırısı (dictionary attack) kullanarak verilmiş bir MD5 veya SHA-512 hash'ini kırmaya çalışır. İkinci örnek ise bir bcrypt uygulamasını gösterir. Daha önce bahsedildiği gibi, bcrypt, şifreler gibi hassas verileri hashlemek için daha güvenli bir algoritmadır. Algoritma ayrıca hızını düşüren bir özelliğe sahiptir; bu da şifrelerin kırılmasını zorlaştırır.

### Bir MD5 veya SHA-256 Hash'ini Kırmak

Liste 11-1 hash kırma kodunu gösteriyor. (Kök dizindeki `/` altındaki tüm kod listeleri, verilen GitHub deposu `https://github.com/blackhat-go/bhg/` içinde yer almaktadır.) Hash'ler doğrudan tersine çevrilemediğinden, kod bunun yerine, bir kelime listesinden alınan yaygın kelimelerin hash'lerini üreterek ve ortaya çıkan hash değerini elinizdeki hash ile karşılaştırarak hash'in düz metin değerini tahmin etmeye çalışır. Eğer iki hash uyuşursa, muhtemelen düz metin değeri doğru tahmin etmişsiniz demektir.

```go
var md5hash = "77f62e3524cd583d698d51fa24fdff4f"
var sha256hash =
"95a5e1547df73abdd4781b6c9e55f3377c15110888011738c2727dbd887d4ced"

func main() {
    f, err :=os.Openrwordlist.txt")0
    if err != nil {
        log.Fatalln(err)

    defer f.Close()

 O scanner := bufio.NewScanner(f)
    for scanner.Scan() {
         password := scanner.Text()
         hash := fmt.Sprintf("%x", md5.Suma]byte(password))0)
         if hash == md5hash {
              fmt.Printf("[+] Password found (MD5): %s\n", password)

        hash = fmt.Sprintf("%x", sha256.Sum256([]byte(password))CD)
        if hash == sha256hash f
             fmt.Printf("[+] Password found (SHA-256): %s\n", password)

    if err := scanner.Err(); err != nil {
         log.Fatalln(err)
```

**Liste 11-1:** MD5 ve SHA-256 hash'lerini kırma (`/ch-11/hashes/main.go`)

Önce hedef hash değerlerini tutan iki değişken tanımlayarak başlarsınız. Bunlardan biri bir MD5 hash'idir, diğeri ise bir SHA-256 hash'idir. Bu iki hash'i, sömürü sonrası (post-exploitation) aşamanın bir parçası olarak elde ettiğinizi ve bunların hangi girdiler (düz metin şifreler) tarafından üretildiğini bulmaya çalıştığınızı hayal edin. Çoğu zaman algoritmayı hash'in uzunluğunu inceleyerek belirleyebilirsiniz. Hedefle eşleşen bir hash bulduğunuzda, doğru girdiye ulaştığınızı bilirsiniz.

Denemek istediğiniz girdilerin listesi, daha önce oluşturmuş olduğunuz bir sözlük dosyasında bulunur. Alternatif olarak, yaygın kullanılan şifreler için sözlük dosyalarını bulmak üzere Google araması yapabilirsiniz. MD5 hash'ini kontrol etmek için, sözlük dosyasını açar ve dosya tanımlayıcısı üzerinde bir `bufio.Scanner` oluşturarak satır satır okursunuz. Her satır, kontrol etmek istediğiniz tek bir şifre değerinden oluşur. O anki şifre değerini `md5.Sum(input []byte)` adlı fonksiyona geçersiniz. Bu fonksiyon MD5 hash değerini ham bayt (raw bytes) olarak üretir; bu yüzden, değeri `fmt.Sprintf()` fonksiyonunu `%x` biçim dizesiyle (format string) kullanarak onaltılık (hexadecimal) bir string'e çevirirsiniz. Sonuçta, `md5hash` değişkeniniz hedef hash'in onaltılık string gösteriminden oluşur. Değerinizi dönüştürmek, hedef ve hesaplanan hash değerlerini karşılaştırabilmenizi sağlar. Bu hash'ler eşleşirse, program `stdout`'a bir başarı mesajı gösterir.

SHA-256 hash'lerini hesaplamak ve karşılaştırmak için benzer bir işlem yaparsınız. Uygulama, MD5 koduna oldukça benzer. Tek gerçek fark, `sha256` paketinin çeşitli SHA hash uzunluklarını hesaplamak için ek fonksiyonlar içermesidir. Var olmayan `sha256.Sum()` fonksiyonunu çağırmak yerine, hash'in SHA-256 algoritması kullanılarak hesaplandığından emin olmak için `sha256.Sum256(input []byte)` fonksiyonunu çağırırsınız. MD5 örneğinde yaptığınız gibi, ham baytlarınızı bir hex string'e dönüştürür ve SHA-256 hash'lerini karşılaştırarak bir eşleşme olup olmadığını kontrol edersiniz.

### bcrypt Uygulama

Sıradaki örnek, bcrypt kullanarak şifreleri nasıl şifreleyeceğinizi (hash'leyeceğinizi) ve kimlik doğrulaması yapacağınızı gösterir. SHA ve MD5'ten farklı olarak bcrypt, özel olarak şifre hash'leme için tasarlanmıştır; bu da onu uygulama geliştiricileri için SHA veya MD5 ailelerinden daha iyi bir seçenek haline getirir. Varsayılan olarak bir tuz (salt) içerir ve algoritmayı daha fazla kaynak tüketir hale getiren bir maliyet faktörü (cost factor) barındırır. Bu maliyet faktörü, dahili kripto fonksiyonlarının kaç kez çalıştırılacağını kontrol eder; böylece bir şifre hash'ini kırmak için gereken zaman ve çabayı artırır. Şifre yine de bir sözlük saldırısı veya kaba kuvvet (brute-force) saldırısıyla kırılabilir, ancak maliyet (zaman açısından) önemli ölçüde artar; bu da zaman kritik sömürü sonrası aşamalarında hash kırma faaliyetlerini caydırır. Ayrıca, hesaplama gücünün gelişimine karşı koymak için zaman içinde maliyeti artırmak da mümkündür. Bu da bcrypt'i gelecekteki kırma saldırılarına uyarlanabilir kılar.

Liste 11-2, bir bcrypt hash'i oluşturur ve ardından bir düz metin şifrenin verilen bir bcrypt hash'iyle eşleşip eşleşmediğini doğrular.

```go
import (
   "log"

   "golang.org/x/crypto/bcrypt "
)

var storedHash = 124.10$2s3ZwsynF.KuvSUE.5WuwtDrK6UVXcBK/rH84V8q30pg1yNdWLu"

func main() {
    var password string
    if len(os.Args) != 2 {
         log.Fatalln("Usage: bcrypt password")

    password = os.Args[i]

    hash, err := bcrypt.GenerateFromPassword(
        Mbyte(password),
        bcrypt.DefaultCost,
```
