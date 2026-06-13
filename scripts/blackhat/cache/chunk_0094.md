Uygulamalı ve Saldırı Odaklı Kriptografi                                                    243
Doğrulama kontrollerinizi tamamladığınızda, şifreli metni (ciphertext) çözmeye devam edebilirsiniz. Daha önce bahsedildiği gibi, IV şifreli metnin başına eklenmiştir, bu yüzden yapmanız gereken ilk şey IV'yi şifreli metinden çıkarmaktır ❶. `aes.BlockSize` sabitini kullanarak IV'yi alır ve ardından `ciphertext` değişkeninizi `ciphertext = [aes.BlockSize:]` ifadesiyle şifreli metninizin geri kalanını gösterecek şekilde yeniden tanımlarsınız. Artık şifrelenmiş veriniz IV'nizden ayrı durumdadır.
 
Sonra `aes.NewCipher()` fonksiyonunu çağırır ve ona simetrik anahtar değerinizi iletirsiniz ❷. Bu, AES blok modlu şifrenizi başlatır ve onu `block` adlı bir değişkene atar. Ardından AES şifrenize `cipher.NewCBCDecryptor(block, iv)` ❸ çağrısını yaparak CBC modunda çalışmasını söylersiniz. Sonucu `mode` adlı bir değişkene atarsınız. (`crypto/cipher` paketi, diğer AES modları için ek başlatma fonksiyonları içerir, fakat burada yalnızca CBC çözme (decryption) işlemi kullanıyorsunuz.) Daha sonra `mode.CryptBlocks(plaintext, ciphertext)` çağrısını yaparak `ciphertext` içeriğinin şifresini çözer ve sonucu `plaintext` byte `slice`'ına yazarsınız ❹. Son olarak, `unpad()` yardımcı fonksiyonunuzu çağırarak PKCS #7 dolgusunu kaldırırsınız ❺. Sonucu döndürürsünüz. Her şey yolunda gittiyse, bu sonuç kredi kartı numarasının düz metin (plaintext) değeri olmalıdır.
 
Programın örnek bir çalıştırması beklenen sonucu üretir:

```bash
$ go run main.go
key         = aca2d6b4765c04beafc3e483b296620d07c32db16029a52808fde98786646c8
ciphertext = 7ff4a8272d6b60f1e7cfc5d8f5bcd047395e31e5fc83d062716082010f637c8f 21150eabace62
--snip--
plaintext = 4321123456789090
```

Bu örnek kodda bir `main()` fonksiyonu tanımlamadığınıza dikkat edin. Neden? Çünkü, tanıdık olmadığınız ortamlarda verinin şifresini çözmek, çeşitli potansiyel incelikler ve değişkenlikler barındırır. Şifreli metin ve anahtar (key) değerleri kodlanmış mı yoksa ham (raw) ikili (binary) mi? Eğer kodlanmışsa, bir hex dizesi (string) mi yoksa Base64 mü? Veriye yerel olarak erişilebiliyor mu, yoksa veriyi bir veri kaynağından çıkarmanız veya örneğin bir donanım güvenlik modülü (hardware security module) ile etkileşime girmeniz mi gerekiyor? Mesele şu ki, şifre çözme işlemi nadiren bir kopyala-yapıştır işidir ve genellikle algoritmaları, modları, veritabanı etkileşimlerini ve veri kodlamasını belirli ölçüde anlamayı gerektirir. Bu nedenle, sizi doğrudan cevaba götürmek yerine, zamanı geldiğinde bunu kendiniz çözmek zorunda kalacağınız beklentisiyle yalnızca yolu gösterdik.
 
Simetrik anahtar şifrelemesi hakkında az da olsa bilgi sahibi olmak, sızma testlerinizin çok daha başarılı olmasını sağlayabilir. Örneğin, müşteri kaynak kodu depolarını karıştırırken edindiğimiz deneyimlere göre, insanların sık sık AES şifreleme algoritmasını, ya CBC ya da Electronic Codebook (ECB) modunda kullandıklarını gördük. ECB modu doğasında bazı zayıflıklar barındırır ve yanlış uygulanırsa CBC de bundan daha iyi değildir. Kriptoyu anlamak zor olabileceğinden, geliştiriciler sıklıkla tüm kripto şifrelerini ve modlarını eşit derecede etkili kabul eder ve bunların inceliklerinin farkında olmazlar. Kendimizi birer kriptograf olarak görmesek de, Go'da kriptoyu güvenli biçimde uygulayacak ve başkalarının kusurlu uygulamalarını sömürecek kadar bilgi sahibiyiz.
 
