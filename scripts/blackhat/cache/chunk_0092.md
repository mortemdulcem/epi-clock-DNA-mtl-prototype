Go'nun `crypto/hmac` paketini kullanarak bu soruları ele alabilirsiniz; bu paket, Anahtarlı-Özet Mesaj Doğrulama Kodu (HMAC – Keyed-Hash Message Authentication Code) standardını uygular. HMAC, mesaj üzerinde oynama yapılıp yapılmadığını kontrol etmemizi ve kaynağın kimliğini doğrulamamızı sağlayan kriptografik bir algoritmadır. Bir karma (hash) fonksiyonu kullanır ve yalnızca geçerli mesajlar ya da veriler üretmeye yetkili tarafların elinde olması gereken paylaşılan bir gizli anahtar tüketir. Bu gizli anahtara sahip olmayan bir saldırgan, makul ölçüde geçerli bir HMAC değeri taklit edemez (forge).

Bazı programlama dillerinde HMAC’i uygulamak biraz zorlayıcı olabilir. Örneğin bazı diller, alınan ve hesaplanan hash değerlerini bayt bayt manuel olarak karşılaştırmanızı zorunlu kılar. Geliştiriciler, bayt bayt karşılaştırma işlemini erken sonlandırırlarsa, istemeden zamanlama farklılıkları yaratabilir; bir saldırgan, mesaj işleme sürelerini ölçerek beklenen HMAC’i çıkarımlayabilir. Buna ek olarak, geliştiriciler zaman zaman HMAC’lerin (bir mesaj ve anahtar tüketir) mesajın başına gizli bir anahtar eklenmiş bir hash ile aynı şey olduğunu düşünür. Ancak HMAC’in içsel işleyişi, saf bir hash fonksiyonunun işleyişinden farklıdır. HMAC’i açıkça kullanmayarak, geliştirici uygulamayı, bir saldırganın bir mesajı ve geçerli bir MAC’i taklit ettiği uzunluk-genişletme (length-extension) saldırılarına maruz bırakır.

Neyse ki biz Gopher’lar için `crypto/hmac` paketi, HMAC işlevselliğini güvenli bir şekilde uygulamayı oldukça kolaylaştırır. Bir uygulamaya bakalım. Aşağıdaki programın tipik bir kullanım senaryosundan çok daha basit olduğuna dikkat edin; tipik bir kullanım, muhtemelen bir tür ağ haberleşmesi ve mesajlaşma içerir. Çoğu durumda, HMAC’i HTTP istek parametreleri ya da ağ üzerinden iletilen başka tür bir mesaj üzerinde hesaplayacaksınız. Liste 11-3’te gösterilen örnekte, istemci-sunucu iletişimini atlıyor ve yalnızca HMAC işlevselliğine odaklanıyoruz.

```go
var key = []byte("some random key")

func checkMAC(message, recvMAC []byte) bool {
    mac := hmac.New(sha256.New, key)
    mac.Write(message)
    calcMAC := mac.Sum(nil)

    return hmac.Equal(calcMAC, recvMAC)
}

func main() {
    // Gerçek uygulamalarda, mesajı ve MAC değerini bir ağ kaynağından okuruz
    message := []byte("The red eagle flies at 10:00")
    mac, _ := hex.DecodeString("69d2c7b6fbbfcaebf2a3172f4662601dfd1acf b46339639ac9c10c8da64631d")
    if checkMAC(message, mac) {
        fmt.Println("EQUAL")
    } else {
        fmt.Println("NOT EQUAL")
    }
}
```

**Liste 11-3: Mesaj doğrulama için HMAC kullanma (`ch-11/hmac/main.go`)**

Program, HMAC kriptografik fonksiyonunuz için kullanacağınız anahtarı tanımlayarak başlar ❶. Burada değeri kod içine gömüyorsunuz (hardcode), ancak gerçek bir uygulamada bu anahtar yeterince korunmuş ve rastgele olurdu. Ayrıca uç noktalar arasında paylaşılırdı; yani hem mesaj gönderici hem de alıcı aynı anahtar değerini kullanıyor olurdu. Burada tam bir istemci-sunucu işlevselliği uygulamadığınız için, bu değişkeni sanki yeterince paylaşılmış bir anahtarmış gibi kullanacaksınız.

