### pcap Alt Paketini Kullanarak Cihazları Tanımlama

Ağ trafiğini yakalamadan önce, üzerinde dinleme yapabileceğiniz kullanılabilir cihazları (arayüzleri) tanımlamanız gerekir. Bunu `gopacket/pcap` alt paketini kullanarak kolayca yapabilirsiniz; bu paket, `pcap.FindAllDevs() (ifs []Interface, err error)` yardımcı fonksiyonu ile cihazları getirir. Liste 8-1, tüm kullanılabilir arayüzleri listelemek için bunu nasıl kullanabileceğinizi gösterir. (Kök dizindeki `/` altındaki tüm kod listeleri, verilen GitHub deposu `https://github.com/blackhat-go/bhg` altında bulunur.)

```go
package main

import (
    "fmt"
    "log"

    "github.com/google/gopacket/pcap"
)

func main() {
    devices, err := pcap.FindAllDevs()
    if err != nil {
        log.Panicln(err)
    }

    for _, device := range devices {
        fmt.Println(device.Name)
        for _, address := range device.Addresses {
            fmt.Printf("     IP:      %s\n", address.IP)
            fmt.Printf("    Netmask: %s\n", address.Netmask)
        }
    }
}
```

**Liste 8-1: Kullanılabilir ağ cihazlarının listelenmesi (`/ch-8/identify/main.go`)**

Cihazlarınızı `pcap.FindAllDevs()` fonksiyonunu çağırarak listelersiniz. Ardından bulunan cihazlar üzerinde döngüye girersiniz. Her bir cihaz için `device.Name` gibi çeşitli özelliklere erişirsiniz. Ayrıca, `pcap.InterfaceAddress` türünde bir slice olan `Addresses` özelliği üzerinden IP adreslerine erişirsiniz. Bu adresler üzerinde de döngüye girer, IP adresini ve netmask değerini ekrana yazdırırsınız.

Aracınızı çalıştırmak, Liste 8-2’ye benzer bir çıktı üretir.

```bash
$ go run main.go
enp0s5
      IP:      10.0.1.20
      Netmask: ffffff00
      IP:      fe80::553a:14e7:92d2:13.413
      Netmask: ffffffiffffffffffoo00000000000000
any
lo
      IP:      127.0.0.1
      Netmask: ffoo0000
      IP:       ::1
      Netmask: ffffffffffffffffffffififffffffff
```

**Liste 8-2: Kullanılabilir ağ arayüzlerini gösteren çıktı**

Bu çıktı, kullanılabilir ağ arayüzlerini—`enp0s5`, `any` ve `lo`—ve bunların IPv4/IPv6 adreslerini ve netmask değerlerini listeler. Sisteminize ait çıktı büyük ihtimalle buradaki ağ ayrıntılarından farklı olacaktır, fakat bilgileri anlamlandırmanıza yetecek kadar benzer olmalıdır.

### Canlı Yakalama ve Sonuçları Filtreleme

Artık kullanılabilir cihazları nasıl sorgulayacağınızı bildiğinize göre, `gopacket` özelliklerini kullanarak kablodan gelen paketleri canlı olarak yakalayabilirsiniz. Bunu yaparken, BPF sözdizimini kullanarak paket kümesini filtreleyeceksiniz. BPF, yakaladığınız ve gösterdiğiniz içeriği kısıtlamanıza, böylece yalnızca ilgili trafiği görmenize olanak tanır. Genellikle protokol ve porta göre trafiği filtrelemek için kullanılır. Örneğin, hedefi port 80 olan tüm TCP trafiğini görmek üzere bir filtre oluşturabilirsiniz. Trafiği hedef konağa göre de filtreleyebilirsiniz. BPF sözdiziminin tam bir tartışması bu kitabın kapsamı dışındadır. BPF’yi kullanmanın ek yolları için `http://www.tcpdump.org/manpages/pcap-filter.html` adresine göz atın.

Liste 8-3, yalnızca port 80’e giden veya port 80’den gelen TCP trafiğini yakalamanız için trafiği filtreleyen kodu göstermektedir.

```go
package main

import (
    "fmt"
    "log"

    "github.com/google/gopacket"
    "github.com/google/gopacket/pcap"
)

var (
    iface    = "enp0s5"
    snaplen  int32 = 1600
    promisc        = false
    timeout        = pcap.BlockForever
    filter         = "tcp and port 80"
    devFound       = false
)

func main() {
    devices, err := pcap.FindAllDevs()
    if err != nil {
        log.Panicln(err)
    }

    for _, device := range devices {
        if device.Name == iface {
            devFound = true
        }
    }

    if !devFound {
        log.Panicf("Device named '%s' does not exist\n", iface)
    }

    handle, err := pcap.OpenLive(iface, snaplen, promisc, timeout)
    if err != nil {
        log.Panicln(err)
    }
    defer handle.Close()

    if err := handle.SetBPFFilter(filter); err != nil {
        log.Panicln(err)
    }

    source := gopacket.NewPacketSource(handle, handle.LinkType())
    for packet := range source.Packets() {
        fmt.Println(packet)
    }
}
```

**Liste 8-3: Belirli ağ trafiğini yakalamak için bir BPF filtresi kullanma (`/ch-8/filter/main.go`)**
