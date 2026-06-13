---
name: drizzle-kit push yeni tablo takılması
description: Bu repoda drizzle-kit push yeni tablo eklerken interaktif rename sorusunda takılıyor; çözüm.
---

# drizzle-kit push yeni tablo eklerken takılıyor

`npm run db:push` (drizzle-kit push) bu repoda YENİ bir tablo eklenince onu mevcut bir
tablodan (ör. `sessions`) "rename" mi yoksa "create" mi diye interaktif sorar ve bekler.

- `--force` bayrağı bu rename-vs-create sorusunu **atlamıyor** (sadece veri-kaybı onayını atlar).
- Sandbox'ta `printf '\n' | npx drizzle-kit push` ile stdin beslemek **çalışmıyor** (exit -1).

**Çözüm:** Yeni tabloyu doğrudan SQL ile oluştur (executeSql callback veya psql),
şema dosyasındaki pgTable tanımıyla birebir kolonları yazarak. Sonra information_schema
ile doğrula. Drizzle tipleri zaten şema dosyasından geldiği için kod tarafı etkilenmez.

**Why:** İnteraktif prompt main agent araçlarıyla yanıtlanamıyor; tabloyu elle oluşturmak
deterministik ve hızlı.
**How to apply:** shared/schema.ts'e pgTable ekledikten sonra db:push takılırsa, CREATE TABLE
IF NOT EXISTS ile aynı kolonları doğrudan çalıştır.
