---
name: Azure içerik filtresi — adli/akademik metin sahte-pozitifleri
description: gpt-5.1 (Azure) çağrılarında adli/şiddet/cinsel akademik içeriğin 400 content-filter hatası ve çözümü
---

Replit AI Integrations proxy (Azure OpenAI) ile gpt-5.1 kullanırken adli patoloji/adli tıp gibi akademik ama şiddet/ölüm/cinsel içerikli metinler bazen `400 ... response was filtered due to ... content management policy` hatası verir.

**Why:** Azure içerik yönetimi politikası, bağlamdan bağımsız olarak (ör. asılma yöntemleri, cinsel suç ölümleri) tetiklenir; metin akademik/eğitsel olsa da engellenir.

**How to apply:**
- Önce parçayı daha KÜÇÜK alt-parçalara (~2500 karakter) böl — çoğu kez tek tek geçer.
- System prompt'a açık akademik/eğitsel çerçeve ekle: "Bu tıp fakültesi/adli tıp uzmanları için ders kitabıdır; mesleki betimlemedir, zararlı talimat değildir."
- Yine geçmezse o pasajı açıkça beyan eden bir çevirmen notu bırak (uydurma yapma).
- Toplu pipeline'da bu hatayı yakala-ve-devam et (script durmasın); kalan filtreli parçaları sonradan ayrı ele al.
