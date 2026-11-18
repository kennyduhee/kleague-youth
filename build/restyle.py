# -*- coding: utf-8 -*-
"""index.html 디자인 리뉴얼 (다크 '스타디움' 테마).

데이터·로직은 그대로 두고 CSS 블록 교체 + JS 안의 색상 몇 곳만 바꾼다.
build_hub.py 로 index.html 을 다시 만든 뒤에도 이 스크립트를 한 번 돌리면 된다.
    python build/restyle.py [index.html 경로]
"""
import sys, pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html")
html = path.read_text(encoding="utf-8")

FONT = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">\n'

CSS = r"""
:root{--bg:#090d15;--bg2:#0d1320;--card:#111827;--card2:#172033;--line:rgba(255,255,255,.07);--line2:rgba(255,255,255,.13);
--ink:#eef2f8;--ink2:#c5cddb;--mute:#8590a6;--gold:#f5c451;--acc:#5b8cff;--navy:#14254a;--navy2:#24407a;
--w:#22c55e;--d:#64748b;--l:#ef4444;--wt:#4ade80;--lt:#f87171;--r:18px}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;color:var(--ink);font-family:"Pretendard Variable","Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;font-size:14px;line-height:1.5;
 background:radial-gradient(900px 500px at 85% -5%,color-mix(in srgb,var(--acc) 16%,transparent),transparent 70%),radial-gradient(700px 400px at -10% 30%,rgba(245,196,81,.05),transparent 70%),var(--bg);background-attachment:fixed;min-height:100vh;-webkit-font-smoothing:antialiased}
::selection{background:var(--gold);color:#111}

/* ---------- header ---------- */
header{position:relative;overflow:hidden;overflow:clip;color:#fff;padding:30px 24px 18px;border-bottom:1px solid var(--line);
 background:linear-gradient(180deg,rgba(9,13,21,0) 40%,rgba(9,13,21,.85) 100%),radial-gradient(800px 300px at 20% -20%,color-mix(in srgb,var(--acc) 40%,transparent),transparent 70%),#0b1120}
body[data-club] header{background:linear-gradient(180deg,rgba(9,13,21,.05) 0%,rgba(9,13,21,.9) 100%),var(--grad)}
header::after{content:"";position:absolute;right:-120px;top:-160px;width:420px;height:420px;border-radius:50%;border:60px solid rgba(255,255,255,.035);pointer-events:none}
header>*{position:relative;z-index:1;max-width:1280px;margin-left:auto;margin-right:auto}
header::before{content:"K LEAGUE · YOUTH ANALYTICS";display:block;max-width:1280px;margin:0 auto 10px;font-size:11px;letter-spacing:.28em;font-weight:800;color:var(--gold);position:relative;z-index:1}
header h1{margin:0;font-size:clamp(24px,3.4vw,36px);font-weight:850;letter-spacing:-.8px;line-height:1.15}
header p{margin:8px auto 0;color:rgba(255,255,255,.62);font-size:13px}
.hrow{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.back{display:none;border:1px solid var(--line2);background:rgba(255,255,255,.06);color:#fff;border-radius:999px;padding:7px 14px;font:700 13px/1 inherit;cursor:pointer;font-family:inherit;backdrop-filter:blur(8px);transition:background .15s}
.back:hover{background:rgba(255,255,255,.14)}
body.detail .back{display:inline-block}
nav{display:flex;gap:6px;flex-wrap:wrap;margin-top:18px}
body:not(.detail) nav{display:none}
nav button{border:1px solid var(--line2);background:rgba(255,255,255,.04);color:var(--ink2);padding:8px 15px;font-size:13.5px;font-weight:700;cursor:pointer;border-radius:999px;font-family:inherit;transition:all .15s}
nav button:hover{background:rgba(255,255,255,.1);color:#fff}
nav button.on{background:var(--gold);border-color:var(--gold);color:#14110a;box-shadow:0 6px 18px -6px rgba(245,196,81,.7)}
nav .sp{flex:1}
nav .pr{border-style:dashed;font-size:12.5px}

main,.hubwrap{max-width:1280px;margin:0 auto;padding:24px}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.sheet{display:none}.sheet.on,body.all .sheet{display:block;animation:rise .35s ease both}body.all .sheet{margin-bottom:40px}

/* ---------- section head ---------- */
.sh-head{display:flex;align-items:baseline;gap:12px;margin:4px 0 16px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.sh-head h2{margin:0;font-size:26px;font-weight:850;letter-spacing:-.6px;color:var(--ink)}
.sh-head span{color:var(--mute);font-size:13px}
.sh-head .src{margin-left:auto;font-size:11.5px}

/* ---------- 2026 hero ---------- */
.y26{position:relative;overflow:hidden;overflow:clip;background:var(--grad,linear-gradient(140deg,#0f1d3d,#2b4583));color:#fff;border-radius:24px;padding:24px;margin-bottom:18px;
 border:1px solid rgba(245,196,81,.45);box-shadow:0 0 0 4px rgba(245,196,81,.06),0 30px 60px -25px rgba(0,0,0,.8)}
.y26::before{content:"";position:absolute;inset:0;background:radial-gradient(600px 260px at 100% 0%,rgba(255,255,255,.12),transparent 60%),repeating-linear-gradient(115deg,rgba(255,255,255,.02) 0 2px,transparent 2px 14px);pointer-events:none}
.y26>*{position:relative}
.y26h{display:flex;align-items:center;gap:12px;margin-bottom:18px;flex-wrap:wrap}
.y26h .badge{background:var(--gold);color:#14110a;font-weight:900;font-size:20px;padding:4px 14px;border-radius:10px;letter-spacing:.5px}
.y26h .ttl{font-size:22px;font-weight:850;letter-spacing:-.4px}
.y26h .delta{margin-left:auto;font-size:14px;font-weight:800;padding:6px 14px;border-radius:999px;background:rgba(0,0,0,.28);border:1px solid rgba(255,255,255,.12)}
.y26h .delta.up{color:var(--wt)}.y26h .delta.dn{color:var(--lt)}
.y26top{display:grid;grid-template-columns:auto 1fr;gap:20px;align-items:center;margin-bottom:18px}
.ring{position:relative;width:132px;height:132px;filter:drop-shadow(0 0 18px rgba(255,215,106,.35))}
.ring svg{transform:rotate(-90deg)}
.ring .rv{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ring .rv b{font-size:34px;font-weight:900;color:#ffd76a;line-height:1;font-variant-numeric:tabular-nums}
.ring .rv i{font-style:normal;font-size:12px;color:rgba(255,255,255,.65);margin-top:4px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.tile{border-radius:16px;padding:12px 8px;text-align:center;border:1px solid rgba(255,255,255,.12)}
.tile b{display:block;font-size:42px;font-weight:900;line-height:1.05;font-variant-numeric:tabular-nums}
.tile i{font-style:normal;font-size:13px;font-weight:800;opacity:.9}
.tile.w{background:linear-gradient(160deg,#22c55e,#15803d)}.tile.d{background:linear-gradient(160deg,#64748b,#3f4a5c)}.tile.l{background:linear-gradient(160deg,#ef4444,#a51d1d)}
.subt{grid-column:1/-1;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.subt div{background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:9px 12px}
.subt b{display:block;font-size:21px;font-weight:850;font-variant-numeric:tabular-nums}.subt b.pos{color:var(--wt)}.subt b.neg{color:var(--lt)}
.subt i{font-style:normal;font-size:11.5px;color:rgba(255,255,255,.6)}
.comps{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:10px}
.comp{background:rgba(6,9,16,.5);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.1);color:var(--ink);border-radius:14px;padding:11px 13px;display:flex;gap:12px;align-items:center;transition:border-color .15s,transform .15s}
.comp:hover{border-color:rgba(245,196,81,.5);transform:translateY(-1px)}
.comp .rb{min-width:76px;text-align:center;font-size:22px;font-weight:900;border-radius:11px;padding:8px 6px;background:rgba(255,255,255,.08);color:#fff;line-height:1.1}
.comp .rb.top{background:linear-gradient(160deg,#ffd76a,#e0a92e);color:#14110a;box-shadow:0 6px 18px -6px rgba(245,196,81,.8)}.comp .rb.good{background:linear-gradient(160deg,#22c55e,#15803d);color:#fff}
.comp .rb small{display:block;font-size:10.5px;font-weight:700;opacity:.8;margin-top:2px}
.comp .cn{font-size:13.5px;font-weight:750;line-height:1.3}
.comp .cs{font-size:12.5px;color:var(--mute);margin-top:3px}
.comp .cs b{color:var(--ink)}

/* ---------- KPI ---------- */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-bottom:14px}
.kpi{position:relative;background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--line);border-radius:var(--r);padding:16px 16px 14px;overflow:hidden}
.kpi::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--acc),var(--gold))}
.kpi h3{margin:0 0 10px;font-size:15px;color:var(--ink);display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.kpi h3 small{font-weight:500;color:var(--mute);font-size:12px}
.kgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.kgrid div{background:rgba(255,255,255,.035);border:1px solid var(--line);border-radius:10px;padding:8px 9px}
.kgrid b{display:block;font-size:18px;font-weight:850;color:var(--ink);font-variant-numeric:tabular-nums;white-space:nowrap}
.kgrid i{font-style:normal;font-size:11px;color:var(--mute)}
.bar{display:flex;height:8px;border-radius:999px;overflow:hidden;margin:12px 0 4px;gap:2px}
.bar span:nth-child(1){background:var(--w)}.bar span:nth-child(2){background:var(--d)}.bar span:nth-child(3){background:var(--l)}
.hl{margin:10px 0 0;padding:0;list-style:none;font-size:12.5px;color:var(--ink2)}
.hl li{padding:3px 0}.hl li::before{content:"★ ";color:var(--gold)}

/* ---------- chart ---------- */
.chartbox{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;margin-bottom:14px;position:relative}
.chartbox h4{margin:0 0 6px;font-size:14px;color:var(--ink)}
.chartbox svg{color:var(--mute);overflow:visible}
.chartbox svg .domain{stroke:var(--line2)}
.legend{font-size:12px;color:var(--mute);display:flex;gap:16px;flex-wrap:wrap}
.legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:-1px}
.tip{position:absolute;pointer-events:none;background:rgba(5,8,14,.92);border:1px solid var(--line2);color:#fff;font-size:12px;padding:7px 10px;border-radius:8px;white-space:nowrap;display:none;z-index:5;box-shadow:0 10px 30px rgba(0,0,0,.5)}

/* ---------- tables ---------- */
.tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:14px}
.tbox{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:auto;max-height:720px}
.tbox h4{margin:0;padding:12px 14px;font-size:14px;color:#fff;background:linear-gradient(90deg,var(--navy2),var(--navy));position:sticky;left:0;top:0;z-index:2}
table{border-collapse:collapse;width:100%;font-size:12.5px;font-variant-numeric:tabular-nums}
th,td{padding:6px 7px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}
th{background:var(--card2);color:var(--mute);font-weight:700;font-size:11.5px;letter-spacing:.02em;position:sticky;top:0;z-index:1}
.tbox th{top:45px}
tbody tr:hover td{background:rgba(255,255,255,.03)}
td.n{text-align:left;white-space:normal;min-width:150px;color:var(--ink2)}
tr.yr td{background:rgba(255,255,255,.04);font-weight:800;border-top:1px solid var(--line2);color:var(--ink)}
tr.yr td.y{color:var(--ink);font-size:13.5px}
.tag{display:inline-block;font-size:10.5px;padding:1px 6px;border-radius:4px;margin-right:5px;font-weight:800;vertical-align:1px}
.tag.L{background:color-mix(in srgb,var(--acc) 18%,transparent);color:color-mix(in srgb,var(--acc) 60%,#fff)}.tag.C{background:rgba(245,196,81,.15);color:var(--gold)}
.res{font-weight:700}
.res.top{color:#14110a;background:var(--gold);border-radius:5px;padding:1px 7px}
.res.good{color:var(--wt)}
.pos{color:var(--wt)}.neg{color:var(--lt)}
.wr{font-weight:800}
tr.yr.y26r td{background:rgba(245,196,81,.12);border-top:2px solid var(--gold);font-size:14px;color:#fff}
tr.yr.y26r td.y::before{content:"★ ";color:var(--gold)}
tr.c26 td{background:rgba(245,196,81,.035)}
tr.c26 td.n{box-shadow:inset 3px 0 0 var(--gold)}
.note{font-size:11.5px;color:var(--mute);margin-top:16px;line-height:1.7;padding:12px 14px;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.02)}

/* ---------- hub ---------- */
#hub{display:none}body:not(.detail) #hub{display:block}body:not(.detail) #main{display:none}
.hub-intro{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin:6px 0 18px}
.hub-intro h2{margin:0;font-size:24px;font-weight:850;letter-spacing:-.5px;color:var(--ink)}.hub-intro span{color:var(--mute);font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:18px;margin-bottom:22px}
.club{position:relative;background:var(--card);border:1px solid var(--line);border-radius:22px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;
 transition:transform .2s cubic-bezier(.2,.8,.2,1),box-shadow .2s,border-color .2s;animation:rise .4s ease both}
.club:nth-child(2){animation-delay:.06s}.club:nth-child(3){animation-delay:.12s}.club:nth-child(4){animation-delay:.18s}
.club:hover{transform:translateY(-5px);border-color:color-mix(in srgb,var(--acc) 55%,transparent);box-shadow:0 24px 50px -20px color-mix(in srgb,var(--acc) 55%,transparent),0 10px 30px -10px rgba(0,0,0,.6)}
.club:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.chead{position:relative;overflow:hidden;overflow:clip;color:#fff;padding:20px 18px;display:flex;align-items:center;gap:14px}
.chead::after{content:"";position:absolute;right:-50px;top:-60px;width:190px;height:190px;border-radius:50%;border:28px solid rgba(255,255,255,.06);pointer-events:none}
.crest{width:52px;height:52px;border-radius:50%;background:rgba(0,0,0,.25);border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:13px;flex:none;box-shadow:0 0 0 4px rgba(245,196,81,.12)}
.chead h3{margin:0;font-size:21px;font-weight:850;letter-spacing:-.4px}.chead small{display:block;color:rgba(255,255,255,.7);font-size:12px;margin-top:3px}
.chead .go{position:relative;z-index:1;margin-left:auto;background:var(--gold);color:#14110a;font-weight:850;font-size:12.5px;padding:7px 13px;border-radius:999px;white-space:nowrap;transition:transform .2s}
.club:hover .go{transform:translateX(3px)}
.cstats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:16px 18px 6px}
.cstats div{background:rgba(255,255,255,.035);border:1px solid var(--line);border-radius:12px;padding:9px 11px}
.cstats b{display:block;font-size:20px;white-space:nowrap;font-weight:850;color:var(--ink);font-variant-numeric:tabular-nums}.cstats b.y{color:var(--gold)}
.cstats i{font-style:normal;font-size:11px;color:var(--mute)}
.ages{padding:6px 18px 4px}
.age{display:grid;grid-template-columns:56px 104px 1fr 44px;gap:10px;align-items:center;padding:7px 0;border-bottom:1px solid var(--line);font-size:13px}
.age:last-child{border-bottom:0}
.age .an{font-weight:850;color:var(--ink)}.age .an small{display:block;font-weight:500;color:var(--mute);font-size:10.5px}
.age .wdl{font-variant-numeric:tabular-nums;color:var(--ink2)}
.age .wr{font-weight:850;text-align:right;font-variant-numeric:tabular-nums}
.mbar{height:8px;border-radius:999px;background:rgba(255,255,255,.06);overflow:hidden;position:relative}
.mbar span{position:absolute;inset:0 auto 0 0;border-radius:999px;box-shadow:0 0 12px currentColor}
.mbar em{position:absolute;top:0;bottom:0;width:1px;background:rgba(255,255,255,.35);left:50%}
.hon{padding:10px 18px 18px;margin-top:auto}
.hon h4{margin:6px 0 8px;font-size:11.5px;letter-spacing:.06em;color:var(--mute);font-weight:800}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12px;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--ink2);font-weight:650}
.chip.top{background:rgba(245,196,81,.14);border-color:rgba(245,196,81,.45);color:var(--gold)}
.cmp{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:auto;margin-bottom:16px}
.cmp h4{margin:0;padding:14px 16px;font-size:14.5px;color:var(--ink);border-bottom:1px solid var(--line)}
.cmp table td,.cmp table th{padding:9px 10px}
.cmp td:first-child{font-weight:850;color:var(--ink)}
.cmp td{color:var(--ink2)}
.cmp td.best{font-weight:850;background:rgba(245,196,81,.12);color:var(--gold)}
.soon{border:2px dashed var(--line2);border-radius:22px;display:flex;align-items:center;justify-content:center;color:var(--mute);font-size:14px;min-height:160px;text-align:center;padding:20px;background:rgba(255,255,255,.015)}

@media (max-width:640px){
 header{padding:22px 16px 14px}main,.hubwrap{padding:16px}
 .y26{padding:18px;border-radius:20px}.y26top{grid-template-columns:1fr;justify-items:center}.tiles,.subt{width:100%}.subt{grid-template-columns:repeat(2,1fr)}.comps{grid-template-columns:1fr}.tile b{font-size:34px}.y26h .delta{margin-left:0}
 .sh-head .src{display:none}.sh-head h2{white-space:nowrap;font-size:21px}.tables{grid-template-columns:1fr}.kgrid{grid-template-columns:repeat(2,1fr)}.kgrid b{font-size:16px}
 .cards{grid-template-columns:1fr}.cstats{grid-template-columns:repeat(2,1fr)}.age{grid-template-columns:50px 80px 1fr 40px;font-size:12.5px;gap:8px}.chead .go{display:none}
 nav button{padding:7px 12px;font-size:12.5px}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media print{
 :root{--bg:#fff;--card:#fff;--card2:#f1f3f7;--ink:#1b1f2a;--ink2:#333a48;--mute:#6b7385;--line:#e3e6ee;--line2:#cfd4de;--wt:#1f7a43;--lt:#b4332a}
 @page{size:A4 portrait;margin:8mm}
 html,body{background:#fff}body{font-size:10px}
 header,.noprint{display:none}
 main{padding:0;max-width:none}
 .sheet{display:block!important;page-break-after:always;zoom:.62;animation:none}
 .sheet:last-child{page-break-after:auto}
 .tables{grid-template-columns:1fr 1fr}
 .tbox{overflow:visible;max-height:none;break-inside:avoid}
 th,.tbox h4{position:static}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}

/* ---------- 승률 색 (비교표) ---------- */
.wrp{display:inline-block;min-width:48px;padding:2px 9px;border-radius:999px;font-weight:850;font-variant-numeric:tabular-nums;margin-right:4px;border:1px solid transparent}
.wrp.hi{background:rgba(34,197,94,.15);border-color:rgba(34,197,94,.35);color:#4ade80}
.wrp.mid{background:rgba(245,196,81,.13);border-color:rgba(245,196,81,.35);color:#f5c451}
.wrp.lo{background:rgba(239,68,68,.14);border-color:rgba(239,68,68,.35);color:#f87171}
.cmp td.hi{box-shadow:inset 3px 0 0 #22c55e}.cmp td.mid{box-shadow:inset 3px 0 0 #f5c451}.cmp td.lo{box-shadow:inset 3px 0 0 #ef4444}
.cmp td.best{background:linear-gradient(90deg,rgba(245,196,81,.16),rgba(245,196,81,.04));color:var(--ink)}
.cmp td.best::before{content:"👑 ";}
.cmp .cum{color:var(--mute);font-size:11.5px}
.cmp .leg{display:flex;gap:12px;flex-wrap:wrap;padding:8px 16px 12px;font-size:11.5px;color:var(--mute)}

/* ---------- 팀별 최고 시즌 ---------- */
tr.yr.best td{background:linear-gradient(90deg,rgba(34,197,94,.16),rgba(34,197,94,.03));border-top:2px solid #22c55e}
tr.yr.y26r.best td{background:linear-gradient(90deg,rgba(245,196,81,.2),rgba(34,197,94,.1))}
tr.yr.best td.y::after{content:"🏆 최고 시즌";display:inline-block;margin-left:8px;font-size:10.5px;font-weight:850;padding:1px 8px;border-radius:999px;background:#22c55e;color:#052e16;vertical-align:1px}
.bestsz{display:flex;align-items:center;gap:10px;margin-top:10px;padding:9px 12px;border-radius:12px;background:linear-gradient(90deg,rgba(34,197,94,.14),rgba(34,197,94,.02));border:1px solid rgba(34,197,94,.3);font-size:12.5px;color:var(--ink2)}
.bestsz b{color:#4ade80;font-size:15px;font-weight:900;font-variant-numeric:tabular-nums}
.bestsz .bt{font-size:10.5px;font-weight:850;padding:2px 8px;border-radius:999px;background:#22c55e;color:#052e16;white-space:nowrap}
@media print{tr.yr.best td.y::after{background:#1f7a43;color:#fff}}
"""

