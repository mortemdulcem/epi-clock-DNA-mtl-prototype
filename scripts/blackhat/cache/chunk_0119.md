### `createChunkSize()` Metodu

Sonraki adımda `createChunkSize()` metodunu kullanarak `Chunk` struct'ının `SIZE` değerini atarsınız (Liste 13-11).

```go
func (mc *MetaChunk) createChunkSize() uint32 {
        return uint32(len(mc.Chk.Data))
}
```

**Liste 13-11:** `createChunkSize()` metodu (`/ch-13/imgInject/pnglib/commands.go`)

Bu metot `chk.DATA` byte dizisinin uzunluğunu alır ve bunu `uint32` değerine tip dönüştürmesiyle elde eder.

### `createChunkCRC()` Metodu

Her bir chunk segmentinin CRC özeti (checksum) değerinin hem `TYPE` hem de `DATA` baytlarını içerdiğini hatırlayın. Bu özeti hesaplamak için `createChunkCRC()` metodunu kullanacaksınız. Metot, Go'nun `hash/crc32` paketinden faydalanır (Liste 13-12).

```go
func (mc *MetaChunk) createChunkCRC() uint32 {
    bytesMSB := new(bytes.Buffer)
    if err := binary.Write(bytesMSB, binary.BigEndian, mc.Chk.Type); err != nil {
        log.Fatal(err)
    }

    if err := binary.Write(bytesMSB, binary.BigEndian, mc.Chk.Data); err != nil {
        log.Fatal(err)
    }

    return crc32.ChecksumIEEE(bytesMSB.Bytes())
}
```

**Liste 13-12:** `createChunkCRC()` metodu (`/ch-13/imgInject/pnglib/commands.go`)

`return` ifadesine gelmeden önce bir `bytes.Buffer` tanımlayıp hem `TYPE` hem de `DATA` baytlarını bu buffer'a yazarsınız. Buffer'dan elde edilen byte dilimi (`[]byte`), argüman olarak `ChecksumIEEE` fonksiyonuna geçirilir ve CRC-32 özet değeri `uint32` veri tipi olarak döndürülür. Asıl işi yapan kısım `return` ifadesidir; gerekli baytlar üzerinde özet hesabını burada gerçekleştirir.

### `marshalData()` Metodu

Bir chunk'ın gerekli tüm parçaları ilgili struct alanlarına atanmıştır; artık bunlar bir `bytes.Buffer` içerisine marshal edilebilir. Bu buffer, yeni görüntü dosyasına eklenecek özel chunk'ın ham baytlarını sağlayacaktır. Liste 13-13, `marshalData()` metodunun nasıl göründüğünü gösteriyor.

```go
func (mc *MetaChunk) marshalData() *bytes.Buffer {
    bytesMSB := new(bytes.Buffer)
    if err := binary.Write(bytesMSB, binary.BigEndian, mc.Chk.Size); err != nil {
        log.Fatal(err)
    }

    if err := binary.Write(bytesMSB, binary.BigEndian, mc.Chk.Type); err != nil {
        log.Fatal(err)
    }

    if err := binary.Write(bytesMSB, binary.BigEndian, mc.Chk.Data); err != nil {
        log.Fatal(err)
    }

    if err := binary.Write(bytesMSB, binary.BigEndian, mc.Chk.CRC); err != nil {
        log.Fatal(err)
    }

    return bytesMSB
}
```

**Liste 13-13:** `marshalData()` metodu (`/ch-13/imgInject/pnglib/commands.go`)

`marshalData()` metodu bir `bytes.Buffer` tanımlar ve chunk bilgilerini — boyut (`size`), tür (`type`), veri (`data`) ve özet (`checksum`) — bu buffer'a yazar. Metot, tüm chunk segment verilerini tek bir birleşik `bytes.Buffer` içinde döndürür.

### `WriteData()` Fonksiyonu

Artık geriye kalan tek şey, yeni chunk segment baytlarını orijinal PNG görüntü dosyasının ilgili offset (ofset) konumuna yazmaktır. Kendi oluşturduğumuz `utils` adlı pakette yer alan `WriteData()` fonksiyonuna göz atalım (Liste 13-14).

```go
// WriteData writes new Chunk data to offset
func WriteData(r *bytes.Reader, c *models.CmdLineOpts, b []byte) {
    offset, _ := strconv.ParseInt(c.Offset, 10, 64)
    w, err := os.Create(c.Output)
    if err != nil {
        log.Fatal("Fatal: Problem writing to the output file!")
    }

    defer w.Close()
    r.Seek(0, 0)

    var buff = make([]byte, offset)
    r.Read(buff)
    w.Write(buff)
    w.Write(b)

    _, err = io.Copy(w, r)
    if err == nil {
        fmt.Printf("Success: %s created\n", c.Output)
    }
}
```

**Liste 13-14:** `WriteData()` fonksiyonu (`/ch-13/imginject/utils/writer.go`)
