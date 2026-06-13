```go
0. void box()
       MessageBox(0, "Is Go the best?", "C GO GO", m00000040;
1
*/
import "C"
func main() f

       C.box()
1
```

**Liste 12-24: C kullanan Go (/ch-12/messagebox/moin.go)**

C kodu, harici dosya `include` ifadeleriyle sağlanabilir. Ayrıca doğrudan bir Go dosyasına da gömülebilir. Burada her iki yöntemi de kullanıyoruz. C kodunu bir Go dosyasına gömmek için, bir yorum (comment) kullanıyor ve bu yorumun içinde bir `MessageBox` oluşturacak fonksiyonu tanımlıyoruz. Go, derleme (compile) zamanı seçenekleri için birçok yorum biçimini destekler; C kodunu derlemek de buna dahildir. Kapanış yorum etiketinden hemen sonra `import "C"` kullanarak Go derleyicisine CGO kullanmasını söylüyoruz; CGO, Go derleyicisinin derleme zamanında yerel (native) C kodu ile bağlanmasını sağlayan bir pakettir. Artık Go kodu içerisinde C'de tanımlanmış fonksiyonları çağırabiliriz ve C kodumuzun gövdesinde tanımladığımız fonksiyonu çalıştıran `C.box()` fonksiyonunu çağırıyoruz.

Örnek kodu `go build` komutuyla derleyin. Çalıştırdığınızda bir mesaj kutusu (message box) görmelisiniz.

**NOT** CGO paketi son derece kullanışlıdır; Go kodundan C kütüphanelerini, C kodundan da Go kütüphanelerini çağırmanıza olanak tanır. Ancak bunu kullanmak, Go’nun bellek yöneticisini ve çöp toplayıcısını devre dışı bırakır. Go’nun bellek yöneticisinin avantajlarından yararlanmak istiyorsanız, belleği Go içinde ayırmalı ve ardından C'ye geçirmelisiniz. Aksi halde, Go’nun bellek yöneticisi C bellek yöneticisi kullanılarak yaptığınız bellek ayırmalarından haberdar olmayacak ve bu ayırmalar, C’nin yerel `free()` fonksiyonunu çağırmadıkça serbest bırakılmayacaktır. Belleği doğru biçimde serbest bırakmamak, Go kodunuz üzerinde olumsuz etkilere yol açabilir. Son olarak, tıpkı Go'da dosya tanıtıcılarını (file handle) açarken olduğu gibi, Go fonksiyonunuz içinde `defer` kullanarak, Go’nun referans verdiği C belleğinin çöp toplama (garbage collection) yoluyla serbest bırakılmasını güvence altına alın.

## Go’yu C İçine Derlemek

Nasıl C kodunu Go programlarına gömebiliyorsak, Go kodunu da C programlarına gömebiliriz. Bu yararlıdır çünkü bu kitabın yazıldığı sıralarda Go derleyicisi, programlarımızı DLL olarak derleyememektedir. Bu da, bu bölümde daha önce oluşturduğumuz yansıtmalı (reflective) DLL enjeksiyon yükleri (payload) gibi yardımcı programları yalnızca Go kullanarak derleyemeyeceğimiz anlamına gelir.

Bununla birlikte, Go kodumuzu bir C arşiv dosyasına dönüştürebilir ve ardından bu arşiv dosyasını C kullanarak bir DLL'e derleyebiliriz. Bu bölümde, Go kodumuzu bir C arşiv dosyasına dönüştürerek bir DLL oluşturacağız. Ardından, mevcut araçları kullanarak bu DLL’i shellcode’a dönüştüreceğiz; böylece belleğe enjekte edip çalıştırabileceğiz. Go koduyla başlayalım (Liste 12-25); bu kodu `main.go` adlı bir dosyaya kaydedin.

```go
package main
import "C"
import "fmt"
//export Start
func Start() {
    fmt.Println("YO FROM GO")

func main() {
}
```

**Liste 12-25: Go yükü (payload) (/ch-12/dlIshellcode/main.go)**

