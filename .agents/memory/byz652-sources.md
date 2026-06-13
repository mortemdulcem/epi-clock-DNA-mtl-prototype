---
name: BYZ652 cram kaynakları
description: Hangi kaynak dosya hangi içeriği taşıyor — coverage iddiası öncesi nereye bakılacağı
---
BYZ652 sınav özeti için kaynaklar `attached_assets/gdrive/arch_folder/` altında. En kapsamlı tek sentez:
**`BYZ652_calisma_rehberi (1).docx`** → `scripts/arch/rehber/rehberi.txt` (618k char, Bölüm 1–36, sınav
Q&A dahil). doc51/ders_notu BUNUN ALT KÜMESİ; bir konu doc51+ders_notu'nda yoksa rehberi.txt'e bak.

**Why:** Anti-örüntüler (Bölüm 20: Big Ball of Mud/God Object/Boilerplate/Fragile Base Class/Distributed
Monolith/Golden Hammer) ve güncel eğilimler (B.21 cloud-native/serverless/event-streaming, B.35 edge/AI/
quantum) SADECE rehberi.txt'te var, doc51/ders_notu'nda yok. Bunlar yok sanıp eksik bırakıldı, kullanıcı
"bu kaynakta var" diye düzeltti.

**How to apply:** "X içerikte var mı" denmeden önce rehberi.txt + LN01–LN10 (pdftotext -layout → /tmp/ln/)
dahil TÜM kaynakları grep'le. DOCX metni: zipfile + word/document.xml + regex <w:t> (python-docx yok).
