```go
    for _, device := range devices {
        if device.Name == iface {
            devFound = true
        }
    }

    if !devFound {
        log.Panicf("Device named '%s does not exist\n", iface)
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
        appLayer := packet.ApplicationLayer()
        if appLayer == nil {
            continue
        }

        payload := appLayer.Payload()
        if bytes.Contains(payload, []byte("USER")) {
            fmt.Print(string(payload))
        } else if bytes.Contains(payload, []byte("PASS")) {
            fmt.Print(string(payload))
        }
    }
```

**Liste 8-5: FTP kimlik doğrulama kimlik bilgilerinin yakalanması (`ch-8/ftp/main.go`)**

Yaptığınız değişiklikler yalnızca yaklaşık 10 satır kodu kapsıyor. İlk olarak, BPF filtrenizi yalnızca port 21’e (FTP trafiği için yaygın olarak kullanılan port) giden trafiği yakalayacak şekilde değiştiriyorsunuz (❶). Paketleri işlemeye başlayana kadar kodun geri kalanı aynı kalıyor.

Paketleri işlemek için önce paketten uygulama katmanını (application layer) çıkarıyor ve gerçekten var olup olmadığını kontrol ediyorsunuz (❷); çünkü FTP komutları ve verileri uygulama katmanında bulunur. Uygulama katmanını, `packet.ApplicationLayer()` çağrısının döndürdüğü değerin `nil` olup olmadığını inceleyerek bulursunuz. Uygulama katmanı pakette mevcutsa, `appLayer.Payload()` ❸ çağrısı ile bu katmandan yükü/faydalı yükü (payload; FTP komutları/verileri) çıkarırsınız.

(Benzer şekilde, diğer katmanları ve verileri çıkarmak ve incelemek için de yöntemler vardır, ancak burada yalnızca uygulama katmanı yüküne/faydalı yüküne ihtiyacınız var.) Yükü/faydalı yükü çıkardıktan sonra, bunun `USER` veya `PASS` komutlarını içerip içermediğini kontrol edersiniz ❹; bu da paketin bir oturum açma dizisinin parçası olduğunu gösterir. Eğer öyleyse, yükü/faydalı yükü ekrana yazdırırsınız.

İşte bir FTP oturum açma girişimini yakalayan örnek bir çalışma:

```bash
$ go build -o ftp
$ sudo ./ftp
USER someuser
PASS password
```

Elbette bu kodu geliştirebilirsiniz. Bu örnekte, `USER` veya `PASS` kelimeleri yük/faydalı yük içinde herhangi bir yerde geçiyorsa yük/faydalı yük görüntülenecektir. Aslında kod, bu anahtar sözcükler istemci ve sunucu arasında aktarılan dosya içeriğinin bir parçası olduğunda veya `PASSAGE` ya da `ABUSER` gibi daha uzun bir kelimenin parçası olduğunda ortaya çıkan yanlış pozitifleri elemek için yalnızca yükün/faydalı yükün başlangıcını aramalıdır. Bu iyileştirmeleri bir öğrenme egzersizi olarak yapmanızı teşvik ediyoruz.

## SYN-flood Koruması Altında Port Tarama

Bölüm 2’de bir port tarayıcı oluşturmayı adım adım incelemiştiniz. Kodu, doğru sonuçlar üreten yüksek performanslı bir uygulama elde edene kadar birden çok yineleme ile geliştirdiniz. Ancak bazı durumlarda bu tarayıcı hâlâ hatalı sonuçlar üretebilir. Özellikle, bir organizasyon SYN-flood korumaları kullandığında, tipik olarak tüm portlar—açık, kapalı ve filtreli—portun açık olduğunu göstermek için aynı paket alışverişini üretir. SYN cookies olarak bilinen bu korumalar, SYN-flood saldırılarını engeller ve saldırı yüzeyini belirsizleştirerek yanlış pozitiflere yol açar.

Hedef SYN cookies kullanıyorsa, bir servisin bir portta dinleyip dinlemediğini ya da bir cihazın portu sahte olarak açık gösterdiğini nasıl belirlersiniz? Sonuçta, her iki durumda da TCP üç yönlü el sıkışması (three-way handshake) tamamlanır. Çoğu araç ve tarayıcı (Nmap dahil), portun durumunu belirlemek için bu diziyi (veya seçtiğiniz tarama türüne bağlı olarak bunun bir varyasyonunu) inceler. Dolayısıyla, bu araçların doğru sonuçlar üreteceğine güvenemezsiniz.

Ancak, bir bağlantı kurduktan sonra ne olduğuna—örneğin bir servis banner’ı (service banner) biçimindeki veri alışverişine—bakarsanız, gerçekte bir servisin yanıt verip vermediğini çıkarabilirsiniz. SYN-flood korumaları, genellikle bir servis dinlemediği sürece ilk üç yönlü el sıkışması sonrasındaki paket alışverişlerine devam etmez; bu nedenle, ek paketlerin varlığı bir servisin mevcut olduğunu gösterebilir.

## TCP Bayraklarını (Flag) Kontrol Etme

SYN cookies’leri hesaba katmak için, üç yönlü el sıkışmanın ötesine bakacak şekilde port tarama yeteneklerinizi genişletmeniz ve bağlantı kurduktan sonra hedeften ek paketler alıp almadığınızı kontrol etmeniz gerekir. Bunu, paketleri koklayarak (sniff) ve bunlardan herhangi birinin ek, meşru servis iletişimlerini gösteren TCP bayrak değerleriyle gönderilip gönderilmediğini inceleyerek yapabilirsiniz.

TCP bayrakları, bir paket aktarımının durumu hakkında bilgi verir. TCP spesifikasyonuna bakarsanız, bayrakların paket başlığında 14. pozisyonda yer alan tek bir bayt içinde saklandığını görürsünüz. Bu bayttaki her bit tek bir bayrak değerini temsil eder. İlgili pozisyondaki bit 1 olarak ayarlanmışsa bayrak “açık”, 0 ise “kapalı”dır. Tablo 8-1’de, TCP spesifikasyonuna göre bayrakların bayt içindeki pozisyonları gösterilmektedir.

**Tablo 8-1: TCP Bayrakları ve Bayt İçindeki Pozisyonları**

| Bit  | 7   | 6   | 5   | 4   | 3   | 2   | 1   | 0   |
|------|-----|-----|-----|-----|-----|-----|-----|-----|
| Flag | CWR | ECE | URG | ACK | PSH | RST | SYN | FIN |

İlgilendiğiniz bayrakların pozisyonlarını öğrendikten sonra, bunları kontrol eden bir filtre oluşturabilirsiniz. Örneğin, aşağıdaki bayrakları içeren paketleri arayabilirsiniz; bunlar dinleyen bir servisin göstergesi olabilir:

- ACK ve FIN  
- ACK  
- ACK ve PSH  

`gopacket` kütüphanesini kullanarak belirli paketleri yakalama ve filtreleme yeteneğine sahip olduğunuz için, uzak bir servise bağlanmaya çalışan, paketleri koklayan ve yalnızca bu TCP başlıklarına sahip paketlerle iletişim kuran servisleri gösteren bir yardımcı program (utility) oluşturabilirsiniz. Diğer tüm servislerin, SYN cookies nedeniyle sahte biçimde “açık” olduğunu varsayabilirsiniz.
