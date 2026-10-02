(function(){
  const KEY="aaptakosha.guest.notes.v1", BOOK="aaptakosha.guest.bookmarks.v1";
  const read=k=>{try{return JSON.parse(localStorage.getItem(k)||"[]")}catch(_){return[]}};
  const write=(k,v)=>localStorage.setItem(k,JSON.stringify(v));
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const notes=read(KEY), bookmarks=read(BOOK);
  function render(){
    const q=(document.querySelector("[data-note-search]")?.value||"").trim().toLowerCase();
    const subject=document.querySelector("[data-subject-filter]")?.value||"All subjects";
    const list=document.querySelector("[data-notes-list]");
    const filtered=notes.filter(n=>(!q||[n.title,n.body,n.subject,...(n.tags||[])].join(" ").toLowerCase().includes(q))&&(subject==="All subjects"||n.subject===subject));
    if(list) list.innerHTML=filtered.length?filtered.map(n=>'<article class="note '+(n.pinned?"featured":"")+'"><div class="note-top"><span class="badge">'+(n.pinned?"Pinned":"Note")+'</span><button type="button" aria-label="Toggle bookmark" data-bookmark="'+escape(n.id)+'">'+(n.bookmarked?"★":"☆")+'</button></div><h3>'+escape(n.title)+'</h3><p>'+escape(n.body||"")+'</p><div class="note-meta"><span>'+escape(n.subject||"General")+'</span>'+(n.topic?'<span>•</span><span>Topic: '+escape(n.topic)+'</span>':"")+'</div><small>Saved locally</small></article>').join(""):'<div class="ui-empty">No saved notes yet. Create a note to start your personal library.</div>';
    const b=read(BOOK), bl=document.querySelector("[data-bookmarks-list]");
    if(bl) bl.innerHTML=b.length?b.map(x=>'<div class="bookmark"><span aria-hidden="true">☘</span><div><strong>'+escape(x.title)+'</strong><small>'+escape(x.subject||"Saved learning item")+'</small></div><b>→</b></div>').join(""):'<div class="ui-empty">No bookmarks yet.</div>';
    const set=(sel,v)=>{const e=document.querySelector(sel);if(e)e.textContent=v};
    set("[data-note-count]",notes.length);set("[data-bookmark-count]",b.length);set("[data-pinned-count]",notes.filter(n=>n.pinned).length);set("[data-subject-count]",new Set(notes.map(n=>n.subject).filter(Boolean)).size);
  }
  document.querySelector("[data-create-note]")?.addEventListener("click",()=>{const title=prompt("Note title");if(!title)return;const body=prompt("Note content")||"";notes.unshift({id:"guest-"+Date.now(),title,body,subject:"General",tags:[],pinned:false,bookmarked:false});write(KEY,notes);render();});
  document.addEventListener("click",e=>{const b=e.target.closest("[data-bookmark]");if(!b)return;const id=b.dataset.bookmark;const n=notes.find(x=>x.id===id);if(!n)return;n.bookmarked=!n.bookmarked;write(KEY,notes);const current=read(BOOK).filter(x=>x.id!==id);if(n.bookmarked)current.unshift({id,title:n.title,subject:n.subject});write(BOOK,current);render();});
  document.querySelector("[data-note-search]")?.addEventListener("input",render);document.querySelector("[data-subject-filter]")?.addEventListener("change",render);
  window.AaptaKoshaNotes={get:()=>read(KEY),save:n=>{const all=read(KEY);all.unshift(n);write(KEY,all);render();}};
  window.AaptaKoshaSessionReady?.then(session=>{if(session.authenticated){document.documentElement.dataset.notesSync="ready";}}).catch(()=>{});
  render();
})();