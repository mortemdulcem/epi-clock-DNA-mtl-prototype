vücudun uzaysal yönelimi, açısal momentum (angular momentum) denkleminden elde edilir:

\[
\frac{d}{dt}\left(\sum \mathbf{M}_I(t)\right) = \dots \tag{2.2}
\]

burada açısal ivme (angular acceleration)  
\[
\frac{d^2\varphi}{dt^2}
\]
ve vücut üzerinde etkili tüm momentlerin (moment, torque/moment) \(M_I(t)\) toplamı yer alır. Katılaşma (solidification) ilkesi nedeniyle, bu denklemler deformasyon gösterebilen (deformable) cisimler için de geçerlidir; ancak bu durumda kütle merkezinin (centre of mass) konumu, cismin dış konturu (contour) ile sabit bir ilişki içinde değildir.

### Süreklilik mekaniği (continuum mechanics): yoğunluk p(x, t), zaman t, hız alanı v(x, t)

Yoğunluk \( \rho(\mathbf{x}, t) \) ve hız alanı \( \mathbf{v}(\mathbf{x}, t) \), uzaydaki belirli, sabit bir konuma karşılık gelir (bu yaklaşım çoğunlukla sürekliliğin Euler gösterimi (Euler representation) olarak adlandırılır). Hareket denklemi (equation of motion) şu biçimdedir:

\[
\frac{\partial}{\partial t}(\rho \mathbf{v}(\mathbf{x},t)) + (\nabla\cdot(\rho(\mathbf{x},t)\mathbf{v}(\mathbf{x},t))) = \mathbf{f}(\mathbf{x},t) + (\nabla \cdot \boldsymbol{\sigma}(\mathbf{x},t)) \tag{2.3}
\]

burada \(\mathbf{f}(\mathbf{x}, t)\) alan kuvvetlerini (field forces) — örneğin yer çekimi (gravity) — belirtirken, gerilme tensörü (stress tensor) \(\boldsymbol{\sigma}(\mathbf{x}, t)\) temas kuvvetlerini (contact forces) içerir. \(\nabla\) Nabla operatörüdür (Nabla operator). Açısal momentum ilişkisinin sağlanabilmesi için gerilme tensörünün \(\boldsymbol{\sigma}\) simetrik olması gerekir.

Kütlenin korunumu (conservation of mass) ayrıca süreklilik denklemini (continuity equation) verir:

\[
\frac{\partial \rho}{\partial t} + (\nabla \cdot \rho \mathbf{v}) = 0 \tag{2.4}
\]

Konumlar ve deformasyonlar 2.3 ve 2.4 numaralı denklemlerden elde edilirken, gerilme tensörü ile deformasyonlar arasındaki ilişki, sürekliliğin mekanik özelliklerini tanımlayan bir konstitutif denklem (constitutive equation) olarak formüle edilmelidir. Biyomekanik söz konusu olduğunda konstitutif ilişkiler genellikle yüksek derecede doğrusal olmayan (nonlinear) yapıdadır ve viskoelastisite (visco-elasticity) ile plastisiteyi (plasticity) içerir.

Katı cisim modelleri (rigid body models), sonlu sayıda serbestlik derecesi (degree of freedom) ile ve bunlara karşılık gelen bir grup adi diferansiyel denklem (ordinary differential equations) ile karakterize edilirken, süreklilik mekaniğinde kısmi diferansiyel denklemler (partial differential equations) baskındır ve serbestlik derecesi sayısı sonsuzdur. Sayısal çözüm için bu kısmi diferansiyel denklemler özel formülasyonlarla yaklaşık hale getirilmek zorundadır; travma-biyomekaniğinde en sık kullanılan yaklaşım Sonlu Eleman yaklaşımıdır (Finite Element approximation) (bkz. Bölüm 2.6).

