(function(){
  function mount(){
    const host=document.querySelector("[data-auth-slot]")||document.querySelector(".top-actions")||document.querySelector(".topbar")||document.querySelector(".learn-top")||document.querySelector(".practice-top")||document.querySelector(".assessment-main .top");
    if(!host||host.querySelector("[data-aapta-auth]"))return;
    const button=document.createElement("button");button.type="button";button.dataset.aaptaAuth="true";button.className="auth-trigger";button.setAttribute("aria-label","Sign in");button.textContent="Sign in";
    host.appendChild(button);
    window.AaptaKoshaSessionReady?.then(s=>{if(s.authenticated){button.textContent="Profile";button.setAttribute("aria-label","Open profile");button.onclick=()=>window.AaptaKoshaAuth?.openUserProfile?.();}else{button.textContent="Sign in";button.setAttribute("aria-label","Sign in");button.onclick=()=>window.AaptaKoshaAuth?.openSignIn?.();}}).catch(()=>{button.textContent="Sign in";});
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount);else mount();
})();