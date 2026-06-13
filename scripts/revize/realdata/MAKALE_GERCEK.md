# Madde Bağımlılığında DNA Metilasyonu: Halka Açık Verinin Sistematik Envanteri ve Madde-Özgü Kohortların Yeniden Üretilebilir Yeniden Analizi

> **Bu belge, `scripts/revize/makale.txt` içindeki FABRİKE (uydurma) makalenin gerçek, yeniden
> üretilebilir karşılığıdır.** Buradaki her sayı ya halka açık bir kaynaktan doğrulanmıştır ya
> da bu repodaki sabit-seed'li (seed=42), committed Python betiklerinden üretilmiştir. Yeniden
> üretilemeyen her şey "YAPILAMADI" olarak açıkça beyan edilmiştir (Zero-Hallucination ilkesi).
> Tam denetim izi ve fabrikasyon kanıtı için bkz. `REPORT.md`.

---

**Yazarlar:** [Ad Soyad — ORCID: 0000-0000-0000-0000]¹, […]
**Kurum¹:** [Kurum / Anabilim Dalı]
**Sorumlu yazar:** [e-posta]
**DOI:** [atanacak] · **Makale türü:** Orijinal araştırma (yeniden analiz) ·
**Çalışma kaydı:** retrospektif, halka açık ikincil veri

> Köşeli parantezli alanlar (yazar adı, ORCID, DOI, dergi) henüz **yer-tutucudur**; uydurma kimlik
> yazmamak için bilerek boş bırakılmıştır.

---

## Öz (Structured Abstract)

**Amaç.** Madde bağımlılığının (alkol, kokain, opioid, metamfetamin, esrar) periferik ve beyin
DNA metilasyonu üzerindeki izlerini, **yalnızca halka açık ve birebir doğrulanmış** veriyle,
uçtan uca yeniden üretilebilir bir boru hattıyla değerlendirmek.

**Yöntem.** PRISMA 2020 uyumlu bir envanterle NCBI GEO'da madde + insan + DNA metilasyonu
çalışmaları tarandı. Madde başına bulunabilen en uygun gerçek kohort, ham seri-matris / beta
verisinden başlanarak aynı istatistik protokolüyle (yaş/cinsiyet düzeltmeli doğrusal model +
Benjamini-Hochberg FDR) yeniden analiz edildi. Epigenetik yaş (Horvath, Hannum, PhenoAge),
istatistiksel güç ve sızıntısız (leakage-free) makine öğrenmesi (RandomForest, ElasticNet,
XGBoost + SHAP) eklendi.

**Bulgular.** Tarama 7.859 kayıt tanımladı, 1.295'i tarandı, **117 veri seti** dahil edildi.
Yeniden analiz edilen kohortlarda anlamlı diferansiyel metile CpG (FDR<0.05) sayıları: sigara
(referans) **89**, alkol-kan **4.387** (sigara-karışımlı, keşifsel), alkol-beyin **8**,
kokain-kan **11.987**, metamfetamin-kan **398**, opioid-beyin **12**. Sigarada altın-standart
biyobelirteç **cg05575921 (AHRR)** birinci sırada doğrulandı (p=2,4×10⁻⁵⁵). Kokainde Hannum yaş
ivmesi vaka grubunda anlamlı yüksekti (p=0,021). Sigara sınıflandırmasında XGBoost dengeli
doğruluk 0,923 / duyarlılık 0,864'e ulaştı; SHAP bağımsız olarak yine **AHRR**'yi en bilgilendirici
belirteç seçti.

**Sonuç.** Halka açık veri büyük ölçüde **sigara** ağırlıklıdır; diğer maddeler için kohortlar
**küçük, farklı doku/platformda** ve sıklıkla **sigara ile karışmıştır**. Orijinal makaledeki
"15 set / 10.542 örnek / 7 sınıf / %87,3 doğruluk" kurgusu **yeniden üretilemez**; her madde
ancak kendi sınırlı kohortunda dürüstçe analiz edilebilir.

**Anahtar kelimeler:** DNA metilasyonu, EWAS, madde bağımlılığı, epigenetik saat, yeniden
üretilebilirlik, PRISMA 2020, AHRR.

