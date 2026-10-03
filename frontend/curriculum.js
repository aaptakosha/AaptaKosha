const years=[
 {year:1,label:"First Professional",note:"Foundation sciences, Sanskrit, Padartha and classical-text study",curriculum_id:"bams_ncism_1"},
 {year:2,label:"Second Professional",note:"Pharmacology, pathology, toxicology, preventive care and Samhita study",curriculum_id:"bams_ncism_2"},
 {year:3,label:"Third Professional",note:"Clinical, procedural, emergency and research-oriented learning",curriculum_id:"bams_ncism_3"}
];
const grid=document.querySelector("#yearGrid"),search=document.querySelector("#curriculumSearch");
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function render(q=""){
 grid.innerHTML=years.filter(y=>(y.label+" "+y.note).toLowerCase().includes(q.toLowerCase())).map(y=>
  `<a class="year-card year-link" href="./year${y.year}.html?curriculum_id=${encodeURIComponent(y.curriculum_id)}" aria-label="Open ${esc(y.label)}">
    <span class="year-number">0${y.year}</span><h2>${esc(y.label)}</h2><div class="year-note">${esc(y.note)}</div>
    <span class="year-open">Open ${esc(y.label)} →</span>
  </a>`).join("");
}
search?.addEventListener("input",e=>render(e.target.value.trim()));
render();