const SUBJECT_FALLBACK={
1:[["AyUG-SN-AI","Sanskrit evam Ayurved Itihas"],["AyUG-PV","Padartha Vijnanam"],["AyUG-SA1","Samhita Adhyayan-1"],["AyUG-RS","Rachana Sharira"],["AyUG-KS","Kriya Sharira"]],
2:[["AyUG-RB","Rasashastra evam Bhaishajyakalpana"],["AyUG-AT","Agada Tantra evam Vidhi Vaidyaka"],["AyUG-SA2","Samhita Adhyayan-2"],["AyUG-DG","Dravyaguna Vijnana"],["AyUG-RN","Roga Nidan evam Vikriti Vijnana"],["AyUG-SW","Swasthavritta evam Yoga"]],
3:[["AyUG-KC","Kayachikitsa"],["AyUG-PK","Panchakarma & Upakarma"],["AyUG-ST","Shalya Tantra"],["AyUG-SL","Shalakya Tantra"],["AyUG-PS","Prasuti Tantra evam Stree Roga"],["AyUG-KB","Kaumarabhritya"],["AyUG-SA3","Samhita Adhyayan-3"],["AyUG-EM","Atyaikachikitsa / Emergency Medicine"],["AyUG-RM","Research Methodology and Medical Statistics"]]
};
const AH_CHAPTERS=[
["y1-sa1-2","AH.Su.1","Ayushkamiya Adhyaya"],
["y1-sa1-3","AH.Su.2","Dinacharya Adhyaya"],
["y1-sa1-4","AH.Su.3","Ritucharya Adhyaya"],
["y1-sa1-5","AH.Su.4","Roganutpadaniya Adhyaya"],
["y1-sa1-6","AH.Su.5","Dravadravya Vijnaniya Adhyaya"],
["y1-sa1-7","AH.Su.6","Annasvarupa Vijnaniya Adhyaya"],
["y1-sa1-8","AH.Su.7","Annaraksha Adhyaya"],
["y1-sa1-9","AH.Su.8","Matrashitiya Adhyaya"],
["y1-sa1-10","AH.Su.9","Dravyadi Vijnaniya Adhyaya"],
["y1-sa1-11","AH.Su.10","Rasabhediya Adhyaya"],
["y1-sa1-12","AH.Su.11","Doshadi Vijnaniya Adhyaya"],
["y1-sa1-13","AH.Su.12","Doshabhediya Adhyaya"],
["y1-sa1-14","AH.Su.13","Doshopakramaniya Adhyaya"],
["y1-sa1-15","AH.Su.14","Dvividhopakramaniya Adhyaya"],
["y1-sa1-16","AH.Su.15","Shodhanadigana Sangraha Adhyaya"]
];
const YEARS={
1:{label:"First Professional",note:"Foundation sciences, Sanskrit, Padartha and classical-text study",curriculum_id:"bams_ncism_1"},
2:{label:"Second Professional",note:"Pharmacology, pathology, toxicology, preventive care and Samhita study",curriculum_id:"bams_ncism_2"},
3:{label:"Third Professional",note:"Clinical, procedural, emergency and research-oriented learning",curriculum_id:"bams_ncism_3"}
};
const qs=new URLSearchParams(location.search),page=document.querySelector("#curriculumPage"),esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const yearFromPath=()=>Number((location.pathname.match(/year([123])\.html$/)||[])[1]||0);
function crumbs(items){return '<nav class="breadcrumbs" aria-label="Breadcrumb">'+items.map((x,i)=>i===items.length-1?'<span aria-current="page">'+esc(x[0])+'</span>':'<a href="'+esc(x[1])+'">'+esc(x[0])+'</a>').join('<b aria-hidden="true">›</b>')+'</nav>'}
function shell(title,subtitle,crumbItems,body,back){return '<section class="curriculum-page">'+crumbs(crumbItems)+'<a class="back-link" href="'+back+'">← Back</a><div class="page-heading"><span class="eyebrow">NCISM-aligned academic map</span><h1>'+esc(title)+' <span>🌿</span></h1><p>'+esc(subtitle)+'</p></div>'+body+'</section>'}
async function apiNodes(curriculumId,subjectId,parentNodeId){
 const u=new URL("/api/curriculum/nodes",location.origin);u.searchParams.set("curriculum_id",curriculumId);u.searchParams.set("subject_id",subjectId);u.searchParams.set("version","2021-22");if(parentNodeId)u.searchParams.set("parent_node_id",parentNodeId);
 let r=await fetch(u);if(!r.ok){const f=new URL("/api/catalog.py",location.origin);f.searchParams.set("route","curriculum/nodes");for(const [k,v] of u.searchParams)f.searchParams.set(k,v);r=await fetch(f)}
 if(!r.ok)throw new Error("hierarchy unavailable");return (await r.json()).data?.nodes||[];
}
async function subjects(year){
 const y=YEARS[year];try{const r=await fetch('/api/catalog/'+y.curriculum_id+'?version=2021-22');if(!r.ok)throw 0;const b=await r.json();return (b.data?.subjects||[]).map(s=>[s.subject_id,s.name||s.subject_id]);}catch{return SUBJECT_FALLBACK[year]||[]}
}
function samhitaContentId(subjectId,nodeCode){
 const map={"AH.Su.1":"ashtanga.hridaya.sutra.01","AH.Su.2":"ashtanga.hridaya.sutra.02","AH.Su.3":"ashtanga.hridaya.sutra.03","AH.Su.4":"ashtanga.hridaya.sutra.04","AH.Su.5":"ashtanga.hridaya.sutra.05","AH.Su.6":"ashtanga.hridaya.sutra.06","AH.Su.7":"ashtanga.hridaya.sutra.07","AH.Su.8":"ashtanga.hridaya.sutra.08","AH.Su.9":"ashtanga.hridaya.sutra.09","AH.Su.10":"ashtanga.hridaya.sutra.10","AH.Su.11":"ashtanga.hridaya.sutra.11","AH.Su.12":"ashtanga.hridaya.sutra.12","AH.Su.13":"ashtanga.hridaya.sutra.13","AH.Su.14":"ashtanga.hridaya.sutra.14","AH.Su.15":"ashtanga.hridaya.sutra.15"};
 return subjectId==="AyUG-SA1"?(map[nodeCode]||null):null;
}
async function fetchSamhitaContent(contentId){
 if(!contentId)return null;try{const r=await fetch("/api/content/samhita?content_id="+encodeURIComponent(contentId),{credentials:"same-origin"});if(!r.ok)return null;const d=await r.json();return d.data||null;}catch{return null}
}
function samhitaVerseItems(payload){
 if(!payload)return [];const raw=Array.isArray(payload.verses)?payload.verses:(Array.isArray(payload.passages)?payload.passages:[]);return raw.map((v,i)=>({id:v.verse_id||v.passage_id||("verse-"+(i+1)),no:v.verse_no??v.passage_no??(i+1),type:v.type||"verse",sanskrit:v.sanskrit_original||v.text||v.sanskrit||v.sanskrit_text||"",translation:v.translation_hi||v.hindi_translation||"",explanation:v.explanation_hi||v.hindi_explanation||""})).filter(v=>String(v.sanskrit).trim());
}
function renderSamhitaOriginalLayer(payload,contentId,name){
 const items=samhitaVerseItems(payload);if(!items.length)return "";const studyUrl="./samhita-study.html?chapter="+encodeURIComponent(contentId);return '<section class="topic-panel samhita-original-layer"><div class="topic-panel-heading"><span class="eyebrow">मूल संहिता पाठ</span><h2>श्लोक — '+esc(payload.title_hi||name)+'</h2><p>प्रमाणित संस्कृत मूलपाठ को अध्याय के साथ सीधे पढ़ें।</p><a class="chapter-study-link" href="'+studyUrl+'">पूर्ण Samhita Study खोलें →</a></div><div class="samhita-verse-list">'+items.map(v=>'<article class="samhita-verse-card"><div class="samhita-verse-no">'+esc(String(v.type).toLowerCase()==="prose"?"गद्य":"श्लोक")+" "+esc(v.no)+'</div><div class="samhita-verse-sanskrit">'+esc(v.sanskrit).replace(/\\n/g,"<br>")+"</div>"+(v.translation?'<div class="samhita-verse-translation"><strong>हिन्दी अर्थ</strong><p>'+esc(v.translation)+'</p></div>':"")+(v.explanation?'<div class="samhita-verse-translation"><strong>व्याख्या</strong><p>'+esc(v.explanation)+'</p></div>':"")+"</article>").join("")+"</div></section>";
}function subjectUrl(year,id,name,cid){return './subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(id)+'&subject_name='+encodeURIComponent(name)}
async function renderYear(){
 const year=yearFromPath(),y=YEARS[year];if(!y){location.href='./curriculum.html';return}
 document.title=y.label+' — AaptaKosha';let list=await subjects(year);
 const q=qs.get("q")||"";if(q)list=list.filter(s=>(s[0]+" "+s[1]).toLowerCase().includes(q.toLowerCase()));
 const body='<div class="page-list">'+list.map(s=>'<a class="content-card" href="'+subjectUrl(year,s[0],s[1],y.curriculum_id)+'"><span class="card-code">'+esc(s[0])+'</span><div><h2>'+esc(s[1])+'</h2><p>Open subject chapters and learning topics</p></div><b>→</b></a>').join('')+'</div>';
 page.innerHTML=shell(y.label,'Subjects in this professional year.',[['Curriculum','./curriculum.html'],[y.label,'./year'+year+'.html']],body,'./curriculum.html');
}
async function renderSubject(){
 const year=Number(qs.get("year")),cid=qs.get("curriculum_id")||YEARS[year]?.curriculum_id,id=qs.get("subject_id"),name=qs.get("subject_name")||id;
 if(!year||!cid||!id){location.href='./curriculum.html';return}
 document.title=name+' — AaptaKosha';let roots=[];try{roots=await apiNodes(cid,id)}catch{}
 let chapters=[];
 for(const n of roots){if(String(n.node_type).toLowerCase()==='chapter')chapters.push(n);else if(String(n.node_type).toLowerCase()==='paper'){try{chapters.push(...await apiNodes(cid,id,n.node_id))}catch{}}}
 if(!chapters.length)chapters=roots;
 if(!chapters.length && id==="AyUG-SA1"){
   chapters=AH_CHAPTERS.map(([node_id,code,name])=>({node_id,code,name,node_type:"chapter"}));
 }
 const body='<div class="page-list">'+chapters.map(n=>'<a class="content-card" href="./chapter.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(id)+'&subject_name='+encodeURIComponent(name)+'&node_id='+encodeURIComponent(n.node_id)+'&node_code='+encodeURIComponent(n.code||'')+'&chapter_name='+encodeURIComponent(n.name)+'"><span class="card-code">'+esc(n.code||n.node_type||'Chapter')+'</span><div><h2>'+esc(n.name)+'</h2><p>Open chapter and its topics</p></div><b>→</b></a>').join('')+(chapters.length?'':'<div class="empty-state">No chapters have been published for this subject yet.</div>')+'</div>';
 page.innerHTML=shell(name,'Chapters and learning units for this subject.',[['Curriculum','./curriculum.html'],[YEARS[year]?.label,'./year'+year+'.html'],[name,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(id)+'&subject_name='+encodeURIComponent(name)]],body,'./year'+year+'.html');
}
async function renderChapter(){
 const year=Number(qs.get("year")),cid=qs.get("curriculum_id"),sid=qs.get("subject_id"),sname=qs.get("subject_name")||sid,nodeId=qs.get("node_id"),name=qs.get("chapter_name")||"Chapter";
 if(!year||!cid||!sid||!nodeId){location.href='./curriculum.html';return}
 document.title=name+' — AaptaKosha';
 let topics=[];try{topics=await apiNodes(cid,sid,nodeId)}catch{}
 const nodeCode=qs.get("node_code")||"";
 let lesson=null;
 let samhitaPayload=null;
 const samhitaId=samhitaContentId(sid,nodeCode);
 if(samhitaId)samhitaPayload=await fetchSamhitaContent(samhitaId);
 if(nodeCode){
   try{
     const u=new URL("/api/curriculum/content",location.origin);
     u.searchParams.set("subject_id",sid);u.searchParams.set("node_code",nodeCode);
     const r=await fetch(u);if(r.ok)lesson=(await r.json()).data||null;
   }catch{}
 }
 const lessonHtml=lesson?'<div class="topic-panel lesson-content"><div class="topic-panel-heading"><span class="eyebrow">NCISM-aligned study content</span><h2>'+esc(lesson.chapter_title||name)+'</h2><p>'+esc(lesson.scope_note||'')+'</p></div><div class="topic-list">'+(lesson.learning_outcomes?.length?'<article class="topic-item"><span>LO</span><div><h3>Learning outcomes</h3><ul>'+lesson.learning_outcomes.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div></article>':'')+(lesson.sections||[]).map(sec=>'<article class="topic-item"><span>'+esc(sec.id?.split("-")[0]||'')+'</span><div><h3>'+esc(sec.title||'')+'</h3>'+(sec.content||[]).map(p=>'<p>'+esc(p)+'</p>').join('')+'</div></article>').join('')+(lesson.exam_focus?.length?'<article class="topic-item"><span>EX</span><div><h3>Exam focus</h3><ul>'+lesson.exam_focus.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div></article>':'')+'</div></div>':'';
 const topicsHtml='<div class="topic-panel"><div class="topic-panel-heading"><span class="eyebrow">Chapter topics</span><h2>'+esc(name)+'</h2></div><div class="topic-list">'+topics.map(n=>'<article class="topic-item"><span>'+esc(n.code||'')+'</span><div><h3>'+esc(n.name)+'</h3><p>'+esc(n.node_type||'Topic')+'</p></div></article>').join('')+(topics.length?'':'<div class="empty-state">No topics have been published under this chapter yet.</div>')+'</div></div>';
 const samhitaHtml=renderSamhitaOriginalLayer(samhitaPayload,samhitaId,name);
 const body=samhitaHtml+lessonHtml+topicsHtml;
 page.innerHTML=shell(name,samhitaPayload?'मूल श्लोक, हिन्दी अर्थ और अध्ययन सामग्री एक ही अध्याय पेज पर उपलब्ध हैं.':(lesson?'Read the NCISM-aligned lesson, then review the chapter topics.':'Study the topics contained in this chapter.'),[['Curriculum','./curriculum.html'],[YEARS[year]?.label,'./year'+year+'.html'],[sname,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname)],[name,'./chapter.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname)+'&node_id='+encodeURIComponent(nodeId)+'&chapter_name='+encodeURIComponent(name)]],body,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname));
}
const file=location.pathname.split('/').pop();if(file==='subject.html')renderSubject();else if(file==='chapter.html')renderChapter();else renderYear();
