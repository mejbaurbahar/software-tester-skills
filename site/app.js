(function(){
  // copy buttons
  document.querySelectorAll('.copy').forEach(function(b){
    b.addEventListener('click',function(){
      var t=b.parentElement.querySelector('pre').innerText.trim();
      (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){
        b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1600);
      }).catch(function(){var r=document.createRange();r.selectNodeContents(b.parentElement.querySelector('pre'));var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Press Ctrl+C';});
    });
  });
  // install tabs
  var tabs=document.querySelectorAll('.tabs [role=tab]');
  function pick(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);
    document.getElementById(x.getAttribute('aria-controls')).hidden=!on;x.tabIndex=on?0:-1;});}
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){pick(t)});
    t.addEventListener('keydown',function(e){var n=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(!n)return;
      var x=tabs[(i+n+tabs.length)%tabs.length];x.focus();pick(x);});
  });
  // catalog search + category filter
  var q=document.getElementById('q'),chips=document.querySelectorAll('.chips button'),cats=document.querySelectorAll('.cat'),count=document.getElementById('count'),empty=document.getElementById('empty');
  if(!q)return;
  var cat='all';
  function run(){
    var term=q.value.trim().toLowerCase(),shown=0;
    cats.forEach(function(c){
      var any=false;
      c.querySelectorAll('li').forEach(function(li){
        var ok=(cat==='all'||c.dataset.cat===cat)&&(!term||li.dataset.s.indexOf(term)>-1);
        li.hidden=!ok;if(ok){any=true;shown++;}
      });
      c.hidden=!any;
    });
    count.textContent=shown+' skill'+(shown===1?'':'s');empty.hidden=shown!==0;
  }
  q.addEventListener('input',run);
  chips.forEach(function(b){b.addEventListener('click',function(){
    chips.forEach(function(x){x.setAttribute('aria-pressed',x===b)});cat=b.dataset.cat;run();});});
  document.addEventListener('keydown',function(e){if(e.key==='/'&&document.activeElement.tagName!=='INPUT'){e.preventDefault();q.focus();}});
  var h=location.hash.match(/^#q=(.+)$/);if(h){q.value=decodeURIComponent(h[1]);run();}
})();
