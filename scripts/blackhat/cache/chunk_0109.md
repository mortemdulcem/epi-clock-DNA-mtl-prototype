Her bir üstten aşağı bölümü, PE ayrıştırıcısını (parser) geliştirirken inceleyeceğiz.

## Bir PE Ayrıştırıcı Yazmak

Aşağıdaki bölümler boyunca, Windows ikili (binary) yürütülebilir dosyası içindeki her PE bölümünü analiz etmek için gerekli olan ayrıştırıcı bileşenlerini yazacağız. Örnek olarak, https://telegram.org adresinde bulunan Telegram mesajlaşma uygulaması ikili dosyasıyla ilişkili PE formatını kullanacağız; çünkü bu uygulama, sıkça kullanılan putty SSH ikili örneğine göre daha az basit ve PE formatında dağıtılıyor. Neredeyse herhangi bir Windows ikili yürütülebilir dosyasını kullanabilirsiniz ve başka dosyaları da araştırmanızı teşvik ediyoruz.

## PE İkilisini Yükleme ve Dosya G/Ç (I/O)

Liste 12-14’te, Telegram ikilisini daha ileri ayrıştırmaya hazırlamak için Go `pe` paketini kullanarak başlayacağız. Bu ayrıştırıcıyı yazarken oluşturduğumuz tüm kodu tek bir dosyada `main()` fonksiyonu içinde tutabilirsiniz.

```go
import (
   "debug/pe"
   "encoding/binary"
   "fmt"
   "ion
   "log"

func main() {
    f, err := os.Open("Telegram.exe")
    check(err)
    pefile, err := pe.NewFile(f)
    check(err)
    defer f.Close()
    defer pefile.Close()
```

**Liste 12-14: PE ikili dosyası için Dosya G/Ç (/ch-12/peParser/main.go)**

Her bir PE yapı bileşenini incelemeden önce, Go `pe` paketini kullanarak ilk `import` ve dosya G/Ç (I/O) kısmını iskelet (stub) olarak hazırlamamız gerekir. Sırasıyla bir dosya tanıtıcısı (file handle) ve bir PE dosya nesnesi oluşturmak için `os.Open()` ve ardından `pe.NewFile()` kullanıyoruz. Bu gerekli, çünkü PE dosya içeriğini bir `Reader` nesnesi (örneğin bir dosya veya ikili (binary) okuyucu) kullanarak ayrıştırmayı amaçlıyoruz.

## DOS Başlığını (Header) ve DOS Stub’ını Ayrıştırma

Şekil 12-6’da gösterilen, yukarıdan aşağı PE veri yapısının ilk bölümü bir DOS başlığıyla başlar. Aşağıdaki benzersiz değer her Windows DOS-tabanlı yürütülebilir ikili dosyada daima mevcuttur: `0x4D 0x5A` (veya ASCII’de `MZ`), ki bu da dosyayı yerinde bir şekilde bir Windows yürütülebilir dosyası olarak tanımlar. Tüm PE dosyalarında evrensel olarak mevcut olan diğer bir değer, `0x3C` ofsetinde bulunur. Bu ofsetteki değer, bir PE dosyasının imzasını içeren başka bir ofsete işaret eder: yerinde bir şekilde `0x50 0x45 0x00 0x00` (veya ASCII’de `PE`).

Hemen ardından gelen başlık, her zaman “This program cannot be run in DOS mode” ifadesi için onaltılık (hex) değerleri sağlayan DOS Stub’dır; istisna, bir derleyicinin `/STUB` bağlayıcı (linker) seçeneğiyle keyfi bir string değeri sağlamasıdır. Favori hex düzenleyicinizi (editor) alıp Telegram uygulamasını açarsanız, Şekil 12-7’ye benzer olmalıdır. Tüm bu değerler mevcuttur.

