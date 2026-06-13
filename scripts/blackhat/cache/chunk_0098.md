Üçüncü taraf `go-luhn` paketinin 0 ve dahili Go deposundan klonladığınız `rc2` paketinin 0 dahil edilmesine dikkat çekmek için burada `import` deyimlerini de ekledik. Ayrıca, ortaya çıkan açık metin bloğunun 8 baytlık sayısal veri olup olmadığını kontrol etmek için kullanacağınız bir düzenli ifade (regular expression) 0 derliyorsunuz.

Kredi kartı numaranızın uzunluğu 16 bayt olmasına rağmen 16 bayt değil, 8 bayt veriyi kontrol ettiğinize dikkat edin. 8 baytı kontrol ediyorsunuz çünkü bu, bir RC2 bloğunun uzunluğu. Şifreli metni blok blok çözeceksiniz; bu yüzden çözdüğünüz ilk bloğun sayısal olup olmadığını kontrol edebilirsiniz. Eğer bloğun 8 baytı da sayısal değilse, bunun bir kredi kartı numarasıyla ilgili olmadığı sonucuna güvenle varabilir ve ikinci şifreli metin bloğunun çözülmesini tamamen atlayabilirsiniz. Bu küçük performans iyileştirmesi, milyonlarca kez çalıştırıldığında geçen süreyi önemli ölçüde azaltacaktır.

254   Bölüm 11

Son olarak, `CryptoData` 0 adında bir tür (type) tanımlıyorsunuz; bu türü, anahtarınızı (key) ve bir `cipher.Block` değerini saklamak için kullanacaksınız. Üreticilerin oluşturacağı ve tüketicilerin üzerinde işlem yapacağı iş birimlerini tanımlamak için bu `struct` yapısını kullanacaksınız.

## İş Üretmek

Üretici fonksiyonuna bakalım (Liste 11-9). Bu fonksiyonu, önceki kod listesindeki tür tanımlarınızın hemen sonrasına yerleştiriyorsunuz.

```go
func generate(start, stop uint64, out chan<- *CryptoData,
done <-chan struct{}, wg *sync.WaitGroup) {
    wg.Add(1)
    go func() {
        defer wg.Done()
        var (
            block cipher.Block
            err   error
            key   []byte
            data  *CryptoData
        )

        for i := start; i <= stop; i++ {
            key = make([]byte, 8)
            select {
            case <-done:
                return
            default:
                binary.BigEndian.PutUint64(key, i)
                if block, err = rc2.New(key[3:], 40); err != nil {
                    log.Fatalln(err)
                }
                data = &CryptoData{
                    block: block,
                    key:   key[3:],
                }
                out <- data
            }
        }
    }()
    return
}
```

Liste 11-9: RC2 üretici fonksiyonu (`ch-11/rc2-brute/main.go`)

Üretici fonksiyonunuzun adı `generate()` 0. Bu fonksiyon, üreticinin üzerinde iş oluşturacağı anahtar uzayının bir bölümünü tanımlamak için kullanılan iki `uint64` değişken kabul eder (temelde, anahtarları üretecekleri aralık). Bu sayede anahtar uzayını bölümlere ayırabilir ve her üreticiye bunun bir kısmını dağıtabilirsiniz.

Fonksiyon ayrıca iki kanal (channel) kabul eder: tüketicilere iş göndermek (push) için kullanılan, yalnızca yazma amaçlı bir `*CryptoData` kanalı ve tüketicilerden sinyal almak için kullanılacak genel bir `struct` kanalı. İkinci kanal,
