(() => {
  const api = window.AaptaKoshaAssessment;
  const key = "aaptakosha.assessment.session.result";
  let r = null;
  try { r = JSON.parse(localStorage.getItem(key) || "null"); } catch {}

  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));

  const optionText = (item, ids) => {
    const match = (item.options || []).find((option) => ids.includes(option.option_id));
    return match ? match.text : "";
  };

  const bindActions = () => { document.querySelector("#reviewAnswers")?.addEventListener("click",()=>document.querySelector(".review")?.scrollIntoView({behavior:"smooth"})); document.querySelector("#continueLearning")?.addEventListener("click",()=>location.href="./samhita-study.html?chapter=charaka.sutra.01"); };\n\n  const paint = async () => {
    if (!r) return;
    bindActions();
    const p = r.percent || 0;
    const assessmentId = r.assessment?.assessment_id || "";
    const isChapter1 = assessmentId === "charaka.sutra.01.ncism-revision";
    const chapterId = assessmentId.startsWith("charaka.sutra.02") ? "charaka.sutra.02" : (isChapter1 ? "charaka.sutra.01" : "");
    document.querySelector(".result-hero .eyebrow").textContent = "Completed · " + (r.assessment?.title || "Assessment");
    document.querySelector(".result-hero p").textContent = `आपने ${r.score} / ${r.maximum_score} अंक प्राप्त किए। गलत उत्तरों को देखकर अगली कोशिश से पहले focused revision करें।`;
    document.querySelector(".score-ring strong").textContent = p + "%";
    document.querySelector(".score-ring span").textContent = `${r.score} / ${r.maximum_score}`;
    document.querySelector(".score-ring").style.background = `conic-gradient(var(--forest) 0 ${p}%,#dfe9df ${p}% 100%)`;
    const retry=document.querySelector("#retryAssessment");
    if(retry){retry.onclick=()=>location.href="./assessment.html?assessment_id="+encodeURIComponent(assessmentId)+(chapterId?"&chapter="+encodeURIComponent(chapterId):"");}
    const continueButton=document.querySelector("#continueLearning");
    if(continueButton) continueButton.onclick=()=>location.href=chapterId?"./samhita-study.html?chapter="+encodeURIComponent(chapterId):"./practice.html";
    const host=document.querySelector(".review");
    const bad=(r.breakdown||[]).filter(item=>!item.is_correct);
    const weakHost=document.querySelector("#weakShlokaList");
    let canonical=null;
    if(chapterId){try{canonical=(await fetch("/api/content/samhita?content_id="+encodeURIComponent(chapterId),{credentials:"same-origin"}).then(x=>x.ok?x.json():null))?.data||null}catch{}}
    if(weakHost){
      const refs=[];
      bad.forEach(item=>(item.content_refs||[]).forEach(ref=>{
        const m=ref.match(/^(charaka\.sutra\.0[12])\.(\d{3})$/);
        if(m&&!refs.some(x=>x.verse===Number(m[2]))) refs.push({verse:Number(m[2]),ref});
      }));
      weakHost.innerHTML=refs.length
        ? refs.map(x=>`<a class="weak-card" href="./samhita-study.html?chapter=${x.ref.split(".").slice(0,3).join(".")}&verse=${x.verse}"><span class="weak-number">श्लोक ${x.verse}</span><span><strong>पुनः पढ़ें और revise करें</strong><small>Canonical content से linked</small></span><span>→</span></a>`).join("")
        : '<div class="weak-empty">इस attempt में कोई linked weak content नहीं मिला। अध्याय की revision फिर भी जारी रख सकते हैं।</div>';
    }
    host.querySelectorAll("article").forEach(x=>x.remove());
    bad.forEach((item,n)=>{
      const selected=optionText(item,item.selected_option_ids||[]),correct=optionText(item,item.correct_option_ids||[]);
      const selectedLabel=selected||(item.selected_option_ids||[]).join(", ")||"उत्तर नहीं दिया";
      const correctLabel=correct||(item.correct_option_ids||[]).join(", ")||"उपलब्ध नहीं";
      const ref=(item.content_refs||[]).find(x=>/^charaka\.sutra\.0[12]\.\d{3}$/.test(x));
      const verse=ref&&canonical?canonical.verses.find(v=>v.verse_id===ref):null;
      const revisionLink=verse?`<a class="filter" href="./samhita-study.html?chapter=${chapterId}&verse=${verse.verse_no}">श्लोक ${verse.verse_no} revise करें →</a>`:"";
      host.insertAdjacentHTML("beforeend",`<article><span class="q-number">Q${String(n+1).padStart(2,"0")}</span><div><strong>${escapeHtml(item.prompt||item.question_id)}</strong><p><b>Your answer:</b> ${escapeHtml(selectedLabel)}</p><p class="correct"><b>Correct:</b> ${escapeHtml(correctLabel)}</p>${verse?`<div class="rationale"><b>हिन्दी rationale:</b> ${escapeHtml(verse.explanation_hi||verse.translation_hi)}</div>`:""}${revisionLink}</div><span class="status">Review</span></article>`);
    });
  };

  (async () => {
    try {
      await window.AaptaKoshaSessionReady;
      const id = new URLSearchParams(location.search).get("attempt_id");
      const authenticated = window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated;
      if (id && (authenticated || !r)) {
        const live = await api.result(id);
        if (live) r = live;
      }
      if (r) localStorage.setItem(key, JSON.stringify(r));
      paint();
    } catch (error) {
      const state = document.querySelector("[data-ui-state]");
      if (state) window.AaptaKoshaUi?.status(state, error.message || "Unable to load assessment results.", "error");
    }
  })();
})();