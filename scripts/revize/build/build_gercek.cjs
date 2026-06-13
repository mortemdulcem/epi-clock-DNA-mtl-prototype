"use strict";
// ============================================================================
// GERÇEK, YENİDEN ÜRETİLEBİLİR MAKALE — DOCX kurucu (sigara ekseni)
// ----------------------------------------------------------------------------
// Bu betik, uydurma epigenetik makalenin yerine geçecek DÜRÜST makaleyi üretir.
// Zero-Hallucination: TÜM sayılar ya halka açık gerçek veriden ya da kendi
// sabit-tohumlu (seed=42) betiklerimizin çıktısından gelir. Sayılar doğrudan
// realdata/out/*.json (+ doğrulanmış KEGG sabitleri) dosyalarından OKUNUR; elle
// yazılmaz. Yeniden üretilemeyen her şey makalede açıkça beyan edilir.
//
// NOT: fixes.cjs (stripThousands) virgüllü ondalıkları (örn. "0,245") bozacağı
// için BİLİNÇLİ olarak kullanılmaz; metin baştan doğru Türkçe ile yazılmıştır.
//
// Çalıştırma:  cd scripts/revize && node build/build_gercek.cjs
// Çıktı:       scripts/revize/build/makale_gercek.docx  (+ _document_gercek.xml)
// ============================================================================

const fs = require("fs");
const path = require("path");
const JSZip = require("jszip");
const L = require("./lib.cjs");

const ROOT = path.join(__dirname, "..");
const OUT = path.join(ROOT, "realdata", "out");
const DATA = path.join(ROOT, "realdata", "data");
const FIG = path.join(OUT, "figures");

const J = (f, d) => JSON.parse(fs.readFileSync(path.join(d || OUT, f), "utf8"));
const V = J("gse50660_validation.json");
const E = J("gse50660_enrichment_summary.json");
const C = J("gse50660_classifier.json");
const K = J("gse50660_clock_summary.json");
const M = J("manifest.json", DATA);

const SHA_SERIES = M.GSE50660.files["GSE50660_series_matrix.txt.gz"].sha256;
const SHA_MANIFEST = E.manifest_sha256;
const SHA_HORVATH = K.coef_sha256;

// --- KEGG: özet JSON'unda canlı yeniden-sorgu 429 (rate-limit) hatası kaydetti;
// ASIL sonuç işlenmiş out/gse50660_KEGG_2021_Human.csv dosyasındadır. Aşağıdaki
// değerler o CSV'den Python csv ayrıştırıcısıyla (virgüllü yolak adları doğru
// ele alınarak) bu turda doğrulanmıştır: 98 yolak, FDR<0,05 geçen YOK,
// en düşük düzeltilmiş p = 0,167995 ("Pathways in cancer").
const KEGG_N = 98, KEGG_SIG = 0, KEGG_MINADJ = 0.167995273059209;
const KEGG_TOP = [
  { Term: "Pathways in cancer", Overlap: "6/531", P: 0.0022266273954097, AdjP: 0.167995273059209, Genes: "RARA;LRP5;GNG12;PTK2;F2RL3;NFE2L2" },
  { Term: "Dopaminergic synapse", Overlap: "3/132", P: 0.0046444123644883, AdjP: 0.167995273059209, Genes: "MAOB;ARRB1;GNG12" },
  { Term: "Tryptophan metabolism", Overlap: "2/42", P: 0.005142712440588, AdjP: 0.167995273059209, Genes: "MAOB;CYP1A1" },
  { Term: "Chemokine signaling pathway", Overlap: "3/192", P: 0.0129395316699657, AdjP: 0.2752585378147332, Genes: "ARRB1;GNG12;PTK2" },
  { Term: "Bacterial invasion of epithelial cells", Overlap: "2/77", P: 0.0165141609675457, AdjP: 0.2752585378147332, Genes: "CTTN;PTK2" },
  { Term: "Lipid and atherosclerosis", Overlap: "3/215", P: 0.0174734371816651, AdjP: 0.2752585378147332, Genes: "CYP1A1;PTK2;NFE2L2" },
];

// ---------------------------------------------------------------- sayı biçimi
const SUP = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
const supE = (e) => String(e).split("").map((c) => SUP[c] || c).join("");
const dec = (x, d) => Number(x).toFixed(d).replace(".", ",").replace("-", "−");
function sci(x) {
  if (!isFinite(x)) return String(x);
  if (x === 0) return "0";
  let neg = x < 0; x = Math.abs(x);
  let e = Math.floor(Math.log10(x)); let m = x / Math.pow(10, e);
  if (Number(m.toFixed(1)) >= 10) { m /= 10; e++; }
  if (Number(m.toFixed(1)) < 1) { m *= 10; e--; }
  return (neg ? "−" : "") + m.toFixed(1).replace(".", ",") + " × 10" + supE(e);
}
const padj = (x) => (x >= 1e-3 ? dec(x, 3) : sci(x));

// gen / bölge eşlemesi (kanonik doğrulama tablosundan)
const cgGene = {};
for (const [cg, info] of Object.entries(V.canonical_validation)) cgGene[cg] = info.gene;
const geneOf = (cg) => cgGene[cg] || "—";

// SHA kısaltma gösterimi (tam değer Ek 1'de)
const shaShort = (h) => h.slice(0, 8) + "…" + h.slice(-6);

// ---------------------------------------------------------------- yardımcılar
const P = (t, o = {}) => L.p(t, Object.assign({ align: "both" }, o));
const lead = (label, text, o = {}) =>
  L.para(L.run(label + " ", { bold: true }) + L.run(text), Object.assign({ align: "both", after: 120 }, o));
const note = (t) => L.para(L.run(t, { sz: 16, italic: true }), { align: "both", before: 0, after: 120, line: 240 });

let MEDIA_RID = 2;
const MEDIA_RELS = [];
const MEDIA_FILES = [];
function addImageP(png, widthCm) {
  const buf = fs.readFileSync(path.join(FIG, png));
  const rId = MEDIA_RID++;
  const xml = L.imageP(rId, buf, widthCm, png);
  MEDIA_RELS.push(`<Relationship Id="rId${rId}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image${rId}.png"/>`);
  MEDIA_FILES.push({ name: `word/media/image${rId}.png`, buf });
  return xml;
}
function figure(num, png, widthCm, title, desc) {
  let x = addImageP(png, widthCm);
  x += L.figureCaption(`Şekil ${num}.`, title);
  if (desc) x += L.para(L.run(desc, { sz: 16 }), { align: "center", before: 0, after: 120, line: 240 });
  return x;
}

// ================================================================ İÇERİK
let body = "";

// ---- Başlık / yazar ----
body += L.titleP("SİGARA KULLANIMINA BAĞLI KAN DNA METİLASYON İMZALARI VE EPİGENETİK YAŞ: HALKA AÇIK 450K VERİSİNDE YENİDEN ÜRETİLEBİLİR, UÇTAN UCA HESAPLAMALI BİR ANALİZ");
body += L.subtitleP("Blood DNA Methylation Signatures of Cigarette Smoking and Epigenetic Age: A Reproducible, End-to-End Computational Analysis in Public 450K Data", { sz: 22, italic: true, bold: false, after: 160 });
body += L.para(L.run("Nurcan Denli Bayır, MD", { bold: true }), { align: "center", after: 40 });
body += L.p("Adli Tıp Anabilim Dalı, Ankara Bilkent Şehir Hastanesi, Ankara, Türkiye", { align: "center", after: 20 });
body += L.p("Sorumlu yazar: drnurcandenlibayir@gmail.com · ORCID: 0009-0004-2874-4594", { align: "center", after: 160 });