Simetrik anahtar şifrelemesi, asimetrik kriptografiden daha hızlı olsa da, gömülü (inherent) anahtar yönetimi sorunlarıyla karşı karşıyadır. Sonuçta, onu kullanmak için, veriler üzerinde şifreleme veya şifre çözme fonksiyonlarını icra eden tüm sistemlere veya uygulamalara aynı anahtarı dağıtmanız gerekir.

244   Bölüm 11
Anahtarı güvenli bir şekilde dağıtmanız gerekir; çoğunlukla sıkı süreçlere ve denetim (audit) gereksinimlerine uymanız beklenir. Ayrıca sadece simetrik anahtar kriptografisine güvenmek, örneğin, rastgele istemcilerin diğer düğümlerle şifreli iletişim kurmasını engeller. Gizli anahtarı müzakere etmenin iyi bir yolu yoktur; ayrıca pek çok yaygın algoritma ve mod için ne kimlik doğrulama (authentication) ne de bütünlük (integrity) güvencesi söz konusudur. Bu da şu anlama gelir: yetkili olsun ya da kötü niyetli, gizli anahtarı ele geçiren herkes onu kullanmaya devam edebilir.
 
İşte asimetrik kriptografinin işe yarayabileceği yer burasıdır.

## Asimetrik Kriptografi

Simetrik anahtar şifrelemesiyle ilişkili pek çok sorun, iki ayrı fakat matematiksel olarak ilişkili anahtar kullanan asimetrik (veya açık anahtar/public-key) kriptografi ile çözülür. Bunlardan biri kamuya açık, diğeri ise gizli tutulur. Özel anahtarla (private key) şifrelenen veri yalnızca açık anahtarla (public key) çözülebilir ve açık anahtarla şifrelenen veri yalnızca özel anahtarla çözülebilir. Eğer özel anahtar düzgün şekilde korunur ve gerçekten de gizli tutulursa, açık anahtarla şifrelenen veri gizli kalır; çünkü şifreyi çözmek için sıkı korunan özel anahtara ihtiyaç vardır. Bunun da ötesinde, özel anahtarı bir kullanıcıyı doğrulamak için kullanabilirsiniz. Örneğin, kullanıcı özel anahtarıyla mesajları imzalayabilir ve kamu tarafı bu imzalı mesajları açık anahtarı kullanarak doğrulayabilir.
 
Burada şöyle sorabilirsiniz: “Peki bunun bedeli ne? Eğer açık anahtar kriptografisi tüm bu güvenceleri sağlıyorsa, neden hâlâ simetrik anahtar kriptografisi kullanıyoruz?” Sorun, açık anahtar şifrelemesinin hızındadır; simetrik muadilinden çok daha yavaştır. Her iki dünyanın da en iyi yanlarını almak (ve en kötü yanlarından kaçınmak) için, kuruluşların çoğu hibrit bir yaklaşım kullanır: Başlangıçtaki iletişim müzakeresi için asimetrik kripto kullanırlar; bununla şifreli bir kanal kurulur ve bu kanal üzerinden bir simetrik anahtar (genellikle oturum anahtarı/session key olarak adlandırılır) üretilir ve paylaşılır. Oturum anahtarı oldukça küçük olduğu için, bu süreçte açık anahtar kriptosu kullanmak çok az ek yük (overhead) gerektirir. Hem istemci hem de sunucu bu oturum anahtarının bir kopyasına sahip olur ve sonraki iletişimleri daha hızlı hâle getirmek için bu anahtarı kullanırlar.
 
Şimdi, açık anahtar kriptosu için birkaç yaygın kullanım durumuna bakalım. Özellikle, şifreleme, imza doğrulama ve karşılıklı kimlik doğrulamayı (mutual authentication) inceleyeceğiz.
