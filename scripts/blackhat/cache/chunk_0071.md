## BPF Filtresini Oluşturma

BPF filtrenizin, paket aktarımını (transfer) gösteren belirli bayrak (flag) değerlerini kontrol etmesi gerekir. Daha önce bahsettiğimiz bayraklar açık olduğunda, bayrak baytı aşağıdaki değerlere sahip olur:

- ACK ve FIN: `00010001` (`0x11`)
- ACK: `00010000` (`0x10`)
- ACK ve PSH: `00011000` (`0x18`)

Açıklık olması için ikili (binary) değerin onaltılık (hex) karşılığını da ekledik; filtörde kullanacağınız değer bu onaltılık değerdir.

Özetle, TCP başlığının 14. baytını (0 tabanlı indeks için ofset 13) kontrol etmeniz ve bayrakları `0x11`, `0x10` veya `0x18` olan paketleri filtrelemeniz gerekir. BPF filtresi şu şekildedir:

```text
tcp[13] == 0x11 or tcp[13] == 0x10 or tcp[13] == 0x18
```

Harika. Artık filtreniz hazır.

## Tarayıcıyı Oluşturma

Şimdi bu filtreyi kullanarak, tam bir TCP bağlantısı kuran ve üç yönlü el sıkışmanın (three-way handshake) ötesindeki paketleri inceleyen bir yardımcı program (utility) yazacaksınız. Böylece başka paketlerin iletilip iletilmediğini, dolayısıyla gerçekten dinleyen bir servis olup olmadığını tespit edeceksiniz.

Program Liste 8-6’da gösterilmiştir. Basitlik uğruna, kodu verimlilik açısından optimize etmemeyi tercih ettik. Ancak, 2. Bölüm’de yaptığımıza benzer optimizasyonlar uygulayarak bu kodu büyük ölçüde geliştirebilirsiniz.

```go
var (
    snaplen = int32(320)
    promisc = true
    timeout = pcap.BlockForever
    filter = "tcp[13] == 0x11 or tcp[13] == 0x10 or tcp[13] == 0x18"
    devFound = false
    results = make(map[string]int)
)

func capture(iface, target string) {
    handle, err := pcap.OpenLive(iface, snaplen, promisc, timeout)
    if err != nil {
        log.Panicln(err)
    }

    defer handle.Close()

    if err := handle.SetBPFFilter(filter); err != nil {
        log.Panicln(err)
    }

    source := gopacket.NewPacketSource(handle, handle.LinkType())
    fmt.Println("Capturing packets")
    for packet := range source.Packets() {
        networkLayer := packet.NetworkLayer()
        if networkLayer == nil {
            continue
        }

        transportLayer := packet.TransportLayer()
        if transportLayer == nil {
            continue
        }

        srcHost := networkLayer.NetworkFlow().Src().String()
        srcPort := transportLayer.TransportFlow().Src().String()

        if srcHost != target {
            continue
        }
        results[srcPort] += 1
    }
}

func main() {

    if len(os.Args) != 4 {
        log.Fatalln("Usage: main.go <capture_iface> <target_ip> <port1,port2,port3>")
    }

    devices, err := pcap.FindAllDevs()
    if err != nil {
        log.Panicln(err)
    }

    iface := os.Args[1]
    for _, device := range devices {
        if device.Name == iface {
            devFound = true
        }
    }

    if !devFound {
        log.Panicf("Device named '%s' does not exist\n", iface)
    }

    ip := os.Args[2]
    go capture(iface, ip)
    time.Sleep(1 * time.Second)

    ports, err := explode(os.Args[3])
    if err != nil {
        log.Panicln(err)
    }

    for _, port := range ports {
        target := fmt.Sprintf("%s:%s", ip, port)
        fmt.Println("Trying", target)
        c, err := net.DialTimeout("tcp", target, 1000*time.Millisecond)
        if err != nil {
            continue
        }

        c.Close()
    }

    time.Sleep(2 * time.Second)

    for port, confidence := range results {
        if confidence >= 1 {
            fmt.Printf("Port %s open (confidence: %d)\n", port, confidence)
        }
    }
}

/* Extraneous code omitted for brevity */
```

**Liste 8-6**: SYN-flood korumalarıyla paket tarama ve işleme (`/ch-8/syn-flood/main.go`)

## 9  
YAZMA VE PORT ETME  
SÖMÜRÜ (EXPLOIT) KODU

Önceki bölümlerin çoğunda, Go’yu ağ tabanlı saldırılar oluşturmak için kullandınız. Ham TCP, HTTP, DNS, SMB, veritabanı etkileşimi ve pasif paket yakalamayı incelediniz.

Bu bölüm, bunun yerine zafiyetleri (vulnerabilities) belirlemeye ve sömürmeye odaklanıyor. Önce, bir uygulamanın güvenlik zayıflıklarını keşfetmek için bir zafiyet fuzz’layıcı (fuzzer) yazmayı öğreneceksiniz. Ardından, mevcut exploit’leri Go’ya nasıl port edeceğinizi göreceksiniz. Son olarak, popüler araçları kullanarak Go ile uyumlu shellcode üretmeyi göstereceğiz. Bölümün sonunda, Go’yu hem açıkları keşfetmek hem de çeşitli yük/faydalı yükleri (payload) yazıp teslim etmek için nasıl kullanacağınıza dair temel bir anlayışa sahip olmalısınız.

## Bir Fuzzer Oluşturma

Fuzzing, bir uygulamaya büyük miktarda veri göndererek uygulamayı anormal davranış üretmeye zorlamayı amaçlayan bir tekniktir. Bu davranış, daha sonra istismar edebileceğiniz kodlama hatalarını veya güvenlik açıklarını ortaya çıkarabilir.

Bir uygulamayı fuzz’lamak aynı zamanda kaynak tüketimi (resource exhaustion), bellek bozulması (memory corruption) ve hizmet kesintisi gibi istenmeyen yan etkilere de neden olabilir. Bu yan etkilerin bir kısmı hata avcıları (bug hunter) ve exploit geliştiricilerinin işlerini yapabilmeleri için gereklidir; ancak uygulamanın kararlılığı açısından olumsuzdur. Bu nedenle, fuzzing işlemlerini her zaman kontrollü bir laboratuvar ortamında gerçekleştirmeniz kritik önem taşır. Bu kitaptaki çoğu teknikte olduğu gibi, sahibi tarafından açıkça yetkilendirilmemiş uygulamaları veya sistemleri fuzz’lamayın.

Bu bölümde iki fuzzer geliştireceksiniz. İlki, bir girdinin kapasitesini test ederek bir hizmeti çökertmeye ve bir arabellek taşmasını (buffer overflow) tespit etmeye çalışacak. İkinci fuzzer ise bir HTTP isteğini tekrar oynatarak (replay), olası girdi değerlerini döngüsel olarak deneyip SQL enjeksiyonunu (SQL injection) tespit etmeye çalışacak.
