## DNS Sunucusu ve Vekil (Proxy) Oluşturma

DNS tünelleme (DNS tunneling), veri sızdırma (data exfiltration) tekniği olarak, çıkış (egress) kontrolleri kısıtlayıcı olan ağlardan bir C2 kanalı kurmak için harika bir yöntem olabilir. Yetkili (authoritative) bir DNS sunucusu kullanıldığında, bir saldırgan, kendi altyapısına doğrudan bağlantı kurmak zorunda kalmadan, bir kuruluşun kendi DNS sunucuları üzerinden ve oradan da internet dışına trafik yönlendirebilir. Yavaş olsa da, savunması zordur. DNS tünelleme yapan birkaç açık kaynak ve tescilli yük/faydalı yük (payload) bulunmaktadır; bunlardan biri de Cobalt Strike'ın Beacon'ıdır. Bu bölümde kendi DNS sunucunuzu ve vekil sunucunuzu (proxy) yazacak ve Cobalt Strike kullanarak DNS tünelleme C2 payload'larını nasıl çoklayacağınızı (multiplex) öğreneceksiniz.

## Cobalt Strike'ı Yapılandırma

Daha önce Cobalt Strike kullandıysanız, varsayılan olarak `teamserver`'ın 53 numaralı portu dinlediğini fark etmiş olabilirsiniz. Bu sebeple ve dokümantasyondaki öneri gereği, bir sistem üzerinde yalnızca tek bir sunucunun çalıştırılması, yani bire bir (one-to-one) oranının korunması gerekir. Bu durum, orta ve büyük ölçekli ekipler için sorunlu hale gelebilir. Örneğin, 20 ayrı kuruluş üzerinde saldırı/sızma faaliyeti yürüten 20 ekibiniz varsa, `teamserver` çalıştırmaya elverişli 20 sistem ayağa kaldırmak zor olabilir. Bu problem yalnızca Cobalt Strike ve DNS'e özgü değildir; Metasploit Meterpreter ve Empire gibi HTTP payload'ları da dahil olmak üzere diğer protokoller için de geçerlidir. Tamamen benzersiz portlarda dinleyiciler (listener) oluşturabilirsiniz ancak TCP 80 ve 443 gibi yaygın portlar üzerinden çıkış trafiği (egress) sağlama olasılığı daha yüksektir. Dolayısıyla soru şudur: Siz ve diğer ekipler tek bir portu nasıl paylaşabilir ve trafiği birden fazla dinleyiciye nasıl yönlendirebilirsiniz? Elbette cevap bir proxy'dir. Şimdi laboratuvara dönelim.

**NOT**   Gerçek angajmanlarda, `teamserver`'ınızın konumunu gizlemek için birden fazla düzeyde aldatma (subterfuge), soyutlama (abstraction) ve iletme (forwarding) kullanmak isteyebilirsiniz. Bu, çeşitli barındırma (hosting) sağlayıcıları üzerinde çalışan küçük yardımcı sunucular üzerinden UDP ve TCP iletme (forwarding) kullanılarak yapılabilir. Birincil `teamserver` ve proxy de ayrı sistemlerde çalıştırılabilir; `teamserver` kümesi (cluster), bol RAM ve CPU gücüne sahip büyük bir sistem üzerinde tutulabilir.

Şimdi Cobalt Strike `teamserver`'ının iki örneğini (instance) iki Docker konteynerinde çalıştıralım. Bu, sunucunun 53 numaralı portu dinlemesine izin verir ve her bir `teamserver`'ın fiilen kendi sistemi ve dolayısıyla kendi IP yığınına (IP stack) sahip olmasını sağlar. Docker'ın yerleşik ağ (networking) mekanizmasını kullanarak konteynerden host'a UDP portları eşleyeceksiniz. Başlamadan önce, https://trialcobaltstrike.com/ adresinden Cobalt Strike'ın deneme sürümünü indirin. Deneme kaydı talimatlarını izledikten sonra, indirme dizininizde taze bir `tarball` dosyanız olmalıdır. Artık `teamserver`'ları başlatmaya hazırsınız.

