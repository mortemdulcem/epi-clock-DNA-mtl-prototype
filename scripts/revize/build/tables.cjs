"use strict";
// Hand-encoded numeric table grids (numbers verbatim from makale.txt).
// New sequential numbering 1..27 (old: 1,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
// 20,21,22,23,24,25,26,27,28,29,30,31). R2 written as R². superior->üstün applied.
// Footnotes are read from disk in build.cjs (noteLines) to avoid transcription risk;
// only 2-column legends are inlined there.

const D = "—"; // em dash where source had "-" as a placeholder is kept as "-"

// 1 (old Tablo 1) Veri Kaynakları
const t1 = {
  headers: ["Veri Seti", "Madde Türü", "Platform", "Örnek Sayısı", "Doku", "Yaş (ort±SS)", "Kadın (%)", "Kaynak"],
  rows: [
    ["GSE50660", "Sigara (nikotin)", "450K", "464", "Tam kan", "55.4±6.7", "veri yok", "GEO"],
    ["GSE110043", "Alkol (AUD)", "450K", "94", "Tam kan", "veri yok", "veri yok", "GEO"],
    ["GSE49393", "Alkol (AUD)", "450K", "48", "Beyin (PFK, postmortem)", "56.2±9.1", "veri yok", "GEO"],
    ["GSE77056", "Kokain/crack", "450K", "47", "Tam kan", "25.6±2.3", "veri yok", "GEO"],
    ["GSE154971", "Metamfetamin", "450K", "24", "Periferik kan lenfositi", "veri yok", "veri yok", "GEO"],
    ["GSE98203", "Opioid/eroin", "450K", "65", "Beyin (OFK, postmortem)", "30.6±11.2", "veri yok", "GEO"],
    ["TOPLAM (derinlemesine analiz)", "Çoklu madde", "450K", "742", "Kan+Beyin", "—", "—", "6 GEO veri seti"],
  ],
};

// 2 (old 6) Epigenetik Saat Performans Değerlendirmesi
const t2 = {
  headers: ["Epigenetik Saat", "MAE (yıl)", "95% GA", "RMSE (yıl)", "R²", "Kalibrasyon Eğimi", "Kalibrasyon Kesişimi"],
  rows: [
    ["Horvath (2013) [GSE50660, n=464]", "3.51", "veri yok", "4.55", "0.586", "veri yok", "veri yok"],
    ["Hannum (2013) [GSE50660, n=464]", "7.82", "veri yok", "8.80", "0.641", "veri yok", "veri yok"],
    ["PhenoAge (Levine 2018) [GSE50660, n=464]", "6.77", "veri yok", "7.98", "0.565", "veri yok", "veri yok"],
    ["GrimAge", "veri yok (450K beta'dan tek başına hesaplanamadı)", "—", "—", "—", "—", "—"],
    ["Ensemble (Ağırlıklı)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—"],
    ["Ensemble (Stacked)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—"],
  ],
};

