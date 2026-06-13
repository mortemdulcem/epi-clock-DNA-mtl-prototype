Birçok güvenlik aracı, çekirdek bileşenlerin belirli bir soyutlama düzeyinde inşa edildiği, işlevselliklerini kolayca genişletmenizi sağlayan **framework**’ler olarak kurgulanır. Düşününce, bu yaklaşım güvenlik uzmanları için oldukça mantıklıdır. Sektör sürekli değişiyor; topluluk, tespitden kaçınmak için sürekli yeni açıklar ve teknikler icat ediyor ve böylece son derece dinamik ve bir ölçüde öngörülemez bir ortam oluşuyor. Ancak, eklentiler (plug-in) ve uzantılar kullanarak, araç geliştiricileri ürünlerini belirli ölçüde geleceğe hazır (future-proof) hale getirebilirler. Araçlarının çekirdek bileşenlerini yeniden kullanarak, zahmetli yeniden yazımlara ihtiyaç duymadan, eklenti tabanlı bir sistem üzerinden sektörün evrimini daha zarif şekilde yönetebilirler.

Büyük topluluk katılımıyla birleştiğinde, Metasploit Framework’ün bu kadar iyi yaşlanmayı başarmasının muhtemel nedeni de budur. Hatta Tenable gibi ticari şirketler bile genişletilebilir ürünler yaratmanın değerini görüyor; Tenable, Nessus zafiyet tarayıcısında imza kontrollerini gerçekleştirmek için eklenti tabanlı bir sisteme dayanıyor.

## Bu Bölümde Ne Yapacağız?

Bu bölümde Go ile iki adet zafiyet tarayıcı uzantısı oluşturacaksınız. Önce yerel (native) Go eklenti sistemini kullanarak, kodunuzu açıkça paylaşılan bir nesne (shared object) olarak derleyerek bunu yapacaksınız. Ardından, aynı eklentiyi, yerel Go eklenti sisteminden daha eski olan gömülü (embedded) bir Lua sistemi kullanarak yeniden inşa edeceksiniz. Java ve Python gibi diğer dillerde eklenti yaratmaya kıyasla, Go’da eklenti yazmanın oldukça yeni bir yapı olduğunu aklınızda bulundurun. Yerel eklenti desteği yalnızca Go 1.8 sürümünden beri mevcut. Dahası, bu eklentileri Windows dinamik bağlantı kitaplıkları (DLL) olarak oluşturabilmeniz de ancak Go 1.10 sürümüyle mümkün hale geldi. Bu bölümdeki tüm örneklerin planlandığı gibi çalışması için, Go’nun en güncel sürümünü kullandığınızdan emin olun.

## Go'nun Yerel Eklenti Sistemini Kullanma

Go’nun 1.8 sürümünden önce, dil eklentileri ya da çalışma zamanında dinamik olarak kod genişletmeyi desteklemiyordu. Java gibi diller, programınızı çalıştırırken bir sınıf veya JAR dosyasını yükleyip içe aktarılan tipleri somutlaştırmanıza (instantiate) ve fonksiyonlarını çağırmanıza izin verirken, Go böyle bir lüks sağlamıyordu. Bazen arayüz (interface) implementasyonları vb. yoluyla işlevselliği genişletebilseniz de, kodun kendisini gerçekten dinamik olarak yükleyip çalıştıramıyordunuz. Bunun yerine, kodu doğru şekilde derleme (compile) zamanında içeri dahil etmeniz gerekiyordu. Örneğin, dosyadan dinamik olarak bir sınıf yükleyen, bu sınıfın bir örneğini oluşturan ve bu örnek üzerinde `someMethod()` fonksiyonunu çağıran aşağıdaki Java işlevselliğini Go’da taklit etmenin bir yolu yoktu:

```java
File file = new File("/path/to/classes/");
URL[] urls = new URL[]{file.toURL()};
ClassLoader cl = new URLClassLoader(urls);
Class clazz = cl.loadClass("com.example.MyClass");
clazz.getConstructor().newInstance().someMethod();
```

Neyse ki, Go’nun daha yeni sürümleri, bu işlevselliği taklit etme yeteneğine sahip, böylece geliştiriciler kodu açıkça bir eklenti olarak kullanılmak üzere derleyebiliyor. Yine de bazı kısıtlamalar mevcut. Özellikle Go 1.10’dan önce, eklenti sistemi yalnızca Linux üzerinde çalışıyordu; yani genişletilebilir framework’ünüzü Linux üzerinde dağıtmanız gerekiyordu.

