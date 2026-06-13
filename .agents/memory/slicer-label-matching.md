---
name: Slicer landmark label -> id eşleme tuzağı
description: Orbital landmark id'leri anatomik son-eklerle (_l lateral, _o outer) yan belirteçlerine çakışır; eşleme token-sınırlı olmalı.
---

# Slicer markup etiketi -> orbital landmark id eşlemesi

`shared/slicerImport.ts` Slicer .mrk.json/.fcsv etiketlerini ORBIT_LANDMARKS id'lerine eşler.

**Tuzak:** Landmark id'lerimiz anatomik son-ekler içerir: `_l`=lateral, `_m`=medial, `_o`=outer, `_i`=inner; ve prefiksli `lort/sort/mort/iort`. Bunlar yan belirteçleriyle (left=`l`, right=`r`, `rt`, `lt`) çakışır:
- Naif `string.includes("rt")` → `lo**rt**_o`, `so**rt**_i`, `mo**rt**` gerçek id'lerini bozar ve hepsini sağ sanır.
- `sow_l` (lateral) tek-harf `l`=left ile karışır.

**Çözüm (uygulanan):**
1. İsmi ayraçlardan token'lara böl (`split /[^a-z0-9]+/`), substring araması YAPMA.
2. Sadece çok-karakterli kesin yan token'ları (right/left/rt/lt/sag/sol/dexter/sinister) doğrudan eşle.
3. Önce kalan token'ları birleştirip nid (alt-çizgisiz id) sözlüğüyle TAM eşle — `sow_l` -> "sowl" doğrudan tutar, asla "sow"+left'e düşmez.
4. Ancak tam eşleşme yoksa, sondaki tek harf `r`/`l`yi yan kabul et (yalnızca kalan gerçek bir id ise) — `ec_r` -> ec+right.

**Why:** Architect FAIL verdi; substring tabanlı eşleme kalınlık parametrelerini (SORT/LORT/IORT/MORT) sistematik kırıyordu ve auto-side yanlış orbitaya yazıyordu.

**Doğrulama:** sow_l→sow_l, lort_o→lort_o, ec_R→ec/right, mf_left→mf/left hepsi tsx testinde doğru.
