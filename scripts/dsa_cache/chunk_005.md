Fred Brooks tasarımın doğası üzerine, tasarımcı ve araştırmacı olarak 50 yıllık
deneyimini yansıtan bir dizi düşünceli deneme kaleme almıştır:
F. P. Brooks, Jr., *The Design of Design: Essays from a Computer Scientist*.
Addison-Wesley, 2010.

Tasarım ve diğer geliştirme etkinlikleri için belgelenmiş bir sürece sahip olmanın
yararlılığı, D. Parnas ve P. Clements, “A Rational Design Process: How and Why
to Fake It”, *IEEE Transactions on Software Engineering*, SE-12, 2, Şubat 1986
makalesinde tartışılmaktadır.

Burada kullanılan yazılım mimarisi tanımı, mimarinin önemine ilişkin argümanlar
ve mimarın rolüyle ilgili görüşlerin tümü şu kaynaktan alınmıştır:
L. Bass, P. Clements ve R. Kazman, *Software Architecture in Practice*, 3. baskı,
Addison-Wesley, 2012.

Mimari geliştirme yaşam döngüsündeki farklı etkinlikleri ele alan birkaç kitap
bulunmaktadır; bunlara G. Fairbanks, *Just Enough Software Architecture: A Risk
Driven Approach*, Marshall & Brainerd, 2010 ve 7. Bölüm’de tasarım yaklaşımları
tanımlanan diğer kitaplar dahildir.

ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) ilk sürümü için erken
bir referans, F. Bachmann, L. Bass, G. Chastek, P. Donohoe ve F. Peruzzi,
*The Architecture Based Design Method*, CMU/SEI-2000-TR-001 çalışmasında
bulunabilir. ADD’nin ikinci sürümü, R. Wojcik, F. Bachmann, L. Bass,
P. Clements, P. Merson, R. Nord ve W. Wood, *Attribute-Driven Design (ADD),
Version 2.0*, CMU/SEI-2006-TR-023 belgesinde tanımlanmıştır. Bu kitapta ADD 2.5
olarak adlandırdığımız ADD sürümü ise H. Cervantes, P. Velasco-Elizondo ve
R. Kazman, “A Principled Way of Using Frameworks in Architectural Design”,
*IEEE Software*, s. 46–53, Mart/Nisan 2013 makalesinde yayımlanmıştır.

# 2
Mimari Tasarım

Şimdi mimari tasarım sürecine dalıyoruz: ne olduğu, neden önemli olduğu,
nasıl çalıştığı (soyut bir düzeyde) ve hangi temel kavramlar ile etkinlikleri
içerdiği. Önce mimari sürücüleri (architectural driver) tartışacağız: Tasarım
kararlarını “yönlendiren” çeşitli etkenler; bunların bazıları gereksinimler olarak
belgelenmiştir, ancak çoğu değildir. Buna ek olarak, tasarım sürecinizin bir
parçası olarak seçeceğiniz, birleştireceğiniz, somutlayacağınız, analiz edeceğiniz
ve belgeleyeceğiniz ana yapı taşları olan tasarım kavramlarına genel bir bakış
sunuyoruz.

## 2.1
Genel Olarak Tasarım

Tasarım hem bir fiildir hem de bir isimdir. Tasarım bir süreçtir, bir etkinliktir,
dolayısıyla bir fiildir. Süreç, bir tasarımın — arzu edilen nihai durumun bir
betiminin — ortaya çıkmasıyla sonuçlanır. Böylece tasarım sürecinin çıktısı,
sonunda gerçekleştireceğiniz şey, yani ad (isim), yapıt (artifact) olur. Tasarlamak,
hedeflere ulaşmak ve gereksinimler ile kısıtları karşılamak için kararlar almak
anlamına gelir. Tasarım sürecinin çıktıları, doğrudan bu hedeflerin, gereksinimlerin
ve kısıtların bir yansımasıdır. Örneğin evler hakkında düşünün. Neden Çin’deki
geleneksel evler, İsviçre ya da Cezayir’dekilerden farklı görünür? Neden bir
“yurt” (göçebe çadırı) bir “yurt” gibi görünür de, bir igloo, dağ evi (chalet) veya
“longhouse”dan (uzun ev) farklıdır?

