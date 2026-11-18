import json, sys
sys.path.insert(0, '/home/claude')
from data import D, SHEETS

html = r"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>서울이랜드FC 유스 연도별 성적 (팀별)</title>
<style>
:root{--navy:#14254a;--navy2:#24407a;--gold:#c9a24a;--bg:#f4f5f8;--card:#fff;--ink:#1b1f2a;--mute:#6b7385;--line:#e3e6ee;
--w:#2f7d4f;--d:#8a8f9c;--l:#c0453a;--wbg:#e6f3ea;--lbg:#fbeaea}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;font-size:14px;line-height:1.45}
header{background:var(--navy);color:#fff;padding:18px 20px 0}
header h1{margin:0;font-size:20px;letter-spacing:-.3px}
header p{margin:4px 0 12px;color:#c8d0e3;font-size:12.5px}
nav{display:flex;gap:4px;flex-wrap:wrap}
nav button{border:0;background:transparent;color:#c8d0e3;padding:10px 16px;font-size:14px;font-weight:600;cursor:pointer;border-bottom:3px solid transparent;font-family:inherit}
nav button.on{color:#fff;border-bottom-color:var(--gold)}
nav .sp{flex:1}
nav .pr{border:1px solid #4a5f8f;border-radius:6px;margin:4px 0 8px;padding:6px 12px;font-size:12.5px}
main{max-width:1280px;margin:0 auto;padding:16px}
.sheet{display:none}.sheet.on,body.all .sheet{display:block}body.all .sheet{margin-bottom:28px}
.sh-head{display:flex;align-items:baseline;gap:10px;margin:4px 0 12px;border-bottom:2px solid var(--navy);padding-bottom:6px}
.sh-head h2{margin:0;font-size:22px;color:var(--navy)}
.sh-head span{color:var(--mute);font-size:13px}
.sh-head .src{margin-left:auto;font-size:11.5px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px;margin-bottom:12px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;border-top:4px solid var(--navy2)}
.kpi h3{margin:0 0 8px;font-size:15px;color:var(--navy);display:flex;justify-content:space-between}
.kpi h3 small{font-weight:500;color:var(--mute);font-size:12px}
.kgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.kgrid div{background:#f7f8fb;border-radius:6px;padding:6px 8px}
.kgrid b{display:block;font-size:18px;color:var(--ink)}
.kgrid i{font-style:normal;font-size:11px;color:var(--mute)}
.bar{display:flex;height:8px;border-radius:4px;overflow:hidden;margin:10px 0 4px}
.bar span:nth-child(1){background:var(--w)}.bar span:nth-child(2){background:var(--d)}.bar span:nth-child(3){background:var(--l)}
.hl{margin:8px 0 0;padding:0;list-style:none;font-size:12.5px}
.hl li{padding:2px 0}.hl li::before{content:"★ ";color:var(--gold)}
.chartbox{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:12px;position:relative}
.chartbox h4{margin:0 0 4px;font-size:13.5px;color:var(--navy)}
.legend{font-size:12px;color:var(--mute);display:flex;gap:14px;flex-wrap:wrap}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px}
.tip{position:absolute;pointer-events:none;background:var(--navy);color:#fff;font-size:12px;padding:6px 8px;border-radius:6px;white-space:nowrap;display:none;z-index:5}
.tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:12px}
.tbox{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:auto}
.tbox h4{margin:0;padding:10px 12px;font-size:14px;color:#fff;background:var(--navy2);position:sticky;left:0}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{padding:4px 6px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}
th{background:#eef1f7;color:var(--navy);font-weight:600;position:sticky;top:0}
td.n{text-align:left;white-space:normal;min-width:150px}
tr.yr td{background:#f3f5fa;font-weight:700;border-top:2px solid #c9d0e0}
tr.yr td.y{color:var(--navy);font-size:13.5px}
.tag{display:inline-block;font-size:10.5px;padding:0 5px;border-radius:3px;margin-right:4px;font-weight:700;vertical-align:1px}
.tag.L{background:#e3e9f7;color:var(--navy2)}.tag.C{background:#f6eedb;color:#8a6a1f}
.res{font-weight:600}
.res.top{color:#fff;background:var(--gold);border-radius:4px;padding:1px 6px}
.res.good{color:var(--w)}
.pos{color:var(--w)}.neg{color:var(--l)}
.wr{font-weight:700}
.y26{background:linear-gradient(140deg,#0f1d3d 0%,#1c3266 60%,#2b4583 100%);color:#fff;border-radius:16px;padding:18px 18px 16px;margin-bottom:16px;border:3px solid var(--gold);box-shadow:0 6px 22px rgba(20,37,74,.25)}
.y26h{display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.y26h .badge{background:var(--gold);color:#0f1d3d;font-weight:900;font-size:22px;padding:4px 14px;border-radius:8px;letter-spacing:.5px}
.y26h .ttl{font-size:22px;font-weight:800}
.y26h .delta{margin-left:auto;font-size:15px;font-weight:700;padding:5px 12px;border-radius:999px;background:rgba(255,255,255,.12)}
.y26h .delta.up{color:#8ff0b0}.y26h .delta.dn{color:#ffb0a6}
.y26top{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;margin-bottom:14px}
.ring{position:relative;width:132px;height:132px}
.ring svg{transform:rotate(-90deg)}
.ring .rv{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ring .rv b{font-size:34px;font-weight:900;color:#ffd76a;line-height:1}
.ring .rv i{font-style:normal;font-size:12px;color:#c8d0e3;margin-top:4px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.tile{border-radius:12px;padding:10px 8px;text-align:center;background:rgba(255,255,255,.08)}
.tile b{display:block;font-size:40px;font-weight:900;line-height:1.05}
.tile i{font-style:normal;font-size:13px;font-weight:700}
.tile.w{background:#2f7d4f}.tile.d{background:#5d6475}.tile.l{background:#b23b31}
.subt{grid-column:1/-1;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.subt div{background:rgba(255,255,255,.08);border-radius:10px;padding:7px 10px}
.subt b{display:block;font-size:20px;font-weight:800}.subt b.pos{color:#8ff0b0}.subt b.neg{color:#ffb0a6}
.subt i{font-style:normal;font-size:11.5px;color:#c8d0e3}
.comps{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:8px}
.comp{background:#fff;color:#14254a;border-radius:12px;padding:10px 12px;display:flex;gap:12px;align-items:center}
.comp .rb{min-width:76px;text-align:center;font-size:22px;font-weight:900;border-radius:10px;padding:8px 6px;background:#e9edf5;color:#14254a;line-height:1.1}
.comp .rb.top{background:var(--gold);color:#0f1d3d}.comp .rb.good{background:#2f7d4f;color:#fff}
.comp .rb small{display:block;font-size:10.5px;font-weight:700;opacity:.8;margin-top:2px}
.comp .cn{font-size:13.5px;font-weight:700;line-height:1.3}
.comp .cs{font-size:12.5px;color:#5b6378;margin-top:3px}
.comp .cs b{color:#14254a}
@media (max-width:640px){.y26top{grid-template-columns:1fr;justify-items:center}.tiles,.subt{width:100%}.subt{grid-template-columns:repeat(2,1fr)}.comps{grid-template-columns:1fr}.tile b{font-size:34px}.y26h .delta{margin-left:0}}
tr.yr.y26r td{background:#fff3cf;border-top:3px solid var(--gold);font-size:14px;color:#14254a}
tr.yr.y26r td.y::before{content:"★ ";color:var(--gold)}
tr.c26 td{background:#fffaf0}
tr.c26 td.n{border-left:4px solid var(--gold)}
.note{font-size:11.5px;color:var(--mute);margin-top:12px;line-height:1.6}
@media (max-width:640px){.sh-head .src{display:none}.sh-head h2{white-space:nowrap;font-size:19px}.tables{grid-template-columns:1fr}.kgrid b{font-size:16px}main{padding:10px}}
@media print{
 @page{size:A4 portrait;margin:8mm}
 body{background:#fff;font-size:10px}
 header,.noprint{display:none}
 main{padding:0;max-width:none}
 .sheet{display:block!important;page-break-after:always;zoom:.62}
 .sheet:last-child{page-break-after:auto}
 .tables{grid-template-columns:1fr 1fr}
 .tbox{overflow:visible;break-inside:avoid}
 th{position:static}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
</style></head><body>
<header>
 <h1>서울이랜드FC 유스 연도별 성적</h1>
 <p>U11 · U12 · U14 · U15 · U17 · U18 | 출처: 넥스트플레이어(nextplayer.co.kr) 클럽 페이지 | 2026-11-14 기준</p>
 <nav id="nav"></nav>
</header>
<main id="main"></main>
<script>
const D=__DATA__, SHEETS=__SHEETS__;
const $=(t,c,txt)=>{const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e};
const pct=(w,p)=>p?Math.round(w/p*100):0;
const sum=ys=>ys.reduce((a,y)=>{a.p+=y[1];a.w+=y[2];a.d+=y[3];a.l+=y[4];a.gf+=y[5];a.ga+=y[6];return a},{p:0,w:0,d:0,l:0,gf:0,ga:0});
function grade(c){const r=c[2];
 if(c[0]==='C'){if(/우승/.test(r))return 'top';if(/4강|8강/.test(r))return 'good';return ''}
 const n=parseInt(r);if(n===1)return 'top';if(n<=3)return 'good';return ''}
function highlights(team){const out=[];
 for(const y of D[team].years)for(const c of y[7]){const g=grade(c);
  if(g)out.push({y:y[0],t:`${y[0]} ${c[1]} — ${c[2]}`,s:(g==='top'?0:1)*10000+(/준우승|^1위/.test(c[2])?0:1)*1000-y[0]})}
 return out.sort((a,b)=>a.s-b.s).slice(0,5).map(x=>x.t)}

const nav=document.getElementById('nav'), main=document.getElementById('main');
function show(id){document.querySelectorAll('.sheet').forEach(s=>s.classList.toggle('on',s.id===id));
 nav.querySelectorAll('button[data-id]').forEach(b=>b.classList.toggle('on',b.dataset.id===id));drawAll();}
SHEETS.forEach(([id,name,sub])=>{const b=$('button',null,`${name} (${sub})`);b.dataset.id=id;b.onclick=()=>show(id);nav.appendChild(b)});
nav.appendChild($('span','sp'));
const pb=$('button','pr','6장 모두 펼치기');pb.onclick=()=>{const all=document.body.classList.toggle('all');pb.textContent=all?'한 장씩 보기':'6장 모두 펼치기';drawAll()};nav.appendChild(pb);

SHEETS.forEach(([id,name,sub,teams],si)=>{
 const S=$('section','sheet');S.id=id;
 const h=$('div','sh-head');h.append($('h2',null,`${name} 성적표`),$('span',null,sub),$('span','src',`${si+1}/${SHEETS.length} · 넥스트플레이어 기준 · 2026-11-14`));S.appendChild(h);
 // 2026 hero
 teams.forEach(t=>{const T=D[t];const y=T.years.find(v=>v[0]===2026),p=T.years.find(v=>v[0]===2025);if(!y)return;
  const Y=$('div','y26');Y.id=id+'-2026';const yh=$('div','y26h');yh.append($('span','badge','2026'),$('span','ttl',`${T.label} 올해 시즌 성적`));
  const wr=pct(y[2],y[1]);
  if(p){const dlt=wr-pct(p[2],p[1]);yh.appendChild($('span','delta '+(dlt>0?'up':dlt<0?'dn':''),`전년 대비 ${dlt>0?'▲':dlt<0?'▼':'–'} ${Math.abs(dlt)}%p`))}
  Y.appendChild(yh);
  const top=$('div','y26top');
  const ring=$('div','ring');const R=56,C=2*Math.PI*R;
  ring.innerHTML=`<svg width="132" height="132"><circle cx="66" cy="66" r="${R}" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="14"/><circle cx="66" cy="66" r="${R}" fill="none" stroke="#ffd76a" stroke-width="14" stroke-linecap="round" stroke-dasharray="${C*wr/100} ${C}"/></svg>`;
  const rv=$('div','rv');rv.append($('b',null,wr+'%'),$('i',null,'승률'));ring.appendChild(rv);top.appendChild(ring);
  const tiles=$('div','tiles');[['w',y[2],'승'],['d',y[3],'무'],['l',y[4],'패']].forEach(([c,v,l])=>{const d=$('div','tile '+c);d.append($('b',null,v),$('i',null,l));tiles.appendChild(d)});
  top.appendChild(tiles);
  const gd=y[5]-y[6];const sb=$('div','subt');
  [[y[1],'경기','' ],[y[5],'득점',''],[y[6],'실점',''],[(gd>0?'+':'')+gd,'득실차',gd>0?'pos':gd<0?'neg':'']].forEach(([v,l,c])=>{const d=$('div');d.append($('b',c,v),$('i',null,l));sb.appendChild(d)});
  top.appendChild(sb);Y.appendChild(top);
  const cs=$('div','comps');
  y[7].forEach(c=>{const cd=$('div','comp');const rb=$('div','rb '+grade(c));if(c[2].length>6){rb.style.fontSize='14px';rb.style.minWidth='96px'}rb.appendChild(document.createTextNode(c[2]));rb.appendChild($('small',null,c[0]==='L'?'리그':'대회'));
   const info=$('div');info.appendChild($('div','cn',c[1]));const st=$('div','cs');st.textContent=`${c[3]}경기 `;const bb=$('b',null,`${c[4]}승 ${c[5]}무 ${c[6]}패`);st.appendChild(bb);st.appendChild(document.createTextNode(` · ${c[7]}득 ${c[8]}실 · ${c[9]}`));info.appendChild(st);
   cd.append(rb,info);cs.appendChild(cd)});
  Y.appendChild(cs);S.appendChild(Y)});
 // KPI
 const K=$('div','kpis');
 teams.forEach(t=>{const T=D[t],a=sum(T.years),last=T.years[T.years.length-1];
  const k=$('div','kpi');const h3=$('h3',null,T.label);h3.appendChild($('small',null,`${T.years[0][0]}~${last[0]} · ${T.years.length}시즌`));k.appendChild(h3);
  const g=$('div','kgrid');
  [[`${a.p}`,'누적 경기'],[`${a.w}-${a.d}-${a.l}`,'승-무-패'],[`${pct(a.w,a.p)}%`,'승률'],[`${a.gf-a.ga>0?'+':''}${a.gf-a.ga}`,`득실(${a.gf}/${a.ga})`]]
   .forEach(([v,l])=>{const d=$('div');d.append($('b',null,v),$('i',null,l));g.appendChild(d)});
  k.appendChild(g);
  const bar=$('div','bar');[a.w,a.d,a.l].forEach(v=>{const s=$('span');s.style.width=(v/a.p*100)+'%';bar.appendChild(s)});k.appendChild(bar);
  const hl=highlights(t);if(hl.length){const ul=$('ul','hl');hl.forEach(x=>ul.appendChild($('li',null,x)));k.appendChild(ul)}
  K.appendChild(k)});
 S.appendChild(K);
 // chart
 const cb=$('div','chartbox');cb.id=id+'-chart';
 cb.appendChild($('h4',null,'연도별 승률 추이 (%)'));
 const lg=$('div','legend');const cols=['#24407a','#c9a24a'];
 teams.forEach((t,i)=>{const s=$('span');const sw=$('i');sw.style.background=cols[i];s.append(sw,document.createTextNode(D[t].label));lg.appendChild(s)});
 cb.appendChild(lg);const holder=$('div');cb.appendChild(holder);const tip=$('div','tip');cb.appendChild(tip);
 S.appendChild(cb);
 cb._draw=()=>drawChart(holder,tip,teams,cols);
 // tables
 const TS=$('div','tables');
 teams.forEach(t=>{const T=D[t];const box=$('div','tbox');box.id=id+'-'+t;box.appendChild($('h4',null,`${T.label} 연도별·대회별 기록`));
  const tb=$('table');const thr=$('tr');['연도/대회','성적','경기','승','무','패','득','실','득실','승률'].forEach(x=>thr.appendChild($('th',null,x)));
  const thead=$('thead');thead.appendChild(thr);tb.appendChild(thead);const body=$('tbody');
  [...T.years].reverse().forEach(y=>{
   const r=$('tr','yr'+(y[0]===2026?' y26r':''));const gd=y[5]-y[6];
   r.append($('td','n y',`${y[0]}년 합계`),$('td',null,''),$('td',null,y[1]),$('td',null,y[2]),$('td',null,y[3]),$('td',null,y[4]),$('td',null,y[5]),$('td',null,y[6]));
   const g=$('td',gd>0?'pos':gd<0?'neg':'',(gd>0?'+':'')+gd);r.appendChild(g);r.appendChild($('td','wr',pct(y[2],y[1])+'%'));body.appendChild(r);
   y[7].forEach(c=>{const tr=$('tr',y[0]===2026?'c26':null);const n=$('td','n');n.append($('span','tag '+c[0],c[0]==='L'?'리그':'대회'),document.createTextNode(c[1]));
    const sub=$('div',null,c[9]);sub.style.cssText='font-size:10.5px;color:#8a90a0';n.appendChild(sub);tr.appendChild(n);
    const rs=$('td');const sp=$('span','res '+grade(c),c[2]);rs.appendChild(sp);tr.appendChild(rs);
    [3,4,5,6,7,8].forEach(i=>tr.appendChild($('td',null,c[i])));const d=c[7]-c[8];
    tr.appendChild($('td',d>0?'pos':d<0?'neg':'',(d>0?'+':'')+d));tr.appendChild($('td',null,pct(c[4],c[3])+'%'));body.appendChild(tr)});
  });
  tb.appendChild(body);box.appendChild(tb);TS.appendChild(box)});
 S.appendChild(TS);
 const note=$('div','note');
 note.textContent='※ 연도 합계는 넥스트플레이어 집계값, 대회별 행은 경기 결과를 대회 단위로 합산한 값입니다(일부 연도는 두 값이 1~3경기 차이). 리그 순위는 사이트의 "리그 순위" 기준, 대회 성적의 "n조 m위"는 조별리그 순위이며 두 개면 1차/2차 조별리그입니다. 승부차기 경기는 무승부로 계산했습니다. 2020년 U12, 코로나 등으로 기록이 없는 연도는 표시되지 않습니다. 2026 시즌은 진행 중일 수 있습니다.';
 S.appendChild(note);
 main.appendChild(S);
});

function drawChart(holder,tip,teams,cols){
 holder.innerHTML='';const W=Math.max(300,holder.clientWidth),H=window.CH||200,m={l:34,r:10,t:24,b:24};
 const yrs=[...new Set(teams.flatMap(t=>D[t].years.map(y=>y[0])))].sort();
 const x=d3.scalePoint().domain(yrs).range([m.l,W-m.r]).padding(.4),y=d3.scaleLinear().domain([0,100]).range([H-m.b,m.t]);
 const svg=d3.select(holder).append('svg').attr('width',W).attr('height',H);
 svg.append('g').attr('transform',`translate(0,${H-m.b})`).call(d3.axisBottom(x).tickSizeOuter(0)).selectAll('text').style('font-size','11px');
 svg.append('g').attr('transform',`translate(${m.l},0)`).call(d3.axisLeft(y).ticks(5).tickSize(-(W-m.l-m.r))).call(g=>g.select('.domain').remove()).call(g=>g.selectAll('line').attr('stroke','#e3e6ee')).selectAll('text').style('font-size','11px');
 if(yrs.includes(2026)){const bw=x.step();svg.insert('rect',':first-child').attr('x',x(2026)-bw/2).attr('y',m.t-20).attr('width',bw).attr('height',H-m.b-m.t+20).attr('fill','#fff3cf');svg.append('text').attr('x',x(2026)).attr('y',m.t-8).attr('text-anchor','middle').attr('font-size','11px').attr('font-weight',800).attr('fill','#8a6a1f').text('2026');}
 svg.append('line').attr('x1',m.l).attr('x2',W-m.r).attr('y1',y(50)).attr('y2',y(50)).attr('stroke','#b9bfcc').attr('stroke-dasharray','4 3');
 teams.forEach((t,i)=>{const pts=D[t].years.map(v=>({yr:v[0],wr:pct(v[2],v[1]),v}));
  svg.append('path').datum(pts).attr('fill','none').attr('stroke',cols[i]).attr('stroke-width',2.5).attr('d',d3.line().x(d=>x(d.yr)).y(d=>y(d.wr)).defined((d,j)=>true));
  const g=svg.append('g');
  g.selectAll('circle').data(pts).join('circle').attr('cx',d=>x(d.yr)).attr('cy',d=>y(d.wr)).attr('r',d=>d.yr===2026?7:4.5).attr('fill',cols[i]).attr('stroke','#fff').attr('stroke-width',1.5)
   .on('pointerenter pointermove',(ev,d)=>{tip.style.display='block';tip.textContent=`${D[t].label} ${d.yr}: ${d.v[1]}경기 ${d.v[2]}승 ${d.v[3]}무 ${d.v[4]}패 · 승률 ${d.wr}% · ${d.v[5]}득 ${d.v[6]}실`;
     const r=holder.parentNode.getBoundingClientRect();let lx=ev.clientX-r.left+10;if(lx+tip.offsetWidth>r.width)lx=r.width-tip.offsetWidth-4;tip.style.left=lx+'px';tip.style.top=(ev.clientY-r.top-34)+'px'})
   .on('pointerleave',()=>tip.style.display='none');
  g.selectAll('text').data(pts).join('text').attr('x',d=>x(d.yr)).attr('y',d=>y(d.wr)-8-(i?0:0)).attr('text-anchor','middle').attr('font-size',d=>d.yr===2026?'13px':'10px').attr('fill',cols[i]).attr('font-weight',700).attr('dy',i?18:0).text(d=>d.wr);
 });
}
function drawAll(){document.querySelectorAll('.chartbox').forEach(c=>c._draw&&c._draw())}
show('u11');
window.addEventListener('resize',()=>{clearTimeout(window._rt);window._rt=setTimeout(drawAll,150)});
window.addEventListener('beforeprint',()=>{if(document.body.classList.contains('pdf'))return;document.querySelectorAll('.sheet').forEach(s=>s.style.display='block');drawAll()});
window.addEventListener('afterprint',()=>{if(document.body.classList.contains('pdf'))return;document.querySelectorAll('.sheet').forEach(s=>s.style.display='');drawAll()});
</script>
<script>
// d3 inline loader placeholder
</script>
</body></html>"""

d3 = open('/home/claude/d3.min.js').read()
sheets = [[a,b,c,d] for a,b,c,d in SHEETS]
html = html.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__SHEETS__', json.dumps(sheets, ensure_ascii=False))
# d3 must load before main script: inject into head
html = html.replace('</style></head>', '</style><script>'+d3+'</script></head>')
html = html.replace("<script>\n// d3 inline loader placeholder\n</script>\n", "<script>drawAll()</script>\n")
open('/home/claude/eland_youth.html','w').write(html)
print(len(html))
