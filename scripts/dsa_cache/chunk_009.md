web sitesinin “1 kişi-gününden daha az emekle tamamlanıp test edilmesi” — yani tartışmaya yer bırakmayan bir ölçüt.

Dolayısıyla, bir kalite niteliği senaryosunun (quality attribute scenario) kalbinde bir uyarıcının (stimulus) bir tepkiyle (response) eşleştirilmesi vardır. Diyelim ki bir video oyunu geliştiriyorsunuz ve şöyle bir işlevsel gereksiniminiz var: “Kullanıcı <C> düğmesine bastığında oyun görünüm kiplerini değiştirmelidir.” Bu işlevsel gereksinim önemliyse, kalite niteliği gereksinimleriyle ilişkilendirilmelidir. Örneğin:

- Bu işlev ne kadar hızlı olmalıdır?
- Bu işlev ne kadar güvenli olmalıdır?
- Bu işlev ne kadar değiştirilebilir (modifiye edilebilir) olmalıdır?

Bu sorunu ele almak için, bir kalite niteliği gereksinimini bir senaryo ile tanımlarız. Bir kalite niteliği senaryosu, bir sistemden bir uyarıcıya karşı nasıl yanıt vermesinin beklendiğini anlatan kısa bir açıklamadır. Örneğin, az önce verilen işlevsel gereksinimi şöyle açıklayıp not düşebiliriz: “Kullanıcı <C> düğmesine bastığında, oyun görünüm kiplerini < 500 ms içinde değiştirmelidir.” Bir senaryo, bir uyarıcıyı (bu durumda <C> düğmesine basılması) bir yanıtla (görünüm kipinin değiştirilmesi) ilişkilendirir ve bu yanıt bir yanıt ölçütü (response measure) (< 500 ms) ile ölçülür. Tam bir kalite niteliği senaryosu üç bileşen daha ekler: uyarıcının kaynağı (stimulus source) (bu durumda kullanıcı), etkilenen artefakt (artifact) (bu durumda, uçtan uca gecikme ile ilgilendiğimiz için artefakt tüm sistemdir) ve ortam (environment) (normal çalışmada mıyız, başlangıçta mı, bozulmuş modda mı, yoksa başka bir kipte mi?). Toplamda, tamamen iyi tanımlanmış bir senaryonun altı parçası vardır; Şekil 2.2’de gösterildiği gibi.

1  
Uyarıcı  
Uyarıcının  
Kaynağı  

Artefakt  

Tepki  

Ortam  

ŞEKİL 2.2 Bir kalite niteliği senaryosunun altı parçası  

2  
3  
4  

Tepki  
Ölçütü  

### 2.4 Mimari Sürücüler (Architectural Drivers)

Senaryolar, ele alınan sistemin kalite niteliği davranışına ilişkin test edilebilir, yanlışlanabilir hipotezlerdir. Açık tanımlanmış uyarıcı ve tepkileri olduğu için, bir tasarımı senaryoyu ne ölçüde destekleyebildiği açısından değerlendirebiliriz ve bir prototip ya da tam olarak gerçekleştirilmiş sistem üzerinde ölçümler yapıp, senaryoyu pratikte karşılayıp karşılamadığını test edebiliriz. Eğer analiz (ya da prototipleme sonuçları) senaryonun tepki hedefinin karşılanamayacağını gösterirse, hipotez yanlışlanmış sayılır.

Diğer gereksinimlerde olduğu gibi, senaryolar da önceliklendirilmelidir. Bu, her senaryo ile ilişkilendirilen ve önem derecesi atanan iki boyut dikkate alınarak gerçekleştirilebilir:

- Birinci boyut, sistemin başarısı açısından senaryonun önemine karşılık gelir. Bu, müşteri tarafından derecelendirilir.
- İkinci boyut, senaryo ile ilişkili teknik risk derecesine karşılık gelir. Bu, mimar (architect) tarafından derecelendirilir.

Her iki boyutu derecelendirmek için düşük/orta/yüksek (L/M/H) ölçeği kullanılır. Boyutlar derecelendirildikten sonra, (H, H), (H, M) ya da (M, H) birleşimine sahip senaryolar seçilerek senaryolar önceliklendirilir.

Buna ek olarak, bazı geleneksel gereksinim çıkarım (requirements elicitation) teknikleri kalite niteliği gereksinimlerine odaklanacak şekilde hafifçe uyarlanabilir; örneğin Birleşik Gereksinim Planlama (Joint Requirements Planning, JRP), Birleşik Uygulama Tasarımı (Joint Application Design, JAD), keşif amaçlı prototipleme (discovery prototyping) ve hızlandırılmış sistem çözümlemesi (accelerated systems analysis).

Ancak hangi tekniği kullanırsanız kullanın, ölçülebilir kalite niteliklerinin (quality attributes) önceliklendirilmiş bir listesini oluşturmadan tasarıma başlamayın! Paydaşlar (stakeholders) bazen cehaletlerini öne sürebilir (“Ne kadar hızlı olması gerektiğini bilmiyorum; sadece hızlı olsun!”), ancak hemen her zaman en azından olası tepkilerin bir aralığını ortaya çıkarabilirsiniz. Sistemin “hızlı” olması gerektiğini söylemek yerine, paydaşa 10 saniyelik yanıt süresinin kabul edilebilir olup olmadığını sorun. Eğer bu kabul edilemezse, 5 saniye uygun mu, 1 saniye uygun mu diye sorun. Çoğu durumda kullanıcıların, gereksinimleri hakkında fark ettiklerinden daha fazla şey bildiklerini ve en azından onları belirli bir aralığa “sıkıştırabildiğinizi” göreceksiniz.

> **💬 Çevirmen notu:** Burada “yanıt ölçütü” ile kastedilen, kalite niteliğini sayısal olarak ifade eden hedef değerdir; örn. “< 500 ms”, “%99.9 erişilebilirlik”, “8 saatten kısa kurtarma süresi” gibi.

### Kalite Niteliği Çalıştayı (Quality Attribute Workshop) ve Fayda Ağacı (Utility Tree)

#### Kalite Niteliği Çalıştayı (Quality Attribute Workshop, QAW)

Kalite Niteliği Çalıştayı (Quality Attribute Workshop, QAW), kalite niteliği senaryolarını üretmek, önceliklendirmek ve iyileştirmek için kullanılan, kolaylaştırıcılı (facilitated), paydaş odaklı bir yöntemdir. Bir QAW oturumu ideal olarak yazılım mimarisi tanımlanmadan önce gerçekleştirilir; ancak pratikte, QAW’nin yazılım geliştirme yaşam döngüsünün her aşamasında kullanıldığını gördük. QAW, sistem düzeyindeki kaygılara ve özel olarak yazılımın sistemde oynayacağı role odaklanır. QAW’nin adımları şöyledir:

22 Bölüm 2—Mimari Tasarım
