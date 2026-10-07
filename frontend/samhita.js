const sarangadharaChapters={purva:[1,2,3,4,5,6,7],madhyama:[1,2,3,4,5,6,7,8,9,10,11,12],uttara:[1,2,3,4,5,6,7,8,9,10,11,12,13]};
const sarangadharaChapterHref=(k,n)=>'./samhita-chapter.html?text=sharangadhara&section='+encodeURIComponent(k)+'&chapter='+String(n).padStart(2,'0');

// Seeded entries preserve the previously visible library even if the registry request is unavailable.
const texts=[
["Charaka Samhita","brihattrayi","samhita","1, 2, 3","aiapget","charaka"],
["Sushruta Samhita","brihattrayi","samhita","1, 2, 3","aiapget","sushruta"],
["Ashtanga Hridaya","brihattrayi","samhita","1, 2, 3","aiapget","ashtanga-hridaya"],
["Ashtanga Sangraha","other_major_classical","samhita","1","aiapget","ashtanga-sangraha"],
["Kashyapa Samhita","other_major_classical","samhita","3","aiapget","kashyapa"],
["Bhela Samhita","other_major_classical","samhita","1","","bhela"],
["Harita Samhita","other_major_classical","samhita","1","","harita"],
["Madhava Nidana","laghutrayi","samhita","2, 3","aiapget","madhava-nidana"],
["Sharangadhara Samhita","laghutrayi","samhita","2, 3","aiapget","sharangadhara"],
["Bhavaprakasha","laghutrayi","samhita","2, 3","aiapget","bhavaprakasha"],
["Chakradatta","later_compendia","compendium","2, 3","","chakradatta"],
["Yogaratnakara","later_compendia","compendium","2, 3","","yogaratnakara"],
["Bhaishajya Ratnavali","later_compendia","compendium","2, 3","","bhaishajya-ratnavali"],
["Gadanigraha","later_compendia","compendium","2, 3","","gadanigraha"],
["Vangasena Samhita","later_compendia","samhita","2, 3","","vangasena"],
["Bhavaprakasha Nighantu","nighantu","nighantu","2","","bhavaprakasha-nighantu"],
["Dhanvantari Nighantu","nighantu","nighantu","2","","dhanvantari-nighantu"],
["Raja Nighantu","nighantu","nighantu","2","","raja-nighantu"],
["Kaiyadeva Nighantu","nighantu","nighantu","2","","kaiyadeva-nighantu"],
["Madanapala Nighantu","nighantu","nighantu","2","","madanapala-nighantu"],
["Abhinavachintamani","other_major_classical","compendium","reference","","abhinava-chintamani"],
["Arka Prakasha","other_major_classical","formulary","reference","","arka-prakasha"],
["Arogya Kalpadruma","other_major_classical","compendium","reference","","arogya-kalpadruma"],
["Ayurbhishak","other_major_classical","chikitsa-compendium","reference","","ayurbhishak"]
];

const registryUrl='./content/samhita-registry.json';
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const slug=s=>String(s||'').toLowerCase().replace(/ā/g,'a').replace(/ī/g,'i').replace(/ū/g,'u').replace(/ṛ/g,'r').replace(/ṅ/g,'n').replace(/ñ/g,'n').replace(/ṭ/g,'t').replace(/ḍ/g,'d').replace(/ṇ/g,'n').replace(/ś/g,'s').replace(/ṣ/g,'s').replace(/ṃ/g,'m').replace(/ṁ/g,'m').replace(/ /g,'-').replace(/[^a-z0-9-]/g,'');

function registryBooksToTexts(payload){
  const out=[];
  const categories=payload?.library_sources?.categories||[];
  for(const category of categories){
    for(const book of (category.books||[])){
      const id=String(book.id||'').trim();
      if(!id) continue;
      out.push([
        book.name_en||book.name||id,
        category.id||'library',
        book.kind||'reference',
        'reference',
        '',
        id,
        book.name||'',
        book.status||'planned',
        category.label||'Classical references'
      ]);
    }
  }
  return out;
}

function mergeLibrary(seed, registryTexts){
  const byId=new Map();
  for(const t of seed) byId.set(t[5],t);
  for(const t of registryTexts){
    const id=t[5];
    if(byId.has(id)){
      const old=byId.get(id);
      byId.set(id,[old[0],old[1],old[2],old[3],old[4],old[5],t[6],t[7],t[8]]);
    } else byId.set(id,t);
  }
  return [...byId.values()];
}

function initSamhitaLibrary(){
  const grid=document.querySelector("#textGrid");
  if(!grid)return;
  const tabs=[...document.querySelectorAll("#tabs button")],search=document.querySelector("#textSearch");
  let filter="all", library=texts.slice();

  function render(){
    const q=(search?.value||'').toLowerCase().trim();
    const visible=library.filter(t=>{
      const hay=[t[0],t[6],t[8],t[2],t[7]].filter(Boolean).join(' ').toLowerCase();
      const yearMatch=filter==="year1"?(t[3]||'').includes("1"):filter==="year2"?(t[3]||'').includes("2"):filter==="year3"?(t[3]||'').includes("3"):true;
      return hay.includes(q)&&(filter==="all"||filter===t[1]||filter===t[4]||yearMatch);
    });
    grid.innerHTML=visible.map(t=>{
      const status=t[7]||'planned';
      const isReference=t[3]==='reference';
      const relevance=isReference?'Reference library':t[3];
      return '<a class="text-card" href="./samhita-detail.html?text='+encodeURIComponent(t[5])+'"><div><span class="pill">'+esc((t[1]||'library').replaceAll('_',' '))+'</span><span class="type"> · '+esc(t[2]||'reference')+'</span><h3>'+esc(t[0])+'</h3><p>'+(isReference?'Classical source: '+esc(t[8]||'Classical references'):'Professional relevance: '+esc(relevance))+'</p><span class="pill">'+esc(status)+'</span>'+(t[4]?'<span class="pill">AIAPGET</span>':'')+'</div><div class="card-arrow"><span>'+(status==='planned'?'Source entry / digitization status':'Open Sthana / section map')+'</span><span>→</span></div></a>';
    }).join("")||'<div class="empty">No texts match your search.</div>';
  }

  tabs.forEach(b=>b.addEventListener("click",()=>{tabs.forEach(x=>x.classList.remove("active"));b.classList.add("active");filter=b.dataset.filter;render();}));
  search?.addEventListener("input",render);
  render();

  fetch(registryUrl,{cache:"no-store"}).then(r=>r.ok?r.json():Promise.reject(new Error("registry unavailable"))).then(payload=>{
    library=mergeLibrary(texts,registryBooksToTexts(payload));
    render();
  }).catch(()=>{});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initSamhitaLibrary);else initSamhitaLibrary();