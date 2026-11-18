import json, re, sys, importlib
sys.path.insert(0,'/home/claude')
import data as E, data_seoul as S, data_seongnam as SN
src=open('/home/claude/build.py',encoding='utf-8').read()
tpl=src[src.index('html = r"""')+len('html = r"""'):src.index('"""',src.index('html = r"""')+12)]
lines=tpl.split('\n')

def rep(a,b,cnt=1):
    global tpl
    assert tpl.count(a)>=1,a[:80]
    tpl=tpl.replace(a,b) if cnt==0 else tpl.replace(a,b,cnt)

base_note=re.search(r"note\.textContent='([^']*)'",tpl).group(1)
eland_note=base_note
seoul_note=base_note.replace("2020년 U12, 코로나 등으로 기록이 없는 연도는 표시되지 않습니다.","기록이 없는 연도(예: U12 2020년)는 표시되지 않습니다. U14는 2020~2025년 서울오산중 U14(팀 7580)와 2026년 FC서울 U14(팀 7381) 기록을 이어 붙였고, U15는 FC서울 U15(오산중, 팀 3166) 기록입니다. U12의 “2팀 추정” 리그는 같은 팀 ID로 두 권역에 동시 출전한 기록으로, 연도 합계에 함께 들어 있습니다.")
assert seoul_note!=base_note

sn_note=base_note.replace("2020년 U12, 코로나 등으로 기록이 없는 연도는 표시되지 않습니다.","기록이 없는 연도(예: U12 2020년)는 표시되지 않습니다. U14·U15는 성남FC U15, U17·U18은 풍생고 기록입니다.")
assert sn_note!=base_note
CLUBS={
 "eland":{"name":"서울이랜드FC","short":"이랜드","asof":"2026-11-14","c1":"#14254a","c2":"#24407a","grad":"linear-gradient(140deg,#0f1d3d 0%,#1c3266 60%,#2b4583 100%)",
   "feeder":"U15 · U18: 서울이랜드FC U15·U18","D":E.D,"sheets":[list(x) for x in E.SHEETS],"note":eland_note},
 "fcseoul":{"name":"FC서울","short":"FC서울","asof":"2026-11-16","c1":"#1a1a1a","c2":"#b5121b","grad":"linear-gradient(140deg,#0d0d0d 0%,#3a0a0e 55%,#8f1018 100%)",
   "feeder":"U14 · U15: 오산중 / U17 · U18: 오산고","D":S.D,"sheets":[list(x) for x in S.SHEETS],"note":seoul_note},
 "seongnam":{"name":"성남FC","short":"성남","asof":"2026-11-18","c1":"#121417","c2":"#3b4652","grad":"linear-gradient(140deg,#0b0c0e 0%,#1f252c 55%,#3b4652 100%)",
   "feeder":"U17 · U18: 풍생고","D":SN.D,"sheets":[list(x) for x in SN.SHEETS],"note":sn_note},
}

# --- header & CSS
rep("<title>서울이랜드FC 유스 연도별 성적 (팀별)</title>","<title>K리그 유스 성적 대시보드</title>")
rep(" <h1>서울이랜드FC 유스 연도별 성적</h1>\n <p>U11 · U12 · U14 · U15 · U17 · U18 | 출처: 넥스트플레이어(nextplayer.co.kr) 클럽 페이지 | 2026-11-14 기준</p>",
    ' <div class="hrow"><button id="back" class="back">← 전체 구단</button><h1 id="ttl">K리그 유스 성적 대시보드</h1></div>\n <p id="sub">출처: 넥스트플레이어(nextplayer.co.kr) 클럽 페이지</p>')
