Her döngü yinelemesinde, üretici fonksiyonunuz olan `generate()` 0 çağrılır ve üreticinin üzerinde yineleme yapacağı başlangıç (`start`) ve bitiş (`end`) anahtar uzayı (key space) ofsetleri ona aktarılır. Ayrıca `work` ve `done` kanallarınızı ve üretici `WaitGroup`’ünüzü de geçirirsiniz. Fonksiyonu çağırdıktan sonra, bir sonraki üreticiye aktarılacak anahtar uzayı aralığını hesaba katmak için `start` ve `end` değişkenlerinizi kaydırırsınız. Anahtar uzayınızı, programın eşzamanlı (concurrent) olarak işleyebileceği, goroutine’ler arasında çakışma olmadan, daha küçük ve sindirilebilir parçalara bu şekilde ayırırsınız.

Üreticileriniz başlatıldıktan sonra, `for` döngüsü kullanarak işçiler (workers) 0 oluşturursunuz. Bu örnekte 30 tane oluşturuyorsunuz. Her yinelemede `decrypt()` fonksiyonunuzu 0 çağırıyor ve ona `ciphertext`, `work` kanalı, `done` kanalı ve tüketici `WaitGroup`’ünü (consumer WaitGroup) iletiyorsunuz. Bu, üreticiler işleri oluşturdukça bunları çekmeye ve işlemeye başlayan eşzamanlı tüketicileri başlatır.

Tüm anahtar uzayı üzerinde yineleme yapmak zaman alır. İşleri doğru ele almazsanız, `main()` fonksiyonu bir anahtar keşfetmeden veya anahtar uzayını tamamen tüketmeden önce kesinlikle sonlanacaktır. Bu nedenle, üreticilerin ve tüketicilerin ya tüm anahtar uzayı üzerinde yineleme yapmaları ya da doğru anahtarı keşfetmeleri için yeterli zamana sahip olduklarından emin olmanız gerekir. Burada `WaitGroup`’lar devreye girer. Üreticiler görevlerini tamamlayana kadar `main()`’i bloklamak için `prodWg.Wait()` 0 çağrısı yaparsınız. Üreticilerin görevlerini, anahtar uzayını tamamen tükettiklerinde veya `done` kanalı aracılığıyla süreci açıkça iptal ettiklerinde tamamladıklarını unutmayın. Bu tamamlandıktan sonra, tüketiciler `work` kanalından okumaya çalışırken sürekli kilitlenmesin (deadlock) diye `work` kanalını açıkça kapatırsınız. Son olarak, `work` kanalındaki kalan işleri tamamlamaları için `WaitGroup` içindeki tüketicilere yeterli süre tanımak amacıyla `consWg.Wait()` 0 çağrısıyla `main()`’i yeniden bloklarsınız.

## Programı Çalıştırma

Programınızı tamamladınız! Eğer çalıştırırsanız, aşağıdaki çıktıyı görmelisiniz:

```bash
$ go run main.go
2020/07/12 14:27:47 Starting producers...
2020/07/12 14:27:47 Producers started!
2020/07/12 14:27:47 Starting consumers...
2020/07/12 14:27:47 Consumers started!
2020/07/12 14:27:47 Now we wait...
2020/07/12 14:27:48 Card [4532651325506680] found using key [e612dObbb6]
2020/07/12 14:27:48 Brute-force complete
```

Program üreticileri ve tüketicileri başlatır ve ardından bunların çalışmasını bekler. Bir kart bulunduğunda, program açık metin (cleartext) kartı ve o kartı şifre çözmek için kullanılan anahtarı gösterir. Bu anahtarın tüm kartlar için sihirli anahtar olduğunu varsaydığımızdan, yürütmeyi (execution) erken keser ve başarımızı, bir otoportre çizerek (gösterilmemiştir) kutlarız.

Elbette, anahtar değerine bağlı olarak, ev tipi bir bilgisayarda kaba kuvvet (brute force) saldırısı önemli bir süre alabilir — günler hatta haftalar. Yukarıdaki örnek çalıştırmada, anahtarı daha hızlı bulmak için anahtar uzayını daralttık. Ancak, 2016 model bir MacBook Pro’da anahtar uzayını tamamen tüketmek yaklaşık yedi gün sürer. Bir dizüstü bilgisayarda çalışan, hızlı ve kirli (quick-and-dirty) bir çözüm için fena sayılmaz.

## Özet

Kripto, öğrenme eğrisi dik olsa da güvenlik uygulayıcıları için önemli bir konudur. Bu bölümde simetrik ve asimetrik kripto, özetleme (hashing), bcrypt ile parola işleme, ileti doğrulama (message authentication), karşılıklı doğrulama (mutual authentication) ve RC2’ye karşı yapılan kaba kuvvet saldırısı ele alındı. Bir sonraki bölümde, Microsoft Windows’a saldırmanın ayrıntılarına gireceğiz.

## WINDOWS SİSTEM ETKİLEŞİMİ
VE ANALİZ
12

Microsoft Windows saldırıları geliştirmek için sayısız yol vardır — bu bölümde hepsini ele almak için fazla sayıdalar. Bunların hepsini tartışmak yerine, ister ilk saldırıda ister sömürü sonrası (post-exploitation) maceralarınız sırasında olsun, Windows’a saldırmanıza yardımcı olabilecek birkaç tekniği tanıtıp inceleyeceğiz.

Microsoft API dokümantasyonundan ve bazı güvenlik endişelerinden bahsettikten sonra üç konuyu ele alacağız. İlk olarak, çekirdek `syscall` paketini kullanarak bir süreç enjeksiyonu (process injection) gerçekleştirerek çeşitli sistem düzeyi Windows API’leriyle etkileşim kuracağız. İkinci olarak, Windows Portable Executable (PE) formatı için Go’nun çekirdek paketini inceleyip bir PE dosya formatı ayrıştırıcısı (parser) yazacağız. Üçüncü olarak, yerel Go koduyla C kodu kullanma tekniklerini tartışacağız. Özgün bir Windows saldırısı geliştirmeniz için bu uygulamalı teknikleri bilmeniz gerekecek.

## Windows API’sinin OpenProcess() Fonksiyonu

Windows’a saldırmak için Windows API’yi anlamanız gerekir. `OpenProcess()` fonksiyonunu inceleyerek Windows API dokümantasyonunu keşfedelim; bu fonksiyon, uzak bir süreç üzerinde bir handle elde etmek için kullanılır. `OpenProcess()` dokümantasyonunu `https://docs.microsoft.com/en-us/windows/desktop/api/processthreadsapi/nf-processthreadsapi-openprocess` adresinde bulabilirsiniz. Şekil 12-1, fonksiyonun nesne özelliği (object property) ayrıntılarını göstermektedir.

```c
HANDLE OpenProcess(
  DWORD dwDesiredAccess,
  BOOL  bInheritHandle,
  DWORD dwProcessId
);
```

**Şekil 12-1:** `OpenProcess()` için Windows API nesne yapısı
