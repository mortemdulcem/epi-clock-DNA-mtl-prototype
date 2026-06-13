### Parolaları Hash Geçme (Pass-the-Hash) Tekniğiyle Yeniden Kullanma

Pass-the-hash tekniği, bir saldırganın, parolanın düz metin (cleartext) haline sahip olmasa bile, parolanın NTLM hash'ini kullanarak SMB kimlik doğrulaması yapmasını sağlar. Bu bölüm, kavramı adım adım açıklayıp bir uygulamasını gösterir.

Pass-the-hash, tipik bir Active Directory etki alanı ele geçirme sürecine yönelik bir kestirme yoldur. Bu saldırı türünde saldırganlar önce ağda bir başlangıç noktası elde eder, ayrıcalıklarını yükseltir ve ağ içinde yatay hareket ederek nihai hedeflerine ulaşmak için ihtiyaç duydukları erişim seviyelerini elde edene kadar ilerler. Active Directory etki alanı ele geçirme saldırıları, parola tahmini gibi bir yöntem yerine bir zafiyet sömürüsü üzerinden gerçekleştiği varsayılırsa, genellikle aşağıdaki yol haritasını izler:

- Saldırgan, bir zafiyeti sömürür ve ağda bir başlangıç noktası elde eder.
- Saldırgan, ele geçirilmiş sistem üzerinde ayrıcalıklarını yükseltir.
- Saldırgan, LSASS üzerinden hash'lenmiş ya da düz metin kimlik bilgilerini elde eder.
- Saldırgan, çevrimdışı kırma (offline cracking) yoluyla yerel yönetici parolasını kurtarmaya çalışır.
- Saldırgan, yönetici kimlik bilgilerini kullanarak diğer makinelerde kimlik doğrulaması yapmayı dener ve parolanın yeniden kullanımını (reuse) arar.
- Saldırgan, etki alanı yöneticisi (domain administrator) ya da diğer hedef ele geçirilene kadar bu adımları tekrar eder.

NTLMSSP kimlik doğrulamasında ise, 3. veya 4. adımda düz metin parolayı kurtarmayı başaramasanız bile, 5. adımda SMB kimlik doğrulaması için parolanın NTLM hash'ini kullanmaya devam edebilirsiniz; başka bir deyişle, hash'i geçirirsiniz (passing the hash).

Pass-the-hash tekniği, hash hesaplamasını, meydan okuma/yanıt (challenge-response) belirteci hesaplamasından ayırdığı için çalışır. Bunun neden böyle olduğuna bakmak için, NTLMSSP belirtiminde tanımlanan ve kimlik doğrulamada kullanılan kriptografik ve güvenlik mekanizmalarıyla ilgili aşağıdaki iki fonksiyonu inceleyelim:

- `NTOWFv2` Kullanıcı adı, etki alanı ve parola değerlerini kullanarak bir MD5 HMAC üreten bir kriptografik fonksiyon. NTLM hash değerini üretir.
- `ComputeResponse` NTLM hash'i, mesajın istemci ve sunucu meydan okumaları, zaman damgası ve hedef sunucu adıyla birlikte kullanarak, kimlik doğrulama için gönderilebilecek bir GSS-API güvenlik belirteci üreten bir fonksiyon.

Bu fonksiyonların uygulamasını Liste 6-13'te görebilirsiniz.

```go
func Ntowfv2(pass, user, domain string) []byte f
    h := hmac.New(md5.New, Ntowfvi(pass))
    h.Write(encoder.ToUnicode(strings.ToUpper(user) + domain))
    return h.Sum(nil)

func ComputeResponseNTLMv2(nthash1), lmhash, clientChallenge, serverChallenge, timestamp,
                        serverName []byte) []byte

      temp := []byte{1, 1}
      temp = append(temp, 0, 0, 0, 0, 0, 0)
      temp = append(temp, timestamp...)
      temp = append(temp, clientChallenge...)
      temp = append(temp, 0, 0, 0, 0)
      temp = append(temp, serverName...)
      temp = append(temp, 0, 0, 0, 0)

      h := hmac.New(md5.New, nthash)
      h.Write(append(serverChallenge, temp...))
      ntproof := h.Sum(nil)
      return append(ntproof, temp...)
```

