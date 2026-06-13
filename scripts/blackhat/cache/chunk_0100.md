Implementing and Attacking Cryptography   257

Tüketici, `in` kanalından `CryptoData` iş `struct`’larını tekrar tekrar okumak için 0 ile başlayan bir `for` döngüsü kullanır. Kanal kapatıldığında döngü durur. Üreticinin bu kanalı doldurduğunu hatırlayın. Birazdan göreceğiniz gibi, bu kanal, üreticiler tüm anahtar uzayı alt bölümlerini dolaşıp ilgili crypto verilerini `work` kanalına gönderdikten sonra kapanır. Dolayısıyla tüketiciniz, üreticiler üretim işini bitirene kadar döngüye devam eder.

Üretici kodunda yaptığınız gibi, `for` döngüsü içerisinde `select` ifadesi kullanarak `done` kanalının kapatılıp kapatılmadığını 0 kontrol edersiniz ve eğer kapatıldıysa, tüketiciye ek iş çabalarını açıkça durdurmasını söylersiniz. Geçerli bir kredi kartı numarası tespit edildiğinde, bunu az sonra tartışacağımız üzere, bir işçi `done` kanalını kapatacaktır. `default` durumunuz 0, kriptografik olarak ağır işi yapar. İlk olarak şifreli metnin (ciphertext) ilk bloğunu (8 bayt) çözer 0 ve ortaya çıkan düz metnin 8 baytlık, sayısal bir değer olup olmadığını kontrol eder 0. Eğer öyleyse, elinizde potansiyel bir kart numarası vardır ve şifreli metnin ikinci bloğunu çözmeye devam edersiniz 0. Bu şifre çözme fonksiyonlarını, kanaldan okuduğunuz `CryptoData` iş nesnesi içindeki `cipher.Block` alanına erişerek çağırırsınız. Üreticinin, anahtar uzayından alınan benzersiz bir anahtar değeri kullanarak bu `struct`’ı örneklediğini hatırlayın.

Son olarak, düz metnin tamamını Luhn algoritmasına göre doğrular ve ikinci düz metin bloğunun 8 baytlık, sayısal bir değer olduğunu 0 doğrularsınız. Bu kontroller başarıya ulaşırsa, geçerli bir kredi kartı numarası bulduğunuzdan makul ölçüde emin olabilirsiniz. Kart numarasını ve anahtarı `stdout`’a yazdırır ve aradığınızı bulduğunuzu diğer goroutine’lere bildirmek için `close(done)` çağrısı yaparsınız.

### main Fonksiyonunu Yazmak

Bu noktada hem üretici hem de tüketici fonksiyonlarınız hazır ve eşzamanlılık (concurrency) ile çalışacak şekilde donatılmış durumda. Şimdi hepsini `main()` fonksiyonunuzda (Liste 11-11) bir araya getirelim; bu fonksiyon önceki listelerle aynı kaynak dosyada yer alacaktır.

```go
func main() {
    var (
        err        error
        ciphertext []byte

      i-F ciphertext, err = hex.DecodeString("0986f2cclebdc5c2e25d04a136faia6b"); err != nil {
           log . Fatal1n(err)

      var prodWg, consWg sync.WaitGroup
      var min, max, prods = uint64(Ox0000000000), uint64(oxffffffffff), uint64(75)
      var step (max - min) / prods

      done := make(chan structffl
      work := make(chan *CryptoData, 100)
      if (step * prods) < max 0
           step += prods
      II

     var start, end = min, min + step
     log.Println("Starting producers...")
     for i := uint64(0); i < prods; i++ f 0
          if end > max f
               end = max

         generate(start, end, work, done, 8prodWg) 0
         end += step
         start += step

    log.Println("Producers started!")
    log.Println("Starting consumers...")
    for i := 0; i < 30; i++ f 0
         decrypt(ciphertext, work, done, &consWg)

    log.Println("Consumers started!")
    log.Println("Now we wait...")
    prodWg.Wait()411
    close(work)
    consWg.Wait().
    log.Println("Brute-force complete")
```

Liste 11-11: RC2 `main()` fonksiyonu (`ch-11/rc2-brute/main.go`)

`main()` fonksiyonunuz, onaltılık (hexadecimal) bir dize 0 olarak gösterilen şifreli metni çözer. Sonra birkaç değişken 0 oluşturursunuz. Önce, hem üretici hem de tüketici goroutine’lerini takip etmek için kullanılan `WaitGroup` değişkenlerini yaratırsınız. Ayrıca 40 bitlik anahtar uzayındaki en küçük değeri (`0x0000000000`), anahtar uzayındaki en büyük değeri (`0xffffffffff`) ve başlatmayı planladığınız üretici sayısını (bu örnekte 75) takip etmek için birkaç `uint64` değer tanımlarsınız. Bu değerleri, her üreticinin yineleyeceği anahtar sayısını temsil eden bir `step` veya aralık hesaplamak için kullanırsınız; amacınız, bu çabaları tüm üreticiler arasında eşit olarak dağıtmaktır. Ayrıca bir `*CryptoData` `work` kanalı ve bir `done` sinyal kanalı yaratırsınız. Bunları üretici ve tüketici fonksiyonlarınıza ileteceksiniz.

Üreticiler için `step` değerini hesaplamak üzere temel tam sayı aritmetiği yaptığınızdan, anahtar uzayı boyutu, oluşturacağınız üretici sayısının bir katı değilse, bazı verileri kaybetme ihtimaliniz vardır. Buna karşılık vermek ve `math.Ceil()` çağrısında kullanılmak üzere kayan noktalı (floating-point) sayıya dönüştürme sırasında hassasiyet kaybını önlemek için, maksimum anahtar (`step * prods`) değerinin, tüm anahtar uzayı için maksimum değerden (`0xffffffffff`) küçük olup olmadığını 0 kontrol edersiniz. Eğer küçükse, anahtar uzayındaki birkaç değer hesaba katılmayacaktır. Bu eksikliği gidermek için `step` değerinizi basitçe artırırsınız. Anahtar uzayını parçalara ayırmak için kullanabileceğiniz başlangıç ve bitiş ofsetlerini takip etmek üzere `start` ve `end` adlı iki değişkeni başlatırsınız.

Ofsetlerinize ve `step` boyutuna ulaşmak için yaptığınız matematik kesin olmaktan uzaktır ve kodunuzun, izin verilen maksimum anahtar uzayının ötesinde arama yapmasına neden olabilir. Ancak bunu, her bir üreticiyi başlatmak için kullanılan `for` döngüsü 0 içerisinde düzeltiyorsunuz. Döngüde, bitiş `step` değeriniz olan `end` değerini, bu değer izin verilen maksimum anahtar uzayı değerinin ötesine düşerse ayarlarsınız.