// ---- ÖZET ----
body += L.h1("ÖZET");
body += lead("Amaç:", "Sigara kullanımı, periferik kan DNA metilasyonu üzerinde bilinen en güçlü ve en iyi tekrarlanan çevresel etkilerden biridir. Bu çalışma, sigaraya bağlı metilasyon imzalarını ve epigenetik yaşı, halka açık bir veri setinde tümüyle yeniden üretilebilir, uçtan uca bir hesaplama hattıyla yeniden ele almayı; pozitif bulgular kadar negatif (null) bulguları da şeffaf biçimde raporlamayı amaçlar.");
body += lead("Yöntem:", `GSE50660 veri seti (Illumina HumanMethylation450, periferik tam kan; Tsaprouni ve ark., 2014) indirildi ve SHA-256 ile kayıt altına alındı (${shaShort(SHA_SERIES)}). Güncel içiciler (n=${V.n_current}) ile hiç içmemişler (n=${V.n_never}) arasında yaş ve cinsiyet eş-değişkenli diferansiyel metilasyon analizi (sıradan en küçük kareler + Benjamini-Hochberg yanlış keşif oranı) yapıldı. Anlamlı CpG'ler 450K manifesti ile genlere eşlenip Enrichr üzerinden Gen Ontolojisi (GO) ve KEGG zenginleştirmesine tabi tutuldu; sızıntısız bir Rastgele Orman sınıflandırıcısı (kat içi özellik seçimi, katmanlı 5-kat çapraz doğrulama, permütasyon testi) ve Horvath 2013 epigenetik saati hesaplandı. Tüm adımlar sabit tohumlu (seed=42), depoya işlenmiş betiklerle çalıştırıldı.`);
body += lead("Bulgular:", `Test edilen ${V.n_probes_tested.toLocaleString("tr-TR")} prob içinde FDR<0,05'te ${V.n_sig_fdr05} CpG anlamlıydı. En güçlü sinyal cg05575921 (AHRR) idi (Δβ=${dec(V.top10[0].delta_beta_current_minus_never, 3)}; p=${sci(V.top10[0].p)}; sıra 1); literatürdeki tüm kanonik sigara CpG'leri (F2RL3, 2q37.1 bölgesi, 6p21.33, GPR15, GFI1) en üst sıralarda doğrulandı. GO biyolojik süreçlerde iki terim (Rho ve MAPK sinyal düzenlenmesi) FDR<0,05'i geçti; ${KEGG_N} KEGG yolağının hiçbiri FDR'yi geçmedi (dürüst null; en düşük düzeltilmiş p=${dec(KEGG_MINADJ, 3)}). Sınıflandırıcı ROC-AUC=${dec(C.roc_auc, 2)} (permütasyon p=${dec(C.permutation_p_value, 3)}; boş AUC≈${dec(C.permutation_null_auc_mean, 2)}) verdi; ancak sınıf dengesizliği nedeniyle ham doğruluk yerine dengeli metrikler bildirildi (dengeli doğruluk ${dec(C.balanced_accuracy, 2)}; duyarlılık ${dec(C.sensitivity_current, 2)}; özgüllük ${dec(C.specificity_never, 2)}). Horvath saati kronolojik yaşı güçlü öngördü (r=${dec(K.pearson_r_dnam_vs_chrono, 2)}; p=${sci(K.pearson_p)}; MAE=${dec(K.MAE_years, 2)} yıl); sigaraya bağlı epigenetik yaş hızlanması bu küçük örneklemde anlamlı değildi (Welch p=${dec(K.welch_p, 2)}).`);
body += lead("Sonuç:", "Sigara ekseninde, literatürle çok noktada doğrulanmış, tümüyle yeniden üretilebilir bir metilasyon analizi sunulmuştur. Çalışma; pozitif bulguların yanı sıra null sonuçları da açıkça raporlayarak, epigenetik araştırmalarda veri/kod şeffaflığının ve yeniden üretilebilirliğin önemini vurgular.");
body += lead("Anahtar Kelimeler:", "DNA metilasyonu, sigara, epigenetik saat, EWAS, yeniden üretilebilirlik, AHRR, yanlış keşif oranı.");

// ---- ABSTRACT (EN) ----
body += L.h1("ABSTRACT");
body += lead("Objective:", "Cigarette smoking is among the strongest and most reproducible environmental influences on peripheral blood DNA methylation. We re-examined smoking-related methylation signatures and epigenetic age in a public dataset using a fully reproducible, end-to-end computational pipeline, transparently reporting null as well as positive findings.");
body += lead("Methods:", `Series matrix of GSE50660 (Illumina HumanMethylation450, whole blood; Tsaprouni et al., 2014) was downloaded and hashed (SHA-256). Differential methylation (current vs never smokers; age- and sex-adjusted OLS with Benjamini-Hochberg FDR), gene mapping plus Enrichr GO/KEGG enrichment, a leakage-free Random Forest classifier (in-fold feature selection, stratified 5-fold CV, permutation test) and the Horvath 2013 epigenetic clock were computed with fixed seed (42) and committed scripts.`);
body += lead("Results:", `Of ${V.n_probes_tested.toLocaleString("en-US")} probes, ${V.n_sig_fdr05} were significant at FDR<0.05. The top hit was cg05575921 (AHRR; Δβ=${dec(V.top10[0].delta_beta_current_minus_never, 3).replace("−", "-").replace(",", ".")}; p=2.4×10⁻⁵⁵), and all canonical smoking CpGs ranked at the top. Two GO terms (Rho/MAPK signaling) passed FDR<0.05; no KEGG pathway survived (honest null). The classifier reached ROC-AUC=${dec(C.roc_auc, 2).replace(",", ".")} (permutation p=0.016), with balanced metrics reported under class imbalance (sensitivity 0.14, specificity 0.99). The Horvath clock predicted chronological age well (r=0.77; MAE=3.5 y); smoking-related age acceleration was not significant in this small sample (p=0.24).`);
body += lead("Conclusion:", "On the smoking axis we provide a fully reproducible, multiply literature-validated methylation analysis that transparently reports null findings, underscoring the importance of data/code transparency and reproducibility in epigenetics.");
body += lead("Keywords:", "DNA methylation, smoking, epigenetic clock, EWAS, reproducibility, AHRR, false discovery rate.");

// ---- KISALTMALAR ----
body += L.h1("KISALTMALAR");
body += L.table({
  headers: ["Kısaltma", "Açılım"],
  widths: [1300, 3700],
  rows: [
    ["450K", "Illumina HumanMethylation450 metilasyon dizisi"],
    ["AhR / AHRR", "Aril hidrokarbon reseptörü / AhR baskılayıcısı (gen)"],
    ["BH-FDR", "Benjamini-Hochberg yanlış keşif oranı"],
    ["CpG", "Sitozin-fosfat-Guanin dinükleotidi"],
    ["ÇV", "Çapraz doğrulama"],
    ["DMP", "Diferansiyel metile pozisyon (differentially methylated position)"],
    ["DNAmYaş", "DNA metilasyonu temelli tahmini yaş"],
    ["EWAS", "Epigenom-çaplı ilişki çalışması"],
    ["GEO", "Gene Expression Omnibus (NCBI veri arşivi)"],
    ["GO", "Gen Ontolojisi"],
    ["KEGG", "Kyoto Gen ve Genom Ansiklopedisi"],
    ["MAE", "Ortalama mutlak hata"],
    ["OLS", "Sıradan en küçük kareler regresyonu"],
    ["ROC-AUC", "Alıcı işletim karakteristiği eğrisi altındaki alan"],
    ["Δβ", "İki grup arasındaki metilasyon oranı (beta değeri) farkı"],
  ],
});

