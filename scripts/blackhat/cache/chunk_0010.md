16   Bölüm 1

Önce, `chan int` türünde `c` adlı bir değişken tanımlayıp kullanırsın. Kanal üzerinden iletmeyi planladığın veri türüne bağlı olarak, farklı türlerde kanal tanımlayabilirsin. Bu örnekte, farklı string'lerin uzunluklarını goroutine'ler arasında tamsayı değerler olarak aktaracağın için bir `int` kanalı kullanmalısın.

Yeni bir işlemci (operator) fark etmiş olmalısın: `<-`. Bu işlemci, verinin bir kanala gidip gitmediğini ya da kanaldan gelip gelmediğini belirtir. Bunu, kovaya eşya koymak veya kovadan eşya çıkarmak gibi düşünebilirsin.

Tanımladığın `strlen()` fonksiyonu, bir kelimeyi string olarak ve veriyi eşzamanlamak (senkronize etmek) için kullanacağın bir kanalı parametre olarak alır. Fonksiyon, `c <- len(s)` ifadesini içeren tek bir deyimden oluşur. Bu ifade, string'in uzunluğunu belirlemek için yerleşik `len()` fonksiyonunu kullanır ve ardından sonucu `<-` işlemcisini kullanarak `c` kanalına yerleştirir.

`main()` fonksiyonu her şeyi bir araya getirir. Önce `make(chan int)` çağrısını yaparak bir tamsayı kanalı oluşturursun. Ardından `go` anahtar sözcüğünü kullanarak `strlen()` fonksiyonuna birden fazla eşzamanlı çağrı yaparsın; bu da birden fazla goroutine başlatır. `strlen()` fonksiyonuna iki string değeri ve sonuçların yerleştirilmesini istediğin kanalı parametre olarak geçersin. Son olarak, bu kez veri kanaldan dışarı doğru akar şekilde, `<-` işlemcisini kullanarak kanaldan veri okursun. Bu, kovadan öğe alıp, bu değerleri `x` ve `y` değişkenlerine atadığın anlamına gelir. Dikkat et, yürütme (execution), kanaldan yeterli veri okunabilene kadar bu satırda bloke olur.

Bu satır tamamlandığında, her bir string'in uzunluğunu ve bunların toplamını stdout'a yazdırırsın. Bu örnekte aşağıdaki çıktıyı üretir:

51116

Bu ilk başta bunaltıcı görünebilir, ancak Go'nun parladığı alan temel eşzamanlılık (concurrency) desenlerini vurgulamaktır. Go'da eşzamanlılık ve paralellik karmaşık hale gelebildiğinden, bu konuyu kendi başına da keşfetmekte özgürsün. Bu kitap boyunca, arabellekli kanallar (buffered channels), `wait group`'ler, `mutex`'ler ve daha fazlasını tanıtırken, eşzamanlılığın daha gerçekçi ve karmaşık uygulamalarından bahsedeceğiz.

## Hata Yönetimi (Error Handling)

Çoğu modern programlama dilinin aksine, Go `try/catch/finally` hata yönetimi için bir sözdizimi (syntax) içermez. Bunun yerine, hataların çağrı zincirindeki diğer fonksiyonlara “yukarı doğru kabarcıklanmasına” (bubble up) izin vermek yerine, hataların oluştukları yerde kontrol edilmesini teşvik eden minimalist bir yaklaşım benimser.

Go, aşağıdaki arayüz (interface) bildirimiyle tanımlanan yerleşik bir `error` türü içerir:

```go
type error interface {
    Error() string
}
```

Bu, `Error()` adlı ve string değer döndüren bir metodu uygulayan herhangi bir veri türünü, bir hata (error) olarak kullanabileceğin anlamına gelir. Örneğin, kodunun tamamında tanımlayıp kullanabileceğin özel bir hata türü şöyledir:

```go
type MyError string

func (e MyError) Error() string {
    return string(e)
}
```

Burada, `MyError` adlı kullanıcı tanımlı bir string türü oluşturur ve bu tür için `Error() string` metodunu uygularsın.

Hata yönetimine gelince, kısa sürede aşağıdaki desene alışacaksın:

```go
func foo() error {
    return errors.New("Some Error Occurred")
}

func main() {
    if err := foo(); err != nil {
        // Handle the error
    }
}
```

Fonksiyon ve metodların en az bir değer döndürmesi oldukça yaygındır. Bu değerlerden biri neredeyse her zaman bir `error` olur. Go'da döndürülen hata, fonksiyonun bir hata üretmediğini ve her şeyin beklenildiği gibi çalıştığını belirten `nil` değeri olabilir. `nil` olmayan bir değer ise fonksiyon içinde bir şeylerin bozulduğunu gösterir.

Dolayısıyla, `main()` fonksiyonunda gösterildiği gibi bir `if` deyimiyle hataları kontrol edebilirsin. Genellikle noktalı virgülle ayrılmış birden fazla ifade görürsün. İlk ifade fonksiyonu çağırır ve dönen hatayı bir değişkene atar. İkinci ifade ise bu hatanın `nil` olup olmadığını kontrol eder. `if` deyiminin gövdesini, hatayı ele almak (handle etmek) için kullanırsın.

Go'da hataların en iyi şekilde nasıl yönetileceği ve loglanacağı konusunda farklı yaklaşımlar ve felsefeler bulunur. Zorluklardan biri, diğer dillerin aksine Go'nun yerleşik `error` türünün, hatanın bağlamını veya konumunu belirlemene yardımcı olacak bir yığın izi (stack trace) içermemesidir. Elbette kendi uygulamanda bir yığın izi üretip bunu özel bir türe atayabilirsin; ancak bunun nasıl uygulanacağı geliştiricilere bırakılmıştır. Bu ilk başta biraz can sıkıcı olabilir, fakat uygun uygulama tasarımıyla yönetebilirsin.

## Yapılandırılmış Veriyi İşleme

Güvenlik uygulayıcıları, genellikle JSON veya XML gibi ortak kodlamaya sahip, yapılandırılmış veriyi işleyen kodlar yazar. Go, veri kodlama için standart paketler içerir. En sık kullanacağın paketler arasında `encoding/json` ve `encoding/xml` bulunur.

Her iki paket de rastgele veri yapılarını `marshal` ve `unmarshal` edebilir; yani string'leri yapılara (struct'lara) ve yapıları string'lere dönüştürebilirler.

Aşağıdaki örneğe bakalım; bu örnekte bir yapıyı (struct) bir byte slice'a serileştiriyor (serialize) ve ardından bu byte slice'ı tekrar bir yapıya deserialize ediyoruz:

```go
type Foo struct {
    Bar string
    Baz string
}

func main() {
    f := Foo{"Joe Junior", "Hello Shabado"}
    b, _ := json.Marshal(f)
    fmt.Println(string(b))
    json.Unmarshal(b, &f)
}
```

Bu kod (en iyi uygulamalardan saparak olası hataları yok sayıyor) `Foo` adlı bir `struct` türü tanımlar. `main()` fonksiyonunda bu `struct`'ı ilklendirir ve `Foo` örneğini (`instance`) parametre olarak geçirerek `json.Marshal()` çağrısı yaparsın. `Marshal()` metodu, `struct`'ı JSON'a kodlar ve bir byte slice döndürür; bu byte slice'ı daha sonra stdout'a yazdırırsın. Ortaya çıkan çıktı, `Foo` struct'ının JSON ile kodlanmış string temsili olacaktır:

```text
{"Bar":"Joe Junior","Baz":"Hello Shabado"}
```
