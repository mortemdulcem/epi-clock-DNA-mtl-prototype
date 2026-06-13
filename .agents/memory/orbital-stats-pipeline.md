---
name: Orbital stats pipeline design
description: How orbital morphometry sex-determination statistics are computed and why TS is the single source of truth.
---

# Orbital morfometri istatistik boru hattı

**Tek doğruluk kaynağı: ölçüm motoru TS'de (shared/orbitalParams.ts).** Python YENİDEN hesaplamaz; yalnızca DB'ye kaydedilmiş `measurements` JSON'u üzerinde İSTATİSTİK yapar.

**Why:** Ölçüm formüllerini hem TS hem Python'da tutmak çift-implementasyon kayması (drift) yaratır; aynı olgu iki farklı sayı verebilir → replit.md inconsistency yasağını ihlal eder. Akış: `scripts/orbital_export.cjs` (DB→düz CSV, SHA-256) → `scripts/orbital_stats.py` (seed=42, Welch t/Mann-Whitney+BH-FDR, LDA+RF CV, ROC-AUC+DeLong GA, asimetri Wilcoxon, ICC sadece reliability dosyası varsa).

**How to apply:** Yeni bir orbital parametre/ölçüm eklerken SADECE orbitalParams.ts'i değiştir; export anahtarları measurements JSON'undan dinamik okunur, Python özellikleri CSV başlığından otomatik alır — ikisinde de elle liste güncellemeye gerek yok.

## Spawn eden route'larda per-request dosya izolasyonu
`POST /api/orbital-cases/stats` script'leri spawn ederken SABİT yol kullanma. Her istek için `os.tmpdir()` altında UUID'li geçici dizin aç, `ORBITAL_OUT_CSV`/`ORBITAL_CSV`/`ORBITAL_OUT` env ile path geç, `finally`'de temizle.

**Why:** Sabit `scripts/data`/`scripts/output` yolları eşzamanlı iki kullanıcıda birbirinin çıktısını ezip cross-user veri sızıntısı yaratır (architect bunu blocking buldu). CLI çağrısı env vermeyince varsayılan committed yolları kullanır (tek-kullanıcı reproducible run için kasıtlı).

## Küçük n davranışı (zero-hallucination)
min_class<3 veya toplam<10 → model "yetersiz veri" diye AÇIKÇA atlanır, sahte sayı üretilmez. min_class 3-4 (toplam≥10) → LOOCV; ≥5 → StratifiedKFold. Cinsiyet: E=erkek=pozitif(1), K=kadın(0); sensitivityMale=TPR, specificityFemale=TNR. scripts/data ve scripts/output git-ignored (hasta türevi veri commit edilmez).
