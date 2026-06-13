---
name: Sandbox kills detached background jobs
description: Long-running shell jobs do not survive past the bash tool call that launched them
---
Uzun süren shell işleri (ör. çok-chunk'lı çeviri), onları başlatan `bash` tool çağrısı dönünce sandbox tarafından öldürülür.

**Why:** `nohup ... &` ve hatta `setsid ... &` ile başlatılan süreçler bile bir sonraki tool çağrısına kadar yaşamadı; süreç sayısı 0'a düştü (sadece o çağrı içinde `sleep` ile canlı tutulduğu sürece çalıştı).

**How to apply:** Resumable (cache'li, idempotent) script yaz; her bir `bash` çağrısında `timeout 115 <script>` ile ÖN PLANDA çalıştır, cache birikir, bitene kadar çağrıyı tekrarla. Tek seferlik 120s tool limitini aşan işler için tek doğru desen budur.