---

## 1. Giriş

Madde bağımlılığı, çevresel maruziyetin epigenetik düzeyde iz bırakabildiği bir alandır; DNA
metilasyonu, bu izlerin en çok çalışılan biçimidir. Sigara için literatür olgundur ve **AHRR**
geninde (özellikle cg05575921) güçlü, tekrarlanabilir hipometilasyon iyi bilinir. Buna karşın
alkol, kokain, opioid, metamfetamin ve esrar için halka açık metilasyon verisi hem **azdır** hem
de doku/platform bakımından **heterojendir**.

**Bu çalışmanın çıkış noktası özeldir:** elimizdeki ön-makale, hiçbiri repoda bulunmayan veriye
dayanarak birleşik 7-sınıflı bir model ve çok sayıda sayı rapor ediyordu. Atıf verilen 14
accession canlı olarak sorgulandığında **hiçbirinin** iddia edilen veri/sayı olmadığı görüldü
(bkz. `REPORT.md`, Tablo 1). Bu nedenle çalışma, sıfırdan ve **yalnızca doğrulanmış** veriyle
yeniden kurulmuştur.

**Araştırma boşluğu (research gap).** Madde-metilasyon literatüründe (i) tek tek küçük kohort
çalışmaları çoktur, ancak (ii) **maddeler arası, aynı şeffaf protokolle, uçtan uca yeniden
üretilebilir** bir karşılaştırma ve (iii) hangi sonuçların **gerçekten üretilebilir** olduğunun
açıkça beyan edildiği bir envanter eksiktir. Mevcut çalışma tam olarak bu boşluğu doldurur:
PRISMA 2020 envanteri + madde-özgü yeniden analiz + her sayının kaynağının (gerçek veri mi, bizim
hesabımız mı, yoksa yapılamaz mı) açık etiketlenmesi.

---

## 2. Yöntemler

### 2.1 Sistematik envanter (PRISMA 2020)

