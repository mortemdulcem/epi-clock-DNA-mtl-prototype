Artık bağlantı kurabilir ve `store` koleksiyonunuzu (tabloya eşdeğer) sorgulayabilirsiniz; bunun için, daha sonra oluşturacağımız SQL örnek kodundan (bkz. Liste 7-6) bile daha az satır kod gereklidir.

```go
package main

import (
    "fmt"
    "log"

    mgo "gopkg.in/mgo.v2"
)

type Transaction struct {
    CCNum      string `bson:"ccnum"`
    Date       string `bson:"date"`
    Amount     float32 `bson:"amount"`
    Cvv        string `bson:"cvv"`
    Expiration string `bson:"exp"`
}

func main() {
    session, err := mgo.Dial("127.0.0.1")
    if err != nil {
        log.Panicln(err)
    }

    defer session.Close()

    results := make([]Transaction, 0)
    if err := session.DB("store").C("transactions").Find(nil).All(&results); err != nil {
        log.Panicln(err)
    }

    for _, txn := range results {
        fmt.Println(txn.CCNum, txn.Date, txn.Amount, txn.Cvv, txn.Expiration)
    }
}
```

**Liste 7-6: Bir MongoDB veritabanına bağlanma ve sorgulama (`/ch-7/db/mongo-connect/main.go`)**

Önce, `store` koleksiyonunuzdaki tek bir dokümanı temsil edecek `Transaction` tipini tanımlarsınız. MongoDB içindeki veri gösterimi için kullanılan dahili mekanizma ikili JSON’dur (binary JSON). Bu nedenle, herhangi bir `marshaling` yönergesini tanımlamak için etiketleme (tagging) kullanırsınız. Bu durumda, ikili JSON verisinde kullanılacak eleman adlarını açıkça tanımlamak için etiketleme kullanıyorsunuz.

`main()` fonksiyonunuzda, veritabanınıza bir bağlantı kurarak bir oturum (session) oluşturmak için `mgo.Dial()` fonksiyonunu çağırırsınız, hata oluşmadığından emin olmak için kontrol yapar ve oturumu kapatmak için bir `defer` çağrısı eklersiniz. Ardından `session` değişkenini kullanarak `store` veritabanını sorgular, `transactions` koleksiyonundaki tüm kayıtları çekersiniz. Sonuçları `results` adlı bir `Transaction` slice’ında saklarsınız. Alt tarafta, yapı (struct) etiketleriniz, ikili JSON verisini tanımladığınız tipe `unmarshal` etmek için kullanılır. Son olarak, sonuç kümeniz üzerinde döngü yapar ve bunları ekrana yazdırırsınız. Hem bu durumda hem de bir sonraki bölümdeki SQL örneğinde, çıktınız aşağıdakine benzer görünmelidir:

```bash
$ go run main.go
4444333322221111 2019-01-05 100.12 1234 09/2020
4444123456789012 2019-01-07 2400.18 5544 02/2021
4465122334455667 2019-01-29 1450.87 9876 06/2020
```

## SQL Veritabanlarını Sorgulama

Go, `database/sql` adlı, SQL ve SQL-benzeri veritabanlarıyla etkileşime girmek için bir arayüz tanımlayan standart bir paket içerir. Temel uygulama, bağlantı havuzu (connection pooling) ve işlem (transaction) desteği gibi işlevleri otomatik olarak içerir. Bu arayüze uyan veritabanı sürücüleri, bu yetenekleri otomatik olarak devralır ve API sürücüler arasında tutarlı kaldığı için esasen birbirlerinin yerine kullanılabilir. Kodunuzdaki fonksiyon çağrıları ve uygulama, Postgres, MSSQL, MySQL veya başka bir sürücü kullanıyor olsanız da aynıdır. Bu, istemci tarafında minimum kod değişikliğiyle arka uç (backend) veritabanlarını değiştirmeyi elverişli kılar. Elbette sürücüler veritabanına özgü yetenekleri uygulayabilir ve farklı SQL sözdizimi kullanabilir, ancak fonksiyon çağrıları neredeyse aynıdır.

Bu nedenle, size yalnızca tek bir SQL veritabanına—MySQL’e—nasıl bağlanılacağını göstereceğiz ve diğer SQL veritabanlarını size egzersiz olarak bırakacağız. Aşağıdaki komutla sürücüyü kurarak başlarsınız:

```bash
$ go get github.com/go-sql-driver/mysql
```

Ardından, veritabanına bağlanan ve `transactions` tablonuzdan bilgileri alan basit bir istemciyi, Liste 7-7’deki betiği kullanarak oluşturabilirsiniz.

```go
package main

import (
    "database/sql"
    "fmt"
    "log"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    db, err := sql.Open("mysql", "root:password@tcp(127.0.0.1:3306)/store")
    if err != nil {
        log.Panicln(err)
    }

    defer db.Close()

    var (
        ccnum, date, cvv, exp string
        amount                float32
    )

    rows, err := db.Query("SELECT ccnum, date, amount, cvv, exp FROM transactions")
    if err != nil {
        log.Panicln(err)
    }

    defer rows.Close()
    for rows.Next() {
        err := rows.Scan(&ccnum, &date, &amount, &cvv, &exp)
        if err != nil {
            log.Panicln(err)
        }
        fmt.Println(ccnum, date, amount, cvv, exp)
    }
    if rows.Err() != nil {
        log.Panicln(err)
    }
}
```

**Liste 7-7: Bir MySQL veritabanına bağlanma ve sorgulama (`/ch-7/db/mysql-connect/main.go`)**

Kod, Go’nun `database/sql` paketini içe aktararak başlar. Bu, veritabanıyla etkileşime girmek için Go’nun harika standart SQL kütüphanesi arayüzünü kullanmanıza olanak tanır. Ayrıca MySQL veritabanı sürücünüzü de içe aktarırsınız. Öndeki alt çizgi, sürücünün anonim olarak içe aktarıldığını gösterir; bu, sürücünün dışa açtığı tiplerin doğrudan kullanılmadığı, ancak sürücünün kendisini `sql` paketiyle kaydettiği anlamına gelir; böylece fonksiyon çağrılarını MySQL sürücüsünün kendisi ele alır.

Sonraki adımda, veritabanınıza bir bağlantı kurmak için `sql.Open()` fonksiyonunu çağırırsınız. İlk parametre, hangi sürücünün kullanılacağını belirtir—bu durumda sürücü `mysql`—ve ikinci parametre, bağlantı dizenizi (connection string) belirtir. Ardından, `transactions` tablonuzdaki tüm satırları seçen bir SQL ifadesi geçerek veritabanınızı sorgularsınız ve dönen satırlar üzerinde döngü yapar, verileri değişkenlerinize okur ve değerleri yazdırırsınız.

Bir MySQL veritabanını sorgulamak için yapmanız gerekenler yalnızca bunlardır. Farklı bir arka uç veritabanı kullanmak, kodda sadece şu küçük değişiklikleri gerektirir:

- Doğru veritabanı sürücüsünü içe aktarın.
- `sql.Open()` fonksiyonuna geçirilen parametreleri değiştirin.
- SQL sözdizimini, arka uç veritabanınızın gerektirdiği türe göre ufak düzeltmelerle uyarlayın.

Mevcut çok sayıdaki veritabanı sürücüsü arasında, birçoğu saf Go ile yazılmıştır; birkaçı ise bazı alt seviye etkileşimler için `cgo` kullanır. Kullanılabilir sürücülerin listesini `https://github.com/golang/go/wiki/SQLDrivers` adresinde bulabilirsiniz.
