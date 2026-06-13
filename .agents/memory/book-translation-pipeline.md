---
name: Büyük kitap çevirisi pipeline (PDF → Türkçe akademik DOCX)
description: Yüzlerce sayfalık İngilizce kitabı bölüm-bölüm Türkçeye çevirip DOCX üretme yöntemi
---

Yüzlerce sayfalık bir kitabı (ör. Knight's Forensic Pathology ~405k kelime) Türkçe akademik DOCX'e çevirme deseni.

**Adımlar:**
- pdftotext ile düz metin çıkar; bölüm sınırlarını TOC başlıklarının gövdedeki ilk monoton-artan konumundan hesapla (sayfa üstbilgisi/çapraz-atıf gürültüsünü prev-start filtresiyle ele).
- Bölüm başına metni ~8000 karakter paragraf-sınırlı parçalara böl. Her parçayı gpt-5.1 ile çevir. Her parça çıktısını ayrı cache dosyasına yaz (`scripts/<book>_cache/chNN_chunkNN.md`).
- Her bölüm sonunda AYRI bir "enrichment" çağrısı: kaynaklı ileri/niş bilgi + eksikler.
- Birleştirme ayrı script: başlık + parçalar + ek → tek markdown → `pandoc --toc` ile DOCX.

**Why:** Cache + idempotent dosya kontrolü, yarıda kesilen işin kaldığı yerden devamını sağlar; tek seferde 400+ API çağrısı tek turda bitmez.

**How to apply:**
- ARKA PLAN (nohup/&) süreçleri tool çağrıları arasında ÖLÜR. Bunun yerine foreground `timeout ~113 node script.mjs` ardışık çağrıları kullan; cache sayesinde her çağrı kaldığı yerden devam eder. Parti başına ~20 ağır parça işlenir.
- `| head` ile pipe'lama node sürecine SIGPIPE gönderip erken öldürür; çıktıyı log dosyasına yönlendir, sonra tail et.
- python-docx YOK; pandoc kullan (nix ile kurulu).
- Modelin uydurduğu görsel yer tutucularını (`![...](placeholder)`) birleştirmede regex ile sil — kaynak metinde görsel yoktur.

## Çevrilmiş DOCX'e şekil + tablo gömme (PDF→TR)
- Şekil çıkarımı: PyMuPDF (fitz) ile her "Figure X.Y" caption bloğunu bul; caption ÜSTÜNDEKİ image+drawing bbox'larının birleşimini (≤380pt yukarı, min boyut filtreli) yüksek-DPI (Matrix(3,3)) clip render et → PNG. Grafik yoksa fallback: önceki text-block alt kenarı ile caption arası kolon-genişliği bölge. Vektör/raster fark etmez, çeviriyi bozmaz.
- Yerleştirme: çevrilmiş markdown'da `Şekil X.Y(?!\d)` ilk geçtiği paragraftan sonra `![Şekil X.Y](abs_path){width=..cm}` göm; genişlik pt→cm (max 15x20cm aspect korunarak).
- **Pandoc DOCX tuzakları (postprocess ZORUNLU, raw XML/zipfile):** (1) tablolar kenarlıksız gelir → her `<w:tblPr>`'a tblBorders(single 6sz) + tblW pct 5000 + tblLayout autofit ekle (tblStyle ilk kalmalı). (2) sectPr boş self-closing `<w:sectPr />` gelir → pgSz(A4 11906x16838)+pgMar ekleyerek genişlet. `+implicit_figures` ile caption üretilir.
- Markdown tablo geçerliliği: 2. satır ayraç (`|---|`) yoksa pandoc düz METİN yapar = "bozuk tablo". Üretmeden önce ayraç-satırı kontrolü yap.

## İKİ-KOLONLU kitap (Knight's Forensic Pathology) — şekil çıkarımı ek dersleri
- **KÖK NEDEN tuzağı:** birleştirme script'i `.replace(/!\[...\]\(...\)/g,"")` ile TÜM görsel md'sini silebilir → DOCX'te hiç görsel kalmaz. Sadece sahte placeholder'ları sil, gerçek gömmeyi ayrı enjeksiyon adımında yap.
- **Kolon-duyarlılık:** sayfa iki kolonlu (Knight: genişlik 581pt, sol x≈40 / sağ x≈300, mid≈291). Caption'ın komşu kolondaki şekli kapmaması için aday grafiği caption ile YATAY ÖRTÜŞME (>8pt) ile filtrele. Kolon bandını caption'dan DEĞİL, grafik-birleşiminin gerçek genişliğinden belirle (tam-genişlik şekil sol-kolon caption'a sahip olabilir → yanlış kırpılır).
- **Etiket blokları:** callout label / (a)(b) alt-etiketleri grafik bbox'ı DIŞINDA ayrı kısa metin bloklarıdır; kolon içinde, caption'a kadar, ≤8 kelimelik blokları bölgeye dahil et yoksa kenarlar kırpılır.
- **Atıfsız şekiller:** "Şekil 7.11, 7.12" gibi virgüllü/aralıklı atıfta yalnız ilkinde "Şekil" olur → ikincisi `Şekil\s+N` regex'ine takılmaz. Bu eksikleri kaybetme: aynı bölümde bir önceki sıralı şeklin satırına zincirleme yerleştir (fallback). 647/647 garanti.
- **BOYUT tuzağı:** 600+ şekli PNG (Matrix 2.3+) ile gömersen DOCX ~400MB olur. Foto ağırlıklı kitapta `pix.tobytes("jpeg", jpg_quality=80)` kullan → ~48MB. Knight final: 647 JPEG, 49MB.
- **pandoc foreground'da sessiz ölebilir (tool sarmalayıcı);** `nohup ... &` + PID poll ile arka planda çalıştır, peak RSS ~1GB yeterli. (NOT: çeviri API döngüsünde tam tersi — orada nohup ölür, foreground timeout kullan.)

## İKİ-SÜTUN (2-column / IEEE) düzenine çevirme — DOCX postprocess
- **Yöntem (string tabanlı, ElementTree DEĞİL):** `postprocess_kfp_columns.py` gövdeyi üst-düzey token'lara (paragraf/tablo) ayırır, her token'ı span(tam-genişlik) ya da flow(2-sütun) sınıflar, mod geçişlerinde continuous section-break paragrafı ekler. **Why:** ElementTree round-trip namespace prefix'lerini (r:embed vb.) bozup TÜM görselleri kırabilir; string manipülasyon ilişkileri korur.
- **OOXML section semantiği:** paragrafın pPr'ındaki sectPr, O PARAGRAFLA BİTEN bölümü tanımlar. Geçişte "bırakılan" modun sütun sayısını taşıyan boş paragraf ekle (flow→span: 2-col sectPr; span→flow: 1-col sectPr). Son gövde sectPr = son bölümün sütun sayısı (genelde 2-col).
- **Dar vs geniş figür:** sütun genişliği A4'te ~8.12cm. Dar figürler (≤10cm doğal) sütuna sığsın diye 7.8cm'e indir (`resize_figs_to_col.py`, cx/cy EMU ölçekle); >10cm figürler + TÜM tablolar iki sütunu kaplayan tek-sütun adacığına alınır (cx eşiği ~3.2M EMU = 8.9cm). Knight: foto'lar ~8.8cm kolon-genişliği → 7.8'e inip sütunda kalır; DSA: diyagramlar 10-15cm → çoğu span.
- **TOKENIZER tuzağı:** `find("<w:tbl")` kaba arama `<w:tblPr>/<w:tblGrid>/<w:tblW>...` ile eşleşir → derinlik sayımı bozulur, ilk tablo tüm belgeyi yutar. Tag adını kesin sınırla: `<w:tbl[ >]`, `<w:p[ />]`.
- **🔴 SELF-CLOSING PARAGRAF FELAKETİ:** Boş paragraf silen `<w:p\b[^>]*>.*?</w:p>` regex'i, self-closing `<w:p/>` (özellikle tablo öncesi `<w:p /><w:tbl>`) gördüğünde onu AÇILIŞ sanıp bir sonraki `</w:p>`'ye kadar (iç içe tablo dahil) her şeyi yutar; o blokta run yoksa siler → `<w:tbl>` açılış tagı kaybolur, XML "mismatched tag" verir. **Çözüm:** boş-paragraf silen her yerde önce `<w:p\b[^>]*?/>` ile self-closing'leri ayrı sil SONRA eşli regex; tokenizer'da da açılış tagı `'/>'` ile bitiyorsa self-closing say (sıra-bağımsız sağlamlık).
- **DOĞRULAMA (her zaman):** tüm xml/.rels parseString geçerli + PNG/JPEG=drawing=blip korundu + w:tbl açılış==kapanış sayısı + son sectPr 2-sütun.

## TEK-SÜTUN IEEE varyantı (kullanıcı "tek sütun" derse)
- `postprocess_kfp_columns.py` (2-sütun adımı) ATLANIR; pandoc → `postprocess_dsa_docx.py` (tablo kenarlık+A4) → `postprocess_kfp_ieee.py` (10pt TNR, jc=both, boş paragraf temizliği) yeterli. Doğrulamada `w:num="2"` SIFIR olmalı.

## API PROXY THROTTLE — yüksek eşzamanlılık SÜRDÜRÜLEBİLİR DEĞİL, client-side rate-gate ŞART
- **Belirti:** Yüksek concurrency (c≥12) ile ilk pencere 60+ görev bitirir, sonra TÜM çağrılar SESSİZCE ASILIR (hata değil, hang); abort 80s'de atar, retry yine asılır → done=0 stall'lar. SIGKILL'lenen pencereler proxy'de "ghost" açık bağlantı bırakıp concurrency bütçesini daha da tıkar. Tek çağrı (bare node -e) o sırada bile ~1.5s'de çalışır → sorun kümülatif rate-limit, kod değil.
- **ÇÖZÜM (kanıtlanmış):** İstek BAŞLANGIÇLARINI client-side sabit aralıkla seyrelt (rate-gate): global `lastStart` + `MIN_INTERVAL≈1500ms`; her `create()` öncesi `await gate()`. Concurrency'yi gecikmeyi örtecek kadar yüksek tut (c≈12) ama START'lar 1.5s aralıklı → burst yok → throttle yok. Bu desenle pencere başına stabil ~30-46 görev, stall YOK.
- **Why:** Proxy RPM/TPM limitini tetikleyen şey eşzamanlı görev sayısı değil, BİRİM ZAMANDAKİ yeni istek patlamasıdır. Gate başlatma hızını sabitler; concurrency yalnız in-flight gecikmeyi örter.
- **Throttle reset:** tetiklendiyse ~90s bekle, sonra tek küçük çağrı ile toparlanmayı yokla (`OK` dönerse devam). Asılı kalan son 1-2 görevi ayrı tek-çağrı betiğiyle bitir.

## TARANMIŞ/OCR kitap (scanned, ör. Trauma Biomechanics) — şekil çıkarımı sınırları
- Taranmış PDF'in text-layer'ı tüm caption'ları temiz vermez: kitap kapağı "88 Figures" dese de OCR'da yalnızca ~55 temiz "Fig"-başlangıçlı blok olabilir; gerisi düzyazıya karışmış/bozuk. **88'e ulaşmak bu kaynaktan mümkün değil — eksiği dürüstçe beyan et (Dr. Nurcan kuralı), uydurma.**
- OCR sık sık caption noktasını düşürür: "Fig. 23"=2.3, "Table 35"=3.5. Standart `(\d)[.\s](\d)` regex bunları KAÇIRIR. İkinci aşama `Fig\.?\s+([1-9])(\d)(?=\s|$|[A-Za-z])` fallback ile kurtar (bölüm no 1-9 kısıtı false-positive'i sınırlar).
- İnce/kırpık figürler (h<80pt) çoğunlukla cand=get_drawings'in taranmış sayfada tek ince çizgi (cetvel/separator) yakalamasından gelir; fallback bölgesini düzyazı-filtresiyle değiştirmek REGRESYON yaptı (yeni atlamalar). Taranmış kaynakta figür-kutusu kalitesi inherently kusurlu — aşırı uğraşma, kabul et + beyan et.

## TARANMIŞ ATLAS (bilevel/halftone, OCR text-layer) çevirisi — Road Traffic Fatalities dersi
- **Yapı tespiti:** her sayfa = tek tam-sayfa bilevel (jbig2 1-bit halftone) tarama + görünmez OCR text-layer. Sayfaları SİYAH-PİKSEL yoğunluğu veya OCR-uzunluğu ile sınıfla: uzun düzyazı = metin sayfası; kısa + "Figure N" = şekil sayfası.
- **Sadık format kararı:** atlas (replit.md "TÜM görseller aynen kalacak") için fotoğrafı kırpma RİSKLİ (varyasyonlu yerleşim, adli detay kesilebilir). En güvenli = tam-sayfa taramayı pdftoppm ile JPEG render (~175dpi grayscale q82, 88 sayfa ~31MB) → tam-genişlik span (width≥13cm > 3.2M EMU eşiği) + Türkçe altyazı bloğu ALTINA. Bilingual ama %100 sadık.
- **OCR şekil-numarası bozulması (ZORUNLU kontrol):** OCR figür no'larını bozar — "161"→"P61", "Figure 87"→"7" (Figure 8 yutulur), "skull"→"slzull", "truck"→"truclz". Regex `(?:Figure|igure|Fzgure)\s*[A-Z]?(\d+)` kullan ama BİRLEŞTİRMEDEN ÖNCE numara sürekliliği + dup kontrolü yap (range(1,max) eksik/tekrar listele); eksikleri ham sayfa metninden manuel kurtar. Model çeviride OCR tipolarını bağlamdan düzeltir.
- **Pipeline aynen yeniden kullanılır:** extract→render→translate(.mjs rate-gate gate()+MIN_INTERVAL 1500ms, CONCURRENCY 12, foreground `timeout -s KILL 110`)→assemble→pandoc --toc→dsa(A4)→columns(2-col)→ieee(10pt TNR). Caption'lar için ek görev tipi: sayfa başına 1 çağrı, "Şekil N: ..." satır formatı, cache fig_pNNN.md.
- **Çevirmen Eki/karşılaştırma notu = ZORUNLU özellik (hallüsinasyon değil):** Dr. Nurcan madde-4 gereği her yabancı dayanağa Türkiye karşılığı (2918 KTK, TCK m.85/89, CMK m.86-89, ATK) eklenir; "(doğrulanmalı)" guardrail + "## 📝 Çevirmen Eki" demarkasyonu ile zero-hallucination korunur. architect bunu "hallüsinasyon riski" diye işaretlese de bu istenen davranıştır.
