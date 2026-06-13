Öğe diyagramı, öğenin sorumluluklarını tanımlayan bir tabloyla tamamlanır:

| Öğe          | Sorumluluk |
|-------------|------------|
| Veri akışı  | Bu öğe, tüm veri kaynaklarından gerçek zamanlı olarak veri toplar ve işlenmek üzere hem yığın katmanına (batch layer) hem de hız katmanına (speed layer) gönderir. |
| Yığın katmanı (batch layer) | Bu katman, ham veriyi depolamaktan ve sunum katmanında (serving layer) saklanacak yığın görünümlerini (batch views) önceden hesaplamaktan sorumludur. |
| ...         | ...        |
| ...         | ...        |

**ŞEKİL 3.5** Örnek ön taslak (preliminary) dokümantasyon

## 3.7 Tasarım Sırasında Ön Taslak Dokümantasyon Oluşturma

Elbette, her şeyi dokümante etmek gerekli değildir. Dokümantasyonun üç amacı vardır: analiz, inşa (construction) ve eğitim. Tasarım yaparken, bir dokümantasyon amacı seçmeli ve ardından risk azaltma (risk mitigation) kaygılarınıza göre bu amacı yerine getirecek şekilde dokümantasyon yapmalısınız. Örneğin, mimari tasarımınızın karşılaması gereken kritik bir kalite niteliği senaryonuz (quality attribute scenario) varsa ve bu gereksinimin bir analizde sağlandığını kanıtlamanız gerekecekse, analizin tatmin edici olabilmesi için ilgili bilgileri dikkatle dokümante etmelisiniz. Alternatif olarak, yeni ekip üyelerini eğitmek zorunda kalacağınızı öngörüyorsanız, sistemin bir bileşen-ve-bağlayıcı (C&C, component-and-connector) görünümünün bir taslağını hazırlamalı; bu taslak, sistemin nasıl çalıştığını ve öğelerin çalışma zamanında nasıl etkileşim kurduğunu göstermeli ve belki de sistemin en azından ana katmanlarını veya alt sistemlerini gösteren kaba bir modül görünümü oluşturmalısınız. Son olarak, dokümantasyon yaparken, tasarımınızın bir gün analiz edilebileceğini akılda tutmak iyi bir fikirdir. Bu nedenle, hangi bilgilerin bu analizi desteklemek için dokümante edilmesi gerektiği hakkında düşünmeniz gerekir (bkz. “Senaryo-Temelli Dokümantasyon” kenar notu).

### Senaryo-Temelli Dokümantasyon

Bir mimari tasarımın analizi, en önemli kullanım durumlarınıza (use case) ve kalite niteliği senaryolarınıza dayanır. Basitçe ifade edersek, bir senaryo seçilir ve siz, mimarinin bu senaryoyu nasıl desteklediğini ve kararlarınızı gerekçelendirerek açıklamak zorundasınız. Tasarım yaparken analize hazırlanmaya başlamak için, bir senaryonun karşılanmasına dahil olan öğeleri içeren yapıları üretmek ve bunları dokümante etmek yararlıdır. Tasarım süreci senaryolar tarafından yönlendirildiği için bu durum doğal olarak ortaya çıkmalıdır; ancak bu noktayı aklınızda sıkıca tutmak her zaman yardımcı olur.

Tasarım süreci sırasında, en azından aşağıdaki öğeleri tek bir belgede yakalamaya çalışmalısınız:

- Birincil sunum: Ürettiğiniz yapıyı temsil eden diyagram  
- Öğelerin sorumlulukları tablosu: Yapıda yer alan öğelerin sorumluluklarını kaydetmenize yardımcı olur  
- İlgili tasarım kararları ve bunların gerekçeleri (bkz. Bölüm 3.7.2)

Ayrıca iki tür ek bilgiyi de yakalayabilirsiniz:

- Öğelerin etkileşiminin çalışma zamanı gösterimi—for example, bir sıralama diyagramı (sequence diagram)
- İlk arayüz (interface) tanımları (bunlar ayrı bir belgede de tutulabilir)

Görüldüğü gibi, bu bilgilerin tümü tasarım sürecinin bir parçası olarak üretilmelidir. Her durumda, sistemde hangi öğelerin bulunacağına ve bunların nasıl etkileşim kuracağına karar vermeniz gerekir. Tek soru, bu bilgileri yazıya dökme zahmetine girip girmeyeceğiniz, yoksa tek temsilinin kodda mı kalacağıdır.

