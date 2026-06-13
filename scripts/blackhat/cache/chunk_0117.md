### Chunk Dizisini Okuma

Dosyanızın bir PNG resmi olduğunu doğruladıktan sonra, chunk dizisini (chunk sequence) okuyan kodu yazabilirsiniz. Bir PNG dosyasında başlık (header) yalnızca bir kez bulunur; buna karşılık chunk dizisi, dosya sonuna (EOF) ulaşılana kadar `SIZE`, `TYPE`, `DATA` ve `CRC` chunk’larını tekrarlar. Dolayısıyla bu tekrarları karşılayabilmeniz gerekir; bunu da en elverişli şekilde bir Go koşullu döngüsüyle yapabilirsiniz. Bunu göz önünde bulundurarak, dosya sonuna kadar tüm veri chunk’larını yinelemeli (iterative) olarak işleyen bir `ProcessImage()` metodu yazalım (Liste 13-5).

```go
func (mc *MetaChunk) ProcessImage(b *bytes.Reader, c *models.CmdLineOpts) {
    // Snip code for brevity (Only displaying relevant lines from code block)
    count := 1 // Start at 1 because 0 is reserved for magic byte
    chunkType := 
    endChunkType := "TEND" // The last TYPE prior to EOF
    for chunkType != endChunkType {
        fmt.Println("---- Chunk # " + strconv.Itoa(count) + " ----")
        offset := chk.getOffset(b)
        fmt.Printf("Chunk Offset: %#02x\n", offset)
        chk.readChunk(b)
        chunkType = chk.chunkTypeToString()
        count++
    }
}
```

**Liste 13-5:** `ProcessImage()` metodu (`/ch-13/imgInject/pnglib/commands.go`)

İlk olarak, `ProcessImage()` metoduna argüman olarak bir `bytes.Reader` bellek adresi işaretçisinin (`*bytes.Reader`) referansını geçiriyorsunuz. Az önce oluşturduğunuz `validate()` metodu (Liste 13-4) da yine bir `bytes.Reader` işaretçisi referansı alıyordu. Konvansiyon gereği, aynı bellek adresi işaretçi konumuna yapılan birden fazla referans, doğası gereği referans verilen veriye değiştirilebilir (mutable) erişim sağlar. Bu, `bytes.Reader` referansını `ProcessImage()` metoduna argüman olarak geçirdiğinizde, aynı `bytes.Reader` örneğine eriştiğiniz için, başlık (Header) boyutu nedeniyle okuyucunun (reader) 8 bayt ilerlemiş olduğu anlamına gelir.

Buna alternatif olarak, bir işaretçi (pointer) geçirmemiş olsaydınız, `bytes.Reader` ya aynı PNG görüntü verisinin bir kopyası ya da tamamen ayrı, benzersiz örnek veri olurdu. Çünkü başlığı okurken işaretçiyi ileri taşımak, dosyanın başka yerlerinde okuyucuyu uygun şekilde ilerletmemiş olurdu. Bu yaklaşımdan kaçınmak istersiniz. Öncelikle, gereksiz yere birden fazla veri kopyası taşımak kötü bir konvansiyondur. Daha da önemlisi, her kopya geçirdiğinizde, bu kopya dosyanın başlangıcına konumlanmış olur ve bir chunk dizisini okumadan önce dosya içindeki konumunu programatik olarak tanımlayıp yönetmek zorunda kalırsınız.

Kod bloğu içerisinde ilerledikçe, görüntü dosyasının kaç adet chunk segmenti içerdiğini takip etmek için bir `count` değişkeni tanımlıyorsunuz. `chunkType` ve `endChunkType` ise karşılaştırma mantığının bir parçası olarak kullanılır; burada, mevcut `chunkType` değeri, EOF koşulunu ifade eden `endChunkType`'ın `TEND` değerine karşı değerlendirilir.

Her bir chunk segmentinin nerede başladığını, daha doğrusu her chunk’ın dosya bayt yapısı içindeki mutlak konumunu bilmek faydalı olacaktır; bu değere `offset` adı verilir. `offset` değerini bilirseniz, dosyanın içine bir yük/faydalı yük (payload) yerleştirmeniz çok daha kolay olur. Örneğin, bir decoder’a (çözücü) bir `offset` konumları koleksiyonu verebilir; bu decoder, her bilinen `offset`teki baytları toplayan ayrı bir fonksiyon olur ve ardından bu baytları çözerek hedeflediğiniz yükü/faydalı yükü geri açar. Her bir chunk’ın `offset` değerini elde etmek için `mc.getOffset(b)` metodunu çağıracaksınız (Liste 13-6).

```go
func (mc *MetaChunk) getOffset(b *bytes.Reader) {
    offset, _ := b.Seek(0, 1)
    mc.Offset = offset
}
```

**Liste 13-6:** `getOffset()` metodu (`/ch-13/imgInject/pnglib/commands.go`)

`bytes.Reader`, geçerli konumu türetmeyi oldukça basit hale getiren bir `Seek()` metodu içerir. `Seek()` metodu, geçerli okuma veya yazma `offset`ini hareket ettirir ve ardından dosya başlangıcına göre yeni `offset`i döndürür.

İlk argümanı, `offset`i kaç bayt hareket ettirmek istediğinizi; ikinci argümanı ise bu hareketin hangi pozisyondan itibaren yapılacağını tanımlar. İkinci argümanın olası değerleri 0 (Dosya Başlangıcı – Start of File), 1 (Geçerli Konum – Current Position) ve 2 (Dosya Sonu – End of File) olarak tanımlanır. Örneğin, geçerli konumunuzdan 8 bayt sola kaymak isteseydiniz, `b.Seek(-8, 1)` kullanırdınız.

Burada `b.Seek(0, 1)` ifadesi, `offset`i geçerli konumdan 0 bayt hareket ettirmek istediğinizi belirtir, dolayısıyla sadece o anki `offset`i döndürür; pratikte `offset`i hareket ettirmeden, mevcut `offset`i geri alır.

Sırada anlattığımız metotlar, gerçek chunk segment baytlarının nasıl okunacağını tanımlar. Okunabilirliği biraz artırmak için bir `readChunk()` metodu oluşturalım ve her bir chunk alt alanını okumak için ayrı metotlar tanımlayalım (Liste 13-7).

```go
func (mc *MetaChunk) readChunk(b *bytes.Reader) {
    mc.readChunkSize(b)
    mc.readChunkType(b)
    mc.readChunkBytes(b, mc.Chk.Size)
    mc.readChunkCRC(b)
}

func (mc *MetaChunk) readChunkSize(b *bytes.Reader) {
    if err := binary.Read(b, binary.BigEndian, &mc.Chk.Size); err != nil {
        log.Fatal(err)
    }
}

func (mc *MetaChunk) readChunkType(b *bytes.Reader) {
    if err := binary.Read(b, binary.BigEndian, &mc.Chk.Type); err != nil {
        log.Fatal(err)
    }
}

func (mc *MetaChunk) readChunkBytes(b *bytes.Reader, cLen uint32) {
    mc.Chk.Data = make([]byte, cLen)
    if err := binary.Read(b, binary.BigEndian, &mc.Chk.Data); err != nil {
        log.Fatal(err)
    }
}

func (mc *MetaChunk) readChunkCRC(b *bytes.Reader) {
    if err := binary.Read(b, binary.BigEndian, &mc.Chk.CRC); err != nil {
        log.Fatal(err)
    }
}
```

**Liste 13-7:** Chunk okuma metotları (`/ch-13/imgInject/pnglib/commands.go`)
