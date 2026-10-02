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
["Madanapala Nighantu","nighantu","nighantu","2","","madanapala-nighantu"]
];
const grid=document.querySelector("#textGrid"),tabs=document.querySelectorAll("#tabs button"),search=document.querySelector("#textSearch");let filter="all";
function render(){const q=(search?.value||"").toLowerCase().trim();const out=texts.filter(t=>{const matchText=t[0].toLowerCase().includes(q);const match=filter==="all"||filter===t[1]||filter===t[4]||(filter==="year1"&&t[3].includes("1"))||(filter==="year2"&&t[3].includes("2"))||(filter==="year3"&&t[3].includes("3"));return matchText&&match}).map(t=>'<a class="text-card" href="./samhita-detail.html?text='+encodeURIComponent(t[5])+'"><div><span class="pill">'+t[1].replaceAll("_"," ")+'</span><span class="type"> · '+t[2]+'</span><h3>'+t[0]+'</h3><p>Professional relevance: '+t[3]+'</p>'+(t[4]?'<span class="pill">AIAPGET</span>':"")+'</div><div class="card-arrow"><span>Open Sthana / section map</span><span>→</span></div></a>').join("");grid.innerHTML=out||'<div class="empty">No texts match your search.</div>'}
tabs.forEach(b=>b.addEventListener("click",()=>{tabs.forEach(x=>x.classList.remove("active"));b.classList.add("active");filter=b.dataset.filter;render()}));search?.addEventListener("input",render);render();