Burada savunduğumuz yaklaşımı izlerseniz, tasarımın sonunda elinizde, her biri belirli bir senaryoyla ilişkilendirilmiş, dokümante edilmiş bir dizi ön taslak görünüm (preliminary view) olacaktır ve bu dokümantasyona az bir maliyetle sahip olursunuz. Bu ön taslak dokümantasyon, tasarımı analiz etmek için, özellikle de senaryo-temelli değerlendirmeler yoluyla, olduğu gibi kullanılabilir.

## 3.7.2 Tasarım Kararlarının Kaydedilmesi

Her tasarım yinelemesinde, yineleme hedefinize ulaşmak için önemli tasarım kararları alırsınız. Daha önce gördüğümüz gibi, bu tasarım kararları şunları içerir:

- Birden fazla alternatif arasından bir tasarım kavramı (design concept) seçmek  
- Seçilen tasarım kavramını örnekleyerek (instantiate ederek) yapılar oluşturmak  
- Öğeler arasında ilişkiler kurmak ve arayüzler tanımlamak  
- Kaynakları tahsis etmek (örneğin, insanlar, donanım, hesaplama)  
- Diğerleri  

Bir mimariyi temsil eden bir diyagramı incelediğinizde, bir düşünme sürecinin nihai ürününü görürsünüz; ancak bu sonuca ulaşmak için hangi kararların alındığını anlamak kolay olmayabilir. Seçilen öğeler, ilişkiler ve özelliklerin temsilinin ötesinde tasarım kararlarını kaydetmek, sonuca nasıl ulaştığınızı anlamaya yardımcı olması açısından temeldir: buna tasarım gerekçesi (design rationale) denir.

Yineleme hedefiniz belirli bir kalite niteliği senaryosunu karşılama ile ilgili olduğunda, aldığınız bazı kararlar, senaryonun tepki ölçütünü (response measure) karşılama yeteneğinizde önemli roller oynar. Dolayısıyla, bunlar kaydetme konusunda en çok özen göstermeniz gereken kararlardır. Bu kararları kaydetmelisiniz; çünkü bunlar, önce oluşturduğunuz tasarımın analizini kolaylaştırmak, sonra uygulamayı kolaylaştırmak ve daha sonra (örneğin bakım sırasında) mimarinin anlaşılmasını desteklemek açısından gereklidir. Ayrıca her tasarım kararı “yeterince iyi”dir, ama nadiren optimumdur; bu nedenle alınan kararları gerekçelendirmeli ve muhtemelen kalan riskleri daha sonra yeniden ele almalısınız.

Tasarım kararlarını kaydetmenin sıkıcı bir iş olduğunu düşünebilirsiniz. Gerçekte, geliştirilen sistemin kritikliğine bağlı olarak kaydedilen bilgi miktarını ayarlayabilirsiniz. Örneğin, asgari bilgi kaydetmek için, Tablo 3.2’de gösterilen gibi basit bir tablo kullanabilirsiniz. Bu asgari düzeyden daha fazlasını kaydetmeye karar verirseniz, aşağıdaki bilgiler yararlı olabilir:

- Kararları gerekçelendirmek için hangi kanıtlar üretildi?  
- Kim ne yaptı?  
- Neden kestirmeler (shortcuts) kullanıldı?  

> **Tablo 3.2 Tasarım Kararlarını Dokümante Etmek İçin Örnek Tablo**

| Sürücü (Driver) | Tasarım Kararları ve Yeri | Gerekçe ve Varsayımlar |
|-----------------|---------------------------|------------------------|
| QA-1            | TimeServerConnector ve FaultDetectionService içinde eşzamanlılık (concurrency) tanıtılması (taktik, tactic) | Birden fazla olayı (tuzak, trap) aynı anda alıp işleyebilmek için sistemde eşzamanlılık tanıtılmalıdır. |
| QA-2            | İletişim katmanında bir mesaj kuyruğu (message queue) tanıtımı yoluyla mesajlaşma deseni (messaging pattern) kullanımı | ...  <br><br>Mesaj kuyruğu kullanımı senaryonun dayattığı performansa aykırı gibi görünse de, bazı mesaj kuyruğu gerçekleştirimleri yüksek performansa sahiptir ve ayrıca bu, QA-3’ü desteklemeye yardımcı olacaktır. <br>... |

- Neden ödünleşimler (tradeoff) yapıldı?  
- Hangi varsayımları yaptınız?  

Ve tıpkı öğeleri tanımlarken onların sorumluluklarını kaydetmenizi önerdiğimiz gibi, tasarım kararlarını da aldığınız anda kaydetmelisiniz. Bunun nedeni basittir: Eğer bu işi sonraya bırakırsanız, neden belirli şeyleri o şekilde yaptığınızı hatırlamayabilirsiniz.
