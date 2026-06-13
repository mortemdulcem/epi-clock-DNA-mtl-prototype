## Veritabanlarını Docker ile Kurmak

Bu bölümde çeşitli veritabanı sistemlerini kuracak ve ardından bu bölümdeki talan (pillaging) örneklerinde kullanacağınız verilerle dolduracaksınız (seed). Mümkün olduğunda, Ubuntu 18.04 sanal makinesi (VM) üzerinde Docker kullanacaksınız. Docker, uygulamaları dağıtmayı ve yönetmeyi kolaylaştıran bir yazılım konteyner platformudur. Uygulamaları ve bağımlılıklarını, dağıtımlarını sadeleştirecek biçimde paketleyebilirsiniz. Konteyner, ana platformun kirlenmesini önlemek için işletim sisteminden yalıtılmıştır. Oldukça kullanışlı bir araçtır.

Bu bölümde, çalışacağınız veritabanları için çeşitli hazır (prebuilt) Docker imajları kullanacaksınız. Henüz kurulu değilse Docker’ı yükleyin. Ubuntu için talimatları `https://docs.docker.com/install/linux/docker-ce/ubuntu` adresinde bulabilirsiniz.

> **NOT**  
> Oracle örneğinin kurulumu ile ilgili ayrıntıları özellikle dışarıda bırakmayı seçtik. Oracle, indirip bir test veritabanı oluşturmak için kullanabileceğiniz VM imajları sağlıyor olsa da, bu adımlarda sizi adım adım yönlendirmenin gereksiz olduğunu düşündük; çünkü aşağıda verilen MySQL örnekleriyle oldukça benzerler. Oracle’a özgü uygulamayı kendi başınıza yapacağınız bir alıştırma olarak bırakıyoruz.

## MongoDB’nin Kurulumu ve Veriyle Doldurulması (Seeding)

MongoDB, bu bölümde kullanacağınız tek NoSQL veritabanıdır. Geleneksel ilişkisel veritabanlarının aksine MongoDB, SQL üzerinden iletişim kurmaz. Bunun yerine MongoDB, verileri almak ve değiştirmek için anlaşılır bir JSON sözdizimi kullanır. MongoDB’yi açıklamaya adanmış kitaplar vardır ve tam bir açıklama bu kitabın kapsamının oldukça dışındadır. Şimdilik Docker imajını kuracak ve sahte verilerle dolduracaksınız.

Geleneksel SQL veritabanlarının aksine MongoDB şemasızdır (schema-less); yani tablo verilerini düzenlemek için önceden tanımlanmış, katı bir kural sistemine uymaz. Bu nedenle, Liste 7-1’de herhangi bir şema tanımı olmadan yalnızca insert komutları göreceksiniz. Önce aşağıdaki komutla MongoDB Docker imajını kurun:

```bash
$ docker run --name some-mongo -p 27017:27017 mongo
```

Bu komut, `mongo` adlı imajı Docker deposundan indirir, `some-mongo` adıyla yeni bir instance (örnek) başlatır — verdiğiniz isim keyfidir — ve yerel 27017 portunu konteynerin 27017 portuna eşler (map). Port eşlemesi kritik önemdedir; çünkü bu sayede veritabanı instance’ına doğrudan işletim sisteminizden erişebilirsiniz. Bu olmadan erişilemez olurdu.

Konteynerin otomatik olarak başlatıldığını, çalışan konteynerleri listeleyerek kontrol edin:

```bash
docker ps
```

Konteyneriniz otomatik başlamadıysa, şu komutu çalıştırın:

```bash
$ docker start some-mongo
```

`start` komutu konteyneri çalışır hale getirmelidir.

Konteyneriniz başlatıldıktan sonra, `run` komutunu kullanarak MongoDB instance’ına bağlanın — `run` komutuna MongoDB istemcisini geçirerek, veritabanıyla etkileşime girip veri doldurabileceksiniz:

```bash
$ docker run -it --link some-mongo:mongo --rm mongo sh \
  -c 'exec mongo "$MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT/store"'
```

Bu büyülü komut, MongoDB istemci ikili dosyasını (binary) yüklü halde içeren, tek kullanımlık (disposable) ikinci bir Docker konteyneri çalıştırır — böylece istemciyi ana işletim sisteminize kurmak zorunda kalmazsınız — ve bunu kullanarak `some-mongo` Docker konteynerindeki MongoDB instance’ına bağlanır. Bu örnekte `test` adlı bir veritabanına bağlanıyorsunuz.

Liste 7-1’de, `transactions` koleksiyonuna bir belge (document) dizisi ekliyorsunuz. (Tüm kod listeleri `/` kök dizininde, `https://github.com/blackhat-go/bhgo` adresinde sağlanan GitHub deposu altında bulunur.)

```js
db.transactions.insert(
  {
    "ccnum" : "4444333322221111",
    "date" : "2019-01-01",
    "amount" : 100.12,
    "cvv" : "1234",
    "exp" : "09/2020"
  },
  {
    "ccnum" : "4444123456789012",
    "date" : "2019-01-07",
    "amount" : 2400.18,
    "cvv" : "5544",
    "exp" : "02/2021"
  },
  {
    "ccnum" : "4465122334455667",
    "date" : "2019-01-29",
    "amount" : 1450.87,
    "cvv" : "9876",
    "exp" : "06/2020"
  }
)
```

**Liste 7-1: Bir MongoDB koleksiyonuna `transactions` ekleme (`/ch-7/db/seed-mongo.js`)**

Bu kadar! Artık bir MongoDB veritabanı instance’ı oluşturdunuz ve sorgulama yapabilmeniz için üç sahte belge içeren bir `transactions` koleksiyonuyla doldurdunuz. Sorgulama kısmına birazdan geleceksiniz; fakat önce, geleneksel SQL veritabanlarını nasıl kuracağınızı ve veriyle dolduracağınızı bilmeniz gerekiyor.

## PostgreSQL ve MySQL Veritabanlarının Kurulumu ve Seed Edilmesi

PostgreSQL (bazı yerlerde Postgres olarak da anılır) ve MySQL, muhtemelen en yaygın, bilinen, kurumsal kalitede, açık kaynak ilişkisel veritabanı yönetim sistemleridir ve her ikisi için de resmi Docker imajları mevcuttur. Benzerlikleri ve kurulum adımlarının genel olarak çakışması nedeniyle, ikisi için de kurulum talimatlarını burada bir araya getirdik.

Önce, bir önceki bölümdeki MongoDB örneğine oldukça benzer şekilde uygun Docker imajını indirip çalıştırın:

```bash
$ docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql
$ docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
```