# 1) CSS 블록 교체
start = html.index("<style>") + len("<style>")
end = html.index("</style><script>// https://d3js")
html = html[:start] + CSS + html[end:]

# 2) 폰트
if FONT.strip() not in html:
    html = html.replace("<style>", FONT + "<style>", 1)

# 3) JS 색상 패치 (다크 배경용)
JS = [
    # 구단별 포인트 색
    ("const $=(t,c,txt)=>",
     "const ACC={eland:'#5b8cff',fcseoul:'#ff4a55',seongnam:'#9fb0c4'};for(const k in CLUBS)CLUBS[k].accent=ACC[k]||'#5b8cff';\nconst $=(t,c,txt)=>"),
    ("r.setProperty('--grad',C.grad);", "r.setProperty('--grad',C.grad);r.setProperty('--acc',C.accent);"),
    ("r.removeProperty('--navy2');", "r.removeProperty('--navy2');r.removeProperty('--acc');"),
    ("card.tabIndex=0;", "card.tabIndex=0;card.style.setProperty('--acc',C.accent);"),
    # 차트
    ("const cols=[CLUBS[CK].c2,'#c9a24a'];", "const cols=[CLUBS[CK].accent,'#f5c451'];"),
    ("g.selectAll('line').attr('stroke','#e3e6ee')", "g.selectAll('line').attr('stroke','rgba(255,255,255,.06)')"),
    (".attr('fill','#fff3cf');", ".attr('fill','rgba(245,196,81,.13)').attr('rx',8);"),
    (".attr('fill','#8a6a1f').text('2026')", ".attr('fill','#f5c451').text('2026')"),
    (".attr('stroke','#b9bfcc').attr('stroke-dasharray','4 3')", ".attr('stroke','rgba(255,255,255,.22)').attr('stroke-dasharray','4 4')"),
    (".attr('stroke',cols[i]).attr('stroke-width',2.5)", ".attr('stroke',cols[i]).attr('stroke-width',3).attr('stroke-linejoin','round').attr('stroke-linecap','round').style('filter',`drop-shadow(0 0 6px ${cols[i]}88)`)"),
    (".attr('fill',cols[i]).attr('stroke','#fff').attr('stroke-width',1.5)", ".attr('fill',cols[i]).attr('stroke','#111827').attr('stroke-width',2)"),
    ("sub.style.cssText='font-size:10.5px;color:#8a90a0'", "sub.style.cssText='font-size:10.5px;color:#6f7a90'"),
    # 허브 막대
    ("sp.style.background=wr>=60?'#2f7d4f':wr>=40?'#c9a24a':'#c0453a';",
     "sp.style.background=wr>=60?'#22c55e':wr>=40?'#f5c451':'#ef4444';sp.style.color=sp.style.background;"),
    ("w.style.color=wr>=60?'#2f7d4f':wr>=40?'#9a7413':'#c0453a';", "w.style.color=wr>=60?'#4ade80':wr>=40?'#f5c451':'#f87171';"),
    # 비교표: 승률 구간 색 (60%↑ 초록 / 40%↑ 금색 / 그 아래 빨강) + 누적 승률도 색
    ("vals.forEach(v=>{const td=$('td',v&&v.w===mx&&keys.length>1?'best':null,v?v.txt:'-');tr.appendChild(td)});",
     "vals.forEach(v=>{const td=$('td',v&&v.w===mx&&keys.length>1?'best':null);"
     "if(v&&v.w!=null){const g=wrCls(v.w);td.classList.add(g);const m=v.txt.match(/^\\d+% · (.*) \\((\\d+)%\\)$/);"
     "td.append($('span','wrp '+g,v.w+'%'),document.createTextNode(m?m[1]+' ':v.txt));if(m){const cu=$('span','cum','누적 ');cu.appendChild($('b',null,m[2]+'%'));cu.lastChild.style.color=wrCol(+m[2]);td.appendChild(cu)}}"
     "else td.textContent=v?v.txt:'-';tr.appendChild(td)});"),
    ("tb.appendChild(bd);box.appendChild(tb);H.appendChild(box);",
     "tb.appendChild(bd);box.appendChild(tb);const lg=$('div','leg');[['hi','60% 이상'],['mid','40~59%'],['lo','40% 미만']].forEach(([c,t])=>lg.appendChild($('span','wrp '+c,t)));lg.appendChild($('span',null,'👑 연령별 2026 최고 승률 구단'));box.appendChild(lg);H.appendChild(box);"),
    # 팀별 최고 시즌: 5경기 이상 시즌 중 승률 → 승 수 → 득실차 순
    ("const pct=(w,p)=>p?Math.round(w/p*100):0;",
     "const pct=(w,p)=>p?Math.round(w/p*100):0;\n"
     "const wrCls=w=>w>=60?'hi':w>=40?'mid':'lo',wrCol=w=>w>=60?'#4ade80':w>=40?'#f5c451':'#f87171';\n"
     "const bestYear=T=>{const c=T.years.filter(y=>y[1]>=5),L=c.length?c:T.years,k=y=>[pct(y[2],y[1]),y[2],y[5]-y[6]];"
     "return L.reduce((b,y)=>{const a=k(y),q=k(b);for(let i=0;i<3;i++)if(a[i]!==q[i])return a[i]>q[i]?y:b;return b})};"),
    ("teams.forEach(t=>{const T=D[t];const box=$('div','tbox');",
     "teams.forEach(t=>{const T=D[t];const BY=bestYear(T)[0];const box=$('div','tbox');"),
    ("const r=$('tr','yr'+(y[0]===2026?' y26r':''));",
     "const r=$('tr','yr'+(y[0]===2026?' y26r':'')+(y[0]===BY?' best':''));"),
    ("k.appendChild(bar);",
     "k.appendChild(bar);{const b=bestYear(T),bw=pct(b[2],b[1]);const bs=$('div','bestsz');bs.append($('span','bt','🏆 최고 시즌'),$('b',null,`${b[0]} · ${bw}%`),"
     "document.createTextNode(`${b[1]}경기 ${b[2]}승 ${b[3]}무 ${b[4]}패 · 득실 ${b[5]-b[6]>0?'+':''}${b[5]-b[6]}`));k.appendChild(bs)}"),
    # 차트: 최고 시즌 포인트 강조
    (".text(d=>d.wr);",
     ".text(d=>d.wr);\n  {const by=bestYear(D[t])[0],bp=pts.find(p=>p.yr===by);if(bp){const cx=x(bp.yr),cy=y(bp.wr);"
     "g.insert('circle',':first-child').attr('cx',cx).attr('cy',cy).attr('r',12).attr('fill','none').attr('stroke','#22c55e').attr('stroke-width',2).attr('stroke-dasharray','3 2');"
     "g.append('text').attr('x',cx).attr('y',i?cy+34:cy-24).attr('text-anchor','middle').attr('font-size','10.5px').attr('font-weight',850).attr('fill','#4ade80').text('🏆 최고')}}"),
]
for old, new in JS:
    if new in html:
        continue
    assert old in html, "패치 대상 없음: " + old[:60]
    html = html.replace(old, new, 1)

path.write_text(html, encoding="utf-8", newline="\n")
print("restyled:", path)
