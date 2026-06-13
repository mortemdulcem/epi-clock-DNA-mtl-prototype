```go
                         if currschema != prevschema {
                              if prevschema != " {
                                   db.Tables = append(db.Tables, table)
                                   s.Databases = append(s.Databases, db)

                             db = dbminer.DatabaselName: currschema, Tables: Mdbminer.Table{}1
                             prevschema = currschema
                             prevtable = ""

                         if currtable != prevtable {
                              if prevtable != "" {
                                   db.Tables = append(db.Tables, table)

                             table = dbminer.Table{Name: currtable, Columns: []string{}}
                             prevtable = currtable

                         table.Columns = append(table.Columns, currcol)
                     }
                     db.Tables = append(db.Tables, table)
                     s.Databases = append(s.Databases, db)
                     if err    schemarows.Err(); err != nil {
                         return nil, err

                     return s, nil

                  func main() {
                      mm, err := New(os.Args[1])
                      if err != nil {
                          panic(err)

                      defer mm.Db.Close()

168   Chopier 7
    if err := dbminer.Search(nr); en 1. nil
        panic(err)

**Liste 7-10: Bir MySQL veritabanı madencisi oluşturma (/ch-7/db/mysql/main.go)**
```

Koda şöyle bir göz attığınızda, büyük olasılıkla çoğunun önceki bölümdeki MongoDB örneğine çok ama çok benzediğini fark edeceksiniz. Aslına bakarsanız, `main()` fonksiyonu birebir aynı.

Başlatma (bootstrapping) fonksiyonları da benzer—yalnızca mantığı MongoDB yerine MySQL ile etkileşime girecek şekilde değiştiriyorsunuz. Bu mantığın `information_schema` veritabanınıza bağlandığına dikkat edin; böylece veritabanı şemasını inceleyebilirsiniz.

Kodun karmaşıklığının büyük kısmı `GetSchema()` uygulamasının içinde yer alır. Tek bir veritabanı sorgusu kullanarak şema bilgisini alabilseniz de, sonuçlar üzerinde döngü kurmanız ve her satırı incelemeniz gerekir; böylece hangi veritabanlarının mevcut olduğunu, her veritabanında hangi tabloların bulunduğunu ve her tabloda hangi sütunların olduğunu belirleyebilirsiniz. MongoDB uygulamanızın aksine, verileri karmaşık yapılara (struct) serilemek (marshal) ve tersine serilemek (unmarshal) için öznitelik etiketlerine sahip JSON/BSON lüksüne sahip değilsiniz; bunun yerine, mevcut satırınızdaki bilgileri izlemek için değişkenler tutar ve yeni bir veritabanı veya tabloyla karşılaşıp karşılaşmadığınızı anlamak için bunları önceki satırdaki verilerle karşılaştırırsınız. En zarif çözüm değil, ama işi görüyor.

Sonrasında, mevcut satırınız için veritabanı adının önceki satırdan farklı olup olmadığını kontrol edersiniz 0. Öyleyse yeni bir `miner.Database` örneği oluşturursunuz. Eğer döngünün ilk yinelemesi değilse, tabloyu ve veritabanını `miner.Schema` örneğinize eklersiniz. Mevcut `miner.Database` örneğinize `miner.Table` örneklerini izlemek ve eklemek için benzer bir mantık kullanırsınız 0. Son olarak, her bir sütunu `miner.Table` örneğinize eklersiniz 0.

Şimdi, çalıştığını doğrulamak için programı Docker MySQL örneğiniz üzerinde çalıştırın; çıktı aşağıdakine benzer olmalıdır:

```bash
$ go run main.go 127.0.0.1
[DB] = store
    [TABLE] = transactions
       [COL]   ccnum
       [COL] = date
       [COL] = amount
       [COL]
       [COL] = exp

[+] HIT: ccnum
```

Çıktı, MongoDB çıktınızdan neredeyse ayırt edilemeyecek kadar benzer olmalıdır. Bunun nedeni, çıktıyı üretenin `dbminer.Schema` değil, `dbminer.Search()` fonksiyonu olmasıdır. Bu, arayüz (interface) kullanmanın gücüdür. Aynı arayüzü paylaşan, fakat farklı altyapılara sahip uygulamalarınız olabilir.

