Yazarlar, görüş ve yorumlarıyla cömert katkılarda bulunan hakemlerimiz Marty
Barrett, Roger Champagne, Siva Muthu, Robert Nord, Vishal Prabhu, Andriy
Shapochka, David Sisk, Perla Velasco-Elizondo ve Olaf Zimmermann’a teşekkür etmek ister. Ayrıca 5. Bölüm’e katkılarından dolayı Serge Haziyev ve Olha
Hrytsay’e de teşekkür ederiz. Bunlara ek olarak, aralarında Serge, Olha ve
Andriy’nin de bulunduğu Softserve’deki birçok mimara, çalışmalarımıza verdikleri güçlü ve sürekli destek için teşekkür borçluyuz.

Humberto, Quarksoft’taki direktörlere ve mimar grubuna teşekkür etmek
ister; ADD’nin (Attribute-Driven Design, nitelik temelli tasarım) revizyonuna dair birçok fikir ve bu kitapta sunulan örnek olay çalışmalarından biri, bu yöntemi söz konusu şirket bünyesinde uygulamaya koymaktan doğmuştur. Birlikte
çalışma ve fikir alışverişinde bulunma fırsatı yakaladığım diğer şirketlerdeki
mimar ve geliştiricilere de teşekkür ederim; onlardan çok şey öğrendim. Ayrıca,
yıllardır ACE Educators Workshop’ta beni ve diğer akademisyenleri ağırlayan
Software Engineering Institute’teki insanlara teşekkür etmek isterim. Üniversitem
Universidad Autónoma Metropolitana Iztapalapa’ya da, çalışmalarımı her zaman
desteklediği için teşekkür etmek istiyorum. Bu mimari yolculukta yıllardır bana
eşlik eden meslektaşlarım Perla Velasco-Elizondo ve Luis Castro’ya da teşekkürler. Yıllar önce bana uygulayıcı bir mimar olma fırsatını veren Alonso Leal’a
teşekkür ederim. Bu kitabı yazarken paha biçilmez olduğu kanıtlanan birçok
beceriyi bana öğreten Richard S. Hall’a teşekkür ederim. Son olarak, birlikte
çalışmanın ve fikir alışverişinde bulunmanın her zaman bir zevk olduğu, çok iyi
bir insan ve meslektaş olan eş yazarım Rick’e teşekkür etmek isterim.

Rick, Software Engineering Institute’ten James Ivers’a ve onun araştırma
grubuna teşekkür etmek ister. Özellikle, özenli ve ufuk açıcı inceleme yorumları
ve önerileri için Rod Nord’a teşekkür etmek isterim. Ayrıca, yıllardır birlikte
çalıştığım işbirlikçim ve akıl hocam Len Bass’e teşekkür etmek isterim; yazılım
mimarisi yolculuğuna yıllar önce beni başlatan kişidir. Len olmasaydı, bugün
nerede olacağımı kim bilebilir. Buna ek olarak, araştırmalarımı yıllarca kararlılıkla destekleyen ve bana pek çok harika “başarılı olma fırsatı” sunan Linda
Northrop’a teşekkür etmek isterim. Son olarak, her zaman enerjik, olumlu ve
birlikte çalışması gerçek bir zevk olan eş yazarım Humberto’ya teşekkür etmek
isterim.

xvii

Bu sayfa bilerek boş bırakılmıştır.

# 1. Giriş

Bu bölümde yazılım mimarisi konusuna bir giriş sunuyoruz. Kısaca mimarinin ne
olduğunu ve neden yazılım sistemleri geliştirilirken mutlaka dikkate alınması
gereken temel bir unsur olduğunu tartışıyoruz. Ayrıca, yazılım mimarisinin geliştirilmesiyle ilişkili farklı etkinlikleri ele alıyoruz; böylece bu kitabın ana konusu olan mimari tasarım, bu etkinliklerin bağlamında anlaşılabilir. Yine kısaca,
tasarımı oluşturmaktan sorumlu kişi olan mimarın rolünü tartışıyoruz. Son olarak, bu kitapta kapsamlı biçimde ele alacağımız mimari tasarım yöntemi olan
nitelik temelli tasarım (Attribute-Driven Design, ADD) yöntemini tanıtıyoruz.

## 1.1 Güdüler

Bu kitaptaki amacımız, sana yazılım mimarisini sistematik, öngörülebilir, tekrarlanabilir ve maliyet etkin bir biçimde nasıl tasarlayacağını öğretmektir. Eğer
bu kitabı okuyorsan, büyük olasılıkla zaten mimariye ilgi duyuyorsun ve mimar
olmayı hedefliyorsun. İyi haber şu ki bu hedef ulaşabileceğin bir noktada. Seni
bu noktada ikna etmek için, tasarım fikrinden—herhangi bir şeyin tasarımından—
kısaca söz edeceğiz ve mimari tasarımın nasıl ve neden bundan çok da farklı
olmadığını göreceğiz. Çoğu alanda “tasarım”, benzer türden zorlukları ve hususları içerir—paydaş (stakeholder) ihtiyaçlarını karşılama, bütçelere ve takvimlere uyma, kısıtlarla başa çıkma vb. Tasarımın ilkel öğeleri (primitive) ve araçları
alandan alana değişse de, tasarımın hedefleri ve adımları değişmez.