rep("</style></head>", r"""
.hrow{display:flex;align-items:center;gap:12px}
.back{display:none;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);color:#fff;border-radius:8px;padding:6px 12px;font:600 13px inherit;cursor:pointer;font-family:inherit}
body.detail .back{display:inline-block}
body:not(.detail) nav{display:none}
body:not(.detail) header{padding-bottom:14px}
body[data-club] .y26{background:var(--grad)}
#hub{display:none}body:not(.detail) #hub{display:block}body:not(.detail) #main{display:none}
.hub-intro{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin:4px 0 14px}
.hub-intro h2{margin:0;font-size:22px;color:#14254a}.hub-intro span{color:var(--mute);font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:16px;margin-bottom:18px}
.club{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;cursor:pointer;transition:transform .12s,box-shadow .12s;display:flex;flex-direction:column}
.club:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(0,0,0,.12)}
.club:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.chead{color:#fff;padding:14px 16px;display:flex;align-items:center;gap:12px}
.crest{width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.15);border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:13px;flex:none}
.chead h3{margin:0;font-size:20px}.chead small{display:block;color:rgba(255,255,255,.75);font-size:12px;margin-top:2px}
.chead .go{margin-left:auto;background:var(--gold);color:#0f1d3d;font-weight:800;font-size:13px;padding:6px 12px;border-radius:999px;white-space:nowrap}
.cstats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:12px 16px 4px}
.cstats div{background:#f6f7fa;border-radius:10px;padding:8px 10px}
.cstats b{display:block;font-size:18px;white-space:nowrap;font-weight:800;color:#1b1f2a}.cstats b.y{color:#b07d10}
.cstats i{font-style:normal;font-size:11px;color:var(--mute)}
.ages{padding:6px 16px 4px}
.age{display:grid;grid-template-columns:56px 104px 1fr 44px;gap:8px;align-items:center;padding:6px 0;border-bottom:1px dashed var(--line);font-size:13px}
.age:last-child{border-bottom:0}
.age .an{font-weight:800;color:#1b1f2a}.age .an small{display:block;font-weight:500;color:var(--mute);font-size:10.5px}
.age .wdl{font-variant-numeric:tabular-nums;color:#3a4152}
.age .wr{font-weight:800;text-align:right;font-variant-numeric:tabular-nums}
.mbar{height:8px;border-radius:4px;background:#eceef3;overflow:hidden;position:relative}
.mbar span{position:absolute;inset:0 auto 0 0;border-radius:4px}
.mbar em{position:absolute;top:-3px;bottom:-3px;width:2px;background:#9aa1b2;left:50%}
.hon{padding:8px 16px 14px;margin-top:auto}
.hon h4{margin:4px 0 6px;font-size:12px;color:var(--mute);font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12px;padding:3px 8px;border-radius:999px;background:#f3f4f7;color:#3a4152;font-weight:600}
.chip.top{background:var(--gold);color:#0f1d3d}
.cmp{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:auto;margin-bottom:14px}
.cmp h4{margin:0;padding:10px 14px;font-size:14px;color:#14254a;border-bottom:1px solid var(--line)}
.cmp table td,.cmp table th{padding:7px 8px}
.cmp td.best{font-weight:800;background:#fff3cf}
.soon{border:2px dashed #cdd2dd;border-radius:16px;display:flex;align-items:center;justify-content:center;color:var(--mute);font-size:14px;min-height:160px;text-align:center;padding:20px;background:transparent}
@media (max-width:640px){.cards{grid-template-columns:1fr}.cstats{grid-template-columns:repeat(2,1fr)}.age{grid-template-columns:54px 76px 1fr 40px;font-size:12.5px}.chead .go{display:none}}
</style></head>""")
rep('<main id="main"></main>','<section id="hub" class="hubwrap"></section>\n<main id="main"></main>')
rep("main{max-width:1280px;margin:0 auto;padding:16px}","main,.hubwrap{max-width:1280px;margin:0 auto;padding:16px}")

