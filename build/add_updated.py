# -*- coding: utf-8 -*-
"""헤더 오른쪽에 '최종 업데이트' 표기 추가.

표기 값은 index.html 안의 NP_UPDATED 상수이고, build/update_data.py 로
데이터를 갱신할 때 그 시각(KST)으로 바뀐다.

restyle.py 다음에 실행:  python build/add_updated.py [index.html 경로] [초기값]
"""
import sys, pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html")
initial = sys.argv[2] if len(sys.argv) > 2 else ""
html = path.read_text(encoding="utf-8")
MARK = "/*np-updated*/"
if MARK in html:
    print("already has updated label:", path); sys.exit(0)

CSS = MARK + r"""
.upd{margin-left:auto;display:inline-flex;align-items:center;gap:7px;border:1px solid rgba(245,196,81,.4);background:rgba(245,196,81,.08);color:rgba(255,255,255,.75);
 border-radius:999px;padding:7px 14px;font-size:12.5px;font-weight:600;white-space:nowrap}
.upd b{color:var(--gold);font-weight:800;font-variant-numeric:tabular-nums}
.upd:empty,.upd.none{display:none}
@media (max-width:640px){.upd{padding:6px 11px;font-size:11.5px}}
"""
HTML_OLD = '<h1 id="ttl">K리그 유스 성적 대시보드</h1></div>'
HTML_NEW = '<h1 id="ttl">K리그 유스 성적 대시보드</h1><span class="upd" id="upd">최종 업데이트 <b id="updv"></b></span></div>'
JS = ("const NP_UPDATED='" + initial + "';\n"
      "document.getElementById('updv').textContent=NP_UPDATED;if(!NP_UPDATED)document.getElementById('upd').classList.add('none');\n")
CALL = "renderHub();route();window.addEventListener('hashchange',route);"

for old in ("</style><script>// https://d3js", HTML_OLD, CALL):
    assert html.count(old) == 1, "패치 대상 없음/중복: " + old[:50]
html = html.replace("</style><script>// https://d3js", CSS + "</style><script>// https://d3js", 1)
html = html.replace(HTML_OLD, HTML_NEW, 1)
html = html.replace(CALL, JS + CALL, 1)
path.write_text(html, encoding="utf-8", newline="\n")
print("added updated label:", path)
