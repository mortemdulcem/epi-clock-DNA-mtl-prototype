```go
      fmt.Println(1       Section Table     ]")
      for _, section := range pefile.Sections
          fmt.Println("[+]                      ")
          fmt.Printf("[+] Section Name: %s\n", section.Name)
          fmt.Printf("[+] Section Characteristics: Utx\n", section.Characteristics)
          fmt.Printf("[+] Section Virtual Size: Utx\n", section.VirtualSize)
          fmt.Printf("[+] Section Virtual Offset: %#x\n", section.VirtualAddress)
          fmt.Printf("[+] Section Raw Size: Ux\n", section.Size)
          fmt.Printf("[+] Section Raw Offset to Data: %Itx\n", section.Offset)
          fmt.Printf("[+] Section Append Offset (Next Section): Ptx\n", section.Offset+section.Size)

/* OUTPUT
      Section Table
[+]
[+] Section Name: .text
[+] Section Characteristics: 0x60000020
[+] Section Virtual Size: Ox1853dd0
[+] Section Virtual Offset: Ox1000 0
[+] Section Raw Size: 0x1853e00 0
[+] Section Raw Offset to Data: Ox400
[+] Section Append Offset (Next Section): 0x1854200
[+]
[+] Section Name: .rodata
[+] Section Characteristics: 0x60000020
[+] Section Virtual Size: Ox1b00
[F] Section Virtual Offset: Ox1855000
[+] Section Raw Size: Ox1c00
[+] Section Raw Offset to Data: 0x1854200
[+] Section Append Offset (Next Section): Ox1855e00
--snip--

**Liste 12-23: Bir Bölüm Tablosundaki (Section Table) tüm bölümlerin ayrıştırılması (/ch-12/peParser/main.go)**
```

Burada, Section Table içindeki tüm bölümler (section) üzerinde yineliyoruz ve ad, sanal boyut, sanal adres, ham (raw) boyut ve ham ofset değerlerini standart çıktıya yazıyoruz. Ayrıca, yeni bir bölüm eklemek isteyebileceğimiz durumlar için bir sonraki 40 baytlık ofset adresini hesaplıyoruz. `characteristics` (özellikler) değeri, bölümün ikili dosyanın bir parçası olarak nasıl davranacağını tanımlar. Örneğin, `.text` bölümü `0x60000020` değeri sağlar.

İlgili Section Flags verisine https://docs.microsoftcom/en-us/windows/win32/debug/pe-format#section-flags (Tablo 12-2) adresinden bakacak olursak, bu değeri üç ayrı özniteliğin oluşturduğunu görebiliriz.

**Tablo 12-2: Section Flags özellikleri**

| Bayrak                    | Değer       | Açıklama                                        |
|---------------------------|------------|-------------------------------------------------|
| IMAGE_SCN_CNT_CODE        | 0x00000020 | Bölüm çalıştırılabilir kod içerir.             |
| IMAGE_SCN_MEM_EXECUTE     | 0x20000000 | Bölüm, kod olarak yürütülebilir.               |
| IMAGE_SCN_MEM_READ        | 0x40000000 | Bölüm okunabilir.                              |

İlk değer olan `0x00000020` (`IMAGE_SCN_CNT_CODE`), bölümün çalıştırılabilir kod içerdiğini belirtir. İkinci değer olan `0x20000000` (`IMAGE_SCN_MEM_EXECUTE`), bölümün kod olarak yürütülebileceğini belirtir. Son olarak üçüncü değer olan `0x40000000` (`IMAGE_SCN_MEM_READ`), bölümün okunmasına izin verir. Dolayısıyla, bunların hepsini topladığınızda `0x60000020` değeri elde edilir. Yeni bir bölüm ekliyorsanız, tüm bu özellikleri uygun değerlerle güncellemeniz gerektiğini aklınızda bulundurun.

Bu noktada PE dosyası veri yapısına ilişkin tartışmamızı sonlandırıyoruz. Bunun kısa bir genel bakış olduğunu biliyoruz. Her bir bölüm başlı başına bir bölüm (chapter) olabilir. Ancak, bu kadarı Go'yu kullanarak keyfi veri yapılarını dolaşabilmenizi sağlamaya yetecektir. PE veri yapısı oldukça karmaşıktır ve tüm bileşenlerine aşina olmak için gerekli zaman ve çabayı harcamaya değer.

