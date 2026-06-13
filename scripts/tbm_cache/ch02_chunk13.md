…bu yöntemin avantajlarıdır. Bu nedenle, insan vücudunun belirli bir bölümünü modelleyerek, yaralanma mekanizmalarının analizi için de kullanılabilir. Ancak, karmaşık bir geometrinin ayrıntılı temsili, muazzam sayıda elemana ve dolayısıyla hesaplanması gereken çok sayıda bilinmeyene yol açar. İlgili malzemelerin doğrusal olmayan anconstitutive özellikleri (nonlinear constitutive properties) ve büyük deformasyonlar söz konusu olduğunda, sonlu eleman (FE, finite element) yöntemine sıklıkla eşlik eden çok yüksek hesaplama maliyeti önemli bir kısıt oluşturur. Paralel işlem (parallel processing) bu noktada yardımcı olabilir. Günümüzde, büyük bilgisayar sistemleri milyonlarca bilinmeyenli FE modellerini (örneğin, ayrıntılı biçimde modellenmiş iki otomobilin yer aldığı uyumluluk testleri simülasyonları için yaklaşık 700.000 eleman) birkaç günlük hesaplama süreleriyle işleyebilmektedir.

Buna karşın, karmaşık kinematik bağlantıları verimli biçimde temsil etme yeteneği, çok cisimli sistemler (MBS, multibody systems) yaklaşımını özellikle cazip kılar. Ayrıca, genellikle sadece nispeten az sayıda sıradan diferansiyel denklem (çoğu zaman rijit/stiff) çözülmesi gerektiğinden, gereken hesaplama süreleri FE hesaplamalarına kıyasla belirgin ölçüde daha kısadır. Bu nedenle MBS’ler, çok sayıda tasarım parametresini içeren optimizasyon çalışmalarına oldukça uygun olduklarından, tasarım araçları olarak geniş ölçüde kullanılmaktadır.

İnsan vücudu modellemesi açısından, her iki tekniğin de başa çıkması gereken genel sorunlar ortaya çıkar. Canlı insan dokusunun malzeme davranışını tanımlamak için kullanılacak parametrelerin seçimi, canlı dokuların deformasyon özelliklerine ilişkin deneysel verilerin bulunabilirliğini gerektirir. Böyle veriler neredeyse hiç mevcut değildir; mevcut olduklarında ise, bir taraftan genel biyolojik değişkenlik, diğer taraftan da anconstitutive testleri için seçilen özel deneysel yöntemin kısıtları nedeniyle, sıklıkla büyük belirsizliklerle ilişkilidir. Ayrıca, özellikle çeşitli farklı çarpma koşullarında kullanılmak üzere tasarlanan insan vücudu modellerinin geçerliliğinin (validation) sağlanması kritik önemdedir; ancak bu, karmaşık bir görev olmaya devam etmektedir.

Sonuç olarak, her iki metodoloji de genel darbe/çarpma (impact) ve yaralanma analizleri alanında makul biçimde kullanılabilir. Amaca bağlı olarak ya en uygun tekniğin seçilmesi ya da her iki yöntemin birlikte kullanımının düşünülmesi gerekir. Böyle entegre (veya hibrit) bir yaklaşımın bir örneği, bir araç yolcusunun açılmakta olan bir hava yastığı (airbag) ile etkileşiminin simülasyonlarında görülür. Bu durumda hava yastığını modellemek için bir FE modeli kullanılırken, insan bir MBS (metinde MRS olarak geçiyor; muhtemelen multibody system) ile temsil edilir. Başka çeşitli çalışmalarda da, örneğin bir buz hokeyi oyuncusunun sahanın çevre duvarına (rink board) çarpması durumunda olduğu gibi, kaba hareketi (gross motion) modellemek üzere bir MBS kullanılırken, tekil yapıların ayrıntılı analizi için FE modelleri dahil edilmektedir. Günümüzde sayısal modeller, emniyet tertibatlarının geliştirme sürecinin hemen her aşamasına dahil edilmektedir.

Yaygın ve hızla artan simülasyon tekniği kullanımı ve bunların çarpışma testlerinin sayısını (ve buna bağlı maliyetini) azaltma potansiyeline karşın, sayısal simülasyonlar henüz genel araç güvenliği standartlarına dahil edilmemiştir. Bu durum kısmen, genel simülasyon kılavuzlarının ve özellikle kalite kontrolüne ilişkin kılavuzların mevcut olmamasına bağlanabilir. Oysa çarpışma simülasyonlarının güvenlik regülasyonlarına dâhil edilebilmesi için bu tür kılavuzlara ihtiyaç duyulacaktır.

> **💬 Çevirmen notu:** Güncel Euro-NCAP veya UNECE regülasyonlarında dahi, simülasyonlar esas olarak destekleyici araçlar olup, hukuken bağlayıcı değerlendirme hâlâ fiziksel tam ölçekli çarpışma testlerine dayanmaktadır. Türkiye’de araç tip onayı süreçlerinde de benzer bir yaklaşım geçerlidir.

---

## 2.7 Kaynaklar (References)

AAAM (2005): AIS 2005: The injury scale (Editörler: Gennarelli T ve Wodzin E),  
Association for the Advancement of Automotive Medicine

> **💬 Çevirmen notu:** AIS (Abbreviated Injury Scale, Kısaltılmış Yaralanma Ölçeği) adli tıp ve travma cerrahisinde yaralanma şiddetini standartlaştırmak için yaygın kullanılan bir skordur. Türkiye’de Adli Tıp Kurumu raporlamalarında da referans alınabilmektedir.