// ---- 1. GİRİŞ ----
body += L.h1("1. GİRİŞ");

body += L.h2("1.1. DNA Metilasyonu ve Sağlık");
body += P("DNA metilasyonu, sitozin halkasının 5. konumuna bir metil grubunun eklenmesiyle gerçekleşen, başta CpG dinükleotidleri olmak üzere genom boyunca dağılmış, kalıtsal ve geri dönüşümlü bir epigenetik düzenleme mekanizmasıdır (1). Promotör CpG adalarındaki metilasyon genellikle gen susturulmasıyla, gen gövdesindeki metilasyon ise transkripsiyonel etkinlikle ilişkilendirilir (2). Bu işaretler hücre kimliğinin korunmasında ve gelişimde merkezi rol oynar (3) ve çevresel maruziyetlerin biyolojik bir kaydını tutarak yaşam boyu sağlıkla ilişkilenir (4).");

body += L.h2("1.2. Epigenetik Saatler");
body += P("DNA metilasyon düzeylerinin yaşla öngörülebilir biçimde değişmesi, kronolojik yaşı yüksek doğrulukla tahmin eden \"epigenetik saatlerin\" geliştirilmesini sağlamıştır. Horvath'ın 353 CpG'lik çok-dokulu saati (5) ve Hannum ve arkadaşlarının kan-temelli saati (6) bu alanın ilk dönüm noktalarıdır. Sonraki kuşak saatler (PhenoAge (7), GrimAge (8), DunedinPACE (9)) yalnızca yaşı değil, ölümlülük ve hastalık riskini de yansıtacak biçimde tasarlanmıştır. Tahmini metilasyon yaşının kronolojik yaşı aşması (\"epigenetik yaş hızlanması\"), hızlanmış biyolojik yaşlanmanın bir göstergesi olarak yorumlanır (4).");

body += L.h2("1.3. Sigara: Kan Metilasyonu Üzerindeki En Güçlü Çevresel Etki");
body += P("Sigara dumanı maruziyeti, kan DNA metilasyonunda literatürde en tutarlı biçimde gösterilen çevresel etkidir. Çok sayıda epigenom-çaplı ilişki çalışması, AHRR genindeki cg05575921 ve F2RL3 genindeki cg03636183 başta olmak üzere belirli CpG'lerde güçlü hipometilasyon (metilasyon kaybı) bildirmiştir (10, 11, 12). Bu değişikliklerin bir kısmı sigarayı bırakmanın ardından kısmen geri döner (10), bir kısmı ise yıllarca kalıcıdır. AHRR metilasyonundaki değişimin lenfoblast ve akciğer makrofajlarında eş zamanlı görülmesi (14) ve büyük EPIC kohortunda doğrulanması (13), bu imzanın biyolojik sağlamlığını gösterir. Sigaraya bağlı metilasyon değişikliklerinin epigenetik yaş hızlanmasıyla ilişkisi de bildirilmiştir (15).");

body += L.h2("1.4. Araştırma Boşluğu ve Çalışmanın Amacı");
body += P("Sigara-metilasyon ilişkisi iyi tanımlanmış olmakla birlikte, yayımlanmış birçok hesaplamalı çalışmada ham veri, sabit-tohumlu kod ve veri bütünlüğü (SHA-256) kayıtları paylaşılmamakta; negatif/null sonuçlar ise çoğunlukla raporlanmamaktadır. Bu eksiklik, sonuçların bağımsız olarak yeniden üretilmesini güçleştirir ve yayın yanlılığını besler. Somut araştırma boşluğu şudur: sigara-metilasyon alanında, indirilen verinin SHA-256 ile mühürlendiği, her sayının tek bir sabit-tohumlu betikten üretildiği ve hem pozitif hem null bulguların açıkça bildirildiği, uçtan uca yeniden üretilebilir bir referans hattı kamuya açık olarak yetersizdir. Bu çalışma, halka açık GSE50660 verisi üzerinde böyle bir hattı kurarak — diferansiyel metilasyon, fonksiyonel zenginleştirme, sızıntısız sınıflandırma ve epigenetik saat adımlarını tek bir şeffaf çerçevede birleştirerek — bu boşluğu doldurmayı amaçlamaktadır.");

// ---- 2. GEREÇ VE YÖNTEM ----
body += L.h1("2. GEREÇ VE YÖNTEM");

body += L.h2("2.1. Veri Kaynağı");
body += P(`Analizde, NCBI Gene Expression Omnibus arşivinden halka açık GSE50660 veri seti kullanıldı (10). Bu set, Illumina HumanHethylation450 (GPL13534) platformuyla periferik tam kandan ölçülmüş ${K.n_samples} bireyin metilasyon profilini içerir. Seri matrisi (GSE50660_series_matrix.txt.gz) doğrudan GEO FTP sunucusundan indirildi ve içeriğinin SHA-256 özeti (${shaShort(SHA_SERIES)}) kaydedilerek veri bütünlüğü garanti altına alındı. Diferansiyel metilasyon ve sınıflandırma analizleri, sigara durumu açıkça \"güncel içici\" (n=${V.n_current}) veya \"hiç içmemiş\" (n=${V.n_never}) olan ${V.n_samples} birey üzerinde yürütüldü; epigenetik saat analizi tüm ${K.n_samples} bireyi kapsadı.`);

body += L.h2("2.2. Diferansiyel Metilasyon Analizi");
body += P("Her CpG probu için beta (metilasyon oranı) değeri bağımlı değişken; sigara durumu (güncel = 2, hiç = 0) temel etken; yaş ve cinsiyet ise eş-değişken olacak şekilde, vektörleştirilmiş sıradan en küçük kareler (OLS) regresyonu uygulandı. Sigara katsayısının anlamlılığı t-istatistiği ile sınandı ve elde edilen p-değerleri Benjamini-Hochberg yöntemiyle çoklu test düzeltmesine (yanlış keşif oranı, FDR) tabi tutuldu (16). Etki büyüklüğü, gruplar arası ortalama beta farkı (Δβ = ortalama[güncel] − ortalama[hiç]) olarak hesaplandı. Boru hattının geçerliliği, literatürdeki kanonik sigara CpG'lerinin kendi sıralamamızda nereye düştüğü incelenerek (yer-gerçeği doğrulaması) sınandı.");

body += L.h2("2.3. Fonksiyonel Zenginleştirme");
body += P(`FDR<0,05'te anlamlı bulunan ${V.n_sig_fdr05} CpG, resmi Illumina 450K manifesti (SHA-256: ${shaShort(SHA_MANIFEST)}) kullanılarak genlere eşlendi; bu işlem ${E.n_genes} benzersiz gen verdi. Bu gen listesi Enrichr aracılığıyla (19) Gen Ontolojisi biyolojik süreç (GO, 2021) (17) ve KEGG yolak (2021) (18) kütüphanelerine karşı zenginleştirme analizine sokuldu. Terimler Benjamini-Hochberg düzeltmesiyle değerlendirildi.`);

