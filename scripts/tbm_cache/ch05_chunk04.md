## 5.4.2     Toraks Travma İndeksi (TTI, Thoracic Trauma Index)

Toraks Travma İndeksi, yandan çarpma (yan darbe, side impact) durumunda toraks için kullanılan bir yaralanma kriteridir (injury criterion). Bu indeks, yaralanma meydana gelişinin, darbe alan taraftaki kosta kafesi (kaburga kafesi, rib cage) ile alt torasik omurganın (lower thoracic spine) maruz kaldığı maksimum lateral ivmenin (lateral acceleration) ortalama değeriyle ilişkili olduğu varsayımına dayanır. Ayrıca TTI, test edilen kişinin vücut ağırlığını (weight) ve yaşını (age) da hesaba katar; böylece kinematiklere ait bilgiyi, deneğin bireysel vücut yapısına ilişkin parametrelerle birleştirir. Bu indeks (boyutsal olarak [g]) aşağıdaki şekilde tanımlanır:

\[
TTI = 1{,}4 \cdot AGE + 0{,}5 \cdot (RIB_y + T12_y)\cdot \left(\frac{M}{M_{std}}\right) \tag{5.1}
\]

Burada:
- AGE: Test edilen kişinin yaşı [yıl],
- RIB\_y [g]: Darbe alan tarafta, 4. ve 8. kostalarda ölçülen lateral ivmenin mutlak değerinin maksimumu,
- T12\_y [g]: 12. torasik vertebranın lateral ivmesinin mutlak değerinin maksimumu,
- M: Denek kütlesi [kg],
- Mstd: Standart kütle, 75 kg.

50. persantil Hybrid III çarpışma testi mankeni (Hybrid III dummy) kullanılarak yapılan çarpışma testlerinde, TTI’nin farklı bir versiyonu olan TTI(d) hesaplanabilir. TTI(d) değerlerinin elde edilmesinde, Denklem 5.1’deki yaşa bağlı terim çıkarılır ve kütle oranı 1,0 alınır.

TTI ve TTI(d) değerlerinin hesaplanması için gerekli ivme sinyallerinin, tanımlı bir prosedüre göre ön işleme tabi tutulması (filtreleme ve örnekleme) zorunludur. Bu prosedür FMVSS 214 ve SAE J1727 dokümanlarında tanımlanmıştır.

TTI değerlerini torasik yaralanmalarla ilişkilendirmek için çok sayıda kadavra testi yapılmış [ör. Kallieris ve ark. 1981] ve istatistiksel olarak yaralanma risk fonksiyonları oluşturulmuştur. Bu nedenle TTI, biyomekanik bir ilişkiden ziyade istatistiksel bir korelasyonu yansıtır; TTI’in doğrudan herhangi bir spesifik yaralanma mekanizmasıyla ilişkilendirilmesi mümkün değildir.

> **💬 Çevirmen notu:** TTI, yan çarpışma regülasyonlarında (FMVSS 214, ECE R95 gibi) sık kullanılan, ancak mekanizmaya değil sonuç istatistiğine dayanan bir ölçüttür. Adli rekonstrüksiyonlarda doğrudan “bu TTI değeri şu tip kırığa karşılık gelir” demekten kaçınmak gerekir.

---

## 5.4.3     Kompresyon Kriteri (C, Compression Criterion)

Künt darbe (blunt impact) testlerini analiz eden Kroell ve ark. (1971, 1974), maksimum toraks kompresyonunun (thorax compression) Kısaltılmış Yaralanma Ölçeği (AIS, Abbreviated Injury Scale) ile iyi korele olduğunu, oysa kuvvet (force) ve ivmenin (acceleration) böyle bir korelasyon göstermediğini ortaya koymuştur. Kompresyon (C), göğüs deformasyonunun (chest deformation) toraks kalınlığına bölünmesiyle tanımlanmış ve şu ilişki elde edilmiştir:

\[
AIS = -3{,}78 + 19{,}56 \cdot C \tag{5.2}
\]

Örneğin 50. persantil erkek için göğüs kalınlığı 230 mm iken 92 mm toraks deformasyonu ölçülürse, kompresyon C = %40 olur ve bu, AIS 4 düzeyinde yaralanma öngörür. %30 kompresyon ise AIS 2’ye karşılık gelir.

Yaralanma riskinin istatistiksel analizi, önden çarpışmada toraks kompresyonunun %35 olmasının, AIS 4 ve üzeri şiddette (severe) yaralanmalar için %25 olasılıkla ilişkili olduğunu göstermektedir. FMVSS 208, 50. persantil Hybrid III dummiesi için önden çarpışmada maksimum 76 mm göğüs deformasyonuna izin vermektedir.

