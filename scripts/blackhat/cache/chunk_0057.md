```go
func parseTags(sf reflect.StructField) (*TagMap, error) {
    ret := &TagMap{
        m:   make(map[string]interface{}),
        has: make(map[string]bool),
    }
    tag := sf.Tag.Get("smb")
    smbTags := strings.Split(tag, ",")
    for _, smbTag := range smbTags {
        tokens := strings.Split(smbTag, ":")
        switch tokens[0] {
        case "len", "offset", "count":
            if len(tokens) != 2 {
                return nil, errors.New("Missing required tag data. Expecting key:val")
            }
            ret.Set(tokens[0], tokens[1])
        case "fixed":
            if len(tokens) != 2 {
                return nil, errors.New("Missing required tag data. Expecting key:val")
            }
            i, err := strconv.Atoi(tokens[1])
            if err != nil {
                return nil, err
            }
            ret.Set(tokens[0], i)
        }
    }
    return ret, nil
}
```

Liste 6-7: Yapı etiketlerini ayrıştırma (`/ch-6/smb/smb/encoder/encoder.go`)

Fonksiyon, Go'nun `reflect` paketinde tanımlı bir tip olan `reflect.StructField` tipinde `sf` adlı bir parametre kabul eder. Kod, ilgili alanda tanımlanmış `smb` etiketlerini almak için `StructField` değişkeni üzerinde `sf.Tag.Get("smb")` çağrısı yapar. Yine, bu programımız için bizim seçtiğimiz rastgele bir isimdir. Yapmamız gereken tek şey, etiketleri ayrıştıran kodun, `struct` tip tanımımızda kullandığımız anahtarla aynı anahtarı kullanmasını sağlamaktır.

Daha sonra, ileride tek bir `struct` alanında birden fazla `smb` etiketi tanımlamamız gerekmesi ihtimaline karşı, `smb` etiketlerini virgül ile böler ve her etiketi döngüyle gezeriz. Her etiketi iki nokta üst üste (`:`) karakterine göre böleriz; etiketlerimiz için `fixed:16` ve `len:SecurityBlob` gibi `ad:değer (name:value)` formatını kullandığımızı hatırlayın. Tekil etiket verisi temel anahtar-değer ikilisine ayrıldıktan sonra, anahtar üzerinde bir `switch` deyimi kullanarak anahtara özgü doğrulama mantığı uygularız; örneğin, `fixed` etiket değerleri için değerleri tam sayıya dönüştürmek gibi.

Son olarak, fonksiyon veriyi `ret` adlı özel haritamıza (`map`) yazar.

## parseTags() Fonksiyonunu Çağırma ve reflect.StructField Nesnesi Oluşturma

Peki fonksiyonu nasıl çağırırız ve `reflect.StructField` tipinde bir nesneyi nasıl oluştururuz? Bu soruları cevaplamak için, `parseTags` yardımcı (`convenience`) fonksiyonumuzla aynı kaynak dosyada bulunan `unmarshal()` fonksiyonuna bakın; bkz. Liste 6-8. `unmarshal()` fonksiyonu oldukça kapsamlıdır, bu yüzden sadece en ilgili kısımlarını parça parça ele alacağız.

```go
func unmarshal(buf []byte, v interface{}, meta *Metadata) (interface{}, error) {
    typev := reflect.TypeOf(v)
    valuev := reflect.ValueOf(v)
    // --snip--
    r := bytes.NewBuffer(buf)
    switch typev.Kind() {
    case reflect.Struct:
        // --snip--
    case reflect.Uint8:
        // --snip--
    case reflect.Uint16:
        // --snip--
    case reflect.Uint32:
        // --snip--
    case reflect.Uint64:
        // --snip--
    case reflect.Slice, reflect.Array:
        // --snip--
    default:
        return errors.New("Unmarshal not implemented for kind:" + typev.Kind().String()), nil
    }
    return nil, nil
}
```

Liste 6-8: Bilinmeyen tipleri dinamik olarak `unmarshal` etmek için reflection kullanma (`/ch-6/smb/smb/encoder/encoder.go`)

`unmarshal()` fonksiyonu, veri arabelleğinin (`buffer`) `unmarshal` edileceği hedef `interface`'in tipini ve değerini almak için Go'nun `reflect` paketini kullanır. Bu gereklidir, çünkü rastgele bir `byte slice`'ı bir `struct`'a dönüştürmek için, `struct` içinde kaç alan olduğunu ve her alan için kaç bayt okunacağını bilmemiz gerekir. Örneğin, `uint16` olarak tanımlanmış bir alan 2 bayt tüketirken, `uint64` 8 bayt tüketir. Reflection kullanarak, hedef `interface`'i sorgulayabilir, hangi veri tipi olduğunu ve veri okuma işlemini nasıl ele alacağımızı belirleyebiliriz. Her tip için mantık farklı olacağından, `typev.Kind()` çağrısı yaparak tip üzerinde bir `switch` uygularız; bu çağrı, üzerinde çalıştığımız veri tipinin türünü belirten bir `reflect.Kind` örneği döndürür. İzin verilen her veri tipi için ayrı bir `case` bloğumuz olduğunu göreceksiniz.

### Struct'ları İşleme

Muhtemel ilk giriş noktası olduğu için, bir `struct` tipini ele alan `case` bloğuna bakalım; bkz. Liste 6-9.

```go
case reflect.Struct:
    m := &Metadata{
        Tags:       &TagMap{},
        Lens:       make(map[string]uint64),
        Parent:     v,
        ParentBuf:  buf,
        Offsets:    make(map[string]uint64),
        CurrOffset: 0,
    }

    for i := 0; i < typev.NumField(); i++ {
        m.CurrField = typev.Field(i).Name
        tags, err := parseTags(typev.Field(i))
        if err != nil {
            return nil, err
        }
        m.Tags = tags
        var data interface{}
        switch typev.Field(i).Type.Kind() {
        case reflect.Struct:
            data, err = unmarshal(buf[m.CurrOffset:], valuev.Field(i).Addr().Interface(), m)
        default:
            data, err = unmarshal(buf[m.CurrOffset:], valuev.Field(i).Interface(), m)
        }
        if err != nil {
            return nil, err
        }
        valuev.Field(i).Set(reflect.ValueOf(data))
    }

    v = reflect.Indirect(reflect.ValueOf(v)).Interface()
    meta.CurrOffset += m.CurrOffset
    return v, nil
```

Liste 6-9: Bir `struct` tipini `unmarshal` etme (`/ch-6/smb/smb/encoder/encoder.go`)
