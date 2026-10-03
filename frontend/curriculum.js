const fallbackYears=[
  {year:1,label:"First Professional",note:"Foundation sciences, Sanskrit, Padartha and classical-text study",curriculum_id:"bams_ncism_1"},
  {year:2,label:"Second Professional",note:"Pharmacology, pathology, toxicology, preventive care and Samhita study",curriculum_id:"bams_ncism_2"},
  {year:3,label:"Third Professional",note:"Clinical, procedural, emergency and research-oriented learning",curriculum_id:"bams_ncism_3"}
];
const subjectNames={
  "AyUG-SN-AI":"Sanskrit evam Ayurved Itihas","AyUG-PV":"Padartha Vijnanam","AyUG-SA1":"Samhita Adhyayan-1","AyUG-RS":"Rachana Sharira","AyUG-KS":"Kriya Sharira",
  "AyUG-RB":"Rasashastra evam Bhaishajyakalpana","AyUG-AT":"Agada Tantra evam Vidhi Vaidyaka","AyUG-SA2":"Samhita Adhyayan-2","AyUG-DG":"Dravyaguna Vijnana","AyUG-RN":"Roga Nidan evam Vikriti Vijnana","AyUG-SW":"Swasthavritta evam Yoga",
  "AyUG-KC":"Kayachikitsa","AyUG-PK":"Panchakarma & Upakarma","AyUG-ST":"Shalya Tantra","AyUG-SL":"Shalakya Tantra","AyUG-PS":"Prasuti Tantra evam Stree Roga","AyUG-KB":"Kaumarabhritya","AyUG-SA3":"Samhita Adhyayan-3","AyUG-EM":"Atyaikachikitsa / Emergency Medicine","AyUG-RM":"Research Methodology and Medical Statistics"
};
const staticSubjects={
  1:[["AyUG-SN-AI","Sanskrit evam Ayurved Itihas"],["AyUG-PV","Padartha Vijnanam"],["AyUG-SA1","Samhita Adhyayan-1"],["AyUG-RS","Rachana Sharira"],["AyUG-KS","Kriya Sharira"]],
  2:[["AyUG-RB","Rasashastra evam Bhaishajyakalpana"],["AyUG-AT","Agada Tantra evam Vidhi Vaidyaka"],["AyUG-SA2","Samhita Adhyayan-2"],["AyUG-DG","Dravyaguna Vijnana"],["AyUG-RN","Roga Nidan evam Vikriti Vijnana"],["AyUG-SW","Swasthavritta evam Yoga"]],
  3:[["AyUG-KC","Kayachikitsa"],["AyUG-PK","Panchakarma & Upakarma"],["AyUG-ST","Shalya Tantra"],["AyUG-SL","Shalakya Tantra"],["AyUG-PS","Prasuti Tantra evam Stree Roga"],["AyUG-KB","Kaumarabhritya"],["AyUG-SA3","Samhita Adhyayan-3"],["AyUG-EM","Atyaikachikitsa / Emergency Medicine"],["AyUG-RM","Research Methodology and Medical Statistics"]]
};
const grid=document.querySelector("#yearGrid"),search=document.querySelector("#curriculumSearch");
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function subjectCard(subjectId,name,year,curriculumId){
  return `<div class="subject-row" data-subject="${esc(subjectId)}"><button class="subject-toggle" data-curriculum="${esc(curriculumId)}" data-subject="${esc(subjectId)}" aria-expanded="false"><span><b>${esc(name)}</b><small class="code">${esc(subjectId)}</small></span><span class="chevron">›</span></button><div class="hierarchy" hidden><div class="hierarchy-loading">Loading hierarchy…</div></div></div>`;
}
function render(years= fallbackYears,q=""){
 grid.innerHTML=years.map(y=>{
  const subjects=(y.subjects||staticSubjects[y.year]||[]).filter(s=>(s[0]+" "+s[1]).toLowerCase().includes(q.toLowerCase()));
  return `<article class="year-card"><h2>${esc(y.label)}</h2><div class="year-note">${esc(y.note)}</div>${subjects.map(s=>subjectCard(s[0],s[1],y.year,y.curriculum_id)).join("")}<span class="status"><i></i>NCISM structure navigation</span></article>`;
 }).join("");
}
async function loadSubjects(){
 try{
  const results=await Promise.all(fallbackYears.map(async y=>{
   const r=await fetch(`/api/catalog/${y.curriculum_id}?version=2021-22`);
   if(!r.ok) throw new Error("catalog unavailable");
   const body=await r.json(); const c=body.data;
   return {...y,subjects:(c.subjects||[]).map(s=>[s.subject_id,s.name||subjectNames[s.subject_id]||s.subject_id])};
  }));
  render(results);
 }catch(e){render(fallbackYears);}
}
async function fetchHierarchyNodes(curriculumId,subjectId,parentNodeId=null){
  const u=new URL("/api/curriculum/nodes",location.origin);
  u.searchParams.set("curriculum_id",curriculumId);
  u.searchParams.set("subject_id",subjectId);
  u.searchParams.set("version","2021-22");
  if(parentNodeId)u.searchParams.set("parent_node_id",parentNodeId);
  let r=await fetch(u);
  if(!r.ok){
    const fallback=new URL("/api/catalog.py",location.origin);
    fallback.searchParams.set("route","curriculum/nodes");
    for(const [key,value] of u.searchParams)fallback.searchParams.set(key,value);
    r=await fetch(fallback);
  }
  if(!r.ok)throw new Error("hierarchy unavailable");
  return (await r.json()).data?.nodes||[];
}
function nodeMarkup(node,curriculumId,subjectId){
  return `<div class="node node-${esc(node.node_type)}" data-node-id="${esc(node.node_id)}">
    <button class="node-toggle" data-node-id="${esc(node.node_id)}" data-curriculum="${esc(curriculumId)}" data-subject="${esc(subjectId)}" aria-expanded="false">
      <span>${esc(node.code||"")} </span><b>${esc(node.name)}</b><i class="node-chevron">›</i>
    </button>
    <div class="node-children" hidden></div>
  </div>`;
}
async function loadNode(button){
  const wrap=button.nextElementSibling;
  if(button.dataset.loaded==="true"){
    wrap.hidden=!wrap.hidden;
    button.setAttribute("aria-expanded",String(!wrap.hidden));
    return;
  }
  wrap.hidden=false;
  wrap.innerHTML="<div class='hierarchy-loading'>Loading subtopics…</div>";
  button.setAttribute("aria-expanded","true");
  try{
    const children=await fetchHierarchyNodes(button.dataset.curriculum,button.dataset.subject,button.dataset.nodeId);
    button.dataset.loaded="true";
    wrap.innerHTML=children.length
      ?children.map(node=>nodeMarkup(node,button.dataset.curriculum,button.dataset.subject)).join("")
      :"<div class='hierarchy-empty'>No subtopics under this item.</div>";
    if(!children.length)button.classList.add("node-leaf");
  }catch(e){
    wrap.innerHTML="<div class='hierarchy-empty'>Subtopics could not be loaded right now.</div>";
  }
}
async function loadHierarchy(button){
 const wrap=button.nextElementSibling;
 if(!wrap)return;
 if(!wrap.hidden){
  wrap.hidden=true;
  button.setAttribute("aria-expanded","false");
  return;
 }
 wrap.hidden=false;
 wrap.innerHTML="<div class='hierarchy-loading'>Loading topics…</div>";
 button.setAttribute("aria-expanded","true");
 try{
  const roots=await fetchHierarchyNodes(button.dataset.curriculum,button.dataset.subject);
  if(!roots.length){
   wrap.innerHTML="<div class='hierarchy-empty'>No NCISM topics have been published for this subject yet.</div>";
   return;
  }
  wrap.innerHTML=roots.map(node=>nodeMarkup(node,button.dataset.curriculum,button.dataset.subject)).join("");
 }catch(e){
  wrap.innerHTML="<div class='hierarchy-empty'>NCISM topic structure could not be loaded right now.</div>";
 }
}
grid.addEventListener("click",e=>{const node=e.target.closest(".node-toggle");if(node){loadNode(node);return;}const b=e.target.closest(".subject-toggle");if(!b)return;b.setAttribute("aria-expanded",b.getAttribute("aria-expanded")!=="true");loadHierarchy(b);});
search?.addEventListener("input",e=>{const q=e.target.value.trim().toLowerCase();[...document.querySelectorAll(".subject-row")].forEach(x=>{const text=x.textContent.toLowerCase();x.hidden=!!q&&!text.includes(q);});});
render();loadSubjects();