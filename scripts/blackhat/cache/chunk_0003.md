## Giriş

Bu bölümde, çeşitli yaygın SQL ve NoSQL platformlarını ele alacağız. SQL veritabanlarına bağlanmanın ve sorgu çalıştırmanın temellerini öğreneceksiniz. Veritabanları ve tablolar içinde hassas bilgileri aramayı göstereceğiz; bu, özellikle sömürü sonrası (post-exploitation) aşamada kullanılan yaygın bir tekniktir. Ayrıca dosya sistemlerinde dolaşmayı ve dosyaları hassas bilgiler için incelemeyi de göstereceğiz.

### Bölüm 8: Ham Paket İşleme

Bu bölümde, `libpcap` kullanan `gopacket` kütüphanesi aracılığıyla ağ paketlerini koklamayı (sniff) ve işlemeyi göstereceğiz. Kullanılabilir ağ aygıtlarını nasıl tespit edeceğinizi, paket filtrelerini nasıl kullanacağınızı ve bu paketleri nasıl işleyeceğinizi öğreneceksiniz. Ardından, `syn-flood` ve `syn-cookies` gibi, normal port taramalarının aşırı sayıda yanlış pozitif üretmesine neden olan çeşitli koruma mekanizmalarının üzerinden güvenilir şekilde tarama yapabilen bir port tarayıcı geliştireceğiz.

### Bölüm 9: Sömürü Kodları Yazma ve Taşıma

Bu bölüm neredeyse tamamen exploit (sömürü) oluşturma üzerine odaklanır. Farklı türde zafiyetler keşfetmek için bir fuzzer oluşturarak başlar. Bölümün ikinci yarısında, mevcut exploit’leri diğer dillerden Go’ya nasıl port edeceğimizi tartışıyoruz. Bu tartışma, bir Java serileştirme (deserialization) exploit’inin ve Dirty COW ayrıcalık yükseltme exploit’inin Go’ya taşınmasını içerir. Bölümü, Go programlarınız içinde kullanmak üzere shellcode oluşturma ve dönüştürme üzerine bir tartışmayla tamamlıyoruz.

### Bölüm 10: Go Eklentileri (Plugins) ve Genişletilebilir Araçlar

Bu bölümde, genişletilebilir araçlar oluşturmak için iki ayrı yöntem tanıtacağız. İlk yöntem, Go sürüm 1.8 ile tanıtılan, Go’nun yerleşik eklenti (plug-in) mekanizmasını kullanır. Bu yaklaşımın kullanım senaryolarını tartışacağız ve Lua’dan yararlanan ikinci bir yaklaşımı ele alacağız; bu yaklaşım genişletilebilir araçlar yaratmayı sağlar. Her iki yaklaşımın da yaygın bir güvenlik görevini gerçekleştirmek için nasıl uyarlanabileceğini gösteren pratik örnekler sunacağız.

### Bölüm 11: Kriptografi Uygulama ve Saldırıları

Bu bölüm, Go kullanarak simetrik ve asimetrik kriptografinin temel kavramlarını kapsar. Bu bilgiler, standart Go paketini kullanarak kriptografiyi kullanmaya ve anlamaya odaklanır. Go, şifreleme için üçüncü taraf bir kütüphane kullanmak yerine dilin içinde yerleşik bir uygulama sunan az sayıdaki dilden biridir. Bu da kodun dolaşılmasını, değiştirilmesini ve anlaşılmasını kolaylaştırır.

Standart kütüphaneyi, yaygın kullanım örneklerini inceleyerek ve araçlar oluşturarak keşfedeceğiz. Bu bölümde hashing (özetleme), mesaj kimlik doğrulaması ve şifreleme yapmayı öğreneceksiniz. Son olarak, RC2 ile şifrelenmiş bir şifreli metni kaba kuvvet (brute-force) yöntemiyle çözdüğümüz bir örnek göstereceğiz.

## Bölüm 12: Windows Sistemiyle Etkileşim ve Analiz

Windows’a yönelik saldırılara ilişkin tartışmamızda, Windows yerel API’siyle etkileşim kurma yöntemlerini gösterecek, `syscall` paketini keşfederek süreç içi enjeksiyon (process injection) gerçekleştirecek ve bir Portable Executable (PE) ikili dosya ayrıştırıcısı (binary parser) nasıl inşa edilir öğreneceğiz. Bölüm, Go’nun C birlikte çalışabilirlik (interoperability) mekanizmaları aracılığıyla yerel C kütüphanelerinin çağrılmasına dair bir tartışmayla sona erecek.

## Bölüm 13: Steganografi ile Veri Gizleme

Steganografi, bir mesajı veya dosyayı başka bir dosyanın içinde gizleme işlemidir. Bu bölüm, steganografinin bir varyasyonunu tanıtır: rastgele verileri bir PNG görüntü dosyasının içeriğine gizlemek. Bu teknikler, veri dışarı sızdırma (exfiltration), örtük/obfuscate C2 mesajları oluşturma ve tespit edici veya önleyici kontrolleri atlatma için faydalı olabilir.

## Bölüm 14: Komuta-Kontrol (C2) RAT Geliştirme

Son bölüm, Go ile komuta-kontrol (command-and-control, C2) implant ve sunucularının pratik uygulamalarını ele alır. Önceki bölümlerde edinilen deneyim ve bilgiden yararlanarak bir C2 kanalı inşa edeceğiz. Özel olarak geliştirilmiş olması itibarıyla, C2 istemci/sunucu uygulaması imza tabanlı güvenlik kontrollerinden kaçınacak ve sezgisel (heuristic) ve ağ tabanlı dışa çıkış (egress) kontrollerini bertaraf etmeye çalışacaktır.

---

## Go Temelleri

Bu bölüm, Go geliştirme ortamınızı kurma sürecinde size rehberlik edecek ve sizi dilin sözdizimine (syntax) tanıtacaktır. Dilin temel mekanikleri üzerine tümüyle yazılmış kitaplar var; bu bölüm, sonraki bölümlerdeki kod örnekleri üzerinde çalışabilmeniz için ihtiyaç duyacağınız en temel kavramları kapsar. İlkel (primitive) veri tiplerinden eşzamanlılık (concurrency) uygulamaya kadar her şeyi ele alacağız. Dile zaten hâkim olan okurlar için bu bölümün büyük kısmı bir tekrar niteliğinde olacaktır.

### Bir Geliştirme Ortamı Kurma

Go ile çalışmaya başlamak için işlevsel bir geliştirme ortamına ihtiyacınız var. Bu bölümde, Go’yu indirip çalışma alanınızı (workspace) ve ortam değişkenlerinizi (environment variables) ayarlama adımlarında size rehberlik edeceğiz. Entegre geliştirme ortamınız (IDE) için çeşitli seçenekleri ve Go ile birlikte gelen standart araçların bazılarını tartışacağız.

### Go’yu İndirme ve Kurma

Başlangıç olarak, işletim sisteminiz ve mimarinize en uygun Go ikili (binary) dağıtımını `https://golang.org/dl/` adresinden indirin. Windows, Linux ve macOS için ikili dosyalar mevcuttur. Önceden derlenmiş (precompiled) ikili dosyanın bulunmadığı bir sistem kullanıyorsanız, Go kaynak kodunu da aynı linkten indirebilirsiniz.

İkili dosyayı çalıştırın ve yönergeleri izleyin; bunlar oldukça minimal olacaktır. Bu işlem, Go çekirdek paketlerinin (core packages) tamamını yükler. Paketler — diğer çoğu dilde “library” olarak adlandırılır — Go programlarınızda kullanabileceğiniz yararlı kodlar içerir.
