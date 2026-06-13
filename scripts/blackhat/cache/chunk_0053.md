## SMB Paket’i

Bu kitabın yazıldığı tarihte, Go içinde resmi bir SMB paket’i bulunmamaktadır; ancak bizim oluşturduğumuz bir paket mevcut ve kitap dostu sürümünü `https://github.con/blackhat-go/bhg/blob/master/ch-6/smb` adresinde bulabilirsiniz. Bu bölümde bu paket’in her detayını göstermeyeceğiz, fakat yine de SMB spesifikasyonunu yorumlamanın temellerini öğrenerek, önceki bölümlerde olduğu gibi tamamen uyumlu paket’leri yeniden kullanmak yerine, “SMB konuşmak” için gerekli ikili (binary) iletişimi nasıl oluşturacağınızı göreceksiniz. Ayrıca, çalışma zamanında arayüz (interface) veri tiplerini incelemek için yansıma (reflection) adı verilen tekniği nasıl kullanacağınızı ve gelecekteki mesaj yapıları ve veri tipleri için ölçeklenebilirliği korurken, karmaşık ve keyfi verileri `marshal` ve `unmarshal` etmek amacıyla keyfi Go struct alan etiketleri (field tags) tanımlamayı öğreneceksiniz.

Oluşturduğumuz SMB kütüphanesi yalnızca temel istemci taraflı iletişime izin verse de, kod tabanı oldukça kapsamlıdır. SMB paket’inden, SMB kimlik doğrulaması gibi iletişimlerin ve görevlerin nasıl çalıştığını tam olarak anlayabilmeniz için ilgili örnekler göreceksiniz.

## SMB’yi Anlamak

SMB, HTTP gibi, ağ düğümlerinin birbirleriyle iletişim kurmasına izin veren bir uygulama katmanı (application-layer) protokolüdür. Ancak ASCII ile okunabilir metin kullanan HTTP 1.1’den farklı olarak SMB; sabit ve değişken uzunluklu, konumsal ve little-endian alanların birleşimini kullanan ikili (binary) bir protokoldür. SMB’nin lehçe (dialect) olarak da adlandırılan birkaç sürümü vardır: 2.0, 2.1, 3.0, 3.0.2 ve 3.1.1. Her lehçe, seleflerinden daha iyi performans gösterir. Lehçeden lehçeye işleme biçimi ve gereksinimler farklılık gösterdiği için, istemci ve sunucunun önceden hangi lehçeyi kullanacakları üzerinde anlaşmaları gerekir. Bunu, ilk mesaj alışverişi sırasında yaparlar.

Genel olarak Windows sistemleri birden fazla lehçeyi destekler ve hem istemcinin hem sunucunun desteklediği en güncel lehçeyi seçer. Microsoft, hangi Windows sürümlerinin, müzakere sürecinde hangi SMB lehçesini seçtiğini gösteren Tablo 6-1’i sağlamıştır. (Grafikte gösterilmeyen Windows 10 ve WS 2016, SMB sürüm 3.1.1’i müzakere eder.)

**Tablo 6-1: Windows Sürümleri Tarafından Müzakere Edilen SMB Lehçeleri**

| İşletim sistemi | Windows 8.1 WS 2012 R2 | Windows 8 WS 2012 | Windows 7 WS 2008 R2 | Windows Vista WS 2008 | Önceki sürümler |
|-----------------|------------------------|--------------------|----------------------|-----------------------|-----------------|
| Windows 8.1 WS 2012 R2 | SMB 3.02 | SMB 3.0 |                | SMB 2.0 | SMB 1.0 |
| Windows 8 WS 2012      | SMB 3.0  | SMB 3.0 | SMB 2.1        | SMB 2.0 | SMB 1.0 |
| Windows 7 WS 2008 R2   |          | SMB 2.1 | SMB 2.1        | SMB 2.0 | SMB 1.0 |
| Windows Vista WS 2008  | SMB 2.0  | SMB 2.0 | SMB 2.0        | SMB 2.0 | SMB 1.0 |
| Önceki sürümler        | SMB 1.0  | SMB 1.0 | SMB 1.0        | SMB 1.0 | SMB 1.0 |

Bu bölümde, çoğu modern Windows sürümü tarafından desteklendiği için SMB 2.1 lehçesini kullanacaksınız.

## SMB Güvenlik Jetonlarını Anlamak

SMB mesajları, ağ üzerinde kullanıcıları ve makineleri kimlik doğrulamak için kullanılan güvenlik jetonları içerir. SMB lehçesinin seçilmesi sürecine benzer şekilde, kimlik doğrulama mekanizmasının seçimi de, istemci ve sunucuların karşılıklı olarak desteklenen bir kimlik doğrulama türü üzerinde anlaşmalarını sağlayan bir dizi Session Setup mesajı aracılığıyla gerçekleşir. Active Directory etki alanları, kullanıcıları ağ üzerinde kimlik doğrulamak için NTLM parola karmalarını, meydan okuma-cevap (challenge-response) jetonlarıyla birlikte kullanan, ikili ve konumsal bir protokol olan NTLM Security Support Provider’ı (NTLMSSP) yaygın olarak kullanır. Meydan okuma-cevap jetonları, bir soruya verilen kriptografik cevap gibidir; yalnızca doğru parolayı bilen bir varlık soruya doğru cevap verebilir. Bu bölüm yalnızca NTLMSSP’ye odaklansa da, Kerberos başka bir yaygın kimlik doğrulama mekanizmasıdır.

Kimlik doğrulama mekanizmasının SMB spesifikasyonundan ayrılması, SMB’nin alan ve kurumsal güvenlik gereksinimlerine ve istemci-sunucu desteğine bağlı olarak farklı ortamlarda farklı kimlik doğrulama yöntemleri kullanmasına izin verir. Ancak kimlik doğrulamanın SMB spesifikasyonundan ayrılması, Go’da bir uygulama (implementation) oluşturmayı zorlaştırır; çünkü kimlik doğrulama jetonları Abstract Syntax Notation One (ASN.1) ile kodlanmıştır. Bu bölüm için ASN.1 hakkında çok fazla şey bilmenize gerek yok; yalnızca, genel SMB için kullanacağınız konumsal ikili kodlamadan farklı bir ikili kodlama formatı olduğunu bilmeniz yeterli. Bu karışık kodlama, karmaşıklık ekler.

NTLMSSP’yi anlamak, tek bir mesaj içindeki bitişik alanların farklı biçimlerde kodlanıp çözümlenebileceği (decode) olasılığını hesaba katarak, mesaj alanlarını seçici olarak `marshal` ve `unmarshal` edecek kadar akıllı bir SMB uygulaması oluşturmak için kritiktir. Go’da ikili (binary) ve ASN.1 kodlama için kullanabileceğiniz standart paket’ler vardır; ancak Go’nun ASN.1 paket’i genel amaçlı kullanım için oluşturulmamıştır; dolayısıyla birkaç ince noktayı hesaba katmanız gerekir.

## Bir SMB Oturumu Kurma

İstemci ve sunucu, bir SMB 2.1 oturumunu başarıyla kurmak ve NTLMSSP lehçesini seçmek için aşağıdaki süreci gerçekleştirir:
