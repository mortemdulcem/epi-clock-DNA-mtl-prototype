## Port Yönlendirme ile Güvenlik Duvarlarını Atlatma

İnsanlar, güvenlik duvarlarını (firewall) belirli sunuculara ve portlara istemcilerin bağlanmasını engelleyecek, diğerlerine ise erişime izin verecek şekilde yapılandırabilirler. Bazı durumlarda, bir ara sistemi kullanarak bağlantıyı güvenlik duvarının etrafından veya içinden dolaylı olarak geçirerek bu kısıtlamaları aşabilirsiniz; bu tekniğe port yönlendirme (port forwarding) denir.

Birçok kurumsal ağ, iç varlıkların kötü amaçlı sitelere HTTP bağlantısı kurmasını kısıtlar. Bu örnek için, evil.com adlı kötü niyetli bir site hayal edin. Bir çalışan evil.com adresine doğrudan göz atmaya çalışırsa, bir güvenlik duvarı isteği engeller. Ancak, çalışan güvenlik duvarı üzerinden geçmesine izin verilen harici bir sisteme (örneğin, stacktitan.com) sahipse, bu çalışan tanınan/izinli alan adını kullanarak evil.com’a giden bağlantıları sekebilir (bounce). Şekil 2-2 bu kavramı göstermektedir.

```
              Request                  Request
         —                            — traverses —0-                   Traffic proxied
             stacktitan.com                                               to evil.com
                                             firewall

  Client                                                 stacktitan.com
```

Şekil 2-2: Bir TCP vekil sunucusu (proxy)

Bir istemci, bir güvenlik duvarının içinden, hedef konak `stacktitan.com`’a bağlanır. Bu konak, bağlantıları `evil.com` konağına iletecek şekilde yapılandırılmıştır. Güvenlik duvarı `evil.com`’a doğrudan bağlantıları yasaklarken, burada gösterilene benzer bir yapılandırma, istemcinin bu koruma mekanizmasını atlatmasına ve `evil.com`’a erişmesine izin verebilir.

Port yönlendirmeyi, çeşitli kısıtlayıcı ağ yapılandırmalarını kötüye kullanmak için kullanabilirsiniz. Örneğin, bir atlama kutusu (jump box) üzerinden yönlendirme yaparak bölümlere ayrılmış (segmented) bir ağa erişebilir veya kısıtlayıcı arayüzlere (interface) bağlı portlara erişim sağlayabilirsiniz.

## Bir TCP Tarayıcı (Scanner) Yazmak

TCP portlarının etkileşimini kavramsallaştırmanın etkili yollarından biri, bir port tarayıcı (port scanner) gerçekleştirmektir. Böyle bir tarayıcı yazarak, bir TCP el sıkışması (handshake) sırasında gerçekleşen adımları ve karşılaşılan durum değişimlerinin etkilerini gözlemleyeceksiniz; bu sayede bir TCP portunun kullanılabilir olup olmadığını veya kapalı ya da filtrelenmiş (filtered) durumda cevap verip vermediğini belirleyebileceksiniz.

Temel bir tarayıcı yazdıktan sonra, daha hızlı çalışan bir tane yazacaksınız. Bir port tarayıcı, tek bir ardışık (contiguous) yöntemle birkaç portu tarayabilir; ancak amacınız tüm 65.535 portu taramak olduğunda bu oldukça zaman alıcı olabilir. Eşzamanlılığı (concurrency) kullanarak, verimsiz bir port tarayıcıyı daha büyük port tarama görevleri için daha uygun hale getirmeyi inceleyeceksiniz.

Bu bölümde öğreneceğiniz eşzamanlılık kalıplarını (concurrency patterns), hem bu kitapta hem de ötesinde birçok başka senaryoda uygulayabileceksiniz.

### Port Kullanılabilirliğini Test Etme

Port tarayıcı oluşturmanın ilk adımı, bir istemciden sunucuya bağlantı başlatmanın nasıl yapılacağını anlamaktır. Bu örnek boyunca, Nmap projesi tarafından işletilen bir servis olan `scanme.nmap.org`’a bağlanacak ve bu adresi tarayacaksınız. Bunu yapmak için Go’nun `net` paketini kullanacaksınız: `net.Dial(network, address string)`.

İlk argüman, başlatılacak bağlantı türünü tanımlayan bir stringtir. Bunun nedeni, `Dial` fonksiyonunun yalnızca TCP için kullanılmamasıdır; Unix soketleri (Unix sockets), UDP ve yalnızca kafanızda var olan Katman 4 (Layer 4) protokoller için bağlantılar oluşturmakta da kullanılabilir (yazarlar bu yoldan geçmişlerdir; kısaca söylemek gerekirse, TCP gayet iyidir). Sağlayabileceğiniz birkaç string vardır, ancak kısalık adına bu örnekte `tcp` stringini kullanacaksınız.

İkinci argüman, `Dial(network, address string)` fonksiyonuna bağlanmak istediğiniz konağı bildirir. Bunun tek bir string olduğuna, bir string ve bir `int` olmadığına dikkat edin. IPv4/TCP bağlantıları için bu string `host:port` biçimini alır. Örneğin, `scanme.nmap.org` adresine TCP port 80 üzerinden bağlanmak isteseydiniz, `scanme.nmap.org:80` değerini sağlardınız.

Artık bir bağlantı oluşturmayı biliyorsunuz; peki bağlantının başarılı olup olmadığını nasıl anlayacaksınız? Bunu hata kontrolüyle yapacaksınız: `Dial(network, address string)` fonksiyonu `Conn` ve `error` döndürür ve bağlantı başarılıysa `error` `nil` olur. Dolayısıyla, bağlantınızı doğrulamak için yapmanız gereken tek şey, `error`’ın `nil` olup olmadığını kontrol etmektir.

Artık tek port tarayıcı (single port scanner) oluşturmak için gereken tüm parçalara sahipsiniz; nezaketsiz (impolite) bir tarayıcı da olsa. Liste 2-1, bunları nasıl bir araya getireceğinizi gösteriyor. (Kök dizinde `/` yer alan tüm kod listeleri, sağlanan GitHub deposu `https://github.com/blackhat-go/bhg` altında bulunur.)

```go
package main

import (
   "fmt"
   "net"
)

func main() {
    _, err := net.Dial("tcp", "scanme.nmap.org:80")
    if err == nil {
        fmt.Println("Connection successful")
    }
}
```

Liste 2-1: Yalnızca bir portu tarayan basit bir port tarayıcı (`/ch-2/dial/main.go`)

Bu kodu çalıştırın. Harika bilgi otoyoluna (internet) erişiminiz varsa `Connection successful` çıktısını görmelisiniz.

## Eşzamanlı Olmayan (Nonconcurrent) Tarama Gerçekleştirme

Tek seferde yalnızca bir portu taramak pek kullanışlı değildir, verimli hiç değildir. TCP portları 1’den 65.535’e kadar uzanır; ancak test için 1’den 1024’e kadar olan portları tarayalım. Bunu yapmak için bir `for` döngüsü kullanabilirsiniz:

```go
for i := 1; i <= 1024; i++ {
    // ...
}
```
