Artık karşılıklı kimlik doğrulamasının çalışan bir örneğine sahipsiniz. Anlayışınızı daha da güçlendirmek için, önceki örnekleri TCP soketleri üzerinde çalışacak şekilde değiştirmenizi öneriyoruz.

Sonraki bölümde, çabalarınızı daha sinsi bir amaca adayacaksınız: RC2 şifreleme algoritmasının simetrik anahtarlarını kaba kuvvet (brute force) yöntemiyle kırmak.

## RC2'yi Kaba Kuvvetle Kırmak

RC2, Ron Rivest tarafından 1987 yılında yaratılmış simetrik anahtarlı bir blok şifrelemedir. Hükümetten gelen tavsiyeler doğrultusunda, tasarımcılar 40 bitlik bir şifreleme anahtarı kullanmışlardır; bu da şifreyi, ABD hükümetinin anahtarı kaba kuvvetle kırıp haberleşmeleri çözebileceği kadar zayıf kılmıştır. Çoğu iletişim için yeterli mahremiyet sağlarken, hükümete örneğin yabancı taraflarla yapılan yazışmalara göz atma imkânı tanıyordu. Elbette 1980'lerde, anahtarı kaba kuvvetle kırmak ciddi hesaplama gücü gerektiriyordu ve yalnızca iyi fonlanan ulus devletler veya özel kurumlar bunu makul sürede gerçekleştirebiliyordu. 30 yıl ileri sararsak; bugün sıradan bir ev bilgisayarı bile 40 bitlik bir anahtarı birkaç gün ya da hafta içerisinde kaba kuvvetle kırabilir.

O halde, ne duruyoruz, hadi 40 bitlik bir anahtarı kaba kuvvetle kıralım.

### Başlarken

Koda dalmadan önce sahneyi hazırlayalım. Öncelikle, ne standart ne de genişletilmiş Go kriptografi kütüphanelerinde, genel kullanıma yönelik bir RC2 paketi bulunmuyor. Ancak, bunun için Go içinde dahili (internal) bir paket var. Dahili paketleri harici programlarda doğrudan `import` edemezsiniz; bu yüzden onu kullanmak için başka bir yol bulmanız gerekecek.

İkinci olarak, işleri basit tutmak için normalde yapmak istemeyeceğiniz bazı varsayımlar yapacaksınız. Özellikle, açık metin (cleartext) verinizin uzunluğunun RC2 blok boyutunun (8 bayt) tam katı olduğunu varsayacaksınız; böylece PKCS #5 dolgu (padding) işlemesini yönetmek gibi idari görevlerle mantığınızı bulandırmamış olursunuz. Dolguyu ele almak, bu bölümde daha önce AES ile yaptığınıza benzer (bkz. Liste 11-4), ancak üzerinde çalışacağınız verinin bütünlüğünü korumak için içeriği doğrulama konusunda daha dikkatli olmanız gerekir. Ayrıca, şifreli metninizin bir kredi kartı numarası olduğunu varsayacaksınız. Olası anahtarları, ortaya çıkan açık metin verisini doğrulayarak kontrol edeceksiniz. Bu durumda veriyi doğrulamak, metnin sayısal olduğundan emin olmayı ve ardından onu bir Luhn kontrolüne tabi tutmayı içerir; bu yöntem, kredi kartı numaralarını ve diğer hassas verileri doğrulamak için kullanılır.

Sonraki varsayımınız, dosya sistemi verilerini veya kaynak kodu karıştırarak — ya da başka bir şekilde — verinin 40 bitlik bir anahtarla, ECB kipinde (mode) ve başlangıç vektörü (initialization vector) olmadan şifrelendiğini belirleyebildiğiniz yönünde olacak. RC2 değişken uzunluklu anahtarları destekler ve bir blok şifre olduğu için farklı kiplerde çalışabilir. En basit kip olan ECB kipinde, veri blokları birbirlerinden bağımsız şekilde şifrelenir. Bu da mantığınızı biraz daha basitleştirecek.

