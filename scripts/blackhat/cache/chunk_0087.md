Senin `head()` implementasyonuna çok benzer şekilde, `get()` fonksiyonun üç değer döndürecek: durum kodu (status code), erişmeye çalıştığın sistemin temel (basic) kimlik doğrulama gerektirip gerektirmediğini ifade eden bir değer ve olası hata mesajları. İki fonksiyon arasındaki tek gerçek fark, `get()` fonksiyonunun iki ek string parametre kabul etmesi: bir kullanıcı adı ve bir parola. Bu değerlerden herhangi biri boş olmayan bir string olarak ayarlanmışsa, temel kimlik doğrulaması yapman gerektiğini varsayacaksın.

Muhtemelen bazılarınız implementasyonların tuhaf biçimde spesifik olduğunu, neredeyse herhangi bir esnekliği, yeniden kullanılabilirliği ve eklenti (plug-in) sisteminin taşınabilirliğini ortadan kaldıracak kadar dar kapsamlı olduğunu düşünüyordur. Sanki bu fonksiyonlar genel bir amaç için değil, çok spesifik bir kullanım durumu—yani temel kimlik doğrulamasını kontrol etmek—için tasarlanmış gibi. Sonuçta, neden yanıt gövdesini (response body) veya HTTP başlıklarını (headers) döndürmüyorsun? Benzer şekilde, neden çerezleri (cookies), diğer HTTP başlıklarını ayarlamak ya da gövde (body) içeren POST istekleri çıkmak için daha gelişmiş parametreler kabul etmiyorsun?

Cevap basitlik. Bu implementasyonların, daha sağlam bir çözüm inşa etmek için bir başlangıç noktası olarak davranabilir. Ancak böyle bir çözümün oluşturulması daha büyük bir çaba gerektirir ve muhtemelen implementasyon detayları arasında gezinmeye çalışırken kodun amacını kaybedersin. Bunun yerine, temel, kurucu kavramları anlamayı daha kolay hale getirmek için işleri daha basit ve daha az esnek bir şekilde yapmayı seçtik. Geliştirilmiş bir implementasyon, muhtemelen `http.Request` ve `http.Response` tiplerinin tamamını daha iyi temsil eden karmaşık, kullanıcı tanımlı tipler açığa çıkarırdı. O zaman Lua'dan birden fazla parametre kabul etmek ve döndürmek yerine, fonksiyon imzalarını sadeleştirebilir, kabul ettiğin ve döndürdüğün parametre sayısını azaltabilirdin. Bu meydan okumayı bir alıştırma olarak ele almanı, kodu ilkel (primitive) tipler yerine kullanıcı tanımlı `struct`’lar kabul edecek ve döndürecek şekilde değiştirmeni teşvik ediyoruz.

## Fonksiyonların Lua VM'e Kaydedilmesi

Buraya kadar, kullanmayı planladığın gerekli `net/http` çağrılarının etrafına sarmalayıcı (wrapper) fonksiyonlar yazdın ve bu fonksiyonları gopher-lua'nın tüketebileceği hâle getirdin. Ancak bu fonksiyonları Lua VM'e gerçekten kaydetmen gerekiyor. Liste 10-6'daki fonksiyon bu kayıt işlemini merkezileştirir.

```go
const LuaHttpTypeName = "http"

func register(L *lua.LState) {
    mt := L.NewTypeMetatable(LuaHttpTypeName)
    L.SetGlobal("http", mt)
    // static attributes
    L.SetField(mt, "head", L.NewFunction(head))
    L.SetField(mt, "get", L.NewFunction(get))
}
```

**Liste 10-6:** Lua ile eklentilerin kaydedilmesi (`/ch-10/lua-core/cmcliscanner/main.go`)

Önce Lua'da oluşturduğun ad alanını (namespace) benzersiz şekilde tanımlayacak bir sabit (constant) belirliyorsun. Bu durumda `http` kullanacaksın, çünkü esasen açığa çıkardığın işlevsellik bu. `register()` fonksiyonunda bir `lua.LState` işaretçisi (pointer) kabul ediyor ve bu ad alanı sabitini, `L.NewTypeMetatable()` çağrısı aracılığıyla yeni bir Lua tipi oluşturmak için kullanıyorsun. Bu metatablosunu, Lua'ya sunulan tipleri ve fonksiyonları takip etmek için kullanacaksın.

Daha sonra metatablo üzerinde `http` adlı global bir isim kaydediyorsun. Bu, `http` adını Lua VM için örtük bir package ismi hâline getirir. Aynı metatablo üzerinde, `L.SetField()` çağrılarını kullanarak iki alan da kaydediyorsun. Burada `http` ad alanında mevcut `head()` ve `get()` adlı iki statik fonksiyon tanımlıyorsun. Statik oldukları için Lua'da `http` tipinden bir örnek (instance) oluşturmadan, doğrudan `http.get()` ve `http.head()` şeklinde çağırabilirsin.

`SetField()` çağrılarında fark etmiş olabileceğin gibi, üçüncü parametre Lua çağrılarını ele alacak hedef fonksiyondur. Bu durumda, daha önce implementasyonunu yaptığın `get()` ve `head()` fonksiyonlarıdır. Bunlar, `L.NewFunction()` çağrısı içine sarılmıştır ve bu fonksiyon `func(*LState) int` formunda bir fonksiyon kabul eder; `get()` ve `head()` fonksiyonlarını da bu şekilde tanımlamıştın. `L.NewFunction()` bir `*lua.LFunction` döndürür. Pek çok veri tipi tanıttığımız ve muhtemelen gopher-lua'ya aşina olmadığın için bu biraz bunaltıcı gelebilir. Yalnızca şunu anlaman yeterli: Bu fonksiyon global ad alanını ve fonksiyon isimlerini kaydediyor ve bu isimlerle Go fonksiyonların arasında eşlemeler (mapping) oluşturuyor.

## Lua Eklentisinin Test Edilmesi

Bu örnek mükemmel değil ve ek tasarım değerlendirmelerinden fayda görebilir. Ancak çoğu saldırgan (adversarial) araçta olduğu gibi, en önemli şey çalışması ve bir problemi çözmesidir. Kodunu çalıştırmak, beklediğin gibi gerçekten de çalıştığını kanıtlar:

```bash
$ go run main.go
Found plugin: tomcat.lua
[+] Endpoint requires Basic Auth. Proceeding with password guessing
[+] Found creds - tomcat:tomcat
```

Artık temel bir çalışan örneğin olduğuna göre, fonksiyonlara gidiş-gelişlerde uzun argüman ve parametre listeleri geçirmek zorunda kalmamak için kullanıcı tanımlı tipler implement ederek tasarımı geliştirmeni teşvik ediyoruz. Bu noktada muhtemelen `struct` üzerinde örnek (instance) metotlarını kaydetmeyi, ister Lua içinde değer set/get işlemleri için, ister belirli bir örnek üzerinde metot çağrıları yapmak için, keşfetmen gerekecek. Bu süreçte, çok sayıda Go işlevselliğini Lua dostu bir şekilde sarmalayacağın için kodunun kayda değer biçimde daha karmaşık hâle geldiğini fark edeceksin.
