matematiksel kafa modelleri, örneğin sonlu eleman yöntemi (finite element method) kullanılarak, bu görevi ele almakta ve darbe/çarpma (impact) karşısında kafanın mekanik cevabının öngörülebilmesi için ölçütler belirlemeyi amaçlamaktadır. Bu tür modeller, yaşayan insanın cevabının ayrıntılı incelenmesine ait sonuçlarla birleştirildiğinde, kafa yaralanması mekanizmalarının ve kafanın darbe toleransının (impact tolerance) günümüzde anlaşılmasına önemli ölçüde katkıda bulunma vaadini taşımaktadır.

## 3.4 Kafa yaralanmaları için yaralanma kriterleri (injury criteria for head injuries)

Son birkaç yılda pasif güvenlik alanında, gelişmiş tutucu sistemlerin (advanced restraint systems) devreye sokulması gibi, kafa yaralanmalarının sayı ve şiddetini azaltmaya yönelik büyük ilerlemeler kaydedilmiş olmasına rağmen, yaygın kullanımda olan yalnızca tek bir yaralanma kriteri vardır; otuz yıldan daha uzun süre önce geliştirilmiş olan Kafa Yaralanması Kriteri (HIC, Head Injury Criterion). HIC ve onun Avrupa’daki karşılığı olan Kafa Koruma Kriteri (HPC, Head Protection Criterion) yanında, “3 ms kriteri (3 ms criterion)” ve Genelleştirilmiş Beyin Yaralanması Eşiği İvme Modeli (GAMBIT, Generalised Acceleration Model for Brain Injury Threshold) de sunulmuştur. Ancak, bu kriterlerin tamamının yalnızca ivme (acceleration) cevabına dayandığına dikkat edilmelidir. Bunun bir sonucu olarak, ivmeden ziyade darbe kuvveti (impact force) ile ilişkili yaralanmalar bu kriterler tarafından kapsanmamaktadır. Başka bir deyişle, bu kriterler kafanın kemik yapılarında kırık (fracture) oluşması riskinin değerlendirilmesine olanak vermez. Yüz bölgesine darbe karşısında kuvvet cevabını ölçebilen tek manken THOR çarpışma testi mankenidir (THOR dummy; bkz. Bölüm 2.5.1), ancak bu manken güncel çarpışma testi standartlarına dâhil değildir.

> **💬 Çevirmen notu:** Otomotiv çarpışma testlerinde hâlen yaygın olarak kullanılan Hybrid III mankenler, yüz ve kafa kemiklerine gelen kuvvetleri doğrudan ölçememektedir; bu nedenle kafatası kırıkları için doğrudan kuvvet esaslı bir kriter kullanılamamaktadır. THOR, daha gelişmiş sensör donanımına sahip yeni nesil bir antropomorfik test cihazıdır.

### 3.4.1 Kafa Yaralanması Kriteri (HIC, Head Injury Criterion)

Kafa Yaralanması Kriteri (HIC), Gadd’in (1961) çalışmalarına dayanan tarihsel bir temele sahiptir; Gadd, Wayne State Tolerans Eğrisini (WSTC, Wayne State Tolerance Curve) (bkz. Bölüm 3.3) kullanarak sözde şiddet indeksi (SI, severity index) geliştirmiştir. 1971’de Versace (1971), WSTC ile korele olan ortalama ivmenin bir ölçüsü olarak HIC’in bir sürümünü önermiştir. HIC’in güncel sürümü daha sonra ABD Ulusal Karayolu Trafik Güvenliği İdaresi (NHTSA, National Highway Traffic Safety Administration) tarafından önerilmiş ve FMVSS No. 208’e dâhil edilmiştir. HIC, aşağıdaki ifadeye göre hesaplanır:

\[
\mathrm{HIC} = \max_{t_1, t_2}
\left[
(t_2 - t_1)
\left(
\frac{1}{t_2 - t_1} \int_{t_1}^{t_2} a(t)\, dt
\right)^{2{,}5}
\right]
\tag{3.1}
\]

burada \(t_2\) ve \(t_1\), ivme darbesi (acceleration pulse) süresince seçilen keyfi iki zaman noktasıdır. İvme, yerçekimi ivmesi (g, acceleration of gravity) katları cinsinden; zaman saniye (s) cinsinden ölçülür. Hesaplamada bileşke ivme (resultant acceleration) kullanılır. FMVSS 208, \(t_2\) ve \(t_1\) arasındaki sürenin 36 ms’ten fazla olmamasını (bu nedenle HIC36 olarak adlandırılır) ve 50. persantil erkek (50th percentile male) için maksimum HIC36 değerinin 1000’i aşmamasını şart koşar. 1998’de NHTSA ayrıca HIC15’i, yani 15 ms’lik bir zaman aralığı üzerinde değerlendirilen HIC’i (Kleinberger ve ark. 1998) devreye sokmuştur. İlgili eşik değer olarak, 50. persantil erkek için maksimum 700 değeri önerilmiştir.

