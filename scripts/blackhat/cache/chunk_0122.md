Yük/Faydalı Yük (Payload)  
Orijinal değer 0, özgün PNG dosyasından okunan, kodlanmış yük verisidir; `Payload Decode` değeri 0 ise çözümlenmiş (decrypted) yükü ifade eder. Önceki örnek komut satırı çalıştırmanız ile buradaki çıktıyı karşılaştırırsanız, çözümlenmiş yükünüzün, en başta verdiğiniz orijinal açık metin (cleartext) değeriyle eşleştiğini fark edeceksiniz.

Ancak kodla ilgili bir sorun var. Program kodunun, yeni çözümlenmiş parçayı (chunk) sizin belirttiğiniz ofset konumuna enjekte ettiğini hatırlayın. Eğer zaten kodlanmış parça segmentini içeren bir dosyanız varsa ve ardından çözümlenmiş parça segmenti içeren yeni bir dosya yazmaya kalkarsanız, yeni çıktı dosyasında her iki parça da bulunur. Bunu Şekil 13-5’te görebilirsiniz.

```
00085250   39 fb bc 9c 92 47 d4 4d    00 00 06 lc 72 4e 44 6d
00085260   31 32 33 34 32 34 33 35    32 35 35 32 32 35 35 32      1234243525522552
80085278   35 32 32 34 35 32 33 35    35 35 32 35 if d8 22 4c      522452355525.."1
08085288   06 80 80 lc 72 4e 44 6d    56 Sd 43 Sc 57 46 48 52      ja.ullguy]C\WF@R
00085290   5d 45 5d 57 40 46 52 5d    45 Sa 57 46 46 55 Sc 45      TETRIMEZWFFU\E
006852a0   5d 58 40 46 77 28 e3 60    00 80 80.00 49 45 4e 44                 ...IEND
00085200   ae 42 60 82
```

Şekil 13-5: Çıktı dosyası hem çözümlenmiş parça segmentini hem de kodlanmış parça segmentini içeriyor

## Kodlanmış Parça Segmentinin Orijinal Konumu

Bu durumun neden gerçekleştiğini anlamak için, kodlanmış PNG dosyasının kodlanmış parça segmentine 0x85258 ofsetinde sahip olduğunu, Şekil 13-6’da gösterildiği gibi, tekrar hatırlayın.

```
.0085240 89 73 bb 47 2a dc cc 3e 90 81 81 el df 82 ff 07 1.s.G* >        I
.0085250 39 fb bc 9c 92 47 d4 4d             72 4e 44 6d 19....G.M„„LNDm
-808526e 56 sd 43 Sc 57 46 40 52 *F M+ 40 46 52 Sd IIINVE@RIENBER]
.0085278 45 5a 57 46 46 SS Sc 45 5d 50 48 46 77 28 e3 68 IEDIFFUMP@FwW1
08885280 BO 00 80 Be 49 45 4e 44 ae 42 60 82
```

Şekil 13-6: Kodlanmış parça segmentini içeren çıktı dosyası

Sorun, çözümlenmiş veri 0x85258 ofsetine yazıldığında ortaya çıkar. Çözümlenmiş veri, kodlanmış verinin bulunduğu aynı konuma yazıldığında, bizim uygulamamız kodlanmış veriyi silmez; sadece dosyanın geri kalan baytlarını sağa kaydırır; bu sırada kodlanmış parça segmenti de dâhildir. Bu durum, daha önce Şekil 13-5’te gösterildiği gibi gerçekleşir. Bu, yük çıkarmayı zorlaştırabilir veya açık metin yükü ağ cihazlarına veya güvenlik yazılımlarına ifşa etmek gibi istenmeyen sonuçlar üretebilir.

Neyse ki bu sorun çözülmesi oldukça kolay bir sorun. Daha önceki `WriteData()` fonksiyonumuza bakalım. Bu kez, problemi çözmek için bu fonksiyonu değiştirebilirsiniz (Liste 13-22).

