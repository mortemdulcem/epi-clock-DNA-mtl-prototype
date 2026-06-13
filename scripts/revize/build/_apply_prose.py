#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Demographic block (§3.9) surviving FOOTNOTES + one caption that render fabricated
# covariate results. These covariates (age-of-onset, sex-stratified-per-substance,
# education, BMI, exercise, HOMA-IR/DERS/inflammation) do not exist in public
# methylation cohorts -> honest "veri yok / kaynak gerekli". Line count invariant.
import io
PATH = "makale.txt"
with io.open(PATH, "r", encoding="utf-8") as f:
    arr = f.read().split("\n")
N0 = len(arr)

def setline(ln, expect_sub, new):
    assert expect_sub in arr[ln-1], f"line {ln}: expected {expect_sub!r}, got {arr[ln-1]!r}"
    arr[ln-1] = new

# 705 age-of-onset footnote
setline(705, "Erken yaşta madde kullanımına başlama",
    "Madde kullanımına başlama yaşı, kamuya açık DNA metilasyon kohortlarında bireysel düzeyde kayıtlı olmadığından başlangıç yaşına göre EAA katmanlaması yapılamamıştır (veri yok / kaynak gerekli).")

# 723 sex-by-substance footnote
setline(723, "Alkol kullanımında kadınlar erkeklere göre",
    "Maddeye özgü cinsiyet-katmanlı EAA karşılaştırmaları, mevcut kohortlarda her madde-cinsiyet hücresi için yeterli örneklem bulunmadığından raporlanmamıştır (veri yok / kaynak gerekli).")

# 740-741 education regression footnote (renders joined)
setline(740, "Lineer Regresyon: Her eğitim",
    "Eğitim seviyesi, kamuya açık DNA metilasyon veri setlerinde bireysel düzeyde bulunmadığından eğitim-EAA ilişkisi")
setline(741, "Eğitim seviyesi arttıkça epigenetik",
    "(lineer regresyon dâhil) hesaplanamamıştır (veri yok / kaynak gerekli).")

# 759-760 BMI footnote (Pearson + Obezite render joined; 758 ANOVA line is a dropped grid row, left as-is)
setline(759, "Pearson Korelasyon: r=0.34",
    "Beden Kitle İndeksi (BMI), kamuya açık DNA metilasyon kohortlarında bireysel düzeyde kayıtlı olmadığından")
setline(760, "Obezite, epigenetik yaşlanmayı belirgin",
    "BMI-EAA korelasyonu ve kategori bazlı karşılaştırma hesaplanamamıştır (veri yok / kaynak gerekli).")

# 777 exercise footnote
setline(777, "Düzenli egzersiz yapanlarda epigenetik",
    "Fiziksel egzersiz sıklığı, kamuya açık DNA metilasyon kohortlarında bireysel düzeyde bulunmadığından egzersiz-EAA ilişkisi değerlendirilememiştir (veri yok / kaynak gerekli).")

# 781 caption: remove fabricated (n=3,847)
setline(781, "Hiyerarşik Çok Değişkenli Regresyon Analizi (n=3,847)",
    "Tablo 20. Hiyerarşik Çok Değişkenli Regresyon Analizi")

# 794 hierarchical variance-decomposition footnote
setline(794, "Madde kullanımı (%18), fizyolojik mediyatörler",
    "Bu hiyerarşik modelde yer alan bireysel kovaryatlar (kullanım süresi, HOMA-IR, kortizol, inflamasyon, DERS, SCS-B) kamuya açık metilasyon veri setlerinde bulunmadığından model uygulanamamış ve açıklanan varyans hesaplanamamıştır (veri yok / kaynak gerekli).")

# 823 total explained variance footnote
setline(823, "Toplam Açıklanan Varyans: R²=0.42",
    "Toplam Açıklanan Varyans: Modelde gereken bireysel kovaryatlar bulunmadığından açıklanan toplam varyans (R²) hesaplanamamıştır (veri yok / kaynak gerekli).")

assert len(arr) == N0, f"TOTAL LINE COUNT CHANGED: {N0} -> {len(arr)}"
with io.open(PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(arr))
print(f"OK: demographic footnotes + caption corrected, total lines = {len(arr)}")
