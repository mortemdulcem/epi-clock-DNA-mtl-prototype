Kapsayıcılarınız (container) oluşturulduktan sonra, çalıştıklarını doğrulayın; eğer çalışmıyorlarsa `docker start name` komutuyla onları başlatabilirsiniz.

Sonra, uygun istemciyi kullanarak kapsayıcılara bağlanabilir—yine, ana makineye (host) ek dosyalar kurmamak için Docker imajını kullanarak—ve veritabanını oluşturup başlangıç verilerini (seed) eklemeye devam edebilirsiniz. Liste 7-2’de, MySQL mantığını görebilirsiniz.

```bash
$ docker run -it --link some-mysql:mysql --rm mysql sh -c \
'exec mysql -h IMYSQL_PORT 3306 TCP ADDR" -P1MYSQL_PORT_3306_TCP_PORT" \
                           A551 7JORD"'
-uroot -p"$MY50.1_ ENV_MYSCILJOOTJ
mysql> create database store;
mysql> use store;
mysql> create table transactions(ccnum varchar(32), date date, amount float(7,2),
     -> cvv char(4), exp date);
```

**Liste 7-2: Bir MySQL veritabanı oluşturma ve ilklendirme**

Bu liste, takip edenle birlikte, uygun veritabanı istemci ikili dosyasını çalıştıran geçici bir Docker kabuğu (shell) başlatır. `store` adlı veritabanını oluşturur ve ona bağlanır, ardından `transactions` adlı bir tablo oluşturur. Her iki liste de özünde aynıdır; aralarındaki tek fark, farklı veritabanı sistemlerine göre uyarlanmış olmalarıdır.

Liste 7-3’te, sözdizimi açısından MySQL’den biraz farklı olan Postgres mantığını görebilirsiniz.

```bash
$ docker run -it --rm --link some-postgres:postgres postgres psql -h postgres -0 postgres
postgres4 create database store;
postgres4 \connect store
store=# create table transactions(ccnum varchar(32), date date, amount money, cvv
       char(4), exp date);
```

**Liste 7-3: Bir Postgres veritabanı oluşturma ve ilklendirme**

Hem MySQL hem de Postgres’te, işlemlerinizi (transactions) eklemek için kullanılan sözdizimi aynıdır. Örneğin, Liste 7-4’te, bir MySQL `transactions` koleksiyonuna (collection) üç belgeyi (document) nasıl ekleyeceğinizi görebilirsiniz.

```sql
mysql> insert into transactions(ccnum, date, amount, cvv, exp) values
   -> ('4444333322221111', '2019-01-05', 100.12, '2234', 2020-09-01');
mysql> insert into transactions(ccnum, date, amount, cvv, exp) values
    > ('4444123456789012', '2019-01-07', 2400.18, '5544', '2021-02-01');
mysql> insert into transactions(ccnum, date, amount, cvv, exp) values
    > ('4465122334455667', '2019-01-29', 1450.87, '9876', '2019-06-01');
```

**Liste 7-4: İşlemleri MySQL/Postgres veritabanlarına ekleme (`/ch-7/db/seed-pg-mysql.sql`)**

Aynı üç belgeyi Postgres veritabanınıza eklemeyi deneyin.

## Microsoft SQL Server Veritabanlarını Kurma ve Başlangıç Verisi Eklemek

2016’da Microsoft, bazı çekirdek teknolojilerini açık kaynak (open source) yapma yönünde önemli adımlar atmaya başladı. Bu teknolojilerden biri de Microsoft SQL (MSSQL) Server’dı. Uzun süre mümkün olmayan bir şeyi—yani, MSSQL Server’ı bir Linux işletim sistemi üzerine kurmayı—gösterirken bu bilgiyi vurgulamak yerinde olacaktır. Dahası, bunun için bir Docker imajı var ve aşağıdaki komutla kurabilirsiniz:

```bash
$ docker run --name some-mssql -p 1433:1433 -e 'ACCEPT_EULAW \
-e '5A_PASSWORD=Password11 1 -d microsoft/mssql-server-linux
```

Bu komut, önceki iki bölümde çalıştırdıklarınıza benzer; ancak dokümantasyona göre `SA_PASSWORD` değerinin karmaşık olması gerekir—büyük harf, küçük harf, rakam ve özel karakter kombinasyonu—aksi takdirde kimlik doğrulaması yapamayacaksınız. Bu yalnızca bir test örneği olduğundan, yukarıdaki değer basit olsa da bu gereksinimleri asgari düzeyde karşılar—kurumsal ağlarda sıkça gördüğümüz gibi!

İmaj kurulduktan sonra, Liste 7-5’te olduğu gibi kapsayıcıyı başlatın, şemayı oluşturun ve veritabanına başlangıç verilerini ekleyin.

```bash
$ docker exec -it some-mssql /opt/mssql-tools/bin/sqlcmd -5 localhost
-U sa -P 'Password1!'
> create database store;
> go
> use store;
> create table transactions(ccnum varchar(32), date date, amount decimal(7,2),
> cvv char(4), exp date);
> go
> insert into transactions(ccnum, date, amount, cvv, exp) values
> ('4444333322221111', '2019-01-05', 100.12, '1234', '2020-09-01');
> insert into transactions(ccnum, date, amount, cvv, exp) values
> ('4444123456789012', '2019-01-07', 2400.18, '5544', '2021-02-01');
> insert into transactions(ccnum, date, amount, cvv, exp) values
> ('4465122334455667', '2019-01-29', 1450.87, 9876', '2020-06-01');
> go
```

**Liste 7-5: Bir MSSQL veritabanı oluşturma ve başlangıç verisi ekleme**

Önceki liste, MySQL ve Postgres için daha önce gösterdiğimiz mantığı tekrarlar. Hizmete bağlanmak için Docker kullanır, `store` veritabanını oluşturup ona bağlanır ve `transactions` tablosunu oluşturup başlangıç verilerini ekler. Bunu diğer SQL veritabanlarından ayrı sunuyoruz, çünkü MSSQL’e özgü bazı sözdizimleri vardır.

## Go’da Veritabanlara Bağlanmak ve Sorgulamak

Artık çalışabileceğiniz çeşitli test veritabanlarına sahip olduğunuza göre, bir Go istemcisinden bu veritabanlarına bağlanmak ve onları sorgulamak için mantığı oluşturabilirsiniz. Bu tartışmayı iki başlığa böldük: biri MongoDB, diğeri ise geleneksel SQL veritabanları için.

### MongoDB’yi Sorgulamak

Mükemmel bir standart SQL paketi olmasına rağmen, Go; NoSQL veritabanlarıyla etkileşim için benzer bir paket barındırmaz. Bunun yerine, bu etkileşimi kolaylaştırmak için üçüncü taraf paketlere güvenmeniz gerekir. Her üçüncü taraf paketin implementasyonunu incelemek yerine yalnızca MongoDB’ye odaklanacağız. Bunun için `mgo` (mango diye okunur) DB sürücüsünü kullanacağız.

Aşağıdaki komutla `mgo` sürücüsünü kurarak başlayın:

```bash
$ go get gopkg.in/mgo.v2
```
