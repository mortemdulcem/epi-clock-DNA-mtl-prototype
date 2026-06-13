Implementing and Attacking Cryptography   255

tüketicinin doğru anahtarı belirlediğinde üreticiye açıkça durmasını
bildirebilmesi için gereklidir. Problemi çoktan çözmüşsen, daha fazla iş
yükü oluşturmanın anlamı yoktur. Son olarak, fonksiyonun üretici
çalıştırılmasını izlemek ve eşzamanlamak için kullanılan bir `WaitGroup`
kabul eder. Her eşzamanlı üretici çalıştığında, yeni bir üretici başlattığını
`WaitGroup`’a söylemek için `wg.Add(1)` çalıştırırsın.

İş kanalını bir goroutine içinde doldurursun 0 ve goroutine çıkarken
`WaitGroup`’ını bilgilendirmek için `defer wg.Done()` 0 çağrısını da
eklersin. Bu, `main()` fonksiyonundan yürütmeye devam etmeye çalışırken
oluşabilecek kilitlenmeleri (deadlock) önleyecektir. `start()` ve `stop()`
değerlerini kullanarak, bir `for` döngüsü 0 ile anahtar uzayının bir alt
bölümünü dolaşırsın. Döngünün her yinelemesi, bitiş ofsetine ulaşana kadar
`i` değişkenini artırır.

Daha önce belirttiğimiz gibi, anahtar uzayın 40 bit, ama `i` değişkeninin
64 bit. Bu boyut farkını anlamak kritik önemdedir. Go’da doğal olarak 40 bitlik
bir tür yoktur; yalnızca 32 veya 64 bitlik türler vardır. 32 bit, 40 bitlik bir
değeri tutmak için çok küçük olduğundan, bunun yerine 64 bitlik türü
kullanman gerekir ve aradaki fazladan 24 biti daha sonra hesaba katarsın.
Belki de `uint64` yerine bir `[]byte` kullanarak tüm anahtar uzayı üzerinde
iterate ederek bu zorluğun tamamından kaçınabilirsin. Ancak bunu yapmak,
muhtemelen örneği gereğinden fazla karmaşıklaştıracak tuhaf bit düzeyinde
(bitwise) işlemler gerektirecektir. Bu yüzden, uzunlukla ilgili inceliği
(boyutsal nüansı) ele almayı tercih ediyorsun.

Döngünün içinde, ilk bakışta tuhaf görünen, çünkü kanal verisi üzerinde
çalışan ve tipik sözdizimine (syntax) uymayan bir `select` deyimi 0
kullanırsın. Bunu, `done` kanalının `case <- done` 0 ile kapatılıp
kapatılmadığını kontrol etmek için kullanırsın. Kanal kapatılmışsa,
goroutine’den çıkmak için bir `return` ifadesi çalıştırırsın. `done` kanalı
kapatılmadığında, `default` durumunu 0 kullanarak işi tanımlamak için
gerekli kripto örneklerini oluşturursun. Özellikle, geçerli anahtar olan
`uint64` değerini `key` adında 8 baytlık bir dilime yazmak için
`binary.BigEndian.PutUint64(key,` 0 çağrısını yaparsın.

Bunu daha önce açıkça belirtmemiş olsak da, `key`’i 8 baytlık bir slice
olarak ilklendirmiştin. Peki, sadece 5 baytlık bir anahtarla uğraşırken neden
slice’ı 8 bayt olarak tanımlıyorsun? Çünkü `binary.BigEndian.PutUint64`
bir `uint64` değeri aldığı için, uzunluğu 8 bayt olan bir hedef slice’a
ihtiyaç duyar; aksi takdirde `index-out-of-range` hatası verir. 8 baytlık bir
değeri 5 baytlık bir slice’a sığdıramaz. Bu yüzden ona 8 baytlık bir slice
verirsin. Kalan kod boyunca, `key` slice’ının yalnızca son 5 baytını
kullandığına dikkat et; ilk 3 bayt sıfır olsa bile, dahil edilseler kripto
fonksiyonlarının bütünlüğünü bozacaklardır. İşte bu yüzden, şifreni ilk
oluştururken `rc2.New(key[3:], 40)` çağrısını yaparsın; böylece alakasız 3
baytı atarsın ve aynı zamanda anahtarının uzunluğunu bit cinsinden (40)
geçersin. Ortaya çıkan `cipher.Block` örneğini ve ilgili anahtar baytlarını
kullanarak bir `CryptoData` nesnesi oluşturur ve bunu dıştaki işçi (worker)
kanalı `G`’ye yazarsın.

Üretici kodu için bu kadar. Bu bölümde yalnızca gerekli anahtar verisini
hazırladığını unutma. Fonksiyonun hiçbir yerinde şifreli metni (ciphertext)
gerçekten çözmeye çalışmıyorsun. Bu işi tüketici fonksiyonunda yapacaksın.

256   Chapter 11

## İş Yapmak ve Veriyi Şifre Çözmek

Şimdi tüketici fonksiyonunu inceleyelim (Liste 11-10). Bu fonksiyonu, önceki
kodunla aynı dosyaya ekleyeceksin.

```go
func decrypt(ciphertext []byte, in <- chan *CryptoData, \
done chan structa, wg *sync.WaitGroup) {
    size := rc2.BlockSize
    plaintext := make([]byte, len(ciphertext))
    wg.Add(i)
    go func() {
        defer wg.Done()
        for data := range in {
            select {
            case <- done:
                return
            default:
                data.block.Decrypt(plaintext[:size], ciphertext[:size])
                if numeric.Match(plaintext[:size]) {
                    data.block.Decrypt(plaintext[size:], ciphertext[size:])
                    if luhn.Valid(string(plaintext)) && \
                    numeric.Match(plaintext[size:]) {
                        fmt.Printf("Card [%s] found using key [%x]\n", /
                        plaintext, data.key)
                        close(done)
                        return
```

Liste 11-10: RC2 tüketici fonksiyonu (`/ch-11/rc2-brute/main.go`)

Tüketici fonksiyonun, `decrypt()` 0, birkaç parametre kabul eder. Çözmek
istediğin şifreli metni (`ciphertext`) alır. Ayrıca iki ayrı kanal kabul
eder: iş kuyruğu olarak kullanacağın, salt okunur bir `*CryptoData` kanalı
olan `in` ve açık iptal (cancellation) sinyalleri göndermek ve almak için
kullanacağın `done` adlı bir kanal. Son olarak, tüketici işçilerini (workers)
yönetmek için kullanacağın, `wg` adlı bir `*sync.WaitGroup` de kabul eder;
tıpkı üretici uygulamanda yaptığın gibi. Yeni bir işçi başlattığını
`WaitGroup`’a bildirmek için `wg.Add(2)` çağrısını yaparsın 0. Bu sayede
çalışan tüm tüketicileri takip edebilir ve yönetebilirsin.

Sonra, goroutine içinde `defer wg.Done()` 0 çağrısını yaparsın; böylece
goroutine fonksiyonu bittiğinde, `WaitGroup` durumunu güncelleyip çalışan
işçi sayısını bir azaltırsın. Bu `WaitGroup` işleri, programının yürütmesini
rastgele sayıda işçi arasında eşzamanlamak için gereklidir. `main()`
fonksiyonunda daha sonra goroutine’lerinin tamamlanmasını beklemek için
`WaitGroup`’u kullanacaksın.
