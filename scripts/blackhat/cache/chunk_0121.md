`encodeDecode()` fonksiyonu, argüman olarak yük/faydalı yük (payload) içeren bir byte slice’ı ve gizli anahtar (secret key) değerini alır. Fonksiyonun iç kapsamı (inner scope) içinde `bArr` adında yeni bir byte slice oluşturulur ve giriş byte uzunluğu (payload uzunluğu) değeriyle başlatılır. Sonraki adımda, fonksiyon koşullu bir döngü kullanarak giriş byte dizisinin her indeks pozisyonu üzerinde iterasyon yapar.

İçteki koşullu döngüde, her yinelemede geçerli indeksin ikili (binary) değeri, geçerli indeks değeri ile gizli anahtarın uzunluğunun modülünden türetilen ikili bir değerle XOR’lanır. Bu, payload’dan daha kısa bir anahtar kullanmanıza olanak tanır. Anahtarın sonuna gelindiğinde, modül işlemi sonraki yinelemenin anahtarın ilk byte’ını kullanmasını zorlar. Her XOR işleminin sonucu yeni `bArr` byte slice’ına yazılır ve fonksiyon bu oluşan slice’ı döndürür.

Liste 13-17’deki fonksiyonlar, kodlama (encoding) ve kod çözme (decoding) sürecini kolaylaştırmak için `encodeDecode()` fonksiyonunu sarmalar.

```go
// XorEncode returns encoded byte array
func XorEncode(decode []byte, key string) []byte {
    return encodeDecode(decode, key)
}

// XorDecode returns decoded byte array
func XorDecode(encode []byte, key string) []byte {
    return encodeDecode(encode, key)
}
```

**Liste 13-17** `XorEncode()` ve `XorDecode()` fonksiyonları (`/ch-13/imgInject/utils/encoders.go`)

İki fonksiyon tanımlarsınız: `XorEncode()` ve `XorDecode()`. Bunlar aynı literal argümanları alır ve aynı değerleri döndürür. Bunun sebebi, XOR ile kodlanmış veriyi çözmek için, veriyi kodlarken kullanılan sürecin aynısını kullanmanızdır. Ancak, program kodu içinde daha anlaşılır olması için bu fonksiyonları ayrı ayrı tanımlarsınız.

Bu XOR fonksiyonlarını mevcut programınızda kullanmak için Liste 13-8’de oluşturduğunuz `ProcessImage()` mantığını değiştirmeniz gerekir. Bu güncellemeler, yük/faydalı yükü şifrelemek için `XorEncode()` fonksiyonundan yararlanır. Liste 13-18’de gösterilen değişiklikler, komut satırı argümanlarını kullanarak koşullu encode ve decode mantığına değerler geçirdiğinizi varsayar.

```go
// Encode Block
if (c.Offset != "") && c.Encode {
    var m MetaChunk
    m.Chk.Data = utils.XorEncode([]byte(c.Payload), c.Key)
    m.Chk.Type = chk.strToInt(c.Type)
    m.Chk.Size = chk.createChunkSize()
    m.Chk.CRC = chk.createChunkCRC()
    bin := chk.marshalData()
    bmb := bm.Bytes()
    fmt.Printf("Payload Original: % X\n", []byte(c.Payload))
    fmt.Printf("Payload Encode: % X\n", chk.Data)
    utils.WriteData(b, c, bmb)
}
```

**Liste 13-18** `ProcessImage()` fonksiyonunun XOR kodlamasını içerecek şekilde güncellenmesi (`/ch-13/imgInject/pnglib/commands.go`)

`XorEncode()` fonksiyon çağrısı, yük/faydalı yükü içeren bir byte slice’ı ve gizli anahtarı alır, bu iki değeri XOR’lar ve sonuçta oluşan byte slice’ı döndürür; bu da `chk.Data`’ya atanır. Geri kalan işlevsellik değişmeden kalır ve yeni parça (chunk) segmentini sonrasında bir imaj dosyasına yazılmak üzere serileştirir (marshal).

