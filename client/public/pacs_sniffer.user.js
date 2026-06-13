// ==UserScript==
// @name         PACS BESK API Sniffer
// @namespace    nurcan.tez
// @version      1.0
// @description  PACS MobileDicomViewer API isteklerini yakalar
// @match        http://pacs.besk.local/ImageServer/Pages/MobileDicomViewer/*
// @match        https://pacs.besk.local/ImageServer/Pages/MobileDicomViewer/*
// @match        http://pacs.besk.local/ImageServer/*
// @match        https://pacs.besk.local/ImageServer/*
// @run-at       document-start
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  var NET = [];
  window.__SNIFFER_NET = NET;

  function tag(s) {
    return '%c[SNIFFER] ' + s;
  }
  var STYLE = 'background:#003;color:#0f0;font-weight:bold;padding:2px 6px;border-radius:3px';

  console.log(tag('Yuklendi @ document-start - tum istekler yakalanacak'), STYLE);

  // FETCH hook
  var oF = window.fetch;
  window.fetch = function (u, opts) {
    var url = typeof u === 'string' ? u : (u && u.url) || '';
    var p = oF.apply(this, arguments);
    p.then(async function (r) {
      try {
        var ct = (r.headers.get('content-type') || '').toLowerCase();
        var len = r.headers.get('content-length');
        var entry = { method: 'fetch', url: url, status: r.status, type: ct, len: len };
        if (ct.indexOf('json') >= 0 || ct.indexOf('xml') >= 0 || ct.indexOf('text') >= 0 || ct.indexOf('html') >= 0) {
          try {
            entry.body = (await r.clone().text()).substring(0, 3000);
          } catch (_) {}
        }
        NET.push(entry);
      } catch (_) {}
    }).catch(function () {});
    return p;
  };

  // XHR hook
  var oOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) {
    this._sm = m;
    this._su = u;
    return oOpen.apply(this, arguments);
  };
  var oSend = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function (body) {
    var x = this;
    x.addEventListener('load', function () {
      try {
        var ct = (x.getResponseHeader('content-type') || '').toLowerCase();
        var len = x.getResponseHeader('content-length');
        var entry = {
          method: 'xhr-' + (x._sm || ''),
          url: x._su || '',
          status: x.status,
          type: ct,
          len: len,
        };
        if (ct.indexOf('json') >= 0 || ct.indexOf('xml') >= 0 || ct.indexOf('text') >= 0 || ct.indexOf('html') >= 0) {
          try {
            var t = '';
            if (x.responseType === '' || x.responseType === 'text') t = x.responseText || '';
            else if (x.responseType === 'json') t = JSON.stringify(x.response);
            entry.body = t.substring(0, 3000);
          } catch (_) {}
        }
        NET.push(entry);
      } catch (_) {}
    });
    return oSend.apply(this, arguments);
  };

  // Yardimci fonksiyonlar
  window.LIST = function () {
    console.log('%c=== TOPLAM ' + NET.length + ' ISTEK ===', 'background:#000;color:cyan;font-weight:bold;font-size:16px;padding:4px 8px');
    var groups = {};
    NET.forEach(function (r) {
      var key = r.url.replace(/[?#].*$/, '').replace(/\d+/g, '#');
      (groups[key] = groups[key] || []).push(r);
    });
    Object.keys(groups).forEach(function (k) {
      var arr = groups[k];
      console.log('%c[' + arr.length + 'x] ' + k, 'color:#0ff;font-weight:bold');
      console.log('   ornek:', arr[0].method, arr[0].status, arr[0].type, arr[0].url);
      if (arr[0].body) console.log('   body:', arr[0].body.substring(0, 500));
    });
  };

  window.LIST_FULL = function (filter) {
    var f = filter || '';
    var matches = NET.filter(function (r) {
      return r.url.indexOf(f) >= 0 || (r.type && r.type.indexOf(f) >= 0);
    });
    console.log('%c=== ' + matches.length + ' eslesen ===', 'color:cyan;font-weight:bold;font-size:14px');
    matches.forEach(function (r) {
      console.log('[' + r.status + '] ' + r.method + ' ' + r.url);
      if (r.body) console.log('   ↳', r.body);
    });
  };

  window.LIST_JSON = function () {
    var matches = NET.filter(function (r) {
      return r.type && (r.type.indexOf('json') >= 0 || r.type.indexOf('xml') >= 0);
    });
    console.log('%c=== ' + matches.length + ' JSON/XML cevap ===', 'color:lime;font-weight:bold;font-size:14px');
    matches.forEach(function (r) {
      console.log('[' + r.status + '] ' + r.url);
      console.log('   ↳', r.body);
    });
  };

  window.SNIFFER_DUMP = function () {
    var blob = new Blob([JSON.stringify(NET, null, 2)], { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'pacs_sniffer_dump_' + Date.now() + '.json';
    a.click();
    console.log(tag('Dump indirildi'), STYLE);
  };

  console.log('%cKomutlar: LIST()  LIST_JSON()  LIST_FULL("filtre")  SNIFFER_DUMP()', 'color:#ff0');
})();
