Windows işletim sisteminin genelinde kullanılacak çeşitli veri tiplerini ve sabitleri tanımlayan bölümdür.

Microsoft tarafından bazı dizinlerin ayrılmış veya henüz uygulanmamış olduğunu, bu nedenle hepsinin kullanımda olmadığını unutmayın. Tüm veri dizinlerinin (Data Directory) listesine ve bunların amaçlanan kullanım ayrıntılarına https://docs.microsaftcom/en-us/windows/win32/debug/peformat#optional-header-data-directories-image-only adresinden ulaşabilirsiniz. Tekrar belirtmek gerekirse, her bir dizinle ilişkilendirilmiş oldukça fazla bilgi vardır; bu yüzden yapılarını gerçekten araştırmak ve iyice tanımak için zaman ayırmanızı öneririz.

Şimdi, Liste 12-21’deki kodu kullanarak Veri Dizini (Data Directory) içindeki birkaç dizin girdisini inceleyelim.

```go
// Print Data Directory
fmt.Println("[+] Data Directory")
var winnt_datadirs []string{
    "IMAGE_DIRECTORY_ENTRY_EXPORT",
    "IMAGE_DIRECTORY_ENTRY_IMPORT",
    "IMAGE_DIRECTORY_ENTRY_RESOURCE",
    "IMAGE_DIRECTORY_ENTRY_EXCEPTION",
    "IMAGE_DIRECTORY_ENTRY_SECURITY",
    "IMAGE_DIRECTORY_ENTRY_BASERELOC",
    "IMAGE_DIRECTORY_ENTRY_DEBUG",
    "IMAGE_DIRECTORY_ENTRY_COPYRIGHT",
    "IMAGE_DIRECTORY_ENTRY_GLOBALPTR",
    "IMAGE_DIRECTORY_ENTRY_TLS",
    "IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG",
    "IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT",
    "IMAGE_DIRECTORY_ENTRY_IAT",
    "IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT",
    "IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR",
    "IMAGE_NUMBEROF_DIRECTORY_ENTRIES",
}

for idx, directory := range oh32.DataDirectory {
    fmt.Printf("[+] Data Directory: %s\n", winnt_datadirs[idx])
    fmt.Printf("[+] Image Virtual Address: 0x%x\n", directory.VirtualAddress)
    fmt.Printf("[+] Image Size: 0x%x\n", directory.Size)
}

/* OUTPUT
[+] Data Directory
[+] Data Directory: IMAGE_DIRECTORY_ENTRY_EXPORT
[+] Image Virtual Address: 0x2a7b660
[+] Image Size: 0x126c
[+] Data Directory: IMAGE_DIRECTORY_ENTRY_IMPORT
[+] Image Virtual Address: 0x2a7c81c
[+] Image Size: 0x12c
--snip--
*/
```

**Liste 12-21** Adres ofseti ve boyut için Veri Dizini’nin (Data Directory) ayrıştırılması (`/ch-12/peParser/main.go`)

Veri Dizini listesi `0` Microsoft tarafından statik olarak tanımlanmıştır; bu da, tek tek dizin adlarının sabit bir sırada kalacağı anlamına gelir. Bu nedenle bunlar sabit (constant) olarak kabul edilir. Bireysel dizin girdilerini saklamak için `winnt_datadirs` adlı bir slice değişkeni kullanacağız; böylece adları indeks pozisyonlarıyla eşleştirebiliriz. Özellikle, Go `pe` paketi Veri Dizini’ni bir `struct` nesnesi olarak uygular, bu yüzden her bir girdiyi, ilişkili adres ofseti ve boyut nitelikleriyle birlikte çıkarmak için girdiler üzerinde yineleme (iterate) yapmamız gerekir. `for` döngüsü 0-indeks tabanlıdır; dolayısıyla her slice girdisini indeks pozisyonuna göre yazdırıyoruz.

Standart çıktıya yazdırılan dizin girdileri `IMAGE_DIRECTORY_ENTRY_EXPORT` (veya EAT) ve `IMAGE_DIRECTORY_ENTRY_IMPORT` (veya IAT)’tır. Bu dizinlerin her biri, çalışmakta olan Windows yürütülebilir dosyasına göre, sırasıyla dışa aktarılan ve içe aktarılan fonksiyonların bir tablosunu tutar. `IMAGE_DIRECTORY_ENTRY_EXPORT` girdisine daha yakından bakarsanız, sanal adresin (`virtual address`) gerçek tablo verilerinin ofsetini içerdiğini, ayrıca dizinin içinde yer alan verilerin boyutunu (`size`) göreceksiniz.

