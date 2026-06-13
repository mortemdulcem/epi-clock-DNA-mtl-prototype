### Bir Yapılandırma `struct`’u ve Bir RPC Metodu Oluşturma

Liste 3-15’te, tanımladığınız tipleri fiilen kullanıyor ve Metasploit’e RPC komutları göndermek için gerekli metotları oluşturuyorsunuz. Shodan örneğinde olduğu gibi, ilgili yapılandırma ve kimlik doğrulama bilgilerini tutmak için keyfi bir tip de tanımlıyorsunuz. Böylece `host`, `port` ve kimlik doğrulama belirteci (authentication token) gibi ortak öğeleri açıkça ve tekrar tekrar geçirmek zorunda kalmazsınız. Bunun yerine, bu tipi kullanır ve üzerinde metotlar inşa edersiniz; böylece veriler örtük olarak kullanılabilir olur.

```go
type Metasploit struct {
    host  string
    user  string
    pass  string
    token string
}

func New(host, user, pass string) *Metasploit {
    msf := &Metasploit{
        host: host,
        user: user,
        pass: pass,
    }

    return msf
}
```

**Liste 3-15: Metasploit istemci tanımı (`/ch-3/metasploit-minimal/rpc/msf.go`)**

Artık bir `struct`’unuz ve kullanım kolaylığı için onu ilklendirip döndüren `New()` adlı bir fonksiyonunuz var.

### Uzaktan Çağrılar Gerçekleştirme

Artık uzak çağrıları gerçekleştirmek için `Metasploit` tipiniz üzerinde metotlar inşa edebilirsiniz. Yoğun kod tekrarını önlemek için, Liste 3-16’da, serileştirme (serialization), ters serileştirme (deserialization) ve HTTP iletişim mantığını gerçekleştiren bir metot yazarak başlıyorsunuz. Böylece geliştirdiğiniz her RPC fonksiyonuna bu mantığı dahil etmek zorunda kalmazsınız.

```go
func (msf *Metasploit) send(req interface{}, res interface{}) error {
    buf := new(bytes.Buffer)

    msgpack.NewEncoder(buf).Encode(req)
    dest := fmt.Sprintf("http://%s/api", msf.host)
    r, err := http.Post(dest, "binary/message-pack", buf)
    if err != nil {
        return err
    }

    defer r.Body.Close()

    if err := msgpack.NewDecoder(r.Body).Decode(&res); err != nil {
        return err
    }

    return nil
}
```

**Liste 3-16: Yeniden kullanılabilir serileştirme ve ters serileştirme içeren genel `send()` metodu (`/ch-3/metasploit-minimal/rpc/msf.go`)**

`send()` metodu, `interface{}` tipinde istek ve yanıt parametreleri alır. Bu `interface` tipi, metoda herhangi bir istek `struct`’u geçirmenize, ardından bu isteği serileştirip sunucuya göndermenize imkân tanır. Yanıtı açıkça döndürmek yerine, `res interface{}` parametresini, çözümlenmiş HTTP yanıtını bellekteki konumuna yazarak doldurmak için kullanırsınız.

Sonrasında, isteği kodlamak için `msgpack` kütüphanesini kullanırsınız. Bunu yapmanın mantığı, diğer standart, yapılandırılmış veri tipleriyle aynıdır: önce `NewEncoder()` ile bir kodlayıcı (encoder) oluşturur, sonra `Encode()` metodunu çağırırsınız. Bu işlem, `buf` değişkenini istek `struct`’unun MessagePack ile kodlanmış temsiliyle doldurur. Kodlamanın ardından, `Metasploit` alıcısındaki (`msf`) verileri kullanarak hedef URL’yi oluşturursunuz. Bu URL’yi kullanır ve gövdesini serileştirilmiş veriye ayarlayarak, içerik tipini açıkça `binary/message-pack` olacak şekilde bir POST isteği gönderirsiniz. Son olarak yanıt gövdesini çözümlersiniz. Önceden de belirttiğimiz gibi, çözümlenen veri, metoda geçirilmiş yanıt `interface`’ının bellekteki konumuna yazılır. Veri kodlama ve çözümleme işlemleri, istek veya yanıt `struct` tiplerini açıkça bilmeye ihtiyaç duymadan yapılır; bu da bu metodu esnek ve yeniden kullanılabilir kılar.

Liste 3-17’de tüm bu mantığın özünü olduğu gibi görebilirsiniz.

```go
func (msf *Metasploit) Login() error {
    ctx := &loginReq{
        Method:   "auth.login",
        Username: msf.user,
        Password: msf.pass,
    }

    var res loginRes
    if err := msf.send(ctx, &res); err != nil {
        return err
    }

    msf.token = res.Token
    return nil
}

func (msf *Metasploit) Logout() error {
    ctx := &logoutReq{
        Method:      "auth.logout",
        Token:       msf.token,
        LogoutToken: msf.token,
    }

    var res logoutRes
    if err := msf.send(ctx, &res); err != nil {
        return err
    }

    msf.token = ""
    return nil
}

func (msf *Metasploit) SessionList() (map[uint32]SessionListRes, error) {
    req := &SessionListReq{Method: "session.list", Token: msf.token}
    res := make(map[uint32]SessionListRes)
    if err := msf.send(req, &res); err != nil {
        return nil, err
    }

    for id, session := range res {
        session.ID = id
        res[id] = session
    }

    return res, nil
}
```

**Liste 3-17: Metasploit API çağrılarının implementasyonu (`/ch-3/metasploit-minimal/rpc/msf.go`)**

Üç metot tanımlıyorsunuz: `Login()`, `Logout()` ve `SessionList()`. Her metot aynı genel akışı kullanır: bir istek `struct`’u oluşturup ilklendirmek, yanıt `struct`’unu oluşturmak ve isteği gönderip çözümlenmiş yanıtı almak için yardımcı fonksiyonu (`send()`) çağırmak. `Login()` ve `Logout()` metotları `token` özelliğini değiştirir. Metot mantığı arasındaki tek önemli fark, `SessionList()` metodunda görülür; burada yanıtı `map[uint32]SessionListRes` olarak tanımlar ve bu yanıtta döngüye girerek `map`’i düzleştirirsiniz; `struct` üzerindeki `ID` özelliğini ayarlarsınız, böylece `map` içinde `map` tutmak yerine tek katmanlı bir yapı kullanırsınız.

`session.list()` RPC fonksiyonunun geçerli bir kimlik doğrulama belirteci gerektirdiğini unutmayın; bu da `SessionList()` metot çağrısından önce oturum açmanız gerektiği anlamına gelir. Liste 3-18’de, henüz geçerli olmayan (boş bir string olan) bir belirtece erişmek için `Metasploit` alıcı `struct`’ının kullanıldığını göreceksiniz. Burada geliştirdiğiniz kod tam özellikli olmadığından, `SessionList()` metodunun içinden `Login()` metodunu açıkça çağırabilirsiniz; ancak implementasyonunu yaptığınız her ek kimlik doğrulamalı metot için, geçerli bir kimlik doğrulama belirteci olup olmadığını kontrol etmeli ve açıkça `Login` çağrısı yapmalısınız. Bu, iyi bir kodlama pratiği değildir; çünkü böyle yaparsanız, örneğin bir başlatma (bootstrapping) sürecinin parçası olarak yazabileceğiniz mantığı tekrar tekrar yazmakla çok fazla zaman harcarsınız.
