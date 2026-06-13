Go'nun sözdizimi (syntax), diğer dillerin sözdiziminden biraz sapar. Örneğin, bu örnekteki `x == 1` koşul kontrolünü parantez içine almazsınız. Tüm kod bloklarını — önceki tek satırlık bloklar da dahil — süslü parantezler içine almak zorundasınız. Birçok modern dil tek satırlık bloklar için süslü parantezleri isteğe bağlı tutar, ancak Go'da zorunludur.

İki veya daha fazla seçeneği içeren koşullar için Go, `switch` ifadesi sağlar. Aşağıda bir örnek bulunmaktadır:

```go
switch x {
    case "foo":
        fmt.Println("Found foo")
    case "bar":
        fmt.Println("Found bar")
    default:
        fmt.Println("Default case")
}
```

Bu örnekte, `switch` ifadesi `x` değişkeninin içeriğini çeşitli değerlerle — `"foo"` ve `"bar"` — karşılaştırır ve `x` bu koşullardan biriyle eşleştiğinde stdout'a bir mesaj yazar. Ayrıca bu örnekte, diğer koşulların hiçbirinin eşleşmemesi durumunda çalışacak bir `default` durumu da bulunmaktadır.

Dikkat edin, birçok modern dilin aksine, `case` bloklarına `break` ifadeleri eklemeniz gerekmez. Diğer dillerde, çalışma çoğu zaman bir `break` ifadesine veya `switch` ifadesinin sonuna ulaşılana kadar her bir `case` bloğunda devam eder. Go ise, birden fazla `case` veya `default` bloğunu **asla** çalıştırmaz; en fazla bir tanesini çalıştırır.

Go ayrıca, `switch` ifadesi kullanarak tür doğrulaması (type assertion) yapan, `type switch` denilen özel bir varyasyona sahiptir. `Type switch` ifadeleri, bir arayüzün (interface) altında yatan gerçek türü anlamaya çalışırken kullanışlıdır.

Örneğin, `i` adında bir arayüzün (interface) altında yatan türü elde etmek için `type switch` kullanabilirsiniz:

```go
func f(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Println("I'm an integer!")
    case string:
        fmt.Println("I'm a string!")
    default:
        fmt.Println("Unknown type!")
    }
}
```

Bu örnek, `i.(type)` gibi özel bir sözdizimi kullanarak `i` arayüz değişkeninin türünü elde eder. Bu değeri, her bir `case` ifadesinin belirli bir türe karşılık geldiği bir `switch` ifadesinde kullanırsınız. Bu örnekte `case` blokları `int` veya `string` temel türlerini kontrol ediyor, ancak aynı şekilde işaretçiler (pointer) veya kullanıcı tanımlı `struct` türlerini de kontrol edebilirsiniz.

Go'nun son akış kontrol yapısı `for` döngüsüdür. `For` döngüsü, yineleme (iteration) veya belirli kod bölümlerini tekrar tekrar çalıştırmak için Go'daki tek yapıdır. Elinizin altında `do` veya `while` gibi döngü yapılarına sahip olmamak ilk bakışta garip gelebilir, ancak `for` döngüsünün çeşitli varyasyonlarını kullanarak bu yapıların davranışlarını yeniden oluşturabilirsiniz. İşte `for` döngüsünün bir varyasyonu:

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

Bu kod 0'dan 9'a kadar sayıları dolaşır ve her bir sayıyı stdout'a yazdırır. İlk satırdaki noktalı virgüllere dikkat edin. Birçok diğer dilde noktalı virgüller satır sonu ayırıcıları olarak kullanılırken, Go'da çeşitli kontrol yapılarında, bir satırda birbiriyle ilişkili ancak ayrı alt görevler gerçekleştirmek için kullanılır. İlk satır, başlangıç (initialization) mantığını (`i := 0`), koşul ifadesini (`i < 10`) ve artış ifadesini (`i++`) birbirinden ayırmak için noktalı virgüller kullanır. Bu yapı, modern dillerden herhangi birinde kod yazmış olanlar için son derece tanıdık olmalıdır; çünkü bu dillerin geleneklerini yakından takip eder.

