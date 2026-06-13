```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata
/core-properties "
                    xmlns:dc="http://purl.org/dc/elements/1.1/ "
                    xmlns:dcterms="http://purl.org/dc/terms/"
                    xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance "›
    <dc:creator>Dan Kottmann</dc:creator>0
    <cp:lastModified8y>DanKottmann</cp:lastModifiedBy>19
    <dcterms:created xsi:type="dcterms:W3CDTF">2016-12-06T18:24:42Zadcterms:created>
    <dcterms:modified xsi:type="dcterms:W3CDTF">2016-12-06T18:25:32Z</dcterms:modified>
</cp:coreProperties>
```

`creator` ve `lastModifiedBy` öğeleri birincil ilgi alanımızdır. Bu alanlar, sosyal mühendislik veya parola tahmin kampanyasında kullanabileceğiniz çalışan isimlerini veya kullanıcı adlarını içerir.

`app.xml` dosyası, Open XML belgesini oluşturmak için kullanılan uygulama türü ve sürümü hakkında ayrıntılar içerir. Yapısı şöyledir:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties "
             xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes ">
    <Application>Microsoft ExceldApplication>0
    <DocSecurity>0</DocSecurity>
    <ScaleCrop>false</ScaleCrop>
    <HeadingPairs>
        <vt:vector size="2" baseType="variant"›
             <vt:variant>
                 <vt:lpstr>Worksheets</vt:lpstr>
             </vt:variant>
             <vt:variant>
                 <vt:14>1</vt:14>
             </vt:variant>
        </vt:vector>
    </HeadingPairs>
    <TitlesOfParts>
        <vt:vector size="1" baseType="lpste>
             <vt:lpstr>Sheeti</vt:lpstr>
        </vt:vector>
    </TitlesOfParts>
     <Company>ACME</Company>4I
     <LinksUpToDate>false</LinksUpToDate>
     <SharedDoc>false</SharedDoc>
     <HyperlinksChanged>false</HyperlinksChanged>
     <AppVersion>15.0300</AppVersion>0
</Properties>
```

## 10    Chapter3

Buradaki öğelerden sadece birkaç tanesiyle öncelikli olarak ilgilenirsiniz: `Application`, `Company` ve `AppVersion`. Sürüm alanı, Office 2013, Office 2016 gibi Office sürüm adlarıyla doğrudan, bariz bir ilişkiye sahip değildir; ancak bu alan ile daha okunabilir, yaygın olarak bilinen alternatifler arasında mantıksal bir eşleme mevcuttur. Geliştireceğiniz kod bu eşlemeyi koruyacaktır.

## metadata Package'ini Tanımlama

Liste 3-20’de, bu XML veri kümelerine karşılık gelen Go tiplerini, `metadata` adlı yeni bir package içinde ve `openxml.go` adlı bir dosyada tanımlayın—ayrıştırmak istediğiniz her XML dosyası için bir tip. Ardından, `AppVersion` alanına karşılık gelen tanınabilir Office sürümünü belirlemek için bir veri eşleme (map) ve yardımcı (convenience) fonksiyon ekleyin.

```go
type OfficeCoreProperty struct {
     XMLName       xml . Name ' xml : " coreProperties" '
     Creator       string 'xml:"creator"'
     LastModifiedBy string 'xml:"lastModifiedBy"'

type OfficeAppProperty struct {
    XMLName     xml.Name 'xml:"Properties"'
    Application string   'xml:"Application"
    Company string 'xml:"Company"'
    Version string 'xml:"AppVersion"'

var OfficeVersions0 = map[string]string{
    "16": "2016",
    "15": "2013",
    "14": "2010",
    "12": "2007",
    "11": "2003",

func (a *OfficeAppProperty) GetMajorVersion00 string {
    tokens := strings.5plit(a.Version, ".")O

     if len(tokens) < 2 {
          return "Unknown"

     v, ok := OfficeVersions0 [tokens[0]]
     if lok {
          return "Unknown"

     return v
11
```

**Liste 3-20:** Open XML tip tanımı ve sürüm eşlemesi (`/ch-3/ging-metadata/metadata/openxml.go`)

`OfficeCoreProperty` ve `OfficeAppProperty` tiplerini tanımladıktan sonra, büyük sürüm numaraları ile tanınabilir çıkış yılları arasındaki ilişkiyi tutan `OfficeVersions` adlı bir map tanımlayın. Bu map’i kullanmak için `OfficeAppProperty` tipi üzerinde `GetMajorVersion()` metodunu tanımlayın. Bu metod, XML verisinin `AppVersion` değerini bölerek ana sürüm numarası kimliğini elde eder ve sonrasında bu değeri `OfficeVersions` map’i ile birlikte kullanarak çıkış yılını bulur.

## Veriyi Struct'lara Eşleme

Artık ilgilendiğiniz XML verisiyle çalışmak ve onu incelemek için gerekli mantığı ve tipleri oluşturduğunuza göre, uygun dosyaları okuyup içeriklerini struct’lara atayan kodu yazabilirsiniz. Bunu yapmak için, Liste 3-21’de gösterildiği gibi `NewProperties()` ve `process()` fonksiyonlarını tanımlayın.

```go
func NewProperties(r *zip.Reader) (*OfficeCoreProperty, *OfficeAppProperty, error) {0
    var coreProps OfficeCoreProperty
    var appProps OfficeAppProperty

     for _, f := range r.File {19
         switch f.Name {41)
         case "docProps/core.xml":
              if err := process(f, &coreProps)0; err 1= nil {
                   return nil, nil, err

         case "docProps/app.xml":
             if err := process(f, &appProps)1); err 1= nil {
                  return nil, nil, err

         default:
             continue

     return &coreProps, &appProps, nil

func process(f *zip.File, prop interface{}) error {0
    rc, err := f.Open()
    if err 1= nil {
         return err

     defer rc.Close()

     if err := Oxml.NewOecoder(rc).Decode(&prop); err != nil {
          return err

     return nil
```

**Liste 3-21:** Open XML arşivlerini ve gömülü XML belgelerini işleme (`/ch-3/ging-metadata/metadata/openxml.go`)

`NewProperties()` fonksiyonu bir `*zip.Reader` kabul eder; bu, ZIP arşivleri için bir `io.Reader`’ı temsil eder. `zip.Reader` örneğini kullanarak arşivdeki tüm dosyalar üzerinde döngü kurarsınız ve dosya adlarını kontrol edersiniz. Bir dosya adı, iki özellik dosyasından birisiyle eşleşirse, dosyayı ve doldurmak istediğiniz rastgele yapı tipini (`OfficeCoreProperty` veya `OfficeAppProperty`) parametre olarak geçirerek `process()` fonksiyonunu çağırırsınız.

`process()` fonksiyonu iki parametre kabul eder: bir `*zip.File` ve bir `interface{}`. Geliştirdiğiniz Metasploit aracına benzer şekilde, bu kod da dosya içeriğinin herhangi bir veri tipine atanabilmesini sağlamak için genel (generic) `interface{}` tipini kabul eder. Bu yaklaşım, `process()` fonksiyonu içinde tipe özgü hiçbir şey bulunmadığından, kodun yeniden kullanılabilirliğini artırır. Fonksiyonun içinde, kod dosyanın içeriğini okur ve XML verisini struct içine unmarshaler (ayrıştırarak) yükler.
