PE dosya yapısındaki bir sonraki üstbilgi (header) Optional Header’dır. Çalıştırılabilir bir ikili görüntü (binary image), yürütülebiliri sanal belleğe yükleyen yükleyiciye (loader) önemli veriler sağlayan bir Optional Header’a sahiptir. Bu header içinde çok fazla veri bulunur; bu yapıda gezinmeye alışmanız için yalnızca birkaç öğeye değineceğiz.

Başlamak için, Liste 12-19’da açıklandığı gibi, mimariye bağlı olarak ilgili bayt uzunluğunu ikili (binary) okuma işlemiyle okumamız gerekir. Daha kapsamlı bir kod yazıyor olsaydınız, uygun PE veri yapılarını kullanmak için (örneğin x86 ile x86_64’ü ayırt ederek) kod boyunca mimariyi kontrol etmek isterdiniz.

```go
// Get size of OptionalHeader
var sizeofOptionalHeader32 = uint16(binary.Size(pe.OptionalHeader32{}))
var sizeofOptionalHeader64 = uint16(binary.Size(pe.OptionalHeader64{}))
var oh32 pe.OptionalHeader32
var oh64 pe.OptionalHeader64

// Read OptionalHeader
switch pefile.FileHeader.SizeOfOptionalHeader {
case sizeofOptionalHeader32:
    _ = binary.Read(sr, binary.LittleEndian, &oh32)
case sizeofOptionalHeader64:
    _ = binary.Read(sr, binary.LittleEndian, &oh64)
```

Liste 12-19: Optional Header baytlarını okumak (/ch-12/peParser/main.go)

Bu kod bloğunda iki değişkeni, `sizeOfOptionalHeader32` ve `sizeOfOptionalHeader64`’ü sırasıyla 224 bayt ve 240 bayt ile başlatıyoruz. Bu bir x86 binary olduğu için, kodumuzda ilk değişkeni kullanacağız. Değişken bildirimlerini hemen pe.OptionalHeader32 ve pe.OptionalHeader64 arayüzlerinin (interface) başlatılması takip eder; bu arayüzler Optional Header verisini barındıracaktır. Son olarak bir ikili okuma (binary read) gerçekleştirir ve bunu ilgili veri yapısına aktarırız (marshal): 32 bitlik bir binary’ye göre `oh32`.

Şimdi Optional Header’ın daha dikkate değer bazı öğelerini açıklayalım. Karşılık gelen `print` ifadeleri ve çıktıları Liste 12-20’de verilmiştir.

```go
// Print Optional Header
fmt.Println("[      Optional Header     ]")
fmt.Printf("[+] Entry Point: 0x%x\n", oh32.AddressOfEntryPoint)
fmt.Printf("[+] ImageBase: 0x%x\n", oh32.ImageBase)
fmt.Printf("[+] Size of Image: 0x%x\n", oh32.SizeOfImage)
fmt.Printf("[+] Sections Alignment: 0x%x\n", oh32.SectionAlignment)
fmt.Printf("[+] File Alignment: 0x%x\n", oh32.FileAlignment)
fmt.Printf("[+] Characteristics: %#x\n", pefile.FileHeader.Characteristics)
fmt.Printf("[+] Size of Headers: 0x%x\n", oh32.SizeOfHeaders)
fmt.Printf("[+] Checksum: 0x%x\n", oh32.CheckSum)
fmt.Printf("[+] Machine: 0x%x\n", pefile.FileHeader.Machine)
fmt.Printf("[+] Subsystem: 0x%x\n", oh32.Subsystem)
fmt.Printf("[+] DLLCharacteristics: 0x%x\n", oh32.DllCharacteristics)
```

```text
/* OUTPUT
       Optional Header
[+] Entry Point: 0x169e682
[+] ImageBase: 0x400000
[+] Size of Image: 0x9172000
[+] Sections Alignment: 0x1000
[+] File Alignment: 0x200
[+] Characteristics: 0x102
[+] Size of Headers: 0x400
[+] Checksum: 0x2e41078
[+] Machine: 0x14c
[+] Subsystem: 0x2
[+] DLLCharacteristics: 0x8140
*/
```

Liste 12-20: Optional Header değerlerinin terminal çıktısına yazılması (/ch-12/peParser/main.go)

Amacın bir PE dosyasını backdoor’lamak olduğunu varsayarsak, shellcode konumuna veya Section Table girdilerinin sayısıyla tanımlanan hedef section’a atlamak (memory jump) ve orayı ele geçirmek (hijack) için hem `ImageBase`’i hem de `Entry Point`i bilmeniz gerekir. `ImageBase`, görüntü (image) belleğe yüklendikten sonra görüntünün ilk baytının adresidir; `Entry Point` ise, `ImageBase`’e göre yürütülebilir kodun göreli (relative) adresidir. `Size of Image`, görüntünün belleğe tamamen yüklendiğinde gerçek boyutudur. Eğer shellcode içeren yeni bir section eklerseniz görüntü boyutunda artış olacağı için bu değerin buna uygun olarak ayarlanması gerekir.

`Sections Alignment`, section’lar belleğe yüklendiğinde bayt hizalamasını (alignment) sağlar; `0x1000` oldukça yaygın bir değerdir. `File Alignment`, section’ların ham diskteki bayt hizalamasını verir; `0x200` (512 bayt) da yaygın bir değerdir. Çalışır durumda bir kod elde etmek için bu değerleri değiştirmeniz gerekecek ve tüm bunları manuel yapmayı planlıyorsanız bir hex editör ve hata ayıklayıcı (debugger) kullanmak zorunda kalacaksınız.

Optional Header çok sayıda girdi (entry) içerir. Her birini tek tek açıklamak yerine, her girdiyi kapsamlı şekilde anlamak için https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#optional-header-windows-specific-fields-image-only adresindeki dokümantasyonu incelemenizi öneririz.

## Data Directory’yi Ayrıştırma (Parsing the Data Directory)

Çalışma zamanında (runtime), bir Windows yürütülebilir dosyası, bağlanmış bir DLL’in nasıl tüketileceği (consume) ya da diğer uygulama süreçlerinin (process) yürütülebilirin sunduğu kaynakları nasıl kullanacağı gibi önemli bilgileri bilmek zorundadır. Binary ayrıca iş parçacığı (thread) depolama gibi daha ayrıntılı (granüler) verileri de yönetmek zorundadır. Data Directory’nin birincil işlevi budur.

Data Directory, Optional Header’ın son 128 baytıdır ve özellikle bir ikili görüntüye (binary image) ilişkindir. Bireysel bir dizinin veri konumuna (data location) olan ofset (offset) adresini ve veri boyutunu içeren bir referans tablosunu tutmak için kullanırız. Çekirdek bir Windows başlık dosyası olan `WINNT.H` içinde tam 16 dizin girdisi tanımlanmıştır.
