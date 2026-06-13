Go ayrıca slice ve map gibi daha karmaşık veri tiplerine sahiptir. Slice'lar,
dinamik olarak yeniden boyutlandırabildiğiniz ve fonksiyonlara daha verimli
şekilde iletebildiğiniz dizilere benzer. Map'ler ise, benzersiz bir anahtar için
değeri verimli ve hızlı şekilde bulmanıza imkân tanıyan, sırasız anahtar/değer
(key/value) çiftleri listeleridir.

Slice ve map tanımlamak, ilklendirmek ve bunlarla çalışmak için pek çok
yol vardır. Aşağıdaki örnek, hem bir slice `s` hem de bir map `m` tanımlamanın
ve her ikisine de eleman eklemenin yaygın bir yolunu göstermektedir:

```go
var s = make([]string, 0)
var m = make(map[string]string)
s = append(s, "some string")
m["some key"] = "some value"
```

Bu kod iki yerleşik fonksiyonu kullanır: her bir değişkeni ilklendirmek için
`make()` ve bir slice'a yeni bir eleman eklemek için `append()`. Son satır,
`some key` ve `some value` anahtar/değer çiftini map `m` içine ekler. Bu veri
tiplerini tanımlamak ve kullanmak için tüm yöntemleri keşfetmek üzere resmi
Go dokümantasyonunu okumanızı öneririz.

---

## İşaretçiler (Pointers), Struct'lar ve Arayüzler (Interfaces)

Bir işaretçi (pointer), bellekte belirli bir alanı gösterir ve orada saklanan
değeri almanıza olanak tanır. C dilinde olduğu gibi, bir değişkenin bellekteki
adresini almak için `&` operatörünü, adresi çözümleyip (dereference) saklanan
değeri elde etmek için `*` operatörünü kullanırsınız. Aşağıdaki örnek bunu
göstermektedir:

```go
var count = int(42)
ptr := &count
fmt.Println(*ptr)
*ptr = 100
fmt.Println(count)
```

Bu kod bir tamsayı `count` tanımlar ve ardından `&` operatörünü kullanarak
bir işaretçi `ptr` oluşturur. Bu, `count` değişkeninin adresini döndürür.
`fmt.Println()` fonksiyon çağrısı sırasında `ptr` değişkenini çözümlersiniz
(dereference) ve `count` değerini stdout'a yazdırırsınız. Daha sonra `*`
operatörünü kullanarak `ptr` işaretçisinin gösterdiği bellek konumuna yeni
bir değer atarsınız. Bu adres `count` değişkenine ait olduğundan, yapılan
atama bu değişkenin değerini değiştirir; bunu da ekrana yazdırarak
doğrularsınız.

Yeni veri tiplerini, bu tiplere ait alanları (field) ve metotları belirleyerek
tanımlamak için `struct` tipini kullanırsınız. Örneğin, aşağıdaki kod bir
`Person` tipi tanımlar:

```go
type Person struct {
    Name string
    Age  int
}

func (p *Person) SayHello() {
    fmt.Println("Hello,", p.Name)
}

func main() {
    var guy = new(Person)
    guy.Name = "Dave"
    guy.SayHello()
}
```

Kod, `type` anahtar kelimesini kullanarak iki alana sahip yeni bir `struct`
tanımlar: `Name` adlı bir `string` ve `Age` adlı bir `int`.

`Person` tipine atanmış, `p` değişkeni üzerinden çalışan bir `SayHello()`
metodu tanımlarsınız. Bu metod, kendisine çağrı yapılan `struct` olan `p`'ye
bakarak stdout'a bir selamlama mesajı yazdırır. `p`'yi, diğer dillerdeki `self`
veya `this` referansına benzetebilirsiniz. Ayrıca programın giriş noktası
olarak görev yapan bir `main()` fonksiyonu tanımlarsınız. Bu fonksiyon,
`new` anahtar kelimesini kullanarak yeni bir `Person` ilklendirir. Bu kişiye
`Dave` adını atar ve ardından o kişiye `SayHello()` demesini söyler.