## Bölüm Tablosunun Ayrıştırılması

Bölüm Tablosu (Section Table), son PE bayt yapısı olarak, doğrudan İsteğe Bağlı Başlık’ı (Optional Header) takip eder. Windows yürütülebilir ikili dosyasında, yürütülebilir kod ve başlatılmış veri konum ofsetleri gibi her ilgili bölümün ayrıntılarını içerir. Giriş sayısı, COFF Dosya Başlığı (COFF File Header) içindeki `NumberOfSections` değeriyle eşleşir. Bölüm Tablosu’nu, PE imza ofseti + `0xF8` konumunda bulabilirsiniz. Bu bölüme bir hex editör içinde bakalım (Şekil 12-8).

```text
Offset(h)   00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F      Decoded text
00000240    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00000250    2E 74 65 78 74 00 00 00 D0 3D 85 01 00 10 00 00      .text... .=......
00000260    D0 36 85 01 00 04 00 00 00 00 00 00 00 00 00 00
00000270    00 00 60 00 20 00 00 20 72 65 64 61 74 61 00 00      ..`. .. redata..
00000280    00 18 00 00 00 50 85 01 00 1C 00 00 00 12 85 01
00000290    00 00 00 00 00 00 00 00 00 00 00 00 20 00 00 60
000002A0    2E 72 64 61 74 61 00 00 38 BA 22 01 00 70 85 01      .rdata..8."..p..
000002B0    00 BC 22 01 00 5E 85 01 00 00 00 00 00 00 00 00
000002C0    00 00 00 00 40 00 00 40 2E 64 61 74 61 00 00 00      ....@..@.data...
000002D0    40 08 51 00 00 38 02 00 12 17 00 00 53 37 00 00
000002E0    2E 71 74 6D 66 74 61 64 38 02 00 00 00 10 79 00      .qtmftad8.....y.
000002F0    00 04 00 00 00 FC 85 02 00 60 00 00 00 00 00 00
00000300    00 00 00 00 40 00 00 50 57 52 44 41 54 41 00 00      ....@..PWRDATA..
00000310    ED F2 02 0D 00 20 84 02 00 74 02 00 00 00 C6 00
00000320    30 00 00 00 00 00 00 00 00 00 00 00 40 00 00 40
00000330    2E 72 73 72 63 00 00 00 68 AD 05 00 00 20 FC 00      .rsrc...h.... ..
00000340    00 A2 05 00 00 74 C8 02 00 00 00 00 00 00 00 00
00000350    00 00 00 00 40 00 00 40 2E 72 65 6C 6F 63 00 00      ....@..@.reloc..
00000360    10 43 15 00 00 D0 01 00 44 15 00 00 32 CE 07 00
00000370    3D 00 00 00 00 00 00 00 00 00 00 00 40 00 00 42
```

**Şekil 12-8**: Hex editör kullanılarak gözlemlenen Bölüm Tablosu (Section Table)

Bu özel Bölüm Tablosu `.text` ile başlıyor, ancak ikili dosyanın derleyicisine bağlı olarak bir `CODE` bölümüyle de başlayabilir. `.text` (veya `CODE`) bölümü yürütülebilir kodu içerirken, bir sonraki bölüm olan `.rodata` salt okunur sabit verileri barındırır. `.rdata` bölümü kaynak (resource) verilerini, `.data` bölümü ise başlatılmış verileri içerir. Her bölüm en az 40 bayt uzunluğundadır.

Bölüm Tablosu’na COFF Dosya Başlığı (COFF File Header) içinden erişebilirsiniz. Ayrıca her bir bölüme tek tek, Liste 12-22’deki kodu kullanarak erişebilirsiniz.

```go
s := pefile.Section(".text")
fmt.Printf("%v", *s)
/* Output
{{.text 25509328 4096 25509376 1024 0 0 0 0 1610612768} 1 [1 0xc0000643c0 0xc0000643c0]}
*/
```

**Liste 12-22** Bölüm Tablosu’ndan belirli bir bölümün ayrıştırılması (`/ch-12/peParser/main.go`)

Diğer bir seçenek de, Liste 12-23’te gösterildiği gibi, tüm Bölüm Tablosu üzerinde yineleme yapmaktır.
