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
function samhitaContentId(subjectId,nodeCode,nodeId){
 if(subjectId!=="AyUG-SA1")return null;
 const byNode={
   "y1-sa1-2":"ashtanga.hridaya.sutra.01","y1-sa1-3":"ashtanga.hridaya.sutra.02","y1-sa1-4":"ashtanga.hridaya.sutra.03","y1-sa1-5":"ashtanga.hridaya.sutra.04","y1-sa1-6":"ashtanga.hridaya.sutra.05","y1-sa1-7":"ashtanga.hridaya.sutra.06","y1-sa1-8":"ashtanga.hridaya.sutra.07","y1-sa1-9":"ashtanga.hridaya.sutra.08","y1-sa1-10":"ashtanga.hridaya.sutra.09","y1-sa1-11":"ashtanga.hridaya.sutra.10","y1-sa1-12":"ashtanga.hridaya.sutra.11","y1-sa1-13":"ashtanga.hridaya.sutra.12","y1-sa1-14":"ashtanga.hridaya.sutra.13","y1-sa1-15":"ashtanga.hridaya.sutra.14","y1-sa1-16":"ashtanga.hridaya.sutra.15","y1-sa1-17":"charaka.sutra.01","y1-sa1-18":"charaka.sutra.02","y1-sa1-19":"charaka.sutra.03","y1-sa1-20":"charaka.sutra.04","y1-sa1-21":"charaka.sutra.05","y1-sa1-22":"charaka.sutra.06","y1-sa1-23":"charaka.sutra.07","y1-sa1-24":"charaka.sutra.08","y1-sa1-25":"charaka.sutra.09","y1-sa1-26":"charaka.sutra.10","y1-sa1-27":"charaka.sutra.11","y1-sa1-28":"charaka.sutra.12"
 };
 const byCode={"AH.Su.1":"ashtanga.hridaya.sutra.01","AH.Su.2":"ashtanga.hridaya.sutra.02","AH.Su.3":"ashtanga.hridaya.sutra.03","AH.Su.4":"ashtanga.hridaya.sutra.04","AH.Su.5":"ashtanga.hridaya.sutra.05","AH.Su.6":"ashtanga.hridaya.sutra.06","AH.Su.7":"ashtanga.hridaya.sutra.07","AH.Su.8":"ashtanga.hridaya.sutra.08","AH.Su.9":"ashtanga.hridaya.sutra.09","AH.Su.10":"ashtanga.hridaya.sutra.10","AH.Su.11":"ashtanga.hridaya.sutra.11","AH.Su.12":"ashtanga.hridaya.sutra.12","AH.Su.13":"ashtanga.hridaya.sutra.13","AH.Su.14":"ashtanga.hridaya.sutra.14","AH.Su.15":"ashtanga.hridaya.sutra.15","Ch.Su.1":"charaka.sutra.01","Ch.Su.2":"charaka.sutra.02","Ch.Su.3":"charaka.sutra.03","Ch.Su.4":"charaka.sutra.04","Ch.Su.5":"charaka.sutra.05","Ch.Su.6":"charaka.sutra.06","Ch.Su.7":"charaka.sutra.07","Ch.Su.8":"charaka.sutra.08","Ch.Su.9":"charaka.sutra.09","Ch.Su.10":"charaka.sutra.10","Ch.Su.11":"charaka.sutra.11","Ch.Su.12":"charaka.sutra.12"};
 return byNode[nodeId]||byCode[nodeCode]||null;
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
function renderMarkdown(md){
 const lines=String(md||"").replace(/\r/g,"").split("\n"),out=[];let inList=false,inTable=false;
 const inline=x=>esc(x).replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>").replace(/\*(.+?)\*/g,"<em>$1</em>").replace(/\`([^\`]+)\`/g,"<code>$1</code>").replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
 const closeList=()=>{if(inList){out.push("</ul>");inList=false}};
 for(let i=0;i<lines.length;i++){
  const line=lines[i],trim=line.trim();
  if(!trim){closeList();if(inTable){out.push("</tbody></table></div>");inTable=false}continue}
  if(/^\|.*\|$/.test(trim)){
   const cells=trim.replace(/^\||\|$/g,"").split("|").map(x=>x.trim());
   if(!inTable){out.push("<div class=\"markdown-table-wrap\"><table class=\"markdown-table\"><thead><tr>"+cells.map(c=>"<th>"+inline(c)+"</th>").join("")+"</tr></thead><tbody>");inTable=true;continue}
   if(cells.every(c=>/^:?-{3,}:?$/.test(c)))continue;
   out.push("<tr>"+cells.map(c=>"<td>"+inline(c)+"</td>").join("")+"</tr>");continue;
  }else if(inTable){out.push("</tbody></table></div>");inTable=false}
  const h=trim.match(/^(#{1,4})\s+(.*)$/);if(h){closeList();out.push("<h"+h[1].length+">"+inline(h[2])+"</h"+h[1].length+">");continue}
  const li=trim.match(/^[-*]\s+(.*)$/);if(li){if(!inList){out.push("<ul>");inList=true}out.push("<li>"+inline(li[1])+"</li>");continue}
  const ol=trim.match(/^\d+[.)]\s+(.*)$/);if(ol){closeList();out.push("<ol><li>"+inline(ol[1])+"</li></ol>");continue}
  if(/^>\s?/.test(trim)){closeList();out.push("<blockquote>"+inline(trim.replace(/^>\s?/,""))+"</blockquote>");continue}
  closeList();out.push("<p>"+inline(trim)+"</p>");
 }
 closeList();if(inTable)out.push("</tbody></table></div>");
 return out.join("");
}

function renderStructuredLesson(d,name){
 const esc2=esc;
 const tabs=[
  ["notes","Study Notes"],["map","Concept Map"],["mind","Mind Map"],["tables","Comparison Tables"],
  ["diagram","Diagram"],["mcq","MCQs"],["flash","Flashcards"],["exam","Exam Zone"],["recall","Active Recall"],["revision","Quick Revision"]
 ];
 const tabbar='<div class="study-tabs" role="tablist">'+tabs.map((t,i)=>'<button type="button" class="study-tab'+(i===0?' active':'')+'" data-study-tab="'+t[0]+'" role="tab">'+t[1]+'</button>').join('')+'</div>';
 const notes='<section class="study-section active" data-study-section="notes"><div class="study-callout"><strong>Study Note</strong><p>'+esc2(d.terminology_note||"")+'</p></div><div class="markdown-content">'+renderMarkdown(d.notes_markdown||"")+'</div></section>';
 const map=d.conceptMap||{};
 const mapHtml='<section class="study-section" data-study-section="map"><div class="concept-map"><div class="concept-center">'+esc2(map.center||"शरीर")+'</div><div class="concept-branches">'+(map.branches||[]).map(b=>'<div class="concept-branch"><h3>'+esc2(b.label)+'</h3>'+(b.items||[]).map(x=>'<span>'+esc2(x)+'</span>').join('')).join('')+'</div><div class="relation-strip">'+(map.relations||[]).map(x=>'<div>'+esc2(x)+'</div>').join('')+'</div></div></section>';
 const mind=d.mindMap||{};
 const mindHtml='<section class="study-section" data-study-section="mind"><div class="mindmap"><div class="mind-root">'+esc2(mind.root||"शरीर")+'</div><div class="mind-branches">'+(mind.nodes||[]).map(n=>'<div class="mind-branch"><h3>'+esc2(n.label)+'</h3>'+(n.children||[]).map(x=>'<span>'+esc2(x)+'</span>').join('')).join('')+'</div></div></section>';
 const tables='<section class="study-section" data-study-section="tables">'+(d.tables||[]).map(t=>'<div class="visual-table-card"><h3>'+esc2(t.title)+'</h3><div class="markdown-table-wrap"><table class="markdown-table"><thead><tr>'+t.headers.map(h=>'<th>'+esc2(h)+'</th>').join('')+'</tr></thead><tbody>'+t.rows.map(row=>'<tr>'+row.map(x=>'<td>'+esc2(x)+'</td>').join('')+'</tr>').join('')+'</tbody></table></div></div>').join('')+'</section>';
 const dg=d.diagram||{};
 const diagram='<section class="study-section" data-study-section="diagram"><div class="dosha-diagram"><h3>'+esc2(dg.title||"पञ्चमहाभूत → त्रिदोष")+'</h3>'+(dg.nodes||[]).map(n=>'<div class="flow-row"><div class="element-pair">'+n.from.map(x=>'<span>'+esc2(x)+'</span>').join('<b> + </b>')+'</div><div class="flow-arrow">→</div><div class="dosha-node">'+esc2(n.to)+'</div></div>').join('')+'</div></section>';
 const mcq='<section class="study-section" data-study-section="mcq"><div class="mcq-list">'+(d.mcqs||[]).map((m,i)=>'<article class="mcq-card"><div class="mcq-number">Question '+(i+1)+'</div><h3>'+esc2(m.q)+'</h3><div class="mcq-options">'+m.options.map((o,j)=>'<button type="button" class="mcq-option" data-correct="'+(j===m.answer)+'">'+String.fromCharCode(65+j)+'. '+esc2(o)+'</button>').join('')+'</div><button type="button" class="reveal-answer">View Answer</button><div class="mcq-answer" hidden><strong>Correct Answer:</strong> '+String.fromCharCode(65+m.answer)+'. '+esc2(m.options[m.answer])+'<p>'+esc2(m.explanation||"")+'</p></div></article>').join('')+'</div></section>';
 const flash='<section class="study-section" data-study-section="flash"><div class="flash-grid">'+(d.flashcards||[]).map((f,i)=>'<button type="button" class="flashcard" aria-expanded="false"><span class="flash-q">'+esc2(f.q)+'</span><span class="flash-a">'+esc2(f.a)+'</span><small>स्पर्श करें — View Answer</small></button>').join('')+'</div></section>';
 const ex=d.exam_zone||{};
 const exam='<section class="study-section" data-study-section="exam"><div class="exam-grid"><div><h3>Long Answer Questions</h3><ol>'+ex.laq.map(x=>'<li>'+esc2(x)+'</li>').join('')+'</ol></div><div><h3>Short Answer Questions</h3><ol>'+ex.saq.map(x=>'<li>'+esc2(x)+'</li>').join('')+'</ol></div><div><h3>Viva Questions</h3><ol>'+ex.viva.map(x=>'<li>'+esc2(x)+'</li>').join('')+'</ol></div></div></section>';
 const recall='<section class="study-section" data-study-section="recall"><div class="recall-list">'+(d.active_recall||[]).map((x,i)=>'<div><span>'+String(i+1).padStart(2,"0")+'</span><p>'+esc2(x)+'</p></div>').join('')+'</div></section>';
 const revision='<section class="study-section" data-study-section="revision"><div class="revision-grid">'+(d.quick_revision||[]).map(x=>'<div><strong>'+esc2(x[0])+'</strong><span>'+esc2(x[1])+'</span></div>').join('')+'</div></section>';
 return '<div class="structured-lesson"><div class="structured-heading"><span class="eyebrow">प्रकाशित अध्ययन-सामग्री</span><h2>'+esc2(d.chapter_title||name)+'</h2><p>'+esc2(d.chapter_subtitle||"")+'</p></div>'+tabbar+notes+mapHtml+mindHtml+tables+diagram+mcq+flash+exam+recall+revision+'</div>';
}
function bindStructuredLesson(){
 document.querySelectorAll(".study-tab").forEach(btn=>btn.addEventListener("click",()=>{const key=btn.dataset.studyTab;document.querySelectorAll(".study-tab").forEach(x=>x.classList.toggle("active",x===btn));document.querySelectorAll(".study-section").forEach(x=>x.classList.toggle("active",x.dataset.studySection===key));}));
 document.querySelectorAll(".reveal-answer").forEach(btn=>btn.addEventListener("click",()=>{const box=btn.parentElement.querySelector(".mcq-answer");box.hidden=!box.hidden;btn.textContent=box.hidden?"View Answer":"Hide Answer";}));
 document.querySelectorAll(".mcq-option").forEach(btn=>btn.addEventListener("click",()=>{const card=btn.closest(".mcq-card");card.querySelectorAll(".mcq-option").forEach(x=>x.classList.remove("selected"));btn.classList.add("selected");}));
 document.querySelectorAll(".flashcard").forEach(card=>card.addEventListener("click",()=>{const open=card.getAttribute("aria-expanded")==="true";card.setAttribute("aria-expanded",String(!open));}));
}
async function renderChapter(){
 const year=Number(qs.get("year")),cid=qs.get("curriculum_id"),sid=qs.get("subject_id"),sname=qs.get("subject_name")||sid,nodeId=qs.get("node_id"),name=qs.get("chapter_name")||"Chapter";
 if(!year||!cid||!sid||!nodeId){location.href='./curriculum.html';return}
 document.title=name+' — AaptaKosha';
 let topics=[];try{topics=await apiNodes(cid,sid,nodeId)}catch{}
 const nodeCode=qs.get("node_code")||"1";
 let lesson=null;
 let samhitaPayload=null;
 const samhitaId=samhitaContentId(sid,nodeCode,nodeId);
 if(samhitaId)samhitaPayload=await fetchSamhitaContent(samhitaId);
 if(nodeCode){
   try{
     const u=new URL("/api/curriculum/content",location.origin);
     u.searchParams.set("subject_id",sid);u.searchParams.set("node_code",nodeCode);u.searchParams.set("node_id",nodeId);
     const r=await fetch(u);if(r.ok)lesson=(await r.json()).data||null;
   }catch{}
 }
 const lessonHtml=lesson?(lesson.content_type==="structured"
   ?renderStructuredLesson(lesson.content||{},name)
   :'<div class="topic-panel lesson-content"><div class="topic-panel-heading"><span class="eyebrow">Published study content</span><h2>'+esc(name)+'</h2><p>यह अध्याय repository में प्रकाशित अध्ययन सामग्री से सीधे लोड किया गया है।</p></div><div class="markdown-content">'+renderMarkdown(lesson.content||"")+'</div></div>'):'';
 const topicsHtml='<div class="topic-panel"><div class="topic-panel-heading"><span class="eyebrow">Chapter topics</span><h2>'+esc(name)+'</h2></div><div class="topic-list">'+topics.map(n=>'<article class="topic-item"><span>'+esc(n.code||'')+'</span><div><h3>'+esc(n.name)+'</h3><p>'+esc(n.node_type||'Topic')+'</p></div></article>').join('')+(topics.length?'':'<div class="empty-state">No topics have been published under this chapter yet.</div>')+'</div></div>';
 const samhitaHtml=renderSamhitaOriginalLayer(samhitaPayload,samhitaId,name);
 const body=samhitaHtml+lessonHtml+topicsHtml;
 page.innerHTML=shell(name,samhitaPayload?'मूल श्लोक, हिन्दी अर्थ और अध्ययन सामग्री एक ही अध्याय पेज पर उपलब्ध हैं.':(lesson?'Read the NCISM-aligned lesson, then review the chapter topics.':'Study the topics contained in this chapter.'),[['Curriculum','./curriculum.html'],[YEARS[year]?.label,'./year'+year+'.html'],[sname,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname)],[name,'./chapter.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname)+'&node_id='+encodeURIComponent(nodeId)+'&chapter_name='+encodeURIComponent(name)]],body,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname));
 bindStructuredLesson();
}
const file=location.pathname.split('/').pop();if(file==='subject.html')renderSubject();else if(file==='chapter.html')renderChapter();else renderYear();
 bindStructuredLesson();
