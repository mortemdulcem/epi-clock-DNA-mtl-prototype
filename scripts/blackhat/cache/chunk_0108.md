### VirtualFree ve Windows API ile Temizlik

`VirtualAllocEx()` ile `Liste 12-8`'de ayırdığımız sanal belleği serbest bırakmak (veya decommit etmek) için `VirtualFreeEx()` Windows fonksiyonunu kullanıyoruz. Bu, belleği düzgün biçimde temizlemek için gereklidir, çünkü başlatılmış bellek bölgeleri, uzaktan bir sürece enjekte edilen kodun (örneğin tüm bir DLL) toplam boyutu düşünüldüğünde oldukça büyük olabilir. Bu kod bloğuna (Liste 12-13) bakalım.

```go
func VirtualFreeEx(i *Inject) error {
    var dwFreeType uint32 = MEM_RELEASE
    var size uint32 = 0 //Size must be 0 to MEM_RELEASE all of the region
    rFreeValue,       lastErr := ProcVirtualFreeEx.Call0(
         i.RemoteProcHandle, // HANDLE hProcess
         i.Lpaddr, // LPVOID 1pAddress 0
         uintptr(size), // SIZE_T dwSize 0
         uintptr(dwFreeType)) // DWORD dwFreeType 0
    if rFreeValue == 0 {
         return errors.Wrap(lastErr, "[!] ERROR : Error freeing process memory.")
   1
    fmt.Println("[+] Success: Freed memory region")
    return nil
1
```

**Liste 12-13:** `VirtualFreeEx()` Windows fonksiyonunu kullanarak sanal belleği serbest bırakma (`/ch-12/procInjector/winsyilinject.go`)

`ProcVirtualFreeEx.Call0` fonksiyonu dört argüman alır. İlki, belleği serbest bırakılacak süreçle ilişkilendirilmiş uzak süreç tanıtıcısıdır (`remote process handle`). Bir sonraki argüman, serbest bırakılacak belleğin konumuna işaret eden bir işaretçidir (pointer).

`size` adında bir değişkenin 0 değerine ayarlandığına dikkat edin. Windows API belirtiminde tanımlandığı üzere, belleğin tüm bölgesini tekrar geri kazanılabilir duruma (`reclaimable state`) döndürmek için bu gereklidir. Son olarak, süreç belleğini tamamen serbest bırakmak için `MEM_RELEASE` işlemini (`operation`) geçiriyoruz (ve süreç enjekte etme konusundaki tartışmamızı burada noktalıyoruz).

### Ek Alıştırmalar

Bu kitapta yer alan diğer bölümlerin çoğunda olduğu gibi, bu bölüm de siz kod yazıp deney yaptıkça en çok değeri sağlayacaktır. Bu nedenle, bu bölümü, ele aldığımız fikirleri genişletmek için birkaç meydan okuma ve olasılıkla bitiriyoruz:

- Kod enjekte etmenin en önemli yönlerinden biri, süreç yürütmesini incelemeye ve hata ayıklamaya yetecek düzeyde kullanılabilir bir araç zinciri (tool chain) oluşturmaktır. Hem Process Hacker hem de Process Monitor araçlarını indirip kurun. Ardından, Process Hacker kullanarak hem `Kernel32` hem de `LoadLibrary`'nin bellek adreslerini bulun. Aynı zamanda süreç tanıtıcısını bulun ve bütünlük seviyesine (`integrity level`) ve doğuştan gelen ayrıcalıklara (`inherent privileges`) bakın. Şimdi kodunuzu aynı kurban sürece enjekte edin ve iş parçacığını (thread) bulun.
- Süreç enjekte etme örneğini daha az basit olacak şekilde genişletebilirsiniz. Örneğin, yükü/faydalı yükü (`payload`) disk üzerinde bir dosya yolu üzerinden yüklemek yerine, `MsfVenom` veya `Cobalt Strike` kullanarak shellcode üretin ve bunu doğrudan süreç belleğine yükleyin. Bu, `VirtualAllocEx` ve `LoadLibrary` fonksiyonlarını değiştirmenizi gerektirecektir.
- Bir DLL oluşturun ve içeriğin tamamını belleğe yükleyin. Bu, önceki alıştırmaya benzer; tek fark, shellcode yerine tüm bir DLL yükleyecek olmanızdır. Process Monitor kullanarak bir yol (path) filtresi, süreç filtresi veya her ikisini birden ayarlayın ve sistem DLL yükleme sırasını (`DLL load order`) gözlemleyin. DLL yükleme sırası kaçırılmasını/hijacking’ini ne engeller?
- `Frida` (https://www.frida.re/) adlı bir projeyi kullanarak Google Chrome V8 JavaScript motorunu kurban sürece enjekte edebilirsiniz. Bu araç, hem mobil güvenlik uygulayıcıları hem de geliştiriciler arasında güçlü bir takipçi kitlesine sahiptir; çalışma zamanı analizi (`runtime analysis`), süreç içi hata ayıklama (`in-process debugging`) ve enstrümantasyon yapmak için kullanılabilir. Frida'yı Windows gibi diğer işletim sistemleriyle de kullanabilirsiniz. Kendi Go kodunuzu yazın, Frida'yı bir kurban sürece enjekte edin ve aynı süreç içinde JavaScript çalıştırmak için Frida'yı kullanın. Frida’nın nasıl çalıştığına aşina olmak biraz araştırma gerektirecektir, ama buna değeceğine söz veriyoruz.

### Taşınabilir Çalıştırılabilir (Portable Executable) Dosyası

Bazı durumlarda, kötü amaçlı kodumuzu teslim edecek bir araca (vehicle) ihtiyaç duyarız. Bu, yeni derlenmiş bir çalıştırılabilir dosya (mevcut bir koddaki bir zafiyet üzerinden teslim edilen) ya da örneğin sistemde hâlihazırda var olan değiştirilmiş bir çalıştırılabilir dosya olabilir. Var olan bir çalıştırılabilir dosyayı değiştirmek isteseydik, Windows Portable Executable (PE) dosya ikili veri biçiminin yapısını anlamamız gerekirdi; çünkü bu biçim, bir çalıştırılabilir dosyanın nasıl oluşturulacağını ve çalıştırılabilir dosyanın yeteneklerini belirler.

Bu bölümde hem PE veri yapısını hem de Go'nun `PE` paketini ele alacağız ve bir PE ikili ayrıştırıcı (`binary parser`) inşa edeceğiz. Bu ayrıştırıcıyı, bir PE ikilisinin yapısı içinde gezinmek için kullanabilirsiniz.

### PE Dosya Biçimini Anlamak

Önce PE veri yapısı biçimini tartışalım. Windows PE dosya biçimi, en sık bir çalıştırılabilir (executable), nesne kodu (object code) veya bir DLL olarak temsil edilen bir veri yapısıdır. PE biçimi ayrıca, PE ikilisinin işletim sistemi tarafından ilk yüklenmesi sırasında kullanılan tüm kaynaklara referanslar da tutar; buna, fonksiyonları sıra numarasıyla (`ordinal`) tutan `export address table (EAT)`, fonksiyonları isimle tutan `export name table`, `import address table (IAT)`, `import name table`, `thread local storage` ve kaynak yönetimi (resource management) gibi diğer yapılar dahildir. PE biçimi belirtimini şu adreste bulabilirsiniz:  
https://docs.microsoft.com/en-us/windows/win32/debug/pe-format  
Şekil 12-6, Windows ikilisinin görsel bir temsili olan PE veri yapısını göstermektedir.

```
   Signature 0x5c4d
      DOS header
  PE header PTR 0x3c

       DOS stub

    COFF file header

     Standard fields
                            Optional header 32-bit
  Windows-spec fields
                            Optional header 64-bit
    Data directories
```

**Şekil 12-6:** Windows PE dosya biçimi