Programınızı komut satırından çalıştırmanız, Liste 13-19’dakine benzer bir çıktı üretmelidir.

```bash
$ go run main.go images/battlecat.png --inject --offset 0x85258 --encode \
    --key gophers --payload 1234243525522552522452355525 --output encodePNGfile
Valid PNG so let us continue!
0 Payload Original: 31 32 33 34 32 34 33 35 32 35 35 32 32 35 35 32 35 32 32
   34 35 32 33 35 35 35 32 35
0 Payload Encode: 56 5D 43 5C 57 46 40 52 5D 45 5D 57 40 46 52 50 45 5A 57 46
   46 55 5C 45 5D 50 40 46
Success: encodePNGfile created
```

**Liste 13-19** Bir veri parça bloğunu XOR ile kodlamak için `imginject` programının çalıştırılması

Yük/faydalı yük, bir byte gösterimine yazılır ve stdout’a `Payload Original` olarak basılır. Ardından, yük/faydalı yük `gophers` anahtar değeriyle XOR’lanır ve stdout’a `Payload Encode` olarak yazdırılır.

Yük/faydalı yük byte’larını çözmek için, Liste 13-20’deki gibi decode fonksiyonunu kullanırsınız.

```go
// Decode Block
if (c.Offset != "") && c.Decode {
    var m MetaChunk
    offset, _ := strconv.ParseInt(c.Offset, 10, 64)
    b.Seek(offset, 0)
    m.readChunk(b)
    origData := m.Chk.Data
    m.Chk.Data = utils.XorDecode(m.Chk.Data, c.Key)
    m.Chk.CRC = m.createChunkCRC()
    bin := m.marshalData()
    bmb := bm.Bytes()
    fmt.Printf("Payload Original: % X\n", origData)
    fmt.Printf("Payload Decode: % X\n", m.Chk.Data)
    utils.WriteData(b, c, bmb)
}
```

**Liste 13-20** İmaj dosyası ve yük/faydalı yükün kodunun çözülmesi (`/ch-13/imgInject/pnglib/commands.go`)

Bu blok, yük/faydalı yükü içeren parça segmentinin başlangıç konumu (offset) bilgisini gerektirir. Dosya konumunu ayarlamak için bu offset değeriyle `Seek()` çağrısı yaparsınız; ardından, `SIZE`, `TYPE`, `DATA` ve `CRC` değerlerini elde etmek için gerekli olan `readChunk()` çağrısı gelir. `XorDecode()` çağrısı, `chk.Data` yük/faydalı yük değerini ve veriyi kodlamak için kullanılan gizli anahtarın aynısını alır ve çözülmüş yük/faydalı yük değerini tekrar `chk.Data`’ya atar. (Bu simetrik şifreleme olduğundan, veriyi hem şifrelemek hem de şifreyi çözmek için aynı anahtarı kullanırsınız.) Kod bloğu, `Chunk` struct’ınızı bir byte slice’a dönüştüren `marshalData()` fonksiyonunu çağırarak devam eder. Son olarak, çözülen yük/faydalı yükü içeren yeni parça segmentini `WriteData()` fonksiyonunu kullanarak bir dosyaya yazarsınız.

Bu kez decode argümanı ile programınızı komut satırından çalıştırmanız, Liste 13-21’deki sonucu üretmelidir.

```bash
$ go run main.go encodePNGfile -o decodePNGfile --offset 0x85258 --decode \
    --key gophers
Valid PNG so let us continue!
0 Payload Original: 56 5D 43 5C 57 46 40 52 5D 45 5D 57 40 46 52 50 45 5A 57
   46 46 55 5C 45 5D 50 40 46
0 Payload Decode: 31 32 33 34 32 34 33 35 32 35 35 32 32 35 35 32 35 32 32 34
   35 32 33 35 35 35 32 35
Success: decodePNGfile created
```

**Liste 13-21** Bir veri parça bloğunun XOR ile çözülmesi için `imginject` programının çalıştırılması
