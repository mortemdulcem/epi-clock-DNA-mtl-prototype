```go
                       if err != nil {
                            log.Fatalln(err)
                       }
                       log.Printf("hash = %s\n", hash)

                       err = bcrypt.CompareHashAndPassword([]byte(storedHash), []byte(password))
                       if err != nil {
                           log.Println("[!] Authentication failed")
                           return
                       }

                       log.Println("[+] Authentication successful")
```

Liste 11-2: bcrypt özetlerini (hash) karşılaştırma (`/ch-11/bcrypt/main.go`)

Bu kitaptaki çoğu kod örneğinde `package` import'larını göstermedik. Bu örnekte ise özellikle ekledik; böylece standart kütüphane dışında bir Go paketi olan `golang.org/x/crypto/bcrypt` paketini kullandığınızı açıkça göstermiş oluyoruz, çünkü Go'nun yerleşik `crypto` paketi `bcrypt` işlevselliğini içermiyor. Daha sonra, önceden hesaplanmış ve kodlanmış bir `bcrypt` özeti tutan `storedHash` değişkenini başlatıyorsunuz. Bu yapay (contrived) bir örnek; örnek kodumuzu bir veritabanına bağlayıp değeri oradan almak yerine, gösterim amacıyla bir değeri doğrudan kod içine yazmayı tercih ettik. Bu değişken, örneğin bir ön uç web uygulamasında kullanıcı kimlik doğrulama bilgilerini saklayan bir veritabanı satırında bulduğunuz bir değeri temsil edebilir.

Sonraki adımda, açık metin bir parola değerinden `bcrypt` ile kodlanmış bir özet üreteceksiniz. `main` fonksiyonu, komut satırı argümanı olarak bir parola değeri okur ve ardından iki ayrı `bcrypt` fonksiyonunu çağırır. İlk fonksiyon olan `bcrypt.GenerateFromPassword()`, iki parametre kabul eder: açık metin parolayı temsil eden bir byte `slice` ve bir maliyet (cost) değeri. Bu örnekte, paketle gelen varsayılan maliyeti kullanmak için sabit `bcrypt.DefaultCost` değişkenini geçiriyorsunuz; bu değerin yazım zamanında 10 olduğunu belirtelim. Fonksiyon, kodlanmış özet (hash) değerini ve oluşan hataları döndürür.

İkinci çağırdığınız `bcrypt` fonksiyonu `bcrypt.CompareHashAndPassword()` fonksiyonudur; sizin yerinize, arka planda özet karşılaştırmasını yapar. `bcrypt` ile kodlanmış bir özet ve açık metin parolayı byte `slice`'ları olarak kabul eder. Fonksiyon, maliyeti ve tuzu (salt) belirlemek için kodlanmış özeti ayrıştırır. Daha sonra bu değerleri, açık metin parola ile birlikte kullanarak bir `bcrypt` özeti üretir. Ortaya çıkan bu özet, kodlanmış `storedHash` değerinden çıkarılan özetle eşleşirse, verilen parolanın `storedHash` değerini oluşturmak için kullanılan parolayla aynı olduğunu anlarsınız.

Bu, SHA ve MD5'e karşı parola kırma işlemlerini gerçekleştirirken kullandığınız yöntemle aynıdır: verilen bir parolayı özet fonksiyonundan geçirip sonucu saklı özetle karşılaştırırsınız. Burada, SHA ve MD5 için yaptığınız gibi üretilen özetleri doğrudan karşılaştırmak yerine, `bcrypt.CompareHashAndPassword()` fonksiyonunun bir hata döndürüp döndürmediğini kontrol edersiniz. Bir hata görürseniz, hesaplanan özetlerin —ve dolayısıyla bunları hesaplamak için kullanılan parolaların— eşleşmediğini anlarsınız.

Aşağıda iki örnek program çalıştırma çıktısı yer alıyor. İlki, yanlış bir parola için üretilen çıktıyı gösterir:

```bash
$ go run main.go someWrongPassword
2020/08/25 08:44:01 hash = $2a$10$YS5anG18ye/NC7GDyLBLU05gE/ng5119TnaBizTChWq5g9i09v0AC
2020/08/25 08:44:01 [!] Authentication failed
```

İkincisi, doğru parola için üretilen çıktıyı gösterir:

```bash
$ go run main.go someCOmpl3xP@sswOrd
2020/08/25 08:39:29 hash = $2a$10$XfeUk.wKeEePNAfjOjuXe8RaM/9EC1X2mqa]8M0B29hZRyuNxz.
2020/08/25 08:39:29 [+] Authentication successful
```

Detaylara dikkat eden okurlar, başarılı kimlik doğrulama için gösterilen özet değerinin, `storedHash` değişkeni için kod içine yazdığınız değerle eşleşmediğini fark etmiş olabilir. Kodunuzun iki ayrı fonksiyon çağırdığını hatırlayın. `GenerateFromPassword()` fonksiyonu, rastgele bir tuz (salt) değeri kullanarak kodlanmış bir özet üretir. Farklı tuzlar verildiğinde, aynı parola farklı özetler üretir. Farkın sebebi budur. `CompareHashAndPassword()` fonksiyonu ise özetleme algoritmasını, saklanan özetle aynı tuz ve maliyet değerlerini kullanarak yürütür; böylece ortaya çıkan özet, `storedHash` değişkenindekiyle birebir aynı olur.

## Mesajların Kimliğini Doğrulama

Şimdi odağımızı mesaj kimlik doğrulamaya çevirelim. Mesaj alışverişi yaparken, verinin bütünlüğünü ve uzaktaki servisin kimliğinin doğruluğunu (authenticity) doğrulamanız gerekir; böylece verinin gerçekten sahici olduğundan ve üzerinde oynama yapılmadığından emin olursunuz. Mesaj, iletim sırasında yetkisiz bir kaynak tarafından değiştirilmiş olabilir mi? Mesaj yetkili bir gönderen tarafından mı gönderildi yoksa başka bir varlık tarafından mı sahte (forged) olarak üretildi?
