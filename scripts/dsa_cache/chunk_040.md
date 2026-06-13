Bu öğeler, her biri iki alt öğeye ayrılır:

- Ad Hoc Görünümler Ön Hesaplama (Ad Hoc Views Precomputing) ve Ad Hoc Yığın Görünümler (Ad Hoc Batch Views) (UC-4, QA-5)  
- Statik Görünümler Ön Hesaplama (Static Views Precomputing) ve Statik Yığın Görünümler (Static Batch Views) (UC‑3, QA-4, CON-2)

Bu alt bölümlendirmenin gerekçesi, önceki durumda olduğu gibi aynıdır: En uygun desenleri ve teknolojileri seçme konusunda bize daha fazla esneklik sağlar. Sonraki tasarım yinelemelerinde, bu iki kaygıyı eşzamanlı olarak ele alan tek bir yaklaşım keşfedersek, bu öğeleri birleştirmek kolay olacaktır.

Bu yalnızca bir isim değişikliği değildir; aynı zamanda anlamsal bir değişikliktir. QA-7’ye göre sistem en az 60 gün boyunca ham veriyi saklamalıdır. Dolayısıyla daha eski veriler arşivlenebilir ve başka depolama teknolojileri kullanılarak saklanabilir (hatta silinebilir). Ana Veri Kümesi (Master Dataset) daha fazla sorumluluk üstlenir: Hem ham veri depolamasını hem de arşivlenmiş veriyi içerir. Bu durumu basitleştirmek için, arşivlenmiş verinin incelenmesi ele alınmayacaktır.

Bu ilk yinelemede işlevselliği ve arayüzleri tam olarak tanımlamak için genellikle çok erkendir.

### 5.3.2.5 Adım 6: Görünümleri Taslak Olarak Çiz ve Tasarım Kararlarını Kaydet

Şekil 5.4, önceki somutlaştırma tasarım kararlarının sonucunu göstermektedir. Sonraki sayfada başlayan tablo, her bir öğenin sorumluluklarını özetlemektedir.

## 5.3 Tasarım Süreci

BATCH Katmanı  
Ham Veri  
Depolama  
Veri  
Akışı

SERVING Katmanı  
Ad Hoc Görünümler  
Ön Hesaplama

Ad Hoc  
Yığın Görünümler

Statik Görünümler  
Ön Hesaplama

Statik Yığın  
Görünümler

Kurumsal  
BI Aracı

SPEED Katmanı

Veri  
Kaynakları

Gerçek Zamanlı  
Görünümler

Açıklama (Legend):

- Katman Sınırı  
- Öğe Sınırı  
- Gösterge Paneli / Görselleştirme Aracı (Dashboard / Visualization Tool)  
- Veri Akışı (yönü belirtilmiş)  
- Sorgu Sonuçları Akışı

**ŞEKİL 5.4** Lambda mimarisinin somutlaştırılması

| Öğe | Sorumluluk |
| --- | ---------- |
| **Veri Kaynakları (Data Sources)** | Günlükler ve sistem metrikleri üreten web sunucuları (örneğin Apache erişim ve hata günlükleri, Linux sysstat). |
| **Veri Akışı (Data Stream)** | Bu öğe, tüm veri kaynaklarından verileri gerçek zamanlı olarak toplar ve işlenmek üzere hem Batch Katmanı’na hem de Speed Katmanı’na yönlendirir. |
| **Batch Katmanı (Batch Layer)** | Bu katman, ham veriyi depolamaktan ve Serving Katmanı’nda saklanacak yığın görünümleri (batch views) önceden hesaplamaktan sorumludur. |
| **Serving Katmanı (Serving Layer)** | Bu katman, yığın görünümlerini rastgele yazma olmayan, ancak yığın güncellemelerini ve rastgele okumaları destekleyen bir veri deposunda açığa çıkarır; böylece bu görünümler düşük gecikmeli sorgulanabilir. |
| **Speed Katmanı (Speed Layer)** | Bu katman, yığın işlemenin yüksek gecikmesi nedeniyle henüz Serving Katmanı’nda bulunmayan güncel verilere, bir dizi gerçek zamanlı görünüm (real-time views) aracılığıyla erişim sağlar ve bu verileri işler. |
| **Ham Veri Depolama (Raw Data Storage)** | Bu öğe, Batch Katmanı’nın bir parçasıdır ve belirlenmiş bir süre boyunca (QA-7) ham veriyi (değişmez, yalnızca ekleme yapılabilir) depolamaktan sorumludur. |
| **Ad Hoc Görünümler Ön Hesaplama (Ad Hoc Views Precomputing)** | Bu öğe, Batch Katmanı’nın bir parçasıdır ve Ad Hoc Yığın Görünümlerini önceden hesaplamaktan sorumludur. Ön hesaplama, ham veri üzerinde, onu insan-zamanında (human-time) hızlı sorgulamaya uygun bir duruma dönüştüren yığın işlemlerini temsil eder. |
| **Statik Görünümler Ön Hesaplama (Static Views Precomputing)** | Bu öğe, Batch Katmanı’nın bir parçasıdır ve Statik Yığın Görünümlerini önceden hesaplamaktan sorumludur. Ön hesaplama, ham veri üzerinde, onu insan-zamanında hızlı sorgulamaya uygun bir duruma dönüştüren yığın işlemlerini temsil eder. |

---

## Bölüm 5 – Vaka Çalışması: Büyük Veri Sistemi