# --- JS: data + wrap renderer
rep("const D=__DATA__, SHEETS=__SHEETS__;","const CLUBS=__CLUBS__; let D, SHEETS, CK;")
rep("/준우승|^1위/","/^우승|^1위/")
a=tpl.index("SHEETS.forEach(([id,name,sub])=>{const b=$('button'")
b=tpl.index("function drawChart(")
body=tpl[a:b]
body=body.replace("넥스트플레이어 기준 · 2026-11-14","넥스트플레이어 기준 · ${CLUBS[CK].asof}")
body=re.sub(r"note\.textContent='[^']*'","note.textContent=CLUBS[CK].note",body)
assert 'CLUBS[CK].note' in body and 'CLUBS[CK].asof' in body
wrapped="""function renderClub(k){CK=k;const C=CLUBS[k];D=C.D;SHEETS=C.sheets;nav.innerHTML='';main.innerHTML='';
 document.body.dataset.club=k;const r=document.documentElement.style;r.setProperty('--navy',C.c1);r.setProperty('--navy2',C.c2);r.setProperty('--grad',C.grad);
 document.getElementById('ttl').textContent=`${C.name} 유스 연도별 성적`;
 document.getElementById('sub').textContent=`U11 · U12 · U14 · U15 · U17 · U18 | 출처: 넥스트플레이어(nextplayer.co.kr) 클럽 페이지 | ${C.asof} 기준`;
"""+body+"""show(SHEETS[0][0]);}
"""
tpl=tpl[:a]+wrapped+tpl[b:]
rep("const cols=['#24407a','#c9a24a']","const cols=[CLUBS[CK].c2,'#c9a24a']")
rep("show('u11');",r"""
function bestOf(T,yr){const y=T.years.find(v=>v[0]===yr);if(!y)return null;let best=null,bs=99;
 for(const c of y[7]){const r=c[2];let s=99;if(/^우승/.test(r))s=0;else if(/준우승/.test(r))s=1;else if(c[0]==='L'&&parseInt(r)===1)s=2;else if(/4강/.test(r))s=3;else if(c[0]==='L'&&parseInt(r)<=3)s=4;else if(/8강/.test(r))s=5;
  if(s<bs){bs=s;best=c}}return best}
function renderHub(){const H=document.getElementById('hub');H.innerHTML='';
 const it=$('div','hub-intro');it.append($('h2',null,'구단 한눈에 보기'),$('span',null,'카드를 누르면 연령별 상세 성적으로 이동합니다 · 2026 시즌 기준'));H.appendChild(it);
 const cards=$('div','cards');
 for(const [k,C] of Object.entries(CLUBS)){
  const ages=Object.keys(C.D);let a26={p:0,w:0,d:0,l:0},all={p:0,w:0,d:0,l:0};
  for(const t of ages){const ys=C.D[t].years;const s=sum(ys);all.p+=s.p;all.w+=s.w;all.d+=s.d;all.l+=s.l;const y=ys.find(v=>v[0]===2026);if(y){a26.p+=y[1];a26.w+=y[2];a26.d+=y[3];a26.l+=y[4]}}
  const card=$('div','club');card.id='club-'+k;card.tabIndex=0;card.setAttribute('role','link');
  card.onclick=()=>{location.hash=k};card.onkeydown=e=>{if(e.key==='Enter')location.hash=k};
  const hd=$('div','chead');hd.style.background=C.grad;const cr=$('div','crest',C.short.slice(0,3));const tt=$('div');tt.append($('h3',null,C.name),$('small',null,C.feeder));
  hd.append(cr,tt,$('span','go','자세히 보기 →'));card.appendChild(hd);
  const st=$('div','cstats');
  [[`${pct(a26.w,a26.p)}%`,'2026 승률','y'],[`${a26.w}-${a26.d}-${a26.l}`,'2026 승-무-패',''],[`${pct(all.w,all.p)}%`,'누적 승률',''],[`${all.p}`,'누적 경기','']].forEach(([v,l,c])=>{const d=$('div');d.append($('b',c,v),$('i',null,l));st.appendChild(d)});
  card.appendChild(st);
  const ag=$('div','ages');
  for(const t of ages){const T=C.D[t];const y=T.years.find(v=>v[0]===2026);const row=$('div','age');
   const an=$('div','an',t);an.appendChild($('small',null,T.label.replace(/^U\d+ /,'').replace(/[()]/g,'')));row.appendChild(an);
   if(y){const wr=pct(y[2],y[1]);row.appendChild($('div','wdl',`${y[2]}승 ${y[3]}무 ${y[4]}패`));
    const mb=$('div','mbar');const sp=$('span');sp.style.width=wr+'%';sp.style.background=wr>=60?'#2f7d4f':wr>=40?'#c9a24a':'#c0453a';mb.append(sp,$('em'));row.appendChild(mb);
    const w=$('div','wr',wr+'%');w.style.color=wr>=60?'#2f7d4f':wr>=40?'#9a7413':'#c0453a';row.appendChild(w)}
   else{row.append($('div','wdl','기록 없음'),$('div'),$('div'))}
   ag.appendChild(row)}
  card.appendChild(ag);
  const hon=$('div','hon');hon.appendChild($('h4',null,'2026 주요 성적'));const ch=$('div','chips');
  for(const t of ages){const b=bestOf(C.D[t],2026);if(b){const top=/^우승|준우승/.test(b[2])||(b[0]==='L'&&parseInt(b[2])===1);
   ch.appendChild($('span','chip'+(top?' top':''),`${t} ${b[1].replace(/\s*\[.*?\]|\(.*?\)/g,'').trim()} ${b[2]}`))}}
  hon.appendChild(ch);card.appendChild(hon);cards.appendChild(card)}
 const soon=$('div','soon');soon.textContent='다른 K리그 유스 구단 추가 예정';cards.appendChild(soon);
 H.appendChild(cards);
 // comparison
 const ages=['U11','U12','U14','U15','U17','U18'];const keys=Object.keys(CLUBS);
 const box=$('div','cmp');box.id='compare';box.appendChild($('h4',null,'연령별 2026 승률 비교 (괄호: 누적 승률)'));
 const tb=$('table');const hr=$('tr');hr.appendChild($('th',null,'연령'));keys.forEach(k=>hr.appendChild($('th',null,CLUBS[k].name)));const th=$('thead');th.appendChild(hr);tb.appendChild(th);
 const bd=$('tbody');
 for(const a of ages){const tr=$('tr');tr.appendChild($('td',null,a));
  const vals=keys.map(k=>{const T=CLUBS[k].D[a];if(!T)return null;const y=T.years.find(v=>v[0]===2026);const s=sum(T.years);return {w:y?pct(y[2],y[1]):null,txt:y?`${pct(y[2],y[1])}% · ${y[2]}승${y[3]}무${y[4]}패 (${pct(s.w,s.p)}%)`:'-'}});
  const mx=Math.max(...vals.map(v=>v&&v.w!=null?v.w:-1));
  vals.forEach(v=>{const td=$('td',v&&v.w===mx&&keys.length>1?'best':null,v?v.txt:'-');tr.appendChild(td)});bd.appendChild(tr)}
 tb.appendChild(bd);box.appendChild(tb);H.appendChild(box);
 H.appendChild($('div','note','※ 넥스트플레이어 클럽 페이지 기준. 기준일: '+Object.values(CLUBS).map(c=>`${c.name} ${c.asof}`).join(', ')+'. 승률 = 승 ÷ 경기(무승부 포함). 승부차기는 무승부로 계산했습니다.'));
}
function route(){const k=location.hash.slice(1);const r=document.documentElement.style;
 if(CLUBS[k]){document.body.classList.add('detail');renderClub(k);window.scrollTo(0,0)}
 else{document.body.classList.remove('detail');delete document.body.dataset.club;r.removeProperty('--navy');r.removeProperty('--navy2');
  document.getElementById('ttl').textContent='K리그 유스 성적 대시보드';document.getElementById('sub').textContent='구단을 선택하면 U11~U18 연령별 상세 성적을 볼 수 있습니다 · 출처: 넥스트플레이어(nextplayer.co.kr)';window.scrollTo(0,0)}}
document.getElementById('back').onclick=()=>{location.hash=''};
renderHub();route();window.addEventListener('hashchange',route);""")
rep("<script>\n// d3 inline loader placeholder\n</script>\n","")
d3=open('/home/claude/d3.min.js').read()
html=tpl.replace('__CLUBS__',json.dumps(CLUBS,ensure_ascii=False))
html=html.replace('</style><script>','</style><script>',1)
html=html.replace('</style>','</style><script>'+d3+'</script>',1) if False else html
i=html.rindex('</head>');html=html[:i]+'<script>'+d3+'</script>'+html[i:]
open('/home/claude/kleague_youth.html','w',encoding='utf-8').write(html)
print(len(html))