## Ek Alıştırmalar

PE dosyası veri yapısı hakkında yeni öğrendiğiniz bilgileri genişletin. Aşağıda hem anlayışınızı pekiştirecek hem de Go `pe` paketini daha fazla keşfetmenizi sağlayacak bazı ek fikirler yer alıyor:

- Çeşitli Windows ikili dosyaları edinin ve bir hex editörü ile hata ayıklayıcı (debugger) kullanarak farklı ofset değerlerini keşfedin. Bölüm sayıları gibi, farklı ikili dosyaların nasıl farklı olduklarını belirleyin. Bu bölümde oluşturduğunuz parser'ı hem keşif hem de manuel gözlemlerinizi doğrulamak için kullanın.
- PE dosya yapısının EAT (Export Address Table) ve IAT (Import Address Table) gibi yeni alanlarını keşfedin.
- Şimdi, parser'ı DLL gezinimini destekleyecek şekilde yeniden yazın.
- Var olan bir PE dosyasına yeni bölüm ekleyerek parlak yeni shellcode'unuzu dahil edin. Bölüm sayısı, giriş noktası (entry point) ve ham (raw) ve sanal (virtual) değerler dahil tüm bölümü uygun şekilde güncelleyin. Bunu bir kez daha yapın ama bu sefer yeni bir bölüm eklemek yerine var olan bir bölümü kullanın ve bir code cave oluşturun.
- Bahsetmediğimiz bir konu da, kodu paketlenmiş (packed) PE dosyalarını nasıl ele alacağımızdı; bu paketleme yaygın paketleyiciler (packer) olan UPX gibi araçlarla veya daha az bilinen paketleyicilerle yapılmış olabilir. Paketlenmiş bir ikili dosya bulun, nasıl paketlendiğini ve hangi paketleyicinin kullanıldığını belirleyin, ardından kodu açmak (unpack) için uygun tekniği araştırın.

---

## Go ile C Kullanımı

Windows API'sine erişmenin bir diğer yöntemi de C'den yararlanmaktır. C'yi doğrudan kullanarak, yalnızca C'de mevcut olan bir kütüphaneden faydalanabilir, bir DLL (sadece Go kullanarak yapamayız) oluşturabilir veya yalnızca Windows API'sini çağırabilirsiniz. Bu bölümde önce Go ile uyumlu bir C araç zinciri (toolchain) yükleyip yapılandıracağız. Ardından, Go programlarında C kodunun nasıl kullanılacağına ve C programlarında Go kodunun nasıl dahil edileceğine ilişkin örneklere bakacağız.

### Windows için C Araç Zinciri Kurulumu

Go ve C kombinasyonu içeren programları derlemek için, C kod bölümlerini derlemek amacıyla kullanılabilecek uygun bir C araç zincirine ihtiyacınız var. Linux ve macOS'te, GNU Compiler Collection'ı (GCC) bir paket yöneticisi aracılığıyla yükleyebilirsiniz. Windows üzerinde ise bir araç zinciri kurmak ve yapılandırmak biraz daha zahmetlidir ve mevcut çok sayıda seçenekle aşina değilseniz can sıkıcı olabilir. Bizim bulduğumuz en iyi seçenek, MinGW-w64'ü paketleyen MSYS2 kullanmaktır; MinGW-w64, GCC araç zincirini Windows üzerinde desteklemek için oluşturulmuş bir projedir. Bunu https://www.msys2.org/ adresinden indirip kurun ve C araç zincirinizi yüklemek için sayfadaki talimatları izleyin. Ayrıca derleyiciyi `PATH` değişkeninize eklemeyi unutmayın.

### C ve Windows API Kullanarak Bir Mesaj Kutusu Oluşturma

Artık bir C araç zincirini yapılandırıp yüklediğimize göre, gömülü C kodundan yararlanan basit bir Go programına bakalım. Liste 12-24, Windows API'yi kullanarak bir mesaj kutusu oluşturan C kodunu içerir; bu da Windows API'nin kullanımına dair görsel bir gösterim sağlar.

```go
package main

/*
#include <stdio.h>
#include <windows.h>
```
