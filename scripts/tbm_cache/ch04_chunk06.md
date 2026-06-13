```markdown
yük durumu (load case)     değer (value)   kaynak (reference)
ekstansiyon (extension)     47.5 Nm         Goldsmith and Ommaya, 1984  
                                            Mertz and Patrick, 1993
fleksiyon (flexion)         88.1 Nm
negatif ve pozitif kesme    845 N
(negative and positive shear)
```

İlgili kesişim (intercept) değerlerine bölündükten sonra, incelenen eğilme modları (bending modes) ve yük tipleri tanımlanır. Sonuçta, zaman ölçeği değiştirilmeden uygun kesme kuvveti (shear force) ve moment (moment/torque) eğrileri toplanarak ve ortaya çıkan eğrinin maksimumu bulunarak Nkm değerleri elde edilir. Dolayısıyla, örneğin Nep, ekstansiyon (extension) ve negatif kesme (negative shear) aynı anda ortaya çıktığında, zamandaki maksimum değeri temsil eder. Analiz edilen zaman aralığı içinde belirli bir yük ve moment kombinasyonu hiç ortaya çıkmazsa, Nkm dörtlüleri (quadruples) eksik olabilir.

Kritik bir Nkm değeri bakımından, 1.0 değeri kullanılmıştır; bunun gerekçesi, ya momentin ya da kesme kuvvetinin kesişim (intercept) değerini aşmasının, boyun yaralanması (neck injury) riskini arttırmasıdır.

Bugüne kadar Nkm, çeşitli testlerde düşük hız arka çarpma (low speed rear-end collision) koşullarını değerlendirmede yararlı olduğunu göstermiştir [örneğin Muser et al. 2002, Szabo et al. 2002, Kullgren et al. 2003]. Özellikle, Nkm değerlerinin, ileri yönlü hareketle ilişkili çarpışma fazının karakterizasyonuna imkân verdiği ve bu bakımdan yalnızca daha erken fazı dikkate alan NICmax’a (maksimum Boyun Yaralanma Kriteri, NICmax, Neck Injury Criterion) ek bilgi sağladığı gösterilmiştir. Nkm ile boyun yaralanması riskinin korelasyonu açısından, Muser et al. (2003) Nek yük durumunun (load case) en güçlü öngörücü olduğunu bulmuştur. Benzer şekilde Kullgren et al. (2003), Nkm ile AIS1 boyun yaralanması (Kısaltılmış Yaralanma Ölçeği seviye 1, AIS1) riski arasında iyi bir korelasyon saptamış ve bu nedenle arka çarpma test değerlendirmesinde Nkm’nin (ve NIC’in) kullanılmasını önermiştir.

Ayrıca, Nkm değerlerinin koltuk tasarımının farklı karakteristiklerini nicelendirebildiği gösterilmiştir [Muser et al. 2002]. İyileştirilmiş otomobil koltukları için tasarım prensipleri üzerine süregelen tartışma (örneğin deformasyona izin verilmesi/plastisiteye karşı elastisite çatışması) [Parkin et al. 1995] bağlamında, hem Nkm hem de NIC değerlerini eşzamanlı olarak en aza indirgemenin dengeli bir koltuk tasarımına işaret etmesi nedeniyle, Nkm’nin yararlı bir araç olduğu bulunmuştur. Sonuç olarak bu kriterin bir ISO standart koltuk test prosedürüne dahil edilmesi önerilmiştir.

> **💬 Çevirmen notu:** Nkm, FMVSS/ECE gibi regülasyonlarda yer alan klasik kuvvet/moment sınırlarının ötesine geçip, boynun kombine yüklenme durumunu (moment + kesme kuvveti) zamana bağlı olarak değerlendiren bir “bileşik” kriterdir. Özellikle arka çarpmalarda “whiplash” riskini koltuk tasarımı ile ilişkilendirmede kullanılır.

---

## 4.4.4 İntervertebral Boyun Yaralanması Kriteri (IV-NIC, Intervertebral Neck Injury Criterion)

