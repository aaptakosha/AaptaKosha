/* Shared Clerk session bootstrap. Only the publishable key reaches the browser. */
(function(){
  function clerkDomain(key){try{const parts=key.split('_');return parts.length>=3?atob(parts[2]).slice(0,-1):'';}catch(_){return '';}}
  function localSignIn(){const redirect=encodeURIComponent(window.location.href);window.location.assign('/sign-in.html?redirect='+redirect);}
  async function loadClerk(key){
    if(!key)throw new Error('clerk_publishable_key_missing');
    if(window.Clerk)return window.Clerk;
    const domain=clerkDomain(key);if(!domain)throw new Error('invalid_clerk_publishable_key');
    await new Promise((resolve,reject)=>{const script=document.createElement('script');const timeout=setTimeout(()=>reject(new Error('clerk_ui_load_timeout')),8000);script.src='https://'+domain+'/npm/@clerk/ui@1/dist/ui.browser.js';script.async=true;script.crossOrigin='anonymous';script.onload=()=>{clearTimeout(timeout);resolve();};script.onerror=()=>{clearTimeout(timeout);reject(new Error('clerk_ui_load_failed'));};document.head.appendChild(script);});
    await new Promise((resolve,reject)=>{const script=document.createElement('script');const timeout=setTimeout(()=>reject(new Error('clerk_sdk_load_timeout')),8000);script.src='https://'+domain+'/npm/@clerk/clerk-js@6/dist/clerk.browser.js';script.async=true;script.crossOrigin='anonymous';script.onload=()=>{clearTimeout(timeout);resolve();};script.onerror=()=>{clearTimeout(timeout);reject(new Error('clerk_sdk_load_failed'));};document.head.appendChild(script);});
    if(!window.Clerk)throw new Error('clerk_sdk_unavailable');return window.Clerk;
  }
  async function bootstrap(){
    let authenticated=false,clerk=null,publishableKey='',error=null;
    try{
      const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),5000);let response;
      try{response=await fetch('/api/config',{headers:{Accept:'application/json'},signal:controller.signal});}finally{clearTimeout(timeout);}
      if(!response.ok)throw new Error('auth_config_unavailable');
      const config=await response.json();publishableKey=config.clerk_publishable_key||'';
      if(!publishableKey)throw new Error('clerk_publishable_key_missing');
      const Clerk=await loadClerk(publishableKey);clerk=new Clerk(publishableKey);
      await clerk.load({ui:{ClerkUI:window.__internal_ClerkUICtor},signInUrl:'/sign-in.html',signUpUrl:'/sign-in.html',signInFallbackRedirectUrl:window.location.href,signUpFallbackRedirectUrl:window.location.href,allowedRedirectOrigins:[window.location.origin]});
      authenticated=Boolean(clerk.isSignedIn&&clerk.session);
    }catch(e){authenticated=false;error=e?.message||'clerk_initialization_failed';}
    window.AaptaKoshaAuth={
      subjectId:clerk?.user?.id||null,getToken:()=>clerk?.session?clerk.session.getToken():null,
      openSignIn:async()=>{try{if(clerk&&typeof clerk.openSignIn==='function')return clerk.openSignIn({fallbackRedirectUrl:window.location.href,signUpFallbackRedirectUrl:window.location.href});}catch(_){}localSignIn();},
      openUserProfile:async()=>{try{if(clerk&&typeof clerk.openUserProfile==='function')return clerk.openUserProfile({});}catch(_){}if(clerk&&typeof clerk.redirectToUserProfile==='function')return clerk.redirectToUserProfile();}
    };
    document.documentElement.dataset.authenticated=authenticated?'true':'false';
    window.AaptaKoshaSession={authenticated,state:authenticated?'authenticated':'anonymous',clerk,error};
    return window.AaptaKoshaSession;
  }
  window.AaptaKoshaSessionReady=bootstrap();
})();