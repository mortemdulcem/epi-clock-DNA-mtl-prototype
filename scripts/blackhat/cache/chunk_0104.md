Adım 1'de, `OpenProcess()` Windows fonksiyonunu kullanarak, istenen süreç erişim haklarıyla birlikte bir süreç (process) tanıtıcısı (handle) elde ediyoruz. Bu, ister yerel ister uzak bir süreçle uğraşalım, süreç seviyesinde etkileşim için bir gerekliliktir.

Gerekli süreç tanıtıcısını elde ettikten sonra, adım 2'de bu tanıtıcıyı `VirtualAllocEx()` Windows fonksiyonuyla birlikte kullanarak uzak süreç içerisinde sanal bellek ayırıyoruz. Bu, shellcode veya bir DLL gibi bayt düzeyinde kodu uzak süreçlerin belleğine yüklemek için bir gerekliliktir.

Adım 3'te, `WriteProcessMemory()` Windows fonksiyonunu kullanarak bayt düzeyinde kodu belleğe yüklüyoruz. Enjeksiyon sürecinin bu noktasında, saldırganlar olarak shellcode veya DLL ile ne kadar yaratıcı olacağımıza biz karar veririz. Çalışan bir programı anlamaya çalışırken hata ayıklama (debugging) kodunu enjekte etmeniz gereken yer de burasıdır.

Son olarak, adım 4'te `CreateRemoteThread()` Windows fonksiyonunu kullanarak, `kernel32.dll` içinde yer alan `LoadLibraryA()` gibi, Windows DLL'lerinde dışa aktarılmış (exported) yerel bir fonksiyonu çağırıyoruz; böylece `WriteProcessMemory()` kullanarak süreç içine önceden yerleştirdiğimiz kodu çalıştırabiliyoruz.

Yeni açıkladığımız bu dört adım temel bir süreç enjeksiyonu örneği sunar. Genel süreç enjeksiyonu örneğimiz içinde, burada mutlaka anlatılmamış birkaç ek dosya ve fonksiyon tanımlayacağız; ancak bunları onlarla karşılaştıkça ayrıntılı olarak açıklayacağız.

## Windows DLL'lerini Tanımlama ve Değişken Atama

İlk adım olarak, Liste 12-3'teki `winmods` dosyasını oluşturuyoruz. (`/` kök dizinindeki tüm kod listeleri, verilen GitHub deposu `https://github.com/blackhat-go/bhg/` altında bulunur.) Bu dosya, Go'nun `syscall` paketini kullanarak çağıracağımız, sistem seviyesindeki dışa aktarılmış API'leri barındıran yerel Windows DLL'lerini tanımlar. `winmods` dosyası, örnek projemiz için gerekenden daha fazla Windows DLL modül referansının bildirimlerini ve atamalarını içerir; ama biz bunları belgeleyeceğiz ki siz bunlardan daha gelişmiş enjeksiyon kodlarında da yararlanabilesiniz.

```go
import "syscall"

var (
    ModKerne132 = syscall.NewLazyDLL("kerne132.d11")
    modUser32 = syscall.NewLazyDa(user32.d11")
    modAdvapi32 = syscall.NewLazyDLL("Advapi32.d11")

    ProcOpenProcessToken       = modAdvapi32.NewProc("GetProcessToken")
    ProcLookupPrivilegeValueW = modAdvapi32.NewProc("LookupPrivilegeValueW")
    ProcLookupPrivilegeNameW = modAdvapi32.NewProc("LookupPrivilegeNameW")
    ProcAdjustTokenPrivileges = modAdvapi32.NewProc("AdjustTokenPrivileges")
    ProcGetAsyncKeyState         modUser32.NewProc("GetAsyncKeyState")
    ProcVirtualAlloc           = ModKerne132.NewProc("VirtualAlloc")
    ProcCreateThread             ModKerne132.NewProc("CreateThread")
    ProcWaitForSingleObject      ModKerne132.NewProc("WaitForSingleObject")
    ProcVirtualAllocEx         = ModKerne132.NewProc("VirtualAllocEx")
    ProcVirtualFreeEx          = ModKerne132.NewProc("VirtualFreeEx")
    ProcCreateRemoteThread     = ModKerne132.NewProc("CreateRemoteThread")
    ProcGetLastError             ModKerne132.NewProc("GetLastError")
    ProcWriteProcessMemory       ModKerne132.NewProc("WriteProcessMemory")
    ProcOpenProcess            = ModKerne132.NewProc("OpenProcess")
    ProcGetCurrentProcess        ModKerne132.NewProc("GetCurrentProcess")
    ProcIsDebuggerPresent        ModKerne132.NewProc("IsDebuggerPresent")
    ProcGetProcAddress           ModKerne132.NewProc("GetProcAddress")
    ProcCloseHandle            = ModKerne132.Newftoc("CloseHandle")
    ProcGetExitCodeThread        ModKerne132.NewProc("GetExitCodeThread")
)
```

