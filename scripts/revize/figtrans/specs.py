#!/usr/bin/env python3
"""Per-figure Turkish overlay specs. Run: python3 run.py [img-034-001 ...]
Translates English WORDS only; numbers, proper names (Horvath, GrimAge, gene IDs)
and standard abbreviations (MAE, RMSE, R2, EAA, PMI, ANOVA, p, d, beta) stay verbatim."""

FIGS = {
 # ---- Figure 1 — Epigenetic Clock Performance Comparison (1598x1417) ----
 "img-034-001": [
   {"box":[338,4,1216,48], "text":"", "font":"serif","bold":True},
   # panel headers (left aligned, sans bold)
   {"box":[56,113,470,147], "text":"A. Tahmin Doğruluğu (MAE)", "font":"sans","bold":True,"align":"left"},
   {"box":[880,113,1110,147], "text":"B. Model Uyumu (R²)", "font":"sans","bold":True,"align":"left"},
   {"box":[56,737,470,770], "text":"C. Kök Ortalama Kare Hata", "font":"sans","bold":True,"align":"left"},
   {"box":[983,720,1444,753], "text":"D. Çok Boyutlu Performans", "font":"sans","bold":True,"align":"left"},
   # y-axis titles (vertical)
   {"box":[4,230,36,560], "text":"Ortalama Mutlak Hata (yıl)", "font":"sans","rotate":90},
   {"box":[788,250,820,610], "text":"R² (Korelasyon)", "font":"sans","rotate":90},
   {"box":[4,938,36,1098], "text":"RMSE (yıl)", "font":"sans","rotate":90},
   # legends
   {"box":[618,164,706,187], "text":"Ortalama: 3.7", "font":"sans"},
   {"box":[1384,597,1536,621], "text":"Eşik (0.90)", "font":"sans","align":"left","color":[60,60,60]},
   # radar axis labels (exact OCR coords; size matched to originals)
   {"box":[1244,754,1340,778], "text":"Kesinlik", "font":"sans","bold":True,"color":[0,0,0],"size":20},
   {"box":[1442,1004,1528,1032], "text":"Doğruluk", "font":"sans","bold":True,"color":[0,0,0],"size":20},
   {"box":[960,850,1030,876], "text":"Hız", "font":"sans","bold":True,"color":[0,0,0],"size":20},
   {"box":[956,1150,1050,1196], "text":"Doku\nAralığı", "font":"sans","bold":True,"color":[0,0,0],"size":20},
   {"box":[1246,1246,1344,1292], "text":"Klinik\nYarar", "font":"sans","bold":True,"color":[0,0,0],"size":20},
   # footer
   {"box":[326,1382,1232,1410], "text":"Analiz, 15 bağımsız veri setinden n=10,542 DNA metilasyon profiline dayanır", "font":"sans","italic":True},
 ],
 # ---- Figure 2 — Substance-Specific Epigenetic Age Acceleration (1600x1022) ----
 "img-035-002": [
   # title
   {"box":[400,6,1300,42], "text":"", "font":"sans","bold":True,"size":30},
   # panel headers
   {"box":[150,80,735,107], "text":"A. Maddeye Özgü Epigenetik Yaş Hızlanması", "font":"sans","bold":True,"align":"left","size":22},
   {"box":[1178,80,1405,104], "text":"B. Etki Büyüklükleri", "font":"sans","bold":True,"align":"left","size":22},
   {"box":[153,566,432,592], "text":"C. EAA Sıralaması", "font":"sans","bold":True,"align":"left","size":22},
   {"box":[740,563,1052,592], "text":"D. Örneklem Dağılımı", "font":"sans","bold":True,"align":"center","size":22},
   {"box":[1178,566,1455,592], "text":"E. İstatistiksel Özet", "font":"sans","bold":True,"align":"left","size":22},
   # panel A y-axis title (rotated, reads bottom-to-top)
   {"box":[86,124,123,470], "text":"Epigenetik Yaş Hızlanması (yıl)", "font":"sans","rotate":90,"size":15,"bold":True,"bg":[255,255,255]},
   # panel A x-axis category labels: originals are ANGLED ~25deg, so clear the whole
   # strip (below the red baseline @y463) then redraw HORIZONTAL labels centered on each
   # tick. Tick centers from bar-center detection (Control inferred, no bar).
   {"box":[150,471,1060,560], "text":"", "bg":[255,255,255]},
   {"box":[181,478,301,514], "text":"Kontrol", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   {"box":[306,478,426,514], "text":"Alkol", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   {"box":[431,478,551,514], "text":"Opioidler", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   {"box":[554,478,674,514], "text":"Kokain", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   {"box":[676,478,806,514], "text":"Çoklu Madde", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   {"box":[806,478,926,514], "text":"Esrar", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   {"box":[929,478,1053,514], "text":"Metamfetamin", "font":"sans","bold":True,"size":15,"color":[16,34,56],"bg":[255,255,255]},
   # panel B y-tick labels (right-aligned at axis ~1167; box left >=1040 to clear panel A bar @1035)
   {"box":[1040,127,1167,153], "text":"Metamfetamin", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1040,180,1167,206], "text":"Esrar", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1040,232,1167,258], "text":"Çoklu Madde", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1040,287,1167,313], "text":"Kokain", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1040,340,1167,366], "text":"Opioidler", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1040,392,1167,418], "text":"Alkol", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1040,447,1167,473], "text":"Kontrol", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   # panel B legend text (dash samples kept; only words covered)
   {"box":[1466,433,1582,452], "text":"Orta etki", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1466,453,1582,471], "text":"Büyük etki", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   # panel C y-tick labels (right-aligned at axis ~148, far-left white gutter)
   {"box":[0,617,148,637], "text":"Kontrol", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[0,660,148,680], "text":"Esrar", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[0,702,148,722], "text":"Alkol", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[0,742,148,762], "text":"Opioidler", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[0,782,148,802], "text":"Kokain", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[0,822,148,842], "text":"Çoklu Madde", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[0,872,148,892], "text":"Metamfetamin", "font":"sans","align":"right","size":15,"color":[0,0,0],"bg":[255,255,255]},
   # panel C in-plot +X yr -> +X yıl (bold black, on white, right of bar ends)
   {"box":[253,658,338,678], "text":"+2.1 yıl", "font":"sans","bold":True,"align":"left","size":15,"color":[0,0,0]},
   {"box":[303,700,388,720], "text":"+3.2 yıl", "font":"sans","bold":True,"align":"left","size":15,"color":[0,0,0]},
   {"box":[376,742,461,762], "text":"+4.8 yıl", "font":"sans","bold":True,"align":"left","size":15,"color":[0,0,0]},
   {"box":[390,785,475,805], "text":"+5.1 yıl", "font":"sans","bold":True,"align":"left","size":15,"color":[0,0,0]},
   {"box":[444,818,550,840], "text":"+6.2 yıl", "font":"sans","bold":True,"align":"left","size":15,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[493,864,587,886], "text":"+7.3 yıl", "font":"sans","bold":True,"align":"left","size":15,"color":[0,0,0],"bg":[255,255,255]},
   # panel C x-axis title
   {"box":[303,930,420,955], "text":"EAA (yıl)", "font":"sans","bold":True,"align":"center","size":15,"color":[0,0,0]},
   # panel D legend (swatches kept at left; only text covered)
   {"box":[1055,685,1180,703], "text":"Kontrol", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1055,704,1180,722], "text":"Alkol", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1055,724,1180,742], "text":"Opioidler", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1055,742,1180,760], "text":"Kokain", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1055,761,1180,779], "text":"Çoklu Madde", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1055,779,1180,797], "text":"Esrar", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1055,798,1180,816], "text":"Metamfetamin", "font":"sans","align":"left","size":13,"color":[0,0,0],"bg":[255,255,255]},
   # panel E table header (white text on dark navy [9,38,70]); EAA col kept
   {"box":[1205,632,1300,653], "text":"Madde", "font":"sans","bold":True,"align":"center","size":14,"color":[255,255,255],"bg":[9,38,70]},
   {"box":[1422,632,1505,653], "text":"%95 GA", "font":"sans","bold":True,"align":"center","size":14,"color":[255,255,255],"bg":[9,38,70]},
   {"box":[1508,632,1582,653], "text":"p değeri", "font":"sans","bold":True,"align":"center","size":14,"color":[255,255,255],"bg":[9,38,70]},
   # panel E table column 1 substance names (black, centered; numbers in other cols kept)
   {"box":[1200,665,1305,684], "text":"Kontrol", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   {"box":[1200,696,1305,715], "text":"Alkol", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   {"box":[1200,726,1305,746], "text":"Opioidler", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   {"box":[1200,757,1305,776], "text":"Kokain", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   {"box":[1195,788,1310,808], "text":"Çoklu Madde", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   {"box":[1200,818,1305,838], "text":"Esrar", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   {"box":[1188,850,1318,870], "text":"Metamfetamin", "font":"sans","align":"center","size":14,"color":[0,0,0]},
   # footer (italic grey in original; numbers kept verbatim)
   {"box":[545,993,1158,1015], "text":"ANOVA: F(6,10535) = 47.3, p < 0.001 | Hata çubukları: %95 GA | Toplam n = 10,542", "font":"sans","align":"center","size":14},
 ],
 # ---- Figure 3 — Mediation Analysis (1598x1256) ----
 # Coords from tesseract OCR (ocrops.py). Colors sampled: navy box (6,39,72),
 # blue box (28,82,152), epi box (46,115,180), summary box (231,244,253)+text(17,39,62).
 # DATA KEPT VERBATIM: a=0.42***, b=0.38***, c'=0.25**, ab=0.16***, c=0.41***,
 # bar values 0.16 (39%)/0.25 (61%)/0.41 (100%), CpG IDs+genes, pie % labels,
 # CI [0.118, 0.205] etc, z=8.42, n = 10,542 (comma). a=/b= lines have NO words -> untouched.
 "img-036-003": [
   # title
   {"box":[150,6,1456,40], "text":"", "font":"sans","bold":True,"align":"center","size":22},
   # panel headers (sans bold, left)
   {"box":[104,104,440,128], "text":"A. Aracılık Yolu Modeli", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[1158,104,1442,128], "text":"B. Etki Ayrıştırması", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[103,695,425,720], "text":"C. En İyi Aracı CpG Bölgeleri", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[683,695,1006,720], "text":"D. Biyobelirteç Katkıları", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[1125,695,1435,720], "text":"E. Bootstrap Doğrulaması", "font":"sans","bold":True,"align":"left","size":18},
   # Panel A diagram boxes — white text on solid colored fills
   {"box":[160,349,286,367], "text":"Madde", "font":"sans","bold":True,"align":"center","size":14,"color":[255,255,255],"bg":[6,39,72]},
   {"box":[150,369,296,388], "text":"Kullanımı (X)", "font":"sans","bold":True,"align":"center","size":14,"color":[255,255,255],"bg":[6,39,72]},
   {"box":[495,205,660,225], "text":"DNA Metilasyon", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[28,82,152]},
   {"box":[505,225,650,242], "text":"Aracıları (M)", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[28,82,152]},
   {"box":[875,349,995,369], "text":"Epigenetik", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[46,115,180]},
   {"box":[890,369,978,388], "text":"Yaş (Y)", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[46,115,180]},
   # Panel A: c' line — keep "c' = 0.25**", only (direct)->(doğrudan)
   {"box":[676,395,765,414], "text":"(doğrudan)", "font":"sans","align":"left","size":13,"bg":[255,255,255]},
   # Panel A summary box (light-blue fill, dark navy text) — full lines, data verbatim
   {"box":[376,481,780,499], "text":"Toplam Etki: c = 0.41***", "font":"sans","bold":True,"align":"center","size":14,"color":[17,39,62],"bg":[231,244,253]},
   {"box":[376,500,780,518], "text":"Dolaylı Etki: ab = 0.16*** (%39 aracılı)", "font":"sans","bold":True,"align":"center","size":14,"color":[17,39,62],"bg":[231,244,253]},
   # Panel B category labels (right-aligned at axis ~x1150; values at bar ends kept)
   {"box":[1000,191,1152,209], "text":"Dolaylı Etki", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[990,358,1152,376], "text":"Doğrudan Etki", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1010,528,1152,546], "text":"Toplam Etki", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # Panel B x-axis title
   {"box":[1220,630,1515,647], "text":"Standartlaştırılmış Etki", "font":"sans","align":"center","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # Panel C x-axis title (CpG IDs/genes + bar % kept verbatim)
   {"box":[150,1144,470,1162], "text":"Aracılık Katkısı (%)", "font":"sans","align":"center","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # Panel D pie category labels (% values kept)
   {"box":[890,746,972,763], "text":"Sigara", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[868,762,992,776], "text":"Belirteçleri", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[560,924,685,938], "text":"İnflamasyon", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[915,1024,1040,1043], "text":"Bağışıklık", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[920,1044,1045,1059], "text":"Fonksiyonu", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1000,946,1058,964], "text":"Diğer", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[728,1080,820,1094], "text":"Metabolik", "font":"sans","align":"center","size":12,"color":[0,0,0],"bg":[255,255,255]},
   # Panel E monospace results box (white bg) — worded lines only; p-value/footnote lines skipped (no words)
   {"box":[1240,784,1497,799], "text":"ARACILIK ANALİZİ SONUÇLARI", "font":"mono","bold":True,"align":"center","size":13,"bg":[255,255,255]},
   {"box":[1244,818,1495,837], "text":"Bootstrap: 10,000 iterasyon", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1236,835,1505,851], "text":"Güven: %95 Yanlılık düzeltmeli", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1275,869,1465,887], "text":"Dolaylı Etki (ab):", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1284,887,1475,903], "text":"Nokta tahmini: 0.160", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1280,904,1475,921], "text":"%95 GA: [0.118, 0.205]", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1236,951,1500,972], "text":"Aracılı Oran: 39.0%", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1280,972,1475,990], "text":"%95 GA: [28.8%, 50.0%]", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   {"box":[1231,1006,1508,1025], "text":"Sobel Testi: z = 8.42, p < 0.001", "font":"mono","align":"left","size":13,"bg":[255,255,255]},
   # footer (italic grey original; Baron-Kenny/bootstrap/n=10,542 kept)
   {"box":[470,1228,1165,1248], "text":"Baron-Kenny aracılık çerçevesi bootstrap doğrulamasıyla | n = 10,542", "font":"sans","align":"center","size":14},
 ],
 # ---- Figure 4 — Study Cohort Characteristics (1600x1266) ----
 # 6 panels: A bar (Sample Dist), B donut (Cohort), C h-bars (Age), D grouped-bars (Sex),
 # E h-bars (Duration), F summary table. DATA KEPT VERBATIM: every bar value, %, n, ±SD
 # (34.1±7.8 etc), table cells, "n=10,542"/"5,007" (commas), source names. Only words->TR.
 # Panel A & D x-labels: originals ANGLED + narrow bars -> clear strip, redraw VERTICAL
 # (rotate 90) on each bar/group tick. E value labels: replace ONLY "yr"->"yıl".
 "img-037-004": [
   # title
   {"box":[508,8,1097,38], "text":"", "font":"serif","bold":True,"align":"center","size":22,"color":[0,0,0],"bg":[255,255,255]},
   # panel headers
   {"box":[78,106,360,130], "text":"A. Örneklem Dağılımı", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[640,109,1010,132], "text":"B. Kohort Kompozisyonu", "font":"sans","bold":True,"align":"center","size":18},
   {"box":[1153,106,1382,130], "text":"C. Yaş Dağılımı", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[78,672,342,692], "text":"D. Cinsiyet Dağılımı", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[616,672,842,692], "text":"E. Kullanım Süresi", "font":"sans","bold":True,"align":"left","size":18},
   {"box":[1153,672,1422,694], "text":"F. Özet İstatistikler", "font":"sans","bold":True,"align":"left","size":18},
   # --- Panel A (Sample Distribution) ---
   {"box":[4,150,32,490], "text":"Örneklem Büyüklüğü (n)", "font":"sans","rotate":90,"size":15,"bold":True,"bg":[255,255,255]},
   # clear angled x-label strip, redraw VERTICAL labels on bar centers (121,176,232,287,342,397,452)
   {"box":[72,553,560,672], "text":"", "bg":[255,255,255]},
   {"box":[97,556,145,672], "text":"Kontrol", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[152,556,200,672], "text":"Alkol", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[208,556,256,672], "text":"Opioidler", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[263,556,311,672], "text":"Kokain", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[318,556,366,672], "text":"Çoklu Madde", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[373,556,421,672], "text":"Esrar", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[428,556,476,672], "text":"Metamfetamin", "font":"sans","rotate":90,"size":13,"color":[0,0,0],"bg":[255,255,255]},
   # --- Panel B (Cohort Composition donut) --- center "Total"->"Toplam"; n=10,542 + % kept
   {"box":[778,322,872,347], "text":"Toplam", "font":"sans","bold":True,"align":"center","size":16,"color":[21,38,68],"bg":[255,255,255]},
   # --- Panel C (Age Distribution) ---
   {"box":[1300,587,1425,608], "text":"Yaş (yıl)", "font":"sans","bold":True,"align":"center","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # C overlapping legend DRAWN FIRST (under y-axis labels, as in original). Bars start @x1156
   # and are ON TOP of the legend, so clear stops at x1154 -> NEVER touches bar data; the legend
   # tail hidden under the bars stays hidden. Swatches @x1040-1058 preserved (box starts x1068).
   {"box":[1068,284,1154,298], "text":"Kontrol", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1068,303,1154,317], "text":"Alkol", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1068,323,1154,337], "text":"Opioidler", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1068,341,1154,355], "text":"Kokain", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1068,358,1154,372], "text":"Çoklu Madde", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1068,375,1154,389], "text":"Esrar", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1068,393,1154,407], "text":"Metamfetamin", "font":"sans","align":"left","size":11,"color":[0,0,0],"bg":[251,251,251]},
   # C y-axis category labels ON TOP (right-aligned @x1150). Rows OUTSIDE legend frame use white
   # bg; the 3 rows INSIDE the legend frame use off-white 251 + box starts x1062 (keep swatch).
   {"box":[1010,164,1150,184], "text":"Metamfetamin", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1010,221,1150,241], "text":"Esrar", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1062,278,1150,298], "text":"Çoklu Madde", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1062,335,1150,355], "text":"Kokain", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1062,392,1150,412], "text":"Opioidler", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[251,251,251]},
   {"box":[1010,449,1150,469], "text":"Alkol", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1010,506,1150,526], "text":"Kontrol", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # --- Panel D (Sex Distribution) ---
   {"box":[20,840,48,990], "text":"Yüzde (%)", "font":"sans","rotate":90,"size":15,"bold":True,"bg":[255,255,255]},
   # D legend Female/Male (swatches kept; plot bg ~249)
   {"box":[432,714,498,730], "text":"Kadın", "font":"sans","align":"left","size":12,"color":[41,41,41],"bg":[249,250,252]},
   {"box":[432,733,498,749], "text":"Erkek", "font":"sans","align":"left","size":12,"color":[41,41,41],"bg":[249,250,252]},
   # D clear angled x-label strip, redraw VERTICAL labels on group centers (118,174,230,286,343,399,455)
   {"box":[44,1122,488,1238], "text":"", "bg":[255,255,255]},
   {"box":[94,1124,142,1235], "text":"Kontrol", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[150,1124,198,1235], "text":"Alkol", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[206,1124,254,1235], "text":"Opioidler", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[262,1124,310,1235], "text":"Kokain", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[319,1124,367,1235], "text":"Çoklu Madde", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[375,1124,423,1235], "text":"Esrar", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[431,1124,479,1235], "text":"Metamfetamin", "font":"sans","rotate":90,"size":12,"color":[0,0,0],"bg":[255,255,255]},
   # --- Panel E (Duration of Use) ---
   # category labels (right-aligned at axis ~615; clear starts x485 to avoid panel D bars at x<480)
   {"box":[485,734,617,756], "text":"Metamfetamin", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[485,802,617,822], "text":"Esrar", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[485,870,617,892], "text":"Çoklu Madde", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[485,938,617,958], "text":"Kokain", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[485,1006,617,1026], "text":"Opioidler", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[485,1073,617,1093], "text":"Alkol", "font":"sans","align":"right","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # E value labels: replace ONLY "yr"->"yıl" (numbers/±SD untouched, on white right of bars)
   {"box":[862,734,909,756], "text":"yıl", "font":"sans","bold":True,"align":"left","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[893,802,940,824], "text":"yıl", "font":"sans","bold":True,"align":"left","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1006,871,1053,893], "text":"yıl", "font":"sans","bold":True,"align":"left","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # Coca/Alco boxes nudged left+up 3px to catch original "y" top-arm tip (still >=5px clear of numbers 8@971,3@1034)
   {"box":[976,935,1026,960], "text":"yıl", "font":"sans","bold":True,"align":"left","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[920,1006,967,1028], "text":"yıl", "font":"sans","bold":True,"align":"left","size":14,"color":[0,0,0],"bg":[255,255,255]},
   {"box":[1039,1070,1090,1095], "text":"yıl", "font":"sans","bold":True,"align":"left","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # E x-axis title
   {"box":[748,1150,902,1172], "text":"Süre (yıl)", "font":"sans","bold":True,"align":"center","size":14,"color":[0,0,0],"bg":[255,255,255]},
   # --- Panel F (Summary table) --- header navy (18,33,52); n column + all numbers kept
   {"box":[1170,791,1285,810], "text":"Grup", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[18,33,52]},
   {"box":[1352,791,1435,810], "text":"Yaş", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[18,33,52]},
   {"box":[1438,791,1508,810], "text":"Kadın%", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[18,33,52]},
   {"box":[1505,791,1570,810], "text":"Süre", "font":"sans","bold":True,"align":"center","size":13,"color":[255,255,255],"bg":[18,33,52]},
   # column-1 row labels (numbers in other cols kept; row bg auto-detected per alternating row)
   {"box":[1158,816,1300,836], "text":"Kontrol", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   {"box":[1158,844,1300,864], "text":"Alkol", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   {"box":[1158,872,1300,892], "text":"Opioidler", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   {"box":[1158,900,1300,920], "text":"Kokain", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   {"box":[1158,930,1300,952], "text":"Çoklu Madde", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   {"box":[1158,960,1300,980], "text":"Esrar", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   {"box":[1158,988,1300,1008], "text":"Metamfetamin", "font":"sans","align":"left","size":13,"color":[0,0,0]},
   # TOPLAM box stops at x1288: the n-value "10,542" starts at x1294 -> never clipped (was x1300)
   {"box":[1158,1017,1288,1037], "text":"TOPLAM", "font":"sans","bold":True,"align":"left","size":13,"color":[255,255,255],"bg":[33,82,149]},
   # footer (italic grey; source names + Mean->Ortalama, SD->SS)
   {"box":[340,1237,1285,1259], "text":"Veri kaynakları: GEO, UK Biobank, MESA, WHI, FHS, KORA, Rotterdam Study | Değerler: Ortalama±SS", "font":"sans","italic":True,"align":"center","size":14},
 ],
 # ---- Figure 5 — Brain Region-Specific Epigenetic Age Acceleration (1599x1122) ----
 # 2 panels: A sagittal brain w/ 5 navy callout boxes (white serif-bold text), B horizontal
 # bars w/ value labels + stat box. EVERYTHING serif bold (title/headers/callouts/bar labels).
 # DATA KEPT VERBATIM: every EAA value, ±, n, p, F(4,142), %95, region abbrevs (PFC/HIP/NAc/
 # AMY/VTA), Horvath, ANOVA, Tukey HSD, "108". Only English words->TR. Callouts & bar value
 # labels: replace ONLY "yr"->"yıl"; white-on-navy gradient callouts need explicit bg per box.
 "img-038-005": [
   # title (serif bold navy on white)
   {"box":[176,8,1314,41], "text":"", "font":"serif","bold":True,"align":"center","size":26,"bg":[255,255,255]},
   # panel headers (serif bold navy, left; pad 0 to match original 'A'/'B' start)
   {"box":[8,242,578,267], "text":"A. Sagital Beyin Kesiti - Bölgesel EAA", "font":"serif","bold":True,"align":"left","pad":0.0,"size":22,"bg":[255,255,255]},
   {"box":[1129,52,1497,77], "text":"B. Bölgesel EAA İstatistikleri", "font":"serif","bold":True,"align":"left","pad":0.0,"size":22,"bg":[255,255,255]},
   # --- Panel A callouts: white serif-bold "yr"->"yıl" on navy gradient (explicit bg per box).
   # "yıl" (21px@17) is wider than "yr", so center the ink in the number->paren gap; box center =
   # gap center (ink delta ~=0 at size 17). Gives balanced ~4px left / ~5px right (paren intact) ---
   {"box":[110,326,138,346], "text":"yıl", "font":"serif","bold":True,"align":"center","size":17,"color":[255,255,255],"bg":[24,48,76]},
   {"box":[110,409,138,428], "text":"yıl", "font":"serif","bold":True,"align":"center","size":17,"color":[255,255,255],"bg":[38,79,120]},
   {"box":[110,493,138,512], "text":"yıl", "font":"serif","bold":True,"align":"center","size":17,"color":[255,255,255],"bg":[45,90,146]},
   {"box":[113,576,141,596], "text":"yıl", "font":"serif","bold":True,"align":"center","size":17,"color":[255,255,255],"bg":[53,121,179]},
   {"box":[110,659,138,679], "text":"yıl", "font":"serif","bold":True,"align":"center","size":17,"color":[255,255,255],"bg":[12,125,183]},
   # --- Panel B bar value labels: serif-bold "yr"->"yıl" (dark on white; color auto) ---
   {"box":[1364,180,1390,197], "text":"yıl", "font":"serif","bold":True,"align":"left","pad":0.04,"size":16,"bg":[255,255,255]},
   {"box":[1384,335,1410,352], "text":"yıl", "font":"serif","bold":True,"align":"left","pad":0.04,"size":16,"bg":[255,255,255]},
   {"box":[1399,491,1425,508], "text":"yıl", "font":"serif","bold":True,"align":"left","pad":0.04,"size":16,"bg":[255,255,255]},
   {"box":[1429,647,1455,664], "text":"yıl", "font":"serif","bold":True,"align":"left","pad":0.04,"size":16,"bg":[255,255,255]},
   {"box":[1490,803,1515,820], "text":"yıl", "font":"serif","bold":True,"align":"left","pad":0.04,"size":16,"bg":[255,255,255]},
   # Panel B x-axis title (serif bold; "years"->"yıl", EAA kept)
   {"box":[1233,941,1422,970], "text":"EAA (yıl)", "font":"serif","bold":True,"align":"center","size":22,"bg":[255,255,255]},
   # footer (serif italic grey; PMI/Horvath kept, words->TR, 95% CI->%95 GA)
   {"box":[390,986,1098,1010], "text":"PMI-düzeltilmiş Horvath saati | Postmortem örnekler | Hata çubukları: %95 GA", "font":"serif","italic":True,"align":"center","size":15,"bg":[255,255,255]},
   # bottom stat box line 3: word-level Total->Toplam, samples->örnek ("108 postmortem" kept).
   # "Toplam" (65px@16) is far wider than "Total" (45px), so even "Toplam n" overflows into "=".
   # Redraw "Toplam n =" as one unit (identical n/= symbols, just re-typeset) at size 15 (95px)
   # so it ends before "108" @x1257. "108" data never touched.
   {"box":[1158,1096,1252,1115], "text":"Toplam n =", "font":"serif","bold":True,"align":"left","pad":0.0,"size":15,"bg":[255,255,255]},
   {"box":[1417,1096,1499,1115], "text":"örnek", "font":"serif","bold":True,"align":"left","pad":0.04,"size":16,"bg":[255,255,255]},
 ],
 # ---- Figure 6 — Intervention Duration vs Epigenetic Age Reversal (1599x979, bubble) ----
 # Fonts: title/axes sans bold navy (17,38,64); callouts sans on white box interiors (border
 # untouched, only tight text box cleared); summary box MONO right-aligned (numbers verbatim,
 # only words->TR); footer sans italic grey. WORDS only; n=/numbers/rho/p/eqn kept verbatim.
 "img-039-006": [
   # title (sans bold navy, 2 lines centered on x~829)
   {"box":[460,8,1200,76], "text":"", "font":"sans","bold":True,"align":"center","color":[17,38,64],"bg":[255,255,255]},
   # y-axis title (rotate 90, sans bold navy)
   {"box":[8,280,36,668], "text":"Epigenetik Yaş Değişimi (yıl)", "font":"sans","bold":True,"rotate":90,"color":[17,38,64],"bg":[255,255,255]},
   # x-axis title (sans bold navy)
   {"box":[688,890,970,914], "text":"Müdahale Süresi", "font":"sans","bold":True,"align":"center","color":[17,38,64],"bg":[255,255,255]},
   # callouts (sans; clear tight text box only -> navy border + connector kept). TR <= EN length.
   {"box":[90,327,234,346], "text":"Farkındalık + Yoga", "font":"sans","align":"center","size":16,"color":[48,53,57],"bg":[255,255,255]},
   {"box":[59,635,202,649], "text":"Diyet Değişikliği", "font":"sans","align":"center","size":16,"color":[48,53,57],"bg":[255,255,255]},
   {"box":[980,286,1162,300], "text":"Madde Bırakma (1 yıl)", "font":"sans","align":"center","size":16,"color":[48,53,57],"bg":[255,255,255]},
   {"box":[578,472,699,486], "text":"Fiziksel Egzersiz", "font":"sans","align":"center","size":16,"color":[48,53,57],"bg":[255,255,255]},
   {"box":[492,798,656,809], "text":"Kombine Müdahale", "font":"sans","align":"center","size":16,"color":[48,53,57],"bg":[255,255,255]},
   {"box":[1403,481,1589,498], "text":"Madde Bırakma (5 yıl)", "font":"sans","align":"center","size":16,"color":[48,53,57],"bg":[255,255,255]},
   # legend title "Sample Size"->TR (auto-fit narrow legend box; n=50/100/150 kept)
   {"box":[1452,114,1590,137], "text":"Örneklem Boyutu", "font":"sans","align":"center","color":[0,0,0],"bg":[253,253,253]},
   # "No Effect" red label
   {"box":[1371,167,1450,184], "text":"Etki Yok", "font":"sans","bold":True,"align":"center","color":[185,53,64],"bg":[249,250,252]},
   # statistical summary box (MONO). header right-aligned; underline @y389 kept untouched.
   {"box":[1352,361,1536,381], "text":"İstatistiksel Özet", "font":"mono","align":"right","pad":0.01,"size":15,"color":[42,44,50],"bg":[255,255,255]},
   # body 3 lines (right-aligned; eqn / R² / n verbatim, only Trend/moderate fit/Total -> TR)
   {"box":[1250,399,1536,416], "text":"Eğilim: y = 0.20·ln(x) + -3.53", "font":"mono","align":"right","pad":0.01,"size":15,"color":[44,48,52],"bg":[255,255,255]},
   {"box":[1250,417,1536,435], "text":"R² = 0.38 (orta uyum)", "font":"mono","align":"right","pad":0.01,"size":15,"color":[44,48,52],"bg":[255,255,255]},
   {"box":[1250,436,1536,453], "text":"Toplam n = 593", "font":"mono","align":"right","pad":0.01,"size":15,"color":[44,48,52],"bg":[255,255,255]},
   # x-axis tick labels (weeks->hafta, months->ay, year(s)->yıl; numbers kept)
   {"box":[278,849,351,872], "text":"8 hafta", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[402,849,486,872], "text":"12 hafta", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[649,849,734,872], "text":"6 ay", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[886,849,943,872], "text":"1 yıl", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[1102,849,1168,872], "text":"2 yıl", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[1395,849,1462,872], "text":"5 yıl", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   # footer (sans italic->upright, grey; words->TR, 95% CI->%95 GA; rho/p/numbers verbatim)
   {"box":[400,949,1210,969], "text":"Nokta boyutları örneklem büyüklüğü ile orantılı | Gölgeli: %95 GA | Spearman rho = -0.42, p = 0.08", "font":"sans","italic":True,"align":"center","color":[128,128,128],"bg":[255,255,255]},
 ],
 # ---- Supplementary Figure S1 — DNA Methylation Pipeline flowchart (1599x2073) ----
 # serif throughout; numbers/proper names/abbr (GEO/ArrayExpress, IDAT, Illumina, 450K/EPIC,
 # BeadChip, CpGs, MAF, SNP, getSex(), Horvath..DunedinPACE, n/years) verbatim; only words->TR.
 "img-040-007": [
   # title + subtitle (navy on white)
   {"box":[540,46,1058,87], "text":"", "font":"serif","bold":True,"size":40,"color":[10,40,64]},
   {"box":[405,109,1192,140], "text":"", "font":"serif","size":26,"color":[24,66,106]},
   # stage 1 (navy box 9,38,70 / white)
   {"box":[688,221,910,243], "text":"HAM VERİ GİRİŞİ", "font":"serif","bold":True,"size":20,"bg":[9,38,70],"color":[255,255,255]},
   {"box":[618,269,978,290], "text":"15 GEO/ArrayExpress Veri Seti (n=10,542)", "font":"serif","italic":True,"size":17,"bg":[9,38,70],"color":[255,255,255]},
   # stage 2 (navy box 20,66,115 / white)
   {"box":[650,407,945,428], "text":"IDAT DOSYA İŞLEME", "font":"serif","bold":True,"size":21,"bg":[20,66,115],"color":[255,255,255]},
   {"box":[638,454,955,476], "text":"Illumina 450K/EPIC BeadChip Dizileri", "font":"serif","italic":True,"size":18,"bg":[20,66,115],"color":[255,255,255]},
   # stage 3 — Quality Control module (section header navy on panel; 4 cards)
   {"box":[585,529,1014,556], "text":"KALİTE KONTROL MODÜLÜ", "font":"serif","bold":True,"size":26,"color":[37,84,138]},
   {"box":[178,655,345,677], "text":"Tespit p-değeri", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[195,699,328,716], "text":"<0.01 eşik", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   {"box":[528,655,724,677], "text":"Bisülfit Dönüşümü", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[560,699,690,716], "text":">%96 verim", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   {"box":[915,655,1062,677], "text":"Cinsiyet Tahmini", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[910,699,1062,716], "text":"getSex() doğrulama", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   {"box":[1285,655,1420,677], "text":"Eksik Veri", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[1283,699,1418,716], "text":"<%5 örnek başına", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   # stage 4 — Probe filtering (section header; 4 cards; MAF>0.01 left verbatim)
   {"box":[658,853,940,882], "text":"PROB FİLTRELEME", "font":"serif","bold":True,"size":26,"bg":[255,255,255],"color":[37,84,138]},
   {"box":[190,981,330,1010], "text":"Çapraz-reaktif", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[190,1027,335,1045], "text":"29,233 kaldırıldı", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   {"box":[558,983,690,1003], "text":"SNP-etkilenen", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[885,983,1095,1003], "text":"Cinsiyet Kromozomları", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[900,1027,1040,1045], "text":"X/Y kaldırıldı", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   {"box":[1283,983,1422,1003], "text":"Düşük Tespit", "font":"serif","bold":True,"size":18,"color":[32,48,71]},
   {"box":[1285,1027,1418,1045], "text":"p>0.01 filtrelendi", "font":"serif","italic":True,"size":15,"color":[149,155,177]},
   # stage 5 / 6 (blue boxes 0,120,183 / white)
   {"box":[200,1216,556,1251], "text":"NORMALİZASYON", "font":"serif","bold":True,"size":24,"bg":[0,120,183],"color":[255,255,255]},
   {"box":[315,1277,585,1294], "text":"Fonksiyonel Normalizasyon", "font":"serif","italic":True,"size":17,"bg":[0,120,183],"color":[255,255,255]},
   {"box":[1018,1230,1278,1250], "text":"BATCH DÜZELTMESİ", "font":"serif","bold":True,"size":24,"bg":[0,120,183],"color":[255,255,255]},
   {"box":[1040,1277,1255,1296], "text":"ComBat Ampirik Bayes", "font":"serif","italic":True,"size":17,"bg":[0,120,183],"color":[255,255,255]},
   # stage 7 (navy box 33,82,149 / white)
   {"box":[590,1415,1008,1436], "text":"HÜCRE BİLEŞİMİ TAHMİNİ", "font":"serif","bold":True,"size":21,"bg":[33,82,149],"color":[255,255,255]},
   {"box":[558,1463,1130,1482], "text":"Houseman Referans-tabanlı Dekonvolüsyon (6 hücre tipi)", "font":"serif","italic":True,"size":16,"bg":[33,82,149],"color":[255,255,255]},
   # stage 8 — section header only (clock cards Horvath..DunedinPACE + CpGs + years all verbatim)
   {"box":[516,1555,1083,1582], "text":"EPİGENETİK SAAT HESAPLAMASI", "font":"serif","bold":True,"size":26,"color":[37,84,138]},
   # stage 9 (navy bar 9,38,70 header + blue Final bar 0,120,183)
   {"box":[540,1936,1060,1962], "text":"İSTATİSTİKSEL ANALİZ VE ÇIKTI", "font":"serif","bold":True,"size":28,"bg":[9,38,70],"color":[255,255,255]},
   {"box":[200,2005,1399,2056], "text":"Sonuç: n=10,542 | 773,765 CpGs | 5 Saat | 6 Madde Kategorisi", "font":"serif","bold":True,"size":22,"bg":[0,120,183],"color":[255,255,255]},
 ],
 # ---- Supplementary Figure S2 — Batch Effect Correction PCA (1599x792) ----
 # axis tick numbers (40,30,20,10,0,-10,-30) + legend dataset IDs (GSE*, UK Biobank, MESA) are DATA -> untouched
 "img-041-008": [
   {"box":[418,5,1180,33], "text":"", "font":"serif","bold":True,"bg":[255,255,255]},
   # panel headers
   {"box":[338,78,516,99], "text":"A) Düzeltme Öncesi", "font":"serif","bold":True,"bg":[255,255,255]},
   {"box":[1132,78,1318,99], "text":"B) Düzeltme Sonrası", "font":"serif","bold":True,"bg":[255,255,255]},
   # y-axis titles (vertical) — boxes kept left of the tick numbers
   {"box":[6,318,24,488], "text":"PC2 (%18.6 varyans)", "font":"serif","rotate":90,"bg":[255,255,255]},
   {"box":[801,320,825,488], "text":"PC2 (%6.2 varyans)", "font":"serif","rotate":90,"bg":[255,255,255]},
   # x-axis titles
   {"box":[344,716,511,745], "text":"PC1 (%32.4 varyans)", "font":"serif","bg":[255,255,255]},
   {"box":[1146,716,1304,745], "text":"PC1 (%8.7 varyans)", "font":"serif","bg":[255,255,255]},
   # corner callout boxes (light fill + coloured bold text)
   {"box":[601,628,763,678], "text":"Batch Etkisi:\nAçıkça Görülür\n(Veri Setleri Ayrışmış)", "font":"serif","bold":True,"bg":[252,234,232],"color":[140,53,58]},
   {"box":[1428,628,1560,674], "text":"Batch Etkisi:\nGiderildi\n(Veri Setleri Karışmış)", "font":"serif","bold":True,"bg":[226,255,220],"color":[55,125,58]},
   # footer caption (italic grey)
   {"box":[396,764,1203,787], "text":"ComBat ampirik Bayes batch düzeltmesi, biyolojik sinyali korurken teknik varyasyonu başarıyla giderdi", "font":"serif","italic":True,"bg":[255,255,255]},
 ],
 # ---- Supplementary Figure S3 — Epigenetic Clock Calibration (1599x1083) ----
 # 5 scatter panels + CALIBRATION SUMMARY box. ALL numbers (every MAE/R²/Slope/Intercept value,
 # axis ticks, 95, 1.0, 2.4, 0.94, 2.1, 0.96), proper names (Horvath/Hannum/PhenoAge/GrimAge/Ensemble),
 # abbreviations (MAE, R², CI) stay as ORIGINAL pixels. Only English WORDS are overlaid.
 "img-042-009": [
   # main title (serif bold navy)
   {"box":[462,6,1178,35], "text":"", "font":"serif","bold":True,"bg":[255,255,255]},
   # panel titles — sans bold, each its own colour (auto). "X Clock" -> "X Saati" (proper name kept verbatim)
   {"box":[216,90,366,109], "text":"Horvath Saati", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[746,90,898,109], "text":"Hannum Saati", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[1269,90,1439,112], "text":"PhenoAge Saati", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[212,588,368,610], "text":"GrimAge Saati", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[739,588,904,608], "text":"Ensemble Saati", "font":"sans","bold":True,"bg":[255,255,255]},
   # y-axis titles (vertical) — boxes kept LEFT of the tick numbers (col2 ticks x560+, col3 x1091+)
   {"box":[4,246,26,410], "text":"Epigenetik Yaş (yıl)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[536,246,557,410], "text":"Epigenetik Yaş (yıl)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[1068,246,1089,410], "text":"Epigenetik Yaş (yıl)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[4,744,26,908], "text":"Epigenetik Yaş (yıl)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[536,744,557,908], "text":"Epigenetik Yaş (yıl)", "font":"sans","rotate":90,"bg":[255,255,255]},
   # x-axis titles
   {"box":[195,559,384,580], "text":"Kronolojik Yaş (yıl)", "font":"sans","bg":[255,255,255]},
   {"box":[727,559,916,580], "text":"Kronolojik Yaş (yıl)", "font":"sans","bg":[255,255,255]},
   {"box":[1258,559,1447,580], "text":"Kronolojik Yaş (yıl)", "font":"sans","bg":[255,255,255]},
   {"box":[195,1056,384,1078], "text":"Kronolojik Yaş (yıl)", "font":"sans","bg":[255,255,255]},
   {"box":[727,1056,916,1078], "text":"Kronolojik Yaş (yıl)", "font":"sans","bg":[255,255,255]},
   # legend (Horvath panel) — marker symbols (dots/dashes/CI swatch) untouched; only the labels
   {"box":[424,456,523,466], "text":"Madde Kullanıcıları", "font":"sans","align":"left"},
   {"box":[424,471,523,481], "text":"Kontroller", "font":"sans","align":"left"},
   {"box":[424,486,523,496], "text":"Mükemmel Kalibrasyon", "font":"sans","align":"left"},
   {"box":[424,501,523,513], "text":"Regresyon Çizgisi", "font":"sans","align":"left"},
   {"box":[424,516,523,526], "text":"%95 GA", "font":"sans","align":"left"},
   # stat boxes — ONLY words; every value AND the whole "R² = .." line stay as pixels.
   # years->yıl (line1, after the value) | Slope->Eğim (line3) | Intercept->Kesişim (line4)
   {"box":[140,139,172,149], "text":"yıl", "font":"sans","align":"left","size":11},
   {"box":[672,139,704,149], "text":"yıl", "font":"sans","align":"left","size":11},
   {"box":[1203,139,1235,149], "text":"yıl", "font":"sans","align":"left","size":11},
   {"box":[140,636,172,647], "text":"yıl", "font":"sans","align":"left","size":11},
   {"box":[671,636,704,647], "text":"yıl", "font":"sans","align":"left","size":11},
   {"box":[79,164,109,175], "text":"Eğim", "font":"sans","align":"left","size":11},
   {"box":[608,164,640,175], "text":"Eğim", "font":"sans","align":"left","size":11},
   {"box":[1140,164,1172,175], "text":"Eğim", "font":"sans","align":"left","size":11},
   {"box":[79,662,109,673], "text":"Eğim", "font":"sans","align":"left","size":11},
   {"box":[608,662,640,673], "text":"Eğim", "font":"sans","align":"left","size":11},
   {"box":[80,177,129,188], "text":"Kesişim", "font":"sans","align":"left","size":11},
   {"box":[608,177,661,188], "text":"Kesişim", "font":"sans","align":"left","size":11},
   {"box":[1140,177,1192,188], "text":"Kesişim", "font":"sans","align":"left","size":11},
   {"box":[80,675,129,685], "text":"Kesişim", "font":"sans","align":"left","size":11},
   {"box":[608,675,661,685], "text":"Kesişim", "font":"sans","align":"left","size":11},
   # CALIBRATION SUMMARY (mono). GrimAge/Ensemble names + (MAE=.., R²=..) parentheticals stay as pixels.
   # Only "1.0" is retyped verbatim (single, unambiguous value, == Ensemble slope) inside centred prose.
   {"box":[1262,730,1445,745], "text":"KALİBRASYON ÖZETİ", "font":"mono","bold":True},
   {"box":[1126,764,1334,783], "text":"En İyi Bireysel Saat:", "font":"mono","align":"left","pad":0.02},
   {"box":[1135,781,1254,799], "text":"En İyi Genel:", "font":"mono","align":"left","pad":0.02},
   {"box":[1126,814,1570,852], "text":"Tüm saatler 1.0'a yakın eğimler ve minimal\nkesişimlerle mükemmel kalibrasyon gösterir.", "font":"mono"},
   {"box":[1126,866,1570,921], "text":"Madde kullanıcıları (kırmızı), kontrollere (mavi)\nkıyasla sistematik pozitif sapma göstererek\nepigenetik yaş hızlanmasını yansıtır.", "font":"mono"},
 ],
 # ---- Supplementary Figure S4 — Differential Methylation Volcano Plots (1599x1051) ----
 # 6 panels (col centers 289/820/1352). ALL data stays as pixels: every n value, callout counts
 # (287,136,198,189,156,147,142,89,94,223,213...), Δβ thresholds (>0.1, <-0.1), gene symbols
 # (AHRR, BDNF, COMT, OPRM1, DRD2, SLC6A3, NR3C1, TH, CNR1/2, FAAH, MGLL, DAGLA, PDYN, PENK ...),
 # abbreviations (CpGs). "Opioid" is identical in TR -> left untouched. Only English words overlaid.
 "img-043-010": [
   {"box":[388,6,1212,34], "text":"", "font":"serif","bold":True,"bg":[255,255,255]},
   # panel titles (sans bold, each its own colour via auto)
   {"box":[250,87,330,106], "text":"Alkol", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[780,87,860,106], "text":"Kokain", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[203,545,375,565], "text":"Metamfetamin", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[775,545,866,565], "text":"Kanabis", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[1284,545,1420,565], "text":"Çoklu Madde", "font":"sans","bold":True,"bg":[255,255,255]},
   # subtitles: ONLY "sig."->"anl." swapped in place; "(n=NNN" and "CpGs)" stay as pixels
   {"box":[278,105,309,122], "text":"anl.", "font":"sans","align":"center"},
   {"box":[810,105,841,122], "text":"anl.", "font":"sans","align":"center"},
   {"box":[1341,105,1372,122], "text":"anl.", "font":"sans","align":"center"},
   {"box":[278,564,309,581], "text":"anl.", "font":"sans","align":"center"},
   {"box":[810,564,841,581], "text":"anl.", "font":"sans","align":"center"},
   {"box":[1341,564,1372,581], "text":"anl.", "font":"sans","align":"center"},
   # y-axis titles (vertical) — left of the tick numbers
   {"box":[7,266,24,357], "text":"-log10(p-değeri)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[539,266,555,357], "text":"-log10(p-değeri)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[1070,266,1087,357], "text":"-log10(p-değeri)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[7,724,24,815], "text":"-log10(p-değeri)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[539,724,555,815], "text":"-log10(p-değeri)", "font":"sans","rotate":90,"bg":[255,255,255]},
   {"box":[1070,724,1087,815], "text":"-log10(p-değeri)", "font":"sans","rotate":90,"bg":[255,255,255]},
   # x-axis titles
   {"box":[197,520,379,536], "text":"Δβ (Metilasyon Farkı)", "font":"sans","bg":[255,255,255]},
   {"box":[729,520,911,536], "text":"Δβ (Metilasyon Farkı)", "font":"sans","bg":[255,255,255]},
   {"box":[1260,520,1442,536], "text":"Δβ (Metilasyon Farkı)", "font":"sans","bg":[255,255,255]},
   {"box":[197,978,379,995], "text":"Δβ (Metilasyon Farkı)", "font":"sans","bg":[255,255,255]},
   {"box":[729,978,911,995], "text":"Δβ (Metilasyon Farkı)", "font":"sans","bg":[255,255,255]},
   {"box":[1260,978,1442,995], "text":"Δβ (Metilasyon Farkı)", "font":"sans","bg":[255,255,255]},
   # callouts — ONLY the word "Hyper:"->"Hiper:" / "Hypo:"->"Hipo:"; the counts stay as pixels
   {"box":[440,142,481,154], "text":"Hiper:", "font":"sans","align":"left"},
   {"box":[445,154,481,167], "text":"Hipo:", "font":"sans","align":"left"},
   {"box":[967,142,1013,154], "text":"Hiper:", "font":"sans","align":"left"},
   {"box":[967,154,1013,167], "text":"Hipo:", "font":"sans","align":"left"},
   {"box":[1498,142,1544,154], "text":"Hiper:", "font":"sans","align":"left"},
   {"box":[1498,154,1544,167], "text":"Hipo:", "font":"sans","align":"left"},
   {"box":[440,601,481,613], "text":"Hiper:", "font":"sans","align":"left"},
   {"box":[445,614,481,626], "text":"Hipo:", "font":"sans","align":"left"},
   {"box":[967,601,1018,613], "text":"Hiper:", "font":"sans","align":"left"},
   {"box":[967,614,1018,626], "text":"Hipo:", "font":"sans","align":"left"},
   {"box":[1498,601,1544,613], "text":"Hiper:", "font":"sans","align":"left"},
   {"box":[1498,614,1544,626], "text":"Hipo:", "font":"sans","align":"left"},
   # bottom legend — coloured dots + (Δβ...) values stay as pixels; only the words overlaid
   {"box":[514,1021,638,1039], "text":"Hipermetile", "font":"sans","align":"left"},
   {"box":[765,1021,883,1039], "text":"Hipometile", "font":"sans","align":"left"},
   {"box":[1015,1021,1123,1039], "text":"Anlamlı Değil", "font":"sans","align":"left"},
 ],
 # ---- Supplementary Figure S5 — Mediation Path Diagrams (1599x636) ----
 # 3 panels, pitch 532 (panel2 = panel1+532, panel3 = +1064). KEEP as pixels: all β values
 # (0.42/0.33/0.39/0.38/0.24/0.44/0.45/0.36/0.37), mediation % (26.4/17.0/30.2), totals
 # (β=0.39, 61%), p<0.001, and names HOMA-IR, ACTH, CRP, IL-6, GrimAge EAA, BMI. Words only.
 "img-044-011": [
   {"box":[502,5,1098,31], "text":"", "font":"serif","bold":True,"bg":[255,255,255]},
   # mediator boxes (white text on colour) — keep (HOMA-IR)/(CRP + IL-6); translate Cortisol->Kortizol
   {"box":[205,139,331,154], "text":"İnsülin Direnci", "font":"sans","bold":True,"color":[255,255,255],"bg":[33,82,149]},
   {"box":[735,139,865,154], "text":"HPA Ekseni", "font":"sans","bold":True,"color":[255,255,255],"bg":[0,120,183]},
   {"box":[735,155,865,169], "text":"(Kortizol/ACTH)", "font":"sans","bold":True,"color":[255,255,255],"bg":[0,120,183]},
   {"box":[1267,139,1397,154], "text":"Sistemik İnflamasyon", "font":"sans","bold":True,"color":[255,255,255],"bg":[20,66,115]},
   # left boxes "Substance Use Duration" -> "Madde Kullanım Süresi" (white on navy)
   {"box":[35,315,155,348], "text":"Madde Kullanım\nSüresi", "font":"sans","bold":True,"color":[255,255,255],"bg":[9,38,69]},
   {"box":[567,315,687,348], "text":"Madde Kullanım\nSüresi", "font":"sans","bold":True,"color":[255,255,255],"bg":[9,38,69]},
   {"box":[1099,315,1219,348], "text":"Madde Kullanım\nSüresi", "font":"sans","bold":True,"color":[255,255,255],"bg":[9,38,69]},
   # Path a / Path b (keep β values below) -> Yol a / Yol b
   {"box":[132,204,178,216], "text":"Yol a", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[359,204,407,216], "text":"Yol b", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[664,204,710,216], "text":"Yol a", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[891,204,939,216], "text":"Yol b", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[1196,204,1242,216], "text":"Yol a", "font":"sans","bold":True,"bg":[255,255,255]},
   {"box":[1423,204,1471,216], "text":"Yol b", "font":"sans","bold":True,"bg":[255,255,255]},
   # Direct Effect (c') -> Doğrudan Etki (c') (keep β below)
   {"box":[214,350,322,363], "text":"Doğrudan Etki (c')", "font":"sans","align":"center","bg":[255,255,255]},
   {"box":[746,350,854,363], "text":"Doğrudan Etki (c')", "font":"sans","align":"center","bg":[255,255,255]},
   {"box":[1278,350,1386,363], "text":"Doğrudan Etki (c')", "font":"sans","align":"center","bg":[255,255,255]},
   # Mediation: NN.N%  -> Aracılık:  (keep % number as pixels)
   {"box":[198,466,286,482], "text":"Aracılık:", "font":"sans","bold":True,"align":"left","bg":[255,255,255]},
   {"box":[730,466,818,482], "text":"Aracılık:", "font":"sans","bold":True,"align":"left","bg":[255,255,255]},
   {"box":[1262,466,1350,482], "text":"Aracılık:", "font":"sans","bold":True,"align":"left","bg":[255,255,255]},
   # bottom summary — keep β = 0.39 and 61% as pixels; keep BMI; translate words
   {"box":[503,613,648,629], "text":"Toplam Dolaylı Etki:", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[710,613,870,629], "text":"| Birleşik Aracılık:", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[911,613,1094,629], "text":"| Kovaryatlar: Yaş, Cinsiyet, BMI", "font":"sans","align":"left","bg":[255,255,255]},
 ],
 "img-045-012": [
   # main title (serif bold)
   {"box":[394,8,1206,35], "text":"", "font":"serif","bold":True,"align":"center","bg":[255,255,255]},
   # panel titles (navy auto) — keep (DERS)/(SCS-B), Madde-EAA + abbreviations
   {"box":[85,88,750,106], "text":"A) Duygu Düzenleme (DERS), Madde-EAA İlişkisini Modere Eder", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
   {"box":[917,88,1513,106], "text":"B) Öz-Kontrol (SCS-B), Madde-EAA İlişkisini Modere Eder", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
   # legend A — retype whole line (width); keep DERS/(±1 SD)/β verbatim; Low/Mean/High -> Düşük/Ortalama/Yüksek
   {"box":[68,126,311,143], "text":"Düşük DERS (-1 SD): β=0.18", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[68,147,311,165], "text":"Ortalama DERS: β=0.42", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[68,168,311,186], "text":"Yüksek DERS (+1 SD): β=0.66", "font":"sans","align":"left","bg":[255,255,255]},
   # legend B — same; keep SCS-B/(±1 SD)/β verbatim
   {"box":[905,126,1111,143], "text":"Düşük SCS-B (-1 SD): β=0.74", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[905,147,1111,165], "text":"Ortalama SCS-B: β=0.48", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[905,168,1111,186], "text":"Yüksek SCS-B (+1 SD): β=0.22", "font":"sans","align":"left","bg":[255,255,255]},
   # y-axis labels (rotated, navy auto) — keep GrimAge EAA; (years)->(yıl)
   {"box":[8,318,28,496], "text":"GrimAge EAA (yıl)", "font":"sans","align":"center","rotate":90,"bg":[255,255,255]},
   {"box":[805,318,826,496], "text":"GrimAge EAA (yıl)", "font":"sans","align":"center","rotate":90,"bg":[255,255,255]},
   # x-axis labels — Substance Use Duration (years) -> Madde Kullanım Süresi (yıl)
   {"box":[284,725,551,745], "text":"Madde Kullanım Süresi (yıl)", "font":"sans","align":"center","bg":[255,255,255]},
   {"box":[1081,725,1348,745], "text":"Madde Kullanım Süresi (yıl)", "font":"sans","align":"center","bg":[255,255,255]},
   # Johnson-Neyman annotation (gray italic) — keep Johnson-Neyman + (DERS=68); Threshold->Eşiği
   {"box":[433,245,592,261], "text":"Johnson-Neyman", "font":"sans","italic":True,"align":"center"},
   {"box":[433,261,592,277], "text":"Eşiği (DERS=68)", "font":"sans","italic":True,"align":"center"},
   # Significant (red auto) -> Anlamlı
   {"box":[551,615,648,631], "text":"Anlamlı", "font":"sans","bold":True,"align":"center"},
   # Protective Effect (green auto, 2 lines) -> Koruyucu Etki
   {"box":[1246,469,1338,501], "text":"Koruyucu\nEtki", "font":"sans","bold":True,"align":"center"},
   # interaction boxes — swap only Interaction:->Etkileşim: (keep β/p/ΔR²/F pixels), white interior
   {"box":[533,636,617,650], "text":"Etkileşim:", "font":"sans","align":"left","bg":[255,255,255]},
   {"box":[1320,636,1406,650], "text":"Etkileşim:", "font":"sans","align":"left","bg":[255,255,255]},
   # bottom KEY FINDING (bold) — keep 50-70% and EAA verbatim
   {"box":[373,767,1227,789], "text":"ANAHTAR BULGU: Yüksek psikolojik dayanıklılık madde kaynaklı EAA'yı 50-70% azaltır", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
 ],
 "img-046-013": [
   # main title (serif bold) — Postmortem Interval->Postmortem Aralık, Correction Effect->Düzeltme Etkisi; keep PMI/S7
   {"box":[353,7,1248,33], "text":"", "font":"serif","bold":True,"align":"center","bg":[255,255,255]},
   # panel titles (navy bold) — keep PMI; vs->Karşı; Pre/Post-Correction->Düzeltme Öncesi/Sonrası; Calibration Comparison->Kalibrasyon Karşılaştırması
   {"box":[101,74,492,93], "text":"A) Düzeltme Öncesi: PMI'ye Karşı Yaş Tahmin Hatası", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
   {"box":[629,74,1027,93], "text":"B) Düzeltme Sonrası: PMI'ye Karşı Yaş Tahmin Hatası", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
   {"box":[1149,74,1569,93], "text":"C) Kalibrasyon Karşılaştırması: Düzeltme Öncesi ve Sonrası", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
   # NOTE: panel A/B regression legends ("y = ...x + ..., R²=...", "95% CI") contain NO English words -> left untouched
   # legend C (3 lines, black, size 10 to fit frame border x1294) — keep dot/dash markers (x<1166)
   {"box":[1172,106,1292,121], "text":"Düzeltme Öncesi", "font":"sans","align":"left","size":10,"bg":[255,255,255]},
   {"box":[1172,125,1292,140], "text":"Düzeltme Sonrası", "font":"sans","align":"left","size":10,"bg":[255,255,255]},
   {"box":[1172,144,1292,159], "text":"Mükemmel Kalibrasyon", "font":"sans","align":"left","size":10,"bg":[255,255,255]},
   # y-axis labels (rotated, navy auto) — Age Prediction Error->Yaş Tahmin Hatası; Epigenetic Age->Epigenetik Yaş; (years)->(yıl)
   {"box":[8,224,23,415], "text":"Yaş Tahmin Hatası (yıl)", "font":"sans","align":"center","rotate":90,"bg":[255,255,255]},
   {"box":[523,224,547,415], "text":"Yaş Tahmin Hatası (yıl)", "font":"sans","align":"center","rotate":90,"bg":[255,255,255]},
   {"box":[1085,238,1107,400], "text":"Epigenetik Yaş (yıl)", "font":"sans","align":"center","rotate":90,"bg":[255,255,255]},
   # x-axis labels — PMI (hours)->PMI (saat); Chronological Age (years)->Kronolojik Yaş (yıl)
   {"box":[257,562,335,578], "text":"PMI (saat)", "font":"sans","align":"center","bg":[255,255,255]},
   {"box":[789,562,867,578], "text":"PMI (saat)", "font":"sans","align":"center","bg":[255,255,255]},
   {"box":[1270,562,1448,578], "text":"Kronolojik Yaş (yıl)", "font":"sans","align":"center","bg":[255,255,255]},
   # MAE annotations — retype whole (keep 7.2/3.8 verbatim); years->yıl; red(A)/green(B) auto color, white interior
   {"box":[382,502,510,512], "text":"MAE = 7.2 yıl", "font":"sans","bold":True,"align":"left","size":12,"bg":[255,255,255]},
   {"box":[905,502,1043,512], "text":"MAE = 3.8 yıl", "font":"sans","bold":True,"align":"left","size":12,"bg":[255,255,255]},
   # panel C results box — retype header + L2/L4 (keep 7.2/3.8/-47%/0.81/0.94 verbatim); years->yıl, Calibration->Kalibrasyon; L3 (R²) untouched
   {"box":[1438,467,1566,477], "text":"PMI Düzeltme Sonuçları:", "font":"sans","bold":True,"align":"center","bg":[255,255,255]},
   {"box":[1409,479,1566,492], "text":"MAE: 7.2 → 3.8 yıl (-47%)", "font":"sans","align":"right","size":10,"bg":[255,255,255]},
   {"box":[1409,504,1566,516], "text":"Kalibrasyon: 0.81 → 0.94", "font":"sans","align":"right","size":10,"bg":[255,255,255]},
   # bottom caption (gray italic) — keep n=108/6-48/5.2-7.1/pH/PMI; brain tissue->beyin dokusu, range->aralığı, hours->saat, Tissue->Doku
   {"box":[511,595,1086,616], "text":"Postmortem beyin dokusu (n=108) | PMI aralığı: 6-48 saat | Doku pH aralığı: 5.2-7.1", "font":"sans","italic":True,"align":"center","bg":[255,255,255]},
 ],
 # ---- Figure S8 — Brain Region-Specific Epigenetic Age Acceleration (1599x1139) ----
 "img-047-014": [
   # main title (serif bold navy) — Supplementary Figure->Ek Şekil; Brain Region-Specific->Beyin Bölgesine Özgü; Epigenetic Age Acceleration->Epigenetik Yaş Hızlanması; keep S8
   {"box":[210,4,1453,42], "text":"", "font":"serif","bold":True,"align":"center","size":28,"bg":[255,255,255]},
   # legend (sans, black) — keep colour dots (x<118) & n=; Cortex->Korteks, Hippocampus->Hipokampüs; "Nucleus Accumbens (n=36)" (Latin name) untouched
   {"box":[128,79,378,98], "text":"Prefrontal Korteks (n=48)", "font":"sans","align":"left","size":18,"bg":[255,255,255]},
   {"box":[128,131,360,151], "text":"Hipokampüs (n=24)", "font":"sans","align":"left","size":18,"bg":[255,255,255]},
   # ANOVA stats box (sans, navy, right-aligned, frame border at x1561) — keep PFC/NAc/Hipp/F/p/NS/values; vs->– ; yrs->yıl. "ANOVA: F=8.7, p<0.001" & "Post-hoc Tukey HSD:" have no English words -> untouched
   {"box":[1228,123,1557,143], "text":"PFC – NAc: +1.2 yıl (p=0.024)*", "font":"sans","align":"right","size":18,"pad":0.0,"bg":[255,255,255]},
   {"box":[1196,144,1557,163], "text":"PFC – Hipp: +2.1 yıl (p<0.001)***", "font":"sans","align":"right","size":18,"pad":0.0,"bg":[255,255,255]},
   {"box":[1206,163,1557,184], "text":"NAc – Hipp: +0.9 yıl (p=0.18) NS", "font":"sans","align":"right","size":18,"pad":0.0,"bg":[255,255,255]},
   # per-violin mean annotations (sans, centered under each violin; widened, neighbours verified clear) — Mean->Ortalama, yrs->yıl; keep +5.3/+4.1/+3.2; n=/95% CI lines untouched
   {"box":[311,948,464,964], "text":"Ortalama: +5.3 yıl", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[755,948,909,964], "text":"Ortalama: +4.1 yıl", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   {"box":[1199,948,1354,964], "text":"Ortalama: +3.2 yıl", "font":"sans","align":"center","size":16,"bg":[255,255,255]},
   # Functional Significance box (sans, light bg, frame x101/x547) — translate words; keep "Nucleus Accumbens" (Latin); Cortex->Korteks, Hippocampus->Hipokampüs
   {"box":[106,985,545,1005], "text":"İşlevsel Önem:", "font":"sans","italic":True,"align":"left","size":16,"pad":0.0,"bg":[248,249,251]},
   {"box":[106,1005,545,1023], "text":"Prefrontal Korteks: Karar verme, dürtü kontrolü", "font":"sans","italic":True,"align":"left","size":16,"pad":0.0,"bg":[248,249,251]},
   {"box":[106,1023,545,1042], "text":"Nucleus Accumbens: Ödül sistemi, bağımlılık merkezi", "font":"sans","italic":True,"align":"left","size":16,"pad":0.0,"bg":[248,249,251]},
   {"box":[106,1042,545,1061], "text":"Hipokampüs: Bellek, öğrenme", "font":"sans","italic":True,"align":"left","size":16,"pad":0.0,"bg":[248,249,251]},
   # bottom x-axis category labels (sans bold) — only Cortex->Korteks line ("Prefrontal" unchanged); Hippocampus->Hipokampüs; "Nucleus"/"Accumbens" (Latin) untouched
   {"box":[345,1109,432,1126], "text":"Korteks", "font":"sans","bold":True,"align":"center","size":18,"bg":[255,255,255]},
   {"box":[1205,1089,1348,1110], "text":"Hipokampüs", "font":"sans","bold":True,"align":"center","size":18,"bg":[255,255,255]},
   # y-axis label (rotated, navy) — keep Horvath (name) & EAA (abbr); (years)->(yıl)
   {"box":[11,460,33,684], "text":"Horvath EAA (yıl)", "font":"sans","align":"center","rotate":90,"bg":[255,255,255]},
 ],
}
