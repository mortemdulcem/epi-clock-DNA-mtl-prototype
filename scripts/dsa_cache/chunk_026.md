### Öğe Etkileşim Tasarımında Arayüzlerin Belirlenmesi

Arayüzleri tanımlamak mimari tasarım sürecinin temel bir parçası olmakla birlikte, mimari tasarım sırasında iç arayüzlerin hepsinin belirlenmediğini fark etmek önemlidir. Mimari tasarım sürecinin bir parçası olarak, tipik olarak birincil kullanım örneklerini (use case) mimari sürücülerin (architectural driver) bir parçası olarak ele alır ve bu birincil işlevselliği diğer sürücülerle birlikte destekleyen öğeleri (genellikle modüller) belirlersiniz. Ancak bu süreç, sistemin tüm kullanım örneklerini desteklemesi için gereken tüm öğeleri ve arayüzleri ortaya çıkarmaz. Bu belirginlik eksikliği kasıtlıdır: Mimari soyutlama ile ilgilidir; dolayısıyla özellikle tasarımın en erken aşamalarında bazı bilgilerin ayrıntı düzeyi daha az önemlidir.

Birincil olmayan kullanım örneklerini destekleyen modüllerin belirlenmesi, çoğu zaman tahmin ya da iş atama amaçları için gereklidir. Arayüzlerinin belirlenmesi, modüllerin ayrı ayrı geliştirilebilmesi ve entegre edilebilmesi ile birim testinin yapılabilmesi için de gereklidir. Bu modül belirleme işi proje yaşam döngüsünün erken safhalarında yapılabilir, ancak büyük tasarımın en başta yapılması (big design up front, BDUF) yaklaşımıyla karıştırılmamalıdır. En fazla, belirli bağlamlarda (örneğin erken tahmin ya da iterasyon planlama gibi) kaçınılması zor olan bir BDUF türüdür.

Bir mimar olarak, sistemin ya da sistemin belirli bir sürümünün tüm kullanım örnekleri kümesini destekleyen modüller kümesini belirleyebilirsiniz; ancak birincil olmayan kullanım örneklerini destekleyen modüllerle ilişkili arayüzlerin belirlenmesi tipik olarak sizin sorumluluğunuzda değildir; zira bu, sizin önemli miktarda zamanınızı gerektirir ve genellikle büyük bir mimari etkisi olmaz. Bizim öğe etkileşim tasarımı (element interaction design) adını verdiğimiz bu görev (bkz. Bölüm 2.2.2), genellikle mimari tasarım sona erdikten sonra, fakat modüllerin (çoğunun) geliştirilmesi başlamadan önce yerine getirilir.

Bu görevin geliştirme ekibinin diğer üyeleri tarafından yerine getirilmesi gerekir, ancak siz bu süreçte kritik bir rol oynarsınız; çünkü bu arayüzlerin sizin oluşturduğunuz mimari tasarıma uyması gerekir. Bir mimar olarak, mimariyi arayüzleri belirlemekten sorumlu mühendislere aktarmalı ve onların mevcut tasarım kararlarının gerekçesini anladıklarından emin olmalısınız.

Bu iletişimi sağlamanın iyi bir yolu, ara tasarımlar için etkin gözden geçirmeler (Active Reviews for Intermediate Design, ARID) yöntemini kullanmaktır. Bu yöntemde, mimari tasarım (ya da onun bir bölümü) bir grup gözden geçiren kişiye sunulur — bu durumda, tasarımı kullanacak mühendislerdir. Tasarım sunumundan sonra, katılımcılar tarafından bir dizi senaryo seçilir. Seçilen senaryolar, gözden geçirenlerin mimaride mevcut öğeleri kullanarak bu senaryoları karşılamaya çalıştıkları alıştırmanın çekirdeğini oluşturur.

Standart ARID’de, arayüzleri belirleme amacıyla gözden geçirenlerden kod ya da sözde kod (pseudo-code) yazmaları istenir. Alternatif olarak, mimar mimariyi sunabilir, birincil olmayan işlevsel bir senaryo seçebilir ve katılımcılardan bu senaryoyu destekleyen bileşenlerin arayüzlerini, sıralama diyagramları (sequence diagram) veya benzeri bir yöntem kullanarak belirlemelerini isteyebilir.

Bu çalışmada mimari tasarımın gözden geçirilmesi gerçeğinin ötesinde, bu yaklaşımın ek faydaları da vardır. Özellikle, tek bir toplantıda mimari tasarım ya da onun bir bölümü tüm ekibe sunulur ve arayüzlerin nasıl tanımlanacağına ilişkin (örneğin ayrıntı düzeyi veya parametre geçirme, veri tipleri, hata/istisna yönetimi gibi konularda) uzlaşmalar sağlanabilir.

### 3.7 Tasarım Sırasında Ön Taslak Dokümantasyon Oluşturma