Aşağıdaki örnek, bir `slice` veya `map` gibi bir koleksiyon üzerinde dönen `for` döngüsünün küçük bir varyasyonunu gösterir:

```go
nums := []int{2, 4, 6, 8}
for idx, val := range nums {
    fmt.Println(idx, val)
}
```

Bu örnekte, `nums` adlı bir `int` slice'ını başlatırsınız. Ardından `for` döngüsünde `range` anahtar sözcüğünü kullanarak slice üzerinde yineleme yaparsınız. `range` anahtar sözcüğü iki değer döndürür: `idx` ile temsil edilen geçerli indeks ve o indeksteki geçerli değerin bir kopyası `val`. Eğer indeksi kullanmayı düşünmüyorsanız, `for` döngüsünde `idx` yerine alt çizgi (`_`) kullanarak Go'ya bu değere ihtiyaç duymayacağınızı belirtebilirsiniz.

Aynı döngü mantığını `map` yapılarıyla da kullanarak her bir anahtar/değer çiftini elde edebilirsiniz.

## Eşzamanlılık (Concurrency)

Daha önce ele aldığımız kontrol yapıları gibi, Go'nun eşzamanlılık (concurrency) modeli de diğer dillere göre çok daha basittir. Kodu eşzamanlı olarak çalıştırmak için, aynı anda çalışabilen fonksiyonlar veya metodlar olan `goroutine`'leri kullanabilirsiniz. `Goroutine`'ler sıklıkla hafif iş parçacıkları (lightweight threads) olarak tanımlanır, çünkü bunları oluşturmanın maliyeti gerçek iş parçacıklarına kıyasla oldukça düşüktür.

Bir `goroutine` oluşturmak için, eşzamanlı çalıştırmak istediğiniz fonksiyon veya metod çağrısının önüne `go` anahtar sözcüğünü koyarsınız:

```go
func f() {
    fmt.Println("f function")
}

func main() {
    go f()
    time.Sleep(1 * time.Second)
    fmt.Println("main function")
}
```

Bu örnekte `f()` adlı bir fonksiyon tanımlarsınız ve programın giriş noktası olan `main()` fonksiyonu içinde `f()` fonksiyonunu çağırırsınız. Çağrının başına `go` anahtar sözcüğünü ekleyerek, programın `f()` fonksiyonunu eşzamanlı olarak çalıştırmasını sağlarsınız; diğer bir deyişle, `main()` fonksiyonunun yürütülmesi `f()` fonksiyonunun tamamlanmasını beklemeden devam eder. Ardından `time.Sleep(1 * time.Second)` kullanarak `main()` fonksiyonunu geçici olarak duraklatırsınız ki `f()` fonksiyonu tamamlanabilsin. Eğer `main()` fonksiyonunu duraklatmasaydınız, program muhtemelen `f()` fonksiyonu tamamlanmadan önce sonlanır ve `f()` fonksiyonunun stdout'a yazdığı çıktıyı hiç görmezdiniz. Doğru şekilde yaparsanız, hem `f()` hem de `main()` fonksiyonlarını çalıştırmayı tamamladığınızı gösteren mesajların stdout'a yazıldığını görürsünüz.

Go, `channel` adı verilen ve `goroutine`'lerin yürütme süreçlerini senkronize etmeleri ve birbirleriyle iletişim kurmaları için bir mekanizma sağlayan bir veri tipine sahiptir. Farklı dizgelerin (string) uzunluklarını ve bunların toplamını aynı anda görüntülemek için `channel` kullanan bir örneğe bakalım:

```go
func strlen(s string, c chan int) {
    c <- len(s)
}

func main() {
    c := make(chan int)
    go strlen("Salutations", c)
    go strlen("world", c)
    x, y := <-c, <-c
    fmt.Println(x, y, x+y)
}
```