NCBI E-utilities (esearch/esummary) ile her madde için "insan + DNA metilasyonu" sorguları
çalıştırıldı (`scripts/15_prisma_inventory.py`). Akış: **tanımlama → tarama → uygunluk → dahil
etme** (Bölüm 3.1, Şekil 1). esummary sayfalama (chunk'lar arası kayıt ezilmesi) hatası
düzeltildi. Ham yanıtlar `out/prisma/raw/`, özet `out/prisma/inventory.json`.

### 2.2 Veri kaynakları ve doğrulama

Madde başına bulunabilen en uygun gerçek kohort GEO'dan indirildi; her dosyanın **SHA-256**
özeti `data/manifest.json` içinde sabitlendi. Makalede atıf verilen 14 accession ayrıca canlı
NCBI/EBI/PMC ile doğrulandı (`scripts/11_verify_cited_sources.py`). Bu doğrulama, makalenin
yanlış etiketlediği **iki gerçek madde kaynağını** ortaya çıkardı: GSE49393 (gerçek alkol-beyin)
ve PMC9979153 (gerçek opioid-kan meta-analizi).

Yeniden analiz edilen kohortlar (tümü Illumina 450K, aksi belirtilmedikçe):

| Veri seti | Madde / doku | n | Not |
|---|---|---|---|
| GSE50660 | Sigara / periferik kan | 464 | Referans / yer-gerçeği |
| GSE110043 | Alkol / tam kan | 94 | Sigara-karışımlı (keşifsel) |
| GSE49393 | Alkol / postmortem prefrontal korteks | 48 | 23 AUD / 25 kontrol |
| GSE77056 | Kokain-crack / tam kan | 47 | 23 / 24 |
| GSE154971 | Metamfetamin / periferik kan lenfositi | 24 | 16 / 8; kronolojik yaş yok |
| GSE98203 | Opioid-eroin / postmortem orbitofrontal korteks (nöron çekirdekleri) | 65 | 37 / 28 |
| GSE255929 | Esrar / kan (EPIC-850K) | 93 | Karışımlı → **atıldı** |

### 2.3 Diferansiyel metilasyon (DMP)

Her kohort için β-değer matrisi okundu; mevcut olduğunda **yaş ve cinsiyet** kovaryat olarak
alınarak CpG başına eşit-varyanslı doğrusal model (OLS, limma-eşdeğeri) kuruldu ve **Benjamini-
Hochberg FDR** uygulandı (`scripts/06/07/08/12`). Bu protokol **tek doğruluk kaynağıdır**; aynı
veriye farklı bir test (örn. Welch) uygulamak farklı anlamlı CpG sayısı üreteceğinden, tutarlılık
için tüm rapor `out/*_dmp.csv` tablolarından beslenir. Gen eşleştirmesi resmi Illumina 450K
manifestiyle yapıldı; GO-BP ve KEGG zenginleştirmesi hipergeometrik test + FDR ile hesaplandı
(`scripts/03/09`).

### 2.4 Epigenetik yaş (saatler)

Horvath 2013 (353 CpG), Hannum 2013 (71 CpG) ve PhenoAge/Levine 2018 (513 CpG) saatleri,
katsayıları halka açık depolardan (SHA kayıtlı) alınarak uygulandı (`scripts/05/10/13`). Her
saat kronolojik yaşa karşı Pearson r ve MAE ile doğrulandı; **yaş ivmesi (EAA)** = saatin yaşa
regresyonunun residüeli, vaka/kontrol arasında Welch t ile karşılaştırıldı. GrimAge ve
DunedinPACE, katsayıları kapalı/lisanslı ve/veya R-Bioconductor gerektirdiği için **hesaplanmadı
ve beyan edildi.**

### 2.5 İstatistiksel güç

Her kohortun kendi DMP t-değerlerinden Cohen d tam olarak geri hesaplandı
(d = t·√(1/n₁+1/n₂)); genom-geneli eşik (Bonferroni 0,05/test) altında, gözlenen N'deki güç ve
%80 güç için gerekli örneklem `statsmodels` ile bulundu (`scripts/19_power.py`).

### 2.6 Makine öğrenmesi (sızıntısız)

Yalnızca yeterince büyük tek kohort olan sigara (GSE50660) üzerinde, **güncel vs hiç içmemiş**
ikili sınıflandırması yapıldı. Protokol (`scripts/04`, `scripts/18`): StratifiedKFold (k=5,
seed=42); öznitelik seçimi (top-200 t-test) **her fold'un yalnız eğitim kısmında** yapıldı
(sızıntı yok). Sınıf dengesizliği `class_weight`/`scale_pos_weight` ile yönetildi. Üç model
karşılaştırıldı (RandomForest, ElasticNet-lojistik, XGBoost); SHAP yorumu tam-veri XGBoost
modelinde hesaplandı (yorum amaçlı; tarafsız başarım yine çapraz-doğrulamadan).

Ayrıca **metilasyon → yaş + sigara + madde** çıkarımı için çalışan bir tahmin sistemi kuruldu
(`scripts/20_dlsystem.py`, `21_substance_models.py`, `predict.py`): (i) gerçek çok-katmanlı
sinir ağları (MLP; yaş regresörü gizli=(256,64), sigara sınıflandırıcı gizli=(128,32), ReLU,
Adam, erken-durdurma) GSE50660'ta; (ii) madde-özgü XGBoost sınıflandırıcıları (kokain/alkol/
metamfetamin), fold-içi top-K t-test seçimi ve etikete-kör aday-CpG havuzuyla; (iii) bir metilasyon
beta tablosu alıp uygulanabilen tüm motorları çalıştıran, CpG kapsamını dürüstçe raporlayan bir
çıkarım komut satırı aracı. Tüm modeller `seed=42`, sızıntısız ÇV; `out/dl/models/` altında committed.

### 2.7 Yeniden üretilebilirlik

Tüm betikler `scripts/revize/realdata/scripts/`, çıktılar `out/`, veriler `data/` altında
committed'dır. Sabit seed = 42. Her veri dosyasının SHA-256'sı kayıtlıdır. Her sayısal sonuç,
üreten betiğe ve çıktı dosyasına işaret eder (bkz. `REPORT.md` Bölüm 5).

