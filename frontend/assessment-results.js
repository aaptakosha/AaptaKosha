(() => {
  const api=window.AaptaKoshaAssessment,key="aaptakosha.assessment.session.result";let r=null;try{r=JSON.parse(localStorage.getItem(key)||"null")}catch{}
  const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const optionText=(item,ids)=>(item.options||[]).find(o=>ids.includes(o.option_id))?.text||"";
  const chapterFromAssessment=id=>{const m=/^charaka\.sutra\.(\d{2})(?:\.revision|\.ncism-revision)?$/.exec(id||"");return m?"charaka.sutra."+m[1]:""};
  const canonicalItems=c=>Array.isArray(c?.verses)?c.verses:(Array.isArray(c?.passages)?c.passages:[]);
  const itemId=i=>i?.verse_id||i?.passage_id||"";
  const itemLabel=i=>i?.verse_no??i?.passage_no??itemId(i);
  const paint=async()=>{
    if(!r)return;
    const assessmentId=r.assessment?.assessment_id||"",chapterId=chapterFromAssessment(assessmentId),p=r.percent||0;
    document.querySelector("#reviewAnswers")?.addEventListener("click",()=>document.querySelector(".review")?.scrollIntoView({behavior:"smooth"}));
    document.querySelector(".result-hero .eyebrow").textContent="Completed · "+(r.assessment?.title||"Assessment");
    document.querySelector(".result-hero p").textContent="आपने "+r.score+" / "+r.maximum_score+" अंक प्राप्त किए। गलत उत्तरों को देखकर अगली कोशिश से पहले focused revision करें।";
    document.querySelector(".score-ring strong").textContent=p+"%";document.querySelector(".score-ring span").textContent=r.score+" / "+r.maximum_score;
    document.querySelector(".score-ring").style.background="conic-gradient(var(--forest) 0 "+p+"%,#dfe9df "+p+"% 100%)";
    const retry=document.querySelector("#retryAssessment");if(retry)retry.onclick=()=>location.href="./assessment.html?assessment_id="+encodeURIComponent(assessmentId)+(chapterId?"&chapter="+encodeURIComponent(chapterId):"");
    const cont=document.querySelector("#continueLearning");if(cont)cont.onclick=()=>location.href=chapterId?"./samhita-study.html?chapter="+encodeURIComponent(chapterId):"./practice.html";
    const host=document.querySelector(".review"),bad=(r.breakdown||[]).filter(x=>!x.is_correct),weak=document.querySelector("#weakShlokaList");let canonical=null;
    if(chapterId){try{canonical=(await fetch("/api/content/samhita?content_id="+encodeURIComponent(chapterId),{credentials:"same-origin"}).then(x=>x.ok?x.json():null))?.data||null}catch{}}
    const items=canonicalItems(canonical),refs=[];
    bad.forEach(item=>(item.content_refs||[]).forEach(ref=>{const m=/^(charaka\.sutra\.\d{2})\.(.+)$/.exec(ref);if(m&&!refs.some(x=>x.ref===ref))refs.push({ref,chapterId:m[1]})}));
    if(weak)weak.innerHTML=refs.length?refs.map(x=>{const f=items.find(i=>itemId(i)===x.ref),label=f?itemLabel(f):x.ref.split(".").pop();return '<a class="weak-card" href="./samhita-study.html?chapter='+encodeURIComponent(x.chapterId)+(f&&f.verse_no?'&verse='+encodeURIComponent(f.verse_no):'')+'"><span class="weak-number">श्लोक/अंश '+esc(label)+'</span><span><strong>पुनः पढ़ें और revise करें</strong><small>Canonical content से linked</small></span><span>→</span></a>'}).join(""):'<div class="weak-empty">इस attempt में कोई linked weak content नहीं मिला। अध्याय की revision फिर भी जारी रख सकते हैं।</div>';
    if(!host)return;host.querySelectorAll("article").forEach(x=>x.remove());
    bad.forEach((item,n)=>{const selected=optionText(item,item.selected_option_ids||[]),correct=optionText(item,item.correct_option_ids||[]),ref=(item.content_refs||[]).find(x=>/^(charaka\.sutra\.\d{2})\./.test(x)),f=ref?items.find(x=>itemId(x)===ref):null;host.insertAdjacentHTML("beforeend",'<article><span class="q-number">Q'+String(n+1).padStart(2,"0")+'</span><div><strong>'+esc(item.prompt||item.question_id)+'</strong><p><b>Your answer:</b> '+esc(selected||(item.selected_option_ids||[]).join(", ")||"उत्तर नहीं दिया")+'</p><p class="correct"><b>Correct:</b> '+esc(correct||(item.correct_option_ids||[]).join(", ")||"उपलब्ध नहीं")+'</p>'+(f?'<div class="rationale"><b>हिन्दी rationale:</b> '+esc(f.explanation_hi||f.translation_hi)+'</div>':"")+(f&&chapterId?'<a class="filter" href="./samhita-study.html?chapter='+encodeURIComponent(chapterId)+(f.verse_no?'&verse='+encodeURIComponent(f.verse_no):'')+'">अंश '+esc(itemLabel(f))+' revise करें →</a>':"")+'</div><span class="status">Review</span></article>')});
  };
  (async()=>{try{await window.AaptaKoshaSessionReady;const id=new URLSearchParams(location.search).get("attempt_id"),auth=window.AaptaKoshaSession&&window.AaptaKoshaSession.authenticated;if(id&&(auth||!r)){const live=await api.result(id);if(live)r=live}if(r)localStorage.setItem(key,JSON.stringify(r));await paint()}catch(e){const state=document.querySelector("[data-ui-state]");if(state)window.AaptaKoshaUi?.status(state,e.message||"Unable to load assessment results.","error")}})();
})();