## Go'yu Neden Sevmeyebilirsiniz?

Go'nun her probleme mükemmel bir çözüm olmadığının farkındayız. İşte dilin bazı olumsuz yönleri:

- **İkili (binary) boyutu**  
  Yeterince açık. Go'da bir ikili dosya derlediğinizde, bu ikili büyük olasılıkla birkaç megabayt boyutunda olacaktır. Elbette hata ayıklama (debug) sembollerini çıkarabilir ve boyutu azaltmak için bir paketleyici (packer) kullanabilirsiniz, ancak bu adımlar ekstra dikkat gerektirir. Bu, özellikle bir ikiliyi e‑postaya eklemesi, paylaşımlı bir dosya sistemi üzerinde barındırması veya bir ağ üzerinden aktarması gereken güvenlik uzmanları için bir dezavantaj olabilir.

- **Fazla sözcüllük (verbosity)**  
  Go, C#, Java veya hatta C/C++ gibi dillere göre daha az sözcül (verbose) olsa da, basit dil yapısının; listeler (Go'da `slice` olarak adlandırılır), veri işleme, döngüler veya hata yönetimi gibi konularda gereğinden fazla açık/uzun yazmanıza sebep olduğunu düşünebilirsiniz. Python'da tek satırla yazılabilen bir ifade, Go'da kolayca üç satıra dönüşebilir.

## Bölüm Özeti

Bu kitabın ilk bölümü, Go'nun sözdizimi (syntax) ve felsefesine dair temel bir genel bakış sunar. Sonrasında HTTP, DNS ve SMB gibi çeşitli yaygın ağ protokollerini içeren, araç geliştirmede yararlanabileceğiniz örnekleri incelemeye başlıyoruz. Ardından sızma testi uzmanları olarak karşılaştığımız çeşitli taktik ve sorunlara daha derinlemesine giriyor; veri yağmalama, paket koklama (packet sniffing) ve exploit geliştirme gibi konuları ele alıyoruz. Son olarak, kriptografi, Microsoft Windows'a saldırılar ve steganografi uygulamalarına dalmadan önce dinamik, eklentili (pluggable) araçlar nasıl oluşturulur konusuna kısaca değiniyoruz.

Birçok durumda, gösterdiğimiz araçları kendi özel hedeflerinize uyacak şekilde genişletme fırsatınız olacak. Kitap boyunca sağlam örnekler sunuyor olsak da, asıl amacımız, bu örnekleri hedeflerinize uyacak biçimde genişletebilmeniz veya yeniden çalışabilmeniz için size bilgi ve temel sağlamaktır. Amacımız size balık vermek değil, balık tutmayı öğretmektir.

Kitaptaki herhangi bir şeyle devam etmeden önce, yazarlar ve yayınevi olarak bu içeriği yalnızca yasal kullanım amacıyla hazırladığımızı lütfen unutmayın. Seçeceğiniz kötü niyetli veya yasa dışı eylemler için herhangi bir sorumluluk kabul etmiyoruz. Buradaki tüm içerik yalnızca eğitim amaçlıdır; yetkili onay olmaksızın hiçbir sistem veya uygulama üzerinde sızma testi faaliyetleri yürütmeyin.

Aşağıdaki bölümler, her bir bölümün kısa bir genel görünümünü sunar.

## Bölüm 1: Go Temelleri

Bu bölümün amacı, Go programlama dilinin temellerini tanıtmak ve bu kitaptaki kavramları anlamak için gerekli altyapıyı sağlamaktır. Buna temel Go sözdizimi ve deyimlerinin (idiom) kısaltılmış bir incelemesi dahildir. Go ekosistemini; yardımcı araçlar, IDE'ler, bağımlılık yönetimi ve daha fazlası dahil olmak üzere ele alıyoruz. Programlama diline yeni olan okuyucular, Go'nun asgari gerekliliklerini öğrenmeyi bekleyebilir; böylece ilerleyen bölümlerdeki örnekleri anlamaları, uygulamaları ve genişletmeleri mümkün olacaktır.

## Bölüm 2: TCP, Tarayıcılar (Scanner) ve Proxy'ler