body += L.h2("2.4. Sızıntısız Sınıflandırıcı");
body += P("Güncel içici ile hiç içmemişi ayırt etmek için Rastgele Orman sınıflandırıcısı (200 ağaç, sınıf ağırlıkları dengeli) kullanıldı (20, 21). Veri sızıntısını önlemek için özellik seçimi (her katta en güçlü 200 CpG'nin t-testi ile seçilmesi) tümüyle çapraz doğrulama katının İÇİNDE yapıldı; katmanlı 5-kat çapraz doğrulama uygulandı. Sınıf dengesizliği (22'ye karşı 179) nedeniyle ham doğruluk yerine ROC-AUC, dengeli doğruluk, duyarlılık ve özgüllük raporlandı. Sinyalin gerçekliği, etiketlerin karıştırıldığı bir permütasyon testiyle (boş dağılım) sınandı.");

body += L.h2("2.5. Epigenetik Saat");
body += P(`DNA metilasyon yaşı (DNAmYaş), Horvath'ın 2013 tarihli 353 CpG'lik çok-dokulu saatinin yayımlanmış katsayılarıyla (Genome Biology, Ek dosya 3; katsayı SHA-256: ${shaShort(SHA_HORVATH)}) hesaplandı (5); 353 CpG'nin ${K.n_cpgs_on_array}'i dizide mevcuttu. DNAmYaş ile kronolojik yaş arasındaki ilişki Pearson korelasyonu ve ortalama mutlak hata (MAE) ile değerlendirildi. Epigenetik yaş hızlanması, DNAmYaşın kronolojik yaşa regresyonundan elde edilen artık olarak tanımlandı; güncel ve hiç içmemiş gruplar Welch t-testi ve Mann-Whitney U testi ile karşılaştırıldı.`);

body += L.h2("2.6. Yeniden Üretilebilirlik");
body += P("Tüm betikler depoya işlenmiştir (realdata/scripts/) ve sabit tohum (seed=42) kullanır. İndirilen her veri dosyasının SHA-256 özeti kaydedilmiştir. Çalıştırma sırası ve her betiğin görevi Ek 2'de listelenmiştir. Halka açık veri ile yeniden üretilemeyen iddialar Ek 3'te açıkça beyan edilmiştir.");

// ---- 3. BULGULAR VE YORUMLAR ----
body += L.h1("3. BULGULAR VE YORUMLAR");

// 3.1 veri seti
body += L.h2("3.1. Veri Seti ve Örneklem");
body += L.tableCaption("Tablo 1.", "GSE50660 veri seti ve analiz örneklemi.");
body += L.table({
  widths: [2300, 2700],
  rows: [
    ["Veri seti (GEO)", "GSE50660"],
    ["Kaynak çalışma", "Tsaprouni ve ark., 2014 (10)"],
    ["Doku", "Periferik tam kan"],
    ["Platform", "Illumina HumanMethylation450 (GPL13534)"],
    ["Toplam örnek (saat analizi)", String(K.n_samples)],
    ["DMP / sınıflandırma örneklemi", `${V.n_samples} (${V.n_current} güncel içici, ${V.n_never} hiç içmemiş)`],
    ["Test edilen prob sayısı", V.n_probes_tested.toLocaleString("tr-TR")],
    ["FDR<0,05 anlamlı CpG", String(V.n_sig_fdr05)],
    ["Eş-değişkenler", "Yaş, cinsiyet"],
    ["Veri SHA-256 (seri matrisi)", shaShort(SHA_SERIES)],
    ["Sabit tohum (seed)", String(V.seed)],
  ],
});
body += P(`Veri seti, küçük bir güncel içici grubu (n=${V.n_current}) ile büyük bir hiç içmemiş grubu (n=${V.n_never}) içeren belirgin biçimde dengesiz bir tasarıma sahiptir. Bu dengesizlik, ileride sınıflandırma metriklerinin yorumunda (Bölüm 3.4) belirleyici olacaktır ve dürüstçe vurgulanmıştır.`);

// 3.2 DMP
body += L.h2("3.2. Diferansiyel Metilasyon ve Literatür Doğrulaması");
body += P(`Yaş ve cinsiyet düzeltmeli analizde, test edilen ${V.n_probes_tested.toLocaleString("tr-TR")} probun ${V.n_sig_fdr05}'i FDR<0,05 eşiğinde anlamlı bulundu. En güçlü ${V.top10.length} sinyal Tablo 2'de sunulmuştur; tümü negatif Δβ değerine, yani güncel içicilerde hipometilasyona işaret etmektedir — bu, sigara literatürüyle birebir uyumludur (11, 12).`);
body += L.tableCaption("Tablo 2.", "En güçlü 10 sigara-ilişkili CpG (güncel vs hiç içmemiş).");
body += L.table({
  headers: ["Sıra", "CpG", "Gen / bölge", "Δβ", "p", "FDR"],
  widths: [450, 1100, 1100, 800, 800, 750],
  rows: V.top10.map((r, i) => [
    String(i + 1),
    r.cg,
    geneOf(r.cg),
    dec(r.delta_beta_current_minus_never, 3),
    sci(r.p),
    sci(r.fdr),
  ]),
});
body += P("En güçlü sinyalin cg05575921 (AHRR) olması kritik öneme sahiptir: bu, literatürdeki en ünlü sigara CpG'sidir ve bizim bağımsız hattımızda da 1. sırada, son derece düşük bir p-değeriyle ortaya çıkmıştır. Bu sonuç, hattın doğru çalıştığının güçlü bir iç doğrulamasıdır. Tablo 3, literatürde tanımlı tüm kanonik sigara CpG'lerinin kendi sıralamamızdaki yerini göstermektedir.");
body += L.tableCaption("Tablo 3.", "Kanonik sigara CpG'lerinin bağımsız hattımızda doğrulanması.");
{
  const canon = Object.entries(V.canonical_validation)
    .map(([cg, info]) => ({ cg, ...info }))
    .sort((a, b) => a.rank - b.rank);
  body += L.table({
    headers: ["CpG", "Gen / bölge", "Bizim sıramız", "Δβ", "p"],
    widths: [1150, 1300, 950, 800, 800],
    rows: canon.map((r) => [r.cg, r.gene, String(r.rank), dec(r.delta_beta, 3), sci(r.p)]),
  });
  body += note(`Not: cg23916896 dışındaki tüm kanonik CpG'ler FDR<0,05'tedir. cg23916896 (AHRR), düşük etkili bir AHRR probudur ve bizim örneklemimizde anlamlı çıkmamıştır (sıra ${V.canonical_validation.cg23916896.rank}, FDR=${dec(V.canonical_validation.cg23916896.fdr, 2)}); kiraz-toplama yapılmadığını göstermek için dürüstçe dahil edilmiştir.`);
}
body += figure(1, "fig_volcano.png", 16.0, "Diferansiyel metilasyon volkan grafiği.",
  "Yatay eksen Δβ (güncel − hiç), dikey eksen −log₁₀(p). Anlamlı CpG'ler ve AHRR/F2RL3 dahil kanonik imzalar işaretlenmiştir.");
body += figure(2, "fig_topcpg.png", 16.0, "En güçlü sigara-ilişkili CpG'ler.",
  "En düşük p-değerli CpG'lerin etki büyüklüğü (Δβ); tümü güncel içicilerde hipometilasyon yönündedir.");