| Öğe | Sorumluluk |
| --- | ---------- |
| **Ad Hoc Yığın Görünümler (Ad Hoc Batch Views)** | Bu öğe, Serving Katmanı’nın bir parçasıdır ve veri bilimcileri/analistler tarafından yürütülen ad hoc düşük gecikmeli sorgular (QA-5) için optimize edilmiş, önceden hesaplanmış ve birleştirilmiş verileri içerir. |
| **Statik Yığın Görünümler (Static Batch Views)** | Bu öğe, Serving Katmanı’nın bir parçasıdır ve kurumsal bir BI aracı tarafından üretilen önceden tanımlı düşük gecikmeli sorgular (QA-4) için optimize edilmiş, önceden hesaplanmış ve birleştirilmiş verileri içerir. |
| **Gerçek Zamanlı Görünümler (Real-Time Views)** | Bu öğe, Speed Katmanı’nın bir parçasıdır ve işletme ve mühendislik personeli tarafından yürütülen ad hoc, düşük gecikmeli arama sorguları (QA-3) için optimize edilmiş, indekslenmiş günlükleri içerir. |
| **Kurumsal BI Aracı (Corporate BI Tool)** | Bu iş zekâsı aracı, farklı departmanlarda kullanılmak üzere lisanslanmıştır. Araç, SQL arayüzünü (ODBC veya JDBC gibi) destekler ve bu sistem de dâhil olmak üzere birden fazla veri kaynağına bağlanabilir (UC-3, UC-4, CON-2). |
| **Gösterge Paneli / Görselleştirme Aracı (Dashboard / Visualization Tool)** | Operasyon ekibi, çevrimiçi servisleri izlemek, günlüklerdeki önemli mesajları aramak ve potansiyel sorunlara hızlı bir biçimde tepki vermek için bu gerçek zamanlı operasyonel gösterge panelini kullanır (UC-1, UC-2). |

### 5.3.2.6 Adım 7: Geçerli Tasarımın Analizini Yap ve Yineleme Hedefini ve Tasarım Amacının Gerçekleşmesini Gözden Geçir

Bu yinelemede alınan kararlar, tüm sistemin yapısını etkileyen önemli erken aşama hususlarını ele almaktadır. Seçilen referans mimari, tasarım süresini ve çabasını önemli ölçüde tasarruf ettiren, kanıtlanmış bir başlangıç parçalanması (decomposition) ve veri akışı sunduğundan, “boş bir sayfadan” başlamanıza gerek yoktur. Aday teknolojilerin seçilmesi için daha fazla tasarım kararı alınması ve kullanım durumlarının (use case) ve kalite niteliklerinin (quality attribute) nasıl destekleneceğine ilişkin daha fazla detay sağlanması gerekecektir.

Aşağıdaki tablo, Bölüm 3.8.2’de tartışılan Kanban panosu (Kanban board) tekniği kullanılarak tasarım ilerlemesini özetlemektedir.

> **💬 Çevirmen notu:** Kanban panosu burada, her gereksinimin durumunu “ele alınmadı / kısmen / tamamen ele alındı” biçiminde görselleştirmek için kullanılıyor.

|  | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Verilen Tasarım Kararları |
| --- | ----------- | ----------------- | ------------------ | -------------------------------------------- |
| **UC-1** |  | X |  | Gerçek zamanlı verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi gösterge paneli teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **UC-2** |  | X |  | Gerçek zamanlı verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi arama teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **UC-3** |  | X |  | Tarihsel verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi depolama ve sorgu teknolojilerinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |

|  | Ele Alınmadı | Kısmen Ele Alındı | Tamamen Ele Alındı | Yineleme Sırasında Verilen Tasarım Kararları |
| --- | ----------- | ----------------- | ------------------ | -------------------------------------------- |
| **UC-4** |  | X |  | Tarihsel verilere erişim sağlamak için Lambda mimarisi kullanılsın. Hangi depolama ve sorgu teknolojilerinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **UC-5** | X |  |  | Bu kullanım durumu, bu yinelemede birincil olmayan (nonprimary) olarak göz ardı edilmiştir; ancak Lambda mimarisi bunu desteklemektedir ve sonraki yinelemelerde ele alacağız. |
| **UC-6** | X |  |  | Bu kullanım durumu, bu yinelemede birincil olmayan olarak göz ardı edilmiştir; ancak mimari bakış açısından UC-3’e benzerdir. |
| **QA-1** |  | X |  | Veri Akışı (Data Stream) öğesi için potansiyel veri kaynakları belirlenmiştir. Veri akışı öğesi için hangi teknolojilerin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-3** |  | X |  | Gerçek Zamanlı Görünümler (Real-Time Views) öğesi tanımlanmıştır. Hangi depolama ve sorgu teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-4** |  | X |  | Statik Yığın Görünümler (Static Batch Views) öğesi tanımlanmış ve sorumlulukları belirlenmiştir. Hangi depolama teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-5** |  | X |  | Ad Hoc Yığın Görünümler (Ad Hoc Batch Views) öğesi tanımlanmış ve sorumlulukları belirlenmiştir. Hangi depolama ve sorgu teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-6** |  | X |  | Gerçek Zamanlı Görünümler öğesinin sorumlulukları belirlenmiştir. Hangi depolama ve sorgu teknolojisinin kullanılacağına dair ayrıntılı kararlar verilmemiştir. |
| **QA-7** |  |  |  |  |
