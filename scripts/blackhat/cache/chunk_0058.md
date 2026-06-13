Olay bloğu, ilgili üstveriyi (metadata) takip etmek için kullanılan bir tür olan yeni bir `Metadata` nesnesi 0 tanımlayarak başlar; buna mevcut arabellek (buffer) ofseti, alan etiketleri (field tags) ve diğer bilgiler dahildir. Tür değişkenimizi kullanarak, `NumField()` metodunu çağırır ve `e` struct’ındaki alanların sayısını alırız. Bu metod, döngü için sınır görevi gören bir tamsayı değeri döndürür.

Döngü içinde, türün `Field(index int)` metodunu çağırarak mevcut alanı çıkarabiliriz. Bu metod, `reflect.StructField` türünde bir değer döndürür. Bu kod parçası boyunca bu metodu birkaç kez kullandığımızı göreceksin. Bunu, bir `slice` içinden indeks değeriyle eleman almayı düşün. İlk kullanımımız 0, alanın adını çıkarmak için alanı alır. Örneğin, `SecurityBufferOffset` ve `SecurityBlob`, Liste 6-6’da tanımlanan `NegotiateRes` struct’ı içindeki alan adlarıdır. Alan adı, `Metadata` nesnemizin `CurrField` özelliğine atanır. `Field(index int)` metoduna yapılan ikinci çağrı ise Liste 6-7’deki `parseTags()` fonksiyonuna 0 girdi olarak verilir. Bu fonksiyonun struct alan etiketlerini (field tags) ayrıştırdığını biliyoruz. Etiketler, daha sonra izlenip kullanılmak üzere `Metadata` nesnemize eklenir.

Sonraki adımda, alan türü üzerinde özel olarak işlem yapmak için bir `switch` ifadesi kullanırız 0. Yalnızca iki durum vardır. İlk durum, alanın kendisinin bir `struct` olduğu durumları işler 0; bu durumda, `unmarshal()` fonksiyonunu özyinelemeli (recursive) olarak çağırır ve ona alanı işaretçi (pointer) olarak bir arayüz (interface) şeklinde geçiririz. İkinci durum ise diğer tüm türleri (ilkel tipler, `slice`’lar vb.) ele alır; `unmarshal()` fonksiyonunu yine özyinelemeli olarak çağırır ve bu kez alana kendisini bir arayüz 0 olarak geçiririz. Her iki çağrı da, arabelleği mevcut ofsetimizde başlayacak şekilde ilerletmek için bazı numaralar yapar. Özyinelemeli çağrımız sonunda `interface{}` döndürür; bu, çözülmüş (unmarshaled) verimizi içeren bir türdür. Yansıma (reflection) kullanarak, mevcut alanımızın değerini, bu arayüz verisinin değeriyle ayarlarız 0. Son olarak, arabellekteki mevcut ofsetimizi `e` içinde ilerletiriz.

Vay canına! Bunu geliştirmenin neden zor olabileceğini görebiliyor musun? Her tür girdi için ayrı bir `case`’imiz var. Neyse ki, `struct`’ı işleyen `case` bloğu en karmaşık olanıdır.

## uint16 İşleme

Dikkatle takip ediyorsan muhtemelen şu soruyu soruyorsundur: veriyi arabellekten gerçekten nerede okuyorsun? Cevap, Liste 6-9’da hiçbir yerde. `unmarshal()` fonksiyonuna özyinelemeli çağrılar yaptığımızı ve her seferinde iç alanları bu fonksiyona geçtiğimizi hatırla. Sonunda ilkel veri türlerine ulaşacağız. Sonuçta, en içteki iç içe `struct`’lar temel veri türlerinden oluşur. Temel bir veri türüyle karşılaştığımızda, kodumuz en dıştaki `switch` ifadesindeki farklı bir `case` ile eşleşir. Örneğin, bir `uint16` veri türüyle karşılaştığımızda, aşağıdaki `case` bloğu (Liste 6-10) çalışır.

```go
                 case reflect.Uint16:
                     var ret uint16
                     if err := binary.Read(r, binary.LittleEndian, &ret); err != nil {
                          return nil, err
                     }
                     if meta.Tags.Has("len") {
                         ref, err := meta.Tags.GetString("len")
                         if err != nil {
                              return nil, err

                          meta.Lens[ref] = uint64(ret)

                  meta.CurrOffset += uint64(binary.Size(ret))
                    return ret, nil
```

**Liste 6-10: uint16 verinin çözülmesi (unmarshaling) (`/ch-6/smb/smbencoder/encoder.go/`)**

Bu `case` bloğunda, veriyi arabelleğimizden `ret` 0 isimli bir değişkene okumak için `binary.Read()` çağrısı yaparız. Bu fonksiyon, hedefin türüne bakarak kaç bayt okunacağını bilecek kadar akıllıdır. Bu durumda `ret` bir `uint16` olduğu için 2 bayt okunur.

Sonra, `len` alan etiketinin 0 mevcut olup olmadığını kontrol ederiz. Eğer mevcutsa, bu anahtara bağlı değeri —yani bir alan adını— elde ederiz S. Bu değerin, mevcut alanın atıfta bulunmasının beklendiği alan adı olacağını hatırla. SMB mesajlarında, uzunluğu belirleyen alanlar gerçek veriden önce geldiğinden, arabellek verisinin tam olarak nerede yer aldığı bilinmez; dolayısıyla henüz bir işlem yapamayız.

Yeni edindiğimiz uzunluk üstverisini saklamak için `Metadata` nesnemizden daha iyi bir yer yoktur. Bunu, başvuru alan adları ile onların uzunlukları arasındaki ilişkiyi tutan bir `map[string]uint64` içinde saklarız 0. Başka bir deyişle, artık değişken uzunluklu bir `byte slice`’ın ne kadar uzun olması gerektiğini biliyoruz. Az önce okuduğumuz verinin boyutu kadar mevcut ofseti 0 ileri alır ve arabellekten okunan değeri geri döndürürüz.

Benzer mantık ve üstveri takibi, `offset` etiket bilgisini işlerken de gerçekleşir, ancak kısalık adına o kodu çıkardık.

## Slice’ların İşlenmesi

Liste 6-11’de, `slice`’ları çözen (unmarshal eden) `case` bloğunu görebilirsin; bu blok, etiketler ve üstveriyi kullanarak hem sabit hem değişken uzunluklu verileri hesaba katmamız için gereklidir.

```go
case reflect.Slice, reflect.Array:
   switch typev.Elem().Kind() {
   case reflect.Uint8:
        var length, offset int
        var err error
        if meta.Tags.Has("fixed") {
            if length, err = meta.Tags.GetInt("fixed"); err != nil {
                 return nil, err
```

```go
              // Sabit uzunluklu alanlar mevcut ofseti ileri alır
              meta.CurrOffset += uint64(length)
            else {
              if val, ok := meta.Lens[meta.CurrField]; ok {
                   length = int(val)
                 else {
                   return nil, errors.New("Variable length field missing length reference in struct")

             if val, ok := meta.Offsets[meta.CurrField]; ok {
                  offset = int(val)
                else {
                  // Map içinde offset bulunamadı. Mevcut ofseti kullan
                  offset = int(meta.CurrOffset)
```
