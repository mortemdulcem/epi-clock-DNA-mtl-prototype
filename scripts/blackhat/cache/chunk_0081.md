Çünkü `msfvenom` çıktısı virgülle ayrılmış olduğundan, bayt listesi verisetlerini beceriksizce eklemeye gerek kalmadan satırlar boyunca düzgünce kaydırılabilir. Gereken tek değişiklik, listedeki son elemandan sonra tek bir virgül eklemektir. Bu çıktı formatı Go kodunuza kolayca entegre edilebilir ve hoş bir biçimde formatlanabilir.

## Ham Dönüşüm (Raw Transform)

Ham bir dönüşüm, yükü/faydalı yükü (payload) ham ikili (binary) formatta üretir. Verinin kendisi, terminal penceresinde görüntülendiğinde, aşağıdakine benzeyen basılamaz karakterler üretmesi muhtemeldir:

```
DaIDDINDPODR
D8DuDIDAiuDXDX$DfDY ID:INDDOODD
```

Bu veriyi, onu farklı bir formatta üretmediğiniz sürece, kodunuzda kullanamazsınız. O halde neden ham ikili veriyi tartışıyoruz diye sorabilirsiniz. Çünkü, bir araç tarafından üretilmiş bir yük (payload), bir ikili dosyanın içeriği veya kripto anahtarları gibi ham ikili veriye rastlamak oldukça yaygındır. İkili veriyi tanımayı ve Go kodunuza dahil etmeyi bilmek değerli olacaktır.

Linux’ta `xxd` yardımcı programını `-i` komut satırı anahtarıyla kullanarak, ham ikili verinizi önceki bölümdeki `num` formatına kolayca dönüştürebilirsiniz. Örnek bir `msfvenom` komutu, `msfvenom` tarafından üretilen ham ikili çıktıyı `xxd` komutuna `pipe` ederek şu şekilde görünebilir:

```bash
$ msfvenom -p [payload] [options] -f raw | xxd
```

Önceki bölümde gösterildiği gibi, sonucu doğrudan bir byte `slice`ına atayabilirsiniz.

## Base64 Kodlama

`msfvenom` saf bir Base64 kodlayıcı içermese de, shellcode dahil ikili veriyi Base64 formatında görmek oldukça yaygındır. Base64 kodlama, verinizin uzunluğunu artırır, ancak çirkin veya kullanılamaz ham ikili veriden kaçınmanızı sağlar. Bu format, örneğin `num` formatına göre, kodunuzda çalışmak için daha kolaydır ve HTTP gibi protokoller üzerinden veri iletimini basitleştirebilir. Bu nedenle, Go içinde kullanımı üzerinde durmaya değerdir.

İkili verinin Base64 ile kodlanmış bir gösterimini üretmenin en kolay yolu, Linux’taki `base64` yardımcı programını kullanmaktır. Bu program, veriyi `stdin` üzerinden ya da bir dosyadan alarak kodlamanıza veya kodunu çözmenize izin verir. `msfvenom` ile ham ikili veri üretebilir ve ardından sonucu aşağıdaki komutla kodlayabilirsiniz:

```bash
$ msfvenom -p [payload] [options] -f raw | base64
```

C çıktınıza benzer şekilde, ortaya çıkan yük (payload) satır sonları içerir; bunu, kodunuzda bir string olarak kullanmadan önce ele almanız gerekir. Linux’ta `tr` yardımcı programını kullanarak tüm satır sonlarını kaldırıp çıktıyı temizleyebilirsiniz:

```bash
$ msfvenom -p [payload] [options] -f raw | base64 | tr -d "\n"
```

Kodlanmış yük artık tek bir, kesintisiz string olarak var olacaktır. Go kodunuzda, string’i çözüp ham yükü bir byte `slice`ı olarak elde edebilirsiniz. Bu işi yapmak için `encoding/base64` paketini kullanırsınız:

```go
payload, err := base64.StdEncoding.DecodeString("/OiCAAAAYIn1McBkilAwi...WFuZAA=")
```

Artık tüm çirkinlik olmadan ham ikili veriyle çalışabilecek duruma geleceksiniz.

## Assembly Üzerine Bir Not

Shellcode ve düşük seviye programlama tartışması, assembly’den en azından kısaca bahsedilmeden tamamlanmış sayılmaz. Ne yazık ki shellcode bestecileri ve assembly ustaları için, Go’nun assembly ile entegrasyonu sınırlıdır. C’nin aksine, Go satır içi (inline) assembly desteklemez. Assembly’yi Go kodunuza entegre etmek isterseniz, bunu bir dereceye kadar yapabilirsiniz. Go tarafında bir fonksiyon prototipi tanımlayıp assembly talimatlarını ayrı bir dosyada tutmanız gerekir. Ardından `go build` çalıştırarak nihai çalıştırılabilir dosyanızı derleyip (build), bağlarsınız (link). Bu çok zor görünmeyebilir, ancak asıl sorun assembly dilinin kendisidir.

Go, Plan 9 işletim sistemi temel alınarak oluşturulmuş bir assembly varyasyonunu destekler. Bu sistem Bell Labs tarafından oluşturulmuş ve 20. yüzyılın sonlarında kullanılmıştır. Kullanılabilir talimatlar ve opcode’lar dahil olmak üzere, assembly söz dizimi neredeyse yok denecek kadar azdır. Bu da saf Plan 9 assembly yazmayı son derece zor, hatta neredeyse imkânsız bir görev haline getirir.

## Özet

Assembly kullanımının sınırlı olmasına rağmen, Go’nun standart paketleri zafiyet avcıları ve exploit geliştiricileri için son derece elverişli büyük bir işlevsellik sunar. Bu bölümde fuzzing, exploit’leri Go’ya taşıma (port etme) ve ikili veri ile shellcode işleme konu edildi. Ek bir öğrenme egzersizi olarak, `https://www.exploit-db.com/` adresindeki exploit veritabanını incelemenizi ve mevcut bir exploiti Go’ya port etmeyi denemenizi öneriyoruz. Kaynak dile olan aşinalık seviyenize bağlı olarak bu görev göz korkutucu görünebilir, ancak veri manipülasyonu, ağ iletişimi ve düşük seviye sistem etkileşimini anlamak için mükemmel bir fırsat olabilir.

Bir sonraki bölümde, exploitation faaliyetlerinden bir adım uzaklaşıp genişletilebilir (extendable) araç setleri üretmeye odaklanacağız.

---

# 10  
GO PLUGIN’LERİ VE GENİŞLETİLEBİLİR ARAÇLAR