Bu bölüm, pratik TCP uygulamaları üzerinden temel Go kavramlarını ve eşzamanlılık (concurrency) ilkel ve kalıplarını, girdi/çıktı (I/O) işlemlerini ve `interface` kullanımını tanıtır. Önce, komut satırı seçeneklerini ayrıştırarak (parse) bir port listesini tarayan basit bir TCP port tarayıcı (`scanner`) oluşturmanızı adım adım anlatacağız. Bu, Go kodunun diğer dillere kıyasla ne kadar basit olabileceğini ortaya koyarken, temel türleri, kullanıcı girdisini ve hata yönetimini anlamanızı sağlayacak.

Sonrasında, eşzamanlı fonksiyonlar (concurrent functions) kullanarak bu port tarayıcının verimliliğini ve hızını nasıl artırabileceğimizi tartışacağız. Ardından temel örneklerden başlayarak bir TCP proxy —bir port yönlendirici (port forwarder)— inşa ederek I/O kavramını tanıtacağız ve kodumuzu daha güvenilir bir çözüm haline getirmek için rafine edeceğiz. Son olarak, Netcat'in "gaping security hole" özelliğini Go'da yeniden oluşturarak, `stdin` ve `stdout`'u manipüle ederken işletim sistemi komutlarını nasıl çalıştıracağınızı ve bunları TCP üzerinden nasıl yönlendireceğinizi öğreteceğiz.

## Bölüm 3: HTTP İstemcileri ve Araçlarla Uzaktan Etkileşim

HTTP istemcileri, modern web sunucu mimarileriyle etkileşimin kritik bileşenleridir. Bu bölüm, çeşitli yaygın web etkileşimlerini gerçekleştirmek için gerekli HTTP istemcilerini nasıl oluşturacağınızı gösterir. Shodan ve Metasploit ile etkileşim kurmak için çeşitli formatları ele alacaksınız. Ayrıca arama motorlarıyla nasıl çalışılacağını; doküman meta verilerini kazımak (scrape) ve ayrıştırmak (parse) için bunların nasıl kullanılacağını ve böylece kurumsal profilleme faaliyetleri için yararlı bilgiler elde etmeyi göstereceğiz.

## Bölüm 4: HTTP Sunucuları, Yönlendirme (Routing) ve Middleware

Bu bölüm, bir HTTP sunucusu oluşturmak için gerekli kavram ve kuralları tanıtır. Yaygın yönlendirme (routing), middleware ve şablonlama (templating) kalıplarını tartışacak, bu bilgiyi kullanarak bir kimlik bilgisi (credential) toplayıcı ve keylogger geliştireceğiz. Son olarak, ters HTTP proxy (reverse HTTP proxy) inşa ederek komuta-kontrol (C2) bağlantılarını nasıl çoklayacağımızı (multiplex) göstereceğiz.

## Bölüm 5: DNS'i Sömürmek

Bu bölümde Go kullanarak temel DNS kavramlarıyla tanışacaksınız. İlk olarak, belirli alan (domain) kayıtlarını aramanın da dahil olduğu istemci işlemlerini gerçekleştireceğiz. Daha sonra, özel bir DNS sunucusu ve DNS proxy'si yazmayı göstereceğiz; her ikisi de C2 operasyonları için kullanışlıdır.

## Bölüm 6: SMB ve NTLM ile Etkileşim

Bu bölümde SMB ve NTLM protokollerini inceleyecek ve bunları Go'da protokol implementasyonlarını tartışmak için temel olarak kullanacağız. SMB protokolünün kısmi bir implementasyonunu kullanarak veri `marshaling` ve `unmarshaling`, özel alan etiketlerinin (custom field tags) kullanımı ve daha fazlasını tartışacağız. Ayrıca bu implementasyonu, SMB imzalama (signing) politikasını almak ve parola tahmin (password guessing) saldırıları gerçekleştirmek için nasıl kullanacağınızı tartışıp göstereceğiz.

## Bölüm 7: Veritabanlarını ve Dosya Sistemlerini Kötüye Kullanmak

Veri yağmalama (pillaging), saldırgan testlerin (adversarial testing) kritik bir yönüdür. Veriler; veritabanları ve dosya sistemleri de dahil olmak üzere birçok kaynaktan beslenir. Bu bölüm, çeşitli veritabanlarına bağlanmanın ve onlarla etkileşimde bulunmanın temel yollarını tanıtır...
