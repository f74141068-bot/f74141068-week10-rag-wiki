(() => {
 const slides = [...document.querySelectorAll('.slide')];
 const prev = document.getElementById('prev');
 const next = document.getElementById('next');
 const count = document.getElementById('counter');
 const bar = document.getElementById('bar');
 const progress = document.getElementById('progress');
 const notesBtn = document.getElementById('notesBtn');
 const outline = document.getElementById('outline');
 let current = Math.max(0, Math.min(slides.length-1, (parseInt(location.hash.replace('#slide-',''),10) || 1)-1));
 let notes = false;
 function show(index) {
   current=Math.max(0,Math.min(slides.length-1,index));
   slides.forEach((slide,i)=>{const on=i===current;slide.classList.toggle('active',on);slide.setAttribute('aria-hidden',String(!on));slide.querySelector('.deck-notes').classList.toggle('visible',on&&notes)});
   count.textContent=`${current+1} / ${slides.length}`;
   progress.setAttribute('aria-valuenow',String(current+1));
   bar.style.width=`${100*(current+1)/slides.length}%`;
   prev.disabled=current===0;next.disabled=current===slides.length-1;
   history.replaceState(null,'',`#slide-${current+1}`);
   window.scrollTo({top:0,behavior:'instant'});
 }
 prev.addEventListener('click',()=>show(current-1));
 next.addEventListener('click',()=>show(current+1));
 notesBtn.addEventListener('click',()=>{notes=!notes;notesBtn.setAttribute('aria-pressed',String(notes));show(current)});
 document.getElementById('outlineBtn').addEventListener('click',()=>outline.showModal());
 document.getElementById('closeDialog').addEventListener('click',()=>outline.close());
 outline.querySelectorAll('[data-jump]').forEach(btn=>btn.addEventListener('click',()=>{outline.close();show(Number(btn.dataset.jump)-1)}));
 document.addEventListener('keydown',(e)=>{
   if(outline.open) return;
   if(e.target instanceof HTMLElement && ['BUTTON','INPUT','TEXTAREA'].includes(e.target.tagName) && e.key!=='ArrowLeft' && e.key!=='ArrowRight')return;
   if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();show(current+1)}
   if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(current-1)}
   if(e.key==='Home'){e.preventDefault();show(0)}
   if(e.key==='End'){e.preventDefault();show(slides.length-1)}
 });
 document.querySelectorAll('.quiz-option').forEach(btn=>btn.addEventListener('click',()=>{
  document.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','incorrect'));
  const ok=btn.dataset.correct==='true';btn.classList.add(ok?'correct':'incorrect');
  document.querySelector('.quiz-result').textContent=ok?'答對了！B 需要持續查詢更新的外部公告，適合優先考慮 RAG。':'再想想：哪一個情境需要持續查詢「更新的外部資料」？';
 }));
 show(current);
})();
