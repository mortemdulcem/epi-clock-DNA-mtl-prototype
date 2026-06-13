## Maliyet Fayda Analizi Yöntemi (Cost Benefit Analysis Method, CBAM)

CBAM, tasarım alternatiflerinin seçiminde nicel (quantitative) bir yaklaşım kullanan bir yöntemdir. Bu yöntem, mimari stratejilerin (yani tasarım kavramı kombinasyonlarının) kalite niteliği (quality attribute) tepkilerini etkilediğini ve her bir tepki düzeyinin de sistem paydaşlarına (stakeholder) fayda sağladığını, bu faydanın da yararlılık (utility) olarak adlandırıldığını varsayar. Her bir mimari strateji farklı bir yararlılık düzeyi sağlar, fakat aynı zamanda bir maliyeti vardır ve uygulanması zaman alır. CBAM’in arkasındaki fikir, yararlılık düzeyleri ve uygulama maliyetleri incelenerek, belirli mimari stratejilerin bunlara bağlı yatırım getirisi (return on investment, ROI) temelinde seçilebilmesidir. CBAM, bir ATAM’in (architecture tradeoff analysis method) ardından uygulanmak üzere tasarlanmıştır, ancak mimari değerlendirmenin yapıldığı andan önce, yani tasarım sırasında da CBAM kullanılabilir.

CBAM, girdisi olarak önceliklendirilmiş geleneksel kalite niteliği senaryoları (quality attribute scenario) kümesini alır; bu senaryolar daha sonra ek bilgilerle analiz edilir ve rafine edilir. Bu ekleme, her senaryo için birden çok tepki düzeyinin dikkate alınmasıdır:

- En kötü durum senaryosu: Sistemin çalışmak zorunda olduğu asgari eşiği temsil eder (yararlılık = 0).
- En iyi durum senaryosu: Paydaşların bundan sonra ilave yararlılık öngörmediği düzeyi temsil eder (yararlılık = 100).
- Mevcut senaryo: Sistemin halihazırda çalıştığı düzeyi temsil eder (mevcut senaryonun yararlılığı paydaşlar tarafından tahmin edilir).
- Arzulanan senaryo: Paydaşların ulaşmayı umdukları tepki düzeyini temsil eder (arzulanan senaryonun yararlılığı paydaşlar tarafından tahmin edilir).

Bu veri noktaları kullanılarak, şekilde gösterildiği gibi bir yararlılık–tepki eğrisi (utility–response curve) çizebiliriz. Farklı senaryoların her biri için yararlılık–tepki eğrisi çıkarıldıktan sonra, düşünülen çeşitli tasarım alternatifleri ele alınabilir ve bunların beklenen tepki değerleri tahmin edilebilir.

Örneğin, arızaya kadar ortalama süre (mean time to failure) ile ilgileniyorsak üç farklı mimari stratejiyi (örneğin yedeklilik (redundancy) seçeneklerini) düşünebiliriz — örneğin, yedeklilik yok, soğuk yedek (cold spare) ve sıcak yedek (hot spare). Bu stratejilerin her biri için beklenen tepkilerini (yani beklenen arızaya kadar ortalama sürelerini) tahmin edebiliriz. Burada gösterilen grafikte “e”, tahmini tepki ölçümüne göre eğri üzerinde yerleştirilmiş olan bu seçeneklerden birini temsil etmektedir.

Bu tepki tahminleri kullanılarak, her bir mimari stratejinin yararlılık değeri artık interpolasyon (ara değer hesaplama) yoluyla belirlenebilir; bu da beklenen faydasını verir. Her bir mimari stratejinin maliyetleri de ortaya çıkarılır — sıcak yedeğin en maliyetli, onu soğuk yedeğin, onun da ardından yedeklilik olmamasının izlemesi beklenir.

Tüm bu bilgiler ışığında mimari stratejiler, artık maliyete göre beklenen değerlerine dayanarak seçilebilir.

### Şekil: Yararlılık–Tepki Eğrisi

_Şekildeki açıklamalar:_

- b: best (en iyi)
- c: current (mevcut)
- d: desired (arzulanan)
- e: expected (beklenen)
- w: worst (en kötü)

Yararlılık (Utility) ekseninde 0’dan 100’e, tepki (Response) ekseninde ise 1, 2, 3 değerleri boyunca, w (en kötü), c (mevcut), d (arzulanan), b (en iyi) ve e (beklenen) noktaları bir eğri üzerinde gösterilmektedir.