// 3 (old 7) Madde Türüne Göre Epigenetik Yaş İvmelenmesi (wide)
const t3 = {
  headers: ["Özellik", "Alkol", "Kokain", "Opioid", "Metamfetamin", "Kannabis", "Çoklu Madde", "Core Addiction Signature"],
  rows: [
    ["n", "48 (GSE49393, beyin)", "47 (GSE77056, kan)", "65 (GSE98203, beyin)", "24 (GSE154971, PBL)", "veri yok", "veri yok", "veri yok"],
    ["Horvath EAA (yıl, vaka−kontrol)", "-0.82", "-0.66", "-1.48", "veri yok", "veri yok", "veri yok", "veri yok"],
    ["GrimAge EAA (yıl)", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok"],
    ["p-değeri (EAA testi)", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok"],
    ["Cohen's d", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok", "veri yok"],
    ["Anlamlı CpG (FDR<0,05)", "8", "11987", "12", "398", "veri yok", "veri yok", "veri yok"],
    ["Hipermetile", "4", "1668", "9", "342", "veri yok", "veri yok", "veri yok"],
    ["Hipometile", "4", "10319", "3", "56", "veri yok", "veri yok", "veri yok"],
    ["Top Genler", "veri yok (anotasyon gerekli)", "veri yok (anotasyon gerekli)", "veri yok (anotasyon gerekli)", "veri yok (anotasyon gerekli)", "—", "—", "—"],
    ["En Anlamlı CpG", "cg00393248", "cg06808467", "cg27504782", "cg06763671", "—", "—", "—"],
    ["Gen", "veri yok (anotasyon gerekli)", "veri yok (anotasyon gerekli)", "veri yok (anotasyon gerekli)", "veri yok (anotasyon gerekli)", "—", "—", "—"],
    ["Δβ Değeri", "+0.051", "-0.114", "-0.026", "+0.064", "—", "—", "—"],
    ["CpG p-değeri", "9.3×10⁻⁸", "8.3×10⁻²³", "7.7×10⁻⁸", "2.7×10⁻¹⁷", "—", "—", "—"],
    ["Önemli Biyolojik Yolak", "veri yok / kaynak gerekli", "veri yok / kaynak gerekli", "veri yok / kaynak gerekli", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Doz-Yanıt İlişkisi", "veri yok / kaynak gerekli", "veri yok / kaynak gerekli", "veri yok / kaynak gerekli", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Postmortem Beyin EAA", "Prefrontal korteks (GSE49393): -0.82 yıl", "—", "Orbitofrontal korteks (GSE98203): -1.48 yıl", "—", "—", "—", "—"],
  ],
};

// 4 (old 8) Gen Ontoloji Zenginleştirmesi
const t4 = {
  headers: ["Kategori (GO Terimi)", "GO Sınıfı", "Gen Sayısı", "FDR"],
  rows: [
    ["positive regulation of Rho protein signal transduction (GO:0035025)", "BP", "3", "0.023"],
    ["positive regulation of MAPK cascade (GO:0043410)", "BP", "6", "0.023"],
    ["positive regulation of Ras protein signal transduction (GO:0046579)", "BP", "3", "0.099"],
    ["intestinal absorption (GO:0050892)", "BP", "2", "0.099"],
    ["regulation of Rho protein signal transduction (GO:0035023)", "BP", "3", "0.112"],
    ["positive regulation of ERK1 and ERK2 cascade (GO:0070374)", "BP", "4", "0.112"],
    ["(Yalnızca ilk iki terim FDR<0,05; GSE50660 sigara kohortu, Enrichr)", "—", "—", "—"],
  ],
};

// 5 (old 9) KEGG Pathway
const t5 = {
  headers: ["Yolak", "Gen Sayısı", "p-değeri", "FDR"],
  rows: [
    ["Pathways in cancer", "6", "0.0022", "0.168"],
    ["Dopaminergic synapse", "3", "0.0046", "0.168"],
    ["Tryptophan metabolism", "2", "0.0051", "0.168"],
    ["Chemokine signaling pathway", "3", "0.0129", "0.275"],
    ["Lipid and atherosclerosis", "3", "0.0175", "0.275"],
    ["Hiçbir KEGG yolağı FDR<0,05 eşiğini geçmedi (GSE50660, Enrichr)", "—", "—", "veri yok"],
  ],
};

// 6 (old 10) Madde Sınıflandırma Performans Metrikleri
const t6 = {
  headers: ["Madde Türü", "Precision", "Recall", "F1-Score", "ROC-AUC"],
  rows: [
    ["Sigara (nikotin) [GSE50660]", "0.864", "0.864", "0.864", "0.928"],
    ["Alkol (AUD) [GSE110043]", "0.911", "0.872", "0.891", "0.926"],
    ["Kokain/crack [GSE77056]", "0.958", "1.000", "0.979", "1.000"],
    ["Metamfetamin [GSE154971]", "0.875", "0.875", "0.875", "0.922"],
    ["Opioid", "veri yetersiz", "veri yetersiz", "veri yetersiz", "veri yetersiz"],
    ["Kannabis", "veri yetersiz", "veri yetersiz", "veri yetersiz", "veri yetersiz"],
    ["Çoklu Madde", "veri yetersiz", "veri yetersiz", "veri yetersiz", "veri yetersiz"],
  ],
};

// 7 (old 11) Konsolide Mediyasyon (multi-segment)
const t7 = {
  segments: [
    {
      subtitle: "1. Genel Mediyasyon",
      headers: ["Alt Grup", "n", "Toplam Etki (β)", "Direkt Etki (β)", "İndirekt Etki (β) & Mediyasyon %", "p-değeri"],
      rows: [
        ["İnsülin Direnci (HOMA-IR)", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["HPA Eksen (Kortizol/ACTH)", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Sistemik İnflamasyon (CRP/IL-6)", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
      ],
    },
    {
      subtitle: "2. Yolak Katsayıları",
      headers: ["Alt Grup", "n", "Path a (Madde → Mediyatör)", "Path b (Mediyatör → EAA)", "İlişki Yönü", "p-değeri"],
      rows: [
        ["İnsülin Yolağı", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["HPA Eksen Yolağı", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["İnflamasyon Yolağı", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
      ],
    },
    {
      subtitle: "3. Maddeye Özgü Etkiler",
      headers: ["Alt Grup", "n", "İnsülin Mediyasyon Oranı", "HPA (Kortizol) Artışı", "Karşılaştırma", "p-değeri"],
      rows: [
        ["Alkol", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Kokain", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Opioid", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Metamfetamin", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
      ],
    },
    {
      subtitle: "4. Biyomarker Düzeyleri",
      headers: ["Alt Grup", "n", "CRP (mg/L) Ort ± SS", "IL-6 (pg/mL) Ort ± SS", "t-istatistiği (CRP / IL-6)", "p-değeri"],
      rows: [
        ["Kontrol Grubu", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Alkol Grubu", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Kokain Grubu", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Opioid Grubu", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Metamfetamin Grubu", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Çoklu Madde Kullanımı", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
      ],
    },
    {
      subtitle: "5. Çoklu Model",
      headers: ["Alt Grup", "n", "İndirekt Etki (β)", "95% Güven Aralığı", "Bağımsız Katkı %", "p-değeri"],
      rows: [
        ["İnsülin Direnci", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["HPA Eksen", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["Sistemik İnflamasyon", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
        ["MODEL TOPLAMI", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
      ],
    },
  ],
};

// 8 (old 12) Moderasyon (multi-segment)
const t8 = {
  segments: [
    {
      subtitle: "Duygu Düzenleme (DERS)",
      headers: ["Seviye/Kategori", "Etki Büyüklüğü (β)", "SE", "95% GA", "p-değeri", "EAA (yıl)", "95% GA (EAA)", "Kontrol/Referans", "Fark (yıl)", "n"],
      rows: [
        ["Düşük (-1 SD) / İyi (<60)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—", "—", "—"],
        ["Ortalama / Orta (60-90)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—", "—", "—"],
        ["Yüksek (+1 SD) / Zayıf (>90)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—", "—", "—"],
      ],
    },
    {
      subtitle: "Öz-Kontrol (SCS-B)",
      headers: ["Seviye/Kategori", "Etki Büyüklüğü (β)", "SE", "95% GA", "p-değeri", "EAA (yıl)", "95% GA (EAA)", "Kontrol/Referans", "Fark (yıl)", "n"],
      rows: [
        ["Düşük (-1 SD) / Düşük (<30)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—", "—", "—"],
        ["Ortalama / Orta (30-40)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—", "—", "—"],
        ["Yüksek (+1 SD) / Yüksek (>40)", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—", "—", "—"],
      ],
    },
  ],
};

// 9 (old 13) PMI Düzeltme
const t9 = {
  headers: ["Metrik", "Düzeltme Öncesi", "95% GA", "Düzeltme Sonrası", "95% GA", "İyileşme", "p-değeri"],
  rows: [
    ["MAE (yıl)", "veri yok / kaynak gerekli", "—", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["RMSE (yıl)", "veri yok / kaynak gerekli", "—", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["R²", "veri yok / kaynak gerekli", "—", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Kalibrasyon Eğimi", "veri yok / kaynak gerekli", "—", "veri yok / kaynak gerekli", "—", "—", "—"],
  ],
};

// 10 (old 14) Doku pH
const t10 = {
  headers: ["pH Kategorisi", "pH Aralığı", "n", "MAE (yıl)", "95% GA", "R²", "Kullanılabilirlik Durumu"],
  rows: [
    ["Mükemmel Kalite", ">6.5", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["İyi Kalite", "6.0-6.5", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["Orta Kalite", "5.5-6.0", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["Zayıf Kalite", "<5.5", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
  ],
};

// 11 (old 15) Başlangıç Yaşı
const t11 = {
  headers: ["Başlangıç Yaş Kategorisi", "n", "EAA (yıl)", "95% GA", "ANOVA Trend"],
  rows: [
    ["<30 yaş", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["30-50 yaş", "veri yok / kaynak gerekli", "—", "—", "—"],
    [">50 yaş", "veri yok / kaynak gerekli", "—", "—", "—"],
  ],
};

// 12 (old 16) Cinsiyet Etkisi
const t12 = {
  headers: ["Madde Türü", "Erkek EAA (yıl)", "95% GA", "Kadın EAA (yıl)", "95% GA", "Fark (yıl)", "t-istatistiği", "p-değeri"],
  rows: [
    ["Alkol", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—"],
    ["Kokain", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—"],
    ["Opioid", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—"],
    ["Metamfetamin", "veri yok / kaynak gerekli", "—", "—", "—", "—", "—", "—"],
  ],
};

// 13 (old 17) Eğitim Seviyesi
const t13 = {
  headers: ["Eğitim Seviyesi", "n", "EAA (yıl)", "95% GA", "ANOVA Trend"],
  rows: [
    ["<Lise", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Lise", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Üniversite", "veri yok / kaynak gerekli", "—", "—", "—"],
  ],
};

// 14 (old 18) BMI
const t14 = {
  headers: ["BMI Kategorisi", "BMI Aralığı", "n", "EAA (yıl)", "95% GA"],
  rows: [
    ["Normal", "18.5-25", "veri yok / kaynak gerekli", "—", "—"],
    ["Fazla Kilolu", "25-30", "veri yok / kaynak gerekli", "—", "—"],
    ["Obez", ">30", "veri yok / kaynak gerekli", "—", "—"],
  ],
};

// 15 (old 19) Egzersiz
const t15 = {
  headers: ["Egzersiz Sıklığı", "n", "EAA (yıl)", "95% GA", "ANOVA Trend"],
  rows: [
    ["Düzenli (≥3×/hafta)", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Ara Sıra (1-2×/hafta)", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Hiç Yok", "veri yok / kaynak gerekli", "—", "—", "—"],
  ],
};

// 16 (old 20) Hiyerarşik Regresyon
const t16 = {
  headers: ["Model", "Eklenen Değişkenler", "R²", "ΔR²", "F-istatistiği", "p-değeri"],
  rows: [
    ["Model 1", "Yaş + Cinsiyet", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Model 2", "+ Madde kullanım süresi", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Model 3", "+ Fizyolojik mediyatörler (HOMA-IR, Kortizol/ACTH, İnflamasyon)", "veri yok / kaynak gerekli", "—", "—", "—"],
    ["Model 4", "+ Psikolojik moderatörler (DERS, SCS-B)", "veri yok / kaynak gerekli", "—", "—", "—"],
  ],
};

// 17 (old 21) Final Model
const t17 = {
  headers: ["Değişken", "β (standardize)", "SE", "95% GA", "p-değeri", "Bağımsız R²"],
  rows: [
    ["Madde Kullanım Süresi", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["BMI", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["Eğitim Seviyesi", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["Egzersiz Sıklığı", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["DERS Skoru", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["İnsülin Direnci (HOMA-IR)", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
    ["İnflamasyon Skoru", "veri yok / kaynak gerekli", "—", "—", "—", "—"],
  ],
};

// 18 (old 22) Tersine Çevrilebilirlik Müdahale (with sub-headers)
const t18 = {
  headers: ["Müdahale Türü", "Çalışma", "n", "Süre", "Epigenetik Yaş Değişimi (yıl)", "95% GA", "p-değeri"],
  rows: [
    ["Yaşam Tarzı Müdahaleleri", "", "", "", "", "", ""],
    ["Metilasyon-Destekleyici Diyet", "Fitzgerald et al.", "43", "8 hafta", "-3.23", "-4.1, -2.4", "<0.001"],
    ["Yoğun Egzersiz Programı", "Quach et al.", "78", "12 hafta", "-2.87", "-3.6, -2.1", "<0.001"],
    ["Mindfulness + Yoga", "Epel et al.", "96", "12 hafta", "-1.96", "-2.7, -1.2", "<0.001"],
    ["Kombine Müdahale", "Fitzgerald et al.", "43", "8 hafta", "-4.60", "-5.8, -3.4", "<0.001"],
    ["Madde Bırakma Etkileri", "", "", "", "", "", ""],
    ["1 yıl sonra", "Ambatipudi et al.", "124", "1 yıl", "-1.52", "-2.3, -0.7", "0.002"],
    ["5 yıl sonra", "Ambatipudi et al.", "89", "5 yıl", "-3.18", "-4.2, -2.1", "<0.001"],
    ["Meta-Analiz Özeti", "", "", "", "", "", ""],
    ["Tüm müdahaleler", "6 çalışma", "473", "-", "-2.73", "-3.4, -2.1", "<0.001"],
  ],
};

// 19 (old 23) Doz-Yanıt
const t19 = {
  headers: ["Müdahale Süresi", "n (Çalışma)", "Ortalama Etki (yıl)", "95% GA", "Trend p-değeri"],
  rows: [
    ["Kısa Vadeli (8-12 hafta)", "4", "-2.67", "-3.5 - -1.8", "-"],
    ["Orta Vadeli (1 yıl)", "1", "-1.52", "-2.3 - -0.7", "p<0.001 (Lineer trend)"],
    ["Uzun Vadeli (5 yıl)", "1", "-3.18", "-4.2 - -2.1", ""],
  ],
};

// 20 (old 24) Özet İstatistikleri
const t20 = {
  headers: ["Parametre", "Değer", "Yorum"],
  rows: [
    ["Maksimum Gözlemlenen Azalma", "-4.60 yıl", "Kombine müdahale (8 hafta)"],
    ["Minimum Gözlemlenen Azalma", "-1.52 yıl", "Madde bırakma (1 yıl)"],
    ["Kısa Vadeli Ortalama (≤12 hafta)", "-2.67 yıl", "Hızlı etki"],
    ["Uzun Vadeli Ortalama (≥1 yıl)", "-2.35 yıl", "Sürdürülebilir etki"],
    ["Kombine Müdahale Avantajı", "+1.93 yıl", "Tek müdahaleye göre ek fayda"],
  ],
};

// 21 (old 25) Klinik Öneriler
const t21 = {
  headers: ["EAA Seviyesi", "Önerilen Müdahale", "Beklenen Etki (8-12 hafta)", "Uzun Vadeli Strateji"],
  rows: [
    ["Hafif (+1-3 yıl)", "Egzersiz + Diyet", "-2.5 ila -3.0 yıl", "Yaşam tarzı sürdürme"],
    ["Orta (+3-5 yıl)", "Kombine Müdahale", "-3.5 ila -4.5 yıl", "Kombine + psikolojik destek"],
    ["Şiddetli (>5 yıl)", "Kombine + Madde Bırakma", "-4.0 ila -5.0 yıl (kısa vadeli), -3.0 ila -4.0 yıl (uzun vadeli)", "Yoğun multidisipliner yaklaşım"],
  ],
};

// 22 (old 26) Literatür Kalite
const t22 = {
  headers: ["Çalışma", "Dizayn", "Örnek Boyutu", "Takip Süresi", "Randomizasyon", "Kör Değerlendirme", "Kalite Skoru"],
  rows: [
    ["Fitzgerald et al. (35)", "RCT", "43", "8 hafta", "Evet", "Evet", "9/10"],
    ["Quach et al. (23)", "Kohort", "78", "12 hafta", "Hayır", "Evet", "7/10"],
    ["Epel et al. (36)", "RCT", "96", "12 hafta", "Evet", "Evet", "9/10"],
    ["Ambatipudi et al. (37)", "Uzunlamasına Kohort", "124", "5 yıl", "Hayır", "Evet", "8/10"],
  ],
};

// 23 (old 27) Mevcut Literatürle Karşılaştırma
const t23 = {
  headers: ["Madde Türü", "Çalışma", "n", "Kohort Özellikleri", "Epigenetik Saat", "EAA (yıl)", "Mevcut Çalışma Bulguları", "Karşılaştırma/Açıklama"],
  rows: [
    ["Alkol", "Rosen et al. (21)", "331", "AUD hastaları", "Horvath", "+2.3", "—", "Önceki pozitif bulgular"],
    ["", "Liu et al. (18)", "1234", "Ağır alkol tüketimi", "GrimAge", "+3.1", "—", "Önceki pozitif bulgular"],
    ["", "Mevcut Çalışma", "94 (kan) + 48 (beyin)", "GSE110043 + GSE49393", "Horvath", "−0,82 (beyin, AD)", "Bütün-doku", "Anlamsız; önceki bulgularla çelişiyor"],
    ["Kokain", "Cheng et al. (19)", "287", "Ort. kullanım: 8.7 yıl", "GrimAge", "+2.9", "—", "Önceki pozitif bulgular"],
    ["", "Mevcut Çalışma", "47", "GSE77056 (kan)", "Horvath/Hannum", "−0,66 (Horvath, AD)", "Hannum ivmesi p=0.021", "Yalnız çoklu-saatte sinyal"],
    ["Opioid", "Monick et al. (20)", "198", "Heroin (illicit)", "GrimAge", "+3.2", "—", "Önceki pozitif bulgular"],
    ["", "Mevcut Çalışma", "65", "GSE98203 (beyin)", "Horvath", "−1,48 (AD)", "Bütün-doku", "Anlamsız; önceki bulgularla çelişiyor"],
    ["Metamfetamin", "Liang et al. (40)", "89", "-", "Horvath", "+4.2", "—", "Önceki pozitif bulgular"],
    ["", "Mevcut Çalışma", "24", "GSE154971 (lenfosit)", "Horvath", "NA (kronolojik yaş yok)", "EAA hesaplanamadı", "Yalnız sınıflandırma (AUC 0.922)"],
  ],
};

// 24 (old 28) Çalışmanın Özgünlüğü
const t24 = {
  headers: ["Özellik", "Önceki Çalışmalar", "Mevcut Çalışma", "Katkı"],
  rows: [
    ["Örnek Boyutu", "Değişken (tek kohort)", "6 ayrı GEO kohortu, toplam n=742", "Havuzlanmamış; entegre mega-kohort iddiası yok"],
    ["Madde Türü Çeşitliliği", "Genellikle tek madde", "6 madde kategorisi", "Kapsamlı karşılaştırmalı analiz"],
    ["Epigenetik Saat Sayısı", "1-2 saat", "3 saat (Horvath, Hannum, PhenoAge)", "GrimAge/DunedinPACE 450K'dan hesaplanamadı; ensemble yok"],
    ["CpG İmza Tanımlama", "Sınırlı veya yok", "Kohort-özgü DMP (FDR<0,05): sigara 89, alkol-kan 4387, kokain 11987, meth 398, opioid 12, alkol-beyin 8", "Sızıntısız sınıflandırma AUC 0.92-1.00"],
    ["Mediyasyon Analizi", "Sınırlı", "Yapılamadı — bireysel mediyatör verisi yok", "veri yok / kaynak gerekli"],
    ["Moderasyon Analizi", "Genellikle yok", "Yapılamadı — bireysel moderatör verisi yok", "veri yok / kaynak gerekli"],
    ["Postmortem Validasyon", "Nadiren", "2 beyin kohortu (toplam n=113), bütün-doku", "PMI verisi yok; bölgesel ayrım yok"],
    ["Beyin Dokusu Analizi", "Nadiren", "2 kohort (PFC alkol, OFC opioid), bütün-doku", "EAA negatif ve anlamsız (AD)"],
  ],
};

// 25 (old 29) Beyin Dokusu Literatür
const t25 = {
  headers: ["Çalışma", "n", "Beyin Bölgesi / Doku", "EAA (yıl)", "Sonuç"],
  rows: [
    ["Önceki çalışmalarda sınırlı veri", "-", "-", "-", "-"],
    ["Mevcut Çalışma (alkol-beyin, GSE49393)", "48", "Prefrontal korteks (bütün-doku)", "−0,82 (p=0,29)", "Anlamsız (AD)"],
    ["Mevcut Çalışma (opioid-beyin, GSE98203)", "65", "Orbitofrontal korteks (bütün-doku)", "−1,48 (p=0,18)", "Anlamsız (AD)"],
  ],
};

// 26 (old 30) Metodolojik Üstünlükler
const t26 = {
  headers: ["Metodolojik Özellik", "Önceki Çalışmalar", "Mevcut Çalışma", "Avantaj"],
  rows: [
    ["Veri Harmonizasyonu", "Sınırlı", "Her kohort kendi içinde ayrı analiz edildi (ComBat/birleştirme yok)", "Kohortlar arası batch karışması önlendi"],
    ["Kalite Kontrol", "Standart", "Çok katmanlı (örnek + prob + batch)", "Yüksek veri kalitesi"],
    ["İstatistiksel Güç", "Orta", "Sınırlı (toplam n=742; bazı kohortlar n<50)", "Küçük örneklem; alt grup analizi sınırlı"],
    ["Çoklu Test Düzeltmesi", "FDR", "FDR + Bonferroni (CpG analizleri)", "Tip I hata kontrolü"],
    ["Duyarlılık Analizleri", "Sınırlı", "Kapsamlı (kovaryat setleri, yöntemler)", "Bulgu robustluğu"],
    ["Açık Bilim", "Nadiren", "GitHub repository + tam pipeline", "Tekrarlanabilirlik"],
  ],
};

// 27 (old 31) Tanısal Doğruluk
const t27 = {
  headers: ["Model (madde vs kontrol)", "AUC-ROC", "Duyarlılık", "Özgüllük", "n", "Yorum"],
  rows: [
    ["Kokain (GSE77056)", "1.000", "1,00", "0,96", "47", "Mükemmel ayrım"],
    ["Sigara (GSE50660)", "0.928", "0,86", "0,98", "201", "Yüksek"],
    ["Alkol (GSE110043)", "0.926", "0,87", "0,91", "94", "Yüksek"],
    ["Metamfetamin (GSE154971)", "0.922", "0,88", "0,75", "24", "Yüksek (küçük örneklem)"],
    ["Opioid-beyin / Alkol-beyin", "—", "—", "—", "65 / 48", "Örneklem seyrek; modellenmedi (veri yok)"],
  ],
};

module.exports = {
  t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15,
  t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27,
};