---

## 3. Bulgular

### 3.1 PRISMA akışı (Şekil 1)

```
TANIMLAMA   GEO/E-utilities sorgularıyla tanımlanan kayıt: 7.859
                │
TARAMA      Madde başına alınıp taranan kayıt: 1.295
                │   (konu-dışı / metilasyon-olmayan / yinelenen elendi)
UYGUNLUK    Uygunluk değerlendirmesi → modaliteye göre:
                │   saat+EWAS 52 · EWAS-dizileme 58 · EWAS-dizi(array) 7
DAHİL       Dahil edilen veri seti: 117
                │   (atıf doğrulamasında bulunan 3 yeni gerçek madde kaynağı dahil)
```

Tam envanter: `out/prisma/inventory.json` (117 kayıt + sorgular + ham önbellek).

### 3.2 Madde-özgü diferansiyel metilasyon

| Madde (kohort, doku) | Test edilen prob | FDR<0,05 CpG | Öne çıkan / not |
|---|---|---|---|
| Sigara (GSE50660, kan) — **referans** | ~450K | **89** | cg05575921 **AHRR** #1, p=2,4×10⁻⁵⁵; kanonik sigara CpG'leri en üstte |
| Alkol (GSE110043, kan) | ~450K | **4.387** | **sigara-karışımlı**, yalnız cinsiyet düzeltmesi → keşifsel |
| Alkol (GSE49393, beyin PFC) | 430.407 | **8** | en üst cg00393248 Δβ=+0,051 p=9,3×10⁻⁸; sigaradan **temiz** |
| Kokain (GSE77056, kan) | 485.577 | **11.987** | KEGG'de 14 yolak FDR<0,05 |
| Metamfetamin (GSE154971, kan) | ~450K | **398** | yalnız cinsiyet düzeltmeli (yaş yok) |
| Opioid (GSE98203, beyin OFC) | 456.513 | **12** | AHRR anlamsız → sigaradan **temiz**; GO sinaptik ama tek-gen kırılgan |

**Zenginleştirme (dürüst):** sigarada GO-BP'de 2, KEGG'de 0 (51 genle güç düşük); kokainde
KEGG'de 14 yolak (geniş listeyle temkinli); opioid-beyin ve alkol-beyinde GO/KEGG terimleri
**tek-gen örtüşmeyle** sürüklendiği için biyolojik tema güçlü ama istatistiksel olarak
kırılgan/düşündürücü olarak işaretlendi. Metamfetaminde GO/KEGG'de anlamlı terim yok (n=24).

**Tamamlayıcı opioid-kan kanıtı (bizim değil, yayının):** PMC9979153 (Epigenomics
2022;14(23):1479-1492, PMID 36700736) opioid-kan meta-analizinde 282 kullanıcı / 10.560 kontrol,
6 CpG (KIAA0226/RUBCNL, CPLX2, TDRP, RNF38, TTC23, GPR179). Ham veri tek set olmadığından
yeniden hesaplanamaz; yalnızca kaynak gösterilir.

### 3.3 Epigenetik saatler ve yaş ivmesi

