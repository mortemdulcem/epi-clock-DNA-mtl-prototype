## İmplant İşlevselliğini Genişletin

Bizim uygulamamız implantların yalnızca işletim sistemi komutlarını almasını ve çalıştırmasını bekliyor. Ancak diğer C2 yazılımlarında, sahip olmak güzel olacak birçok başka kolaylık işlevi bulunur. Örneğin, implantlarımıza dosya yükleyip indirebilmek güzel olurdu. Ayrıca, ham shellcode çalıştırmak da hoş olabilir; örneğin, diske dokunmadan bir Meterpreter shell başlatmak istediğimizde. Mevcut işlevselliği bu ek özellikleri destekleyecek şekilde genişletin.

## İşletim Sistemi Komutlarını Zincirleyin

Go'nun `os/exec` paketinin komutları oluşturup çalıştırma şekli nedeniyle, şu anda bir komutun çıktısını ikinci bir komuta girdi olarak aktaramazsınız (pipe edemezsiniz). Örneğin, mevcut uygulamamızda şu çalışmaz: `ls -la | wc -l`. Bunu düzeltmek için, komut örneğini oluşturmak için `exec.Command()` çağırıldığında yaratılan `command` değişkeni üzerinde oynama yapmanız gerekecek. `stdin` ve `stdout` özelliklerini uygun şekilde yönlendirmek için değiştirebilirsiniz. Bir `io.Pipe` ile birlikte kullanıldığında, bir komutun (örneğin `ls -la`) çıktısını sonraki bir komuta (örneğin `wc -l`) girdi olarak zorla kullanabilirsiniz.

## İmplantın Gerçekçiliğini Artırın ve İyi OPSEC Uygulayın

Bu bölümdeki ilk egzersizde implantınıza şifreli iletişim eklediğinizde, kendi imzaladığınız (self-signed) bir sertifika mı kullandınız? Eğer öyleyse, taşıma katmanı (transport) ve arka uç (backend) sunucunuz cihazlarda ve denetleyici proxy'lerde şüphe uyandırabilir. Bunun yerine, özel veya anonimleştirilmiş iletişim bilgileri kullanarak bir alan adı (domain name) kaydedin ve bir sertifika otoritesi (certificate authority) hizmetiyle birlikte meşru bir sertifika oluşturun. Ayrıca, imkanınız varsa implant ikili dosyanızı (binary) imzalamak için bir kod imzalama sertifikası (code-signing certificate) edinmeyi düşünün.

Ek olarak, kaynak kodu konumlarınız (path) için kullandığınız adlandırma şemasını gözden geçirmeyi düşünün. İkili dosyanızı derlediğinizde, dosya `package` yollarını (path) içerecektir. Açıklayıcı yol adları olay müdahale ekiplerinin sizi bulmasına yol açabilir. Ayrıca ikili dosyanızı derlerken hata ayıklama (debugging) bilgilerinin kaldırılmasını düşünün. Bunun ek faydası, ikili dosyanızın boyutunu küçültmek ve tersine mühendisliği zorlaştırmaktır. Aşağıdaki komut bunu sağlayabilir:

```bash
$ go build -ldflags "-s -w" implant/implant.go
```

Bu bayraklar (flags), hata ayıklama bilgisini kaldırmak ve ikili dosyayı strip etmek için bağlayıcıya (linker) iletilir.

## ASCII Sanatı Ekleyin

Uygulamanız tam bir karmaşa da olsa, ASCII sanatı varsa meşrudur. Şaka yapıyoruz elbette. Ama nedense her güvenlik aracında bir ASCII sanatı var, o yüzden siz de kendi aracınıza eklemek isteyebilirsiniz. Selamlamalar (greetz) isteğe bağlıdır.

## Özet

Go, bu bölümde inşa ettiğiniz RAT gibi çapraz platform implantlar yazmak için harika bir dildir. Bu projenin muhtemelen en zor kısmı implantı oluşturmak oldu; çünkü Go kullanarak alttaki işletim sistemiyle etkileşime girmek, C# ve Windows API gibi işletim sistemi API'si için tasarlanmış dillere kıyasla zorlayıcı olabilir. Ayrıca Go statik olarak derlenmiş bir ikili dosya ürettiğinden, implantlar büyük ikili boyutlara neden olabilir; bu da teslim (delivery) üzerinde bazı kısıtlamalar getirebilir.

Ancak arka uç (backend) servisleri için, Go'dan daha iyisi yok. Bu kitabın yazarlarından biri (Tom), başka bir yazarla (Dan) şu an devam eden bir iddiaya sahip: Eğer bir gün arka uç servisler ve genel amaçlı araçlar için Go kullanmayı bırakırsa, 10.000 dolar ödemek zorunda kalacak. Yakın zamanda böyle bir değişime dair hiçbir işaret yok (her ne kadar Elixir havalı görünse de). Bu kitapta anlatılan tüm teknikleri kullanarak, sağlam çerçeveler (framework) ve yardımcı araçlar (utility) inşa etmeye başlamak için güçlü bir temele sahipsiniz.

Bu kitabı okumaktan ve egzersizlere katılmaktan, bizim yazmaktan aldığımız kadar keyif almış olmanızı umuyoruz. Go yazmaya devam etmenizi ve bu kitapta öğrendiğiniz becerileri, mevcut görevlerinizi geliştiren veya onların yerini alan küçük yardımcı araçlar inşa etmek için kullanmanızı teşvik ediyoruz. Ardından, deneyim kazandıkça daha büyük kod tabanları üzerinde çalışmaya başlayın ve harika projeler geliştirin. Becerilerinizi geliştirmeye devam etmek için özellikle büyük organizasyonlardan çıkan, popüler büyük Go projelerine göz atın. GopherCon gibi konferanslardan sunumlar izleyin; bu sunumlar sizi daha ileri konularda yönlendirebilir, tuzakları ve programlamanızı geliştirme yollarını tartışır. En önemlisi, eğlenin — ve eğer güzel bir şey inşa ederseniz bize anlatın! Görüşmek üzere.