Son olarak, isterseniz eşzamanlı olmayan (nonconcurrent) bir uygulamada da anahtarı kırabilirsiniz, ancak eşzamanlı (concurrent) bir uygulama performans açısından çok daha iyi olacaktır. Bunu adım adım, önce eşzamanlı olmayan bir sürüm, sonra eşzamanlı bir sürüm göstererek inşa etmek yerine, doğrudan eşzamanlı derlemeye geçeceğiz.

Şimdi birkaç önkoşulu kuracaksınız. Önce, resmi RC2 Go uygulamasını `https://github.cotn/golang/cryptilblob/master/frkcs12/internalfrc2/rc2.go` adresinden edinin. Bunu yerel çalışma alanınıza (workspace) kurmanız gerekecek ki brute force aracınıza `import` edebilesiniz. Daha önce belirttiğimiz gibi, bu paket bir dahili (internal) paket, yani varsayılan olarak dış paketler onu `import` edip kullanamaz. Bu biraz hack sayılabilir, ama böylece üçüncü taraf bir uygulama kullanmak veya — tüyler ürpertici — kendi RC2 şifreleme kodunuzu yazmak zorunda kalmazsınız. Eğer bu dosyayı çalışma alanınıza kopyalarsanız, dışa aktarılmamış (unexported) fonksiyonlar ve tipler geliştirme paketinizin parçası hâline gelir ve bu da onları erişilebilir kılar.

Ayrıca, Luhn kontrolünü gerçekleştirmek için kullanacağınız bir paketi de kuralım:

```bash
$ go get github.com/joeljunstrom/go-luhn
```

Bir Luhn kontrolü, kredi kartı numaraları veya diğer kimlik verileri üzerinde, geçerli olup olmadıklarını belirlemek için sağlama toplamı (checksum) hesaplar. Bunun için mevcut paketi kullanacaksınız. İyi belgelenmiş ve tekerleği yeniden icat etmekten kurtaracak.

Artık kodunuzu yazabilirsiniz. 40 bitlik tüm anahtar uzayındaki her kombinasyonda döngüye girmeniz, her anahtarla şifreli metninizi çözmeniz ve sonucun yalnızca sayısal karakterlerden oluştuğunu ve bir Luhn kontrolünden geçtiğini doğrulayarak sonucu doğrulamanız gerekecek. Çalışmayı yönetmek için üretici/tüketici (producer/consumer) modelini kullanacaksınız — üretici bir anahtarı bir kanala (channel) itip, tüketiciler kanaldan anahtarı okuyacak ve buna göre çalışacak. İşin kendisi tek bir anahtar değerinden ibaret olacak. Doğru doğrulanmış açık metin üreten bir anahtar bulduğunuzda (yani bir kredi kartı numarası bulduğunuzu gösterdiğinde), her bir goroutine'in işini durdurması için sinyal göndereceksiniz.

Bu problemin ilginç zorluklarından biri, anahtar uzayında nasıl dolaşılacağıdır. Bizim çözümümüzde, anahtar uzayını `uint64` değerleriyle temsil ederek bir `for` döngüsüyle üzerinden geçiyorsunuz. Zorluk, `uint64`'ün bellekte 64 bit yer kaplaması. Dolayısıyla, bir `uint64`'ü 40 bitlik (5 baytlık) bir RC2 anahtarına dönüştürmek, gereksiz 24 biti (3 bayt) kırpmanızı gerektiriyor. Umarız kodu gördükten sonra bu süreç netleşir. Yavaş ilerleyip, programın bölümlerini parça parça ele alacağız. Liste 11-8 programı başlatıyor.

```go
import f
    "crypto/cipher"
    "encoding/binary"
    "encoding/hex"

    "log"
    "regexp"
    "sync"

    luhn "github.com/joeljunstrom/go-luhn"

    "github.com/blackhatgabhg/ch-11/rc2-brute/rc2 "

ID var numeric regexp.MustCompileCA\df8W)

0 type CryptoData struct f
    block cipher.Block
    key   []byte
```

**Liste 11-8:** RC2 brute force tipinin `import` edilmesi (`/ch-11/rc2-brute/main.go`)