Katı cisim yaklaşımı (rigid body approximation) çerçevesinde (denklemler 2.1, 2.2), bir darbe/çarpma (impact) olayının tanımlanması için yapılan ampirik incelemeler ve laboratuvar deneyleri, etki kuvvetlerinin (impact forces) etkisi altındaki bir vücut segmentinin kütle merkezinin ivmesinin (acceleration of the centre of mass) darbenin şiddetini değerlendirmek için önemli bir parametre olduğunu göstermiştir. Birçok pratik durumda, ivmenin \(|\mathbf{a}(t)|\) büyüklüğü, yer çekimi ivmesi (acceleration due to gravity) \(g\) ile ilişkilendirilir (1 g = 9.81 m/s²), çünkü yer çekimine sürekli maruz kaldığımız için belirli bir ivme büyüklüğünü günlük deneyimlerimizle ilişkilendirebiliriz. Bununla birlikte, bir kaza (accident) sırasında vücudun maruz kaldığı ivme zamanla değişir; bu nedenle, "tepe (maksimum) ivme" (peak acceleration) ve "ortalama ivme"nin (mean acceleration) ve bunlara karşılık gelen zaman aralıklarının her zaman net biçimde ayırt edilmesi, yanlış anlamaları önlemek açısından zorunludur.

> **💬 Çevirmen notu:** Adli raporlarda sıklıkla sadece "ivme" değeri verilir; ancak mahkeme değerlendirmesi için hem zirve (peak) hem de etki süresi (pulse duration) kritik olup, HIC gibi yaralanma kriterleri bu zaman bağımlılığını doğrudan içerir.

### Kaza rekonstrüksiyonu bağlamında tanımlanan bazı parametreler

Rekonstrüksiyon teknikleri, çoğunlukla sistematik biçimde trafik kazaları (traffic accidents) için geliştirilmiştir. Bu tür durumlarda, ilgili araca ait belirli sayıda parametrenin, yolcu/iştirakçilerin maruz kaldığı yüklenme durumunun (loading situation of occupants) değerlendirilmesinde kullanışlı olduğu gösterilmiştir.

- Bir aracın çarpışma hızı veya darbe hızı (collision or impact velocity), kamuoyunda muhtemelen en sık atıf yapılan parametredir. Kaza rekonstrüksiyonunda, seyir hızı (travelling speed) — veya daha doğrusu, herhangi bir frenleme (braking) eyleminin başlangıcından önceki hız — bir çarpışmanın hangi koşullarda önlenebileceğini araştırırken bazen önem taşır.

- Buna karşın, söz konusu araç için çarpışma kaynaklı hız değişimi (collision-induced velocity change), yani delta-v, yolcular üzerindeki çarpışma etkileri söz konusu olduğunda çarpışmanın şiddetini tanımlamak için çoğu durumda daha kullanışlıdır. Delta-v, tek darbeli ve aracın belirgin dönme hareketi göstermediği çarpışmalarda, aracın çarpışma süresi boyunca maruz kaldığı doğrusal yavaşlamanın (translational vehicle deceleration) integraliyle yaklaşık olarak örtüşür. Ancak, karmaşık çarpışma durumlarında (devrilme, yoldan aşağı yuvarlanma vb.) delta-v iyi tanımlanmış bir parametre olmayabilir.

> **💬 Çevirmen notu:** Uygulamada sigorta ve adli değerlendirmelerde “delta-v” sıklıkla tek başına şiddet göstergesi gibi kullanılmaktadır; devrilme, çoklu çarpışma gibi senaryolarda bu yaklaşım yetersiz ve yanıltıcı olabilir.

- Enerji eşdeğer hızı (energy equivalent speed, EES), bir aracı deforme etmek için gereken enerji miktarını karakterize eder. Gerçekte EES, rijit bir bariyere (rigid barrier) olan çarpma hızını temsil eder; bu hız, gerçek kazada gözlenen kalıcı deformasyon (permanent deformation) ile aynı miktarda kalıcı deformasyon oluşturmak için gerekli olurdu. EES, [km/h] birimiyle verilir ve birçok araç tipi için, sözde EES kataloglarından (EES catalogues) elde edilebilir. Bu kataloglar, iyi tanımlanmış test koşullarında gerçekleştirilen çarpışma testleri (crash tests) temelinde oluşturulur.