Sonra, bir mesaj ve alınan HMAC’i parametre olarak kabul eden `checkMAC()` ❷ adında bir fonksiyon tanımlıyorsunuz. Mesaj alıcısı, kendisine gelen MAC değerinin, yerel olarak hesapladığı değerle eşleşip eşleşmediğini kontrol etmek için bu fonksiyonu çağırır. İlk olarak `hmac.New()` ❸ fonksiyonunu çağırıyorsunuz; buna, bir `hash.Hash` örneği döndüren `sha256.New` fonksiyonunu ve paylaşılan gizli anahtarı geçiriyorsunuz. Bu durumda `hmac.New()` fonksiyonu, HMAC’inizi SHA-256 algoritmasını ve gizli anahtarınızı kullanarak başlatır ve sonucu `mac` adlı değişkene atar. Ardından, tıpkı önceki hashing örneklerinde yaptığınız gibi HMAC hash değerini hesaplamak için bu değişkeni kullanırsınız. Burada sırasıyla `mac.Write(message)` ve `mac.Sum(nil)` çağrılarını yaparsınız. Sonuç, yerel olarak hesaplanmış HMAC’inizdir ve `calcMAC` adlı değişkende saklanır.

Bir sonraki adım, yerel olarak hesaplanan HMAC değerinizin, aldığınız HMAC değeriyle eşit olup olmadığını değerlendirmektir. Bunu güvenli bir şekilde yapmak için `hmac.Equal(calcMAC, recvMAC)` ❹ fonksiyonunu çağırırsınız. Pek çok geliştirici, bayt dilimlerini `bytes.Compare(calcMAC, recvMAC)` çağrısıyla karşılaştırma eğiliminde olur. Sorun şu ki `bytes.Compare()` sözlüksel (lexicographical) bir karşılaştırma yapar; verilen dilimlerin her bir öğesini, bir fark bulana ya da dilimlerden birinin sonuna ulaşana kadar yürür ve karşılaştırır. Bu karşılaştırmayı tamamlamanın süresi, `bytes.Compare()` fonksiyonunun bir farkı ilk öğede mi, son öğede mi yoksa arada bir yerde mi bulduğuna bağlı olarak değişir. Bir saldırgan, bu süre varyasyonlarını ölçerek beklenen HMAC değerini belirleyebilir ve meşru şekilde işlenen bir isteği taklit edebilir. `hmac.Equal()` fonksiyonu, dilimleri neredeyse sabit ölçülebilir süreler üretecek şekilde karşılaştırarak bu sorunu çözer. Fonksiyonun farkı nerede bulduğunun bir önemi yoktur; çünkü işlem süreleri önemsiz düzeyde değişir ve belirgin ya da algılanabilir bir desen üretmez.

`main()` fonksiyonu, bir istemciden mesaj alma sürecini simüle eder. Gerçekte bir mesaj alıyor olsaydınız, HMAC ve mesaj değerlerini iletimden okuyup ayrıştırmanız gerekirdi. Bu sadece bir simülasyon olduğundan, bunun yerine alınan mesajı ❺ ve alınan HMAC’i ❻ sabit olarak kod içine yazıyor, HMAC hex string’ini bir `[]byte` ile temsil edilecek şekilde decode ediyorsunuz. Bir `if` ifadesi kullanarak `checkMAC()` fonksiyonunuzu ❼ çağırıyor, ona alınan mesajı ve HMAC’i geçiriyorsunuz. Daha önce açıklandığı gibi `checkMAC()` fonksiyonunuz alınan mesajı ve paylaşılan gizli anahtarı kullanarak bir HMAC hesaplar ve alınan HMAC ile hesaplanan HMAC’in eşleşip eşleşmediğine ilişkin bir `bool` değeri döndürür.

HMAC, her ne kadar hem kimlik doğrulaması (authenticity) hem de bütünlük (integrity) güvencesi sağlasa da gizliliği (confidentiality) garanti etmez. Mesajın, yetkisiz kaynaklar tarafından görülmediğinden emin olamazsınız. Bir sonraki bölüm, çeşitli şifreleme (encryption) türlerini inceleyerek ve uygulayarak bu kaygıyı ele alır.