Arka çarpışmalarda (rear-end collisions) oluşan boyun ağrısının, intervertebral rotasyonun fizyolojik intervertebral hareket sınırını aşmasından kaynaklandığı varsayımına dayanarak, Panjabi et al. (1999) intervertebral boyun yaralanması kriterini (IV-NIC, intervertebral neck injury criterion) önermiştir. IV-NIC, travmatik yükleme altındaki intervertebral hareket θ_trau (travma altı intervertebral hareket) ile fizyolojik hareket aralığı θ_physio (fizyolojik hareket aralığı) oranı olarak tanımlanır (Denklem 4.6). Kriter, her bir intervertebral eklem i için tanımlanır ve fleksiyon (flexion) ile ekstansiyon (extension) için ayrı ayrı hesaplanır.

\[
\text{IV-NIC}_{\text{trauma}, i} = \frac{\theta_{\text{trau}, i}}{\theta_{\text{physio}, i}} \tag{4.6}
\]

Böylece, maksimum IV-NIC değeri, zamandaki, bölgedeki (lokasyon) ve eğilme modundaki (fleksiyon/ekstansiyon) en büyük intervertebral rotasyonu tanımlar; değer 1.0’dan büyükse, fizyolojik hareket aralığının aşıldığını gösterir.

Bugüne kadar IV-NIC ne doğrulanmış (validated) ne de bir eşik değer (threshold) önerilmiştir. Bütün antropomorfik test cihazlarında (ATD, crash test dummy) vertebraları birbirine bağlamak için pimli eklemler (pin joint) kullanılması nedeniyle intervertebral hareket taklit edilememekte, dolayısıyla IV-NIC’in değerlendirilmesi ATD deneylerinde imkânsız olmaktadır. Panjabi ve ark.’nın (1999) çalışmasında fizyolojik hareket aralığının sadece tek bir insan kadavra örneğine dayanılarak tanımlanmış olması da ayrı bir güçlük yaratmaktadır.

> **💬 Çevirmen notu:** IV-NIC, teorik olarak klinikte sık tartışılan “segmenter instabilite / aşırı segmenter hareket” kavramını, özellikle C4–C7 seviyelerinde nicel olarak tarif etmeye çalışan bir ölçüttür; fakat pratikte ne ATD testlerine ne de rutin adli değerlendirmeye henüz doğrudan aktarılabilmiş değildir.

---

## 4.4.5 Boyun Yer Değiştirme Kriteri (NDC, Neck Displacement Criterion)

Boyun yer değiştirme kriteri (NDC, neck displacement criterion), yumuşak doku boyun yaralanması (soft tissue neck injury) riskini değerlendirmek için önerilmiştir [Viano 2001b]. Kriter, boynun S-şeklini, ekstansiyon momentini (extension moment), z (aksiyel) yönündeki yer değiştirmeyi ve x (sagittal) yönündeki yer değiştirmeyi dikkate alarak ele alır. Baş rotasyonunun x-yer değiştirmesine karşı, z-yer değiştirmesinin ise x-yer değiştirmesine karşı grafiğe dökülmesiyle iki NDC diyagramı elde edilir.

Gönüllüler, BioRID ve Hybrid III çarpışma testi mankeni (ATD, crash test dummy) kullanılarak yapılan kızak testleri (sled test) ile NDC diyagramları için tolerans koridorları tanımlanmıştır. Ancak bu koridorların henüz kesinleşmiş olduğu kabul edilemez. Kullgren et al. (2003) tarafından sunulan bir çalışma, NDC’nin gerçek hayatta “whiplash” yaralanması (kamçı yaralanması, WAD) riskini pek iyi yansıtmadığını (kötü korelasyon) ortaya koymuştur. Bugüne kadar NDC ile ilgili ek ve anlamlı bir çalışma yayımlanmamış olup, kriter neredeyse hiç kullanılmamaktadır.

> **💬 Çevirmen notu:** NDC, daha çok baş/toraks relatif hareketini “geometrik” bir bakışla ifade etmeye çalıştığı için, klinikte görülen kronik boyun ağrı sendromlarıyla korelasyon kurmakta yetersiz kalmıştır; bu nedenle regülasyonlara girememiştir.

---

## 4.4.6 Alt Boyun Yük İndeksi (LNL, Lower Neck Load Index)

