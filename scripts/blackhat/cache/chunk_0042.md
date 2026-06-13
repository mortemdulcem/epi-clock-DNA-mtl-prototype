Bu, `payload1.exe` ve `payload2.exe` adlı iki çıktı dosyası üretir. Dikkat ederseniz, çıktı dosya adları dışında bu ikisi arasındaki tek fark `HttpHostHeader` değerleridir. Bu sayede ortaya çıkan yük/faydalı yük (payload), HTTP isteklerini belirli bir `Host` başlık değeriyle gönderir. Ayrıca dikkat edilmesi gereken bir diğer nokta, `LHOST` ve `LPORT` değerlerinin Meterpreter dinleyicilerine (listener) değil, ters vekil sunucunuza (reverse proxy) ait bilgilerle eşleşiyor olmasıdır. Ortaya çıkan çalıştırılabilir dosyaları bir Windows sistemine veya sanal makineye aktarın. Dosyaları çalıştırdığınızda, biri 10080 portuna bağlanmış dinleyicide, diğeri 20080 portuna bağlanmış dinleyicide olmak üzere iki yeni oturumun kurulduğunu görmelisiniz.

Bu oturumlar aşağıdakine benzer görünmelidir:

```
[*] http://10.0.1.20:10080 handling request from 10.0.1.20; (UUID: hff7podk) Redirecting stageless
connection from /px5_2g1431v34_birNgRHgL4A33A9w3i9FXG3Ne2-3UdLhAer8-Qt6Q010w
PTkzww3NEptWTOan2rLORT42eDdhYykyPYW8dq3B0Mi2TaAEB with UA 'Mozilla/5.0 (Windows NT 6.1;
Trident/7.0;
rv:11.0) like Gecko'
[*] http://10.0.1.20:10080 handling request from 10.0.1.20; (UUID: hff7podk) Attaching
orphaned/stageless session...
[*] Meterpreter session 1 opened (10.0.1.20:10080 -> 10.0.1.20:60226) at 2020-07-03 16:13:34 -0500
```

`tcpdump` veya Wireshark kullanarak 10080 ya da 20080 portuna giden ağ trafiğini incelerseniz, Metasploit dinleyicisiyle iletişim kuran tek sunucunun ters vekil sunucunuz (reverse proxy) olduğunu görmelisiniz. Ayrıca `Host` başlığının 10080 portundaki dinleyici için `attacker1.com`, 20080 portundaki dinleyici için `attacker2.com` olarak uygun şekilde ayarlandığını da doğrulayabilirsiniz.

Hepsi bu kadar. Bunu başardınız. Şimdi işi biraz daha ileri taşıyın. Bir alıştırma olarak, kodu basamaklı (staged) bir yük/faydalı yük (payload) kullanacak şekilde güncellemenizi öneriyoruz. Bu muhtemelen ek zorluklarla birlikte gelecektir; çünkü her iki aşamanın da proxy üzerinden düzgün biçimde yönlendirildiğinden emin olmanız gerekecektir. Ayrıca, bunu düz metin HTTP yerine HTTPS kullanarak uygulamaya çalışın. Bu, trafiği işe yarar ve kötü niyetli şekillerde proxy’lemek konusundaki anlayışınızı ve etkinliğinizi daha da artıracaktır.

## Özet

HTTP yolculuğunuzu tamamladınız; son iki bölümde hem istemci hem sunucu uygulamalarını incelediniz. Bir sonraki bölümde, güvenlik uygulayıcıları için en az HTTP kadar faydalı bir protokol olan DNS’e odaklanacaksınız. Hatta DNS kullanarak bu HTTP çoklama (multiplexing) örneğini neredeyse birebir yeniden oluşturacaksınız.

---

# DNS’İ SÖMÜRME