CBAM ilk bakışta göreli olarak karmaşık ve zaman alıcı görünebilse de, bazı tasarım kararlarının maliyetleri, faydaları ve proje zaman çizelgesine etkileri bakımından devasa ekonomik sonuçlar doğurabileceğini göz önünde bulundurmanız gerekir. Bu kararları sadece sezgisel bir yaklaşımla mı, yoksa bu daha rasyonel ve sistematik yaklaşımla mı vereceğinize karar vermelisiniz.

Önceki analiz teknikleri sizi uygun bir seçim yapma konusunda yönlendirmediyse, deneme amaçlı (throwaway) prototipler oluşturmanız ve bunlardan ölçümler toplamanız gerekebilir. Erken aşamada deneme amaçlı prototipler oluşturmak, dışarıdan geliştirilen bileşenlerin seçiminde yardımcı olan yararlı bir tekniktir. Bu tür prototipler genellikle bakım yapılabilirlik veya yeniden kullanım çok fazla gözetilmeden, “hızlı ve biraz da özensiz” biçimde oluşturulur. Bu nedenlerle, deneme amaçlı prototiplerin daha ileri geliştirme için temel olarak kullanılmaması gerektiğini akılda tutmak önemlidir.

Prototip oluşturma, analize kıyasla maliyetli olabilir (kaynaklarımıza göre maliyet oranı 10’a 5 ila 1 arasındadır), ancak bazı senaryolar prototip oluşturmayı güçlü biçimde motive eder. Prototip oluşturup oluşturmayacağınıza karar verirken göz önüne almanız gereken hususlar şunlardır:

- Proje, ortaya çıkan (emerging) teknolojileri mi içeriyor?
- Teknoloji, şirket için yeni mi?
- Seçilen teknolojiyi kullanarak belirli sürücülerin, özellikle kalite niteliklerinin, tatmin edilmesi riskler içeriyor mu (yani tatmin edilip edilemeyeceği anlaşılmamış mı)?
- Seçilen teknolojinin proje sürücülerini tatmin etmek için faydalı olacağını belirli bir kesinlik derecesiyle gösteren, güvenilir içsel veya dışsal bilginin eksikliği var mı?
- Teknolojiyle ilişkili, test edilmesi veya anlaşılması gereken yapılandırma (configuration) seçenekleri var mı?
- Seçilen teknolojinin projede kullanılan diğer teknolojilerle bütünleştirilebileceği (integrate) belirsiz mi?

Bu soruların çoğuna cevabınız “evet” ise, deneme amaçlı bir prototip oluşturmayı ciddi biçimde düşünmelisiniz.

Tasarım kavramlarını (design concept) tanımlayıp seçerken, mimari sürücülerin (architectural driver) parçası olan kısıtları akılda tutmanız gerekir; çünkü bazı kısıtlar belirli alternatifleri seçmenizi engelleyecektir. Örneğin, bir kısıt sistemdeki tüm kütüphane ve çerçevelerin (framework) GPL lisansı kullanmamasını gerektirebilir; dolayısıyla gereksinimlerinize uygun bir çerçeve bulmuş olsanız bile, GPL lisansına sahipse onu göz ardı etmeniz gerekebilir. Ayrıca, önceki yinelemelerde tasarım kavramlarının seçimine ilişkin aldığınız kararların, uyumsuzluklar nedeniyle gelecekte seçebileceğiniz tasarım kavramlarını sınırlayabileceğini akılda tutmanız gerekir. Örneğin, ilk yinelemede kullanım için bir web uygulaması referans mimarisi (web application reference architecture) seçtiyseniz, sonraki bir yinelemede yerel uygulamalar için tasarlanmış bir kullanıcı arayüzü çerçevesini seçemezsiniz.

Son olarak, nitelik temelli tasarım (Attribute-Driven Design, ADD) süreci nasıl yürüteceğinize dair yol gösterse de, uygun tasarım kararları vereceğinizi garanti edemeyeceğini hatırlamanız gerekir. Kapsamlı akıl yürütme ve farklı alternatifleri (sadece akla ilk geleni değil) göz önünde bulundurma, iyi bir çözüm bulma olasılığını artırmanın en iyi yollarıdır. Tasarım sürecinde “analiz yapma” konusunu Bölüm 8’de tartışıyoruz.

## 3.5

Yapıların Üretilmesi