Go eklentileri, derleme sürecinde paylaşılan nesneler (shared object) olarak oluşturulur. Bu paylaşılan nesneyi üretmek için, `buildmode` seçeneğine `plugin` vererek aşağıdaki derleme komutunu girersiniz:

```bash
$ go build -buildmode=plugin
```

Alternatif olarak, bir Windows DLL oluşturmak için `buildmode` seçeneği olarak `c-shared` kullanın:

```bash
$ go build -buildmode=c-shared
```

Bir Windows DLL oluşturmak için, programınızın fonksiyonlarınızı dışa aktarmak (export) için belirli kurallara uyması ve ayrıca C kütüphanesini içe aktarması (import) gerekir. Bu ayrıntıları kendi başınıza keşfetmenize bırakıyoruz. Bu bölüm boyunca, DLL’leri nasıl yükleyip kullanacağınızı 12. Bölüm’de göstereceğimiz için, neredeyse tamamen Linux eklenti varyantına odaklanacağız.

DLL veya paylaşılan nesneye derleme yaptıktan sonra, ayrı bir program bu eklentiyi çalışma zamanında yükleyip kullanabilir. Dışa aktarılan (exported) fonksiyonların tümüne erişilebilir olacaktır. Paylaşılan bir nesnenin dışa aktarılan özellikleriyle etkileşim kurmak için Go’nun `plugin` paketini kullanırsınız. Bu paketin işlevselliği oldukça yalındır. Bir eklentiyi kullanmak için şu adımları izlersiniz:

- `plugin.Open(filename string)` fonksiyonunu çağırarak bir paylaşılan nesne dosyasını açın ve bir `*plugin.Plugin` örneği oluşturun.
- `*plugin.Plugin` örneği üzerinde `Lookup(symbolName string)` çağırarak, adıyla bir `Symbol` (dışa aktarılan değişken veya fonksiyon) elde edin.
- Programınızın beklediği tipe dönüştürmek için, genel `Symbol` üzerinde bir tür iddiası (type assertion) kullanın.
- Ortaya çıkan dönüştürülmüş nesneyi istediğiniz gibi kullanın.

`Lookup()` çağrısının tüketiciden (consumer) bir sembol adı sağlamasını gerektirdiğini fark etmiş olabilirsiniz. Bu, tüketicinin önceden tanımlanmış ve mümkünse kamuya açık bir adlandırma şemasına sahip olması gerektiği anlamına gelir. Bunu, eklentilerin uyması beklenen tanımlı bir API veya genel bir arayüz (interface) olarak düşünebilirsiniz. Standart bir adlandırma şeması olmadan, yeni eklentiler tüketici kodunda değişiklik yapmanızı gerektirirdi ki bu da eklenti tabanlı bir sistemin tüm amacını boşa çıkarır.

Takip eden örneklerde, eklentilerin belirli bir arayüz tipini döndüren, `New()` adlı dışa aktarılan bir fonksiyon tanımlamasını beklemelisiniz. Bu sayede başlatma (bootstrapping) sürecini standartlaştırabileceksiniz. Bir arayüze geri dönen bir tutamaç (handle) elde etmek, nesne üzerinde fonksiyonları öngörülebilir bir şekilde çağırmamıza olanak tanır.

Şimdi eklenti tabanlı zafiyet tarayıcınızı oluşturmaya başlayalım. Her eklenti, kendi imza kontrol (signature-checking) mantığını uygulayacak. Ana tarayıcı kodunuz, dosya sisteminizde tek bir dizinden eklentilerinizi okuyarak süreci başlatacak. Tüm bunların çalışması için, iki ayrı depo (repository) kullanacaksınız: biri eklentileriniz için, diğeri ise bu eklentileri tüketen ana program için.

## Ana Programı Oluşturma

Eklentilerinizi bağlayacağınız ana programınızla başlayalım. Bu, eklentilerinizi yazma sürecini anlamanıza yardımcı olacak. Depo dizin yapınızı, aşağıda gösterilene uygun şekilde ayarlayın:

```bash
$ tree

cmd
└── scanner
    └── main.go
plugins
└── scanner
    └── scanner.go
```
