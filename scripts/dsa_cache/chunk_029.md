Bu bölümde, nitelik temelli tasarım (Attribute-Driven Design, ADD) yönteminin 3.0 sürümüne dair ayrıntılı bir örnek yürütme sunduk. Ayrıca, tasarım sürecinin çeşitli adımlarında dikkate alınması gereken birkaç önemli yönü tartıştık. Bu yönler arasında bir backlog’un kullanılması, olası farklı tasarım yol haritaları (greenfield, brownfield ve yeni/alışılmamış bağlamlar için), tasarım kavramlarının tanımlanması ve seçilmesi ve bunların yapıları üretmek için kullanılması, arayüzlerin tanımlanması ve ön dokümantasyonun üretilmesi yer alır.

Genel mimari geliştirme yaşam döngüsü, mimarinin belgelenmesini ve analiz edilmesini tasarım faaliyetlerinden ayrı etkinlikler olarak içerse de, bu etkinliklerin net bir biçimde ayrılmasının yapay ve zararlı olduğunu savunduk. Ön dokümantasyon ve analiz etkinliklerinin, tasarım sürecinin ayrılmaz parçaları olarak düzenli bir biçimde gerçekleştirilmesi gerektiğini vurguluyoruz.

4., 5. ve 6. bölümlerde, ADD 3.0’ı bir dizi genişletilmiş örnek üzerinden somutlayacak, yöntemin hem greenfield hem de brownfield bağlamlarda gerçek dünyada nasıl çalıştığını göstereceğiz.

## 3.10 Ek Okumalar

ADD 3.0’ın bazı kavramları ilk kez şu IEEE Software makalesinde tanıtılmıştır:  
H. Cervantes, P. Velasco ve R. Kazman, “A Principled Way of Using Frameworks in Architectural Design”, IEEE Software, 46–53, Mart/Nisan 2013.

ADD’nin 2.0 sürümü ilk kez şu SEI teknik raporunda belgelenmiştir:  
R. Wojcik, F. Bachmann, L. Bass, P. Clements, P. Merson, R. Nord ve B. Wood, “Attribute-Driven Design (ADD), Version 2.0”, SEI/CMU Technical Report CMU/SEI-2006-TR-023, 2006.

ADD 2.0’ın kullanımına ilişkin genişletilmiş bir örnek şu raporda yer almaktadır:  
W. Wood, “A Practical Example of Applying Attribute-Driven Design (ADD), Version 2.0”, SEI/CMU Technical Report: CMU/SEI-2007-TR-005.

Yazılım mimarilerinin tasarımını desteklemek için bir dizi alternatif yöntem de vardır. Bunlar 7. bölümde daha ayrıntılı biçimde tartışılmakta ve referans verilmektedir.

Bir mimari backlog (architecture backlog) kavramı şu çalışmada ele alınmaktadır:  
C. Hofmeister, P. Kruchten, R. Nord, H. Obbink, A. Ran ve P. America, “A General Model of Software Architecture Design Derived from Five Industrial Approaches”, Journal of Systems and Software, 80:106–126, 2007.

ARID yöntemi (Architecture Review for Intermediate Design) şu kaynakta tartışılmaktadır:  
P. Clements, R. Kazman ve M. Klein, *Evaluating Software Architectures: Methods and Case Studies*, Addison-Wesley, 2002.

CBAM yöntemi (Cost Benefit Analysis Method) şu kaynakta sunulmaktadır:  
L. Bass, P. Clements ve R. Kazman, *Software Architecture in Practice*, 3. baskı, Addison-Wesley, 2013.

Mimarinin nasıl belgelenebileceği konusu, şu kaynakta kapsamlı şekilde ele alınmaktadır:  
P. Clements vd., *Documenting Software Architectures: Views and Beyond*, 2. baskı, Addison-Wesley, 2011. Daha çevik (Agile) dokümantasyon yaklaşımları ise şu kitapta tartışılmaktadır:  
S. Brown, *Software Architecture for Developers*, Lean Publishing, 2015.

Tasarım gerekçesinin (design rationale) yakalanmasının önemi ve zorlukları şu çalışmada tartışılmaktadır:  
A. Tang, M. Ali Babar, I. Gorton ve J. Han, “A Survey of Architecture Design Rationale”, Journal of Systems and Software, 79(12):1792–1804, 2007.

Gerekçenin yakalanmasına yönelik minimalist bir teknik ise şu makalede ele alınmaktadır:  
U. Zdun, R. Capilla, H. Tran ve O. Zimmermann, “Sustainable Architectural Design Decisions”, IEEE Software, 30(6):46–53, 2013.

---

# 4  
Vaka Çalışması: FCAPS Sistemi

Şimdi, olgun bir alanda, greenfield bir sistem için ADD 3.0 kullanımına dair bir vaka çalışması sunacağız. Bu vaka çalışması, üç yinelemeden (iteration) oluşan bir ilk tasarım turunu ayrıntılandırmakta ve gerçek bir örneğe dayanmaktadır. Önce iş bağlamını sunuyor, ardından sistemin gereksinimlerini özetliyoruz. Bunu, ADD yinelemeleri sırasında gerçekleştirilen etkinliklerin adım adım bir özeti izliyor.

## 4.1 İş Senaryosu

2006 yılında, büyük bir telekomünikasyon şirketi, İnternet Protokolü (Internet Protocol, IP) ağını “operatör sınıfı hizmetleri (carrier-class services)” ve daha özelde yüksek kaliteli IP üzerinden ses (voice over IP, VOIP) sistemlerini destekleyecek şekilde genişletmek istedi. Bu hedefe ulaşmanın önemli yönlerinden biri, VOIP sunucularının ve diğer ekipmanların senkronizasyonuydu. Zayıf senkronizasyon, düşük hizmet kalitesi (Quality of Service, QoS), bozulan performans ve mutsuz müşterilerle sonuçlanır. Gerekli senkronizasyon seviyesine ulaşmak için şirket, Ağ Zaman Protokolü’nü (Network Time Protocol, NTP) destekleyen bir zaman sunucuları ağı konuşlandırmak istedi.

Zaman sunucuları, tipik olarak coğrafi bölgelere karşılık gelen gruplar hâlinde organize edilir. Bu bölgeler içinde zaman sunucuları, üst düzeyde konumlandırılan zaman sunucularının alt düzeydekilerin zamanı için referans görevi gördüğü, düzeyler ya da kademeler (strata) hâlinde hiyerarşik olarak düzenlenir.

> **💬 Çevirmen notu:** FCAPS, telekom yönetiminde “Fault, Configuration, Accounting, Performance, Security” alanlarını kapsayan klasik yönetim çerçevesidir; ilerleyen kısımlarda bu bağlam netleşecektir.