Bir yazılım mimarisi tipik olarak, mimariyi oluşturan farklı yapıları temsil eden bir dizi görünüm (view) olarak dokümante edilir. Bu görünümlerin biçimsel dokümantasyonu tasarım sürecinin bir parçası değildir. Buna karşın, yapılar (structure) tasarımın bir parçası olarak üretilir. Bu yapıların ve bu yapıları oluşturmanıza yol açan tasarım kararlarının, gayriresmî bir biçimde (örneğin kaba eskizler olarak) bile olsa yakalanması, normal tasarım faaliyetlerinin bir parçası olarak yerine getirilmesi gereken bir görevdir.

#### 3.7.1 Görünümlerin Eskizlerini Kaydetme

Belirli bir tasarım problemini ele almak için seçtiğiniz tasarım kavramlarını somutlaştırarak yapılar ürettiğinizde, bu yapıları genellikle zihninizde üretmez, bunun yerine onların bazı eskizlerini oluşturursunuz. En basit durumda, bu eskizleri bir beyaz tahta, bir flipchart ya da hatta bir kâğıt parçası üzerinde üretirsiniz. Alternatif olarak, bu yapıları çizeceğiniz bir modelleme aracı da kullanabilirsiniz. Ürettiğiniz eskizler, mimariniz için yakalamanız gereken ve gerekirse ileride detaylandırabileceğiniz ilk dokümantasyondur.

Eskizler oluştururken, her zaman UML gibi daha biçimsel bir dil kullanmanız gerekmez. Gayriresmî bir gösterim kullanıyorsanız, en azından sembollerin kullanımında tutarlılığı koruma konusunda dikkatli olmalısınız. Er ya da geç, diyagramlarınıza açıklık sağlamak ve belirsizliği önlemek için bir lejant (legend) eklemeniz gerekecektir.

Yapıları oluştururken, öğelere atadığınız sorumlulukları yazıya dökme disiplinini geliştirmelisiniz. Bunun nedenleri basittir: Bir öğeyi tanımladığınız anda, zihninizde o öğe için bazı sorumlulukları da belirlemiş olursunuz. Bu sorumlulukları o anda yazmak, bunları daha sonra hatırlamak zorunda kalmamanızı sağlar. Ayrıca öğelerinizle ilişkili sorumlulukları zaman içinde yavaş yavaş yazmak, bunların tümünü daha sonra topluca derlemekten daha kolaydır.

Tasarım yaparken bu ön taslak dokümantasyonu hazırlamak belli bir disiplin gerektirir. Ancak faydaları emeğe değer — ileride daha ayrıntılı mimari dokümantasyonu nispeten kolay ve hızlı bir şekilde üretebileceksiniz. Bir beyaz tahta, flipchart ya da PowerPoint slaytı kullanıyorsanız, sorumlulukları dokümante etmenin basit bir yolu, ürettiğiniz eskizin fotoğrafını çekip bunu bir belgeye yapıştırmak ve diyagramda gösterilen her bir öğenin sorumluluklarını özetleyen bir tabloyla birlikte sunmaktır (Şekil 3.5 bir örnek sağlar). Bir bilgisayar destekli yazılım mühendisliği (computer-aided software engineering, CASE) aracı kullanıyorsanız, oluşturduğunuz bir öğeyi seçebilir ve söz konusu öğenin özellikler (properties) sayfasında genellikle bulunan metin alanını, onun sorumluluklarını dokümante etmek için kullanabilir ve ardından dokümantasyonu otomatik olarak üretebilirsiniz.

Bu diyagram, Bölüm 5’teki vaka çalışmasında genel sistem yapısını gösteren bir modül görünümü (module view) eskizini sunmaktadır.

BATCH Katmanı  
Ham Veri  
Depolama  
Veri  
Akışı  
Veri  
Kaynakları  

SERVING Katmanı  
Anlık (Ad Hoc) Görünümler  
Ön-hesaplama  

Anlık (Ad Hoc)  
Toplu Görünümler  

Statik Görünümler  
Ön-hesaplama  

Statik Toplu  
Görünümler  

SPEED Katmanı  
Gerçek Zamanlı  
Görünümler  

Lejant (Legend):  
Katman  
Sınırı  
Öğe  
Sınırı  

Kurumsal  
BI Aracı  

Pano (Dashboard) /  
Görselleştirme  
Aracı  

Veri Akışı  
(yön belirtilmiş)  
Sorgu Sonuçları Akışı  

> **💬 Çevirmen notu:** Buradaki örnek, sıkça “lambda mimarisi” olarak adlandırılan, batch/serving/speed katmanlarından oluşan veri işleme mimarilerini çağrıştırmaktadır; modül görünümü eskizlerinin, böyle yüksek seviyeli yapıları da sergilemesi amaçlanıyor.