| Kohort (doku) | Horvath r / MAE | Horvath EAA p | Hannum r/MAE · p | PhenoAge r/MAE · p |
|---|---|---|---|---|
| Sigara (kan) | 0,77 / 3,5y | 0,24 (null) | 0,80 / 7,8y · 0,352 | 0,75 / 6,8y · **0,051**↑ |
| Kokain (kan) | 0,435 / 12,3y | 0,57 (null) | 0,57 / 14,7y · **0,021**↑ | 0,63 / 5,5y · 0,924 |
| Alkol (beyin) | 0,796 / 6,5y | 0,29 (null) | 0,46 / 17,1y · 0,580 | 0,38 / 47,5y · 0,546 |
| Opioid (beyin) | 0,906 / 10,8y | 0,18 (null) | 0,80 / 16,3y · 0,207 | 0,71 / 65,8y · 0,715 |
| Metamfetamin (kan) | — | — | — | — (GEO'da kronolojik yaş **yok** → saat doğrulanamaz) |

İki gerçek pozitif sinyal: **kokain**de Hannum yaş ivmesi vaka grubunda anlamlı yüksek
(p=0,021); **sigara**da PhenoAge yaş ivmesi sınırda yüksek (p=0,051). Diğerleri **null** olarak
dürüstçe raporlandı. Kan-eğitimli Hannum/PhenoAge beyin dokusunda daha zayıf; pan-doku Horvath
beyinde daha iyi (r=0,80–0,91) — bu, saatlerin doku-spesifikliğinin gerçek yansımasıdır.

### 3.4 İstatistiksel güç

| Kohort | medyan Cohen d (anlamlı CpG) | %80 güç için N/grup |
|---|---|---|
| Metamfetamin | 2,60 | 15 |
| Alkol-beyin | 1,71 | 32 |
| Opioid-beyin | 1,42 | 22 |
| Kokain-kan | 1,26 | 33 |
| Sigara-kan | 1,21 | 27 |

Genom-geneli eşik (~10⁻⁷) çok katı olduğundan bu küçük keşif kohortları yalnız **büyük etkiler**
(d>1,2) için yeterince güçlüdür; medyan etki için %80 güç grup başına 15–33 örnek gerektirir →
**doğrulama (replikasyon) kohortu şarttır.**

### 3.5 Makine öğrenmesi (sigara, sızıntısız)

| Model | ROC-AUC | Dengeli doğruluk | Duyarlılık | Özgüllük |
|---|---|---|---|---|
| RandomForest | 0,950 | 0,565 | 0,136 | 0,994 |
| ElasticNet (L1/L2) | 0,821 | 0,702 | 0,409 | 0,994 |
| **XGBoost** | 0,928 | **0,923** | **0,864** | 0,983 |

RandomForest yüksek AUC'ye rağmen dengesizlik nedeniyle gerçek duyarlılığı çok düşüktür (0,136) —
AUC'nin tek başına neden yanıltıcı olduğunun kanıtı. `scale_pos_weight`'li **XGBoost** gerçek
kullanışlı modeldir. RandomForest için permütasyon testi şans-üstü doğruladı (p=0,016). **SHAP**,
tam-veri XGBoost modelinde en bilgilendirici belirteç olarak yine **cg05575921 (AHRR)**'yi seçti
(ardından cg21566642, cg06126421) — modelin gürültü değil **gerçek biyoloji** öğrendiğinin
bağımsız doğrulaması.

**Çoklu-madde 7-sınıf sınıflandırma yapılamadı:** farklı platform/doku/çok küçük n nedeniyle
birleşik model **imkânsızdır** (açık beyan).

### 3.6 Tahmin sistemi: derin ağlar, madde sınıflandırıcıları ve çıkarım

Makalenin uydurma "ensemble ML, MAE 2,1 yıl, R²=0,96" ve çoklu-madde tahmin iddialarının gerçek,
çalışan karşılığı kuruldu: **metilasyon girer → epigenetik yaş + sigara + madde durumu çıkar.**

**(a) Derin sinir ağları (MLP, GSE50660, n=201).** Sıfırdan eğitilen gerçek çok-katmanlı
perceptron'lar:

| Görev | Mimari | Dürüst OOF başarım |
|---|---|---|
| Yaş regresörü (derin) | MLP (256,64) | MAE = 5,40 yıl; r = 0,38; R² = 0,04 |
| Sigara sınıflandırıcı (derin) | MLP (128,32) + oversample | AUC = 0,72; dengeli doğr. = 0,56 |

n=201, dar yaş aralığı (40–65) ve sigara-optimize özniteliklerle sıfırdan derin ağ, **doğrulanmış
Horvath saatini** (r=0,77; MAE=3,5y; §3.3) ve **XGBoost'u** (AUC=0,928; §3.5) **geçemedi** — küçük
veride derin öğrenmenin klasik yöntemlerin gerisinde kaldığının dürüst bir kanıtıdır. Bu nedenle
dağıtılan çıkarım motoru birincil olarak **Horvath saati (yaş) + XGBoost (sigara)** kullanır; MLP'ler
derin-öğrenme kıyas modeli olarak raporlanır.

**(b) Madde-özgü sınıflandırıcılar** (sızıntısız StratifiedKFold-5, fold-içi top-K t-test, XGBoost):

| Madde | Kohort (doku) | n (vaka/kontrol) | OOF ROC-AUC | Dengeli doğr. |
|---|---|---|---|---|
| Kokain | GSE77056 (kan) | 47 (23/24) | **1,00** | 0,979 |
| Alkol | GSE110043 (kan) | 94 (47/47) | 0,926 | 0,894 |
| Metamfetamin | GSE154971 (PBL) | 24 (16/8) | 0,922 | 0,813 |

**Modellenmeyenler (açık beyan, uydurulmadı):** opioid (GSE98203, yalnız 12 DMP) ve alkol-beyin
(GSE49393, 8 DMP, postmortem) için güvenilir sınıflandırıcı kurulmadı — küçük n ile başarım yanıltıcı
olurdu. Kokain AUC=1,00, küçük örneklemde (n=47) ayrılabilirliği gösterir ama dış doğrulama gerektirir.

**(c) Çıkarım aracı** (`predict.py`). Bir metilasyon beta tablosu alır, uygulanabilen tüm motorları
çalıştırır ve her motor için **CpG kapsamını** dürüstçe raporlar. Seri-matristen çıkarılan iki gerçek
GSE50660 örneğinde uçtan uca doğrulandı: sigara içen GSM1225377 (kronolojik 50) → Horvath 54,1 y
(+4,1), XGBoost sigara %89,9 → "güncel"; hiç içmeyen GSM1225378 (kronolojik 56) → Horvath 56,9 y
(+0,87), XGBoost sigara %0,2 → "hiç" — ikisi de doğru. **Kohortlar-arası uyarı:** madde modelleri
yalnız kendi kohortunda doğrulanmıştır; başka kohorta uygulanan madde olasılıkları batch/platform
etkileriyle karışır → **göstergeseldir, tanısal değildir** (araç çıktısında otomatik beyan edilir).

---

## 4. Tartışma

Bulgular tutarlı bir tabloyu destekler: (i) **sigara** sinyali hem güçlü hem tekrarlanabilirdir
ve AHRR'yi hem klasik EWAS'ta (#1, p=2,4×10⁻⁵⁵) hem de bağımsız olarak SHAP'ta yeniden bulmamız
boru hattının doğruluğunu kanıtlar; (ii) **kan** kohortlarındaki büyük CpG sayıları (alkol-kan
4.387, kokain 11.987) önemli ölçüde **sigara karışımını** yansıtabilir, çünkü madde kullanan
gruplarda sigara içiciliği yüksektir ve bu kohortlarda sigara için tam düzeltme yapılamadı; (iii)
buna karşın **beyin** kohortları (alkol-beyin, opioid-beyin) küçük ama **sigaradan temiz** ve
nöronal/sinaptik temalı sinyaller verir. Epigenetik yaş tarafında tek tutarlı sinyal kokainde
Hannum ivmesidir; geri kalan EAA karşılaştırmaları null'dur ve abartılmamalıdır.

En önemli kavramsal sonuç şudur: madde-metilasyon alanında halka açık veri **dengesizdir** —
nicelik sigaradadır, diğer maddeler küçük ve heterojendir. Bu nedenle "tek büyük birleşik model"
anlatısı (ön-makalenin yaptığı gibi) veriyle **desteklenemez**; alanın dürüst hali, madde-madde,
doku-doku, küçük-kohort gerçekliğidir.

## 5. Sınırlılıklar

1. **R/Bioconductor yok:** ham IDAT→β normalizasyonu (minfi/SeSAMe), GrimAge ve DunedinPACE
   hesaplanamadı; yayımlanmış β/seri-matris verisi kullanıldı, bu saatler beyan edilerek atlandı.
2. **Küçük kohortlar:** kokain (47), meth (24), alkol-beyin (48), opioid-beyin (65) — güç
   analizinin gösterdiği gibi yalnız büyük etkiler için güçlü; replikasyon gerekir.
3. **Sigara karışımı:** kan kohortlarında (özellikle alkol-kan) sigara için tam düzeltme
   yapılamadı; bu listeler keşifseldir.
4. **Doku karışıklığı:** kan ve postmortem beyin kohortları doğrudan birleştirilemez; saat
   doku-spesifikliği sonuçları etkiler.
5. **Metamfetaminde kronolojik yaş yok:** epigenetik yaş doğrulanamadı.
6. **Esrar:** uygun temiz kohort bulunamadı; kendi alt-kohort analizimiz karışımlı çıkıp atıldı,
   yerine yayımlanmış sayılar (BMC Pulm Med 2025, PMID 40205553) yalnız kaynak olarak verildi.
7. **GSE66348 (sıçan, NAc):** MeDIP modalitesi β-dizisi olmadığından dizi-tabanlı boru hatta
   uymadı; dışlandı.

## 6. Sonuç

Madde bağımlılığı epigenetiği, halka açık veriyle **dürüstçe** ancak parça parça incelenebilir.
Bu çalışma, fabrike bir makalenin yerine, PRISMA 2020 envanteri (117 set), altı kohortun yeniden
analizi, üç epigenetik saat, güç analizi ve sızıntısız makine öğrenmesinden oluşan **tamamen
yeniden üretilebilir** bir iskelet sunar. Sigara dışında güçlü sonuç için daha büyük, sigara-
düzeltmeli, doku-eşleşmiş **replikasyon kohortları** gereklidir.

---

## Etik beyanı

Çalışma yalnızca halka açık, kimliksizleştirilmiş ikincil veri (GEO) kullanır; yeni insan/hayvan
verisi toplanmamıştır. Her kaynak kohort kendi orijinal etik onayı altında yayımlanmıştır.

## Veri ve kod erişilebilirliği

Tüm GEO setleri herkese açıktır (accession'lar metinde). Analiz kodu, çıktılar ve veri SHA-256
değerleri bu repoda committed'dır: betikler `scripts/revize/realdata/scripts/`, sonuç tabloları
`out/`, şeffaflık raporu `REPORT.md`. Sabit seed = 42 ile yeniden üretilebilir.

## Çıkar çatışması

Beyan edilmemiştir. [Gerekirse güncellenecek.]

## Yazar katkıları / Finansman

[Yer-tutucu — uydurma kimlik yazılmadı.]

---

## Kaynaklar (yalnız doğrulanmış)

1. Page MJ, McKenzie JE, Bossuyt PM, ve ark. The PRISMA 2020 statement. *BMJ.* 2021;372:n71.
   doi:10.1136/bmj.n71
2. Horvath S. DNA methylation age of human tissues and cell types. *Genome Biol.*
   2013;14(10):R115. doi:10.1186/gb-2013-14-10-r115
3. Hannum G, Guinney J, Zhao L, ve ark. Genome-wide methylation profiles reveal quantitative
   views of human aging rates. *Mol Cell.* 2013;49(2):359-367. doi:10.1016/j.molcel.2012.10.016
4. Levine ME, Lu AT, Quach A, ve ark. An epigenetic biomarker of aging for lifespan and
   healthspan (PhenoAge). *Aging (Albany NY).* 2018;10(4):573-591. doi:10.18632/aging.101414
5. [Opioid-kan EWAS meta-analizi] *Epigenomics.* 2022;14(23):1479-1492. PMID 36700736.
   doi:10.2217/epi-2022-0353
6. [Esrar / CanCOLD akciğer metilasyonu] *BMC Pulm Med.* 2025. PMID 40205553.
7. GEO veri setleri: GSE50660, GSE110043, GSE49393, GSE77056, GSE154971, GSE98203 (ve dahil
   edilen 117 setin tam listesi `out/prisma/inventory.json`).

> Not: 5. ve 6. kaynakların başlık/yazar alanları, canlı doğrulamada erişilen PMID/DOI ile
> sınırlı tutulmuştur; yer-tutucu köşeli parantezler uydurma künye yazmamak içindir.
