```json
=> {
    "type" => "shell",
    "tunnel local" => "192 168 35 149'44444",
    "tunnel_peer" => "192.168.35.149:43886",
    "via_exploit" => "exploit/multi/handler",
    "via_payload" => "payload/windows/shell_reverse_tcp",
    "desc" => "Command shell",
    "info" => "",
    "workspace" => "Projecti",
    "target_host" => "",
    "username" => "root",
    "uuid" => "hjahs9kw",
    "exploit_uuid" => "gcprpj2a",
    "routes" => [ ]
}
```

Bu yanıt bir `map` olarak döndürülür: Meterpreter oturum tanımlayıcıları anahtar (key), oturum detayları ise değer (value) olarak kullanılır.

Şimdi hem istek hem de yanıt verilerini ele almak için Go tiplerini oluşturalım. Liste 3-13, `sessionListReq` ve `SessionListRes` tanımlarını gösterir.

```go
type sessionListReq struct {
    _msgpack struct{} `msgpack:",asArray"`
    Method   string
    Token    string
}

type SessionListRes struct {
    ID          uint32 `msgpack:",omitempty"`
    Type        string `msgpack:"type"`
    TunnelLocal string `msgpack:"tunnel_local"`
    TunnelPeer  string `msgpack:"tunnel_peer"`
    ViaExploit  string `msgpack:"via_exploit"`
    ViaPayload  string `msgpack:"via_payload"`
    Description string `msgpack:"desc"`
    Info        string `msgpack:"info"`
    Workspace   string `msgpack:"workspace"`
    SessionHost string `msgpack:"session_host"`
    SessionPort int    `msgpack:"session_port"`
    Username    string `msgpack:"username"`
    UUID        string `msgpack:"uuid"`
    ExploitUUID string `msgpack:"exploit_uuid"`
}
```

**Liste 3-13: Metasploit oturum listeleme tip tanımları (`/ch-3/metasploit-minimal/rpc/msf.go`)**

İstek tipi `sessionListReq`'i, Metasploit RPC sunucusunun beklediği biçimle tutarlı olacak şekilde, yapılandırılmış veriyi MessagePack formatına serileştirmek için kullanırsın; özellikle de bir metot adı ve token değeriyle. Bu alanlar için herhangi bir tanımlayıcı (descriptor) olmadığını fark et. Veri bir `map` olarak değil, bir dizi (array) olarak geçirilir; yani RPC arayüzü veriyi anahtar/değer biçiminde beklemek yerine, konumsal (positional) bir dizi olarak bekler. Bu nedenle bu özellikler için açıklama (annotation) eklemezsin; anahtar adlarını tanımlamaya gerek yoktur. Ancak varsayılan olarak bir `struct`, alan adlarından türetilmiş anahtarlarla bir `map` olarak kodlanır. Bunu devre dışı bırakmak ve zorla konumsal bir dizi olarak kodlatmak için `_msgpack` adında özel bir alan ekler, `asArray` tanımlayıcısını kullanarak kodlayıcı/çözücüye veriyi dizi olarak ele alması gerektiğini açıkça belirtirsin.

`SessionListRes` tipi, yanıt alanlarıyla struct özellikleri arasında bire bir eşleme içerir. Önceki örnek yanıtta gösterilen veri özünde iç içe geçmiş bir `map`'tir. Dış `map`, oturum tanımlayıcılarını oturum ayrıntılarına eşlerken, iç `map` oturum ayrıntılarını anahtar/değer çiftleri olarak temsil eder. İstekten farklı olarak yanıt, konumsal bir dizi olarak yapılandırılmamıştır; ancak struct içindeki her bir özellik, veriyi Metasploit’in temsilinden alıp ona yazarken isimlendirmek ve eşlemek için tanımlayıcılar kullanır. Kod, oturum tanımlayıcısını struct üzerinde bir özellik olarak içerir. Ancak tanımlayıcının gerçek değeri anahtar değeri olduğundan, bu alan biraz farklı bir şekilde doldurulacaktır; bu nedenle veriyi isteğe bağlı yapmak, dolayısıyla kodlama ya da çözmeyi etkilememesi için `omitempty` tanımlayıcısını eklersin. Bu yaklaşım veriyi düzleştirir (flatten), böylece iç içe geçmiş `map`'lerle uğraşmak zorunda kalmazsın.

## Geçerli Bir Token Alma

Şu anda yalnızca tek bir eksik nokta kaldı. İstek için kullanacağın geçerli bir token değeri alman gerekiyor. Bunu yapmak için `auth.login()` API metoduna bir giriş (login) isteği göndereceksin; bu metot aşağıdaki formatı bekler:

```text
["auth.login", "username", "password"]
```

Buradaki `username` ve `password` değerlerini, başlangıç kurulumunda Metasploit içinde `msfrpc` modülünü yüklerken kullandığın değerlerle (hatırlarsan bunları ortam değişkeni olarak ayarlamıştın) değiştirmen gerekir. Kimlik doğrulama başarılı olursa, sunucu aşağıdaki mesajla yanıt verir; bu mesaj, sonraki isteklerde kullanabileceğin bir kimlik doğrulama token’ı içerir.

```json
{ "result" => "success", "token" => "alaialaiaialaial" }
```

Kimlik doğrulama başarısız olursa aşağıdaki yanıt üretilir:

```json
"error" => true,
"error_class" => "Msf::RPC::Exception",
"error_message" => "Invalid User ID or Password"
```

Ek olarak, token’ı oturum kapatarak (logout) geçersiz kılacak bir işlevsellik de oluşturalım. İstek, metot adını, kimlik doğrulama token’ını ve bu senaryoda ihtiyaç duymadığın üçüncü bir isteğe bağlı parametreyi alır:

```text
["auth.logout", "token", "logoutToken"]
```

Başarılı bir yanıt şu şekilde görünür:

```json
{ "result" => "success" }
```

## İstek ve Yanıt Metatiplerini Tanımlama

`tSession.list()` metodunun istek ve yanıtları için Go tiplerini nasıl yapılandırdıysan, aynı şeyi `auth.login()` ve `auth.logout()` için de yapman gerekir (bkz. Liste 3-14). Daha öncekiyle aynı gerekçeler geçerlidir: isteklerin dizi olarak serileştirilmesini zorlamak ve yanıtların `map` olarak ele alınması için tanımlayıcılar kullanmak:

```go
type loginReq struct {
    _msgpack struct{} `msgpack:",asArray"`
    Method   string
    Username string
    Password string
}

type loginRes struct {
    Result       string `msgpack:"result"`
    Token        string `msgpack:"token"`
    Error        bool   `msgpack:"error"`
    ErrorClass   string `msgpack:"error_class"`
    ErrorMessage string `msgpack:"error_message"`
}

type logoutReq struct {
    _msgpack    struct{} `msgpack:",asArray"`
    Method      string
    Token       string
    LogoutToken string
}

type logoutRes struct {
    Result string `msgpack:"result"`
}
```

**Liste 3-14: Giriş (login) ve çıkış (logout) için Metasploit tip tanımları (`/ch-3/metasploit-minimal/rpc/msf.go`)**

Go’nun, login yanıtını alanları dinamik olarak doldurarak serileştirdiğini belirtmeye değer: yalnızca mevcut alanlar doldurulur. Bu da hem başarılı hem de başarısız girişleri tek bir struct formatıyla temsil edebileceğin anlamına gelir.
