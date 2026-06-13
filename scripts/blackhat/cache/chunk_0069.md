176   bölümler

Kod, paket yakalamayı ayarlamak için gerekli birkaç değişken tanımlayarak başlar 0. Bunlar arasında, veriyi hangi arayüz (interface) üzerinde yakalamak istediğinizin adı, anlık görüntü uzunluğu (snapshot length; her çerçeve için yakalanacak veri miktarı), promisc değişkeni (karışık dinleme modu, yani promiscuous mode, kullanıp kullanmayacağınızı belirler) ve zaman aşımı (time-out) bulunur. Ayrıca, `tcp and port 80` şeklinde bir BPF filtresi tanımlarsınız. Bu, sadece bu ölçütlerle eşleşen paketleri yakalamanızı sağlar.

`main()` fonksiyonunuzun içinde, kullanılabilir aygıtları (devices) listelersiniz 0 ve istediğiniz yakalama arayüzünün aygıt listenizde bulunup bulunmadığını belirlemek için bunlar üzerinde döngüye girersiniz 0. Arayüz adı listede yoksa, bunun geçersiz olduğunu belirterek `panic` çağırırsınız.

`main()` fonksiyonunun geri kalanında ise yakalama mantığınız bulunur. Yüksek seviyede bakarsak, öncelikle paketleri okumanıza ve enjekte etmenize izin veren bir `*pcap.Handle` elde etmeniz veya oluşturmanız gerekir. Bu handle’ı kullanarak bir BPF filtresi uygulayabilir ve buradan paketleri okuyabileceğiniz yeni bir paket veri kaynağı (packet data source) oluşturabilirsiniz.

Kodda `handle` adı verilen `*pcap.Handle`’ı, `pcap.OpenLive()` 0 fonksiyonunu çağırarak oluşturursunuz. Bu fonksiyon bir arayüz adı, anlık görüntü uzunluğu, promiscuous olup olmadığını belirleyen bir boolean değer ve bir zaman aşımı değeri alır. Bu giriş değişkenlerinin hepsi, daha önce ayrıntılı biçimde açıkladığımız gibi `main()` fonksiyonundan önce tanımlanmıştır. Handle için BPF filtresini ayarlamak amacıyla `handle.SetBPFFilter(filter)` çağrısını yapar 0 ve ardından `gopacket.NewPacketSource(handle, handle.LinkType())` fonksiyonunu çağırırken `handle`’ı girdi olarak kullanarak yeni bir paket veri kaynağı oluşturursunuz 0. İkinci girdi olan `handle.LinkType()`, paketleri işlerken hangi çözücünün (decoder) kullanılacağını tanımlar. Son olarak, `source.Packets()` 0 üzerinde döngü kurarak hattaki (wire) paketleri gerçekten okursunuz; bu fonksiyon bir kanal (channel) döndürür.

Bu kitaptaki önceki örneklerden hatırlayabileceğiniz gibi, bir kanal üzerinde döngü yaptığınızda, kanaldan okunacak veri olmadığında döngü bloke olur. Bir paket geldiğinde, bu paketi okur ve içeriğini ekrana yazdırırsınız.

Çıktı, Liste 8-4’e benzer görünmelidir. Programın, ağdan ham içerik (raw content) okuduğumuz için ayrıcalıklı (yükseltilmiş) yetkiler gerektirdiğini unutmayın.