## Summary

Bu bölümde, hem Go’nun yerleşik paketlerini hem de üçüncü taraf kütüphaneleri kullanarak veritabanı etkileşimleri ve dosya sistemi üzerinde gezinmeye (filesystem walking) daldık; veritabanı üstverilerini (metadata) ve dosya adlarını inceledik. Bir saldırgan için bu kaynaklar sıklıkla değerli bilgiler içerir ve bu cazip bilgiyi aramamıza izin veren çeşitli araçlar oluşturduk.

Bir sonraki bölümde, uygulamalı paket (packet) işleme konusuna göz atacaksınız. Özellikle, ağ paketlerini nasıl koklayacağınızı (sniff) ve manipüle edeceğinizi öğreneceksiniz.

## RAW PACKET PROCESSING

Bu bölümde, ağ paketlerini nasıl yakalayacağınızı ve işleyeceğinizi öğreneceksiniz. Paket işleme, düz metin (cleartext) kimlik doğrulama bilgilerini yakalamak, paketlerin uygulama işlevselliğini değiştirmek, trafiği sahtelemek (spoof) ve zehirlemek (poison) gibi pek çok amaçla kullanılabilir. Ayrıca SYN taraması (scan) ve SYN-flood korumalarının üzerinden port taraması yapmak gibi işler için de kullanabilirsiniz.

Sizi, Google’dan harika `gopacket` paketine tanıştıracağız; bu paket, hem paketleri çözmenizi (decode) hem de trafik akışını yeniden birleştirmenizi (reassemble) sağlar. Bu paket, Berkeley Packet Filter (BPF) kullanarak—tcpdump söz dizimi (syntax) olarak da bilinir—trafiği filtrelemenize, `.pcap` dosyalarını okumanıza ve yazmanıza, çeşitli katmanları ve verileri incelemenize ve paketleri manipüle etmenize olanak tanır.

Cihazları nasıl tanımlayacağınızı, sonuçları nasıl filtreleyeceğinizi ve SYN-flood korumalarını atlayabilen bir port tarayıcıyı nasıl oluşturacağınızı göstermek için birkaç örnek üzerinden geçeceğiz.

## Setting Up Your Environment

Bu bölümdeki kodları çalıştırmadan önce, ortamınızı ayarlamanız gerekir. Öncelikle `gopacket` paketini aşağıdaki komutla kurun:

```bash
$ go get github.com/google/gopacket
```

`gopacket`, işletim sisteminin protokol yığını (protocol stack) üzerinden geçmeden çalışabilmek için harici kütüphanelere ve sürücülere dayanır. Bu bölümdeki örnekleri Linux veya macOS üzerinde kullanmak üzere derlemek istiyorsanız, `libpcap-dev` kurmanız gerekir. Bunu `apt`, `yum` veya `brew` gibi çoğu paket yönetim aracıyla yapabilirsiniz. `apt` kullanarak kurulum aşağıdaki gibidir (diğer seçeneklerde de süreç benzerdir):

```bash
$ sudo apt-get install libpcap-dev
```

Bu bölümdeki örnekleri Windows üzerinde derlemek ve çalıştırmak istiyorsanız, çapraz derleme (cross-compile) yapıp yapmayacağınıza bağlı olarak birkaç seçeneğiniz var. Çapraz derleme yapmıyorsanız, bir geliştirme ortamı kurmak daha basittir, ama bu durumda bir Windows makinede Go geliştirme ortamı oluşturmanız gerekir; eğer başka bir ortamı kalabalıklaştırmak istemiyorsanız bu cazip olmayabilir. Şimdilik, Windows ikili dosyaları (binary) derleyebileceğiniz çalışan bir ortamınız olduğunu varsayacağız. Bu ortamda WinPcap kurmanız gerekir. Bunu ücretsiz olarak şu adresten indirip kurabilirsiniz: `https://unow.winfrcap.org/`.