**Liste 12-3:** `winmods` dosyası (`/ch-12/procInjector/winsys/winmods.go`)

`ModKerne132` değişkenini tanımlarken `NewLazyDLL()` metodunu kullanarak `Kerne132` DLL’ini yüklüyoruz. `Kerne132`, adresleme, handle yönetimi, bellek ayırma ve daha fazlası gibi pek çok dahili Windows süreç işlevselliğini yönetir. (Go sürüm 1.12.2 itibarıyla, DLL'leri daha iyi yüklemek ve sistem DLL hijacking saldırılarını engellemek için kullanabileceğiniz iki yeni fonksiyon olduğunu belirtmekte fayda var: `LoadLibraryEx()` ve `NewLazySystemDLL()`.)

DLL ile etkileşime girebilmeden önce, kod içinde kullanabileceğimiz bir değişken tanımlamamız gerekir. Bunu, kullanmamız gerekecek her API için `module.NewProc` çağırarak yaparız. `OpenProcess()` fonksiyonu için bu çağrıyı yapar ve sonucu `ProcOpenProcess` adında dışa aktarılmış bir değişkene atarız. `OpenProcess()`'ün kullanımı burada keyfidir; amaç, herhangi bir dışa aktarılmış Windows DLL fonksiyonunu betimleyici bir değişken adına atama tekniğini göstermekten ibarettir.

## OpenProcess Windows API'si ile Bir Süreç Belirteci (Token) Elde Etme

Sonraki adımda, bir süreç tanıtıcısı (handle) belirteci (token) elde etmek için kullanacağımız `OpenProcessHandle()` fonksiyonunu oluşturuyoruz. Kod boyunca `token` ve `handle` terimlerini muhtemelen birbirinin yerine kullanacağız, ancak bir Windows sistemindeki her sürecin benzersiz bir süreç belirteci (process token) olduğunu unutmayın. Bu belirteç, Zorunlu Bütünlük Kontrolü (Mandatory Integrity Control) gibi ilgili güvenlik modellerini uygulamak için bir yol sağlar; bu karmaşık bir güvenlik modelidir (ve süreç seviyesindeki mekaniklere daha fazla aşina olmak için araştırmaya değer). Güvenlik modelleri, örneğin süreç seviyesindeki haklar ve ayrıcalıklar gibi öğelerden oluşur ve ayrıcalıksız (unprivileged) ve ayrıcalıklı (elevated) süreçlerin birbirleriyle nasıl etkileşime girebileceğini belirler.

Önce, Windows API dokümantasyonunda tanımlandığı şekliyle, C++ `OpenProcess()` veri yapısına (Listing 12-4) bir göz atalım. Bu nesneyi, sanki onu yerel Windows C++ kodundan çağıracakmışız gibi tanımlayacağız. Ancak bunu yapmayacağız; çünkü bu nesneyi Go'nun `syscall` paketiyle kullanılmak üzere tanımlıyor olacağız. Bu nedenle, bu nesneyi standart Go veri tiplerine çevirmemiz gerekecek.