Struct'larda diğer dillerde üyelerine erişimi kontrol etmek için kullanılan
`private`, `public` veya `protected` gibi kapsam (scope) değiştiricileri yoktur.
Bunun yerine Go, kapsamı belirlemek için büyük/küçük harf kullanımını
esas alır: büyük harfle başlayan tipler ve alanlar dışarıya ihraç edilir
(exported) ve paket dışından erişilebilir; küçük harfle başlayanlar ise
özeldir (private) ve yalnızca paket içinde erişilebilir.

Go'nun `interface` tipini bir şablon veya sözleşme (contract) olarak
düşünebilirsiniz. Bu şablon, herhangi bir somut uygulamanın, bu arayüz
tipinin bir türü olarak kabul edilmesi için yerine getirmesi gereken beklenen
eylemler (metotlar) kümesini tanımlar. Bir arayüz tanımlamak için, bir dizi
metot tanımlarsınız; bu metotları doğru imzalarla (signature) içeren her veri
tipi bu sözleşmeyi yerine getirir ve o arayüzün bir türü olarak kabul edilir.
Bir örneğe bakalım:

```go
type Friend interface {
    SayHello()
}
```

Bu örnekte, `Friend` adlı bir arayüz tanımladınız; bu arayüz, tek bir metodun
gerçeklenmesini gerektirir: `SayHello()`. Bu, `SayHello()` metodunu
gerçekleyen herhangi bir tipin bir `Friend` olduğu anlamına gelir. Dikkat
ederseniz `Friend` arayüzü bu fonksiyonu aslında implement etmez; yalnızca
şunu söyler: Eğer bir `Friend` isen, `SayHello()` yapabilmelisin.

Aşağıdaki `Greet()` fonksiyonu, girdi olarak bir `Friend` arayüzü alır ve
arkadaşa özgü (Friend-specific) bir şekilde merhaba der:

```go
func Greet(f Friend) {
    f.SayHello()
}
```

Bu fonksiyona herhangi bir `Friend` tipini geçebilirsiniz. Neyse ki, önceki
örnekte kullanılan `Person` tipi `SayHello()` diyebilmektedir—yani bir
`Friend`'dir. Bu nedenle, yukarıda gösterilen koddaki gibi `Greet()` adlı bir
fonksiyon bir `Friend` girdi parametresi bekliyorsa, ona bir `Person` geçebilirsiniz:

```go
func main() {
    var guy = new(Person)
    guy.Name = "Dave"
    Greet(guy)
}
```

Arayüzler ve struct'lar kullanarak, `Friend` arayüzünü implement ettikleri
sürece aynı `Greet()` fonksiyonuna geçebileceğiniz birden fazla tip
tanımlayabilirsiniz. Şu değiştirilmiş örneği düşünün:

```go
type Dog struct{}

func (d *Dog) SayHello() {
    fmt.Println("Woof woof")
}

func main() {
    var guy = new(Person)
    guy.Name = "Dave"
    Greet(guy)
    var dog = new(Dog)
    Greet(dog)
}
```

Bu örnek, `SayHello()` yapabilen yeni bir `Dog` tipini gösterir; dolayısıyla
`Dog` da bir `Friend`'dir. Hem `Person` hem de `Dog` `SayHello()` yapabildiği
için, ikisini de `Greet()` edebilirsiniz.

Arayüzleri kitap boyunca birçok kez ele alacağız; böylece bu kavramı daha
iyi anlayacaksınız.

---

## Kontrol Yapıları

Go, diğer modern dillere kıyasla biraz daha az sayıda kontrol yapısı içerir.
Buna rağmen, Go ile koşullar (conditionals) ve döngüler (loops) dahil olmak
üzere karmaşık işlemleri hâlâ gerçekleştirebilirsiniz.

Go'daki birincil koşul yapısı `if/else` yapısıdır:

```go
if x == 1 {
    fmt.Println("X is equal to 1")
} else {
    fmt.Println("X is not equal to 1")
}
```
