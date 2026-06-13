// One-shot: line-locked rewrite of the 6 main-figure legends (Şekil 1-6) in
// makale.txt so they match the regenerated real-data figures. Each block is
// replaced with EXACTLY the same number of lines (asserted) -> total line count
// (1886) is preserved. Run once: node build/relegend.cjs
const fs = require("fs");
const path = require("path");
const FILE = path.join(__dirname, "..", "makale.txt");
const lines = fs.readFileSync(FILE, "utf8").split("\n");
const before = lines.length;

// [1-indexed inclusive start, end, newLines]
const blocks = [
  [1669, 1677, [
    "           Şekil 1: Epigenetik Saat Performans Karşılaştırması",
    "Bu grafik, katsayıları halka açık olan üç epigenetik saatin gerçek performansını göstermektedir (sızıntısız çapraz-doğrulama):",
    "          A. Tahmin Doğruluğu (MAE): GSE50660 referans kohortunda (n=464) Horvath en düşük hatayı (3,51 yıl), Hannum en yüksek hatayı",
    "           (7,82 yıl) vermiştir; PhenoAge 6,77 yıldır.",
    "          B. Kronolojik Yaşla Korelasyon (r): Hannum en yüksek korelasyona (0,80), PhenoAge ise en düşük değere (0,75) sahiptir.",
    "          C. Horvath MAE — Kohort Bazında: Sigara-kan 3,5 yıl ile en düşük, kokain-kan 12,3 yıl ile en yüksek hatayı verir; metamfetaminde",
    "           kronolojik yaş bulunmadığından saat doğrulanamamıştır (NA).",
    "          D. Hesaplama Kapsamı: GrimAge ve DunedinPACE 450K beta değerlerinden hesaplanamaz; tek bir 'ensemble' saat kurulmamıştır (veri yok).",
    "Bu şekil, altı bağımsız GEO kohortundan (toplam n=742) elde edilen gerçek DNA metilasyon profillerinin analizine dayanmaktadır.",
  ]],
  [1678, 1685, [
    " Şekil 2: Maddeye Özgü Epigenetik Yaş İvmelenmesi",
    "Bu grafik, madde kullanımının Horvath epigenetik yaş ivmelenmesi (EAA) üzerindeki gerçek etkisini göstermektedir:",
    "          A. Maddeye Özgü EAA (vaka − kontrol): Tüm farklar küçük ve NEGATİF yöndedir — opioid-beyin −1,48 yıl, alkol-beyin −0,82 yıl ve",
    "           kokain −0,66 yıl; hiçbiri istatistiksel olarak anlamlı değildir (p>0,05).",
    "          B. Vaka vs Kontrol Ortalaması: Her kohort için vaka ve kontrol gruplarının ortalama yaş ivmesi ayrı ayrı karşılaştırılmıştır.",
    "          C. Yorum: Metamfetaminde kronolojik yaş olmadığından EAA hesaplanamamıştır. Çoklu-saat analizinde iki gerçek ek sinyal vardır —",
    "           kokainde Hannum ivmesi (p=0.021) ve sigarada PhenoAge ivmesi (p=0.051, sınırda).",
    "Maddeler arası ortak ölçek bulunmadığından çoklu-madde havuzu ile Cohen's d etki büyüklüğü hesaplanmamıştır (veri yok).",
  ]],
  [1686, 1692, [
    "Şekil 3: Diferansiyel Metilasyon ve Yolak Zenginleştirme Analizleri",
    "Bu grafik, test edilemeyen aracılık (X→M→Y) modelinin yerine gerçek diferansiyel metilasyon ve zenginleştirme sonuçlarını göstermektedir:",
    "         A. Diferansiyel Metilasyon (FDR<0,05): Kohort başına anlamlı CpG sayısı — kokain 11.987, alkol-kan 4.387, metamfetamin 398, sigara 89,",
    "          opioid-beyin 12 ve alkol-beyin 8.",
    "         B. Sigara Modeli — En Önemli CpG: XGBoost SHAP değerlerine göre cg05575921 (AHRR) açık ara en güçlü belirteçtir (2,27), ardından ALPPL2 gelir.",
    "         C. Yolak Zenginleştirme (GO-BP, FDR<0,05): Yalnız opioid-beyin (25 terim) ve alkol-beyin (2 terim) anlamlı; diğer kohortlarda anlamlı terim yoktur.",
    "         D. Yorum: Sigara imzası AHRR/ALPPL2/F2RL3 gibi klasik genleri yakalar; bireysel fenotip verisi yoktur, bu yüzden aracılık testi yapılamamıştır (veri yok).",
  ]],
  [1693, 1704, [
    " Şekil 4: Çalışma Kohortu Özellikleri",
    "",
    "Şekil 4'te sunulan çalışma, altı bağımsız GEO metilasyon kohortundan (toplam n=742) oluşur; her kohort ayrı analiz edilmiştir. Örneklem dağılımı",
    "sigara-kan (n=464), alkol-kan (n=94), opioid-beyin (n=65), alkol-beyin (n=48), kokain-kan (n=47) ve metamfetamin-lenfosit (n=24) gruplarındandır.",
    "",
    "Doku dağılımında örneklerin çoğu kandan (n=605), kalanı postmortem beyin (n=113) ve lenfositten (n=24) elde edilmiştir. Vaka/kontrol oranları her",
    "kohort için ayrı belirtilmiştir (ör. alkol-kan 47/47, opioid-beyin 37/28, alkol-beyin 23/25, kokain 23/24, metamfetamin 16/8).",
    "",
    "Kohortların yalnız bir kısmında kronolojik yaş bulunduğundan Horvath saati sigara, alkol-beyin, opioid-beyin ve kokain kohortlarında doğrulanmıştır.",
    "Yaş, cinsiyet ve kullanım süresi gibi ortak demografik değişkenler tüm setlerde mevcut olmadığından kohortlar arası kovaryat olarak kullanılamamıştır.",
    "",
    "Bu gerçek kohort özellikleri, madde kullanımının epigenetik etkilerini değerlendirirken örneklem ve doku farklılıklarının önemini göstermektedir.",
  ]],
  [1705, 1727, [
    " Şekil 5: Beyin Dokusunda Epigenetik Yaş İvmelenmesi",
    "",
    "Bu grafik, postmortem beyin kohortlarında bütün-doku (bulk) düzeyinde ölçülen gerçek Horvath epigenetik yaş ivmelenmesini göstermektedir:",
    "",
    "          A. Sagital Beyin Kesiti — Bütün-doku EAA: İki postmortem kohortun vaka−kontrol yaş ivmesi anatomik kesit üzerinde işaretlenmiştir.",
    "",
    "          B. Beyin Kohortları İstatistikleri: Prefrontal korteks (alkol-beyin, GSE49393) −0,82 yıl ve orbitofrontal korteks (opioid-beyin,",
    "           GSE98203) −1,48 yıl; her iki fark da NEGATİF ve istatistiksel olarak ANLAMSIZDIR (p>0,05).",
    "",
    "Bu analiz, iki bağımsız postmortem beyin kohortunda (toplam n=113) bütün-doku düzeyinde yapılmıştır.",
    "",
    "- Prefrontal korteks (alkol-beyin): −0,82 yıl (n=48, p=0,29)",
    "",
    "- Orbitofrontal korteks (opioid-beyin): −1,48 yıl (n=65, p=0,18)",
    "",
    "Beyin dokusu yalnızca bütün-doku (bulk) olarak analiz edilebilmiştir; nükleus akumbens, amigdala, hipokampus ve ventral tegmental alan gibi",
    "bölgesel alt-bölümler için ayrı veri bulunmamaktadır (veri yok).",
    "",
    "Postmortem interval (PMI) düzeltmesi için gerekli bireysel PMI verisi de kamuya açık setlerde mevcut değildir; bu nedenle PMI düzeltmesi",
    "uygulanamamıştır.",
    "",
    "Negatif ve anlamsız EAA bulguları, bu kohortlarda madde kullanımına bağlı hızlanmış beyin yaşlanmasının doğrulanamadığını gösterir; daha",
    "büyük ve bölge-çözünürlüklü örneklemlere ihtiyaç vardır.",
  ]],
  [1728, 1758, [
    " Şekil 6: Maddeye Özgü İkili Sınıflandırma Performansı",
    "",
    "Bu grafik, her madde için ayrı kurulan ikili (madde-vs-kontrol) sınıflandırma modellerinin sızıntısız çapraz-doğrulama ile elde edilen gerçek",
    "performansını göstermektedir:",
    "",
    "İkili Sınıflandırma Sonuçları (XGBoost, sızıntısız 5-kat çapraz-doğrulama)",
    "",
    "          A. ROC-AUC: Kokain modeli mükemmel ayrım sağlar (AUC 1.000); sigara (0.928), alkol (0.926) ve metamfetamin (0.922) modelleri de",
    "           yüksek performans gösterir. Kesikli çizgi şans düzeyini (0.5) gösterir.",
    "",
    "          B. Duyarlılık ve Özgüllük: Her madde modeli için duyarlılık (gerçek pozitif) ve özgüllük (gerçek negatif) oranları sunulmuştur.",
    "",
    "Kohort Bazında Performans",
    "",
    "          Kokain (GSE77056, n=47): AUC 1.000 — duyarlılık 1,00, özgüllük 0,96",
    "",
    "          Sigara (GSE50660, n=201): AUC 0.928 — duyarlılık 0,86, özgüllük 0,98",
    "",
    "          Alkol (GSE110043, n=94): AUC 0.926 — duyarlılık 0,87, özgüllük 0,91",
    "",
    "          Metamfetamin (GSE154971, n=24): AUC 0.922 — duyarlılık 0,88, özgüllük 0,75",
    "",
    "Yöntem ve Sınırlılıklar",
    "",
    "          Tüm modeller seed=42 ile sızıntısız StratifiedKFold-5 kullanır; öznitelik seçimi her katın yalnız eğitim kısmında yapılır.",
    "",
    "          Opioid-beyin ve alkol-beyin kohortları örneklem açısından çok seyrek olduğundan sınıflandırma için modellenmemiştir.",
    "",
    "          Maddeler arasında ortak bir kohort bulunmadığından tek bir çok-sınıflı genel doğruluk değeri hesaplanmamıştır (veri yok).",
    "",
    "Bu sonuçlar, makalenin uydurma %87,3'lük yedi-sınıflı doğruluk iddiasının gerçek, yeniden üretilebilir karşılığını oluşturur.",
  ]],
];

for (const [s, e, repl] of blocks) {
  const expected = e - s + 1;
  if (repl.length !== expected) {
    throw new Error(`Block ${s}-${e}: expected ${expected} lines, got ${repl.length}`);
  }
  for (let k = 0; k < repl.length; k++) lines[s - 1 + k] = repl[k];
}

const after = lines.length;
if (after !== before) throw new Error(`line count changed ${before} -> ${after}`);
fs.writeFileSync(FILE, lines.join("\n"));
console.log(`OK: rewrote 6 legends, line count preserved = ${after}`);