```go
//WriteData writes new data to offset
func WriteData(r *bytes.Reader, c *models.CmdLineOpts, b []byte) {
    offset, err := strconv.ParseInt(c.Offset, 10, 64)
    if err != nil {
        log.Fatal(err)

    w, err := os.OpenFile(c.Output, os.O_RDWRIos.O_CREATE, 0777)
    if err 1= nil f
        log.Fatal("Fatal: Problem writing to the output file!")

    r.Seek(0, 0)

    var buff = make(Mbyte, offset)
    r.Read(buff)
    w.Write(buff)
    w.Write(b)
 0 if c.Decode {
      0 r.Seek(int64(len(b)), 1)
    1
    _, err = io.Copy(w,
    if err == nil {
         fmt.Printf("Success: %s created\n", c.Output)
```

Liste 13-22: Yinelenen tali (ancillary) chunk tiplerini önlemek için `WriteData()` güncellenmesi (`/ch-13/imgInject/utils/writer.go`)

Düzeltmeyi `c.Decode` koşullu mantığı 0 ile ekliyorsunuz. XOR işlemi bayt-bayt bir dönüşüm üretir. Dolayısıyla kodlanmış ve çözümlenmiş parça segmentleri uzunluk olarak birebir aynıdır. Ayrıca, çözümlenmiş parça segmenti yazıldığı anda, `bytes.Reader` hâlâ özgün kodlanmış görüntü dosyasının geri kalanını içeriyor olacaktır. Bu nedenle, `bytes.Reader` üzerinde çözümlenmiş parça segmentinin uzunluğu kadar bir sağa bayt kaydırma işlemi 0 gerçekleştirebilir, `bytes.Reader`’ı kodlanmış parça segmentinin ötesine ilerletebilir ve kalan baytları yeni görüntü dosyanıza yazabilirsiniz 0.

Voila! Şekil 13-7’de görebileceğiniz gibi, hex editör sorunu çözdüğünüzü doğruluyor. Yinelenen tali chunk tipleri artık yok.

```
.0085240   09 73 bb 47 2a dc cc 3e      90 81 81 el df 82 ff 07         >
:6085256   39 fb bc 9c 92 47 d4 4d      BA BA       72 4e 44 6d 19....G.MayiaiNDmi
;8085260   31 32 33 34 32 34 33 35      32 35 35 32 32 35 35 32 112342435255225521
.8085278   35 32 32 34 35 32 33 35      35 35 32 35 if d8 22 4c 1522452355525—N1
;8085280   Kt 00 00 Be 49 45 4e 44      ae 42 68 82
```

Şekil 13-7: Yinelenen tali veriler olmadan çıktı dosyası

Kodlanmış veri artık mevcut değil. Ek olarak, dosyalar üzerinde `ls -la` çalıştırmak, dosya baytları değişmiş olsa bile, aynı dosya uzunluklarını üretmelidir.

## Özet

Bu bölümde, PNG görüntü dosyası biçimini, her birinin kendi amacı ve uygulanabilirliği olan tekrarlı bayt parça segmentleri dizisi olarak nasıl tanımlayacağınızı öğrendiniz. Ardından, ikili dosyayı okuma ve içinde gezinme yöntemlerini öğrendiniz. Sonra bayt verisi oluşturup bunu bir görüntü dosyasına yazdınız. Son olarak, yükünüzü gizlemek (obfuscate) için XOR kodlaması kullandınız.

Bu bölüm görüntü dosyalarına odaklandı ve steganografi teknikleriyle yapabileceklerinizin yalnızca yüzeyine değindi. Ancak burada öğrendiklerinizi kullanarak diğer ikili dosya türlerini de keşfedebilmelisiniz.

## Ek Alıştırmalar

Bu kitaptaki diğer birçok bölümde olduğu gibi, bu bölüm de en fazla değeri siz gerçekten kod yazıp deney yaptığınızda sağlayacaktır. Bu nedenle, burada ele alınan fikirleri genişletmek için birkaç meydan okumayla sonlandırmak istiyoruz:
