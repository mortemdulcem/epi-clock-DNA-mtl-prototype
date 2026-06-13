```go
                     for _, payload := range payloads {
                          client := new(http.Client)
                          body := Hbyte(fmt.Sprintf("username4s&password=p", payload))
                          req, err := http.NewRequest(
                               "POST",
                               "http://10.0.1.20:8080/WebApplication/login.j5p ",
                              bytes.NewReader(body),

                         if err != nil {
                             log.Fatalf(111 Unable to generate request: %s\n", err)

                         req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
                         resp, err := client.Do(req)
                         if err != nil {
                             log.Fatalf(10 Unable to process response: %s\n", err)
```

194 chapter9

```go
         body, err = ioutil.ReadAll(resp.Body)
         if err != nil {
             log.Fatalf("[1] Unable to read response body: %s\n", err)

         resp.Body.Close()

         for idx, re := range errRegexes {
              if re.MatchString(string(body)) {
                   fmt.Printf(
                      "[+] SQL Error found ('%s') for payload: %s\n",
                      sqlErrors[idx],
                      payload,

                  break
```

Liste 9-2: Bir SQL enjeksiyon fuzz aracı (`/ch-9/http_fuzz/main.go`)

Kod, denemek istediğiniz yüklerin (payloads) bir `slice`ını tanımlayarak başlar ❶. Bu, daha sonra `username` istek parametresine değer olarak sağlayacağınız fuzzing listenizdir. Benzer şekilde, bir SQL hata mesajı içindeki anahtar sözcükleri temsil eden bir `slice` tanımlarsınız ❷. Bunlar, HTTP yanıt gövdesinde arayacağınız değerler olacaktır. Bu değerlerden herhangi birinin varlığı, bir SQL hata mesajının bulunduğuna dair güçlü bir göstergedir. Her iki listeyi de genişletebilirsiniz, ancak bu örnek için yeterli veri kümeleridir.

Sonraki adımda, biraz ön işleme çalışması yaparsınız. Aramak istediğiniz her bir hata anahtar sözcüğü için birer düzenli ifade (regular expression) oluşturup derlersiniz. Bu işi ana HTTP mantığınızın dışında yaparsınız; böylece her payload için bu düzenli ifadeleri yeniden oluşturup derlemek zorunda kalmazsınız. Kuşkusuz bu yalnızca küçük bir optimizasyondur, ancak yine de iyi bir uygulamadır. Daha sonra kullanmak üzere, derlenmiş bu düzenli ifadeleri ayrı bir `slice` içinde saklayacaksınız.

Sonra fuzz aracının çekirdek (core) mantığı gelir. Payloadların her birini ❸ döngüye sokar, her birini `username` değerinin mevcut payload olduğu uygun bir HTTP istek gövdesi oluşturmak için kullanırsınız ❹. Elde ettiğiniz değeri, giriş formunuzu hedefleyen bir HTTP POST isteği oluşturmak için kullanırsınız ❺. Ardından `Content-Type` başlığını ayarlar ve `client.Do(req)` çağrısı yaparak isteği gönderirsiniz.

İsteği, bir `client` ve ayrı bir `request` oluşturup ardından `client.Do()` çağırarak uzun form sürecini kullanarak gönderdiğinize dikkat edin. Aynı davranışı daha özlü biçimde elde etmek için Go'nun `http.PostForm()` fonksiyonunu da kullanabilirdiniz. Ancak, daha ayrıntılı (verbose) teknik, HTTP başlık değerleri üzerinde size daha ince ayarlı (granüler) kontrol sağlar. Bu örnekte yalnızca `Content-Type` başlığını ayarlıyor olsanız da, HTTP istekleri yaparken ek başlık değerleri (örneğin `User-Agent`, `Cookie` ve diğerleri) ayarlamak yaygındır. Bunu `http.PostForm()` ile yapamazsınız; dolayısıyla uzun yolu kullanmak, gelecekte gerekli olabilecek HTTP başlıklarını eklemenizi kolaylaştıracaktır; özellikle de bir gün başlıkların kendisini fuzz etmekle ilgilenirseniz.

Sonraki adımda, `ioutil.ReadAll()` ❻ kullanarak HTTP yanıt gövdesini okursunuz. Gövdeye sahip olduğunuzda, tüm önceden derlenmiş düzenli ifadeleri ❼ döngüye sokar ve yanıt gövdesini SQL hata anahtar sözcüklerinizin ❽ varlığı açısından test edersiniz. Bir eşleşme bulursanız, muhtemelen bir SQL enjeksiyon hata mesajına sahipsinizdir. Program, payload ve hataya ilişkin ayrıntıları ekrana yazar ve döngünün bir sonraki iterasyonuna geçer.

Kodunuzu çalıştırarak, zafiyetli bir giriş formunda SQL enjeksiyon kusurunu başarıyla tespit ettiğini doğrulayın. `username` değerine tek bir tırnak işareti verdiğinizde, aşağıda gösterildiği gibi `SQL` hata göstergesini alırsınız:

```bash
$ go run main.go
[+] SQL Error found ('SQL') for payload: '
```

Aşağıdaki alıştırmaları denemenizi öneririz; böylece kodu daha iyi anlarsınız, HTTP iletişiminin inceliklerini kavrarsınız ve SQL enjeksiyon tespit etme yeteneğinizi geliştirirsiniz:

- Koda zaman tabanlı (time-based) SQL enjeksiyon testleri ekleyin. Bunu yapmak için, arka uç sorgusu çalıştığında zaman gecikmesi oluşturan çeşitli payloadlar göndermeniz gerekecek. Round-trip süresini ölçmeli ve SQL enjeksiyonun mevcut olup olmadığını çıkarmak için bunu temel (baseline) bir istekle karşılaştırmalısınız.
- Kodu, boolean tabanlı kör (blind) SQL enjeksiyonu test etmek için güncelleyin. Bunun için farklı göstergeler kullanabilirsiniz; ancak basit bir yöntem, HTTP yanıt kodunu temel bir yanıtla karşılaştırmaktır. Temel yanıt kodundan bir sapma, özellikle 500 (internal server error) yanıt kodu almak, SQL enjeksiyonunu işaret ediyor olabilir.
- Go'nun `net.http` paketine güvenmek yerine, ham bir TCP bağlantısını `net` paketiyle açmayı (dial) deneyin. `net` paketini kullanırken, mesaj gövdesinin uzunluğunu temsil eden `Content-Length` HTTP başlığının farkında olmanız gerekir. Gövde uzunluğu değişebileceği için her istek için bu uzunluğu doğru hesaplamanız gerekir. Geçersiz bir uzunluk değeri kullanırsanız, sunucu büyük olasılıkla isteği reddedecektir.

Bir sonraki bölümde, Python veya C gibi diğer dillerden Go'ya exploit taşımayı (port etmeyi) nasıl yapacağınızı göstereceğiz.
