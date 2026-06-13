Önce Ubuntu sanal makinesini (VM) oluşturun. Bunu yapmak için 16.04.1 LTS sürümünü kullanacağız. Özel bir ayarlama yapmanıza gerek yok, ancak VM’i en az 4 gigabayt bellek ve iki CPU ile yapılandırmalısınız. Elinizde mevcut bir VM veya ana makine varsa onu da kullanabilirsiniz. İşletim sistemi kurulduktan sonra, bir Go geliştirme ortamı kurmanız gerekecek (Bkz. Bölüm 1).

Ubuntu VM’yi oluşturduktan sonra, Docker adlı bir sanallaştırma konteyner aracını kurun. Bu bölümün proxy kısmında, birden fazla Cobalt Strike örneğini çalıştırmak için Docker kullanacaksınız. Docker’ı kurmak için terminal penceresinde aşağıdaki komutları çalıştırın:

```bash
$ sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv \
                               --keyserver hkp://ha.pool.sks-keyservers.net:80 \
                               --recv-keys 58118689F3A912897020ADBF26221622C62600
$ echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee \
/etc/apt/sources.list.d/docker.list
$ sudo apt-get update
$ sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
$ sudo apt-get install docker-engine
$ sudo service docker start
$ sudo usermod -aG docker USERNAME
```

Kurulumdan sonra sistemden çıkış yapıp tekrar giriş yapın. Sonraki adımda, Docker’ın kurulu olduğunu aşağıdaki komutu çalıştırarak doğrulayın:

```bash
$ docker version
Client:
 Version:     1.13.1
 API version: 1.26

Go version:   go1.7.5
Git commit:   082cba3
Built:        Wed Feb 5 06:50:14 2020
OS/Arch:      linux/amd64
```

Docker kurulduktan sonra, bir Java imajı indirmek için aşağıdaki komutu kullanın. Bu komut temel Docker Java imajını indirir ama herhangi bir konteyner oluşturmaz. Bunu, birazdan Cobalt Strike derlemelerinizi hazırlamak için yapıyorsunuz.

```bash
$ docker pull Java
```

Son olarak, `dnsmasq`’ın çalışmadığından emin olmanız gerekiyor; çünkü 53 numaralı portu dinler. Aksi halde, kendi DNS sunucularınız çalışamayacaktır; çünkü onların da aynı portu kullanması beklenir. Çalışıyorsa, işlemi kimliğine göre öldürün:

```bash
$ ps -ef | grep dnsmasq
nobody    3386 2020 0 12:08
$ sudo kill 3386
```

Şimdi bir Windows VM oluşturun. Yine, mevcut bir makineyi kullanabiliyorsanız kullanabilirsiniz. Özel bir ayara ihtiyacınız yok; asgari ayarlar yeterli olacaktır. Sistem çalışır hale geldiğinde, DNS sunucusunu Ubuntu sisteminin IP adresi olacak şekilde ayarlayın.

Laboratuvar kurulumunuzu test etmek ve DNS sunucuları yazmaya giriş yapmak için, yalnızca A kayıtları döndüren basit bir sunucu yazarak başlayın. Ubuntu sisteminizdeki `GOPATH` içinde `github.com/blackhat-go/bhg/ch-5/a_server` adlı yeni bir dizin ve `main.go` kodunuzu tutacak bir dosya oluşturun. Liste 5-5, basit bir DNS sunucusu oluşturmak için gereken kodun tamamını gösterir.

```go
package main

import (
    "log"
    "net"

    "github.com/miekg/dns"
)

func main() {
    dns.HandleFunc(".", func(w dns.ResponseWriter, req *dns.Msg) {
        var resp dns.Msg
        resp.SetReply(req)
        for _, q := range req.Question {
            a := dns.A{
                Hdr: dns.RR_Header{
                    Name:   q.Name,
                    Rrtype: dns.TypeA,
                    Class:  dns.ClassINET,
                    Ttl:    0,
                },
                A: net.ParseIP("127.0.0.1").To4(),
            }

            resp.Answer = append(resp.Answer, &a)

        }
        w.WriteMsg(&resp)
    })
    log.Fatal(dns.ListenAndServe(":53", "udp", nil))
}
```

**Liste 5-5: Bir DNS sunucusu yazmak (`/ch-5/a_server/main.go`)**

Sunucu kodu, `HandleFunc()` çağrısıyla başlar; `net/http` paketine oldukça benzer görünür. Fonksiyonun ilk argümanı, eşleştirilmek üzere bir sorgu desenidir. Bu deseni, DNS sunucularına hangi isteklerin verilen fonksiyon tarafından ele alınacağını belirtmek için kullanırsınız. Bir nokta (`"."`) kullanarak, ikinci argümanda verdiğiniz fonksiyonun tüm istekleri ele alacağını sunucuya söylüyorsunuz.

`HandleFunc()`’a verilen bir sonraki argüman, handler (işleyici) için mantığı içeren bir fonksiyondur. Bu fonksiyon iki argüman alır: bir `ResponseWriter` ve isteğin kendisi. Handler içinde, yeni bir mesaj oluşturarak ve yanıtı ayarlayarak başlarsınız. Sonraki adımda, her bir soru için bir yanıt oluşturursunuz; bunun için `RR` arayüzünü (interface) uygulayan bir A kaydı kullanırsınız. Bu bölüm, aradığınız yanıt türüne göre değişiklik gösterecektir. A kaydına işaretçi, `append()` kullanılarak yanıtın `Answer` alanına eklenir. Yanıt tamamlandığında, bu mesajı `w.WriteMsg()` kullanarak çağıran istemciye yazabilirsiniz. Son olarak, sunucuyu başlatmak için `ListenAndServe()` çağrılır. Bu kod, tüm istekleri `127.0.0.1` IP adresine çözümler.

Sunucu derlenip başlatıldıktan sonra, `dig` kullanarak test edebilirsiniz. Sorguladığınız hostname’in `127.0.0.1` adresine çözümlendiğini doğrulayın. Bu, tasarlandığı gibi çalıştığını gösterir.

```bash
$ dig @localhost facebook.com

; <<>> DIG 9.10.3-P4-Ubuntu <<>> @localhost facebook.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 33594
;; flags: qr rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;facebook.com.                        IN        A

;; ANSWER SECTION:
facebook.com.               0         IN        A        127.0.0.1

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
;; WHEN: Sat Dec 19 13:13:45 MST 2020
;; MSG SIZE rcvd: 58
```

Sunucunun, ayrıcalıklı bir port olan 53 numaralı portu dinlediği için `sudo` veya kök (root) hesapla başlatılması gerektiğini unutmayın. Sunucu başlamazsa, `dnsmasq`’ı öldürmeniz gerekebilir.
