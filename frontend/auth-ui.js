(function(){
  function isHome(){const p=window.location.pathname.replace(/\/+$/,'')||'/';return p==='/'||p==='/index.html';}
  function mount(){
    // The homepage owns its profile/sign-in control; every other page gets the shared control.
    if(isHome()) return;
    const host=document.querySelector('[data-auth-slot]')||document.querySelector('.top-actions')||document.querySelector('.topbar')||document.querySelector('.learn-top')||document.querySelector('.practice-top')||document.querySelector('.assessment-main .top');
    if(!host||host.querySelector('[data-aapta-auth]'))return;
    const button=document.createElement('button');
    button.type='button';button.dataset.aaptaAuth='true';button.className='auth-trigger';button.setAttribute('aria-label','Sign in');button.textContent='Sign in';
    host.appendChild(button);
    const hide=()=>{button.remove();};
    const showSignIn=()=>{button.textContent='Sign in';button.setAttribute('aria-label','Sign in');button.onclick=()=>window.AaptaKoshaAuth?.openSignIn?.();};
    window.AaptaKoshaSessionReady?.then(session=>{
      if(session?.authenticated) hide(); else showSignIn();
    }).catch(showSignIn);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
