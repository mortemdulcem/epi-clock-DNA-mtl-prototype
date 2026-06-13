### Gunk Dizisi

PNG dosyasının geri kalanı, Şekil 13-2’de gösterildiği gibi, şu deseni izleyen tekrar eden bayt parçalarından (chunk) oluşur: SIZE (4 bayt), TYPE (4 bayt), DATA (herhangi sayıda bayt) ve CRC (4 bayt).

```
00008008   8958 4e47 Eid Oa la Oa       0868666.49484452                 .PNG           IHOR
00000810   06 22. 03 26 66 64 02 58     08 66 88 65 00 9a 76 82                 ...x......v.
00000020   12 00 05 do 2c 49 44 41      54 78 5e cc bd 87 74 53
00000030   57 beef of 3b 93 c0 a4       53 d2 48 48 32 10 42 12          W    •   5 1*12.8.
00000040   08 d5 c6 bd f7 2a 17 b9      48 b6 64 15 cb 92 65 d9          ..... *..H.d...e.
00000058   72 b7 cl 06 4c ef al 97      98 32 40 42 31 ee 15 53
00000068   43 2f ee b6 7a b3 8a 8b      64 f5 66 d9 a6 85 b7 8?          C/..z...d.f .....
00000078   81 dc cc dc f9 af bc fb      bf ef bd 3h 77 66 if 58                      wf.X
00000086   df b5 8? 24 97 73 24 60      9d cf fa ed df de 28 14
```

**Şekil 13-2:** Görüntü verisinin geri kalanı için kullanılan chunk’ların deseni

Hex dökümünü daha ayrıntılı incelediğinizde, ilk chunk’ın — SIZE chunk’ının — `0x00 0x00 0x00 0x0d` baytlarından oluştuğunu görebilirsiniz. Bu chunk, ardından gelecek DATA chunk’ının uzunluğunu tanımlar. Onaltılık ASCII’ye çevrim değeri 13’tür — dolayısıyla bu chunk, DATA chunk’ının 13 bayttan oluşacağını belirtir. TYPE chunk’ının baytları olan `0x49 0x48 0x44 0x52` ise bu durumda ASCII olarak IHDR değerine karşılık gelir. PNG standardı çeşitli geçerli type değerleri tanımlar. Bunlardan bazıları, örneğin IHDR, görüntü metadata’sını tanımlamak veya bir görüntü veri akışının sonunu işaretlemek için kullanılır. Diğer type’lar, özellikle IDAT type’ı, asıl görüntü baytlarını içerir.

Sonraki chunk, uzunluğu SIZE chunk’ı tarafından tanımlanan DATA chunk’ıdır. Son olarak CRC chunk’ı, genel chunk segmentini sonlandırır. Bu, TYPE ve DATA baytlarının birleşiminin CRC-32 sağlama toplamından oluşur. Bu örnekte ilgili CRC chunk’ının baytları `0x9a 0x76 0x82 0x70` değerleridir. Bu format, `IEND` type’ındaki chunk’a ulaşıp Dosya Sonu (EOF) durumuna gelene kadar dosyanın tamamı boyunca tekrar eder.

Liste 13-1’de yer alan `Header` struct’ında yaptığınız gibi, tek bir chunk’ın değerlerini tutacak bir struct inşa edin; bu struct Liste 13-2’de tanımlanmıştır.

```go
//Chunk represents a data byte chunk segment
type Chunk struct {
    Size uint32
    Type uint32
    Data []byte
    CRC uint32
}
```

**Liste 13-2:** `Chunk` struct tanımı (`/ch-13/imgInject/pnglib/commands.go`)

---

### Görüntü Bayt Verisini Okuma

Go dili, kısmen `binary` paketinin (Bölüm 6’dan hatırlıyor olabilirsiniz) sayesinde, ikili (binary) veri okuma ve yazma işlemlerini oldukça kolaylıkla gerçekleştirir. Ancak PNG verisini ayrıştırmadan önce, okumak için bir dosyayı açmanız gerekir. `*os.File` tipinde bir dosya tanıtıcısı alan ve dönüş değeri olarak `*bytes.Reader` tipini veren bir `PreProcessImage()` fonksiyonu yazalım (Liste 13-3).