> **💬 Çevirmen notu:** Buradaki kompresyon yüzdeleri, özellikle emniyet kemeri tasarımı ve araç içi pasif güvenlik değerlendirmelerinde kritik eşiği temsil eder. Türkiye’de kullanılan yeni araçlar da ECE/FMVSS uyumlu olduğundan, bu değerler yerli vakaların mühendislik analizi için doğrudan referans alınabilir.

---

## 5.4.4     Viskoz Kriter (VC, Viscous Criterion)

Viskoz kriter (VC; viskoz kompresyon hızı, velocity of compression), yumuşak doku kriteri (soft tissue criterion) olarak da adlandırılır; göğüs bölgesi için tanımlanmış bir yaralanma kriteridir. Bu kriter, yumuşak doku (soft tissue) yaralanmasının hem kompresyona (compression) hem de kompresyon hızına (rate) bağımlı olduğunu dikkate alır.

VC değeri [m/s], toraks deformasyon hızının (deformation speed) toraks deformasyonuyla çarpımının zamana bağlı en büyük (maksimum) anlık değeridir. Her iki büyüklük de kaburga (yan darbe, side impact) ya da göğüs (önden darbe, frontal impact) deformasyonu ölçülerek belirlenir. Buna göre:

\[
VC = V(t) \times C(t) = \left[\frac{dD(t)}{dt}\right] \times \frac{D(t)}{b} \tag{5.3}
\]

Burada:
- V(t) [m/s]: Deformasyonun zamana göre türevinden elde edilen deformasyon hızı,
- D(t): Zamana bağlı deformasyon,
- C(t): Anlık kompresyon fonksiyonu (instantaneous compression function); deformasyon D(t)’nin, başlangıç gövde kalınlığına (initial torso thickness) b oranı,
- b: Başlangıç gövde kalınlığı.

Deformasyon verilerinin nasıl filtre edileceğine ilişkin ayrıntılar, yan darbe için ECE R95’te, önden darbe için ise SAE J1727’de verilmektedir. Uygulamada çoğunlukla maksimum VC, yani VCmax rapor edilir; VCmax’ın torasik yaralanma riskiyle iyi korele olduğu gösterilmiştir [Viano ve Lau 1985].

Lobdell modeli kullanılarak (bkz. Bölüm 5.3.1), VC ile toraksta absorbe edilen enerji (energy) arasında bir ilişki kurulabilir. Kritik değerlere ilişkin olarak hem ECE R95 (lateral darbe) hem de ECE R94 (frontal darbe) düzenlemelerinde VC’nin 1,0 m/s’den küçük veya ona eşit olması (≤ 1,0 m/s) gerekmektedir.

> **💬 Çevirmen notu:** VC, özellikle yüksek hızda ve kısa süreli yüklemelerde (örneğin hava yastığı açılması) yumuşak doku zedelenmelerini açıklamak için klasik kompresyon yüzdesinden daha duyarlı bir ölçüttür.

---

## 5.4.5     Kombine Torasik İndeks (CTI, Combined Thoracic Index)

Kombine Torasik İndeks (CTI), önden çarpışma (frontal impact) durumunda göğüs bölgesi için tanımlanmış bir yaralanma kriteridir [Kleinberger ve ark. 1998]. Kompresyon ve ivme yanıtlarını bir araya getiren CTI, özellikle hem hava yastığı (airbag) hem de emniyet kemeri (seat belt) yüklemelerini dikkate alır.

CTI, omurganın bileşke (resultant) ivmesinin 3 ms’lik değerlendirilmiş değeri (3 ms value) ile göğüs deformasyonunun kombinasyonu olarak tanımlanır. CTI, şu eşitliğe göre hesaplanır:

\[
CTI = \frac{A_{max}}{A_{int}} + \frac{D_{max}}{D_{int}} \tag{5.4}
\]

Burada:
- \(A_{max}\): Omurganın bileşke ivmesinin 3 ms’lik tek tepe (single peak) değeri [g],
- \(A_{int}\): Kritik 3 ms kesme (intercept) değeri [g],
- \(D_{max}\): Göğüs deformasyonu [mm],
- \(D_{int}\): Deformasyon için kritik kesme değeri [mm].

