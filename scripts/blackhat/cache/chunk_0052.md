```go
records, err := parse("proxy.config")
if err != nil {
    panic(err)
}
dns.HandleFunc(".", func(w dns.ResponseWriter, req *dns.Msg) {
    if len(req.Question) == 0 {
        dns.HandleFailed(w, req)
        return
    }

    fqdn := req.Question[0].Name
    parts := strings.Split(fqdn, ".")
    if len(parts) >= 2 {
        fqdn = strings.Join(parts[len(parts)-2:], ".")
    }

    recordLock.RLock()
    match := records[fqdn]
    recordLock.RUnlock()
    if match == "" {
        dns.HandleFailed(w, req)
        return
    }

    resp, err := dns.Exchange(req, match)
    if err != nil {
        dns.HandleFailed(w, req)
        return
    }

    if err := w.WriteMsg(resp); err != nil {
        dns.HandleFailed(w, req)
        return
    }
})

go func() {
    sigs := make(chan os.Signal, 1)
    signal.Notify(sigs, syscall.SIGUSR1)

    for sig := range sigs {
        switch sig {
        case syscall.SIGUSR1:
            log.Println("SIGUSR1: reloading records")
            recordLock.Lock()
            parse("proxy.config")
            recordLock.Unlock()
        }
    }
}()

log.Fatal(dns.ListenAndServe(":53", "udp", nil))
```

Liste 5-7: Tamamlanmış proxy’niz (`/ch-5/dns_proxy/main.go`)

Program, eşzamanlı `goroutine`’lar tarafından kullanılmakta olabilecek bir `map`’i değiştireceği için, bu `map`’e erişimi denetlemek amacıyla bir mutex kullanmanız gerekir. Bir mutex, hassas kod bloklarının eşzamanlı yürütülmesini engeller; bu sayede erişimi kilitleyip (lock) açabilirsiniz (unlock). Bu durumda `RWMutex` kullanabilirsiniz; bu tür, herhangi bir `goroutine`’un diğerlerini kilitlemeden okuma yapmasına izin verir, ancak yazma işlemi gerçekleşirken diğerlerini kilitler. Alternatif olarak, kaynağınız üzerinde mutex kullanmadan `goroutine`’lar uygularsanız, iç içe geçme (interleaving) ortaya çıkar; bu da yarış durumlarına (race condition) veya daha kötü sonuçlara yol açabilir.

Handler içinde `map`’e erişmeden önce, eşleşecek değeri okumak için `RLock` çağrısı yaparsınız; okuma tamamlandıktan sonra `RUnlock` çağrısı yapılarak `map` bir sonraki `goroutine` için serbest bırakılır. Yeni bir `goroutine` içinde çalışan anonim bir fonksiyonda, bir sinyali dinleme sürecini başlatırsınız. Bu, `os.Signal` türünde bir kanal (channel) kullanılarak yapılır; bu kanal `signal.Notify()` çağrısına literal sinyal ile birlikte verilir ve `SIGUSR1` kanalı, keyfi amaçlar için ayrılmış bir sinyaldir. Sinyaller üzerinde dönen bir döngü içinde, alınan sinyal türünü belirlemek için bir `switch` ifadesi kullanırsınız. Yalnızca tek bir sinyali izleyecek şekilde yapılandırma yapmış olsanız da gelecekte bunu değiştirebilirsiniz; bu nedenle bu, uygun bir tasarım desenidir. Son olarak, çalışma zamanındaki yapılandırmayı yeniden yüklemeden önce `Lock()` çağrısı yapılarak, kayıt `map`’inden okuma yapmaya çalışan tüm `goroutine`’lar engellenir. Yürütmeyi sürdürmek için `Unlock()` kullanırsınız.

