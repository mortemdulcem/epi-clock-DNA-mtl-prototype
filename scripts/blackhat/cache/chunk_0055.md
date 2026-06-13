`BinaryMarshallable` arayüzü, uygulanması gereken iki metot tanımlar: `MarshalBinary()` ve `UnmarshalBinary()`. Fonksiyonlara geçirilen `Metadata` tipini dert etmeyin; temel işlevselliği anlamak için kritik değil.

### Arayüzü Sarmak

`BinaryMarshallable` arayüzünü uygulayan herhangi bir tip, kendi kodlamasını kontrol edebilir. Ne yazık ki bu, `Foo` veri tipi üzerinde birkaç fonksiyon tanımlamak kadar basit değildir. Sonuçta, ikili (binary) veriyi kodlamak ve çözmek için kullandığınız Go'nun `binary.Write()` ve `binary.Read()` fonksiyonları, sizin keyfi olarak tanımladığınız arayüz hakkında hiçbir şey bilmez.

Bu nedenle, içinde veriyi inceleyerek tipin `BinaryMarshallable` arayüzünü uygulayıp uygulamadığını belirleyeceğiniz bir `marshal()` ve `unmarshal()` sarmalayıcı (wrapper) fonksiyon oluşturmanız gerekir; bu, Liste 6-3'te gösterilmiştir. (Tüm kod listeleri, verilen GitHub deposunda `/ch-6/smb/smb/encoder/encoder.go` kök konumu altında bulunur: `https://github.com/blackhat-go/bhg`)

```go
func marshal(v interface{}, meta *Metadata) ([]byte, error) {
      --snip--
      bm, ok := v.(BinaryMarshallable)
      if ok {
          // Özel marshallable arayüzü bulundu.
          buf, err := bm.MarshalBinary(meta)
          if err != nil {
              return nil, err
          }
          return buf, nil
      }
      --snip--
}
```

```go
--snip--
func unmarshal(buf []byte, v interface{}, meta *Metadata) (interface{}, error) {
    --snip--
    bm, ok := v.(BinaryMarshallable)
    if ok {
         // Özel marshallable arayüzü bulundu.
         if err := bm.UnmarshalBinary(buf, meta); err != nil {
              return nil, err
         }
        return bm, nil
    }
    --snip--
}
```

**Liste 6-3:** Özel veri marshaling ve unmarshaling gerçekleştirmek için tip iddialarını (type assertion) kullanmak (`/ch-6/smb/smb/encoder/encoder.go`)

Liste 6-3, `https://github.com/blackhat-go/bhg/blob/master/ch-6/smb/smb/encoder/encoder.go` konumundan alınan `marshal()` ve `unmarshal()` fonksiyonlarının yalnızca bir alt bölümünü göstermektedir. Her iki fonksiyon da, verilen `interface` olan `v`'yi `bm` adlı bir `BinaryMarshallable` değişkenine dönüştürmeye (assert) çalışan benzer bir kod bölümüne sahiptir. Bu dönüşüm, yalnızca `v` her ne tip ise o tip, `BinaryMarshallable` arayüzü tarafından gerektiren fonksiyonları gerçekten uygularsa başarılı olur.

Bu işlem başarılı olursa, `marshal()` fonksiyonunuz `bm.MarshalBinary()` çağrısı yapar ve `unmarshal()` fonksiyonunuz `bm.UnmarshalBinary()` çağrısı yapar. Bu noktada, program akışınız tipin kendi kodlama ve çözme mantığına dallanır ve böylece tipin, nasıl ele alınacağı üzerinde tam kontrol sahibi olmasını sağlar.

### ASN.1 Kodlamasını Zorlamak

Şimdi, `Foo` tipinizi ASN.1 ile kodlamaya zorlayıp `Message` struct’ınızdaki diğer alanları olduğu gibi bırakmanın nasıl yapılacağına bakalım. Bunu yapmak için, Liste 6-4’te gösterildiği gibi bu tip üzerinde `MarshalBinary()` ve `UnmarshalBinary()` fonksiyonlarını tanımlamanız gerekir.

```go
func (f *Foo) MarshalBinary(meta *encoder.Metadata) ([]byte, error) {
    buf, err := asn1.Marshal(*f)
    if err != nil {
        return nil, err
    }
    return buf, nil
}

func (f *Foo) UnmarshalBinary(buf []byte, meta *encoder.Metadata) error {
    data := Foo{}
    if _, err := asn1.Unmarshal(buf, &data); err != nil {
        return err
    }
    *f = data
    return nil
}
```

**Liste 6-4:** ASN.1 kodlaması için `BinaryMarshallable` arayüzünü uygulamak

Bu metotlar, Go'nun `asn1.Marshal()` ve `asn1.Unmarshal()` fonksiyonlarını çağırmaktan başka pek bir şey yapmaz. Bu fonksiyonların varyasyonlarını `gss` package kodunda, `https://github.com/blackhat-go/bhg/blob/master/ch-6/smb/gss/gss.go` adresinde bulabilirsiniz. Aralarındaki tek gerçek fark, `gss` package kodunun, Go'nun ASN.1 kodlama fonksiyonunun SMB spesifikasyonunda tanımlanan veri formatıyla uyumlu çalışmasını sağlamak için ek ince ayarlara sahip olmasıdır.

`https://github.com/blackhat-go/bhg/blob/master/ch-6/smb/ntlmssp/ntlmssp.go` adresindeki `ntlmssp` package, `MarshalBinary()` ve `UnmarshalBinary()` fonksiyonlarının alternatif bir implementasyonunu içerir. Her ne kadar ASN.1 kodlamasını göstermese de, `ntlmssp` kodu, gerekli metadata'yı kullanarak keyfi bir veri tipinin nasıl kodlanacağını gösterir. Bu metadata — değişken uzunluklu byte slice’ların uzunlukları ve ofsetleri — kodlama süreciyle doğrudan ilişkilidir. Bu metadata, ele almanız gereken bir sonraki zorluğa bizi götürüyor.