AAAM (2001): The Abbreviated Injury Scale, 1990 version/update 98, Association  
of Advancement of Automotive Medicine

Appel H, Krabbel G, Vetter D (2002): Unfallforschung, Unfallmechanik und  
Unfallrekonstruktion, Verlag Information Ambs GmbH, Kippenheim, Germany

Baker S, O'Neill B (1976): The injury severity score: an update, J Trauma, Cilt 11,  
ss. 882-885

Bathe K (1996): Finite Element Procedures; Prentice-Hall Inc.; Upper Saddle  
River; New Jersey 07458

Campbell F, Woodford M, Yates D (1994): A comparison of injury impairment scale  
scores and physician's estimates of impairment following injury to the head,  
abdomen and lower limbs, Bildiri, 38. AAAM Konferansı

Carsten O, Day J (1988): Injury priority analysis; NHTSA Technical Report DOT  
HS 807 224

Comptom C (2002): The use of public crash data in biomechanical research, in  
Accidental Injury – Biomechanics and Prevention (Editörler: Nahum, Melvin),  
Springer Verlag, New York

Damm R, Schnottale B, Lorenz B (2006): Evaluation of the biofidelity of the  
WorldSID and the ES-2 on the basis of PMHS data, Bildiri, IRCOBI Konferansı,  
ss. 225-237

> **💬 Çevirmen notu:** PMHS (Post Mortem Human Subjects, ölüm sonrası insan kadavraları) verileri, antropomorfik test cihazlarının (ATD, crash test dummy) biyofidelitesini değerlendirmek için altın standart kabul edilir.

DSD (2000): PC-Crash, Dr. Steffan Datentechnik, Linz, Austria

Denton ATD Inc., Milan, USA

ESI (1998): Engineering Systems International S.A.; 20 rue Saarinen, 94578  
Rungis Cedex; France, http://www.esi.fr

EDC (2006): http://www.edccorp.com/products/edcrash3.html

Ewing C ve ark. (1978): Dynamic response of human and primate head and neck to  
+Gy impact acceleration, Rapor DOT HS-803 058

Gesac Inc., Boonsboro, USA

IBB (2002): Carat 4.0, Ibb-Informatik, Mülheim/Mosel, Germany

ISO WorldSID Task Group, http://www.worldsid.org

Iwamoto M, Kisanuki Y, Watanabe I, Furusu K, Miki K, Hasegawa J (2002):  
Development of a finite element model of the total human model for safety  
(THUMS) and application to injury reconstruction, Bildiri, IRCOBI Konferansı,  
ss. 31-42

Kramer F (1998/2006): Passive Sicherheit von Kraftfahrzeugen, Vieweg Verlag,  
Braunschweig, Germany

Livermore (1999): Livermore Software Tech. Corp, http://www.lstc.com

Malliaris A (1985): Harm causation and ranking in car crashes; SAE paper No.  
85090

Mecalog (2000): Radioss, Mecalog Sarl, France, http://www.radioss.com

Muser M, Zellmer H, Walz F, Hell W, Langwieder K (1999): Test procedure for the  
evaluation of the injury risk to the cervical spine in a low speed rear end  
impact, Proposal for the ISO/TC22 N 2071 / ISO/TC22/SC10 (collision test  
procedures), http://www.agu.ch

Ono K, Kaneoka K (1997): Motion analysis of human cervical vertebrae during  
low speed rear impacts by the simulated sled, Bildiri, IRCOBI Konferansı, ss. 223-237

Schmitt K-U, Muser M, Vetter D, Walz F (2003a): Whiplash injuries: cases with a  
long period of sick leave need biomechanical assessment, European Spine,  
Springer Verlag’te çevrimiçi yayımlanmış, basılı versiyon baskıda.

Schmitt K-U, Beyeler F, Muser M, Niederer P (2003b): A visco-elastic foam as  
head restraint material – experiments and numerical simulations using a  
BioRID model, Traffic Injury Prevention, gönderilmiş (submitted)

Schmitt K-U, Muser M, Walz F, Niederer P (2002): On the role of fluid-structure  
interaction in the biomechanics of soft tissue neck injuries; Traffic Injury  
Prevention; Cilt 3 (1), ss. 65-73

Spitzer W, Skovron M, Salmi L, Cassiy J, Duranceau J, Suissa S, Zeiss E (1995):  
Scientific Monograph of the Quebec Task Force on Whiplash Associated  
Disorders: Redefining “whiplash” and its management, Spine, Cilt 20(85), ss. 3-73

> **💬 Çevirmen notu:** Quebec Task Force raporu, whiplash ilişkili bozuklukların (WAD, whiplash associated disorder) tanımı, sınıflaması ve tedavi yaklaşımlarını köklü biçimde tartışan temel referanslardandır.

TNO (2001): Madymo V6.0, TNO Automotive, Delft, The Netherlands

Verriest J, Chapon A, Trauchesse R (1981): Cinephotogrammetrical study of  
porcine thoracic response to belt applied load in frontal impact: comparison  
between living and dead subjects, SAE paper No. 811015

Wismans J (1994): Injury Biomechanics, ders notları, Eindhoven University of  
Technology, The Netherlands

Zeidler F, Pletschen B, Mattem R, Alt B, Miksch T, Eichendorf W, Reiss S (1989):  
Development of a new injury cost scale; Bildiri, 33. Yıllık AAAM Konferansı

Zienkiewicz O, Taylor R (1994): The Finite Element Method; McGraw-Hill Book  
Company; London; ISBN 0-07-084175-6
