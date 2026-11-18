# -*- coding: utf-8 -*-
"""상단 '최신 데이터' 버튼 추가.

버튼을 누르면 브라우저가 넥스트플레이어 API(teamInfoCup / teamInfoLeague)를
구단·연령별로 직접 불러와 올해 시즌 기록을 다시 계산하고 화면을 갱신한다.
결과는 그 브라우저의 localStorage 에 저장돼 다음 방문 때도 유지된다.
(사이트 파일 자체는 바뀌지 않는다 — 모든 방문자에게 반영하려면 재빌드·배포 필요)

restyle.py 다음에 실행:  python build/add_refresh.py [index.html 경로]
"""
import sys, pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html")
html = path.read_text(encoding="utf-8")
MARK = "/*np-refresh*/"
if MARK in html:
    print("already has refresh:", path); sys.exit(0)

CSS = MARK + r"""
.refresh{margin-left:auto;display:inline-flex;align-items:center;gap:7px;border:1px solid rgba(245,196,81,.55);background:rgba(245,196,81,.12);color:var(--gold);
 border-radius:999px;padding:8px 15px;font:800 13px/1 inherit;font-family:inherit;cursor:pointer;transition:background .15s,transform .15s;white-space:nowrap}
.refresh:hover{background:rgba(245,196,81,.22);transform:translateY(-1px)}
.refresh:disabled{opacity:.7;cursor:progress;transform:none}
.refresh .ic{display:inline-block;font-size:15px}
.refresh.busy .ic{animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#rstat{display:block;margin-top:6px;font-size:12px;color:rgba(255,255,255,.6);min-height:0}
#rstat.ok{color:#4ade80}#rstat.err{color:#f87171}
@media (max-width:640px){.refresh{padding:7px 12px;font-size:12px}}
"""

BTN_OLD = '<h1 id="ttl">K리그 유스 성적 대시보드</h1></div>'
BTN_NEW = ('<h1 id="ttl">K리그 유스 성적 대시보드</h1>'
           '<button id="refresh" class="refresh" title="넥스트플레이어에서 올해 시즌 기록을 다시 불러옵니다"><span class="ic">⟳</span><span class="tx">최신 데이터</span></button></div>\n'
           ' <span id="rstat"></span>')

