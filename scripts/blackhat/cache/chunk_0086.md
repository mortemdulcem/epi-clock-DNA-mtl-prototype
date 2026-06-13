```go
                       host = 1.CheckString(1)
                       port = uint64(1.CheckInt64(2))
                       path = 1.CheckString(3)
                       url = fmt.Sprintf("http://%5AdAs a , host, port, path)
                       if resp, err = http.Nead(ur1); err I= nil {
                            1.Push(lua.LNumber(0))
                            1.Push(lua.LBool(false))
                            1.Push(lua.LString(fmt.Sprintf("Request failed: %s", err)))
                            return 3

                       1.Push(lua.LNumber(resp.StatusCode))
                       1.Push(lua.LBool(resp.Header.Get("NWN-Authenticate")
                       1.Push(lua.LStringr "))
                       return 3

**Liste 10-4: Lua için bir head() fonksiyonu oluşturma (/ch-10/lua-core/cmd/scanner/main.go)**
```

İlk olarak, `head()` fonksiyonunuzun bir `lua.LState` işaretçisini parametre olarak aldığını ve bir `int` döndürdüğünü fark edin. Bu, Lua VM’e kaydetmek istediğiniz herhangi bir fonksiyon için beklenen imzadır. `lua.LState` türü, birazdan göreceğiniz gibi, Lua’dan Go’ya ve Go’dan Lua’ya aktarılan parametreler de dahil olmak üzere VM’in çalışan durumunu tutar. Geri dönüş değerleriniz `lua.LState` örneği içinde bulunacağı için, `int` dönüş türü, döndürülen değerlerin sayısını temsil eder. Bu sayede, Lua eklentiniz (plug-in) bu dönüş değerlerini okuyup kullanabilecektir.

`lua.LState` nesnesi `l`, fonksiyonunuza aktarılan tüm parametreleri içerdiğinden, veriyi `l.CheckString()` ve `l.CheckInt64()` çağrılarıyla okursunuz. (Bu örnek için gerek duyulmasa da, diğer beklenen veri tiplerini karşılamak için başka `Check*` fonksiyonları da vardır.) Bu fonksiyonlar, istenen parametrenin indeksini temsil eden bir tamsayı alır. 0-indeksli Go `slice`’larının aksine Lua 1-indekslidir. Dolayısıyla `l.CheckString(1)` çağrısı, Lua fonksiyon çağrısında verilen ilk parametreyi, bir `string` olmasını bekleyerek, alır. Beklediğiniz her parametre için, beklenen değerin doğru indeksini vererek aynı işlemi yaparsınız. `head()` fonksiyonunuz için, Lua’dan `head(host, port, path)` şeklinde bir çağrı bekliyorsunuz; burada `host` ve `path` `string`, `port` ise tam sayıdır. Daha dayanıklı bir uygulamada, gelen verinin geçerli olduğundan emin olmak için burada ek kontroller yapmak isteyebilirsiniz.

Fonksiyon, bir HTTP HEAD isteği göndermeye ve bazı hata kontrolleri yapmaya devam eder. Lua çağıranlarına değer döndürmek için, `l.Push()` fonksiyonunu çağırarak ve `lua.LValue` arayüzünü (interface) gerçekleştiren (implement eden) bir nesne vererek bu değerleri `lua.LState` üzerine itersiniz (push). `gopher-lua` paketi, bu arayüzü uygulayan çeşitli türler içerir; örneğin sayısal ve mantıksal (boolean) dönüş türleri oluşturmak için `lua.LNumber(0)` ve `lua.LBool(false)` çağrılarını yapmak kadar kolaydır.

Bu örnekte, üç değer döndürüyorsunuz. İlki HTTP durum (status) kodu, ikincisi sunucunun temel kimlik doğrulama (basic authentication) gerektirip gerektirmediğini belirler, üçüncüsü ise bir hata mesajıdır. Bir hata oluşursa durum kodunu 0’a ayarlamayı seçmiş bulunuyoruz. Daha sonra, `LState` örneğiniz üzerine ittiğiniz öğe sayısı olan 3’ü döndürürsünüz. `http.Head()` çağrınız bir hata üretmezse, bu sefer geçerli bir durum kodu ile dönüş değerlerinizi `LState` üzerine itersiniz, temel kimlik doğrulamasını kontrol edersiniz ve yine 3 döndürürsünüz.

## get() Fonksiyonunu Oluşturma

Sonraki adımda, önceki örnekte olduğu gibi `net/http` paketinin işlevselliğini saran `get()` fonksiyonunu oluşturacaksınız. Ancak bu sefer, bir HTTP GET isteği gönderiyorsunuz. Bunun dışında, `get()` fonksiyonu hedef uç noktaya (endpoint) bir HTTP isteği göndermek için `head()` fonksiyonunuzla oldukça benzer yapılar kullanır. Liste 10-5’teki kodu girin.

```go
func get (1 *lua .LState) int {
    var (
        host      string
        port      uint64
        username string
        password string
        path      string
        resp      *http. Response
        err       error
        url       string
        client *http.Client
        req       *http.Request

    host = 1.CheckString(i)
    port = uint64(1.CheckInt64(2))
 0 username = 1.CheckString(3)
    password = 1.CheckString(4)
    path = 1.CheckString(5)
    un = fmt.Sprintf("http://%s:%d/%s", host, port, path)
    client = new(http.Client)
```

```go
                      if req, err = http.NewRequest("GET", url, nil); err != nil {
                           1.Push(lua.LNumber(0))
                           1.Push(lua.LBool(false))
                           1.Push(lua.LString(fmt.Sprintf("Unable to build GET request: %s", err)))
                           return 3

                      if username != "" II password != "" (
                           // Assume Basic Auth is required since user and/or password is set
                           req.SetBasicAuth(username, password)

                      if resp, err = client.Do(req); err 1= nil {
                           1.Push(lua.LNumber(0))
                           1.Push(lua.LBool(false))
                           1.Push(lua.LString(fmt.Sprintf("Unable to send GET request: %s", err)))
                           return 3

                      1.Push(lua.LNumber(resp.StatusCode))
                      1.Push(lua.LBool(false))
                      1.Push(lua.LString(""))
                      return 3

**Liste 10-5: Lua için bir get() fonksiyonu oluşturma (/ch-10/lua-core/cmd/scanner/main.go)**
```