CGO’yu derlememize dahil etmek için `C` paketini içe aktarıyoruz. Sonraki adımda, bir yorumu kullanarak C arşivimizde bir fonksiyon ihraç (export) etmek istediğimizi Go’ya bildiriyoruz. Son olarak C’ye dönüştürmek istediğimiz fonksiyonu tanımlıyoruz. `main()` fonksiyonu boş kalabilir.

C arşivini derlemek için şu komutu çalıştırın:

```bash
> go build -buildmode=c-archive
```

Artık `dllshellcode.a` adlı bir arşiv dosyasına ve `dllshellcode.h` adlı ilişkili bir başlık (header) dosyasına sahip olmalısınız. Bunları henüz doğrudan kullanamayız. `dllshellcode.a` dosyasını derleyiciye dahil etmeye zorlayacak bir C şimi (shim) oluşturmamız gerekir. Zarif çözümlerden biri, bir fonksiyon tablosu kullanmaktır. Liste 12-26’daki kodu içeren bir dosya oluşturun. Bu dosyayı `scratch.c` olarak adlandırın.

```c
#include "dlIshellcode.h"
void (*table[1]) = {Start};
```

**Liste 12-26: `scratch.c` dosyasında saklanan bir fonksiyon tablosu (/ch-12/dllshellcode/scratch.c)**

Artık GCC kullanarak `scratch.c` dosyasını aşağıdaki komutla bir DLL’e derleyebiliriz:

```bash
> gcc -shared -pthread -o x.d11 scratch.c dllshellcode.a -lWinM1 -lntd11 -lWS2_32
```

DLL’imizi shellcode’a dönüştürmek için, çok sayıda işlevselliğe sahip mükemmel bir araç olan sRDI’yi (https://github.com/monoxgas/sRDI/) kullanacağız. Başlangıç için, depoyu (repo) Windows’ta ve tercihe bağlı olarak bir GNU/Linux makinede Git ile indirin; Python 3 ortamı olarak GNU/Linux’u daha rahat bulabilirsiniz. Bu alıştırma için Python 3’e ihtiyacınız olacak; yüklü değilse kurun.

`sRDI` dizininden bir `python3` kabuğu (shell) çalıştırın. İhraç edilen fonksiyonun hash’ini üretmek için aşağıdaki kodu kullanın:

```bash
>>> from ShellCodeRDI import *
>>> HashFunctionName('Start')
1168596138
```

sRDI araçları, daha sonra üreteceğimiz shellcode içinden bir fonksiyonu tanımlamak için bu hash’i kullanacaktır.

Sonraki adımda, shellcode üretmek ve çalıştırmak için PowerShell araçlarından yararlanacağız. Kolaylık olması için, shellcode enjekte etmek amacıyla kullanabileceğimiz bir PowerShell araç takımı olan PowerSploit’ten (https://github.com/PowerShellMafia/PowerSploit/) bazı araçlar kullanacağız. Bunu Git ile indirebilirsiniz. `PowerSploit\CodeExecution` dizininden yeni bir PowerShell kabuğu başlatın:

```bash
c:\tools\PowerSploit\CodeExecution> powershell.exe -exec bypass
Windows PowerShell
Copyright (C) 2016 Microsoft Corporation. All rights reserved.
```

Şimdi PowerSploit ve sRDI’den iki PowerShell modülünü içe aktarın:

```powershell
PS C:\tools\PowerSploit\CodeFxecution> Import-Module .\Invoke-Shellcode.ps1
PS C:\tools\PowerSploit\CodeExecution> cd
PS C:\tools\sRDI> cd .\PowerShell\
PS C:\tools\sRDI\PowerShell> Import-Module .\ConvertTo-Shellcode.ps1
```

Her iki modülü de içe aktardıktan sonra, sRDI’den `ConvertTo-Shellcode` komutunu kullanarak DLL’den shellcode üretebilir ve ardından bu shellcode’u PowerSploit’ten `Invoke-Shellcode` komutuna geçirerek enjeksiyonu gösterebiliriz. Bu çalıştırıldığında, Go kodunuzun çalıştığını gözlemlemelisiniz:

```powershell
PS C:\tools\sRDI\PowerShell> Invoke-Shellcode -Shellcode (ConvertTo-Shellcode `
-File C:\Users\tom\Downloads\x.d11 -FunctionHash 1168596138)
```