JS = r"""
/* ---- 넥스트플레이어 최신화 ---- */
const NP='https://mobile.nextplayer.co.kr/back_front/base_front/api/v1/',NP_YEAR=new Date().getFullYear(),NP_KEY='np-refresh-v2';
const today=()=>{const d=new Date(),z=n=>String(n).padStart(2,'0');return `${d.getFullYear()}-${z(d.getMonth()+1)}-${z(d.getDate())}`};
async function npGet(ep,id,ag,yr){const r=await fetch(`${NP}${ep}?teamId=${id}&ageGroup=${ag}&sYear=${yr}`);if(!r.ok)throw new Error('HTTP '+r.status);
 const j=await r.json();if(j.state!=='SUCCESS')throw new Error(j.msg||'API 오류');return j.data}
function npName(ty,raw){const m=String(raw).match(/^\[([^\]]+)\]\s*(.*)$/);let br=m?m[1]:'',rest=(m?m[2]:String(raw)).trim();
 rest=rest.replace(/^20\d\d\s+/,'');br=br.replace(/^U1\d_/,'');
 return ty==='C'?`${rest}(${br.split('/').pop().trim()})`:`${rest} [${br}]`}
const npMD=s=>s?`${s.slice(4,6)}.${s.slice(6,8)}`:'';
const npD8=s=>s?String(s).replace(/\D/g,'').slice(0,8):'';
const npPer=(a,b)=>a||b?`${npMD(a||b)}~${npMD(b||a)}`:'';
const npLists=new Map();   // 연령별 시즌 리그·대회 목록 (id → 이름), 한 번만 불러옴
function npList(ep,ag,yr){const k=ep+ag+yr;if(!npLists.has(k))npLists.set(k,fetch(`${NP}${ep}?sYear=${yr}&ageGroup=${ag}`).then(r=>r.json()).then(j=>j.data||{}).catch(()=>({})));return npLists.get(k)}
const npSortRes=a=>a.sort((x,y)=>x.localeCompare(y,'ko',{numeric:true})).join('/');
// 한 팀의 올해 시즌 → [연도, 경기, 승, 무, 패, 득, 실, [대회...]]
//  · 대회별 기록: teamInfo 의 전체 경기 목록을 리그/대회 id 별로 묶어 계산 (승부차기는 무승부)
//  · 연도 합계: 넥스트플레이어 시즌 요약(teamResultMap) — 기존 데이터와 같은 방식
//  · 이미 있던 대회(같은 구분·같은 시작일)는 다듬어 둔 기존 대회명을 유지
async function npSeason(id,ag,yr,old){
 const [inf,c,l,LL,CL]=await Promise.all([npGet('teamInfo',id,ag,yr),npGet('teamInfoCup',id,ag,yr),npGet('teamInfoLeague',id,ag,yr),npList('league',ag,yr),npList('cup',ag,yr)]);
 const sid=String(id),LN={},CN={},CR={},LR={};
 for(const x of LL.totalleagueList||[])LN[x.league_id]=x.league_name;
 for(const x of CL.totalCupList||[])CN[x.cup_id]=x.cup_name;
 for(const x of [...(c.teamCupMatchList||[]),...(c.teamCupResultList||[])])if(x.cup_id!=null&&x.cup_name)CN[x.cup_id]=CN[x.cup_id]||x.cup_name;
 for(const x of c.teamCupResultList||[])if(x.result){const a=CR[x.cup_id]=CR[x.cup_id]||[];if(!a.includes(x.result))a.push(x.result)}
 for(const x of l.teamLeagueEnterList||[])if(String(x.team_id)===sid){LN[x.league_id]=LN[x.league_id]||x.league_name;if(x.rank)LR[x.league_id]=`${x.rank}위`}
 const rankByName={};for(const x of l.teamLeagueRankList||[])if(String(x.play_year)===String(yr)&&x.rank)rankByName[x.league_name]=`${x.rank}위`;
 const g=new Map();
 for(const m of inf.teamTotalMatchList||[]){const home=String(m.home_id)===sid;if(!home&&String(m.away_id)!==sid)continue;
  if(m.home_score==null||m.away_score==null)continue;const ty=+m.total_type===1?'L':'C',k=ty+m.league_id;
  const e=g.get(k)||{ty,id:String(m.league_id),m:[]};g.set(k,e);e.m.push({gf:+(home?m.home_score:m.away_score),ga:+(home?m.away_score:m.home_score),d:npD8(m.pdate)})}
 const oc=(old&&old[7])||[];const comps=[];
 for(const e of g.values()){const ds=e.m.map(x=>x.d).filter(Boolean).sort(),per=npPer(ds[0],ds[ds.length-1]);
  const w=e.m.filter(x=>x.gf>x.ga).length,d=e.m.filter(x=>x.gf===x.ga).length;
  const raw=e.ty==='L'?LN[e.id]:CN[e.id];let res=e.ty==='L'?(LR[e.id]||rankByName[raw]):(CR[e.id]&&npSortRes(CR[e.id]));
  const prev=oc.find(o=>o[0]===e.ty&&o[9].split('~')[0]===npMD(ds[0]));
  const nm=prev?prev[1]:raw?npName(e.ty,raw):(e.ty==='L'?'리그':'대회')+` #${e.id}`;
  if(prev&&res&&npSortRes(prev[2].split('/'))===npSortRes(res.split('/')))res=prev[2];   // 같은 성적이면 기존 표기 순서 유지
  comps.push({k:ds[0]||'',c:[e.ty,nm,res||(prev&&prev[2])||'-',e.m.length,w,d,e.m.length-w-d,e.m.reduce((a,x)=>a+x.gf,0),e.m.reduce((a,x)=>a+x.ga,0),per]})}
 if(!comps.length)return null;
 comps.sort((a,b)=>a.k<b.k?-1:a.k>b.k?1:0);const cs=comps.map(x=>x.c);
 const R=inf.teamResultMap,t=i=>cs.reduce((a,x)=>a+x[i],0);
 const tot=R&&+R.played>0?[+R.played,+R.won,+R.draw,+R.lost,+R.gf,+R.ga]:[t(3),t(4),t(5),t(6),t(7),t(8)];
 return [yr,...tot,cs]}
function npApply(club,ag,y){const T=CLUBS[club]&&CLUBS[club].D[ag];if(!T||!y)return false;const i=T.years.findIndex(v=>v[0]===y[0]);
 const same=i>=0&&JSON.stringify(T.years[i])===JSON.stringify(y);if(i>=0)T.years[i]=y;else{T.years.push(y);T.years.sort((a,b)=>a[0]-b[0])}return !same}
function npRerender(){const k=location.hash.slice(1);renderHub();
 if(CLUBS[k]){const on=document.querySelector('.sheet.on');const sid=on&&on.id;renderClub(k);if(sid&&document.getElementById(sid))show(sid)}else route()}
function npStat(t,c){const s=document.getElementById('rstat');s.textContent=t;s.className=c||''}
function npLoadCache(){try{const c=JSON.parse(localStorage.getItem(NP_KEY)||'null');if(!c||c.year!==NP_YEAR)return;
  for(const [club,ages] of Object.entries(c.data)){if(!CLUBS[club]||c.day<CLUBS[club].asof)continue;for(const [ag,y] of Object.entries(ages))npApply(club,ag,y);CLUBS[club].asof=c.day}
  npStat(`${c.at} 최신화된 기록 (이 브라우저에 저장됨)`)}catch(e){}}
async function npRefresh(){const b=document.getElementById('refresh');if(b.disabled)return;b.disabled=true;b.classList.add('busy');
 const jobs=[];for(const [club,C] of Object.entries(CLUBS))for(const [ag,T] of Object.entries(C.D))jobs.push({club,ag,id:T.id,name:`${C.short} ${ag}`});
 let done=0,changed=0;const fails=[],out={};npStat(`넥스트플레이어에서 불러오는 중… 0/${jobs.length}`);
 const run=async j=>{try{const y=await npSeason(j.id,j.ag,NP_YEAR,CLUBS[j.club].D[j.ag].years.find(v=>v[0]===NP_YEAR));if(y){(out[j.club]=out[j.club]||{})[j.ag]=y;if(npApply(j.club,j.ag,y))changed++}}catch(e){fails.push(j.name)}
  done++;npStat(`넥스트플레이어에서 불러오는 중… ${done}/${jobs.length}`)};
 const q=[...jobs];await Promise.all(Array.from({length:6},async()=>{while(q.length)await run(q.shift())}));
 const d=new Date(),at=`${today()} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
 for(const club of Object.keys(out))CLUBS[club].asof=today();
 try{localStorage.setItem(NP_KEY,JSON.stringify({year:NP_YEAR,day:today(),at,data:out}))}catch(e){}
 npRerender();b.disabled=false;b.classList.remove('busy');
 if(fails.length===jobs.length)npStat('불러오기 실패 — 잠시 후 다시 시도해 주세요','err');
 else npStat(`✓ ${at} 최신화 완료 · ${NP_YEAR} 시즌 ${jobs.length-fails.length}팀 확인 · 변경 ${changed}팀`+(fails.length?` · 실패: ${fails.join(', ')}`:''),fails.length?'err':'ok')}
document.getElementById('refresh').onclick=npRefresh;
"""

CALL_OLD = "renderHub();route();window.addEventListener('hashchange',route);"
CALL_NEW = "npLoadCache();renderHub();route();window.addEventListener('hashchange',route);"

for old in ("</style><script>// https://d3js", BTN_OLD, CALL_OLD):
    assert html.count(old) == 1, "패치 대상 없음/중복: " + old[:50]
html = html.replace("</style><script>// https://d3js", CSS + "</style><script>// https://d3js", 1)
html = html.replace(BTN_OLD, BTN_NEW, 1)
html = html.replace(CALL_OLD, JS + CALL_NEW, 1)
path.write_text(html, encoding="utf-8", newline="\n")
print("added refresh:", path)
