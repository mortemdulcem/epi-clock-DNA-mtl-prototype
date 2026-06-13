Çalışan PowerShell sürecine shellcode enjekte ediliyor!
      Kötü planlarınızı gerçekleştirmek istiyor musunuz?
      [Y] Yes [N] No [S] Suspend [?] Help (default is "Y"): Y
      YO FROM GO

`YO FROM Go` mesajı, shellcode'a dönüştürülmüş bir C ikili dosyasının içinden Go yükünü (payload) başarıyla başlattığımızı gösterir. Bu, bir dizi olanağın kapısını aralar.

## Özet

Bu bölümde ele aldığımız konu oldukça fazlaydı ve yine de yalnızca yüzeye değinmiş olduk. Bölüme, Windows API dokümantasyonunda nasıl gezinileceğine dair kısa bir tartışmayla başladık; böylece Windows nesnelerini kullanılabilir Go nesneleriyle (fonksiyonlar, parametreler, veri tipleri ve dönüş değerleri) eşleştirmeye aşina olabilesiniz. Ardından, Go `syscall` paketini kullanırken gerekli olan farklı tür dönüşümlerini gerçekleştirmek için `uintptr` ve `unsafe.Pointer` kullanımını ve kaçınılması gereken olası tuzakları tartıştık. Sonrasında, Windows süreç iç yapılarına etkileşim sağlamak için çeşitli Go sistem çağrılarını kullanan bir süreç enjeksiyonu gösterimiyle tüm parçaları bir araya getirdik.

Bunun ardından, PE dosya formatı yapısını ele aldık ve farklı dosya yapılarını dolaşmak için bir ayrıştırıcı (parser) yazdık. İkili PE dosyada gezinmeyi biraz daha kullanışlı kılan çeşitli Go nesnelerini gösterdik ve bir PE dosyasını arka kapılamak (backdoor) istediğinizde ilgi çekici olabilecek belirgin ofsetlerle bölümü tamamladık.

Son olarak, Go ve yerel C kodunun birlikte çalışabildiği bir araç zinciri (toolchain) inşa ettiniz. Kısaca `CGO` paketinden bahsedip, C kodu örnekleri oluşturmaya ve yerel Go DLL'leri oluşturmak için yeni araçları keşfetmeye odaklandık.

Bu bölümü alın ve öğrendiklerinizi genişletin. Farklı saldırı disiplinlerini durmaksızın inşa edin, kırın ve araştırın. Windows saldırı yüzeyi sürekli evrim geçiriyor; doğru bilgi ve araçlara sahip olmak, saldırı tarafındaki yolculuğunuzu çok daha ulaşılabilir kılacaktır.

---

# 13  
## STEGANOGRAFI İLE VERİ GİZLEME

`Steganography` sözcüğü, Yunanca `steganos` (örtmek, gizlemek veya korumak) ve `graphien` (yazmak) sözcüklerinin birleşiminden oluşur. Güvenlik bağlamında steganografi, veriyi gelecekte bir zamanda çıkartılabilecek şekilde başka verilerin (örneğin bir görüntünün) içine gömerek gizlemek için kullanılan teknik ve prosedürlere karşılık gelir. Güvenlik topluluğunun bir üyesi olarak, hedefe teslim edildikten sonra geri alacağınız yükleri (payload) gizleyerek bu uygulamayı rutin olarak inceleyeceksiniz.

Bu bölümde, veriyi bir Portable Network Graphics (PNG) görüntüsünün içine yerleştireceksiniz. Önce PNG formatını inceleyip PNG verisinin nasıl okunacağını öğreneceksiniz. Ardından, kendi verinizi mevcut görüntünün içine yerleştireceksiniz. Son olarak, yerleştirdiğiniz veriyi şifrelemek ve çözmek için kullanılan bir yöntem olan XOR’u keşfedeceksiniz.

## PNG Formatını Keşfetme

