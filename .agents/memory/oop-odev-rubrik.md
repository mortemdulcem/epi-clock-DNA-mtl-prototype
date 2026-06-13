---
name: OOP ödev (Ebru Hoca) UML rubriği
description: Dr. Nurcan'ın OOP ödevinde hocanın UML diyagramları için gerçek değerlendirme kuralları
---

# Hocanın UML diyagramı rubriği (her soru için)
Kural (kullanıcı tarafından doğrulandı):
1. (i) Tasarım örüntüsü kullanıldıysa **adını belirt**.
2. (ii) Senaryoda **bahsi geçen metot ve nitelikler** çizimde yer almalı.
3. (iii) **Yalnızca kısa açıklama** yazılabilir — uzun analiz/tablo/gerekçe istemiyor.
4. (iv) **UML notasyonuna** uy.

**Why:** İlk teslimde "kötü" denmişti; sebep eksik sequence değil, hocanın bu 4 maddesiydi. Kullanıcı sequence diyagramı İSTEMEDİĞİNİ ve detaylı "örüntü seçimi/reddedilen alternatif" tablolarının KALDIRILMASINI açıkça onayladı (sadeleştir).

**How to apply:** Çıktı her soru için: başlık + "Kullanılan örüntü: ..." + sınıf diyagramı (metot+nitelik içeren) + tek paragraf kısa açıklama. Sequence diyagramı, uzun gerekçe tabloları, iş akışı listeleri EKLEME. PlantUML'de referans verilen her tip (enum/class) açıkça tanımlı olsun (tanımsız tip = örtük varsayım/halüsinasyon riski).

## Ders notu birleştirme (docx merge)
İki+ sınav notu docx'i tek dosyada birleştirme: `docxcompose` (kurulu) + `scripts/notes/build_birlesik_notlar.py`. Kaynak docx'ler aynen eklenir (zero-hallucination), kapak + içindekiler python-docx ile üretilir.
**Why/Dikkat:** docxcompose, FARKLI sayfa yönüne sahip bölümleri tek section'a düzleştirir — BYZ652 yatay/4-sütun cram'i portrait notlarla birleştirince landscape+cols KAYBOLDU. Aynı yönlü (portrait) notlar sorunsuz birleşir. Kullanıcı sonuçta sadece BBM486+BBS656 (ikisi de portrait) istedi.
