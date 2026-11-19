# -*- coding: utf-8 -*-
"""허브를 구단이 많아도 보기 좋게 정리.

  · 승률 비교표를 '구단 = 행, 연령 = 열'로 전환 (구단 26개도 한 화면 폭에 들어감)
    칸: 2026 승률(색 배지) · 2026 승-무-패 · 누적 승률, 연령별 최고 승률 구단 👑
    구단명을 누르면 그 구단 상세로 이동
  · '다른 K리그 유스 구단 추가 예정' 카드 삭제
  · 비교표를 허브 맨 위(구단 카드 위)로 이동
  · 구단 카드 위아래 간격 압축 (글자 크기·색은 유지)

restyle.py → add_updated.py 다음에 실행:  python build/hub_compare.py [index.html 경로]
"""
import sys, pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html")
html = path.read_text(encoding="utf-8")
MARK = "/*hub-compare*/"
if MARK in html:
    print("already applied:", path); sys.exit(0)

SOON = "const soon=$('div','soon');soon.textContent='다른 K리그 유스 구단 추가 예정';cards.appendChild(soon);"

START = "const ages=['U11','U12','U14','U15','U17','U18'];const keys=Object.keys(CLUBS);"
END = "else td.textContent=v?v.txt:'-';tr.appendChild(td)});bd.appendChild(tr)}"
NEW = (MARK + "const ages=['U11','U12','U14','U15','U17','U18'];const keys=Object.keys(CLUBS);\n"
 "  const box=$('div','cmp');box.id='compare';box.appendChild($('h4',null,'구단별 2026 승률 비교 (가나다순 · 칸: 2026 승률 / 승-무-패 / 누적 승률)'));\n"
 "  const tb=$('table');const hr=$('tr');['구단',...ages].forEach(x=>hr.appendChild($('th',null,x)));const th=$('thead');th.appendChild(hr);tb.appendChild(th);\n"
 "  const bd=$('tbody');\n"
 "  const cell=(k,a)=>{const T=CLUBS[k].D[a];if(!T)return null;const y=T.years.find(v=>v[0]===2026);const s=sum(T.years);return {w:y?pct(y[2],y[1]):null,y,cum:pct(s.w,s.p)}};\n"
 "  const M={};for(const a of ages)M[a]=Math.max(...keys.map(k=>{const v=cell(k,a);return v&&v.w!=null?v.w:-1}));\n"
 "  for(const k of keys){const tr=$('tr');const n=$('td','cn');const ln=$('a',null,CLUBS[k].name);ln.href='#'+k;n.appendChild(ln);tr.appendChild(n);\n"
 "   for(const a of ages){const v=cell(k,a);const td=$('td',v&&v.w!=null&&v.w===M[a]&&keys.length>1?'best':null);\n"
 "    if(v&&v.w!=null){const g=wrCls(v.w);td.classList.add(g);td.appendChild($('span','wrp '+g,v.w+'%'));td.appendChild($('small','rec',`${v.y[2]}-${v.y[3]}-${v.y[4]}`));\n"
 "     const cu=$('span','cum','누적 ');cu.appendChild($('b',null,v.cum+'%'));cu.lastChild.style.color=wrCol(v.cum);td.appendChild(cu)}\n"
 "    else{td.textContent=v?'2026 기록 없음':'팀 없음';td.className='na'}tr.appendChild(td)}\n"
 "   bd.appendChild(tr)}")

CSS = MARK + r"""
.cmp table{min-width:760px}
.cmp td{vertical-align:middle;white-space:nowrap}
.cmp table td,.cmp table th{padding:8px 7px}.cmp td .wrp{min-width:42px;padding:2px 7px}
.cmp td.cn{text-align:left;white-space:nowrap;position:sticky;left:0;background:var(--card);z-index:1;box-shadow:inset -1px 0 0 var(--line)}
.cmp td.cn a{color:var(--ink);text-decoration:none;font-weight:850}.cmp td.cn a:hover{color:var(--gold);text-decoration:underline}
.cmp td .rec{display:inline;font-size:11.5px;color:var(--ink2);margin-left:6px;font-variant-numeric:tabular-nums}
.cmp td .cum{display:inline;font-size:11px;margin-left:6px;color:var(--mute)}
.cmp td.na{color:var(--mute);font-size:11px;opacity:.6}
.cmp tbody tr:hover td.cn{background:var(--card2)}
/*cmp-leg-right*/
.cmp h4{display:flex;align-items:center;flex-wrap:wrap;gap:8px 14px}
.cmp h4 .leg{margin-left:auto;padding:0;gap:8px;font-size:11.5px;font-weight:500;letter-spacing:0}
.cmp h4 .leg .wrp{min-width:0;padding:1px 8px;font-size:11px}
/*hub-compact*/
.cards{gap:12px;margin-bottom:16px}
.hub-intro{margin:4px 0 10px}
.chead{padding:11px 14px;gap:10px}
.chead::after{width:130px;height:130px;right:-40px;top:-50px;border-width:20px}
.crest{width:38px;height:38px;font-size:11.5px;box-shadow:0 0 0 3px rgba(245,196,81,.12)}
.chead h3{font-size:18px}.chead small{font-size:11.5px;margin-top:1px;line-height:1.35}
.chead .go{font-size:11.5px;padding:5px 10px}
.cstats{gap:6px;padding:10px 14px 4px}
.cstats div{padding:5px 8px;border-radius:9px}
.cstats b{font-size:17px;line-height:1.25}
.cstats i{font-size:10.5px;white-space:nowrap;line-height:1.2}
.ages{padding:2px 14px 0}
.age{padding:4px 0;gap:8px;font-size:12.5px;grid-template-columns:62px 100px 1fr 40px;min-height:0}
.age .an{line-height:1.2}.age .an small{display:inline;margin-left:4px;font-size:10px}
.mbar{height:6px}
.hon{padding:6px 14px 12px;margin-top:0}
.hon h4{margin:4px 0 5px;font-size:10.5px}
.chips{gap:4px}.chip{font-size:11.5px;padding:2px 8px}
@media (max-width:640px){.age{grid-template-columns:58px 78px 1fr 38px}}
"""

for old in (SOON, START, END, "</style><script>// https://d3js"):
    assert html.count(old) == 1, "패치 대상 없음/중복: " + old[:50]
html = html.replace(SOON, "", 1)
# 비교표를 허브 맨 위로
CMP_TOP_OLD = "lg.appendChild($('span',null,'👑 연령별 2026 최고 승률 구단'));box.appendChild(lg);H.appendChild(box);"
CMP_TOP_NEW = "lg.appendChild($('span',null,'👑 연령별 2026 최고 승률 구단'));box.firstChild.appendChild(lg);H.insertBefore(box,H.firstChild);"
assert html.count(CMP_TOP_OLD) == 1, '패치 대상 없음: 비교표 위치'
html = html.replace(CMP_TOP_OLD, CMP_TOP_NEW, 1)
s, e = html.index(START), html.index(END) + len(END)
html = html[:s] + NEW + html[e:]
html = html.replace("</style><script>// https://d3js", CSS + "</style><script>// https://d3js", 1)
path.write_text(html, encoding="utf-8", newline="\n")
print("hub compare applied:", path)