Kesme değerleri (intercept values) farklı dummies türleri için ayrı ayrı tanımlanmıştır. Örneğin 50. persantil Hybrid III için \(A_{int} = 85\) g ve \(D_{int} = 102\) mm olarak verilmiştir.

Kombine kompresyon ve ivme kriteri, kemer ve hava yastığı sistemlerinin toraksa uyguladığı farklı yükleme karakteristiklerini hesaba katar. Aynı toplam yük için, temas alanı daha küçük olan bir kemer sistemi, temas alanı daha geniş bir hava yastığına göre toraks üzerinde daha yüksek basınç (pressure) oluşturacaktır. Kombine kemer/hava yastığı sisteminde baskın yükleme bir çizgisel yük (line load) olabilir; yani kemerin uyguladığı yük, hava yastığınınkinden büyük olabilir veya tersi durumda dağıtılmış bir yük (distributed load) söz konusu olur.

CTI, bu iki uç durum arasındaki tüm yükleme senaryolarının yelpazesini yansıtmayı amaçlar. Maksimum toraks ivmesi, gövdeye kütlesiyle orantılı olarak uygulanan toplam kuvvetlerin büyüklüğünün bir ölçüsüyken, toraks deformasyonu kemer yüklemesinin bir göstergesidir. Birim ivme başına deformasyon ne kadar büyükse, kemer sisteminin göreli katkısı o kadar fazladır [Cavanaugh 2002].

CTI, kadavra testlerine dayalı olarak geliştirilmiş ve lojistik regresyon analizi ile AIS ile ilişkilendirilmiştir. Günümüzde CTI, veri toplama ayrıntıları ve farklı kesme değerlerinin verildiği FMVSS 208 regülasyonuna dâhil edilmiştir.

> **💬 Çevirmen notu:** CTI’nin FMVSS 208 içine alınmış olması, özellikle ABD pazarına yönelik araçların toraks koruma performansında sadece deformasyon veya sadece ivme sınırlarının yeterli görülmediğini, kombinasyonun esas alındığını gösterir. Forensik değerlendirmede, sadece “göğüs çökmüş mü?” sorusuna değil, yüklemenin dinamiğine de bakmak gerektiğini hatırlatır.

---

## 5.4.6     Diğer Kriterler

Kaburga Sapma Kriteri (RDC, Rib Deflection Criterion), yan darbe çarpışmasında kaburgaların sapmasını (deflection) mm cinsinden ifade eden kriterdir. ECE R95’e göre, yan darbe dummiesi için RDC değeri 42 mm’den küçük veya 42 mm’ye eşit olmalıdır (≤ 42 mm).

ThCC (ya da TCC), Toraks Kompresyon Kriteri’nin (Thoracic Compression Criterion) kısaltmasıdır. ThCC, önden çarpışmada sternum ile omurga arasındaki toraks kompresyonu kriteridir ve toraks kompresyonunun mutlak değeri kullanılarak, mm cinsinden belirlenir. Günümüzde ECE R94’te maksimum eşik değer (threshold) 50 mm olarak tanımlanmıştır.

> **💬 Çevirmen notu:** RDC ve ThCC, pratik regülasyonlar için doğrudan ölçülebilir ve anlaşılır limitler sunar. Özellikle araç içi yaralanma bilirkişiliğinde, “kaburga defleksiyonu/toraks kompresyonu mevcut Euro-NCAP/ECE limitlerine göre aşırı mıydı?” sorusu, üretici sorumluluğu tartışmalarında sıkça gündeme gelebilir.

---

## 5.5       Sporda Torasik Yaralanmalar

Spora özgü torasik yaralanmalarla ilgili olarak literatürde fazla bilgi bulunmamaktadır. Yukarıda açıklanan yaralanma ve yaralanma mekanizması tanımları, travmatik spor yaralanmaları için de geçerlidir. Buna ek olarak aşırı kullanım (overuse) yaralanmaları da görülebilir; örneğin elit kürekçilerde (elite rowers) kosta stres kırıkları (rib stress fractures) [Karlson 1998]. Ancak bu, oldukça nadir bir fenomen olarak görünmektedir.

> **💬 Çevirmen notu:** Üst düzey kürek ve benzeri sporlar, kosta kafesini tekrarlayan eğilme ve kas çekiş yüklerine maruz bırakarak, klasik trafik kazalarından farklı bir “mikrotravma” profili oluşturur. Adli ve spor hekimliği pratiğinde bu tür stres kırıklarının yanlışlıkla akut künt travma sonucu sanılmaması için antrenman öyküsünün ayrıntılı alınması önemlidir.
