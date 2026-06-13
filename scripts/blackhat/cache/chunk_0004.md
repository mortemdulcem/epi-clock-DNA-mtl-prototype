### Go İkili Dosyasının Konumunu Belirlemek için GOROOT Ayarlama

Sonraki adımda, işletim sisteminin Go kurulumunu nasıl bulacağını bilmesi gerekir. Çoğu durumda, Go’yu *Nix/BSD tabanlı bir sistemde `/usr/local/go` gibi varsayılan bir yola kurduysanız burada hiçbir şey yapmanız gerekmez. Ancak, Go’yu standart olmayan bir yola kurmayı seçtiyseniz veya Go’yu Windows üzerinde yüklüyorsanız, işletim sistemine Go ikili dosyasını (binary) nerede bulacağını söylemeniz gerekir.

Bunu komut satırınızdan, rezerve edilmiş `GOROOT` ortam değişkenini ikili dosyanızın bulunduğu konuma ayarlayarak yapabilirsiniz. Ortam değişkenlerini ayarlamak işletim sistemine özgüdür. Linux veya macOS üzerinde bunu `~/.profile` dosyanıza ekleyebilirsiniz:

```bash
set GOROOT ./path/to/go
```

Windows’ta ise bu ortam değişkenini Denetim Masası’ndaki System bölümünden, Environment Variables düğmesine tıklayarak ekleyebilirsiniz.

### Go Çalışma Alanınızın Konumunu Belirlemek için GOPATH Ayarlama

Yalnızca belirli kurulum senaryolarında gerekli olan `GOROOT` ayarının aksine, `GOPATH` adlı bir ortam değişkenini her zaman tanımlamanız gerekir. Bu değişken, Go araç takımına kaynak kodlarınızın, üçüncü taraf kütüphanelerinizin ve derlenmiş programlarınızın nerede bulunacağını söyler. Bu, seçtiğiniz herhangi bir konum olabilir. Bu temel çalışma alanı (workspace) dizinini seçtikten veya oluşturduktan sonra, içinde `bin`, `pkg` ve `src` (bu dizinler hakkında birazdan daha fazla konuşacağız) adlı üç alt dizin oluşturun. Ardından, `GOPATH` isimli bir ortam değişkenini bu temel çalışma alanı dizinini gösterecek şekilde ayarlayın. Örneğin, projelerinizi Linux üzerinde ev dizininizde bulunan `gocode` adlı bir dizine koymak istiyorsanız, `GOPATH`’i aşağıdaki gibi ayarlarsınız:

```bash
GOPATH=$HOME/gocode
```

`bin` dizini, derlenmiş ve kurulmuş Go ikili (executable) dosyalarınızı içerecektir. Derlenen ve kurulan ikili dosyalar otomatik olarak bu konuma yerleştirilir. `pkg` dizini, üçüncü taraf Go bağımlılıkları da dahil olmak üzere çeşitli package nesnelerini saklar; kodunuz bunlara ihtiyaç duyabilir.

Örneğin, HTTP yönlendirmesini daha zarif şekilde ele alan başka bir geliştiricinin kodunu kullanmak isteyebilirsiniz. `pkg` dizini, bu geliştiricinin implementasyonunu kendi kodunuzda kullanabilmeniz için gerekli ikili yapıtları (binary artifacts) barındıracaktır. Son olarak, `src` dizini yazacağınız tüm “kötü” (evil) kaynak kodu içerecektir.

Çalışma alanınızın konumu keyfidir, ancak içindeki dizinler bu adlandırma kuralı ve yapısına uymak zorundadır. Bu bölümde daha sonra öğreneceğiniz derleme (build), paketleme ve package yönetimi komutlarının tümü, bu ortak dizin yapısına dayanır. Bu önemli kurulum olmadan Go projeleri derlenmeyecek veya gerekli bağımlılıklarını bulamayacaktır!

Gerekli `GOROOT` ve `GOPATH` ortam değişkenlerini yapılandırdıktan sonra, doğru şekilde ayarlandıklarını doğrulayın. Bunu Linux ve Windows’ta `set` komutu ile yapabilirsiniz. Ayrıca sisteminizin Go ikili dosyasını bulabildiğini ve beklediğiniz Go sürümünü kurduğunuzu `go version` komutuyla kontrol edin:

```bash
$ go version
go version go1.11.5 linux/amd64
```

Bu komut, kurduğunuz ikili dosyanın sürümünü döndürmelidir.

### Tümleşik Geliştirme Ortamı Seçmek (IDE)

Sonraki olarak, muhtemelen kodunuzu yazacağınız bir tümleşik geliştirme ortamı (integrated development environment, IDE) seçmek isteyeceksiniz. Bir IDE zorunlu olmasa da, birçoğu kodunuzdaki hataları azaltmaya yardımcı olan özellikler, sürüm kontrolü (version control) için kısayollar, package yönetimi desteği ve daha fazlasını sunar. Go hala görece genç bir dil olduğundan, diğer dillere göre o kadar olgun IDE’ler olmayabilir.

Neyse ki, son birkaç yıldaki gelişmeler size birkaç tam özellikli seçenek sunuyor. Bunlardan bazılarını bu bölümde inceleyeceğiz. Daha kapsamlı bir IDE veya editör listesi için, Go wiki sayfasındaki `IDEsAndTextEditorPlugins` sayfasına bakabilirsiniz:  
`https://github.com/golang/go/wiki/IDEsAndTextEditorPlugins`  
Bu kitap IDE/editör konusunda tarafsızdır; yani sizi tek bir çözüme zorlamayacağız.

### Vim Editörü

Pek çok işletim sistemi dağıtımında bulunan Vim metin editörü, çok yönlü, genişletilebilir ve tamamen açık kaynaklı bir geliştirme ortamı sağlar. Vim’in cazip özelliklerinden biri, kullanıcıların her şeyi terminalden, gösterişli GUI’ler araya girmeden çalıştırmasına izin vermesidir.

Vim, temaları özelleştirmenize, sürüm kontrolü eklemenize, snippet’ler tanımlamanıza, yerleşim ve kod gezinme (navigation) özellikleri eklemenize, otomatik tamamlama (autocomplete) yapmanıza, sözdizimi renklendirme (syntax highlighting) ve linting gerçekleştirmenize ve daha fazlasına olanak tanıyan geniş bir eklenti ekosistemine sahiptir. Vim’in en yaygın eklenti yönetim sistemleri arasında Vundle ve Pathogen bulunur.

Go için Vim kullanmak amacıyla, aşağıda Şekil 1-1’de gösterilen `vim-go` eklentisini (`https://github.com/fatih/vim-go/`) kurun.

![Figure 1-1](figure_1_1_placeholder)

**Şekil 1-1: `vim-go` eklentisi**

Elbette, Go geliştirme için Vim kullanmak istiyorsanız Vim’le rahat olmanız gerekir. Ayrıca, geliştirme ortamınızı istediğiniz tüm özelliklerle özelleştirmek sinir bozucu bir süreç olabilir. Ücretsiz olan Vim’i kullanırsanız, muhtemelen ticari IDE’lerin sunduğu bazı kolaylıklardan feragat etmeniz gerekecektir.