Yumuşak doku boyun yaralanması riskini değerlendirmek için önerilen bir diğer boyun yaralanma kriteri, Alt Boyun Yük İndeksi’dir (LNL, Lower Neck Load Index) [Heitplatz et al. 2003]. LNL, boyun tabanında ölçülen üç kuvvet bileşeni ile iki moment bileşenini dikkate alır (Denklem 4.7). Bu nedenle, kriterin değerlendirilebilmesi için alt boyun yük hücresi (lower neck load cell) ile donatılmış bir mankene ihtiyaç vardır.

\[
\text{LNL}(t) =
\sqrt{
\frac{M_3(t)^2}{C_{\text{moment}}^2}
+
\frac{F_{Y\_\text{lower}}(t)^2}{C_{\text{shear}}^2}
+
\frac{F_{X\_\text{lower}}(t)^2}{C_{\text{shear}}^2}
+
\frac{F_{Z\_\text{lower}}(t)^2}{C_{\text{tension}}^2}
}
\tag{4.7}
\]

Burada \(F_i(t)\) ve \(M_i(t)\) sırasıyla kuvvet ve moment bileşenleridir. Paydalar, kesişim (intercept) değerlerini temsil eder; RID mankeni (BioRID tipi ATD) için bu değerlerin \(C_{\text{moment}} = 15\), \(C_{\text{shear}} = 250\) ve \(C_{\text{tension}} = 900\) olması önerilmiştir [Heitplatz et al. 2003]. Diğer mankenler için henüz kesişim değerleri önerilmemiştir.

Arka çarpışmalar (rear-end collisions) açısından bakıldığında, LNL’nin tanımı, gerilme (tension) kuvveti için ek terim ve verilerin alt boyun yük hücresinde kaydedilmesi dışında, Nkm tanımıyla oldukça benzerdir. Bugüne dek LNL ile ilgili deneyim oldukça sınırlıdır. Mevcut aşamada LNL’nin olası bir yaralanma mekanizması ile kurulmuş bir biyomekanik bağlantısının olmayışı ve gerçek dünya yaralanma sonuçlarıyla korelasyonunun gösterilememiş olması gibi eksiklikleri bulunmaktadır [Bortenschlager et al. 2003].

> **💬 Çevirmen notu:** LNL, özellikle C7–T1 seviyesinde ölçülen yükleri (alt boyun) normalleştirerek tek bir indeks üretir. Ancak klinik “whiplash” tablolarının çoğu radyolojik lezyon göstermediğinden, bu tarz kuvvet-temelli indekslerin pratikte prognostik değeri sınırlı kalmaktadır.

---

## 4.4.7 ECE ve FMVSS’de Boyun Yaralanma Kriterleri

Mevcut regülasyonlar, önden çarpma (frontal impact) durumları için maksimum spinal yükleri tanımlar (ECE R94, FMVSS 208). Düşük hız arka çarpma (low speed rear-end impact) için tanımlanmış homologasyon testleri yoktur.

ECE R94, boyun ekstansiyon momentinin (neck extension moment) 57 Nm’yi aşmamasını gerektirir. Ayrıca, ölçülen kesme kuvvetleri (shear forces) ve aksiyel gerilme kuvvetinin (axial tension force) Şekil 4.16’da belirtilen değerlerin altında kalması gerekir.

Mevcut FMVSS 208, kompresyon (compression), gerilme (tension), kesme (shear), fleksiyon (flexion) ve ekstansiyon momenti (extension moment) için bireysel tolerans sınırlarından oluşan boyun yaralanma kriterlerini içerir (Tablo 4.6). Tolerans değerleri gönüllü, kadavra ve manken testlerine dayanmakta olup, 50. persentil erkek için geçerlidir.

> **💬 Çevirmen notu:** ECE R94 ve FMVSS 208 çerçevesindeki bu sınırlar, araç tip onayı ve pasif güvenlik değerlendirmelerinde doğrudan referans alınır. Türkiye’de ithal/yerli araçlar için UNECE regülasyonlarına uyum zorunluluğu, bu kriterleri pratikte adli ve sigorta uyuşmazlıkları açısından da önemli hale getirir.

---

Şekil 4.16 ECE R94’te belirtilen boyun kuvvetleri için süreye bağlı limitler. Üstte: gerilme (tension), altta: kesme (shear).
```
