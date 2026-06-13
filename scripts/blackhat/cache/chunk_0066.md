```go
             var doc bson.Raw0
             if err := docRaw.Unmarshal(&doc); err 1= nil {ID
                  if err 1= nil {
                       return nil, err

             for _, f := range doc {
                 table.Columns = append(table.Columns, f.Name)

             db.Tables = append(db.Tables, table)

        s.Databases    append(s.Databases, db)
    }
    return s, nil

func main() {

    mm, err := New(os.Args[1])
    if err 1= nil {
        panic(err)

 CD if err := dbminer.Search(mm); err 1= nil {
        panic(err)

**Liste 7-9: Bir MongoDB veritabanı madencisi oluşturma (/ch-7/db/mongo/main.go)**
```

Önce, `DatabaseMiner` arayüzünü tanımlayan `dbminer` paketini içe aktarıyorsunuz ❶. Ardından, arayüzü uygulamak için kullanacağınız bir `MongoMiner` tipi tanımlıyorsunuz ❷. Kolaylık olması için, `MongoMiner` tipinizin yeni bir örneğini oluşturan bir `New()` fonksiyonu tanımlıyorsunuz ❸; bu fonksiyon, veritabanına bağlantı kurmak için `connect()` adlı bir metodu çağırıyor ❹. Bu mantığın tamamı esasen kodunuzu önyükleyerek, Liste 7-6’da tartışılan biçime benzer bir şekilde veritabanına bağlanıyor.

Koddaki en ilginç kısım, `GetSchema()` arayüz metodunu (interface method) uygulamanız ❺. Liste 7-6’daki önceki MongoDB örnek kodundan farklı olarak, artık MongoDB üstverisini (metadata) inceliyorsunuz; önce veritabanı isimlerini alıyor ❻, sonra da bu veritabanlarının her birinin koleksiyon (collection) isimlerini almak için onların üzerinde döngü kuruyorsunuz ❼. Son olarak, ham (raw) dokümanı alıyorsunuz ve bu, tipik bir MongoDB sorgusundan farklı olarak tembel ayrıştırma (lazy unmarshaling) kullanıyor ❽.

Tembel ayrıştırma, kaydı genel bir yapıya açıkça ayrıştırabilmenizi (unmarshal) sağlayarak alan adlarını incelemenize imkân verir ❾. Tembel ayrıştırma olmasaydı, veriyi sizin tanımladığınız bir `struct` içine nasıl ayrıştıracağınıza dair kodunuza talimat verebilmek için muhtemelen `bson` etiket (tag) öznitelikleri kullanan açık bir tip tanımlamak zorunda kalırdınız. Bu durumda ise alan tipleri veya yapısıyla ilgilenmiyorsunuz (veya bilmiyorsunuz)—sadece alan adlarını (verinin kendisini değil) istiyorsunuz—dolayısıyla, verinin yapısını önceden bilmeye gerek kalmadan yapılandırılmış veriyi ayrıştırmak için bu yaklaşımı kullanıyorsunuz.

`main()` fonksiyonunuz, tek argüman olarak MongoDB örneğinizin IP adresini bekliyor, her şeyi önyüklemek için `New()` fonksiyonunuzu çağırıyor ve ardından `MongoMiner` örneğinizi ona geçirerek `dbminer.Search()` fonksiyonunu çağırıyor ❿. Hatırlarsanız, `dbminer.Search()`, kendisine verilen `DatabaseMiner` örneği üzerinde `GetSchema()` çağırıyor; bu, `MongoMiner` implementasyonunuzun çalışmasına neden oluyor ve sonuçta Liste 7-8’deki regex listesine karşı aranan bir `dbminer.Schema` oluşturuluyor.

Aracınızı çalıştırdığınızda aşağıdaki çıktıyı elde ediyorsunuz:

```bash
$ go run main.go 127.0.0.1
[DB] = store
    [TABLE] = transactions
       [COL] = _id
       [COL] = ccnum
       [COL] = date
       [COL] = amount
       [COL] = cvv
       [COL] = exp

[+] HIT: ccnum
```

Bir eşleşme buldunuz! Görünüş olarak pek hoş olmayabilir ama işini görüyor—`ccnum` adlı bir alan içeren veritabanı koleksiyonunu başarıyla tespit ediyor.

MongoDB implementasyonunuzu tamamladığınıza göre, bir sonraki bölümde aynı işi bir MySQL arka uç (backend) veritabanı için yapacaksınız.

## Bir MySQL Veritabanı Arayıcı (Miner) Uygulamak

MySQL implementasyonunuzun çalışması için `information_schema.columns` tablosunu inceleyeceksiniz. Bu tablo, tüm veritabanları ve yapıları hakkında; tablo ve sütun adları dahil üstveri (metadata) tutar. Veriyi tüketmeyi (consume) olabildiğince basit kılmak için, MySQL’in yerleşik bazı veritabanları hakkında—yağmalama (pillaging) çabalarınız açısından önemsiz olan—bilgileri kaldıran aşağıdaki SQL sorgusunu kullanın:

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM columns
    WHERE TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
    ORDER BY TABLE_SCHEMA, TABLE_NAME
```

Sorgu, aşağıdakine benzer sonuçlar üretir:

```text
1 TABLE_SCHEMA 1 TABLE_NAME   1 COLUMN_NAME 1
+              +              +             +
1 store        1 transactions 1 ccnum       1
1 store        1 transactions 1 date        1
1 store        1 transactions 1 amount      1
1 store        1 transactions 1 cvv         1
1 store        1 transactions 1 exp         1
--snip--
```

Bu sorguyu kullanarak şema bilgisini elde etmek oldukça doğrudan olsa da, kodunuzdaki karmaşıklık `GetSchema()` fonksiyonunuzu tanımlarken her satırı mantıksal olarak ayırmaya ve kategorize etmeye çalışmanızdan kaynaklanıyor. Örneğin, çıktının ardışık satırları aynı veritabanına veya tabloya ait olabilir de olmayabilir de; dolayısıyla satırları doğru `dbminer.Database` ve `dbminer.Table` örnekleriyle ilişkilendirmek biraz zorlayıcı bir işe dönüşüyor.

Liste 7-10, implementasyonu tanımlıyor.

```go
type MySCRMiner struct {
    Host string
    Db sql.DB
}

func New(host string) (*MySQLMiner, error) f
    m := MySOLMiner{Host: host}
    err := m.connect()
    if err != nil {
         return nil, err

    return &m, nil

func (m *MySOLMiner) connect() error {

    db, err := sql.Open(
         "mysql",
      0 fmt.Sprintfcroot:password@tcp(%5:3306)/information_schema", m.Host))
    if err 1= nil f
         log.Panicln(err)

   m.Db = *db
   return nil

func (m *MySOLMiner) GetSchema() (*dbminer.Schema, error) {
    var $ = new(dbminer.Schema)
```

```go
49 sql := 'SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME FROM columns
   WHERE TABLE_SCHEMA NOT IN
   ('mysql', 'information_schema', 'performance_schema', 'sys')
   ORDER BY TABLE_SCHEMA, TABLE_NAME
   schemarows, err := m.Db.Query(sql)
   if err != nil {
       return nil, err

   defer schemarows.Close()

   var prevschema, prevtable string
   var db dbminer.Database
   var table dbminer.Table
0 for schemarows.Next() {
        var currschema, currtable, currcol string
        if err := schemarows.Scan(&currschema, &currtable, &currcol); err != nil I
             return nil, err
```
