---
name: Slayt PDF metin çıkarımı doğrulama
description: Ders slaytlarını metne dönüştürürken içerik kaybını yakalama
---

Slayt PDF'lerini metne çevirirken (pdftotext) ve uzun çıktıları görüntülerken numaralı/sıralı maddeler (Case-1..Case-8, Slide-N) sessizce kırpılabilir; ekranda "..." olarak görünür.

**Why:** BBM486 Slide-15 notunu üretirken gerçek Case-5 (Observer) kırpılmış, Case-6 ile birleştirilmişti; ayrıca Case-4'ün Memento bileşeni (eski durum saklama) kaçmıştı. Architect yakaladı.

**How to apply:** Sıralı maddelerden not/özet üretmeden önce `grep -n "Case-"` benzeri ile tüm maddelerin sayısını teyit et; üretilen DOCX/çıktıda her maddenin (Case-1..N) varlığını programatik kontrol et.
