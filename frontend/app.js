const links=document.querySelectorAll('.nav-item,.bottom-nav a');
links.forEach(link=>link.addEventListener('click',()=>{links.forEach(x=>x.classList.remove('active'));link.classList.add('active')}));
const menu=document.querySelector('.mobile-menu'),sidebar=document.querySelector('.sidebar');
if(menu&&sidebar){menu.addEventListener('click',()=>{sidebar.style.display=sidebar.style.display==='flex'?'none':'flex';if(innerWidth<=820){sidebar.style.position='fixed';sidebar.style.inset='0 auto 0 0';sidebar.style.width='280px';sidebar.style.zIndex='20';sidebar.style.boxShadow='0 18px 50px rgba(20,60,45,.2)';sidebar.style.alignItems='stretch';sidebar.querySelectorAll('.brand span:last-child,.nav-item span,.sidebar-note').forEach(x=>x.style.display='');sidebar.querySelectorAll('.nav-item').forEach(x=>{x.style.width='';x.style.justifyContent=''})}})}
const search=document.querySelector('.search input');
search?.addEventListener('keydown',e=>{if(e.key==='Enter'&&search.value.trim())document.title=search.value.trim()+' — AaptaKosha'});
window.AaptaKoshaSessionReady?.then(session=>{
  document.querySelectorAll('[data-auth-state]').forEach(el=>{el.textContent=session.authenticated?'Signed in':'Sign in to sync'});
});