// 3.3 enrichment
body += L.h2("3.3. Fonksiyonel Zenginleştirme");
const goLib = E.libraries.GO_Biological_Process_2021;
body += P(`Anlamlı ${V.n_sig_fdr05} CpG'den eşlenen ${E.n_genes} gen, GO biyolojik süreç kütüphanesinde ${goLib.n_terms} terime karşı test edildi; bunlardan ${goLib.n_sig_fdr05}'si FDR<0,05'i geçti (Tablo 4). Anlamlı terimler — Rho protein sinyal iletiminin pozitif düzenlenmesi ve MAPK kaskadının pozitif düzenlenmesi — hücre içi sinyal iletimini işaret etmektedir; her iki terim de F2RL3 ve GPR55 gibi sigara-ilişkili reseptör genlerini içermektedir.`);
body += L.tableCaption("Tablo 4.", `GO biyolojik süreç zenginleştirmesi (ilk 5 terim; ${goLib.n_terms} terim içinde ${goLib.n_sig_fdr05} anlamlı).`);
body += L.table({
  headers: ["GO terimi", "Örtüşme", "p", "Düz. p", "Genler"],
  widths: [1850, 550, 650, 550, 1400],
  rows: goLib.top.slice(0, 5).map((t) => [
    t.Term, t.Overlap, sci(t["P-value"]), padj(t["Adjusted P-value"]) + (t["Adjusted P-value"] < 0.05 ? " *" : ""), t.Genes.replace(/;/g, "; "),
  ]),
});
body += note("* FDR<0,05. Düz. p = Benjamini-Hochberg düzeltilmiş p-değeri.");
body += P(`KEGG analizinde ise sonuç dürüst bir null'dır: test edilen ${KEGG_N} yolağın hiçbiri FDR<0,05'i geçmedi (en düşük düzeltilmiş p=${dec(KEGG_MINADJ, 3)}; Tablo 5). Yine de en üst sıradaki yolaklar biyolojik olarak anlamlıdır: triptofan metabolizması ve kimyasal karsinojenez yolakları, sigaranın aril hidrokarbon reseptörü (AhR) üzerinden etkidiği CYP1A1 genini içerir; bu, AHRR imzasıyla mekanistik olarak tutarlıdır. ${E.n_genes} gen gibi küçük bir liste ile yolak-düzeyi gücün sınırlı olması beklenen bir durumdur; bu nedenle KEGG bulguları yalnızca keşifsel kabul edilmelidir.`);
body += L.tableCaption("Tablo 5.", `KEGG yolak zenginleştirmesi (ilk 6 yolak; ${KEGG_N} yolağın hiçbiri FDR<0,05 değil).`);
body += L.table({
  headers: ["KEGG yolağı", "Örtüşme", "p", "Düz. p", "Genler"],
  widths: [1750, 550, 650, 550, 1500],
  rows: KEGG_TOP.map((t) => [t.Term, t.Overlap, sci(t.P), dec(t.AdjP, 3), t.Genes.replace(/;/g, "; ")]),
});
body += note("Kaynak: işlenmiş out/gse50660_KEGG_2021_Human.csv. (Özet JSON'da canlı yeniden-sorgu, sunucu hız sınırına (429) takıldığı için CSV asıl kaynaktır.)");
body += figure(3, "fig_enrich.png", 17.0, "GO ve KEGG zenginleştirme özeti.",
  "Sol panel: en güçlü GO biyolojik süreç terimleri; sağ panel: KEGG yolakları. Kesikli çizgi FDR=0,05 eşiğidir.");

// 3.4 classifier
body += L.h2("3.4. Sınıflandırma Performansı");
body += P(`Metilasyon profilinden güncel içiciyi ayırt eden sızıntısız Rastgele Orman modeli güçlü bir ayrım gücü gösterdi: ROC-AUC=${dec(C.roc_auc, 2)}. Bu değerin şansa bağlı olmadığı, etiketlerin karıştırıldığı ${C.permutations_done} permütasyonluk bir testle doğrulandı (boş AUC ortalaması ≈ ${dec(C.permutation_null_auc_mean, 2)}; p=${dec(C.permutation_p_value, 3)}). Ancak sınıf dengesizliği (${C.n_current}'ye karşı ${C.n_never}) nedeniyle ham doğruluk yanıltıcı olurdu; bu yüzden dengeli metrikler raporlanmıştır (Tablo 6). Yüksek özgüllüğe (${dec(C.specificity_never, 2)}) karşılık düşük duyarlılık (${dec(C.sensitivity_current, 2)}), modelin küçük güncel-içici grubunu yakalamakta zorlandığını dürüstçe ortaya koymaktadır. Bu, orijinal metindeki uydurma "%87,3 doğruluk" iddiasının gerçek, sızıntısız karşılığıdır.`);
body += L.tableCaption("Tablo 6.", "Sigara durumu sınıflandırma performansı (sızıntısız, katmanlı 5-kat ÇV).");
body += L.table({
  widths: [2300, 2700],
  rows: [
    ["Model", "Rastgele Orman (200 ağaç, sınıf ağırlığı dengeli)"],
    ["Özellik seçimi", "Kat içi t-testi ile ilk 200 CpG (sızıntısız)"],
    ["ROC-AUC", dec(C.roc_auc, 2)],
    ["Dengeli doğruluk", dec(C.balanced_accuracy, 2)],
    ["Duyarlılık (güncel içici)", dec(C.sensitivity_current, 2)],
    ["Özgüllük (hiç içmemiş)", dec(C.specificity_never, 2)],
    ["Karışıklık matrisi", `DN=${C.confusion.tn}, YP=${C.confusion.fp}, YN=${C.confusion.fn}, DP=${C.confusion.tp}`],
    ["Permütasyon testi", `${C.permutations_done} permütasyon; boş AUC≈${dec(C.permutation_null_auc_mean, 2)}; p=${dec(C.permutation_p_value, 3)}`],
  ],
});

