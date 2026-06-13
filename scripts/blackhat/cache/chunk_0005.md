GitHub Atom

GitHub’un IDE’si olan Atom (https://atom.io), topluluk odaklı paketlerin geniş bir yelpazesine sahip, hack’lenebilir (özelleştirilebilir) bir metin düzenleyicidir. Vim’den farklı olarak Atom, Şekil 1-2’de gösterildiği gibi, terminal içi bir çözüm yerine bağımsız bir IDE uygulaması sunar.

Şekil 1-2: Go desteğiyle Atom

Atom da Vim gibi ücretsizdir. Döşemeli pencere (tiling) düzeni, paket yönetimi, sürüm kontrolü, hata ayıklama (debugging), otomatik tamamlama (autocomplete) ve kutudan çıktığı haliyle ya da özel Go desteği sağlayan `go-plus` eklentisi (https://atom.io/packages/go-plus) aracılığıyla pek çok ek özellik sunar.

Microsoft Visual Studio Code

Microsoft’un Visual Studio Code’u, ya da kısaca VS Code (https://code.visualstudio.com), muhtemelen yapılandırılması en kolay ve en fazla özelliğe sahip IDE uygulamalarından biridir. Şekil 1-3’te gösterildiği gibi VS Code tamamen açık kaynaklıdır ve MIT lisansı altında dağıtılır.

Şekil 1-3: Go desteğiyle VS Code IDE

VS Code; temalar, sürümleme (versioning), kod tamamlama, hata ayıklama, linting ve biçimlendirme (formatting) için çok çeşitli eklentiler destekler. Go entegrasyonunu `vscode-go` eklentisiyle (https://github.com/Microsoft/vscode-go/) elde edebilirsiniz.

JetBrains GoLand

JetBrains’in geliştirme araçları koleksiyonu, hem verimli hem de zengin özelliklidir; bu da profesyonel geliştirme ve hobi projelerini gerçekleştirmeyi kolaylaştırır. Şekil 1-4, JetBrains GoLand IDE’sinin nasıl göründüğünü göstermektedir.

GoLand, JetBrains’in Go diline adanmış ticari IDE’sidir. GoLand fiyatlandırması; öğrenciler için ücretsiz, bireysel kullanıcılar için yıllık 89 dolar ve organizasyonlar için yıllık 199 dolar aralığındadır. GoLand; hata ayıklama, kod tamamlama, sürüm kontrolü, linting, biçimlendirme ve daha fazlası dâhil olmak üzere zengin bir IDE’den beklenen tüm özellikleri sunar. Ücretli bir ürüne para ödemek cazip gelmeyebilir, ancak GoLand gibi ticari ürünler genellikle resmî destek, dokümantasyon, zamanında hata düzeltmeleri ve kurumsal yazılımlarla birlikte gelen diğer güvenceleri sağlar.

Şekil 1-4: GoLand ticari IDE

## Yaygın Go Araç Komutlarını Kullanma

Go, geliştirme sürecini basitleştiren birkaç kullanışlı komutla birlikte gelir. Bu komutlar genellikle IDE’lere de entegre edilmiştir; böylece araçlar geliştirme ortamları arasında tutarlı kalır. Şimdi bu komutlardan bazılarına göz atalım.

### `go run` Komutu
