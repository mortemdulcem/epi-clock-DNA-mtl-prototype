### Temel Kriptografi Kavramlarını Gözden Geçirme

Go'da kriptoyu incelemeden önce, birkaç temel kriptografi kavramından bahsedelim. Uykunun derinliklerine düşmemeniz için bunu kısa tutacağız.

Öncelikle, şifreleme (özellikle gizliliği koruma amacıyla) kriptografinin görevlerinden yalnızca biridir. Genel olarak şifreleme, veriyi karıştırmanıza ve ardından başlangıçtaki girdiyi geri elde etmek için bu karıştırmayı çözmenize olanak tanıyan iki yönlü bir fonksiyondur. Veriyi şifreleme işlemi, veri çözülene kadar onu anlamsız hale getirir.

Hem şifreleme hem de şifre çözme, veriyi ve ona eşlik eden bir anahtarı kriptografik bir fonksiyona vermeyi içerir. Fonksiyon, ya şifrelenmiş veriyi (ciphertext) ya da orijinal, okunabilir veriyi (cleartext) çıktı olarak üretir. Bunu yapan çeşitli algoritmalar vardır. Simetrik algoritmalar, şifreleme ve şifre çözme işlemleri sırasında aynı anahtarı kullanırken, asimetrik algoritmalar şifreleme ve şifre çözme için farklı anahtarlar kullanır. Şifrelemeyi, aktarım halindeki veriyi korumak için veya kredi kartı numaraları gibi hassas bilgileri daha sonra, örneğin gelecekteki bir satın alma sırasında kolaylık sağlamak ya da sahtekarlık takibi için çözmek üzere saklamak için kullanabilirsiniz.

Öte yandan, özetleme (hashing), veriyi matematiksel olarak karıştırmaya yönelik tek yönlü bir süreçtir. Hassas bilgileri sabit uzunlukta bir çıktı üretmek için bir hashing fonksiyonuna verebilirsiniz. SHA-2 ailesindeki gibi güçlü algoritmalarla çalışırken, farklı girdilerin aynı çıktıyı üretme olasılığı son derece düşüktür. Yani çakışma (collision) olasılığı düşüktür. Tersine çevrilemez oldukları için hash'ler, veritabanında cleartext parolalar saklamaya alternatif olarak veya verinin değiştirilip değiştirilmediğini anlamak için bütünlük (integrity) kontrolü yapmada yaygın olarak kullanılır. Eğer iki özdeş girdi için çıktıları gizlemek veya rastgeleleştirmek istiyorsanız, hashing sürecinde iki özdeş girdiyi birbirinden ayırmak için kullanılan rastgele bir değer olan salt kullanırsınız. Salt'lar parola saklama için yaygındır; çünkü tesadüfen aynı parolayı kullanan birden fazla kullanıcının yine de farklı hash değerlerine sahip olmasını sağlarlar.

Kriptografi ayrıca mesajları doğrulamak (authenticate etmek) için de bir araç sağlar. Mesaj doğrulama kodu (MAC, message authentication code), özel bir tek yönlü kriptografik fonksiyondan üretilen çıktıdır. Bu fonksiyon, verinin kendisini, bir gizli anahtarı ve bir initialization vector'ü tüketir ve çakışma olasılığı düşük bir çıktı üretir. Bir mesajın göndericisi, MAC üretmek için bu fonksiyonu çalıştırır ve ardından MAC'i mesajın bir parçası olarak ekler. Alıcı, MAC'i yerel olarak hesaplar ve aldığı MAC ile karşılaştırır. Eşleşme, göndericinin doğru gizli anahtara sahip olduğunu (yani göndericinin gerçek/kimlik doğrulanmış olduğunu) ve mesajın değişmediğini (bütünlüğünün korunduğunu) gösterir.

Artık bu bölümün içeriğini anlayacak kadar kriptografi bilgisine sahipsiniz. Gerekli yerlerde, ilgili konuya yönelik daha fazla detayı tartışacağız. Go'nun standart `crypto` kütüphanesine bakarak başlayalım.

### Standart Crypto Kütüphanesini Anlama

Go'da kriptoyu uygulamaya koymanın güzel yanlarından biri, muhtemelen kullanacağınız kriptografik özelliklerin çoğunun standart kütüphanenin bir parçası olmasıdır. Diğer diller yaygın olarak OpenSSL veya başka üçüncü taraf kütüphanelere dayanırken, Go'nun kripto özellikleri resmi depoların bir parçasıdır. Bu da kriptoyu uygulamayı nispeten basit hale getirir; çünkü geliştirme ortamınızı kirletecek hantal bağımlılıkları kurmak zorunda kalmazsınız. İki ayrı depo vardır.

Kendi içinde yeterli `crypto` paketi, en yaygın kriptografik görevler ve algoritmalar için kullanılan çeşitli alt paketler içerir. Örneğin, simetrik anahtarlı algoritmaları uygulamak için `aes`, `des` ve `rc4` alt paketlerini; asimetrik şifreleme için `dsa` ve `rsa` alt paketlerini; hashing için `md5`, `sha1`, `sha256` ve `sha512` alt paketlerini kullanabilirsiniz. Bu, kapsamlı bir liste değildir; başka kripto fonksiyonları için de ek alt paketler bulunmaktadır.

Standart `crypto` paketine ek olarak Go, çeşitli ek kripto işlevselliğini içeren resmi, genişletilmiş bir pakete sahiptir: `golang.org/x/crypto`. Bunun içindeki işlevsellik, ek hashing algoritmaları, şifreleme cipher'ları ve yardımcı araçlar içerir. Örneğin, paket; parolalar ve hassas veriler için daha iyi, daha güvenli bir hashing alternatifi olan `bcrypt` alt paketini, geçerli sertifikalar üretmek için `acme/autocert` paketini ve SSH protokolü üzerinden iletişimi kolaylaştırmak için SSH alt paketlerini içerir.

Yerleşik `crypto` paketi ile ek `golang.org/x/crypto` paketleri arasındaki tek gerçek fark, `crypto` paketinin daha katı uyumluluk gereksinimlerine uymasıdır. Ayrıca, herhangi bir `golang.org/x/crypto` alt paketini kullanmak isterseniz, önce aşağıdakini girerek paketi kurmanız gerekir:

```bash
$ go get -u golang.org/x/crypto/...
```

Resmi Go `crypto` paketlerinin içerisindeki tüm işlevsellik ve alt paketlerin tam listesi için, resmi dokümantasyona `https://golang.org/pkg/crypto/` ve `https://godoc.org/golang.org/x/crypto/` adreslerinden bakabilirsiniz.

Sonraki bölümler çeşitli kripto uygulamalarına dalacak. Go'nun `crypto` işlevselliğini kullanarak parola hash'lerini kırmak, statik bir anahtar kullanarak hassas verileri çözmek ve zayıf şifreleme cipher'larını kaba kuvvet (brute-force) ile kırmak gibi bazı kötü niyetli işleri nasıl yapacağınızı göreceksiniz. Ayrıca, TLS kullanarak aktarım halindeki iletişiminizi koruyan, verinin bütünlüğünü ve özgünlüğünü (authenticity) kontrol eden ve karşılıklı kimlik doğrulama (mutual authentication) yapan araçlar oluşturmak için de bu işlevselliği kullanacaksınız.