Domain Name System (DNS), internet alan adlarını bulur ve bunları IP adreslerine çevirir. Kurumlar genellikle bu protokolün kısıtlı ağlardan dışarıya (egress) çıkmasına izin verdiği ve kullanımı yeterince izlenmediği için, saldırganların elinde etkili bir silah olabilir. Biraz bilgiyle donanmış uyanık saldırganlar, bu sorunlardan saldırı zincirinin neredeyse her adımında yararlanabilir: keşif (reconnaissance), komuta ve kontrol (command and control, C2) ve hatta veri sızdırma (data exfiltration) dahil. Bu bölümde, Go ve üçüncü taraf paketler kullanarak bu kabiliyetlerden bazılarını yerine getiren kendi araçlarınızı nasıl yazacağınızı öğreneceksiniz.

İlk olarak, çözümlenebilecek birçok DNS kayıt türünü ortaya çıkarmak için ana makine adlarını ve IP adreslerini çözeceksiniz. Daha sonra, önceki bölümlerde gösterilen kalıpları kullanarak yüksek düzeyde eşzamanlı (massively concurrent) bir alt alan adı tahmin (subdomain guessing) aracı inşa edeceksiniz. Son olarak, kendi DNS sunucunuzu ve proxy’nizi nasıl yazacağınızı öğrenecek ve kısıtlayıcı bir ağdan dışarıya bir C2 kanalı kurmak için DNS tünelleme (DNS tunneling) kullanacaksınız!

## DNS İstemcileri Yazma

Daha karmaşık programları incelemeden önce, istemci işlemleri için mevcut bazı seçeneklere aşina olalım. Go’nun yerleşik `net` paketi harika işlevsellik sunar ve kayıt türlerinin çoğunu, hatta muhtemelen tamamını destekler. Yerleşik paketin avantajı, arayüzünün (API) oldukça basit ve anlaşılır olmasıdır. Örneğin, `LookupAddr(addr string)` belirli bir IP adresi için bir ana makine adı listesi döndürür. Go’nun yerleşik paketini kullanmanın dezavantajı ise hedef sunucuyu belirleyememenizdir; bunun yerine paket, işletim sisteminizde yapılandırılmış çözümleyiciyi (resolver) kullanır. Bir diğer dezavantaj da sonuçlar üzerinde derinlemesine inceleme yapamamanızdır.

Bu kısıtlamayı aşmak için, Miek Gieben tarafından yazılmış harika bir üçüncü taraf paket olan Go DNS paketini kullanacaksınız. Bu, yüksek modülerliği, iyi yazılmış ve iyi test edilmiş olması nedeniyle tercih ettiğimiz DNS paketidir. Paketi kurmak için aşağıdakini kullanın:

```bash
$ go get github.com/miekg/dns
```

Paket kurulduktan sonra, sıradaki kod örneklerini takip etmeye hazırsınız. Başlangıç olarak, ana makine adlarını IP adreslerine çözmek için A kayıt sorguları yapacaksınız.

### A Kayıtlarını Çekme

Tam nitelikli alan adları (fully qualified domain name, FQDN) için bir sorgu yaparak başlayalım. FQDN, bir ana makinenin DNS hiyerarşisindeki tam konumunu belirtir. Daha sonra, bu FQDN’yi bir IP adresine çözmeye çalışacağız; bunun için A kaydı denen bir DNS kayıt türünü kullanacağız. A kayıtları, bir alan adını bir IP adresine işaret etmek için kullanılır. Liste 5-1, örnek bir sorgu göstermektedir. (Kök `/` konumundaki tüm kod listeleri, sağlanan GitHub deposu `https://github.com/blackhat-go/bhg` altında yer alır.)

```go
package main

import (

    "github.com/miekg/dns"

func main() {
    var msg dns.Msg
    fqdn := dns.Fqdn("stacktitan.com")
    msg.5eWuestion(fqdn, dns.TypeA)
    dns.Exchange(8msg, "8.8.8.8:53")
```

**Liste 5-1: Bir A kaydı çekme (`/ch-5/get_a/main.go`)**
