---
name: DOCX'e UML/geniş diyagram gömme
description: Dr. Nurcan'ın akademik DOCX'lerinde geniş diyagramların okunaklı çıkması için yerleşim kuralları
---

# Geniş diyagramları DOCX'e gömerken

**Kural:** Geniş (yatay) UML sınıf diyagramları dikey A4 sayfaya tam-genişlikte (~17.6cm) gömülünce metin okunaksız küçülür. Her diyagramı **kendi landscape (yatay) bölümüne** (section) koy ve PIL ile en-boy oranını ölç, içerik kutusuna (~27.3cm x 16.4cm) sığacak şekilde min-scale ile yerleştir.

**Why:** Dr. Nurcan sınav/tez için sürekli UML diyagramlı DOCX istiyor; portrait'te gömülen geniş diyagramlar (özellikle çok sınıflı State/Observer kombinasyonları) okunmuyordu.

**How to apply:** python-docx'te `doc.add_section(WD_SECTION.NEW_PAGE)` ile landscape bölüm aç (page_width/height swap + WD_ORIENT.LANDSCAPE), diyagram+başlık+caption'ı içine koy, sonra tekrar portrait bölüme dön. Örnek: `scripts/uml/build_uml_odev.py::place_diagram`.

**Numaralandırma gotcha:** Word "List Number" stili bölümler/sayfalar arası numarayı SÜRDÜRÜR (her soruda 1'e dönmez). Soru-bazlı 1..N iş akışı için elle `f"{i}. "` ön-eki yaz, stil kullanma.