**Liste 6-13: NTLM hash'leriyle çalışma (`/ch-6/smbintlmsspicrypto.go`)**

`ComputeResponseNTLMv2` fonksiyonuna giriş olarak NTLM hash'i (`nthash`) verilir, yani hash değeri, güvenlik belirteci oluşturma mantığından bağımsız olarak önceden oluşturulmuştur. Bu da, LSASS içinde saklananlar da dahil olmak üzere, herhangi bir yerde saklanan hash'lerin önceden hesaplanmış (precalculated) sayıldığı anlamına gelir; çünkü etki alanı, kullanıcı veya parolayı giriş olarak vermeniz gerekmez. Kimlik doğrulama süreci şu şekildedir:

- Etki alanı, kullanıcı ve parola değerlerini kullanarak kullanıcının hash'ini hesaplayın.
- Hash'i, SMB üzerinde NTLMSSP için kimlik doğrulama belirteçlerini hesaplamak üzere giriş olarak kullanın.

Elinizde zaten bir hash bulunduğuna göre, 1. adımı tamamlamış durumdasınız. Hash'i geçirmek (pass the hash) için, bu bölümün başlarında tanımladığınız SMB kimlik doğrulama dizisini başlatırsınız. Ancak, hash'i asla hesaplamazsınız; bunun yerine size verilen değeri doğrudan hash'in kendisi olarak kullanırsınız.

Liste 6-14, belirli bir kullanıcı olarak bir makine listesine kimlik doğrulaması yapmayı denemek için bir parola hash'i kullanan bir pass-the-hash aracını göstermektedir.

```go
func main() {
    if len(os.Args) 1= 5 {
         log.Fatalln("Usage: main <target/hosts> <user> <domain> <hash>")

    buf, err := ioutil.ReadFile(os.Args[i])
    if err != nil {
        log.Fatalln(err)

    options := smb.Options{
        User:   os Args [2],
        Domain: os.Args[3],
        Hashe: os.Args[4],
        Port:   445,

    targets := bytes.Split(buf, Hbyte{ 1 \n'})
    for _, target := range targets° {
        options.Host = string(target)

         session, err := smb.NewSession(options, false)
         if err != nil {
             fmt.Printf("[-] Login failed [%s]: %s\n", options.Host, err)
             continue

         defer session. Close()
         if session.IsAuthenticated {
              fmt.Printf("[+] Login successful [%s]\n", options.Host)

    I.
```

**Liste 6-14: Kimlik doğrulama testi için hash geçme (`/ch-6/password-reuse/main.go`)**

Bu kod, parola tahmini örneğine oldukça benzer görünmelidir. Tek önemli fark, `smb.Options` struct'ının `Password` alanını değil `Hash` alanını ayarlıyor olmanız ve hedef kullanıcılar yerine hedef makinelerin bir listesi üzerinde yineleme yapmanızdır. `smb.NewSession()` fonksiyonunun içindeki mantık, `options` struct'ı içinde `Hash` alanı doldurulmuşsa bu değeri kullanacaktır.

### NTLM Parolalarını Kurtarma

Bazı durumlarda, yalnızca parola hash'ine sahip olmak genel saldırı zinciriniz (attack chain) için yeterli olmayacaktır. Örneğin, Uzak Masaüstü (Remote Desktop), Outlook Web Access ve diğer birçok hizmet, ya hash tabanlı kimlik doğrulamayı desteklemediğinden ya da varsayılan yapılandırma bu olmadığı için hash tabanlı kimlik doğrulamasına izin vermez. Saldırı zinciriniz bu hizmetlerden birine erişim gerektiriyorsa, düz metin bir parolaya ihtiyacınız olacaktır. Aşağıdaki bölümlerde, hash'lerin nasıl hesaplandığını ve temel bir parola kırıcıyı nasıl yazacağınızı inceleyeceksiniz.
