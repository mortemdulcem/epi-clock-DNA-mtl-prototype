// ==UserScript==
// @name         PACS BESK Toplu DICOM Indirici
// @namespace    nurcan.tez
// @version      2.7
// @description  PACS MobileDicomViewer - tum kesitleri otomatik kesfeder, ZIP olarak indirir. GM_download ile sekme kapansa bile inme tamamlanir.
// @match        http://pacs.besk.local/ImageServer/Pages/MobileDicomViewer/*
// @match        https://pacs.besk.local/ImageServer/Pages/MobileDicomViewer/*
// @run-at       document-start
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_deleteValue
// @grant        GM_download
// ==/UserScript==

(function () {
  'use strict';

  function rTimeout(fn, ms) { setTimeout(fn, ms); }

  // ========== MANUEL STORE ZIP ENCODER (JSZip yerine, donma riski yok) ==========
  // CRC-32 tablosu
  var CRC_TABLE = (function () {
    var t = new Uint32Array(256);
    for (var i = 0; i < 256; i++) {
      var c = i;
      for (var j = 0; j < 8; j++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[i] = c >>> 0;
    }
    return t;
  })();
  function crc32(bytes) {
    var c = 0xFFFFFFFF;
    for (var i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }
  function utf8(s) {
    return new TextEncoder().encode(s);
  }
  // ZIP STORE encoder - dosyalari teker teker isler, tek seferde Blob olarak doner
  // Memory: max(en buyuk dosya) + central directory. JSZip'ten cok daha verimli.
  async function buildStoreZip(files, onProgress) {
    // files: [{name, blob}]
    var parts = [];
    var central = [];
    var offset = 0;
    var now = new Date();
    var dosTime = ((now.getHours() & 0x1F) << 11) | ((now.getMinutes() & 0x3F) << 5) | ((now.getSeconds() / 2) & 0x1F);
    var dosDate = (((now.getFullYear() - 1980) & 0x7F) << 9) | (((now.getMonth() + 1) & 0x0F) << 5) | (now.getDate() & 0x1F);

    for (var i = 0; i < files.length; i++) {
      var f = files[i];
      var nameBytes = utf8(f.name);
      var data = new Uint8Array(await f.blob.arrayBuffer());
      var crc = crc32(data);
      var size = data.length;

      // Local file header (30 byte + name)
      var lfh = new ArrayBuffer(30 + nameBytes.length);
      var dv = new DataView(lfh);
      dv.setUint32(0, 0x04034b50, true);   // signature
      dv.setUint16(4, 20, true);           // version needed
      dv.setUint16(6, 0x0800, true);       // flags (UTF-8 names)
      dv.setUint16(8, 0, true);            // method = STORE
      dv.setUint16(10, dosTime, true);
      dv.setUint16(12, dosDate, true);
      dv.setUint32(14, crc, true);
      dv.setUint32(18, size, true);        // compressed size = uncompressed
      dv.setUint32(22, size, true);
      dv.setUint16(26, nameBytes.length, true);
      dv.setUint16(28, 0, true);           // extra length
      new Uint8Array(lfh, 30).set(nameBytes);

      parts.push(new Uint8Array(lfh));
      parts.push(data);

      // Central directory record
      var cdr = new ArrayBuffer(46 + nameBytes.length);
      var dv2 = new DataView(cdr);
      dv2.setUint32(0, 0x02014b50, true);
      dv2.setUint16(4, 20, true);          // version made by
      dv2.setUint16(6, 20, true);          // version needed
      dv2.setUint16(8, 0x0800, true);
      dv2.setUint16(10, 0, true);
      dv2.setUint16(12, dosTime, true);
      dv2.setUint16(14, dosDate, true);
      dv2.setUint32(16, crc, true);
      dv2.setUint32(20, size, true);
      dv2.setUint32(24, size, true);
      dv2.setUint16(28, nameBytes.length, true);
      dv2.setUint16(30, 0, true);
      dv2.setUint16(32, 0, true);
      dv2.setUint16(34, 0, true);
      dv2.setUint16(36, 0, true);
      dv2.setUint32(38, 0, true);
      dv2.setUint32(42, offset, true);
      new Uint8Array(cdr, 46).set(nameBytes);
      central.push(new Uint8Array(cdr));

      offset += 30 + nameBytes.length + size;

      if (onProgress) onProgress(i + 1, files.length);
      // event loop'a nefes ver (UI donmasin)
      if ((i % 5) === 0) await new Promise(function (r) { setTimeout(r, 0); });
    }

    // Central directory
    var cdStart = offset;
    var cdSize = 0;
    for (var c = 0; c < central.length; c++) {
      parts.push(central[c]);
      cdSize += central[c].length;
    }

    // End of central directory record (22 byte)
    var eocd = new ArrayBuffer(22);
    var dv3 = new DataView(eocd);
    dv3.setUint32(0, 0x06054b50, true);
    dv3.setUint16(4, 0, true);
    dv3.setUint16(6, 0, true);
    dv3.setUint16(8, files.length, true);
    dv3.setUint16(10, files.length, true);
    dv3.setUint32(12, cdSize, true);
    dv3.setUint32(16, cdStart, true);
    dv3.setUint16(20, 0, true);
    parts.push(new Uint8Array(eocd));

    return new Blob(parts, { type: 'application/zip' });
  }
  // ========== / MANUEL ZIP ENCODER ==========

  // Yakalanan WADO URL'leri (orijinal)
  var WADO = new Set();
  // seriesUID -> ornek URL (base'i cikarmak icin)
  var SERIES_SAMPLE = {};
  // seriesUID -> [TUM yakalanan URL'ler] (scroll sirasinda dolar)
  var WADO_BY_SERIES = {};
  var META = { studyUid: '', patientId: '', patientName: '' };

  // Hasta adini sayfadan cek (OZBEN^FERIHA FIKRET formatini ara)
  function findPatientName() {
    if (META.patientName) return META.patientName;
    var sels = ['#patientName', '.patientName', '[data-patient-name]', '.patient-info', '.study-info', '.viewer-header'];
    for (var i = 0; i < sels.length; i++) {
      var el = document.querySelector(sels[i]);
      if (el && el.textContent) {
        var t = el.textContent.trim();
        if (t && t.length < 80) return t;
      }
    }
    // DICOM PN format (^) iceren elementleri ara
    var all = document.querySelectorAll('div, span, td, h1, h2, h3, h4, p, label');
    for (var j = 0; j < all.length; j++) {
      var t2 = (all[j].textContent || '').trim();
      if (t2.length > 4 && t2.length < 60 && /\^/.test(t2) && /^[A-ZÇĞİÖŞÜ]{2,}/.test(t2)) {
        return t2;
      }
    }
    return '';
  }

  function parseQs(u) {
    var qs = u.split('?')[1] || '';
    var p = {};
    qs.split('&').forEach(function (kv) {
      var i = kv.indexOf('=');
      if (i > 0) p[kv.substring(0, i)] = decodeURIComponent(kv.substring(i + 1));
    });
    return p;
  }

  function addWadoUrl(u) {
    if (typeof u !== 'string') return;
    if (u.indexOf('/wado/BESKPACS') < 0) return;
    if (u.indexOf('ContentType=application/dicom') < 0) return;
    if (WADO.has(u)) return;
    WADO.add(u);
    try {
      var p = parseQs(u);
      if (p.studyUID) META.studyUid = p.studyUID;
      if (p.seriesUID) {
        if (!SERIES_SAMPLE[p.seriesUID]) SERIES_SAMPLE[p.seriesUID] = u;
        if (!WADO_BY_SERIES[p.seriesUID]) WADO_BY_SERIES[p.seriesUID] = [];
        WADO_BY_SERIES[p.seriesUID].push(u);
      }
    } catch (_) {}
  }

  // Viewer'da scroll edilebilir konteyneri bul
  function findScrollables() {
    var all = document.querySelectorAll('div, section, main');
    var scrollables = [];
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      var s = window.getComputedStyle(el);
      if ((s.overflowY === 'scroll' || s.overflowY === 'auto') &&
          el.scrollHeight - el.clientHeight > 50) {
        scrollables.push(el);
      }
    }
    // En buyuk scroll kapasiteli olanlari öncelikle dene
    scrollables.sort(function (a, b) { return b.scrollHeight - a.scrollHeight; });
    return scrollables;
  }

  // Viewer'i otomatik scroll et — viewer kesitleri sirasiyla yukler, sniffer yakalar
  // Birden fazla scrollable + canvas wheel + ok tusu fallback kullanir.
  async function autoScroll(onProgress) {
    var beforeUrlCount = WADO.size;
    var scrollables = findScrollables();
    console.log('[PACS-DL] Bulunan scrollable sayisi:', scrollables.length);
    var maxIter = 250;
    var lastNewCount = beforeUrlCount;
    var stallCount = 0;

    // Strateji 1: Tum scrollable konteynerleri scroll et
    for (var sc = 0; sc < scrollables.length; sc++) {
      var el = scrollables[sc];
      el.scrollTop = 0;
      await delay(200);
      var maxScroll = el.scrollHeight - el.clientHeight;
      var step = Math.max(20, Math.floor(maxScroll / 100));
      console.log('[PACS-DL] Scroll edilen el:', el.tagName, 'maxScroll:', maxScroll, 'step:', step);
      for (var y = 0; y <= maxScroll; y += step) {
        el.scrollTop = y;
        await delay(80);
      }
      el.scrollTop = maxScroll;
      await delay(300);
    }

    // Strateji 2: Canvas/viewport uzerine wheel olayi gonder
    var canvases = document.querySelectorAll('canvas');
    console.log('[PACS-DL] Canvas sayisi:', canvases.length);
    for (var c = 0; c < canvases.length; c++) {
      var canv = canvases[c];
      var rect = canv.getBoundingClientRect();
      if (rect.width < 50 || rect.height < 50) continue;
      // 200 kez asagi wheel
      for (var w = 0; w < maxIter; w++) {
        canv.dispatchEvent(new WheelEvent('wheel', {
          deltaY: 100, deltaMode: 0,
          clientX: rect.left + rect.width / 2,
          clientY: rect.top + rect.height / 2,
          bubbles: true, cancelable: true
        }));
        if (w % 5 === 0) {
          await delay(60);
          if (onProgress) onProgress(WADO.size - beforeUrlCount);
          // Yeni URL gelmiyorsa duraksa
          if (WADO.size === lastNewCount) {
            stallCount++;
            if (stallCount > 8) break;
          } else {
            stallCount = 0;
            lastNewCount = WADO.size;
          }
        }
      }
    }

    // Strateji 3: Body/document uzerinde Ok asagi tus olayi
    for (var k = 0; k < 200; k++) {
      document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', code: 'ArrowDown', keyCode: 40, bubbles: true }));
      document.body.dispatchEvent(new KeyboardEvent('keydown', { key: 'PageDown', code: 'PageDown', keyCode: 34, bubbles: true }));
      if (k % 10 === 0) await delay(50);
    }
    await delay(500);
    var gained = WADO.size - beforeUrlCount;
    console.log('[PACS-DL] Auto-scroll tamam. Yeni URL:', gained, 'Toplam:', WADO.size);
    return gained;
  }

  // XHR + fetch hook
  var oOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) {
    addWadoUrl(u);
    try {
      if (typeof u === 'string' && u.indexOf('patientId=') > 0) {
        var m2 = u.match(/patientId=(\d+)/);
        if (m2) META.patientId = m2[1];
      }
    } catch (_) {}
    return oOpen.apply(this, arguments);
  };
  var oFetch = window.fetch;
  window.fetch = function (u, opts) {
    var url = typeof u === 'string' ? u : (u && u.url) || '';
    addWadoUrl(url);
    return oFetch.apply(this, arguments);
  };

  function safeName(s) {
    return (s || 'unknown').replace(/[\\/:*?"<>|^]/g, '_').replace(/\s+/g, '_').substring(0, 60);
  }
  function delay(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  // Bir series icin tum objectUID'leri kesfet (base.N icin N=1..MAX)
  async function discoverSeries(seriesUID, sampleUrl, onProgress) {
    var p = parseQs(sampleUrl);
    var base = (p.objectUID || '').split('.').slice(0, -1).join('.');
    if (!base) return [];

    var baseUrl = sampleUrl.split('?')[0];
    var found = [];
    var miss = 0;
    var MAX = 1500;       // guvenli ust sinir
    var STOP_AFTER_404 = 8;

    var batch = 16;
    for (var n = 1; n <= MAX; n += batch) {
      var promises = [];
      for (var k = 0; k < batch && (n + k) <= MAX; k++) {
        var nn = n + k;
        var url = baseUrl + '?requesttype=WADO' +
                  '&studyUID=' + encodeURIComponent(p.studyUID) +
                  '&seriesUID=' + encodeURIComponent(seriesUID) +
                  '&objectUID=' + encodeURIComponent(base + '.' + nn) +
                  '&ContentType=application/dicom';
        promises.push(fetch(url).then(function (r) {
          return { ok: r.ok, status: r.status, blob: r.ok ? r.blob() : null, url: r.url || url, n: this };
        }.bind(nn)).catch(function (e) { return { ok: false, status: 0, n: this }; }.bind(nn)));
      }
      var results = await Promise.all(promises);
      for (var i = 0; i < results.length; i++) {
        var r = results[i];
        if (r.ok && r.blob) {
          var blob = await r.blob;
          // Cok kucuk = bos/hata, atla
          if (blob && blob.size > 1000) {
            found.push({ n: r.n, blob: blob });
            miss = 0;
          } else {
            miss++;
          }
        } else {
          miss++;
        }
      }
      if (onProgress) onProgress(found.length, n + batch);
      if (miss >= STOP_AFTER_404) break;
    }
    return found;
  }

  // Bir DICOM dosyasinin ilk 16KB'sini tarayip seri tipi tespit et (KEMIK/BEYIN/YUMUSAK)
  async function classifySeries(seriesUID, sampleUrl) {
    try {
      var p = parseQs(sampleUrl);
      var base = (p.objectUID || '').split('.').slice(0, -1).join('.');
      if (!base) return { type: 'UNKNOWN', desc: '', wc: 0, ww: 0 };
      var url = sampleUrl.split('?')[0] + '?requesttype=WADO' +
                '&studyUID=' + encodeURIComponent(p.studyUID) +
                '&seriesUID=' + encodeURIComponent(seriesUID) +
                '&objectUID=' + encodeURIComponent(base + '.1') +
                '&ContentType=application/dicom';
      var resp = await fetch(url);
      if (!resp.ok) return { type: 'UNKNOWN', desc: '', wc: 0, ww: 0 };
      var buf = await resp.arrayBuffer();
      if (buf.byteLength < 1000) return { type: 'UNKNOWN', desc: '', wc: 0, ww: 0 };
      var bytes = new Uint8Array(buf, 0, Math.min(buf.byteLength, 32768));
      var text = '';
      for (var i = 0; i < bytes.length; i++) {
        var c = bytes[i];
        text += (c >= 32 && c < 127) ? String.fromCharCode(c) : ' ';
      }
      var T = text.toUpperCase();
      // Series Description (0008,103E) - genelde acik metin olarak yazili
      // Window Center (0028,1050) ve Window Width (0028,1051) - bone window: WC=300-700, WW=1500-3500
      var descMatch = '';
      var typ = 'UNKNOWN';
      if (/KEMIK|\bBONE\b|OSSEOUS|OSSIOUS|KNOCHEN/.test(T)) typ = 'KEMIK';
      else if (/BEYIN|\bBRAIN\b|CEREBRAL|CEREBRUM/.test(T)) typ = 'BEYIN';
      else if (/YUMUSAK|\bSOFT\b|WEICHTEIL/.test(T)) typ = 'YUMUSAK';

      // Pencere genisligi ile dogrula (kemik penceresinde WW>1000)
      var wc = 0, ww = 0;
      var wcMatch = T.match(/(\d{2,5})\s*\\?\s*(\d{2,5})/);
      // Daha guvenli: ascii icinde "DS" sonrasi sayilari ara — basit tutalim
      // Eger description'da hicbir keyword yoksa, byte arrayde window width ara
      if (typ === 'UNKNOWN') {
        // Basit heuristic: 1500-3500 araligindaki sayilar bone window olabilir
        var nums = T.match(/\b(1[5-9]\d{2}|2\d{3}|3[0-5]\d{2})\b/g);
        if (nums && nums.length >= 1) typ = 'KEMIK_TAHMIN';
      }
      return { type: typ, desc: descMatch, wc: wc, ww: ww };
    } catch (e) {
      return { type: 'UNKNOWN', desc: '', wc: 0, ww: 0 };
    }
  }

  async function smartZip() {
    var btn = document.getElementById('pacs-dl-btn');
    var stat = document.getElementById('pacs-dl-status');
    btn.disabled = true;
    btn.style.background = '#a60';

    var isOto = false;
    try { isOto = localStorage.getItem('OTO_AUTO') === '1'; } catch (_) {}

    var seriesIds = Object.keys(SERIES_SAMPLE);
    if (seriesIds.length === 0) {
      btn.textContent = 'Once viewer yuklensin (5sn bekle)';
      btn.style.background = '#a00';
      btn.disabled = false;
      return;
    }

    var pid = META.patientId || 'NN';
    var pname = findPatientName();
    if (pname) META.patientName = pname;
    var shortStudy = (META.studyUid || 'study').split('.').slice(-2).join('_');
    var nameSlug = pname ? safeName(pname.replace(/\^/g, '_')) + '_' : '';
    var fileBase = 'DICOM_' + nameSlug + safeName(pid) + '_' + shortStudy;

    if (isOto) {
      console.log('[PACS-DL] TURBO MOD: Scroll atlanıyor, direkt enumeration');
      btn.textContent = '⚡ TURBO: Direkt indirme (scroll yok)...';
    } else {
      btn.textContent = 'Otomatik scroll (kesitler yukleniyor)...';
      console.log('[PACS-DL] Manuel mod: Auto-scroll basliyor. Mevcut URL:', WADO.size);
      await autoScroll(function (gained) {
        btn.textContent = 'Scroll: +' + gained + ' kesit yakalandi';
      });
    }
    seriesIds = Object.keys(SERIES_SAMPLE);
    console.log('[PACS-DL] Seri sayisi:', seriesIds.length);
    for (var sid in WADO_BY_SERIES) {
      console.log('[PACS-DL] Seri', sid.split('.').slice(-3).join('_'), '→', WADO_BY_SERIES[sid].length, 'URL');
    }

    // 2. Her serinin tipini tespit et (kemik/beyin/yumusak)
    btn.textContent = 'Seriler siniflandiriliyor...';
    var classes = {};
    for (var c = 0; c < seriesIds.length; c++) {
      classes[seriesIds[c]] = await classifySeries(seriesIds[c], SERIES_SAMPLE[seriesIds[c]]);
      console.log('[PACS-DL] Seri ' + (c + 1) + ' tipi:', classes[seriesIds[c]], '— URL:', (WADO_BY_SERIES[seriesIds[c]] || []).length);
    }

    // 2. Sadece KEMIK olanlari sec (varsa). Yoksa hepsini al (ZIP yine olmasin).
    var kemikIds = seriesIds.filter(function (id) { return classes[id].type === 'KEMIK' || classes[id].type === 'KEMIK_TAHMIN'; });
    var hedefIds;
    if (kemikIds.length > 0) {
      hedefIds = kemikIds;
      btn.textContent = '🦴 ' + kemikIds.length + ' kemik seri secildi (' + (seriesIds.length - kemikIds.length) + ' atlandi)';
      console.log('[PACS-DL] KEMIK serileri:', kemikIds);
    } else {
      // Kemik bulunamadi - hepsini indir (yedek)
      hedefIds = seriesIds;
      btn.textContent = '⚠ Kemik seri yok, hepsi (' + seriesIds.length + ')';
      console.log('[PACS-DL] UYARI: Kemik seri bulunamadi, hepsi indiriliyor');
    }
    await delay(800);

    // Tum kesitleri tek listede topla (manuel ZIP encoder icin)
    // YENI YAKLASIM: Auto-scroll sayesinde sniffer URL'leri yakaladi.
    // Yakalanan URL'leri DOGRUDAN indir, tahmin etmeye gerek yok.
    var allFiles = [];

    for (var s = 0; s < hedefIds.length; s++) {
      var sid = hedefIds[s];
      var typTag = (classes[sid].type === 'KEMIK_TAHMIN' ? 'kemik?' : classes[sid].type.toLowerCase());
      var capturedUrls = (WADO_BY_SERIES[sid] || []).slice();
      var sShort = sid.split('.').slice(-3).join('_');
      var folder = (classes[sid].type === 'KEMIK' || classes[sid].type === 'KEMIK_TAHMIN') ? 'kemik_' : 'seri_';

      console.log('[PACS-DL] Seri', s + 1, 'icin yakalanan URL:', capturedUrls.length, 'OTO:', isOto);

      var useEnum = isOto || capturedUrls.length < 3;
      if (!useEnum) {
        btn.textContent = 'Seri ' + (s + 1) + '/' + hedefIds.length + ' (' + typTag + ') indiriliyor (' + capturedUrls.length + ' kesit)...';
        var dlBatch = 10;
        for (var b = 0; b < capturedUrls.length; b += dlBatch) {
          var promises = [];
          for (var bk = 0; bk < dlBatch && (b + bk) < capturedUrls.length; bk++) {
            var idx = b + bk;
            var u = capturedUrls[idx];
            promises.push(fetch(u).then(function (r) {
              return r.ok ? r.blob() : null;
            }).catch(function () { return null; }));
          }
          var blobs = await Promise.all(promises);
          for (var bi = 0; bi < blobs.length; bi++) {
            if (blobs[bi] && blobs[bi].size > 1000) {
              var n = b + bi + 1;
              var fname = folder + sShort + '/' + String(n).padStart(4, '0') + '.dcm';
              allFiles.push({ name: fname, blob: blobs[bi] });
            }
          }
          btn.textContent = 'Seri ' + (s + 1) + '/' + hedefIds.length + ' indiriliyor: ' + allFiles.length + ' kesit';
        }
      } else {
        console.log('[PACS-DL] Enumeration (TURBO/az URL)');
        btn.textContent = '⚡ Seri ' + (s + 1) + '/' + hedefIds.length + ' (' + typTag + ') numaralaniyor...';
        var slices = await discoverSeries(sid, SERIES_SAMPLE[sid], function (count, scanned) {
          btn.textContent = '⚡ Seri ' + (s + 1) + ': ' + count + ' kesit (' + scanned + ' tarandi)';
        });
        for (var i = 0; i < slices.length; i++) {
          var fname2 = folder + sShort + '/' + String(slices[i].n).padStart(4, '0') + '.dcm';
          allFiles.push({ name: fname2, blob: slices[i].blob });
        }
      }
    }
    var totalOk = allFiles.length;

    if (totalOk === 0) {
      btn.textContent = 'Hicbir kesit alinamadi!';
      btn.style.background = '#a00';
      btn.disabled = false;
      try {
        localStorage.setItem('OTO_DONE', JSON.stringify({
          ts: Date.now(), ok: false, hata: 'KESIT_YOK', kesit: 0
        }));
      } catch (_) {}
      return;
    }

    btn.textContent = 'ZIP yaziliyor (0/' + totalOk + ')...';
    console.log('[PACS-DL] Manuel STORE encoder basliyor. Dosya:', totalOk);
    var lastTick = Date.now();
    var blob;
    try {
      blob = await buildStoreZip(allFiles, function (done, total) {
        lastTick = Date.now();
        var pct = Math.round((done / total) * 100);
        btn.textContent = 'ZIP %' + pct + ' (' + done + '/' + total + ')';
        if (done % 25 === 0 || done === total) console.log('[PACS-DL] ZIP', done, '/', total);
      });
    } catch (e) {
      console.error('[PACS-DL] ZIP encoder hatasi:', e);
      btn.textContent = '✗ ZIP hatasi: ' + e.message;
      btn.style.background = '#a00';
      btn.disabled = false;
      try {
        localStorage.setItem('OTO_DONE', JSON.stringify({
          ts: Date.now(), ok: false, hata: 'ENCODER_HATASI', kesit: totalOk
        }));
      } catch (_) {}
      return;
    }
    console.log('[PACS-DL] ZIP tamam. Boyut:', blob.size, 'byte');
    var sizeMb = (blob.size / 1024 / 1024).toFixed(1);
    var fileName = fileBase + '.zip';
    var blobUrl = URL.createObjectURL(blob);

    // Orkestratore basari haberi (henuz indirme tamamlanmadi ama ZIP hazir)
    var oto = false;
    try {
      oto = localStorage.getItem('OTO_AUTO') === '1';
    } catch (_) {}

    btn.textContent = 'Diske yaziliyor (' + sizeMb + ' MB)...';
    btn.style.background = '#085';

    // GM_download: Tampermonkey'in kendi indirme motoru - sekme kapansa bile tamamlar.
    // Fallback: <a download> click yontemi (eski tarayicilar/yetki yoksa)
    var downloaded = false;
    var doneSignal = function (success, hata) {
      if (downloaded) return;
      downloaded = true;
      try {
        localStorage.setItem('OTO_DONE', JSON.stringify({
          ts: Date.now(),
          ok: success,
          kesit: totalOk,
          mb: parseFloat(sizeMb),
          patientId: pid,
          patientName: pname || '',
          studyUid: META.studyUid || '',
          file: fileName,
          hata: hata || ''
        }));
      } catch (_) {}
      if (success) {
        btn.textContent = '✅ ' + totalOk + ' kesit / ' + sizeMb + ' MB';
        btn.style.background = '#070';
      } else {
        btn.textContent = '⚠ Indirme: ' + (hata || 'hata');
        btn.style.background = '#a60';
      }
      setTimeout(function () { btn.disabled = false; }, 2000);
      // ZIP gercekten kaydedildikten SONRA sekmeyi kapat (orkestrator yeni hastayi acsin)
      if (oto && success) {
        setTimeout(function () {
          try { URL.revokeObjectURL(blobUrl); } catch (_) {}
          try { window.close(); } catch (_) {}
        }, 2000);
      }
    };

    // 1. ONCELIKLE: GM_download dene (sekme kapansa da indirir)
    if (typeof GM_download === 'function') {
      console.log('[PACS-DL] GM_download kullaniliyor (resilient)');
      try {
        GM_download({
          url: blobUrl,
          name: fileName,
          saveAs: false,
          onload: function () {
            console.log('[PACS-DL] GM_download tamam:', fileName);
            doneSignal(true);
          },
          onerror: function (e) {
            console.warn('[PACS-DL] GM_download hata, fallback deneniyor:', e);
            // Fallback: a.click yontemi
            fallbackDownload();
          },
          ontimeout: function () {
            console.warn('[PACS-DL] GM_download timeout, fallback');
            fallbackDownload();
          }
        });
        // GM_download eger 60sn icinde callback vermezse fallback'e gec
        setTimeout(function () { if (!downloaded) fallbackDownload(); }, 60000);
      } catch (e) {
        console.warn('[PACS-DL] GM_download exception:', e);
        fallbackDownload();
      }
    } else {
      console.log('[PACS-DL] GM_download yok, a.click yontemi');
      fallbackDownload();
    }

    function fallbackDownload() {
      if (downloaded) return;
      try {
        var a = document.createElement('a');
        a.href = blobUrl;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        // a.click ile inmenin tamamlandigini anlamanin kesin yolu yok.
        // Buyuk dosyalar icin uzun bekle: 100MB icin ~30sn yeter.
        // 1 MB icin 0.5 sn pay, min 8sn, max 60sn.
        var waitMs = Math.min(60000, Math.max(8000, Math.round(blob.size / 1024 / 1024 * 500) + 5000));
        console.log('[PACS-DL] Fallback indirme baslatildi, beklenecek ms:', waitMs);
        setTimeout(function () { doneSignal(true); }, waitMs);
      } catch (e) {
        console.error('[PACS-DL] Fallback indirme hatasi:', e);
        doneSignal(false, 'INDIRME_HATA');
      }
    }
  }

  // Orkestrator otomatik tetikleme: localStorage 'OTO_AUTO' === '1' ise viewer acildiktan sonra otomatik smartZip baslat
  function checkAutoTrigger() {
    try {
      var auto = localStorage.getItem('OTO_AUTO');
      if (auto !== '1') return;
      console.log('[PACS-DL] TURBO auto-trigger: 6sn sonra basliyor');
      rTimeout(function () {
        if (Object.keys(SERIES_SAMPLE).length === 0) {
          console.log('[PACS-DL] Seri henuz yok, 6sn daha bekleniyor');
          rTimeout(function () {
            if (Object.keys(SERIES_SAMPLE).length > 0) {
              smartZip();
            } else {
              console.warn('[PACS-DL] 12sn sonra hala seri yok — hata');
              localStorage.setItem('OTO_DONE', JSON.stringify({ ts: Date.now(), ok: false, hata: 'no_series_12sn' }));
            }
          }, 6000);
        } else {
          smartZip();
        }
      }, 6000);
    } catch (_) {}
  }

  function addUI() {
    if (document.getElementById('pacs-dl-panel')) return;
    var panel = document.createElement('div');
    panel.id = 'pacs-dl-panel';
    panel.style.cssText =
      'position:fixed;top:10px;right:10px;z-index:2147483647;' +
      'background:#001a33;color:#fff;padding:12px;border-radius:10px;' +
      'font:13px Consolas,monospace;box-shadow:0 6px 18px rgba(0,0,0,.6);' +
      'min-width:260px;border:2px solid #0af';
    panel.innerHTML =
      '<div style="font-weight:bold;color:#0af;margin-bottom:6px">📦 Akilli DICOM ZIP</div>' +
      '<div id="pacs-dl-status" style="font-size:11px;line-height:1.5;margin-bottom:8px">Bekleniyor...</div>' +
      '<button id="pacs-dl-btn" style="width:100%;padding:10px;background:#070;color:#fff;border:0;border-radius:5px;cursor:pointer;font-weight:bold;font-size:13px">📦 TUM KESITLERI ZIP\'LE</button>';
    document.body.appendChild(panel);
    document.getElementById('pacs-dl-btn').onclick = smartZip;
    setInterval(function () {
      var s = document.getElementById('pacs-dl-status');
      if (!s) return;
      s.innerHTML =
        'Yakalanan: <b style="color:#0f0">' + WADO.size + '</b> | ' +
        'Seri: <b>' + Object.keys(SERIES_SAMPLE).length + '</b><br>' +
        'Hasta: <b>' + (META.patientId || '?') + '</b>';
    }, 500);
  }

  function keepAliveAudio() {
    try {
      var ctx = new (window.AudioContext || window.webkitAudioContext)();
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      gain.gain.value = 0.001;
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
    } catch (_) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { keepAliveAudio(); addUI(); checkAutoTrigger(); });
  } else {
    keepAliveAudio();
    addUI();
    checkAutoTrigger();
  }
  console.log('[PACS-DL v2.7 TURBO] GM_download + Scroll-skip + KeepAlive yuklendi');
})();