HIC ile kranium/kafatası (skull) ve beyin yaralanmaları arasındaki ilişkiyi belirlemek için, mevcut test verileri üzerine normal, log-normal ve iki parametreli Weibull kümülatif dağılımlar oturtularak istatistiksel analiz yapılmış; her bir fonksiyon için en iyi uyumu sağlamak amacıyla En Çok Olabilirlik (Maximum Likelihood) yöntemi kullanılmıştır [Hertz 1993]. Veriler için en iyi uyum log-normal eğriyle elde edilmiştir (Şekil 3.9).

Kafatası kırığı (AIS 2) olasılığı aşağıdaki formülle verilir:

\[
p(\text{fracture}) = N\left(\frac{\ln(\mathrm{HIC}) - \mu}{\sigma}\right)
\tag{3.2}
\]

burada \(N(\cdot)\) kümülatif normal dağılımı, \(\mu = 6{,}96352\) ve \(\sigma = 0{,}84664\)’tür.

Bu risk analizinin oluşturulmasında kullanılan veriler, tipik olarak 12 ms’ten kısa süreli darbelerden oluştuğu için, HIC eğrisi hem HIC15 hem de HIC36 için uygulanabilirdir. Buna göre, orta boy erkek (mid-sized male) için HIC15 eşik değeri 700 ile ilişkili kafatası kırığı (AIS 2) olasılığı %31’dir; HIC36 için 50. persantil erkek için sınır değer 1000 olduğunda ise bu olasılık yaklaşık %48’dir.

Temelde, WSTC için tanımlanmış sınırlamaların (bkz. Bölüm 3.3) burada da geçerli olduğu söylenebilir. Dönme ivmesinin (rotational acceleration) hesaba katılmaması sıkça eleştirilmektedir. Bir diğer dezavantaj, insan kafa yaralanması ile antropomorfik test cihazında (ATD, anthropomorphic test device) ölçülen ivme cevabı arasında fonksiyonel bir ilişkinin eksikliğidir. Bu sınırlamalara rağmen, HIC hâlâ otomotiv araştırmalarında kafa yaralanması için en yaygın kullanılan kriterdir.

0,8  

0,2  

0          500      1000      1500      2000      2500      3000  
                          HIC  

Şekil 3.9 Kafatası kırığı (AIS 2) olasılığının HIC ile ilişkisi; Hertz (1993) tarafından belirlenmiştir.

> **💬 Çevirmen notu:** Buradaki olasılık eğrisi, belirli bir HIC değerinin “mutlak kırık var/yok” sınırı olmadığını; kırık riskinin istatistiksel olarak kademeli arttığını göstermektedir. Örneğin, 1000’in altında HIC değerlerinde dahi anlamlı bir kırık olasılığı mevcuttur; bu, adli değerlendirmelerde “limitin altında → mutlaka zarar yok” şeklindeki yanlış yorumların önüne geçmek için önemlidir.

### 3.4.2 Kafa Koruma Kriteri (HPC, Head Protection Criterion)

Kafa Koruma Kriteri (HPC, Head Performance/Protection Criterion) belirlenmesi, ECE R94 ve R95 regülasyonlarında zorunlu tutulmaktadır. Dolayısıyla HPC, hem önden çarpma (frontal impact) hem de yandan çarpma (lateral impact) durumlarında kafa darbesini niceliksel olarak değerlendirmek için kullanılır. HPC’nin tanımı ve hesaplama prosedürü, HIC36 ile özdeştir. Buna göre, ilgili maksimum zaman aralığı 36 ms’tir. Önden ve yandan çarpma yönleri için eşik düzeyi 1000’dir.

Herhangi bir kafa teması gerçekleşmezse, ulaşılan ivme düzeyi ne olursa olsun HPC koşulu sağlanmış kabul edilir. Kafa temasının başlangıcı yeterli doğrulukla belirlenebiliyorsa, \(t_1\) ve \(t_2\) (bkz. Denklem 3.1) HPC’nin maksimum olduğu zaman dilimini tanımlayan, kafa temasının başlangıcı ile kaydın sonu arasındaki iki zaman noktasıdır.