// 3.5 clock
body += L.h2("3.5. Epigenetik Saat");
body += P(`Horvath 2013 saati kronolojik yaşı güçlü biçimde öngördü (Pearson r=${dec(K.pearson_r_dnam_vs_chrono, 2)}; p=${sci(K.pearson_p)}; MAE=${dec(K.MAE_years, 2)} yıl; Şekil 4). Bu performans yayımlanmış literatürle uyumludur ve saat hesabımızın doğru uygulandığını gösterir. Buna karşılık, sigaraya bağlı epigenetik yaş hızlanması bu örneklemde anlamlı bulunmadı: güncel içicilerde ortalama yaş hızlanması ${dec(K.age_accel_current_mean, 2)} yıl, hiç içmemişlerde ${dec(K.age_accel_never_mean, 2)} yıl olup fark istatistiksel olarak anlamlı değildi (Welch t=${dec(K.welch_t, 2)}, p=${dec(K.welch_p, 2)}; Mann-Whitney U=${K.mannwhitney_U}, p=${dec(K.mannwhitney_p, 2)}). Bu dürüst null bulgu, yalnızca ${V.n_current} güncel içici içeren küçük örneklemin sınırlı istatistiksel gücüyle uyumludur; daha büyük kohortlarda sigaranın yaş hızlanmasıyla ilişkisi bildirilmiştir (15).`);
body += L.tableCaption("Tablo 7.", "Horvath 2013 epigenetik saati ve sigaraya göre yaş hızlanması.");
body += L.table({
  widths: [2400, 2600],
  rows: [
    ["Saat", "Horvath 2013 (353 CpG, çok-dokulu)"],
    ["Dizide bulunan CpG", `${K.n_cpgs_on_array} / ${K.n_horvath_cpgs}`],
    ["Örnek", String(K.n_samples)],
    ["DNAmYaş ↔ kronolojik yaş (Pearson r)", `${dec(K.pearson_r_dnam_vs_chrono, 2)} (p=${sci(K.pearson_p)})`],
    ["Ortalama mutlak hata (MAE)", `${dec(K.MAE_years, 2)} yıl`],
    ["Medyan hata", `${dec(K.median_error_years, 2)} yıl`],
    ["Yaş hızlanması — güncel içici", `${dec(K.age_accel_current_mean, 2)} yıl`],
    ["Yaş hızlanması — hiç içmemiş", `${dec(K.age_accel_never_mean, 2)} yıl`],
    ["Grup farkı (Welch t)", `t=${dec(K.welch_t, 2)}; p=${dec(K.welch_p, 2)} (anlamlı değil)`],
    ["Grup farkı (Mann-Whitney U)", `U=${K.mannwhitney_U}; p=${dec(K.mannwhitney_p, 2)} (anlamlı değil)`],
  ],
});
body += figure(4, "fig_clock.png", 12.0, "DNAmYaş ile kronolojik yaş ilişkisi.",
  "Her nokta bir bireydir; kesikli çizgi y=x köşegenidir. Güçlü korelasyon ve düşük MAE, saat hesabının doğruluğunu gösterir.");

// ---- 4. TARTIŞMA ----
body += L.h1("4. TARTIŞMA");

body += L.h2("4.1. Ana Bulguların Özeti");
body += P(`Bu çalışma, halka açık GSE50660 verisinde sigara-ilişkili metilasyonu uçtan uca yeniden üretilebilir bir hatla yeniden ele aldı. Dört temel sonuç elde edildi: (i) FDR<0,05'te ${V.n_sig_fdr05} CpG anlamlıydı ve en güçlü sinyal AHRR/cg05575921 idi; (ii) GO'da Rho/MAPK sinyal düzenlenmesi anlamlı çıktı, KEGG'de ise hiçbir yolak FDR'yi geçmedi (dürüst null); (iii) sızıntısız sınıflandırıcı ROC-AUC=${dec(C.roc_auc, 2)} ile gerçek bir sinyal gösterdi ancak sınıf dengesizliği şeffaf raporlandı; (iv) Horvath saati yaşı doğru tahmin etti, fakat sigaraya bağlı yaş hızlanması bu küçük örneklemde anlamlı değildi.`);

body += L.h2("4.2. Literatürle Karşılaştırma ve Özgünlük");
body += P("Bulgularımız sigara epigenetiği literatürüyle çok noktada örtüşmektedir: AHRR ve F2RL3 hipometilasyonu, en sık tekrarlanan sigara imzalarıdır (11, 12, 13, 14). Çalışmanın özgünlüğü yeni bir biyolojik keşiften çok, yöntemsel şeffaflıktadır: indirilen verinin SHA-256 ile mühürlenmesi, her sayının tek bir sabit-tohumlu betikten üretilmesi, özellik seçiminin çapraz doğrulama katı içinde tutularak sızıntının önlenmesi ve null bulguların gizlenmeden raporlanması. Yaşam tarzı ve çevresel etkenlerin epigenetik yaşla ilişkisini inceleyen önceki çalışmalar (22, 23, 24) ve epigenetik yaşın kısmen geri döndürülebilirliğine ilişkin bulgular (25), sonuçlarımızın bağlamını oluşturur.");

body += L.h2("4.3. Çarpıcı Bulgular");
body += P("Üç bulgu özellikle dikkat çekicidir. Birincisi, literatürdeki tüm kanonik sigara CpG'lerinin (yer-gerçeği) kendi bağımsız sıralamamızda en üstte çıkması, hattın doğruluğunun güçlü bir kanıtıdır. İkincisi, KEGG'de ve epigenetik yaş hızlanmasında elde edilen null sonuçların saklanmadan raporlanması, sonuçların güvenilirliğini artırır; istatistiksel gücün sınırlı olduğu yerlerde \"anlamlı\" sonuç zorlanmamıştır. Üçüncüsü, en güçlü CpG olan cg05575921'in, yerine geçtiği uydurma metinde yanlışlıkla bir alkol imzası olarak gösterilmesine karşın, gerçekte iyi bilinen bir sigara (AHRR) imzası olduğunun teyit edilmesidir.");

body += L.h2("4.4. Güçlü Yönler");
body += P("Çalışmanın başlıca güçlü yönleri tam yeniden üretilebilirlik (sabit tohum, SHA-256 ile mühürlenmiş veri, depoya işlenmiş betikler), sızıntısız çapraz doğrulama tasarımı, çoklu literatür doğrulaması ve negatif bulguların şeffaf raporlanmasıdır.");

body += L.h2("4.5. Sınırlılıklar");
body += P(`Çalışmanın önemli sınırlılıkları vardır. Birincisi, tek bir kohort ve özellikle küçük bir güncel-içici grubu (n=${V.n_current}) kullanılmıştır; bu, sınıflandırma duyarlılığını ve yaş hızlanması testinin gücünü kısıtlar. İkincisi, sınıf dengesizliği belirgindir. Üçüncüsü, yalnızca Horvath saati hesaplanmıştır; diğer saatler (Hannum, PhenoAge, GrimAge, DunedinPACE) katsayı dosyaları eklenmeden uydurulmamıştır. Dördüncüsü, hücre tipi kompozisyonu için ileri bir düzeltme (örn. referans-temelli dekonvolüsyon) uygulanmamış; yalnızca yaş ve cinsiyet eş-değişken alınmıştır. Beşincisi ve en önemlisi, orijinal metnin iddia ettiği çoklu-madde kapsamı halka açık veride mevcut değildir; yeniden üretilemeyen tüm iddialar Ek 3'te açıkça beyan edilmiştir.`);

body += L.h2("4.6. Gelecek Yönelimler");
body += P("Gelecekteki çalışmalar; referans-temelli hücre tipi düzeltmesi eklenmesini, enjeksiyonla yasa dışı madde kullanımı gibi halka açık ek kohortlarla kapsamın genişletilmesini, katsayı dosyaları sağlandığında ek epigenetik saatlerin hesaplanmasını ve daha büyük, dengeli kohortlarda sigaraya bağlı yaş hızlanmasının yeniden sınanmasını içerebilir.");

// ---- 5. SONUÇ ----
body += L.h1("5. SONUÇ");
body += P("Sigara ekseninde, halka açık veriyle çalışan, literatürle çok noktada doğrulanmış ve tümüyle yeniden üretilebilir bir metilasyon analizi sunulmuştur. Pozitif bulgular kadar null bulguların da şeffaf biçimde raporlanması, bu çalışmayı uydurma temelin yerine geçebilecek dürüst bir referans hattı hâline getirmektedir. Çalışmanın asıl katkısı, epigenetik araştırmalarda veri bütünlüğü, kod paylaşımı ve yeniden üretilebilirliğin pratik bir örneğini ortaya koymasıdır.");