> **💬 Çevirmen notu:** Burada “design primitives” ile kastedilen, bir tasarımın
> üzerinde inşa edildiği temel yapıtaşlarıdır; yazılımda bileşen, konnektör, arayüz
> gibi kavramlar bu tür “ilkel öğe” örnekleridir.

Bu cesaret verici bir bilgidir; çünkü tasarımın yalnızca “büyücülerin”
tekelinde olmadığını gösterir. Yani, tasarım öğretilebilir ve öğrenilebilir. Özellikle mühendislikteki tasarımın çoğu, bilinen tasarım ilkel öğelerini, öngörülebilir
sonuçlar elde edecek (kimi zaman yenilikçi) biçimlerde bir araya getirmekten
ibarettir. Elbette ayrıntılar zordur; ancak bu nedenle yöntemlerimiz vardır. Tasarım gibi yaratıcı bir uğraşın adım adım bir yöntemle yakalanabileceğini hayal
etmek ilk başta zor görünebilir; yine de Parnas ve Clements’in “A Rational Design Process: How and Why to Fake It” başlıklı makalelerinde tartıştıkları gibi
bu yalnızca mümkün değil, aynı zamanda değerlidir. Elbette herkes iyi bir tasarımcı olamaz; tıpkı herkesin bir Thomas Edison ya da LeBron James ya da
Ronaldo olamayacağı gibi. İddiamız, herkesin çok daha iyi bir tasarımcı olabileceğidir; bu kitapta sunduğumuz, yeniden kullanılabilir tasarım bilgisi parçacıklarıyla desteklenen yapılandırılmış yöntemlerin, vasatlıktan mükemmelliğe giden
yolu döşemeye yardımcı olabileceğidir.

Neden yazılım mimarisi tasarımı hakkında bir kitap yazıyoruz? Tasarım
üzerine genel olarak çok şey yazılmış olmasına ve yazılım mimarisi tasarımı
üzerine de bazı yazılar bulunmasına karşın, yalnızca mimari tasarıma adanmış
bir kitap yoktur. Dahası, mimari tasarım hakkında yazılanların çoğu görece soyut kalmaktadır.

Bu kitabı yazmaktaki amacımız, herhangi yetkin bir yazılım mühendisi tarafından uygulanabilecek pratik bir yöntem sunmak ve ayrıca (ve en az bunun
kadar önemli olarak) bu yöntemi somutlaştıran zengin örnek olay çalışmaları
(topluluğu) sağlamaktı. Albert Einstein’ın “Örnek, öğretmenin bir başka yolu
değil, tek yoludur” dediği rivayet edilir. Buna yürekten inanıyoruz. Çoğumuz,
kurallar, adımlar ya da ilkeler kümelerinden çok örneklerden öğreniriz. Elbette,
yaptıklarımızı yapılandırmak ve örnekleri oluşturmak için adımlara, kurallara
ve ilkelere ihtiyaç duyarız; ancak örnekler, günlük kaygılarımıza hitap eder ve
adımları somutlaştırarak bize yardımcı olur.

Bu, mimari tasarımın hiçbir zaman basit olacağı anlamına gelmez. Eğer
karmaşık bir sistem inşa ediyorsan, büyük olasılıkla pazara çıkma süresi, maliyet, performans, evrilebilirlik (evolvability), kullanılabilirlik (usability), erişilebilirlik/süreklilik (availability) gibi pek çok birbirleriyle rekabet eden gücü dengelemeye çalışıyorsun. Bu boyutlardan herhangi birinde sınırları zorluyorsan, mimar
olarak işin daha da karmaşık olacaktır. Bu durum yalnızca yazılımda değil, herhangi bir mühendislik disiplininde böyledir. Büyük gemiler, gökdelenler ya da
diğer karmaşık “sistemlerin” tarihine bakarsan, bu sistemlerin mimarlarının da
uygun kararlar ve ödünleşimler (tradeoff) yapmak için nasıl mücadele ettiklerini görürsün. Evet, mimari tasarım belki hiçbir zaman kolay olmayacak; ancak
amacımız, iyi yetişmiş, iyi eğitimli yazılım mühendislerinin üstesinden gelebileceği, yönetilebilir (tractable) ve başarılabilir bir uğraş haline getirmektir.

## 1.2 Yazılım Mimarisi