Birinci konteyneri başlatmak için terminal penceresinde aşağıdakini çalıştırın:

```bash
$ docker run --rm -it -p 2020:53 -p 50051:50050 -v <full path to \
cobalt strike download>:/data java /bin/bash
```

Bu komut birkaç şey yapar. Önce Docker'a, konteyner sonlandıktan sonra onu kaldırmasını (`--rm`) ve konteyner başlatıldıktan sonra onunla etkileşimde bulunmak istediğinizi (`-it`) söylersiniz. Ardından, host sisteminizdeki 2020 numaralı portu konteyner içindeki 53 numaralı porta, 50051 numaralı portu da 50050 numaralı porta eşlersiniz (`-p`). Sonra, Cobalt Strike `tarball` dosyasını içeren dizini (`-v`) konteyner üzerindeki `data` dizinine eşlersiniz. İstediğiniz herhangi bir dizini belirtebilirsiniz; Docker sizin için memnuniyetle oluşturacaktır. Son olarak, kullanmak istediğiniz imajı (bu durumda `java`) ve başlangıçta çalıştırılmasını istediğiniz komutu (`/bin/bash`) belirtirsiniz. Bu, çalışır durumdaki Docker konteynerinde bir bash kabuğu ile kalmanızı sağlar.

Docker konteynerinin içindeyken, aşağıdaki komutları çalıştırarak `teamserver`'ı başlatın:

```bash
$ cd /root
$ tar -zxvf /data/cobaltstrike-trial.tgz
$ cd cobaltstrike
$ ./teamserver <IP address of host> <some password>
```

Verdiğiniz IP adresi, konteynerin IP adresi değil, gerçek sanal makinenizin (VM) IP adresi olmalıdır.

Sonra, Ubuntu host üzerinde yeni bir terminal penceresi açın ve Cobalt Strike `tarball` dosyasını içeren dizine geçin. Java'yı kurmak ve Cobalt Strike istemcisini (client) başlatmak için aşağıdaki komutları çalıştırın:

```bash
$ sudo add-apt-repository ppa:webupd8team/java
$ sudo apt update
$ sudo apt install oracle-java8-installer
$ tar -zxvf cobaltstrike-trial.tgz
$ cd cobaltstrike
$ ./cobaltstrike
```

Cobalt Strike'ın GUI arayüzü başlamalıdır. Deneme mesajını geçtikten sonra, `teamserver` portunu 50051 olarak değiştirin ve kullanıcı adınızı ve parolanızı uygun şekilde ayarlayın.

Docker içinde tamamen çalışan bir sunucuya başarıyla bağlandınız! Şimdi, aynı işlemi tekrar ederek ikinci bir sunucu başlatalım. Yeni bir `teamserver` başlatmak için önceki adımları izleyin. Bu kez farklı portları eşleyeceksiniz. Portları bire bir artırmak işinizi görecek ve mantıklı olacaktır. Yeni bir terminal penceresinde, yeni bir konteyner başlatmak ve 2021 ile 50052 portlarını dinlemek için aşağıdaki komutu çalıştırın:

```bash
$ docker run --rm -it -p 2021:53 -p 50052:50050 -v <full path to cobalt strike \
download>:/data java /bin/bash
```

Cobalt Strike istemcisinden, **Cobalt Strike → New Connection**'ı seçerek yeni bir bağlantı oluşturun, portu 50052 olarak değiştirin ve **Connect**'i seçin. Bağlandığınızda, konsolun alt kısmında sunucular arasında geçiş yapmak için kullanabileceğiniz iki sekme görmelisiniz.

Artık iki `teamserver`'a da başarıyla bağlandığınıza göre, iki DNS dinleyici (listener) başlatmalısınız. Bir dinleyici oluşturmak için menüden **Configure Listeners**'ı seçin; simgesi bir kulaklık çiftine benzer. Buradayken, alt menüden **Add**'i seçerek **New Listener** penceresini açın. Aşağıdaki bilgileri girin:

```text
Name: DNS 1
Payload: windows/beacon_dns/reverse_dns_txt
Host: <IP address of host>
Port: 0
```
