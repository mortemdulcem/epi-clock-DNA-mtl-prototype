Bu özel durumda, nesnenin Go'daki bir struct türüne oldukça benzediğini görebiliyoruz. Ancak C++ struct alan türleri her zaman Go türleriyle birebir uyuşmaz ve Microsoft veri türleri de her zaman Go veri türleriyle eşleşmez.

Windows veri türü tanımları başvurusu, https://docs.microsoft.com/en-us/windows/desktop/WinProg/windows-data-types/ adresinde yer alır ve bir Windows veri türünü Go’nun karşılık gelen veri türüyle uzlaştırırken faydalı olabilir. Tablo 12-1, bu bölümün ilerleyen kısımlarındaki işlem enjeksiyonu örneklerinde kullanacağımız tür dönüştürmelerini kapsar.

Tablo 12-1: Windows Veri Türlerinin Go Veri Türlerine Eşlenmesi

| Windows data Type | Go data type                           |
|-------------------|----------------------------------------|
| BOOLEAN           | byte                                   |
| BOOL              | int32                                  |
| BYTE              | byte                                   |
| DWORD             | uint32                                 |
| DWORD32           | uint32                                 |
| DWORD64           | uint64                                 |
| WORD              | uint16                                 |
| HANDLE            | uintptr (unsigned integer pointer)     |
| LPVOID            | uintptr                                |
| SIZE_T            | uintptr                                |
| LPCVOID           | uintptr                                |
| HMODULE           | uintptr                                |
| LPCSTR            | uintptr                                |
| LPDWORD           | uintptr                                |

Go dokümantasyonu, `uintptr` veri türünü “herhangi bir işaretçinin (pointer) bit desenini tutacak kadar büyük olan bir tamsayı türü” olarak tanımlar. `uintptr` özel bir veri türüdür; bunun nedenini bu bölümde ileride, 266. sayfadaki “The unsafe.Pointer and uintptr Types” kısmında Go’nun `unsafe` paketi ve tür dönüşümlerini tartışırken göreceksiniz. Şimdilik, Windows API dokümantasyonunu incelemeyi bitirelim.

Sırada, bir nesnenin parametrelerine bakmanız gerekir; dokümantasyondaki Parameters (Parametreler) bölümü bu detayları sağlar. Örneğin, ilk parametre olan `dwDesiredAccess`, işlem tanıtıcısının (process handle) sahip olması gereken erişim seviyesine ilişkin ayrıntıları verir. Sonrasında Return Value (Dönüş Değeri) bölümü, hem başarılı hem de başarısız bir sistem çağrısı için beklenen değerleri tanımlar (Şekil 12-2).

Dönüş Değeri  
Fonksiyon başarılı olursa, dönüş değeri belirtilen işleme (process) ait açık bir tanıtıcıdır (handle).

Fonksiyon başarısız olursa, dönüş değeri NULL olur. Genişletilmiş hata bilgisini almak için `GetLastError` çağırın.

Şekil 12-2: Beklenen dönüş değerinin tanımı

Yaklaşan örnek kodumuzda `syscall` paketini kullanırken `GetLastError` hata mesajından faydalanacağız; ancak bu, standart hata işleme (örneğin `if err != nil` söz dizimi) yaklaşımından çok az sapacaktır.

Windows API belgemizin son bölümü olan Requirements (Gereksinimler) kısmı, Şekil 12-3’te gösterildiği gibi önemli ayrıntılar sağlar. Son satır, dışa aktarılabilir fonksiyonları (örneğin `OpenProcess()`) içeren dinamik bağlantı kitaplığını (DLL) tanımlar ve Windows DLL modülümüzün değişken bildirimlerini oluştururken gerekli olacaktır. Başka bir deyişle, ilgili Windows DLL modülünü bilmeden Go içinden ilgili Windows API fonksiyonunu çağıramayız. Bu, ileride işlem enjeksiyonu (process injection) örneğimize geçtiğimizde daha da netleşecektir.

Requirements

Minimum supported client: Windows XP [desktop apps | UWP apps]  
Minimum supported server: Windows Server 2003 [desktop apps | UWP apps]  
Target Platform: Windows  
Header: `processthreadsapi.h` (include Windows Server 2003, Windows Vista, Windows 7, Windows Server 2008, Windows Server 2008 R2, Windows 8)  
Library: `Kernel32.lib`  
DLL: `Kernel32.dll`

Şekil 12-3: Requirements bölümü, API’yi çağırmak için gereken kütüphaneyi tanımlar.

## unsafe.Pointer ve uintptr Türleri

Go `syscall` paketiyle uğraşırken, kesinlikle Go’nun tür güvenliği (type-safety) korumalarını bir şekilde es geçmemiz gerekecek. Bunun sebebi, örneğin, paylaşımlı bellek yapıları kurmamız ve Go ile C arasında tür dönüşümleri yapmamız gerekecek olmasıdır. Bu bölüm, belleği manipüle edebilmeniz için ihtiyaç duyduğunuz temel bilgiyi sağlar; ancak Go’nun resmi dokümantasyonunu da ayrıca incelemelisiniz.

Go’nun güvenlik önlemlerini, bu bölümde (ve Bölüm 9’da bahsedilen) Go’nun `unsafe` paketini kullanarak atlayacağız. Bu paket, Go programlarının tür güvenliğini aşan işlemler içerir. Go, bize yardımcı olmak için dört temel kılavuz ortaya koymuştur:

- Herhangi bir türdeki işaretçi (pointer) değeri `unsafe.Pointer`’a dönüştürülebilir.
- Bir `unsafe.Pointer`, herhangi bir türdeki işaretçi değerine dönüştürülebilir.
- Bir `uintptr`, `unsafe.Pointer`’a dönüştürülebilir.
- Bir `unsafe.Pointer`, `uintptr`’a dönüştürülebilir.

> **WARNING**  
> `unsafe` paketini içe aktaran paketlerin taşınabilir (portable) olmayabileceğini aklınızda bulundurun; ayrıca Go genellikle Go 1 sürümüyle geriye dönük uyumluluk sağlasa da, `unsafe` paketini kullanmak bu garantilerin tamamını bozar.

`uintptr` türü, diğer kullanım alanlarının yanı sıra, yerel güvenli türler arasında tür dönüşümü ya da aritmetik yapmanızı sağlar. `uintptr` bir tamsayı türü olmasına rağmen, bir bellek adresini temsil etmek için yaygın olarak kullanılır. Tür güvenli işaretçilerle birlikte kullanıldığında, Go’nun yerleşik çöp toplayıcısı (garbage collector) çalışma zamanında ilgili referansları korur.

Ancak `unsafe.Pointer` devreye girdiğinde durum değişir. `uintptr`’ın esasen sadece işaretsiz (unsigned) bir tamsayı olduğunu hatırlayın. Bir işaretçi değeri `unsafe.Pointer` kullanılarak oluşturulur ve ardından `uintptr`’a atanırsa, Go’nun çöp toplayıcısının başvurulan bellek konumunun değerinin bütünlüğünü koruyacağına dair herhangi bir garanti yoktur. Şekil 12-4 bu sorunu daha ayrıntılı açıklamaya yardımcı olur.

Go güvenli işaretçi → bellek adresi korunur, çöp toplayıcı referansı takip eder.  
Go güvensiz işaretçi (`unsafe.Pointer` + `uintptr`) → bellek geri kazanılabilir (reclaimed) ve adres artık geçerli olmayabilir.
