Bu komut, daha önce bahsettiğimiz ilk kurulumu tamamladıktan sonra kullanılabilir hale gelir, geçerli dizinde `imp/ara.prota` adlı Protobuf dosyasını arar ve geçerli dizinde Go’ya özgü çıktı üretir. Komutu başarılı şekilde çalıştırdıktan sonra, `grpcapi` dizininizde `implant.pb.go` adlı yeni bir dosya bulunmalıdır. Bu yeni dosya, Protobuf şemasında oluşturulan servisler ve mesajlar için arayüz ve `struct` tanımlarını içerir. Bunu sunucu, implant ve admin bileşenlerimizi inşa etmek için kullanacağız. Bunları tek tek inşa edelim.

## Sunucuyu Oluşturma

Sunucudan başlayalım; bu bileşen admin istemcisinden gelen komutları ve implanttan gelen yoklamaları (polling) kabul edecek. Sunucu, Implant ve Admin servislerinin her ikisini de uygulaması gerektiği için bileşenler arasında en karmaşık olanı olacaktır. Ayrıca, admin bileşeni ile implant arasında bir aracı (middleman) olarak davrandığından, her iki taraftan gelen ve giden mesajları proxy’leyip yönetmesi gerekecek.

### Protokol Arayüzünü Uygulama

Önce `server/server.go` dosyasındaki (Liste 14-2) sunucumuzun iç kısmına bakalım. Burada, sunucunun paylaşılan kanallardan komut okuyup yazabilmesi için gerekli arayüz metodlarını uyguluyoruz.

```go
type implantServer struct {
    work, output chan *grpcapi.Command
}

type adminServer struct {
    work, output chan *grpcapi.Command
}

func NewImplantServer(work, output chan *grpcapi.Command) *implantServer {
    s := new(implantServer)
    s.work = work
    s.output = output
    return s
}

func NewAdminServer(work, output chan *grpcapi.Command) *adminServer {
    s := new(adminServer)
    s.work = work
    s.output = output
    return s
}

func (s *implantServer) FetchCommand(ctx context.Context,
    empty *grpcapi.Empty) (*grpcapi.Command, error) {
    var cmd = new(grpcapi.Command)
    select {
    case cmd, ok := <-s.work:
        if ok {
            return cmd, nil
        }
        return cmd, errors.New("channel closed")
    default:
        // No work
        return cmd, nil
    }
}

func (s *implantServer) SendOutput(ctx context.Context,
    result *grpcapi.Command) (*grpcapi.Empty, error) {
    s.output <- result
    return &grpcapi.Empty{}, nil
}

func (s *adminServer) RunCommand(ctx context.Context, cmd *grpcapi.Command)
    (*grpcapi.Command, error) {
    var res *grpcapi.Command
    go func() {
        s.work <- cmd
    }()
    res = <-s.output
    return res, nil
}
```

**Liste 14-2: Sunucu tiplerinin tanımlanması (`/ch-14/server/server.go`)**

Admin ve implant API’lerimizi sunabilmek için, gerekli tüm arayüz metodlarını uygulayan sunucu tiplerini tanımlamamız gerekir. Bunun başka bir yolu yoktur.