PNG spesifikasyonunu gözden geçirerek başlayalım; bu size PNG görüntü formatını ve bir dosyanın içine veri yerleştirmeyi anlamanızda yardımcı olacak. Teknik spesifikasyonu `http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html` adresinde bulabilirsiniz. Bu doküman, yinelenen bayt parçalarından (byte chunks) oluşan ikili PNG görüntü dosyasının bayt formatına dair ayrıntılar sunar.

Bir PNG dosyasını bir hex editör ile açın ve ilgili her bayt parçası bileşenini, her birinin ne işe yaradığını görmek için gezinerek inceleyin. Biz Linux’ta yerleşik `hexdump` hex editörünü kullanıyoruz, ancak herhangi bir hex editörü işinizi görecektir. Örneğini açacağımız görüntü dosyasını `https://github.com/blackhat-go/bhg/blob/master/ch-13/imgInject/images/battlecat.png` adresinde bulabilirsiniz; ancak tüm geçerli PNG görüntüleri aynı formatı izleyecektir.

### Başlık (Header)

Görüntü dosyasının ilk 8 baytı, `89 50 4e 47 0d 0a 1a 0a` (Şekil 13-1’de vurgulanan) başlık (header) olarak adlandırılır.

```
00806000  89 50 4e 47 0d 0a 1a 0a      00 00 08 0d 49 48 44 52      .PNG......IHDR
00000010  00 00 03 20 00 00 02 58      08 06 00 00 00 90 76 82      ... ...X......v.
00000020  70 00 05 d0 2c 49 44 41      54 78 9c cc bd 07 74 53      p...,IDA Tx....tS
00000030  57 be ef df 3b 93 c0 04      53 d2 48 48 32 10 42 12      W....;...S.HH2.B.
00000040  08 d5 c6 bd f7 2a 17 b9      48 b6 64 15 cb 92 65 d9      ....*..H.d...e.
00000050  72 b7 c1 06 4c ef a1 97      98 32 40 42 31 ee 15 53      r...L....2@B1..S
00000060  43 2f ee b6 7a b3 8a 8b      64 f5 66 d9 a6 85 b7 8f      C/..z...d.f.....
00000070  81 dc cc dc f9 df be fb      bf ef bd 36 77 66 1f 58      .........6wf.X
00000080  df b5 8f 24 97 73 24 6e      9f 33 cf fa ed df de 28      ...$.s$n.3.....(
```

Şekil 13-1: PNG dosyasının başlığı

İkinci, üçüncü ve dördüncü hex değerleri ASCII’ye dönüştürüldüğünde kelimenin tam anlamıyla `PNG` olarak okunur. Sonraki rastgele baytlar hem DOS hem de Unix `Carriage-Return Line Feed` (CRLF) karakterlerinden oluşur. Bir dosyanın sihirli baytları (magic bytes) olarak anılan bu belirli header dizisi, tüm geçerli PNG dosyalarında aynı olacaktır. İçerikteki farklılıklar, birazdan göreceğiniz gibi, kalan parçalarda (chunk) ortaya çıkar.

Bu spesifikasyonu incelerken, PNG formatının Go’daki bir temsilini oluşturmaya başlayalım. Bu, yükleri (payload) gömme konusundaki nihai hedefimize ulaşmamızı hızlandırmaya yardımcı olacak. Başlık 8 bayt uzunluğunda olduğundan, bir `uint64` veri tipine sığdırılabilir; bu nedenle değeri tutacak `Header` adlı bir `struct` oluşturalım (Liste 13-1). (Tüm kod listeleri `/ch-13/imgInject/pnglib/commands.go` kök konumunda, verilen GitHub deposu `https://github.com/blackhat-go/bhg` altında bulunmaktadır.)

```go
// Header holds the first UINT64 (Magic Bytes)
type Header struct {
    Header uint64
}
```

Liste 13-1: `Header` struct tanımı (`/ch-13/imgInject/pnglib/commands.go`)