> **💬 Çevirmen notu:** HPC’nin HIC36 ile aynı matematiksel yapıda olması, araç içi farklı temas senaryolarında (örn. panel, yan perde hava yastığı, direk çarpması) daha tutarlı regülasyon uygulamasını hedefler. Ancak yine yalnızca ivmeye dayalıdır ve temas kuvveti veya temas alanı gibi parametreleri içermez.

### 3.4.3 3 ms kriteri (a3ms)

“3 ms kriteri (3 ms criterion)” de WSTC’ye dayanmaktadır. 3 ms süreyle aşılan ivme düzeyi olarak tanımlanır ve 80 g değerini aşmamalıdır [Got ve ark. 1978]. Bu kriter, araç içi yapıların (interior structures) yolcuya etkisi ve baş dayanaklarına (head restraints) çarpma ile ilgili regülasyonlar olan ECE R21 ve R25’e de dâhil edilmiştir. Benzer ABD regülasyonu FMVSS 201 ile önden çarpma regülasyonu FMVSS 208 de bu kriterin sağlanmasını şart koşar.

Ayrıca, a3ms kriterinin bir modifikasyonu kask testlerinde kullanılmaktadır. Süre 5 ms olarak seçildiğinde, ivme düzeyi 150 g’den küçük veya ona eşit olmalıdır. Bu sözde a5ms kriterinin ayrıntıları ECE R22’de tanımlanmıştır.

> **💬 Çevirmen notu:** 3 ms ve 5 ms kriterlerinin kısa süreli pik ivmeleri sınırlamaya yönelik olması, özellikle kask ve iç trim tasarımında “sert, kısa pikler”in filtrelenmesini amaçlar. Türk mevzuatında ECE R22 uyumlu kask testleri, motosiklet ve bazı spor kasklarında doğrudan uygulama bulmaktadır.

### 3.4.4 Beyin Yaralanması Eşiği için Genelleştirilmiş İvme Modeli  
(GAMBIT, Generalized Acceleration Model for Brain Injury Threshold)

Doğrusal (translational) ve dönme (rotational) ivmeyi birleştirme girişimi kapsamında Newman (1986), Beyin Yaralanması Eşiği için Genelleştirilmiş İvme Modeli’ni (GAMBIT, Generalized Acceleration Model for Brain Injury Threshold) önermiştir. Doğrusal ve dönme ivmelerinden oluşan birleşik bir yükleme durumunun (combined load case) kafa yaralanmasına neden olabileceği varsayımına dayanarak, aşağıdaki ilişki önerilmiştir:

\[
\mathrm{GAMBIT} = \left[\left(\frac{a(t)}{a_c}\right)^n + \left(\frac{\phi(t)}{\phi_c}\right)^m\right]^{1/k}
\tag{3.3}
\]

Burada \(a(t)\) ve \(\phi(t)\), sırasıyla doğrusal (translational) ve dönme ivmesini (rotational acceleration) belirtir. \(a_c\) ve \(\phi_c\), bu ivmeler için kritik tolerans düzeylerini temsil eder; \(n\), \(m\) ve \(k\) ise sabitlerdir. Mevcut verilere istatistiksel analiz ve bilgisayar simülasyonları ile bu sabitlerin uydurulması sonucunda Kramer (1998/2006), aşağıdaki çözümü sunmuştur:

\[
\mathrm{GAMBIT} = \left[\left(\frac{a(t)}{251\,g}\right)^{2{,}5} + \left(\frac{\phi(t)}{25\,\text{krad/s}^2}\right)^{2{,}5}\right]^{\frac{1}{2{,}5}}
\tag{3.4}
\]

burada \(a(t)\) [g] ve \(\phi(t)\) [krad/s²] cinsinden verilmiştir. Şekil 3.10, Denklem 3.4 kullanılarak elde edilmiş sabit GAMBIT eğrilerini göstermektedir. Bu eğrilerden biri için \(a\) … (metin devam ediyor).

> **💬 Çevirmen notu:** GAMBIT, yalnızca doğrusal ivmeye bakan HIC türü kriterlere kıyasla, beyin dokusu için önemli olduğu bilinen dönme bileşenini de hesaba katması nedeniyle özellikle diffüz aksonal yaralanma (DAI) gibi lezyonların değerlendirilmesinde teorik olarak daha uygun bir çerçeve sunar. Bununla birlikte, otomotiv regülasyonlarında henüz yaygın kabul görmüş bir zorunlu kriter değildir.
