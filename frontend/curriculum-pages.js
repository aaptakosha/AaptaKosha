const SUBJECT_FALLBACK={
1:[["AyUG-SN-AI","Sanskrit evam Ayurved Itihas"],["AyUG-PV","Padartha Vijnanam"],["AyUG-SA1","Samhita Adhyayan-1"],["AyUG-RS","Rachana Sharira"],["AyUG-KS","Kriya Sharira"]],
2:[["AyUG-RB","Rasashastra evam Bhaishajyakalpana"],["AyUG-AT","Agada Tantra evam Vidhi Vaidyaka"],["AyUG-SA2","Samhita Adhyayan-2"],["AyUG-DG","Dravyaguna Vijnana"],["AyUG-RN","Roga Nidan evam Vikriti Vijnana"],["AyUG-SW","Swasthavritta evam Yoga"]],
3:[["AyUG-KC","Kayachikitsa"],["AyUG-PK","Panchakarma & Upakarma"],["AyUG-ST","Shalya Tantra"],["AyUG-SL","Shalakya Tantra"],["AyUG-PS","Prasuti Tantra evam Stree Roga"],["AyUG-KB","Kaumarabhritya"],["AyUG-SA3","Samhita Adhyayan-3"],["AyUG-EM","Atyaikachikitsa / Emergency Medicine"],["AyUG-RM","Research Methodology and Medical Statistics"]]
};
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
function subjectUrl(year,id,name,cid){return './subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(id)+'&subject_name='+encodeURIComponent(name)}
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
 const body='<div class="page-list">'+chapters.map(n=>'<a class="content-card" href="./chapter.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(id)+'&subject_name='+encodeURIComponent(name)+'&node_id='+encodeURIComponent(n.node_id)+'&chapter_name='+encodeURIComponent(n.name)+'"><span class="card-code">'+esc(n.code||n.node_type||'Chapter')+'</span><div><h2>'+esc(n.name)+'</h2><p>Open chapter and its topics</p></div><b>→</b></a>').join('')+(chapters.length?'':'<div class="empty-state">No chapters have been published for this subject yet.</div>')+'</div>';
 page.innerHTML=shell(name,'Chapters and learning units for this subject.',[['Curriculum','./curriculum.html'],[YEARS[year]?.label,'./year'+year+'.html'],[name,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(id)+'&subject_name='+encodeURIComponent(name)]],body,'./year'+year+'.html');
}
function mdInline(s){return esc(s).replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>').replace(/\\*([^*]+)\\*/g,'<em>$1</em>').replace(/\`([^\`]+)\`/g,'<code>$1</code>')}
function mdHtml(md){
 const lines=String(md||'').replace(/\\r/g,'').split('\\n');let out='',code=false,buf=[];
 for(const line of lines){
  if(line.trim().startsWith('\\`\\`\\`')){if(code){out+='<pre><code>'+esc(buf.join('\\n'))+'</code></pre>';buf=[];code=false}else code=true;continue}
  if(code){buf.push(line);continue}
  if(/^### /.test(line))out+='<h3>'+mdInline(line.slice(4))+'</h3>';
  else if(/^## /.test(line))out+='<h2>'+mdInline(line.slice(3))+'</h2>';
  else if(/^# /.test(line))out+='<h1>'+mdInline(line.slice(2))+'</h1>';
  else if(/^> /.test(line))out+='<blockquote>'+mdInline(line.slice(2))+'</blockquote>';
  else if(/^[-*] /.test(line))out+='<li>'+mdInline(line.slice(2))+'</li>';
  else if(/^\\d+\\. /.test(line))out+='<li>'+mdInline(line.replace(/^\\d+\\. /,''))+'</li>';
  else if(line.trim()==='')out+='<br>';
  else out+='<p>'+mdInline(line)+'</p>';
 }
 if(code)out+='<pre><code>'+esc(buf.join('\\n'))+'</code></pre>';return out;
}
async function padarthaContent(nodeId){
 const r=await fetch('/api/content/padartha?node_id='+encodeURIComponent(nodeId));
 if(!r.ok)throw new Error('content unavailable');const b=await r.json();return b.data?.content||'';
}
async function renderChapter(){
 const year=Number(qs.get("year")),cid=qs.get("curriculum_id"),sid=qs.get("subject_id"),sname=qs.get("subject_name")||sid,nodeId=qs.get("node_id"),name=qs.get("chapter_name")||"Chapter";
 if(!year||!cid||!sid||!nodeId){location.href='./curriculum.html';return}
 document.title=name+' — AaptaKosha';let topics=[];try{topics=await apiNodes(cid,sid,nodeId)}catch{}
 let article='';
 if(sid==='AyUG-PV'){try{const md=await padarthaContent(nodeId);if(md)article='<article class="topic-panel chapter-content">'+mdHtml(md)+'</article>'}catch{}}
 const topicPanel='<div class="topic-panel"><div class="topic-panel-heading"><span class="eyebrow">Chapter topics</span><h2>'+esc(name)+'</h2></div><div class="topic-list">'+topics.map(n=>'<article class="topic-item"><span>'+esc(n.code||'')+'</span><div><h3>'+esc(n.name)+'</h3><p>'+esc(n.node_type||'Topic')+'</p></div></article>').join('')+(topics.length?'':'<div class="empty-state">No topics have been published under this chapter yet.</div>')+'</div></div>';
 const body=article+topicPanel;
 page.innerHTML=shell(name,'Study the topics contained in this chapter.',[['Curriculum','./curriculum.html'],[YEARS[year]?.label,'./year'+year+'.html'],[sname,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname)],[name,'./chapter.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname)+'&node_id='+encodeURIComponent(nodeId)+'&chapter_name='+encodeURIComponent(name)]],body,'./subject.html?year='+year+'&curriculum_id='+encodeURIComponent(cid)+'&subject_id='+encodeURIComponent(sid)+'&subject_name='+encodeURIComponent(sname));
}
const file=location.pathname.split('/').pop();if(file==='subject.html')renderSubject();else if(file==='chapter.html')renderChapter();else renderYear();
