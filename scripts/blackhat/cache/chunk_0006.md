Geliştirme sırasında en sık çalıştıracağınız komutlardan biri olan `go run`, `main` package’ını derler ve çalıştırır; yani programınızın giriş noktasını.

Örneğin, aşağıdaki kodu `GOPATH/src` altındaki bir proje dizinine (kurulum sırasında bu çalışma alanını oluşturduğunuzu unutmayın) `main.go` adıyla kaydedin:

```go
package main
import (
    "fmt"
)

func main() {
    fmt.Println("Hello, Black Hat Gophers!")
}
```

Komut satırında, bu dosyanın bulunduğu dizinde `go run main.go` komutunu çalıştırın. Ekranınızda `Hello, Black Hat Gophers!` çıktısını görmelisiniz.

## `go build` Komutu

`go run` dosyanızı çalıştırdı ama bağımsız (standalone) bir ikili (binary) dosya üretmedi. İşte bu noktada devreye `go build` komutu girer. `go build` komutu, uygulamanızı, içe aktarılan tüm paketleri ve bunların bağımlılıklarını derler, ancak sonucu yüklemez (install etmez). Programınızı çalıştırmaz; disk üzerinde bir ikili dosya oluşturur. Ürettiği dosyalar makul adlandırma kurallarına uyar ama çoğu zaman üretilen ikili dosyanın adını `-o` (output) komut satırı seçeneğiyle değiştirirsiniz.

Önceki örnekteki `main.go` dosyasının adını `hello.go` olarak değiştirin. Bir terminal penceresinde `go build hello.go` komutunu çalıştırın. Her şey yolunda giderse bu komut `hello` adında çalıştırılabilir bir dosya oluşturacaktır. Ardından şu komutu girin:

```bash
$ ./hello
Hello, Black Hat Gophers!
```

Bu komut bağımsız ikili dosyayı çalıştırmalıdır.

Varsayılan olarak üretilen ikili dosya hata ayıklama (debug) bilgisi ve sembol tablosu içerir. Bu da dosya boyutunu şişirebilir. Dosya boyutunu küçültmek için derleme sürecinde bu bilgileri ikili dosyadan ayıklayacak ek bayraklar kullanabilirsiniz. Örneğin, aşağıdaki komut ikili dosya boyutunu yaklaşık yüzde 30 azaltır:

```bash
$ go build -ldflags "-w -s"
```

Daha küçük bir ikili dosya, kötü niyetli girişimleriniz sırasında onu aktarmayı veya gömmeyi daha verimli hale getirir.

## Çapraz Derleme (Cross-Compiling)

`go build` komutunu kullanmak, ikili dosyayı mevcut sisteminizde veya aynı mimariye sahip bir sistemde çalıştırmak için gayet iyidir; peki ya farklı bir mimaride çalışacak bir ikili üretmek isterseniz? İşte burada çapraz derleme devreye girer. Çapraz derleme, Go’nun en havalı yönlerinden biridir; başka hiçbir dil bu işi bu kadar kolay yapamaz. `go build` komutu, programınızı birden çok işletim sistemi ve mimari için çapraz derlemenize olanak tanır. Uyumlu işletim sistemi ve mimari derleme türlerinin hangi kombinasyonlarda mümkün olduğu konusunda daha fazla ayrıntı için resmi Go dokümantasyonundaki `https://golang.org/doc/install/source#environment` sayfasına bakabilirsiniz.

Çapraz derleme yapmak için bir kısıt (constraint) ayarlamanız gerekir. Bu, derleme komutuna hangi işletim sistemi ve mimari için derleme yapmak istediğinizi bildirmenin bir yoludur. Bu kısıtlar `GOOS` (işletim sistemi için) ve `GOARCH` (mimari için) değerlerini içerir.

Derleme kısıtlarını üç şekilde tanıtabilirsiniz: komut satırından, kod yorumları üzerinden veya dosya adı soneki (suffix) adlandırma kuralı kullanarak. Burada komut satırı yöntemini ele alacağız; diğer iki yöntemi dilerseniz siz araştırabilirsiniz.

Diyelim ki macOS üzerinde bulunan önceki `hello.go` programını, Linux 64-bit mimaride çalışacak şekilde çapraz derlemek istiyorsunuz. Bunu komut satırında `GOOS` ve `GOARCH` kısıtlarını ayarlayarak gerçekleştirebilirsiniz:

```bash
$ GOOS="linux" GOARCH="amd64" go build hello.go
$ ls
hello hello.go
$ file hello
hello: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```

Çıktı, ortaya çıkan ikili dosyanın 64-bit bir ELF (Linux) dosyası olduğunu doğrular.

Çapraz derleme süreci, neredeyse tüm modern programlama dillerine kıyasla Go’da çok daha basittir. Karşılaşabileceğiniz tek gerçek “tuzak”, yerel C bağlamaları (native C bindings) kullanan uygulamaları çapraz derlemeye çalıştığınızda ortaya çıkar. Ayrıntılara fazla girmeyip, bu zorlukları kendi başınıza incelemenize bırakacağız. İçe aktardığınız paketlere ve geliştirdiğiniz projelere bağlı olarak, bu sorunla çok sık karşılaşmayabilirsiniz.

## `go doc` Komutu

`go doc` komutu, bir package, fonksiyon, metot veya değişkenle ilgili dokümantasyonu sorgulamanızı sağlar. Bu dokümantasyon, kodunuz boyunca yorumlar (comment) halinde gömülüdür. `fmt.Println()` fonksiyonu hakkında nasıl bilgi alacağımıza bakalım:

```bash
$ go doc fmt.Println
func Println(a ...interface()) (n int, err error)
    Println formats using the default formats for its operands and writes to
    standard output. Spaces are always added between operands and a newline
    is appended. It returns the number of bytes written and any write error
    encountered.
```

`go doc` komutunun ürettiği çıktı doğrudan kaynak kod yorumlarından alınır. Paketlerinizi, fonksiyonlarınızı, metotlarınızı ve değişkenlerinizi yeterince yorumladığınız sürece, `go doc` komutu aracılığıyla dokümantasyonu otomatik olarak inceleyebileceksiniz.

## `go get` Komutu

Bu kitapta geliştireceğiniz birçok Go programı üçüncü taraf paketlere ihtiyaç duyacaktır. Paket kaynak kodunu elde etmek için `go get` komutunu kullanın. Örneğin, `stacktitan/ldapauth` paketini içe aktaran aşağıdaki kodu yazdığınızı varsayalım:

```go
package main

import (
    "net/http"
    "github.com/stacktitan/ldapauth"
)
```

`stacktitan/ldapauth` paketini içe aktarmış olsanız da, henüz bu pakete erişemezsiniz. Önce `go get` komutunu çalıştırmanız gerekir. `go get github.com/stacktitan/ldapauth` komutunu kullanmak, paketi indirir ve `GOPATH/src` dizinine yerleştirir.

Aşağıdaki dizin ağacı, `ldapauth` paketinin Go çalışma alanınız (workspace) içindeki konumunu göstermektedir:

```bash
$ tree src/github.com/stacktitan/
src/github.com/stacktitan/
    ldapauth
        LICENSE
        README.md
        ldap_auth.go
```
