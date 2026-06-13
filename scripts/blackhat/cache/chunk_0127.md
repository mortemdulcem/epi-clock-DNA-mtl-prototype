324     Bölüm 14

gRPC istemcisinin bağlantısını `grpcapi.NewImplantClient(conn)` ➊ çağrısı için kullanıyoruz (bizim için `protoc` tarafından oluşturulmuş bir fonksiyon). Artık implant sunucumuza geri dönük kurulmuş bir bağlantıya sahip olması gereken bir gRPC istemcimiz var.

Kodumuz, implant sunucusunu yoklamak için sonsuz bir `for` döngüsü ➋ kullanarak devam eder; tekrar tekrar yapılması gereken bir iş olup olmadığını kontrol eder. Bunu, bir istek context'i ve `Empty` struct'ını geçirerek `client.FetchCommand(ctx, req)` çağrısını yaparak gerçekleştirir. Arka planda, API sunucumuza bağlanmaktadır. Aldığımız yanıtta `cmd.In` alanında bir şey yoksa 3 saniye bekleyip tekrar deneriz. Bir iş birimi alındığında, implant `strings.Split(cmd.In, " ")` ➌ çağrısını yaparak komutu tek tek kelimelere ve argümanlara böler. Bu zorunludur, çünkü Go'nun işletim sistemi komutlarını çalıştırma söz dizimi `exec.Command(name, args...)` şeklindedir; burada `name` çalıştırılacak komut, `args...` ise o işletim sistemi komutunda kullanılan tüm alt komutların, bayrakların ve argümanların listesidir. Go bunu, işletim sistemi komut enjeksiyonunu önlemek için yapar ama bu da bizim çalıştırma sürecimizi karmaşıklaştırır, çünkü komutu çalıştırmadan önce ilgili parçalara bölmemiz gerekir. Komutu çalıştırmak ve çıktısını toplamak için `c.CombinedOutput()` ➍ çalıştırırız. Son olarak, bu çıktıyı alır ve `client.SendOutput(ctx, cmd)` gRPC çağrısını başlatarak komutumuzu ve çıktısını sunucuya geri göndeririz ➎.

Artık implantınız tamamlandı ve `go run implant/implant.go` ile çalıştırabilirsiniz. Sunucunuza bağlanmalıdır. Yine de pek heyecan verici olmayacaktır, çünkü yapılacak bir iş yok. Sadece birkaç çalışan süreç, bağlantı kuruyor ama anlamlı bir şey yapmıyor. Bunu düzeltelim.

## Yönetici (Admin) Bileşenini İnşa Etme

Yönetici bileşeni RAT'imizin son parçasıdır. Aslında işi üreteceğimiz yer burasıdır. Bu iş, admin gRPC API'miz üzerinden sunucuya gönderilecek, sunucu da bunu implant'a iletecektir. Sunucu, çıktıyı implant'tan alır ve admin istemcisine geri gönderir. Liste 14-5, `client/client.go` dosyasındaki kodu gösterir.

```go
func main() {
    var

        opts    []grpc.DialOption
        conn *grpc.ClientConn
        err     error
        client grpcapi.AdminClient // ➊

   opts = append(opts, grpc.WithInsecure())
   if conn, err = grpc.Dial(fmt.Sprintf("localhost:%d", 9090), opts...); err != nil {
        log.Fatal(err)
   }
   defer conn.Close()
   client = grpcapi.NewAdminClient(conn) // ➋
```

325     Komuta-Kontrol (Command-and-Control) RAT İnşa Etme

Her bir implant için bir `ID` atayabilir veya bir UUID kullanabilirsiniz (bkz. `https://github.com/google/uuid/`). Bu, hem admin hem de implant API'lerinde değişiklikler yapmanızı gerektirecektir; implant `.proto` dosyanızdan başlayarak. `Implant` servisine `RegisterNewImplant` adlı bir RPC metodu ekleyin ve `Admin` servisine `ListRegisteredImplants` ekleyin. Şemayı `protoc` ile yeniden derleyin, `server/server.go` içinde uygun arayüz (interface) metodlarını uygulayın ve yeni işlevselliği `client/client.go` (admin tarafı için) ve `implant/implant.go` (implant tarafı için) içindeki mantığa ekleyin.

### Veritabanı Kalıcılığı (Persistence) Ekleyin

Bu bölümdeki önceki alıştırmaları tamamladıysanız, bağlantı kesintilerine dayanmak için implantlara bir miktar dayanıklılık eklediniz ve kayıt (registration) işlevselliğini kurdunuz. Bu noktada, büyük olasılıkla kayıtlı implant listesini `server/server.go` içinde bellekte tutuyorsunuz. Peki ya sunucuyu yeniden başlatmanız gerekirse veya sunucu çökerse? Implantlar yeniden bağlanmaya devam edecek, ancak bunu yaptıklarında sunucunuz, kayıtlı hangi implantların olduğunu bilmeyecektir; çünkü implantların UUID'lerine olan eşlemeyi kaybetmiş olursunuz.

Sunucu kodunuzu, bu veriyi seçtiğiniz bir veritabanında saklayacak şekilde güncelleyin. Oldukça hızlı ve kolay, minimum bağımlılığa sahip bir çözüm için bir SQLite veritabanı düşünün. Birkaç Go sürücüsü mevcuttur. Biz şahsen `go-sqlite3` (`https://github.com/mattn/go-sqlite3/`) kullandık.

### Birden Fazla İmplantı Destekleyin

Gerçekçi olmak gerekirse, sunucunuzdan iş istemek için yoklama (polling) yapan birden fazla implantı eşzamanlı olarak desteklemek isteyeceksiniz. Bu, RAT'inizi önemli ölçüde daha kullanışlı hale getirir, çünkü tek bir implanttan fazlasını yönetebilir; ancak aynı zamanda oldukça ciddi değişiklikler de gerektirir.

Bunun nedeni, bir implant üzerinde komut çalıştırmak istediğinizde, muhtemelen komutu ilk gelen implantta değil, belirli tek bir implantta çalıştırmak isteyecek olmanızdır. Kayıt sırasında oluşturulan implant ID'sine güvenerek implantları birbirinden yalıtabilir ve komutları ile çıktıları uygun şekilde yönlendirebilirsiniz. Komutun çalıştırılması gereken hedef implantı açıkça seçebileceğiniz bir işlevsellik uygulayın.

Bu mantığı daha da karmaşıklaştıran bir diğer konu da, bir ekip ile çalışırken yaygın olduğu üzere, aynı anda komut gönderen birden fazla admin operatörünün olabilmesidir. Bu, muhtemelen iş ve çıktı kanallarınızı (channel) buffer'sız türlerden buffer'lı türlere dönüştürmek isteyeceğiniz anlamına gelir. Bu, birden fazla mesaj uçuşta (in-flight) olduğunda çalışmanın bloklanmasını engellemeye yardımcı olacaktır. Ancak bu tür bir çoklama (multiplexing) desteği için, bir istekte bulunanı (requestor) doğru yanıtla eşleştirebilen bir mekanizma uygulamanız gerekecektir. Örneğin, iki admin operatörü aynı anda implantlara iş gönderirse, implantlar iki ayrı yanıt üretecektir. Eğer operatör 1 `ls` komutunu, operatör 2 ise `ifconfig` komutunu gönderirse, operatör 1'in `ifconfig` komutunun çıktısını alması ve tersinin olması uygun olmaz.
