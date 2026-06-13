## Verilerin Şifrelenmesi

Şifreleme muhtemelen en bilinen kriptografi kavramıdır. Sonuçta, gizlilik ve veri koruması, genellikle kuruluşların kullanıcı parolalarını ve diğer hassas verileri şifrelenmemiş biçimlerde saklaması nedeniyle ortaya çıkan, yüksek profilli veri ihlalleri sayesinde önemli ölçüde medya ilgisi görmüştür. Medya ilgisi olmasa bile, şifreleme kara şapkalı saldırganların ve geliştiricilerin ilgisini çekmelidir. Temel süreci ve uygulamayı anlamak, kârlı bir veri ihlali ile saldırı öldürme zincirinde (kill chain) sinir bozucu bir kesinti arasındaki fark olabilir. Aşağıdaki bölüm, şifrelemenin farklı biçimlerini ve her biri için faydalı uygulama ile kullanım örneklerini sunar.

### Simetrik Anahtarlı Şifreleme

Şifrelemeye girişiniz, muhtemelen en sade biçimi olan simetrik anahtarlı şifreleme ile başlayacak. Bu biçimde, hem şifreleme hem de şifre çözme fonksiyonları aynı gizli anahtarı kullanır. Go, varsayılan veya genişletilmiş paketlerinde en yaygın algoritmaların çoğunu desteklediği için simetrik kriptografiyi oldukça basit hale getirir.

Kısalık adına, simetrik anahtarlı şifrelemeye dair tartışmamızı tek bir pratik örnekle sınırlandıracağız. Bir kuruluşa sızdığınızı hayal edin. Yetki yükseltme (privilege escalation), yatay hareket (lateral movement) ve ağ keşfi (network recon) için gerekli adımları tamamladınız ve bir e-ticaret web sunucusuna ve arka uç veritabanına erişim elde ettiniz. Veritabanı finansal işlemler barındırıyor; ancak bu işlemlerde kullanılan kredi kartı numarası doğal olarak şifrelenmiş durumda. Web sunucusundaki uygulama kaynak kodunu inceliyor ve kuruluşun Gelişmiş Şifreleme Standardı (Advanced Encryption Standard, AES) şifreleme algoritmasını kullandığını belirliyorsunuz. AES, her biri biraz farklı hususlara ve uygulama ayrıntılarına sahip birden fazla çalışma kipini (mode) destekler. Kipler birbirlerinin yerine kullanılamaz; şifre çözme için kullanılan kip, şifreleme için kullanılan kip ile aynı olmalıdır.

Bu senaryoda, uygulamanın AES’i Cipher Block Chaining (CBC) kipinde kullandığını belirlediğinizi varsayalım. Öyleyse, bu kredi kartlarının şifresini çözen bir fonksiyon yazalım (Liste 11-4). Simetrik anahtarın uygulama içinde sabit kodlanmış (hardcoded) veya bir yapılandırma dosyasında statik olarak ayarlanmış olduğunu varsayalım. Bu örnek üzerinde ilerlerken, bu uygulamayı diğer algoritmalar veya şifreler (cipher) için uyarlamanız gerekeceğini unutmayın; ancak bu iyi bir başlangıç noktasıdır.

```go
func unpad(buf []byte) []byte { 0
    // Assume valid length and padding. Should add checks
    padding := int(buf[len(buf)-1])
    return buf[:len(buf)-padding]
1

func decrypt(ciphertext, key []byte) ([]byte, error) { 49
    var (
        plaintext []byte
        iv        []byte
        block     cipher.Block
        mode      cipher. BlockMode

242    Chapter 11
         err       error

    if len(ciphertext) < aes.BlockSize { 0
         return nil, errors.New("Invalid ciphertext length: too short")

    if len(ciphertext)%aes.BlockSize I. 0 {
         return nil, errors.New("Invalid ciphertext length: not a multiple of blocksize")

    iv = ciphertext[:aes.BlockSize]
    ciphertext = ciphertext[aes.BlockSize:]

    if block, err = aes.NewCipher(key); err 1= nil { 0
         return nil, err

    mode = cipher.NewCBCDecrypter(block, iv) 0
    plaintext = make(Mbyte, len(ciphertext))
    mode.CryptBlocks(plaintext, ciphertext) 0
    plaintext = unpad(plaintext)

    return plaintext, nil
```

**Liste 11-4:** AES doldurma (padding) ve şifre çözme (`ch-11/aes/main.go`)

Kod iki fonksiyon tanımlar: `unpad()` ve `decrypt()`. `unpad()` fonksiyonu 0, şifre çözmeden sonra doldurma (padding) verisinin kaldırılmasını ele almak için alelacele bir araya getirilmiş bir yardımcı (utility) fonksiyondur. Bu gerekli bir adımdır, ancak bu tartışmanın kapsamı dışındadır. Daha fazla bilgi için Public Key Cryptography Standards (PKCS) #7 doldurma (padding) hakkında araştırma yapın. Bu konu AES için önemlidir, çünkü verilerimizin doğru blok hizalamasına sahip olmasını sağlamak için kullanılır. Bu örnek için, yalnızca verinizi temizlemek için bu fonksiyona daha sonra ihtiyaç duyacağınızı bilmeniz yeterlidir. Fonksiyonun kendisi, gerçek dünya senaryosunda açıkça doğrulamak isteyeceğiniz bazı varsayımlarda bulunur. Özellikle, doldurma baytlarının değerinin geçerli olduğunu, slice sınırlarının (offset) geçerli olduğunu ve sonucun uygun uzunlukta olduğunu doğrulamak isterdiniz.

En ilginç mantık `decrypt()` fonksiyonu 0 içinde yer alır; bu fonksiyon iki bayt slice’ı alır: şifresini çözmeniz gereken `ciphertext` ve bunu yapmak için kullanacağınız simetrik `key`. Fonksiyon, şifreli metnin en azından blok boyutunuz kadar uzun olduğunu doğrulamak için bazı kontroller yapar 0. Bu gerekli bir adımdır, çünkü CBC kipinde şifreleme rastgelelik için bir başlangıç vektörü (initialization vector, IV) kullanır. Parola karması için tuz (salt) değeri gibi, bu IV’nin gizli kalması gerekmez. Bir AES bloğuyla aynı uzunlukta olan IV, şifreleme sırasında şifreli metninizin başına eklenir. Eğer şifreli metnin uzunluğu beklenen blok boyutundan kısa ise, ya şifreli metinde bir sorun olduğunu ya da IV’nin eksik olduğunu bilirsiniz. Ayrıca şifreli metnin uzunluğunun AES blok boyutunun bir katı olup olmadığını da kontrol edersiniz 0. Eğer değilse, şifre çözme feci biçimde başarısız olur, çünkü CBC kipi şifreli metin uzunluğunun blok boyutunun katı olmasını bekler.