```
 Offmet(b) 00 01 02 03 04 05 06 07 08 09 OA OB OC OD OE OF Decoded tea
 00000000   4D5A900O03000O0004000o00FpFy0O0o CI
 00000010       0 GO 00 00 00 00 00 40 00 00 00 00 00 00 00
 00000020   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 00000030   00 00 00 00 00 00 00 00 00 00 00 00 50 01 00 00                 X
 00000040   OE IF BA OE 00 84 09 CD 21 148 01 4C     I 54 68 .....".f!,.Lf!Th
 00000050   69 73 20 70 72 6F 67 72 61 60 20 63 61 6E 66 SF is program casino
 00000060   74 20 62 65 20 72 75 6E20 69 66 20 44 4F53 20 t be run 1n DOS
 00000070   6D 6F 64 65 26 OD OD OA 24 00 00 00 00 00 GO 00 mode....5
 00000080   13 DD C2 16 57 BC AC 4D 57 BC AC 4D 57 BC AC 4D .A.PP*41144,14FP4-24
 00000090   32 DA AF 4C 68 BC AC 4032 DA A9 4C BC BC AC 40 2D-thh-.142D01L54-24
 000000A0   C9 IC 63 40 50 BC AC 40 D6 07 AY 4C 64 BC AC 4D 6.1031F4*-246.-Ld4-21
 00000080   D6 07 AS 4C DI BC AC 40 06 07 A8 4C 7E BC AC 4D DaDISB0440. -L.0t44
 00000000   C6 05 A9 4C 80 BE AC 40 57 BC AC 4D 66 BC AC 40 Eatt.IrreSP*41144-.M
 000000D0   C4 D5 AS 4C 1C BD AC 4D 61 DO Al 4C 43 BC AC 4D AO L.1/2-,MaD-LC24-24
 000000E0   61 DO AB 4C 70 BE AC 4D 23 D7 AS 4C 50 BC AC 4D aD-LIM,H#0. -LF44-21
 000000F0   C6 05 AS 4C 64 BC AC 40 32 DA AB 4C 56 BC AC 40 JEO-IS4.-.M2taLVII,B
 00000100   32 DA AS 40 68 BC AC 4D 32 DA AA 4C 56 BC AC 40 2D-Lkit-1921aLiMe-24
 00000110   32 DA ID 4C 4A BC AC 40 57 BC AD 40 09 BE AC 40 215.1411hars.H.N-24
 00000120   61 DO AS 4C 33 BE AC 40 61 DO AC 4C 56 BC AC 40 aDATI.34-41aB,LV1/4-2(
 00000190   61 DO 53 40 56 BC AC 40 57 BC 38 40 56 BC AC 40 a051.0The-AMP4:14V4-21
 00000140   61 DO AK 4C 56 BC AC 4D 52 69 63 68 57 BC   gg4D &EC
 00000150   00 00 00 00 00 00 00 00150 45 00 17014C 01 00 00           PE
```

**Şekil 12-7: Tipik bir PE ikili biçimi dosya başlığı**

Şimdiye kadar, DOS Header ve Stub’ı anlattık ve bir hex editörle onaltılık gösterimlerini inceledik. Şimdi, Liste 12-15’te verildiği üzere, aynı değerleri Go kodu ile ayrıştırmaya bakalım.

```go
dosHeader := make(Mbyte, 96)
sizeOffset := make([lbyte, 4)

// Dec to Ascii (searching for MZ)
err = f.Read(dosHeader) 0
check (err)
fmt.Println("[      DOS Header / Stub    ]")
fmt.Printf("[+] Magic Value: %s%s\n", string(dosHeader[0]), string(dosHeader[1]))

// Validate PE+0+0 (Valid PE format)
pe_sig_offset := int64(binary.LittleEndian.Uint32(dosHeader[Ox3c:11) 0
f.ReadAt(sizeOffset[:], pe_sig_offset) 0
fmt.Println("[     Signature Header      ]")
fmt.Printf("[+] LFANEW Value: %s\n", string(sizeOffset))
```

```text
/* OUTPUT
[     DOS Header / Stub
[+] Magic Value: MZ
[     Signature Header          ]
[+] LFANEW Value: PE
```

**Liste 12-15: DOS Başlığı ve Stub değerlerinin ayrıştırılması (/ch-12/peParser/main.go)**
