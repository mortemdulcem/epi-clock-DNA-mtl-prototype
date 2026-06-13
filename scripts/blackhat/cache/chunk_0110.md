Windows System Etkileşimi ve Analizi

Başlangıçtan itibaren dosyanın başını kullanarak, bir Go `file Reader` örneğiyle 96 bayttan itibaren okuma yapıp ilk ikili imzayı (binary signature) doğrularız. İlk 2 baytın ASCII olarak `MZ` değeri sağladığını hatırlayın. `pe` paketi, PE veri yapılarını daha kolay tüketilebilir bir şeye dönüştürmeye yardımcı olacak kullanışlı nesneler sunar. Ancak buna rağmen, oraya ulaşmak için manuel ikili okuyucular (binary reader) ve bit düzeyinde (bitwise) işlevsellik gerekecektir. `0x3c`’te referans verilen ofset değerini ikili okuma (binary read) ile okuruz ve ardından tam olarak 4 bayt okuruz; bunlar, `0x50 0x45` (PE) değerini ve ardından 2 adet `0x00` baytını içerir.

### COFF Dosya Başlığını Ayrıştırma

PE dosya yapısında aşağı doğru ilerlediğimizde, DOS Stub’dan hemen sonra COFF File Header bulunur. COFF File Header’ı Liste 12-16’da tanımlanan kodu kullanarak ayrıştıralım ve sonra bazı ilginç özelliklerini tartışalım.

```go
// Create the reader and read COFF Header
sr := io.NewSectionReader(f, 0, 1<<63-1)
err := sr.Seek(pe_sig_offset+4, os.SEEK_SET)
check(err)
binary.Read(sr, binary.LittleEndian, &pefile.FileHeader)
```

Liste 12-16: COFF File Header’ın ayrıştırılması (`/ch-12/peParser/main.go`)

Dosyanın başlangıcından (konum 0) başlayan ve bir `int64`’ün maksimum değerine kadar okuyan yeni bir `SectionReader` oluştururuz. Ardından `sr.Seek()` fonksiyonu, konumu PE imza ofseti ve değerini hemen takip edecek şekilde yeniden ayarlar (literaldeki `PE + 0x00 + 0x00` değerlerini hatırlayın). Son olarak, baytları `pefile` nesnesinin `FileHeader` struct’ına dönüştürmek (marshal) için ikili okuma (binary read) yaparız. `pefile` nesnesini daha önce `pe.NewFile()` çağırdığımızda oluşturduğumuzu hatırlayın.

Go dokümantasyonu, Liste 12-17’de tanımlanan struct ile `FileHeader` tipini tanımlar. Bu struct, Microsoft’un belgelenmiş PE COFF File Header formatı ile oldukça iyi hizalanır (bkz. https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#coff-file-header-object-and-image).

```go
type FileHeader struct {
        Machine              uint16
        NumberOfSections     uint16
        TimeDateStamp        uint32
        PointerToSymbolTable uint32
        NumberOfSymbols      uint32
        SizeOfOptionalHeader uint16
        Characteristics      uint16
}
```

Liste 12-17: Go `pe` paketinin yerel PE File Header struct’ı

Bu struct’ta, `Machine` değeri (başka bir deyişle, PE hedef sistem mimarisi) dışında not edilmesi gereken tek öğe `NumberOfSections` özelliğidir. Bu özellik, Section Table içinde tanımlanan bölüm (section) sayısını içerir; Section Table, başlıkları (headers) doğrudan takip eder. Bir PE dosyasını yeni bir bölüm ekleyerek arka kapı (backdoor) yapmak istiyorsanız `NumberOfSections` değerini güncellemeniz gerekecektir. Ancak, diğer stratejiler bu değerin güncellenmesini gerektirmeyebilir; örneğin, diğer yürütülebilir bölümlerde (CODE, `.text` vb.) ardışık kullanılmayan `0x00` veya `0xCC` değerlerini aramak (shellcode yerleştirilebilecek bellek bölgelerini bulmak için kullanılan bir yöntem) gibi; çünkü bölüm sayısı değişmeden kalır.

Son olarak, COFF File Header’ın ilginç bazı değerlerini çıktılamak için aşağıdaki `print` ifadelerini kullanabilirsiniz (Liste 12-18).

```go
// Print File Header
fmt.Println("[      COFF File Header      ]")
fmt.Printf("[+] Machine Architecture: %#x\n", pefile.FileHeader.Machine)
fmt.Printf("[+] Number of Sections: %#x\n", pefile.FileHeader.NumberOfSections)
fmt.Printf("[+] Size of Optional Header: %#x\n", pefile.FileHeader.SizeOfOptionalHeader)
// Print section names
fmt.Println("[      Section Offsets      ]")
fmt.Printf("[+] Number of Sections Field Offset: %#x\n", pe_sig_offset+6)
// this is the end of the Signature header (0x7c) + coff (20bytes) + oh32 (224bytes)
fmt.Printf("[+] Section Table Offset: %#x\n", pe_sig_offset+0xF8)

/* OUTPUT
[      COFF File Header      ]
[+] Machine Architecture: 0x14c
[+] Number of Sections: 0x8
[+] Size of Optional Header: 0xe0
[      Section Offsets      ]
[+] Number of Sections Field Offset: 0x15e
[+] Section Table Offset: 0x250
*/
```

Liste 12-18: COFF File Header değerlerinin terminal çıktısına yazılması (`/ch-12/peParser/main.go`)

`NumberOfSections` değerini, PE imzası + 4 bayt + 2 bayt ofsetini hesaplayarak (yani toplam 6 bayt ekleyerek) bulabilirsiniz. Kodumuzda `pe_sig_offset`’i zaten tanımladık, bu nedenle bu değere sadece 6 bayt ekleriz. Bölümleri (sections) daha detaylı olarak, Section Table yapısını incelediğimizde tartışacağız.

Üretilen çıktı, `0x14c` olan `Machine Architecture` değerini tanımlar: bu, https://docs.microsoft.com/en-us/windows/win32/debug/pe-format#machine-types sayfasında belirtildiği gibi `IMAGE_FILE_MACHINE_I386`’tir. Bölüm sayısı (`Number of sections`) `0x8`’dir; bu da Section Table içinde sekiz giriş bulunduğunu ifade eder. `Optional Header` (bir sonraki kısımda tartışılacaktır) mimariye bağlı olarak değişken uzunluğa sahiptir: değer `0xe0` (ondalıkta 224), ki bu 32 bitlik bir sisteme karşılık gelir. Son iki satır daha çok kolaylık amacıyla üretilmiş çıktılar olarak görülebilir. Özellikle, `Sections Field Offset` bölüm sayısına giden ofseti, `Section Table Offset` ise Section Table’ın konumuna giden ofseti sağlar. Örneğin shellcode eklemek istediğinizde, her iki ofset değerinin de değiştirilmesi gerekebilir.

### Optional Header’ı Ayrıştırma
