(function(){
  function status(el,message,type){if(!el)return;el.textContent=message;el.dataset.state=type||"info";el.hidden=false}
  function busy(button,label){if(!button)return()=>{};const old=button.textContent;button.disabled=true;button.setAttribute("aria-busy","true");button.textContent=label;return()=>{button.disabled=false;button.removeAttribute("aria-busy");button.textContent=old}}
  function empty(container,message){if(!container)return;container.innerHTML="<p class=\\"ui-empty\\">"+message+"</p>"}
  window.AaptaKoshaUi={status,busy,empty};
})();
