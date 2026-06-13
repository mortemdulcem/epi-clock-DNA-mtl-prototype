## Bir Veritabanı Madencisi (Database Miner) İnşa Etmek

Bu bölümde, veritabanı şemasını (örneğin sütun adları) inceleyerek içindeki verilerin çalınmaya değip değmediğini belirleyen bir araç oluşturacaksınız. Örneğin, parolalar, hash’ler, sosyal güvenlik numaraları ve kredi kartı numaralarını bulmak isteyebilirsiniz.

Tek bir devasa yardımcı program yazıp farklı arka uç (backend) veritabanlarını madencilikle uğraştırmak yerine, her veritabanı için ayrı yardımcı programlar yazacak ve uygulamalar arasında tutarlılığı sağlamak için tanımlanmış bir arayüz (interface) kullanacaksınız. Bu esneklik, bu örnek için biraz “aşırı mühendislik” gibi görünebilir; ancak yeniden kullanılabilir ve taşınabilir kod yazma fırsatı sunar.

Arayüz minimum düzeyde olmalı; birkaç temel tür ve fonksiyondan oluşmalı ve veritabanı şemasını almak için tek bir metodun uygulanmasını zorunlu kılmalıdır. `dbminer.go` adlı Liste 7-8, veritabanı madencisinin arayüzünü tanımlar.

```go
package dbminer

import (

    "regexp"

type DatabaseMiner interface {
    GetSchema() (*Schema, error)

type Schema struct {
    Databases []Database
}
type Database struct {
    Name   string
    Tables []Table
}

type Table struct {
    Name    string
    Columns []string
}

func Search(m DatabaseMiner) error {
    s, err := m.GetSchema()
    if err != nil {
        return err
    }

    re := getRegex()
    for _, database := range s.Databases {
        for _, table := range database.Tables {
            for _, field := range table.Columns {
                for _, r := range re {
                    if r.MatchString(field) {
                        fmt.Println(database)
                        fmt.Printf("{-11 HIT: %s\n", field)
                    }
                }
            }
        }
    }

    return nil
}

func getRegex() []*regexp.Regexp {
    return []*regexp.Regexp{
        regexp.MustCompile("(?i)social"),
        regexp.MustCompile("(?i)ssn"),
        regexp.MustCompile("(?i)pass(word)?"),
        regexp.MustCompile("(?i)hash"),
        regexp.MustCompile("(?i)ccnum"),
        regexp.MustCompile("(?i)card"),
        regexp.MustCompile("(?i)security"),
        regexp.MustCompile("(?i)key"),
    }
}

/* Extranneous code omitted for brevity */
```

**Liste 7-8: Veritabanı madencisi uygulaması (`/ch-7/db/dbminer/dbminer.go`)**

Kod, `DatabaseMiner` adlı bir arayüz tanımlayarak başlar ❶. Bu arayüzü uygulayan tüm türler için `GetSchema()` adlı tek bir metod gereklidir. Her arka uç veritabanının, veritabanı şemasını çekmek için kendine özgü mantığa ihtiyaç duyabileceği düşünüldüğünde, her özel yardımcı programın, kullanılan arka uç veritabanı ve sürücüye (driver) özgü mantığı uygulaması beklenir.

Sonrasında, birkaç alt türden oluşan bir `Schema` türünü tanımlarsınız ❷. `Schema` türünü, veritabanı şemasını — yani veritabanları, tablolar ve sütunlar — mantıksal olarak temsil etmek için kullanacaksınız. Arayüz tanımındaki `GetSchema()` fonksiyonunuzun, uygulamalardan bir `*Schema` döndürmesini beklediğini fark etmiş olabilirsiniz.

Şimdi, ana mantığın büyük kısmını barındıran `Search()` adlı tek bir fonksiyon tanımlıyorsunuz. `Search()` fonksiyonu, kendisine fonksiyon çağrısı esnasında bir `DatabaseMiner` örneği geçirilmesini bekler ve bu madenciyi `m` adlı bir değişkende saklar ❸. Fonksiyon, şemayı almak için `m.GetSchema()` çağrısı yaparak başlar ❹. Daha sonra fonksiyon, tüm şema boyunca döngü yaparak sütun adlarını, bir dizi düzenli ifade (regex) değeri ile karşılaştırır ❺. Bir eşleşme bulunduğunda, veritabanı şeması ve eşleşen alan ekrana yazdırılır.

Son olarak, `getRegex()` adlı bir fonksiyon tanımlayın ❻. Bu fonksiyon, Go’nun `regexp` paketini kullanarak regex dizgilerini derler ve bu değerlerin bir `slice`’ını döndürür. Regex listesi, `ccnum`, `ssn` ve `password` gibi yaygın veya ilgi çekici alan adlarıyla eşleşen, büyük/küçük harf duyarsız dizgilerden oluşur.

Veritabanı madencisi arayüzünüz hazır olduğuna göre, veritabanına özgü uygulamalar geliştirebilirsiniz. MongoDB veritabanı madencisiyle başlayalım.

## Bir MongoDB Veritabanı Madencisi Uygulamak

Liste 7-9’daki MongoDB yardımcı programı, Liste 7-8’de tanımlanan arayüzü uygular ve ayrıca Liste 7-6’da yazdığınız veritabanı bağlantı (connectivity) kodunu da entegre eder.

```go
package main

import (

    "github.com/blackhatgobook/ch-7/db/dbminer"
    "gopkg.in/mgo.v2"
    "gopkg.in/mgo.v2/bson"
)

type MongoMiner struct {
    Host    string
    session *mgo.Session
}

func New(host string) (*MongoMiner, error) {
    m := MongoMiner{Host: host}
    err := m.connect()
    if err != nil {
        return nil, err
    }

    return &m, nil
}

func (m *MongoMiner) connect() error {
    s, err := mgo.Dial(m.Host)
    if err != nil {
        return err
    }

    m.session = s
    return nil
}

func (m *MongoMiner) GetSchema() (*dbminer.Schema, error) {
    var s = new(dbminer.Schema)

    dbnames, err := m.session.DatabaseNames()
    if err != nil {
        return nil, err
    }

    for _, dbname := range dbnames {
        db := dbminer.Database{Name: dbname, Tables: []dbminer.Table{}}
        collections, err := m.session.DB(dbname).CollectionNames()
        if err != nil {
            return nil, err
        }

        for _, collection := range collections {
            table := dbminer.Table{Name: collection, Columns: []string{}}

            var docRaw bson.Raw
            err := m.session.DB(dbname).C(collection).Find(nil).One(&docRaw)
            if err != nil {
                return nil, err
            }
```