- Darbe koşullarını tanımlamak için kullanılan bir başka parametre, araç örtüşmesi (vehicle overlap)dir. Bu, aracın ve çarpışma partnerinin (örneğin başka bir araç ya da bir çarpışma testindeki bariyer) birbirinin üzerine ne ölçüde bindirildiğini (overlap extent) gösterir. Örtüşme genellikle, dikkate alınan aracın toplam genişliğinin, karşıt araç (ya da duvar) tarafından kaplanan yüzdesi olarak ifade edilir.

> **💬 Çevirmen notu:** Euro-NCAP ve benzeri çarpışma testlerinde “%40 önden çarpma” gibi ifadeler, burada anlatılan overlap tanımına karşılık gelir; adli rekonstrüksiyonda araç üzerindeki deformasyon alanının genişliği ile tahmin edilir.

---

### Şekil 2.1: Restitüsyon katsayısı ve hız ilişkisi

koefisiyent of restitution k (restitüsyon katsayısı k)

1,0

0,8

0,6

0,4

0,2

0         20 40 60 80 100 120  
göreli hız (relative velocity) [km/h]

**Şekil 2.1** Rijit bir bariyere (rigid barrier) karşı bir binek otomobil (passenger car) için önden çarpma (frontal impact) durumunda, restitüsyon katsayısı (coefficient of restitution) ile göreli hız (relative velocity) arasındaki ilişkinin şematik gösterimi [Appel ve ark. 2002’den uyarlanmıştır].

Temel mekanik bilgisine göre, elastik ve plastik darbe (elastic and plastic impact) ilkeleri ve bunlara eşlik eden restitüsyon katsayısı (coefficient of restitution, k-faktörü), çarpma sırasında ortaya çıkan elastik ve plastik (yani kalıcı) deformasyon bileşenlerini karakterize etmek için kullanılır. Şekil 2.1, örnek olarak, restitüsyon katsayısının çarpma hızına (impact velocity) (rijit bir duvara karşı) bağımlılığını göstermektedir.

> **💬 Çevirmen notu:** Restitüsyon katsayısı k, çarpışma sonu hızının başlangıç hızına oranı gibi düşünülebilir; otomotiv çarpışmalarında k < 1 olup, hız arttıkça enerji daha çok plastisiteye (kalıcı deformasyona) gider ve k küçülür.

---

Günümüzde trafik kazalarının çoğu, Carat [IBB 2002], PC-Crash [DSD 2000] ya da EDCRASH [EDC 2006] gibi, kullanımı kolaylaştırılmış bilgisayar programları kullanılarak rekonstrükte edilmektedir. Bu programlar kapsamlı olarak doğrulanmıştır (validated) ve uygulama prosedürleri iyi tanımlanmıştır. Bu kapsamda katı cisim dinamiği (rigid body dynamics) uygulanır (denklemler 2.1, 2.2). Bu tür programlar kullanılırken, ilke olarak iki yöntem ayırt edilir: "ileri" (forward) ve "geri" (backward) hesaplama.

- İleri hesaplamada, çarpışma öncesi kinematik varsayılır; yani başlangıçta çarpışma partnerlerine hareket yönleri, hızlar vb. atanır. Daha sonra, katı cisim denklemleri, lastik (tire) ve çarpışma (collision) kuvvetleri hesaba katılarak integre edilir ve gerçek çarpışma ile çarpışma sonrası partnerlerin son konumları belirlenir. Son aşamada, gerçek kaza yerinde kaydedilen konumlar ve izler (traces), hesaplama sonuçlarıyla karşılaştırılır. Yinelemeli (iterative) bir süreçle, giriş parametreleri ayarlanır ve hesaplama, elde edilen sonuçlar ile mevcut kaza verileri arasında tatmin edici bir uyum sağlanıncaya kadar tekrarlanır.

- Geri hesaplama yöntemi ise çarpışma partnerlerinin son konumlarının incelenmesiyle başlar. Sonraki adımda …

> **💬 Çevirmen notu:** PC-Crash ve benzeri yazılımlar, Türkiye’de bilirkişiler ve Adli Tıp Kurumu tarafından da yaygın kullanılır; mahkeme dosyalarında “ileri/geri simülasyon” tartışmalarında bu forward/backward yöntem ayrımı önemlidir.