Bu tarz evlerin mimarileri, yüzyıllar boyunca, kendilerine özgü hedef, gereksinim
ve kısıt kümelerini yansıtacak biçimde evrimleşmiştir. Çin’deki evler; simetrik
iç avlular, havalandırmayı artırmak için gökyüzü boşlukları, güneş toplamak ve
soğuk kuzey rüzgârlarından korunmak için güneye bakan avlular vb. özelliklere
sahiptir. A-çatılı evlerin, zemine kadar inen dik eğimli çatıları vardır; bu da
en az boyama gereksinimi ve yoğun kar yüklerine karşı koruma sağlar (kar
kolayca yere kayar). İglolar buzdan inşa edilir; bu da buzun bolluğunu, diğer
yapı malzemelerinin göreli kıtlığını ve zaman kısıtını (küçük bir igloo bir saatte
inşa edilebilir) yansıtır.

Her durumda, tasarım süreci bir dizi çözüm yaklaşımının seçilmesini ve
uygulanmasını içerir. İglo tasarımları bile değişkenlik gösterebilir. Bazıları
küçük ve geçici seyahat barınağı olarak tasarlanmıştır. Diğerleri, birden fazla
yapının birbirine bağlandığı, tüm toplulukların bir araya gelmesi için tasarlanan
büyük yapılardır. Bazıları süssüz, basit kar kulübeleridir. Diğerleri kürklerle
kaplanmıştır; buzdan “pencereleri” ve hayvan derisinden yapılmış kapıları vardır.

Tasarım süreci, her durumda, tasarımcının karşısındaki çeşitli “kuvvetler”
arasında bir denge kurar. Bazı tasarımların uygulanması ciddi beceri gerektirir
(örneğin, kar bloklarını kendi kendini taşıyan bir kubbe oluşturacak şekilde
oymak ve istiflemek gibi). Diğerleri görece az beceri gerektirir — bir siper (lean-to),
neredeyse herkesin dallar ve kabuk kullanarak inşa edebileceği bir yapıdır. Ancak
bu yapıların sergilediği nitelikler de önemli ölçüde farklılık gösterebilir. Siperler
doğal koşullara karşı çok az koruma sağlar ve kolayca yıkılırken, bir igloo
Arktik fırtınalara dayanabilir ve çatısında duran bir kişinin ağırlığını taşıyabilir.

Tasarım “zor” mudur? Hem evet hem hayır. Yenilikçi tasarım zordur. Geleneksel
bir bisikletin nasıl tasarlanacağı oldukça açıktır; ancak Segway’in tasarımı yeni
bir çığır açmıştır. Neyse ki, tasarımların çoğu yenilikçi değildir; çünkü çoğu
zaman gereksinimlerimiz yenilikçi değildir. Çoğu insan, kendisini güvenilir şekilde
bir yerden başka bir yere götürecek bir bisiklet ister. Bu durum her alanda
geçerlidir. Örneğin evleri düşünün. Phoenix’te yaşayan çoğu insan, kolay ve
ekonomik bir biçimde serin tutulabilecek bir ev isterken, Edmonton’da yaşayan
çoğu insanın öncelikli kaygısı, sıcak tutulabilecek bir evdir. Buna karşılık,
Japonya ve Los Angeles’ta yaşayan insanlar, depremlere dayanabilecek binalar
hususunda kaygılıdır.

Mimar olarak sizin için iyi haber, bu hedeflere güvenilir biçimde ulaşmak
üzere yeniden kullanılabilecek ve birleştirilebilecek, kanıtlanmış pek çok tasarım
ve tasarım parçası (bina blokları) olmasıdır; biz bunlara tasarım kavramları
(design concept) diyoruz. Tasarımınız gerçekten yenilikçi ise — eğer bir sonraki
Sydney Opera Binası’nı tasarlıyorsanız — tasarım süreci muhtemelen “zor”
olacaktır. Örneğin Sydney Opera Binası, ilk bütçe tahmininin 14 katına mal
olmuş ve on yıl gecikmeli olarak teslim edilmiştir. Yazılım mimarilerinin tasarımı
için de durum böyledir.

## 2.2
Yazılım Mimarisi Tasarımı
