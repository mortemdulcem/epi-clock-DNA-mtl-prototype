```c
                 HANDLE OpenProcess(
                    DWORDO dwDesiredAccess,
                    BOOL bInheritHandle,
                    DWORD dwProcessId
                 );
```

**Liste 12-4: Rastgele bir Windows C++ nesnesi ve veri tipleri**

İlk gerekli görev, `DWORD` değerini Go'nun sürdürebileceği kullanılabilir bir tipe çevirmektir. `DWORD`, Microsoft tarafından 32 bit işaretsiz tamsayı olarak tanımlanır; bu da Go'nun `uint32` tipine karşılık gelir. `DWORD` değeri `dwDesiredAccess` içermelidir ya da dokümantasyonda belirtildiği gibi, "bir veya daha fazla süreç erişim hakkı (process access rights)" barındırmalıdır. Süreç erişim hakları, geçerli bir süreç belirteci (process token) verildiğinde bir süreç üzerinde gerçekleştirmek istediğimiz eylemleri tanımlar.

Çok çeşitli süreç erişim hakları tanımlamak istiyoruz. Bu değerler değişmeyeceği için, ilgili değerleri Liste 12-5'te gösterildiği gibi bir Go sabitler (constants) dosyasında saklıyoruz. Bu listedeki her satır bir süreç erişim hakkı tanımlar. Liste, neredeyse mevcut tüm süreç erişim haklarını içerir, ancak biz yalnızca bir süreç tutamacı (process handle) elde etmek için gerekli olanları kullanacağız.

```go
const (
   // docs.microsoft.com/en-us/windows/desktop/ProcThread/process-security-and-access-rights
   PROCESS_CREATE_PROCESS           = 0x0080
   PROCESS_CREATE_THREAD            = 0x0002
   PROCESS_DUP_HANDLE               = Ox0040
   PROCESS_QUERY_INFORMATION        = Ox0400
   PROCESS_QUERYSIMITED_INFORMATION = Ox1000
   PROCESS SET INFORMATION          = Ox0200
   PROCESS_SET_QUOTA                = ox0100
   PROCESS_SUSPEND_RESUME           = oxo800
```

```go
    PROCESS_TERMINATE                       = Ox0001
    PROCESS_VM_OPERATION                    = Ox0008
    PROCESS_VM_READ                         = Ox0010
    PROCESS_VM_WRITE                        = Ox0020
    PROCESS_ALL_ACCESS                      = Ox001FOEFF
```

**Liste 12-5: Süreç erişim haklarını ilan eden bir constants bölümü (`/ch-12/procInjector/winsys/constants.go`)**

Liste 12-5'te tanımladığımız tüm süreç erişim hakları, kendi sabit onaltılık (hexadecimal) değerleriyle uyumludur; bunlar, bir Go değişkenine atanmaları için gerekli olan formattır.

Liste 12-6'yı incelemeden önce bahsetmek istediğimiz bir konu, izleyen süreç enjeksiyon fonksiyonlarının çoğunun (yalnızca `OpenProcessHandle()` değil) `Inject` tipinde özel bir nesne tüketmesi ve `error` tipinde bir değer döndürmesidir. `Inject` struct nesnesi (Liste 12-6), ilgili Windows fonksiyonuna `syscall` aracılığıyla verilecek çeşitli değerler içerecektir.

```go
                    type Inject struct
                        Pid             uint32
                        D11Path         string
                        DLLSize         uint32
                        Privilege       string
                        RemoteProcHandle uintptr
                        Lpaddr          uintptr
                        LoadLibAddr     uintptr
                        RThread         uintptr
                        Token           TOKEN

                    type TOKEN struct {
                        tokenHandle syscall .Token
```

**Liste 12-6: Belirli süreç enjeksiyon veri tiplerini tutmak için kullanılan `Inject` struct'ı (`/ch-12/procInjector/winsys/models.go`)**

Liste 12-7, ilk gerçek fonksiyonumuz olan `OpenProcessHandle()` fonksiyonunu göstermektedir. Aşağıdaki kod bloğuna bakalım ve çeşitli ayrıntıları tartışalım.

```go
                    func OpenProcessHandle(i *Inject) error {
                            var rights uint32 = PROCESS_CREATE_THREAD 1
                             PROCESSAUERY_INFORMATION
                             PROCESS_VM_OPERATION 1
                             PROCESS_VM_WRITE 1
                             PROCESS_VM_READ
                            var inheritHandle uint32 = 0
                            var processID uint32 = i.Pid
                            remoteProcHandle,        lastErre := ProcOpenProcess.Call0(
                              uintptr(rights), // DWORD dwDesiredAccess
                              uintptr(inheritHandle), // BOOL bInheritHandle
                              uintptr(processID)) // DWORD dwProcessId
                        if remoteProcHandle == 0 I
                              return errors.Wrap(lastErr, 'DJ ERROR :
```

```go
                          Can't Open Remote Process. Maybe running w elevated integrity?')

                     i.RemoteProcHandle = remoteProcHandle
                     fmt.Printf("[-] Input PID: %v\n", i.Pid)
                     fmt.Printf(1-] Input DLL: %v\n", i.D11Path)
                     fmt.Printf("[+] Process handle: %v\n", unsafe.Pointer(i.RemoteProcHandle))
                     return nil
```

**Liste 12-7: Bir süreç tutamacı (process handle) elde etmek için kullanılan `OpenProcessHandle()` fonksiyonu (`/ch-12/procInjector/winsys/inject.go`)**
