`readChunkSize()`, `readChunkType()` ve `readChunkCRC()` metotlarının hepsi benzerdir. Her biri, `Chunk` struct'ının ilgili alanına bir `uint32` değeri okur. Ancak `readChunkBytes()` biraz sıra dışı bir yöntemdir. Görüntü verisi değişken uzunlukta olduğundan, `readChunkBytes()` fonksiyonuna bu uzunluğu vermemiz gerekir ki kaç bayt okuyacağını bilsin. Veri uzunluğunun, parçanın SIZE alt alanında tutulduğunu hatırlayın. SIZE değerini belirleyip `readChunkBytes()` fonksiyonuna argüman olarak geçirir ve uygun bir `slice` tanımlarsınız.

Doğru boyuttaki bu `slice` tanımlandıktan sonra bayt verisi struct'ın `Data` alanına okunabilir. Veri okuma kısmı kabaca bu kadar; şimdi devam edip bayt verisi yazmayı inceleyelim.

## Yük/Faydalı Yük (Payload) Yerleştirmek İçin Görsel Bayt Verisi Yazma

Yük/faydalı yük (payload) yerleştirmek için seçebileceğiniz pek çok karmaşık steganografi tekniği bulunmasına karşın, bu bölümde belirli bir bayt ofsetine yazma yöntemine odaklanacağız. PNG dosya formatı, spesifikasyon içinde kritik (critical) ve tamamlayıcı (ancillary) parça (chunk) segmentlerini tanımlar. Kritik parçalar görüntü kod çözücünün (decoder) görüntüyü işleyebilmesi için gereklidir. Tamamlayıcı parçalar ise isteğe bağlıdır ve zaman damgaları, metin gibi kodlama veya kod çözme için kritik olmayan çeşitli meta verileri sağlar.

Dolayısıyla, tamamlayıcı parça türü (ancillary chunk type), mevcut bir parçayı üzerine yazmak veya yeni bir parça eklemek için ideal bir konum sunar. Burada, tamamlayıcı bir parça segmentine yeni bayt `slice`'ları nasıl ekleyeceğinizi göstereceğiz.

### Bir Parça Ofseti Bulma

Öncelikle, tamamlayıcı verinin bir yerinde uygun bir ofset belirlemeniz gerekir. Tamamlayıcı parçaları, her zaman küçük harfle başlamalarından tanıyabilirsiniz. Hex editörü bir kez daha kullanalım ve orijinal PNG dosyasını açıp hex dökümünün sonuna ilerleyelim.

Her geçerli PNG görüntüsünde, dosyanın son parçasını (IEND chunk) gösteren bir `IEND` parça türü (chunk type) bulunur. Son SIZE parçasından önceki 4 bayta ilerlemek, sizi `IEND` parçasının başlangıç ofsetine ve genel PNG dosyasında yer alan (kritik veya tamamlayıcı) parçaların sonuncusuna götürecektir. Tamamlayıcı parçaların isteğe bağlı olduğunu tekrar hatırlayın; bu nedenle, siz bu adımları izlerken incelediğiniz dosyada aynı tamamlayıcı parçalar olmayabilir, hatta hiç olmayabilir. Bizim örneğimizde, `IEND` parçasına ait ofset `0x85258` bayt ofsetinde başlamaktadır (Şekil 13-3).

```
00085110 67 cf e5 60 e2 6c be 79   13 66 b8 81 6d 60 87 If
00085288   25 5b a2 dd 23 56 68 8f 86 c2 b5 ff 47 19 15 8c              11[..09 ...... G...
80085218   Oc Oc ac ec ec ec Oc Oc ec bf 27 72 ee 5b 55 of                          1 1-.[Uo
00085220   Ob 61 eb c6 c9 48 ba fb 34 50 76 f2 b5 be fc ft
80085230   21 d2 4c df cd ce ce ce c0 ce c8 ce ce CO to 8f
00085248   09 73 bb 47 2a dc cc 3e 98 81 81 el dl 82 ff 07                      >
08085258   39 fb bc 9c 92 47 d4 4d 08 08 ee ea 49 45 4e 44              9....G.M....IEND
00085260   ae 42 60 82                                                  .B'.] c
```

**Şekil 13-3:** IEND konumuna göre bir parça ofsetinin belirlenmesi

### ProcessImage() Metodu ile Bayt Yazma

Sıralı baytları bir bayt akışına (byte stream) yazmanın standart yollarından biri bir Go `struct`'ı kullanmaktır. Liste 13-5'te inşa etmeye başladığımız `ProcessImage()` metodunun başka bir bölümüne geri dönelim ve ayrıntıları üzerinden geçelim. Liste 13-8'deki kod, bu bölümde ilerledikçe inşa edeceğiniz bireysel fonksiyonları çağırır.

```go
func (mc *MetaChunk) ProcessImage(b *bytes.Reader, c *models.CmdLineOpts) 0 f
    --snip--
    var in MetaChunk
    m.Chk.Data = Mbyte(c.Payload)
    m.Chk.Type=m.strToInt(c.Type)0
    m.Chk.Size = m.createChunkSize00
    m.Chk.CRC=m.createChunkCRCO0
    bm := m.marshalData00
    bmb := bm.Bytes()
    fmt.Printf("Payload Original: % X\n", []byte(c.Payload))
    fmt.Printf("Payload: % X\n", m.Chk.Data)
    utils.WriteData(b, c, bmb)
1
```

**Liste 13-8:** `ProcessImage()` metodu ile bayt yazma (`/ch-13/imglniect/pnglib/commands.go`)

Bu metod, argüman olarak bir `byte.Reader` ve `models.CmdLineOpts` adlı başka bir struct alır. Liste 13-9'da gösterilen `CmdLineOpts` struct'ı, komut satırı üzerinden geçirilen bayrak (flag) değerlerini içerir. Bu bayrakları, hangi yük/faydalı yükü (payload) kullanacağımızı ve onu görüntü verisinin neresine yerleştireceğimizi belirlemek için kullanacağız. Yazacağınız baytlar, mevcut parça segmentlerinden okunanlarla aynı yapılandırılmış biçimi takip ettiğinden, yeni parça segmenti değerlerinizi kabul edecek yeni bir `MetaChunk` struct örneği oluşturmanız yeterlidir.

Bir sonraki adım, payload'ı bir bayt `slice`'ına okumaktır. Ancak, literal flag değerlerini kullanılabilir bir bayt dizisine dönüştürmek için ek işlevselliğe ihtiyaç duyacaksınız. Şimdi `strToInt()`, `createChunkSize()`, `createChunkCRC()`, `MarshalData()` ve `WriteData()` metotlarının ayrıntılarına girelim.

```go
package models

//CmdLineOpts represents the cli arguments
type CmdLineOpts struct {
    Input    string
    Output string
    Meta     bool
    Suppress bool
    Offset string
    Inject bool
    Payload string
    Type     string
    Encode bool
    Decode bool
    Key     string
```

**Liste 13-9:** `CmdLineOpts` struct'ı (`/ch-13/imglnject/models/opts.go`)

### `strToInt()` Metodu

`strToInt()` metodu ile başlayacağız (Liste 13-10).

```go
func (mc *MetaChunk) strToInt(s string)0 uint32 f
     t := Hbyte(s)
  0 return binary.BigEndian.U1nt32(t)
```

**Liste 13-10:** `strToInt()` metodu (`/ch-13/imgInject/pnglib/commands.go`)

`strToInt()` metodu, argüman olarak bir `string` alan ve `Chunk` struct'ının TYPE değeri için gerekli veri türü olan `uint32` döndüren yardımcı (helper) bir yöntemdir.
