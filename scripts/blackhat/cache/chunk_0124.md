316    Bölüm 4

## Proje Çalışma Alanını Oluşturma

Şimdi, proje çalışma alanımızı oluşturalım. Üç bileşeni (implant, server ve admin bileşeni) ve gRPC API tanım dosyalarını hesaba katmak için dört alt dizin oluşturacağız. Her bir bileşen dizininde, aynı isimli tek bir Go dosyası oluşturacağız; bu dosya kendi `main` package'ına ait olacak. Bu, her birini bağımsız bir bileşen olarak derleyip çalıştırmamıza olanak tanır ve ilgili bileşen üzerinde `go build` çalıştırdığımızda açıklayıcı bir ikili (binary) isim oluşmasını sağlar. Ayrıca `grpcapi` dizinimizde `implant.proto` adlı bir dosya oluşturacağız. Bu dosya Protobuf şemamızı ve gRPC API tanımlarımızı barındıracak. Sahip olmanız gereken dizin yapısı şöyle:

```bash
tree

-- client
    |-- client.go
    grpcapi
    |-- implant.proto
-- implant
    |-- implant.go
-- server
    |-- server.go
```

Bu yapıyı oluşturduğumuza göre, artık uygulamamızı inşa etmeye başlayabiliriz. Sonraki birkaç bölüm boyunca, her dosyanın içeriğini adım adım açıklayacağız.

## gRPC API’sini Tanımlama ve Derleme

Bir sonraki işimiz, gRPC API’mizin kullanacağı işlevsellik ve veriyi tanımlamak. REST uç noktaları (endpoint) inşa etmek ve tüketmek, oldukça iyi tanımlanmış bir beklenti setine sahiptir (örneğin, hangi veri üzerinde hangi eylemin yapılacağını tanımlamak için HTTP fiilleri ve URL yolları kullanılır); gRPC ise daha keyfidir. Etkili biçimde bir API servisi tanımlar ve bu servise ait fonksiyon prototiplerini ve veri tiplerini bağlarsınız. API’mizi tanımlamak için Protobuf kullanacağız. Protobuf söz diziminin (syntax) tam açıklamasını kısa bir Google aramasıyla bulabilirsiniz; biz burada kısaca açıklayacağız.

En azından, operatörlerin sunucuya işletim sistemi komutları (iş/emir) göndermek için kullanacağı bir yönetim (administrative) servisini tanımlamamız gerekecek. Ayrıca implant’ımızın sunucudan iş/emir çekmek ve komut çıktısını tekrar sunucuya göndermek için kullanacağı bir implant servisine ihtiyacımız olacak. Liste 14-1, `implant.proto` dosyasının içeriğini gösterir. (`/` kök konumundaki tüm kod listeleri, verilen GitHub deposu `https://github.com/blackhat-go/bhe` altında bulunur.)

```proto
//implant.proto
syntax = "proto3";

package grpcapi;

// Implant defines our C2 API functions
service Implant {
    rpc FetchCommand (Empty) returns (Command);
    rpc SendOutput (Command) returns (Empty);
}

// Admin defines our Admin API functions
service Admin {
    rpc RunCommand (Command) returns (Command);
}

// Command defines a with both input and output fields
message Command {
    string In = 1;
    string Out = 2;
}

// Empty defines an empty message used in place of null
message Empty {
}
```

**Liste 14-1: Protobuf kullanarak gRPC API’sini tanımlamak (`/ch-14/grpcapi/implant.proto`)**

Bu tanım dosyasını Go’ya özgü çıktılara derlemeyi planladığımızı hatırlayın. `package grpcapi` ifadesini özellikle ekliyoruz; derleyiciye bu çıktıları `grpcapi` package’ı altında oluşturmak istediğimizi söylemek için. Bu package adının kendisi keyfidir; API kodunun diğer bileşenlerden ayrı kalmasını sağlamak için bu adı seçtik.

Şemamız daha sonra `Implant` adlı bir servis ve `Admin` adlı bir servis tanımlar. Bunları ayırıyoruz, çünkü `Implant` bileşenimizin API ile, `Admin` istemcisinden farklı biçimde etkileşime girmesini bekliyoruz. Örneğin, implant’ımızın sunucuya işletim sistemi komut işi göndermesini istemeyiz; tıpkı `Admin` bileşenimizin komut çıktısını sunucuya göndermesini zorunlu kılmak istemediğimiz gibi.

`Implant` servisi üzerinde iki metot tanımlıyoruz: `FetchCommand` ve `SendOutput`. Bu metotları tanımlamak, Go’da bir arayüz (interface) tanımlamaya benzer. Herhangi bir `Implant` servis implementasyonunun bu iki metodu da uygulaması gerektiğini söylüyoruz. `FetchCommand`, parametre olarak bir `Empty` mesajı alır ve bir `Command` mesajı döner; bu, sunucudan bekleyen işletim sistemi komutlarını alacaktır. `SendOutput` ise bir `Command` mesajını (komut çıktısını içeren) sunucuya geri gönderecektir. Bu mesajlar — birazdan ele alacağımız — uç noktalarımız arasında veri ileri geri taşımak için ihtiyaç duyduğumuz alanları içeren, keyfi ve karmaşık veri yapılarıdır.

`Admin` servisimiz tek bir metot tanımlar: `RunCommand`. Bu metot, parametre olarak bir `Command` mesajı alır ve karşılığında bir `Command` mesajı okunmasını bekler. Amacı, RAT operatörü olarak size, implant’ın çalıştığı uzak bir sistem üzerinde bir işletim sistemi komutu çalıştırma imkanı sağlamaktır.

Son olarak, etrafta dolaştıracağımız iki mesajı tanımlarız: `Command` ve `Empty`. `Command` mesajı iki alan içerir: biri işletim sistemi komutunun kendisini tutmak için (`In` adlı bir `string`), diğeri komut çıktısını tutmak için (`Out` adlı bir `string`). Mesaj ve alan adlarının keyfi olduğuna dikkat edin, ama her alan için sayısal bir değer atadığımızı da fark edin. `In` ve `Out` değerlerine sayısal değer atayabilmemizin nasıl mümkün olduğunu, bunları `string` olarak tanımlamışken merak ediyor olabilirsiniz. Bunun cevabı, bunun bir implementasyon değil, bir şema tanımı olmasıdır. Bu sayısal değerler, alanların mesajın içinde görüneceği ofsetleri temsil eder. `In`’in önce, `Out`’un ikinci sırada görüneceğini söylüyoruz. `Empty` mesajı herhangi bir alan içermez. Bu, Protobuf’un bir RPC metoduna açıkça `null` değerlerin geçirilmesine veya bir RPC metodundan döndürülmesine izin vermemesi gerçeğine karşı bir geçici çözüm (hack) niteliğindedir.

Artık şemaya sahibiz. gRPC tanımını tamamlamak için, bu şemayı derlememiz gerekiyor. `grpcapi` dizininden aşağıdaki komutu çalıştırın:

```bash
> protoc -I . implant.proto --go_out=. --go-grpc_out=.
```
