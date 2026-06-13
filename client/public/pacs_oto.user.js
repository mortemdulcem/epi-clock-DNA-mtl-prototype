e bulundu ('+(n*1.5).toFixed(1)+'sn)','lime'); this._sonuc(fAd); return; }
      if(n>=20){ // 20*1500ms = 30sn timeout
        L(h.tc+' '+h.ad+' bulunamadi (30sn)','red');
        s.hata.push(h.tc+':notfound');s.i++;GM.set('STATE',s);
        setTimeout(function(){self._sonraki();},800); return;
      }
      setTimeout(function(){self._sonucBekle(n+1);},1500);
    },
    _sonuc:function(f){
      var s=GM.get('STATE');var h=HASTALAR[s.i];
      if(!f){f=null;document.querySelectorAll('tr').forEach(function(r){if((r.innerText||'').indexOf(h.tc)>=0)f=r;});}
      if(!f){L(h.tc+' bulunamadi','red');s.hata.push(h.tc+':notfound');s.i++;GM.set('STATE',s);var self=this;setTimeout(function(){self._sonraki();},800);return;}
      (f.querySelector('td')||f).click();
      var self=this;
      setTimeout(function(){
        var v=document.getElementById(IDS.view);
        if(!v){L('viewBtn yok','red');s.hata.push(h.tc+':noviewbtn');s.i++;GM.set('STATE',s);setTimeout(function(){self._sonraki();},800);return;}
        GM.del('DONE');GM.del('TELE');v.click();
        L('DICOM aciliyor (max 8dk)...','orange');
        self._bek(0);
      },1000);
    },
    _bek:function(n){
      var self=this;var d=GM.get('DONE');
      if(d){
        var s=GM.get('STATE');var h=HASTALAR[s.i];
        if(d.ok){L('OK '+(d.boyut/1024/1024).toFixed(1)+'MB '+(d.kesit||'?')+' kesit','lime');s.bitti.push(h.tc);}
        else{L('HATA '+d.hata,'red');s.hata.push(h.tc+':'+d.hata);}
        s.i++;GM.set('STATE',s);GM.del('DONE');GM.del('TELE');
        var dk=Math.round((Date.now()-s.t0)/60000);
        var ort=s.bitti.length>0?dk/s.bitti.length:0;
        var kalan=HASTALAR.length-s.i;
        console.log('  '+s.bitti.length+'/'+HASTALAR.length+' Hata:'+s.hata.length+' Sure:'+dk+'dk Kalan~'+Math.round(kalan*ort)+'dk');
        setTimeout(function(){self._sonraki();},1500);
        return;
      }
      if(n>240){L('8dk timeout','red');var s=GM.get('STATE');var h=HASTALAR[s.i];s.hata.push(h.tc+':timeout');s.i++;GM.set('STATE',s);GM.del('DONE');GM.del('TELE');setTimeout(function(){self._sonraki();},1000);return;}
      setTimeout(function(){self._bek(n+1);},2000);
    }
  };
  unsafeWindow.OTO=OTO;window.OTO=OTO;
  var s=GM.get('STATE');
  if(s&&s.aktif){L('Aktif - devam','orange');setTimeout(function(){OTO._sonraki();},2000);}
  else{L('v8 hazir. OTO.baslat() | OTO.yardim()','lime');}
})();
yalnı