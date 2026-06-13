Şekil 12-4: `uintptr` ve `unsafe.Pointer` kullanırken potansiyel olarak tehlikeli bir işaretçi (pointer)

## 

Görselin üst yarısında, Go tür güvenli işaretçisine (type-safe pointer) referans değeri taşıyan bir `uintptr` gösterilmektedir. Bu sayede, çalışma zamanında referansını koruyacak ve sıkı bir çöp toplayıcı (garbage collector) davranışıyla birlikte çalışacaktır. Görselin alt yarısı ise, `unsafe.Pointer` türüne referans verse de `uintptr` değerinin çöp toplanabildiğini göstermektedir; çünkü Go, rastgele veri türlerine (arbitrary data types) ait işaretçileri ne saklar ne de yönetir. Liste 12-1 bu sorunu göstermektedir.

```go
func state() {
    var onload = createEvents("onload")
    var receive = createEvents("receive")
    var success = createEvents("success")

    mapEvents := make(map[string]interface{})
    mapEvents["messageOnload"] = unsafe.Pointer(onload)
    mapEvents["messageReceive"] = unsafe.Pointer(receive)
    mapEvents["messageSuccess"] = uintptr(unsafe.Pointer(success))

    // This line is safe - retains orginal value
    fmt.Println(*(*string)(mapEvents["messageReceive"].(unsafe.Pointer)))

    // This line is unsafe - original value could be garbage collected
    fmt.Println(*(*string)(unsafe.Pointer(mapEvents["messageSuccess"].(uintptr))))
}

func createEvents(s string) *string {
    return &s
}
```

Liste 12-1: `unsafe.Pointer` ile `uintptr`’ı hem güvenli hem güvensiz şekilde kullanmak

Bu kod listesi, örneğin, bir durum makinesi (state machine) oluşturma girişimi olabilir. Üç değişkeni vardır; `createEvents()` fonksiyonu çağrılarak `onload`, `receive` ve `success` değişkenlerine kendi işaretçi değerleri atanır. Sonrasında, anahtar türü `string` ve değer türü `interface{}` olan bir `map` oluştururuz. `interface{}` türünü kullanmamızın sebebi, farklı (disparate) veri türlerini alabilmesidir. Bu örnekte, hem `unsafe.Pointer` hem de `uintptr` değerlerini tutmak için kullanacağız.

Bu noktada, muhtemelen tehlikeli kod parçalarını fark etmişsinizdir. `mapEvents["messageReceive"]` `map` girdisi `unsafe.Pointer` türünde olsa da, hâlâ `receive` değişkenine orijinal referansını korur ve ilk halindekiyle aynı, tutarlı çıktıyı üretir. Buna karşılık, `mapEvents["messageSuccess"]` `map` girdisi `uintptr` türündedir. Bu, `success` değişkenine referans veren `unsafe.Pointer` değeri bir `uintptr` türüne atandığı anda `success` değişkeninin çöp toplamaya (garbage collection) açık hale geldiği anlamına gelir. Tekrar vurgulamak gerekirse, `uintptr`, bir bellek adresinin literal tam sayı (integer) değerini tutan bir türdür, bir işaretçiye referans değildir. Sonuç olarak, beklenen çıktının üretileceğine dair herhangi bir garanti yoktur; çünkü değer artık mevcut olmayabilir.

`uintptr`’ı `unsafe.Pointer` ile güvenli şekilde kullanmanın bir yolu var mıdır? Bunu, bir değişkenin çöp toplanmasını engelleyebilen `runtime.KeepAlive` fonksiyonundan faydalanarak yapabiliriz.

Go `runtime`’ı, `runtime.KeepAlive` çağrısı sayesinde bir değişkenin yaşam ömrünü (lifetime) uzatabilir. Önceki kod bloğumuzu (Liste 12-2) biraz değiştirerek bunu inceleyelim.

```go
func state() {
    var onload = createEvents("onload")
    var receive = createEvents("receive")
    var success = createEvents("success")

    mapEvents := make(map[string]interface{})
    mapEvents["messageOnload"] = unsafe.Pointer(onload)
    mapEvents["messageReceive"] = unsafe.Pointer(receive)
    mapEvents["messageSuccess"] = uintptr(unsafe.Pointer(success))

    // This line is safe - retains orginal value
    fmt.Println(*(*string)(mapEvents["messageReceive"].(unsafe.Pointer)))

    // This line is unsafe - original value could be garbage collected
    fmt.Println(*(*string)(unsafe.Pointer(mapEvents["messageSuccess"].(uintptr))))

    runtime.KeepAlive(success)
}

func createEvents(s string) *string {
    return &s
}
```

Liste 12-2: Bir değişkenin çöp toplanmasını engellemek için `runtime.KeepAlive()` fonksiyonunu kullanmak

Gerçekten, yalnızca küçük bir satır ekledik. Bu satır `runtime.KeepAlive(success)`, Go çalışma zamanına `success` değişkeninin açıkça serbest bırakılıncaya veya çalışma durumu sona erene kadar erişilebilir kalmasını temin etmesini söyler. Bu, `success` değişkeni bir `uintptr` olarak saklanıyor olsa bile, açık `runtime.KeepAlive()` direktifi nedeniyle çöp toplanamayacağı anlamına gelir.

Go `syscall` paketinin, genel olarak `uintptr(unsafe.Pointer())` kullanımına yoğun şekilde başvurduğunu unutmayın. `syscall()` gibi bazı fonksiyonlar istisnai olarak tür güvenliği sağlasa da, tüm fonksiyonlar bunu yapmaz. Ayrıca, kendi proje kodlarınız üzerinde çalışırken, güvenli olmayan biçimde yığın (stack) veya yığın belleği (heap memory) manipüle etmeyi gerektiren durumlarla neredeyse kesin olarak karşılaşacaksınız.

## `syscall` Paketi ile Proses Enjeksiyonu Gerçekleştirme

Çoğu zaman, kendi kodumuzu bir prosese enjekte etmemiz gerekir. Bu, örneğin bir sistemde uzaktan komut satırı erişimi (shell) elde etmek istememizden ya da kaynak kodu mevcut olmayan bir çalışma zamanı uygulamasını hata ayıklamak istememizden kaynaklanabilir. Proses enjeksiyonunun mekaniklerini anlamak, bellek ikametli (memory-resident) kötü amaçlı yazılım yükleme veya fonksiyonlara hook ekleme gibi daha ilgi çekici görevleri gerçekleştirmenize de yardımcı olacaktır. Her iki durumda da bu bölüm, proses enjeksiyonu gerçekleştirmek için Go'nun Microsoft Windows API'leriyle nasıl etkileşime girebileceğini göstermektedir. Diskte saklanan bir yük/faydalı yükü (payload) mevcut proses belleğine enjekte edeceğiz. Şekil 12-5, genel olay zincirini açıklamaktadır.

---

Orijin proses                                       Kurban proses

1. Kurban prosesine
   ekle (attach):

   `OpenProcess()`
                                                     Proses handle’ı

2. Kurban proses
   üzerinde bellek
   ayır (allocate):

   `VirtualAllocEx()`
                                                     Bellek boşluğu (memory cave)

3. Yük/faydalı yükü
   kurban proses
   belleğine yaz:

   `WriteProcessMemory()`
                                                     Yükün/faydalı yükün konumu

4. Yük/faydalı yükü
   kurban proses
   üzerinde çalıştır:

   `CreateRemoteThread()`

Şekil 12-5: Temel proses enjeksiyonu
