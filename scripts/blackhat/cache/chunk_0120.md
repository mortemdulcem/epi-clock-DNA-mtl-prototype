`WriteData()` fonksiyonu, orijinal görüntü dosyasının bayt verilerini içeren bir `bytes.Reader` 0, komut satırı argüman değerlerini kapsayan bir `models.CmdLineOpts` 0 struct’ı ve yeni parça (chunk) bayt segmentini tutan bir `byte` slice’ı `S` tüketir. Kod bloğu, `models.CmdLineOpts` struct’ındaki ofset değerini elde etmek için bir string’ten `int64`’e dönüştürme 0 ile başlar; bu, yeni parça segmentinizi diğer parçaları bozmadan belirli bir konuma yazmanıza yardımcı olacaktır. Ardından, yeni değiştirilmiş PNG görüntüsünün diske yazılabilmesi için bir dosya tanıtıcısı (file handle) 0 oluşturursunuz.

`r.Seek(0, 0)` fonksiyon çağrısını kullanarak `bytes.Reader`’ın mutlak başlangıcına geri sararsınız. İlk 8 baytın PNG başlığı için ayrıldığını hatırlayın; bu nedenle yeni çıktı PNG görüntüsünün de bu başlık baytlarını içermesi önemlidir. Bu başlık baytlarını, uzunluğu ofset değerine göre belirlenen bir `byte` slice oluşturarak dahil edersiniz 0. Sonra, orijinal görüntüden bu sayıda bayt okur ve aynı baytları yeni görüntü dosyanıza yazarsınız 0. Artık hem orijinal hem de yeni görüntüde aynı başlıklar mevcuttur.

Sonrasında yeni parça segmenti baytlarını 0 yeni görüntü dosyasına yazarsınız. Son olarak, `bytes.Reader`’daki kalan baytları 0 (yani, orijinal görüntünüzdeki parça segmenti baytlarını) yeni görüntü dosyasına eklersiniz. `bytes.Reader`’ın, daha önce `byte` slice’a okuma işlemi yapıldığından, ofset konumuna kadar ilerlemiş olduğunu hatırlayın; bu slice, ofsetten EOF’a (dosya sonuna) kadar olan baytları içerir. Sonuçta yeni bir görüntü dosyanız olur. Bu yeni dosya, orijinal görüntüyle aynı öndeki ve sondaki parçalara sahiptir; ancak ayrıca yükünüzü (payload) yeni bir ikincil parça (ancillary chunk) olarak enjekte eder.

Şimdiye kadar inşa ettiklerinize çalışan bir temsil üzerinden bakmanıza yardımcı olmak için, genel çalışan proje koduna `https://github.com/blackhat-go/bhg/tree/master/ch-13/imginject/` adresinden bakın. `imgInject` programı, orijinal PNG görüntü dosyası, bir ofset konumu, rastgele bir veri yükü (payload), kendi belirlediğiniz rastgele parça tipi ve değiştirilmiş PNG görüntü dosyanız için çıktı dosya adı değerlerini içeren komut satırı argümanlarını tüketir; bu, Liste 13-15’te gösterilmiştir.

```bash
$ go run main.go     images/battlecat.png -o newPNGfile --inject -offset \
    0x85258 --payload 1234243525522552522452355525
```

Liste 13-15: `imgInject` komut satırı programının çalıştırılması

Eğer her şey planlandığı gibi gittiyse, ofset `0x85258` artık Şekil 13-4’te gösterildiği gibi yeni bir `rNDm` parça segmenti içermelidir.

```
00085220   Ob 61 eb c6 c9 48 be fb     34 50 76 f2 b5 Oe fc ff         .a...11..4Pv
00085230   21 d2 4c df cd c0 c8 ce     c0 c0 c0 c0 c8 c0 fel 8f
08085240   09 73 bb 47 2a Sc cc 3e     90 81 81 el df 82 ff 07
08085250   39 fb bc 9c 92 47 d4 4d     00 BO 00 lc 72 4e 44 64
00085260   31 32 33 34 32 34 33 35     32 35 35 32 32 35 35 32         1234243525522552
00085278   35 32 32 34 35 32 33 35     35 35 32 35 if de 22 4c         522452355525..1_
00085280   00 00 00 08 49 45 4e 44     ae 42 60 82                     ....IEN0.8'.1
```

Şekil 13-4: İkincil bir parça (örneğin `rNDm`) olarak enjekte edilen bir yük (payload)

Tebrikler—ilk steganografi programınızı yazdınız!

## XOR Kullanarak Görüntü Bayt Verilerini Kodlama ve Çözme

Nasıl ki çok sayıda steganografi türü varsa, aynı şekilde ikili (binary) bir dosya içinde veriyi örtmek (obfuscate) için kullanılan pek çok teknik de vardır. Önceki bölümdeki örnek programı geliştirmeye devam edelim. Bu sefer, yükünüzün gerçek amacını gizlemek için obfuscation ekleyeceksiniz.

Obfuscation, yükünüzü ağ izleme cihazlarından ve uç nokta güvenlik çözümlerinden gizlemeye yardımcı olabilir. Örneğin, yeni bir Meterpreter shell veya Cobalt Strike beacon başlatmak için kullanılan ham shellcode gömüyorsanız, bunun tespitten kaçtığından emin olmak istersiniz. Bunun için veriyi şifrelemek ve şifresini çözmek amacıyla Exclusive OR (XOR) bit düzeyinde (bitwise) işlemler kullanacaksınız.

Exclusive OR (XOR), iki ikili değer arasında yapılan ve yalnızca iki değer aynı değilse Boolean `true` değeri üreten, aksi takdirde Boolean `false` üreten koşullu bir karşılaştırmadır. Başka bir deyişle, ifade ancak ve ancak `x` veya `y`’den biri doğruysa doğrudur; fakat her ikisi birden doğruysa değildir. `x` ve `y`’nin her ikisinin de ikili giriş değerleri olduğu göz önünde bulundurulduğunda, bunu Tablo 13-1’de gösterildiği gibi görebilirsiniz.

Tablo 13-1: XOR Doğruluk Tablosu

| X | Y | Çıktı         |
|---|---|---------------|
| 0 | 1 | True veya 1   |
| 1 | 0 | True veya 1   |
| 0 | 0 | False veya 0  |
| 1 | 1 | False veya 0  |

Bu mantığı, verideki bitleri gizlemek (obfuscate) için, verideki bitleri gizli bir anahtarın bitleriyle karşılaştırarak kullanabilirsiniz. İki değer eşleştiğinde, yükteki biti 0’a değiştirirsiniz; farklı olduklarında ise 1’e değiştirirsiniz. Önceki bölümde oluşturduğunuz kodu genişleterek bir `encodeDecode()` fonksiyonu ile `XorEncode()` ve `XorDecode()` fonksiyonlarını ekleyelim. Bu fonksiyonları `utils` package’ına yerleştireceğiz (Liste 13-16).

```go
func encodeDecode(input []byte0, key stringe) []byte {
    var bArr = make([]byte, len(input))
    for i := 0; i < len(input);     {
     0 bArr[i] += input[i]    key[i%len(key)]

    return bArr
```

Liste 13-16: `encodeDecode()` fonksiyonu (`/ch-13/imgInject/utils/encoders.go`)