Bu programı, proxy’yi başlatarak ve mevcut bir teamserver içinde yeni bir dinleyici (listener) oluşturarak test edelim. `attacker3.com` alan adını kullanın. Proxy çalışırken, `proxy.config` dosyasını değiştirin ve alan adını dinleyicinize işaret eden yeni bir satır ekleyin. Sürecin yapılandırmasını yeniden yüklemesi için `kill` kullanarak sinyal gönderebilirsiniz, ancak önce `ps` ve `grep` kullanarak süreç kimliğini (PID) bulun.

```bash
$ ps -el | grep proxy
$ kill -10 PID
```

Proxy yeniden yüklenmelidir. Bunu, yeni bir aşamasız (stage-less) yürütülebilir dosya (executable) oluşturup çalıştırarak test edin. Proxy artık işlevsel ve üretim ortamına hazır olmalıdır.

1. Go’nun 1.9 ve daha yeni sürümleri, kodunuzu basitleştirmek için kullanabileceğiniz, eşzamanlı kullanıma güvenli `sync.Map` türünü içerir.

---

## Özet

Bu bölüm burada sona erse de, kodunuz için hâlâ bir dünya dolusu olasılık mevcut. Örneğin Cobalt Strike, HTTP ve DNS’i farklı işlemler için kullanarak hibrit bir şekilde çalışabilir. Bunu yapmak için proxy’nizi, A kayıtları için dinleyicinin IP’siyle yanıt verecek şekilde değiştirmeniz gerekir; ayrıca konteyner’larınıza ek portlar yönlendirmeniz gerekecektir. Bir sonraki bölümde, SMB ve NTLM’in karmaşık dünyasına dalacaksınız. Artık yola çıkma ve fethetme zamanı!

## SMB ve NTLM ile Etkileşim

Önceki bölümlerde ham TCP, HTTP ve DNS dahil olmak üzere ağ iletişiminde kullanılan çeşitli yaygın protokolleri incelediniz. Bu protokollerin her birinin saldırganlar için ilginç kullanım alanları vardır. Çok sayıda başka ağ protokolü de mevcut olmasına rağmen, ağ protokollerine ilişkin tartışmamızı, Windows sonrası sömürü (post-exploitation) sırasında tartışmasız en faydalı protokol olan Server Message Block (SMB) protokolünü inceleyerek tamamlayacağız.

SMB, bu kitapta göreceğiniz muhtemelen en karmaşık protokoldür. Çeşitli kullanım amaçları vardır, ancak SMB çoğunlukla ağ üzerinden dosya, yazıcı ve seri port gibi kaynakları paylaşmak için kullanılır. Saldırı odaklı okur için SMB, adlandırılmış borular (named pipes) aracılığıyla dağıtık ağ düğümleri arasında süreçler arası iletişime (interprocess communication) izin verir. Başka bir deyişle, uzak sistemlerde keyfi komutlar çalıştırabilirsiniz. Esasen bu, uzak komutları yerelmiş gibi çalıştıran Windows aracı PsExec’in çalışma şeklidir.

SMB’nin, özellikle NT LAN Manager (NTLM) kimlik doğrulamasını ele alış biçimi nedeniyle, başka pek çok ilginç kullanım alanı da vardır. NTLM, Windows ağlarında yoğun biçimde kullanılan bir meydan okuma/yanıt (challenge-response) güvenlik protokolüdür. Bu kullanım alanları arasında uzaktan parola tahmini, hash tabanlı kimlik doğrulama (ya da pass-the-hash), SMB relay ve NBNS/LLMNR sahtecilikleri (spoofing) sayılabilir. Bu saldırıların her birini ayrıntılı ele almak başlı başına bir kitap gerektirir.

Bu bölüme, Go ile SMB’yi nasıl uygulayacağınıza dair ayrıntılı bir açıklamayla başlayacağız. Ardından SMB paketini kullanarak uzaktan parola tahmini gerçekleştirecek, yalnızca bir parolanın hash’ini kullanarak başarılı şekilde kimlik doğrulamak için pass-the-hash tekniğini kullanacak ve bir parolanın NTLMv2 hash’ini kıracaksınız.