```bash
$ go build -o filter 218. sudo ./filter
PACKET: 74 bytes, wire length 74 cap length 74 @ 2020-04-26 08:44:43.074187 -0500 CDT
  Layer 1 (14 bytes) = Ethernet     {Contents=[. .14..] Payload=[. .60..]
SrcMAC=00:1c:42:cf:57:11 DstM4C=90:72:40:04:33:c1 EthernetType=IPv4 Length=0I
- Layer 2 (20 bytes) = IPv4         gontents=[..20..] Payload=[. .40..] Version=4 IHL=5
T0S=0 Length=60 Id=998 Flags=DF FragOffset=0 TTL=64 Protoco1=TCP Checksum=55712
SrcIP=10.0.1.20 DstIP=54.164.27.126 Options=[] Padding-4H
  Layer 3 (40 bytes) = TCP          {Contents=[. .40..] Payload=[] SrcPort=51064
DstPort=80(http) Seq=3543761149 Ack=0 DataOffset=10 FIN=false SYN=true RST=false
PSH=false ACK=false URG=false ECE=false CWR=false P45=   -false Window=29200
Checksum=23908 Urgent=0 Options=[. .5..] Padding=[]}

PACKET: 74 bytes, wire length 74 cap length 74 @ 2020-04-26 08:44:43.086706 -0500 CDT
- Layer 1 (14 bytes) = Ethernet    {Contents=[. .14..] Payload=[. .60..]
SrcMAC=00:1c:42:cf:57:11 D5tMAC=90:72:40:04:33:c1 EthernetType=IPv4 Length=01
  Layer 2 (20 bytes) = IPv4        {Contents=[..20..] Payload=[. .40..] Version=4 IHL=5
TOS=0 Length=60 Id=23414 Flags=DF FragOffset=0 TTL=64 Protoco1=TCP Checksum=16919
SrcIP=10.0.1.20 DstIP=204.79.197.203 Options=[] Padding=[]}
- Layer 3 (40 bytes) = TCP        {Contents=[. .40..] Payload=[] SrcPort=37314
DstPort=80(http) Seq=2821118056 Ack=0 DataOffset=10 FIN=false SYN=true R5T=false
P5H=false ACK=false URG=false ECE=false CWR=false N5=false Window=29200
Checksum=40285 urgent=o Options=[. .5..] Padding=(]}
```

Liste 8-4: stdout’a kaydedilen yakalanmış paketler

Ham çıktı çok kolay sindirilebilir olmasa da, her katmanın güzel bir şekilde ayrıldığını görüyoruz. Şimdi `packet.ApplicationLayer()` ve `packet.Data()` gibi yardımcı fonksiyonları kullanarak tek bir katmanın veya tüm paketin ham baytlarını elde edebilirsiniz. Bu çıktıyı `hex.Dump()` ile birleştirerek içeriği çok daha okunabilir bir formatta gösterebilirsiniz. Bununla kendi başınıza oynayın.

## Düz Metin Kullanıcı Kimlik Bilgilerini Koklama ve Gösterme

Şimdi yeni oluşturduğunuz kodun üzerine bir şeyler koyalım. Başka araçların sağladığı bazı işlevleri kopyalayarak düz metin (cleartext) kullanıcı kimlik bilgilerini koklayıp göstereceksiniz.

Çoğu organizasyon artık, veriyi yayın (broadcast) olarak göndermek yerine iki uç nokta arasında doğrudan ileten anahtarlamalı (switched) ağlar kullanıyor; bu da kurumsal ortamlarda trafiği pasif olarak yakalamayı zorlaştırıyor. Ancak, aşağıda açıklanan düz metin koklama saldırısı; Adres Çözümleme Protokolü (Address Resolution Protocol, ARP) zehirleme (poisoning) gibi, anahtarlamalı bir ağda uç noktaları kötü amaçlı bir aygıtla iletişim kurmaya zorlayabilen bir saldırıyla birlikte kullanıldığında veya ele geçirilmiş bir kullanıcı iş istasyonundan (workstation) dışa giden trafiği gizlice kokladığınız durumlarda faydalı olabilir. Bu örnekte, bir kullanıcı iş istasyonunu ele geçirdiğinizi varsayacağız ve kodu kısa tutmak için yalnızca FTP kullanan trafiği yakalamaya odaklanacağız.

Birkaç küçük değişiklik dışında, Liste 8-5’teki kod, Liste 8-3’teki koda neredeyse aynıdır.

```go
package main

import (
   "bytes"
   "fmt t
   "log"

   "github.com/google/gopachet "
   "github.com/google/gopacket/pcap"

var (
    iface    = "enp0s5"
    snaplen = int32(1600)
    promisc    false
    timeout = pcap.BlockForever
 0 filter = "tcp and dst port 21"
    devFound = false

func main() f
    devices, err := pcap.FindAllDevs()
    if err != nil f
        log.Panicln(err)
```
