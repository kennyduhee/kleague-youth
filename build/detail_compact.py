# -*- coding: utf-8 -*-
"""구단 상세 화면(연령별 성적표) 위아래 간격 압축.

  · 2026 시즌 카드: 승률 원 · 승/무/패 · 경기/득점/실점/득실차를 한 줄에 배치 (데스크톱)
  · 대회 카드·누적 KPI·제목 여백을 줄이고 글자 크기는 읽기 좋은 수준 유지
  · 모바일(640px 이하)은 기존 세로 배치 유지, 여백만 축소

hub_compare.py 다음에 실행:  python build/detail_compact.py [index.html 경로]
"""
import sys, pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html")
html = path.read_text(encoding="utf-8")
MARK = "/*detail-compact*/"
if MARK in html:
    print("already applied:", path); sys.exit(0)

CSS = MARK + r"""
.sh-head{margin:0 0 10px;padding-bottom:7px}.sh-head h2{font-size:22px}
.y26{padding:14px 16px;margin-bottom:12px;border-radius:18px}
.y26h{margin-bottom:10px;gap:10px}
.y26h .badge{font-size:16px;padding:2px 10px;border-radius:8px}
.y26h .ttl{font-size:18px}
.y26h .delta{font-size:12.5px;padding:4px 11px}
.y26top{gap:10px;margin-bottom:10px}
.tile{padding:6px 6px;border-radius:12px}.tile b{font-size:30px;line-height:1.05}.tile i{font-size:12px}
.subt{gap:8px}.subt div{padding:6px 10px;border-radius:10px}.subt b{font-size:19px;line-height:1.2}.subt i{font-size:11px}
.comps{grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:8px}
.comp{padding:7px 10px;gap:10px;border-radius:12px}
.comp .rb{font-size:18px;padding:5px 8px;min-width:64px;border-radius:9px;white-space:nowrap;flex:none}
.comp .rb small{font-size:10px;margin-top:1px}
.comp .cn{font-size:13px;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.comp>div:last-child{min-width:0}
.comp .cs{font-size:12px;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kpis{gap:10px;margin-bottom:10px}
.kpi{padding:11px 13px 10px}
.kpi h3{margin:0 0 7px;font-size:14.5px}
.kgrid{gap:6px}.kgrid div{padding:5px 9px}.kgrid b{font-size:17px;line-height:1.2}
.kpi>*+*{margin-top:7px}
.kpi ul{margin-top:6px}
.chartbox{padding:10px 14px;margin-bottom:10px}
.chartbox h4{margin:0 0 4px}
@media (min-width:641px){
 .y26top{grid-template-columns:auto minmax(0,1.05fr) minmax(0,1fr);align-items:stretch}
 .ring{zoom:.74;align-self:center}
 .subt{grid-column:auto;grid-template-columns:repeat(4,1fr)}
 .subt div{display:flex;flex-direction:column;justify-content:center}
}
@media (max-width:640px){.comps{grid-template-columns:1fr}.comp .cn{white-space:normal}}
"""
anchor = "</style><script>// https://d3js"
assert html.count(anchor) == 1
html = html.replace(anchor, CSS + anchor, 1)
path.write_text(html, encoding="utf-8", newline="\n")
print("detail compact applied:", path)