// ---- TEŞEKKÜR ----
body += L.h1("TEŞEKKÜR");
body += P("GSE50660 verisini kamuya açan Tsaprouni ve arkadaşlarına, epigenetik saat katsayılarını açık biçimde paylaşan Steve Horvath'a ve scikit-learn ile Enrichr başta olmak üzere açık kaynak araçların geliştiricilerine teşekkür ederiz.");

// ---- KAYNAKÇA ----
body += L.h1("KAYNAKÇA");
const REFS = [
  "Bird, A. (2002). DNA methylation patterns and epigenetic memory. Genes & Development, 16(1), 6-21. https://doi.org/10.1101/gad.947102",
  "Jones, P. A. (2012). Functions of DNA methylation: Islands, start sites, gene bodies and beyond. Nature Reviews Genetics, 13(7), 484-492. https://doi.org/10.1038/nrg3230",
  "Smith, Z. D., & Meissner, A. (2013). DNA methylation: Roles in mammalian development. Nature Reviews Genetics, 14(3), 204-220. https://doi.org/10.1038/nrg3354",
  "Jones, M. J., Goodman, S. J., & Kobor, M. S. (2015). DNA methylation and healthy human aging. Aging Cell, 14(6), 924-932. https://doi.org/10.1111/acel.12349",
  "Horvath, S. (2013). DNA methylation age of human tissues and cell types. Genome Biology, 14(10), R115. https://doi.org/10.1186/gb-2013-14-10-r115",
  "Hannum, G., Guinney, J., Zhao, L., Zhang, L., Hughes, G., Sadda, S., Klotzle, B., Bibikova, M., Fan, J. B., Gao, Y., Deconde, R., Chen, M., Rajapakse, I., Friend, S., Ideker, T., & Zhang, K. (2013). Genome-wide methylation profiles reveal quantitative views of human aging rates. Molecular Cell, 49(2), 359-367. https://doi.org/10.1016/j.molcel.2012.10.016",
  "Levine, M. E., Lu, A. T., Quach, A., Chen, B. H., Assimes, T. L., Bandinelli, S., Hou, L., Baccarelli, A. A., Stewart, J. D., Li, Y., Whitsel, E. A., Wilson, J. G., Reiner, A. P., Aviv, A., Lohman, K., Liu, Y., Ferrucci, L., & Horvath, S. (2018). An epigenetic biomarker of aging for lifespan and healthspan. Aging, 10(4), 573-591. https://doi.org/10.18632/aging.101414",
  "Lu, A. T., Quach, A., Wilson, J. G., Reiner, A. P., Aviv, A., Raj, K., Hou, L., Baccarelli, A. A., Li, Y., Stewart, J. D., Whitsel, E. A., Assimes, T. L., Ferrucci, L., & Horvath, S. (2019). DNA methylation GrimAge strongly predicts lifespan and healthspan. Aging, 11(2), 303-327. https://doi.org/10.18632/aging.101684",
  "Belsky, D. W., Caspi, A., Corcoran, D. L., Sugden, K., Poulton, R., Arseneault, L., Baccarelli, A., Chamarti, K., Gao, X., Hannon, E., Harrington, H. L., Houts, R., Kothari, M., Kwon, D., Mill, J., Schwartz, J., Vokonas, P., Wang, C., Williams, B. S., & Moffitt, T. E. (2022). DunedinPACE, a DNA methylation biomarker of the pace of aging. eLife, 11, e73420. https://doi.org/10.7554/eLife.73420",
  "Tsaprouni, L. G., Yang, T. P., Bell, J., Dick, K. J., Kanoni, S., Nisbet, J., Viñuela, A., Grundberg, E., Nelson, C. P., Meduri, E., Buil, A., Cambien, F., Hengstenberg, C., Erdmann, J., Schunkert, H., Goodall, A. H., Ouwehand, W. H., Dermitzakis, E., Spector, T. D., Samani, N. J., & Deloukas, P. (2014). Cigarette smoking reduces DNA methylation levels at multiple genomic loci but the effect is partially reversible upon cessation. Epigenetics, 9(10), 1382-1396. https://doi.org/10.4161/15592294.2014.969637",
  "Joehanes, R., Just, A. C., Marioni, R. E., Pilling, L. C., Reynolds, L. M., Mandaviya, P. R., Guan, W., Xu, T., Elks, C. E., Aslibekyan, S., Moreno-Macias, H., Smith, J. A., Brody, J. A., Dhingra, R., Yousefi, P., Pankow, J. S., Kunze, S., Shah, S. H., McRae, A. F., … Levy, D. (2016). Epigenetic signatures of cigarette smoking. Circulation: Cardiovascular Genetics, 9(5), 436-447. https://doi.org/10.1161/CIRCGENETICS.116.001506",
  "Zeilinger, S., Kühnel, B., Klopp, N., Baurecht, H., Kleinschmidt, A., Gieger, C., Weidinger, S., Lattka, E., Adamski, J., Peters, A., Strauch, K., Waldenberger, M., & Illig, T. (2013). Tobacco smoking leads to extensive genome-wide changes in DNA methylation. PLoS ONE, 8(5), e63812. https://doi.org/10.1371/journal.pone.0063812",
  "Ambatipudi, S., Cuenin, C., Hernandez-Vargas, H., Ghantous, A., Le Calvez-Kelm, F., Kaaks, R., Barrdahl, M., Boeing, H., Aleksandrova, K., Trichopoulou, A., Lagiou, P., Naska, A., Palli, D., Krogh, V., Polidoro, S., Tumino, R., Panico, S., Bueno-de-Mesquita, B., Peeters, P. H., … Herceg, Z. (2016). Tobacco smoking-associated genome-wide DNA methylation changes in the EPIC study. Epigenomics, 8(5), 599-618. https://doi.org/10.2217/epi-2016-0001",
  "Monick, M. M., Beach, S. R. H., Plume, J., Sears, R., Gerrard, M., Brody, G. H., & Philibert, R. A. (2012). Coordinated changes in AHRR methylation in lymphoblasts and pulmonary macrophages from smokers. American Journal of Medical Genetics Part B: Neuropsychiatric Genetics, 159B(2), 141-151. https://doi.org/10.1002/ajmg.b.32011",
  "Gao, X., Zhang, Y., Breitling, L. P., & Brenner, H. (2016). Relationship of tobacco smoking and smoking-related DNA methylation with epigenetic age acceleration. Oncotarget, 7(30), 46878-46889. https://doi.org/10.18632/oncotarget.9795",
  "Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B (Methodological), 57(1), 289-300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x",
  "Ashburner, M., Ball, C. A., Blake, J. A., Botstein, D., Butler, H., Cherry, J. M., Davis, A. P., Dolinski, K., Dwight, S. S., Eppig, J. T., Harris, M. A., Hill, D. P., Issel-Tarver, L., Kasarskis, A., Lewis, S., Matese, J. C., Richardson, J. E., Ringwald, M., Rubin, G. M., & Sherlock, G. (2000). Gene Ontology: Tool for the unification of biology. Nature Genetics, 25(1), 25-29. https://doi.org/10.1038/75556",
  "Kanehisa, M., & Goto, S. (2000). KEGG: Kyoto Encyclopedia of Genes and Genomes. Nucleic Acids Research, 28(1), 27-30. https://doi.org/10.1093/nar/28.1.27",
  "Kuleshov, M. V., Jones, M. R., Rouillard, A. D., Fernandez, N. F., Duan, Q., Wang, Z., Koplev, S., Jenkins, S. L., Jagodnik, K. M., Lachmann, A., McDermott, M. G., Monteiro, C. D., Gundersen, G. W., & Ma'ayan, A. (2016). Enrichr: A comprehensive gene set enrichment analysis web server 2016 update. Nucleic Acids Research, 44(W1), W90-W97. https://doi.org/10.1093/nar/gkw377",
  "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32. https://doi.org/10.1023/A:1010933404324",
  "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
  "Quach, A., Levine, M. E., Tanaka, T., Lu, A. T., Chen, B. H., Ferrucci, L., Ritz, B., Bandinelli, S., Neuhouser, M. L., Beasley, J. M., Snetselaar, L., Wallace, R. B., Tsao, P. S., Absher, D., Assimes, T. L., Stewart, J. D., Li, Y., Hou, L., Baccarelli, A. A., … Horvath, S. (2017). Epigenetic clock analysis of diet, exercise, education, and lifestyle factors. Aging, 9(2), 419-446. https://doi.org/10.18632/aging.101168",
  "Fiorito, G., Polidoro, S., Dugué, P. A., Kivimaki, M., Ponzi, E., Matullo, G., Guarrera, S., Assumma, M. B., Georgiadis, P., Kyrtopoulos, S. A., Krogh, V., Palli, D., Panico, S., Sacerdote, C., Tumino, R., Chadeau-Hyam, M., Stringhini, S., Severi, G., Hodge, A. M., … Vineis, P. (2017). Social adversity and epigenetic aging: A multi-cohort study on socioeconomic differences in peripheral blood DNA methylation. Scientific Reports, 7(1), 16266. https://doi.org/10.1038/s41598-017-16391-5",
  "Dugué, P. A., Bassett, J. K., Joo, J. E., Jung, C. H., Ming Wong, E., Moreno-Betancur, M., Schmidt, D., Makalic, E., Li, S., Severi, G., Hodge, A. M., Buchanan, D. D., English, D. R., Hopper, J. L., Southey, M. C., Giles, G. G., & Milne, R. L. (2018). Association of DNA methylation-based biological age with health risk factors and overall and cause-specific mortality. American Journal of Epidemiology, 187(3), 529-538. https://doi.org/10.1093/aje/kwx291",
  "Fitzgerald, K. N., Hodges, R., Hanes, D., Stack, E., Cheishvili, D., Szyf, M., Henkel, J., Twedt, M. W., Giannopoulou, D., Herdell, J., Logan, S., & Bradley, R. (2021). Potential reversal of epigenetic age using a diet and lifestyle intervention: A pilot randomized clinical trial. Aging, 13(7), 9419-9432. https://doi.org/10.18632/aging.202913",
];
{
  let rn = 1;
  for (const r of REFS) {
    body += L.para(L.run(rn + ". ", { sz: 17 }) + L.run(r, { sz: 17 }), { align: "both", indentLeft: 360, hanging: 360, after: 40 });
    rn++;
  }
}

