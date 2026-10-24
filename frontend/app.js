const links=document.querySelectorAll('.nav-item,.bottom-nav a');
const path=location.pathname.replace(/\/+$/, '') || '/';
links.forEach(link=>{const href=link.getAttribute('href')||'';const target=href.split('#')[0];if(target&&target!=='#'){const normalized=target.replace('./','/');if((path==='/'&&normalized==='/')||normalized===path||path.endsWith(normalized)){link.classList.add('active')}}link.addEventListener('click',()=>{if((link.getAttribute('href')||'').includes('#'))return;links.forEach(x=>x.classList.remove('active'));link.classList.add('active')})});
const menu=document.querySelector('.mobile-menu'),sidebar=document.querySelector('.sidebar');
if(menu&&sidebar){menu.addEventListener('click',()=>{sidebar.style.display=sidebar.style.display==='flex'?'none':'flex';if(innerWidth<=820){sidebar.style.position='fixed';sidebar.style.inset='0 auto 0 0';sidebar.style.width='280px';sidebar.style.zIndex='20';sidebar.style.boxShadow='0 18px 50px rgba(20,60,45,.2)';sidebar.style.alignItems='stretch';sidebar.querySelectorAll('.brand span:last-child,.nav-item span,.sidebar-note').forEach(x=>x.style.display='');sidebar.querySelectorAll('.nav-item').forEach(x=>{x.style.width='';x.style.justifyContent=''})}})}
const authButton=document.querySelector('#authButton');
const greeting=document.querySelector('#greeting');
function updateGreeting(){
  if(!greeting) return;
  const hour=new Date().getHours();
  greeting.textContent=hour<12?'Good morning':hour<17?'Good afternoon':'Good evening';
}
updateGreeting();
if(authButton){
  window.AaptaKoshaSessionReady?.then(session=>{
    const label=document.querySelector('#authButtonLabel');
    const sub=document.querySelector('#authButtonSub');
    if(session.authenticated){
      authButton.setAttribute('aria-label','Open profile');
      if(label) label.textContent='Student';
      if(sub) sub.textContent='BAMS learner';
      authButton.onclick=()=>window.AaptaKoshaAuth?.openUserProfile?.();
    }else{
      authButton.setAttribute('aria-label','Sign in');
      authButton.onclick=()=>window.AaptaKoshaAuth?.openSignIn?.();
    }
  });
}
const search=document.querySelector('.search input');
search?.addEventListener('keydown',e=>{if(e.key==='Enter'&&search.value.trim())document.title=search.value.trim()+' — AaptaKosha'});
window.AaptaKoshaSessionReady?.then(session=>{document.querySelectorAll('[data-auth-state]').forEach(el=>{el.textContent=session.authenticated?'Signed in':'Sign in to sync'})});


// AaptaKosha motion enhancements. No invented sales, reviews, or vanity metrics.
(function initAaptaKoshaMotion(){
  const reduceMotion=window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  const heroPromise=document.querySelector('.ak-hero h2 em');
  if(heroPromise&&!reduceMotion){
    const promises=['Understand it.','Study with clarity.','Remember with confidence.','Build strong foundations.'];
    let index=0;
    window.setInterval(()=>{
      if(document.hidden)return;
      heroPromise.classList.add('is-changing');
      window.setTimeout(()=>{
        index=(index+1)%promises.length;
        heroPromise.textContent=promises[index];
        heroPromise.classList.remove('is-changing');
      },180);
    },3400);
  }

  // Count up only real numeric values supplied by the existing app/API; placeholders stay untouched.
  const animateNumeric=(el)=>{
    if(el.dataset.akCounted==='true')return;
    const raw=(el.textContent||'').trim();
    const match=raw.match(/^([^0-9]*)(\d[\d,]*(?:\.\d+)?)(.*)$/);
    if(!match)return;
    const target=Number(match[2].replace(/,/g,''));
    if(!Number.isFinite(target)||target<=0||target>10000000)return;
    el.dataset.akCounted='true';
    const prefix=match[1],suffix=match[3],start=performance.now(),duration=650;
    const frame=(now)=>{
      const progress=Math.min(1,(now-start)/duration);
      const eased=1-Math.pow(1-progress,3);
      const value=target*eased;
      const formatted=Number.isInteger(target)?Math.round(value).toLocaleString():value.toFixed(1);
      el.textContent=prefix+formatted+suffix;
      if(progress<1)requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  };
  document.querySelectorAll('[data-streak],[data-weekly-goal],[data-streak-stat],[data-count-up]').forEach(animateNumeric);
  const observer=new MutationObserver(records=>records.forEach(record=>{
    if(record.target.nodeType===Node.ELEMENT_NODE)animateNumeric(record.target);
  }));
  document.querySelectorAll('[data-streak],[data-weekly-goal],[data-streak-stat],[data-count-up]').forEach(el=>observer.observe(el,{childList:true,characterData:true,subtree:true}));

  const storyItems=document.querySelector('.ak-story-items');
  if(storyItems){
    if(reduceMotion)storyItems.classList.add('is-drawn');
    else if('IntersectionObserver'in window){
      const storyObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
        if(entry.isIntersecting){entry.target.classList.add('is-drawn');storyObserver.unobserve(entry.target);}
      }),{threshold:.25});
      storyObserver.observe(storyItems);
    }else storyItems.classList.add('is-drawn');
  }

  // Lightweight click feedback on primary calls to action; navigation still proceeds normally.
  document.querySelectorAll('.ak-primary,.primary').forEach(button=>button.addEventListener('click',()=>{
    button.classList.remove('is-celebrating');
    void button.offsetWidth;
    button.classList.add('is-celebrating');
    window.setTimeout(()=>button.classList.remove('is-celebrating'),450);
    if(reduceMotion||!button.matches('.ak-primary'))return;
    const rect=button.getBoundingClientRect();
    const colors=['#b6924a','#54a978','#d4bd83','#8fb89a'];
    for(let i=0;i<9;i++){
      const piece=document.createElement('span');
      piece.className='ak-confetti-piece';
      piece.style.setProperty('--x',(rect.left+rect.width/2)+'px');
      piece.style.setProperty('--y',(rect.top+rect.height/2)+'px');
      piece.style.setProperty('--dx',(Math.cos(i*Math.PI*2/9)*42)+'px');
      piece.style.setProperty('--dy',(Math.sin(i*Math.PI*2/9)*34-14)+'px');
      piece.style.setProperty('--piece-color',colors[i%colors.length]);
      document.body.appendChild(piece);
      window.setTimeout(()=>piece.remove(),800);
    }
  }));
})();
