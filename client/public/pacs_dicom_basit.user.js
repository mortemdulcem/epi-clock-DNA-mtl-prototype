// ==UserScript==
// @name         PACS BESK Basit DICOM Indirici
// @namespace    nurcan.tez
// @version      1.0
// @description  PACS MobileDicomViewer - tum DICOM dosyalarini ayri ayri indirir (ZIP yok, CDN yok)
// @match        http://pacs.besk.local/ImageServer/Pages/MobileDicomViewer/*
// @match        https://pacs.besk.local/ImageServer/Pages/MobileDicomViewer/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  var WADO = new Set();
  var META = { studyUid: '', patientId: '', seriesCount: new Set() };

  function addWadoUrl(u) {
    if (typeof u !== 'string') return;
    if (u.indexOf('/wado/BESKPACS') < 0) return;
    if (u.indexOf('ContentType=application/dicom') < 0) return;
    if (WADO.has(u)) return;
    WADO.add(u);
    try {
      var qs = u.split('?')[1] || '';
      var p = {};
      qs.split('&').forEach(function (kv) {
        var i = kv.indexOf('=');
        if (i > 0) p[kv.substring(0, i)] = decodeURIComponent(kv.substring(i + 1));
      });
      if (p.studyUID) META.studyUid = p.studyUID;
      if (p.seriesUID) META.seriesCount.add(p.seriesUID);
    } catch (_) {}
  }

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
    return (s || 'unknown').replace(/[\\/:*?"<>|^]/g, '_').replace(/\s+/g, '_').substring(0, 40);
  }

  function delay(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  async function downloadAll() {
    var btn = document.getElementById('pacs-dl-btn');
    btn.disabled = true;
    btn.style.background = '#a60';
    var urls = Array.from(WADO);
    if (urls.length === 0) {
      btn.textContent = 'Hicbir DICOM yakalanmadi!';
      btn.style.background = '#a00';
      btn.disabled = false;
      return;
    }
    var pid = META.patientId || 'NN';
    var shortStudy = (META.studyUid || 'study').split('.').slice(-2).join('_');
    var ok = 0, fail = 0;
    for (var i = 0; i < urls.length; i++) {
      btn.textContent = 'Indiriliyor ' + (i + 1) + '/' + urls.length;
      try {
        var r = await fetch(urls[i]);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        var b = await r.blob();
        var pa = new URL(urls[i]);
        var oUID = pa.searchParams.get('objectUID') || ('obj_' + i);
        var oShort = oUID.split('.').slice(-2).join('_');
        var fname = safeName(pid) + '_' + shortStudy + '_' + String(i + 1).padStart(3, '0') + '_' + oShort + '.dcm';
        var a = document.createElement('a');
        a.href = URL.createObjectURL(b);
        a.download = fname;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(a.href);
        ok++;
        await delay(150);
      } catch (e) {
        fail++;
        console.warn('[DL] FAIL', urls[i], e);
      }
    }
    btn.textContent = '✅ ' + ok + ' OK / ' + fail + ' hata';
    btn.style.background = '#070';
    setTimeout(function () { btn.disabled = false; }, 2000);
  }

  function addUI() {
    if (document.getElementById('pacs-dl-panel')) return;
    var panel = document.createElement('div');
    panel.id = 'pacs-dl-panel';
    panel.style.cssText =
      'position:fixed;top:10px;right:10px;z-index:2147483647;' +
      'background:#001a33;color:#fff;padding:12px;border-radius:10px;' +
      'font:13px Consolas,monospace;box-shadow:0 6px 18px rgba(0,0,0,.6);' +
      'min-width:240px;border:2px solid #0af';
    panel.innerHTML =
      '<div style="font-weight:bold;color:#0af;margin-bottom:6px">📥 DICOM Indirici (Basit)</div>' +
      '<div id="pacs-dl-status" style="font-size:11px;line-height:1.5;margin-bottom:8px">Bekleniyor...</div>' +
      '<button id="pacs-dl-btn" style="width:100%;padding:10px;background:#070;color:#fff;border:0;border-radius:5px;cursor:pointer;font-weight:bold;font-size:13px">⬇ TUMUNU INDIR</button>';
    document.body.appendChild(panel);
    document.getElementById('pacs-dl-btn').onclick = downloadAll;
    setInterval(function () {
      var s = document.getElementById('pacs-dl-status');
      if (!s) return;
      s.innerHTML =
        'DICOM yakalandi: <b style="color:#0f0">' + WADO.size + '</b><br>' +
        'Seri: <b>' + META.seriesCount.size + '</b> | Hasta: <b>' + (META.patientId || '?') + '</b>';
    }, 500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addUI);
  } else {
    addUI();
  }
  console.log('[PACS-DL-BASIT] Yuklendi');
})();
