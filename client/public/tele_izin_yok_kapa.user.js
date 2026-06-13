// ==UserScript==
// @name         Teleradyoloji Izin Yok Otomatik Kapatici
// @namespace    nurcan
// @version      1.0
// @description  Hasta izin vermemis sayfasini hemen kapatir, ana otomasyon zaman kaybetmesin
// @match        https://teleradyoloji.saglik.gov.tr/*
// @match        http://teleradyoloji.saglik.gov.tr/*
// @grant        none
// @run-at       document-end
// ==/UserScript==

(function(){
  var KAPAT_SURE_MS = 1500;
  var KONTROL_ARALIK_MS = 800;
  var MAX_KONTROL = 30;
  var sayac = 0;

  function L(m){ try{ console.log('%c[IZIN-KAPA] '+m,'color:orange;font-weight:bold'); }catch(e){} }

  function kapat(sebep){
    L('TESPIT: '+sebep+' -> '+KAPAT_SURE_MS+'ms sonra kapatiliyor');
    try{ localStorage.setItem('SON_IZIN_YOK', new Date().toISOString()); }catch(e){}
    setTimeout(function(){
      try{ window.close(); }catch(e){}
      try{ window.open('','_self').close(); }catch(e){}
      try{ window.location.href='about:blank'; }catch(e){}
    }, KAPAT_SURE_MS);
  }

  function kontrol(){
    sayac++;
    var url = (location.href||'').toLowerCase();
    var bt = (document.body && document.body.innerText || '').toLowerCase();

    if (url.indexOf('otacerror') >= 0) { kapat('URL otacerror'); return true; }
    if (url.indexOf('errorcode') >= 0) { kapat('URL errorCode'); return true; }
    if (bt.indexOf('izin vermemi') >= 0) { kapat('text: izin vermemis'); return true; }
    if (bt.indexOf('görüntü paylaşımına') >= 0) { kapat('text: goruntu paylasim'); return true; }
    if (bt.indexOf('goruntu paylasimi') >= 0) { kapat('text: goruntu paylasim'); return true; }
    if (bt.indexOf('görüntülenememekte') >= 0) { kapat('text: goruntulenememekte'); return true; }
    if (bt.indexOf('goruntulenememekte') >= 0) { kapat('text: goruntulenememekte'); return true; }
    if (bt.indexOf('notauthorized') >= 0) { kapat('text: notauthorized'); return true; }
    if (bt.indexOf('yetkilendirme') >= 0 && bt.indexOf('hata') >= 0) { kapat('text: yetkilendirme hatasi'); return true; }

    if (sayac >= MAX_KONTROL) {
      L('30 kontrol bitti, viewer normal calistigi varsayiliyor');
      return true;
    }
    return false;
  }

  L('aktif - '+location.host+location.pathname);
  if (!kontrol()) {
    var iv = setInterval(function(){
      if (kontrol()) clearInterval(iv);
    }, KONTROL_ARALIK_MS);
  }
})();