```go
//PreProcessImage reads to buffer from file handle
func PreProcessImage(dat *os.File) (*bytes.Reader, error) {
    stats, err := dat.Stat()
    if err != nil {
        return nil, err
    }

    var size = stats.Size()
    b := make([]byte, size)

    bufR := bufio.NewReader(dat)
    _, err = bufR.Read(b)
    bReader := bytes.NewReader(b)

    return bReader, err
}
```

**Liste 13-3:** `PreProcessImage()` fonksiyonu tanımı (`/ch-13/imgInject/utilsReader.go`)

Bu fonksiyon, boyut bilgisini alabilmek için bir `FileInfo` yapısı elde etmek amacıyla bir dosya nesnesi açar. Hemen ardından, `bufio.NewReader()` çağrısıyla bir `Reader` örneği ve `bytes.NewReader()` çağrısıyla bir `*bytes.Reader` örneği oluşturmak için kullanılan birkaç satır kod gelir. Fonksiyon, bir `*bytes.Reader` döndürür ve bu sayede `binary` paketini kullanarak bayt verilerini okumaya başlayabilecek duruma gelirsiniz. İlk olarak header verisini, ardından chunk dizisini okuyacaksınız.

---

### Header Verisini Okuma

Bir dosyanın gerçekten PNG dosyası olduğunu doğrulamak için, bir PNG dosyasını tanımlayan ilk 8 baytı kullanarak `validate()` metodunu oluşturun (Liste 13-4).

```go
func (mc *MetaChunk) validate(b *bytes.Reader) {
    var header Header

    if err := binary.Read(b, binary.BigEndian, &header.Header); err != nil {
        log.Fatal(err)
    }

    bArr := make([]byte, 8)
    binary.BigEndian.PutUint64(bArr, header.Header)

    if string(bArr[1:4]) != "PNG" {
        log.Fatal("Provided file is not a valid PNG format")
    } else {
        fmt.Println("Valid PNG so let us continue!")
    }
}
```

**Liste 13-4:** Dosyanın PNG dosyası olduğunu doğrulama (`/ch-13/imgInject/pnglib/commands.go`)

Bu metod ilk bakışta çok karmaşık görünmeyebilir, ama birkaç yeni kavram tanıtır. Bunlardan ilki ve en belirgini, `bytes.Reader` içinden ilk 8 baytı `Header` struct değerine kopyalayan `binary.Read()` fonksiyonudur. `Header` struct alanını `uint64` tipinde (Liste 13-1) tanımladığınızı hatırlayın; bu da 8 bayta eşdeğerdir. Ayrıca `binary` paketinin, sırasıyla `binary.BigEndian` ve `binary.LittleEndian` aracılığıyla En Önemli Bit (Most Significant Bit) ve En Az Önemli Bit (Least Significant Bit) formatlarında okuma yapmaya yönelik metotlar sağladığını da not etmek gerekir. Bu fonksiyonlar, binary yazma işlemleri yaparken de oldukça faydalıdır; örneğin, ağ bayt sıralaması (network byte order) kullanımını belirlemek için baytları hatta (wire) yerleştirirken `BigEndian` seçebilirsiniz.

Binary endianlık fonksiyonu, veri tiplerinin literal veri tiplerine (örneğin `uint64`) dönüştürülmesini (marshaling) kolaylaştıran metotları da içerir. Burada, uzunluğu 8 olan bir bayt dizisi oluşturuyor ve veriyi bir `uint64` veri tipine kopyalamak için gerekli binary okumayı yapıyorsunuz. Ardından baytları string temsillerine dönüştürebilir ve dilimleme (slicing) ile basit bir string karşılaştırması kullanarak 1’den 4’e kadar olan baytların PNG ürettiğini doğrulayabilirsiniz; bu da elinizde geçerli bir görüntü dosya formatı olduğunu gösterir.

Bir dosyanın PNG dosyası olup olmadığını kontrol etme sürecini geliştirmek için, Go’nun `bytes` paketine bakmanızı öneririz; bu paket, daha önce sözünü ettiğimiz PNG sihirli bayt dizisiyle (magic byte sequence) bir dosya header’ını karşılaştırmak için kısayol olarak kullanabileceğiniz yardımcı (convenience) fonksiyonlar içerir. Bunu kendi başınıza keşfetmenizi bırakıyoruz.