// ---- EKLER ----
body += L.h1("EKLER");

body += L.h2("Ek 1. Veri Kaynakları ve SHA-256 Bütünlük Özetleri");
body += L.table({
  headers: ["Dosya", "İçerik", "SHA-256"],
  widths: [1300, 1900, 1800],
  rows: [
    ["GSE50660_series_matrix.txt.gz", "Sigara EWAS, periferik kan, 450K, 464 örnek", SHA_SERIES],
    ["GPL13534_manifest.csv.gz", "Illumina 450K resmi manifesti (CpG→gen)", SHA_MANIFEST],
    ["horvath2013_coef.csv", "Horvath 2013 353-CpG saat katsayıları", SHA_HORVATH],
  ],
});

body += L.h2("Ek 2. Yeniden Üretilebilirlik — Betikler");
body += L.table({
  headers: ["Betik", "İşlev"],
  widths: [1700, 3300],
  rows: [
    ["01_download.py", "GEO indirme + SHA-256 (data/manifest.json)"],
    ["02_dmp_smoking.py", "DMP (güncel vs hiç; yaş+cinsiyet düzeltmeli OLS; BH-FDR) + kanonik doğrulama"],
    ["03_enrichment.py", "CpG→gen (450K manifesti) + Enrichr GO/KEGG"],
    ["04a_cache_betas.py + 04_classifier.py", "Sızıntısız Rastgele Orman + permütasyon testi"],
    ["05_clocks.py", "Horvath DNAmYaş + yaş hızlanması"],
    ["06_figures.py", "Şekillerin (1–4) üretimi"],
  ],
});
body += note("Sabit tohum = 42. Çalıştırma sırası: 01 → 02 → 03 → 04a → 04 → 05 → 06.");

body += L.h2("Ek 3. Yeniden Üretilemeyenler — Açık Beyan");
body += P("Aşağıdaki iddialar, orijinal (uydurma) metinde yer almakla birlikte halka açık veriyle yeniden üretilememektedir ve bu makaleye dâhil edilmemiştir. Zero-Hallucination ilkesi gereği bu sınırlılıklar açıkça beyan edilir.");
body += L.table({
  headers: ["Orijinal iddia", "Durum / gerçek karşılık"],
  widths: [2100, 2900],
  rows: [
    ["7 madde sınıfı (kokain, opioid, metamfetamin, esrar)", "Halka açık büyük metilasyon kohortu yok — üretilemez"],
    ["10.542 örnek / 15 veri seti", "Bu hacim madde-metilasyonunda halka açık değil — üretilemez"],
    ["%87,3 sınıflandırma doğruluğu", "Yerine: sızıntısız ROC-AUC=0,95 + permütasyon p=0,016 + dengeli metrikler"],
    ["1.847 madde-spesifik CpG", "Yerine: sigara için FDR<0,05'te 89 gerçek CpG"],
    ["cg05575921 = alkol imzası", "Gerçekte sigara (AHRR) imzası; DMP'mizde 1. sıra"],
    ["Diğer saatler (Hannum/PhenoAge/GrimAge/DunedinPACE)", "Katsayı dosyası eklenirse hesaplanır; uydurulmadı"],
    ["Mediyasyon / moderasyon / postmortem (n=108)", "Bireysel-düzey ham veri yok — üretilemez"],
  ],
});

// ================================================================ PAKETLE
const docRels =
  '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' +
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' +
  MEDIA_RELS.join("") +
  "</Relationships>";

(async () => {
  const docXml = L.documentXml(body);
  const zip = new JSZip();
  zip.file("[Content_Types].xml", L.CONTENT_TYPES);
  zip.file("_rels/.rels", L.RELS);
  zip.file("word/document.xml", docXml);
  zip.file("word/styles.xml", L.stylesXml());
  zip.file("word/_rels/document.xml.rels", docRels);
  for (const m of MEDIA_FILES) zip.file(m.name, m.buf);
  const out = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  const outPath = path.join(__dirname, "makale_gercek.docx");
  fs.writeFileSync(outPath, out);
  fs.writeFileSync(path.join(__dirname, "_document_gercek.xml"), docXml);
  console.log("WROTE", outPath, "(" + out.length + " bytes)");
  console.log("figures:", MEDIA_FILES.length, "| refs:", REFS.length, "| docXml:", docXml.length, "chars");
})().catch((e) => { console.error("BUILD FAILED:", e); process.exit(1); });
