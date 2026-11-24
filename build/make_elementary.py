# -*- coding: utf-8 -*-
"""초등부(U11·U12)만 담은 공유용 페이지 생성:  index.html → elementary/index.html

  · 데이터에서 U14·U15·U17·U18 기록을 아예 빼서 (페이지 소스에도 남지 않음)
  · 비교표·구단 카드·상세 탭·안내문·미리보기(og) 문구를 초등부 기준으로 변경
  · 주소: https://kleague-youth.vercel.app/elementary/

전체 페이지(index.html)를 고치거나 데이터를 업데이트한 뒤 다시 실행:
    python build/make_elementary.py
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "elementary" / "index.html"
KEEP = ("U11", "U12")
TITLE = "K리그 유스 초등부(U11·U12) 성적"


def rep(html, old, new, count=1):
    assert html.count(old) == count, f"패치 대상 {html.count(old)}개: {old[:60]}"
    return html.replace(old, new)


def main():
    html = SRC.read_text(encoding="utf-8")
    i = html.index("const CLUBS=") + len("const CLUBS=")
    clubs, end = json.JSONDecoder().raw_decode(html, i)
    for c in clubs.values():
        c["D"] = {a: t for a, t in c["D"].items() if a in KEEP}
        c["sheets"] = [s for s in c["sheets"] if any(a in KEEP for a in s[3])]
        ages = [a for a in KEEP if a in c["D"]]
        c["feeder"] = "초등부 " + " · ".join(f"{a} {'초5' if a == 'U11' else '초6'}" for a in ages)
        # 안내문: 중·고등부 이야기가 들어간 문장은 빼기
        parts = re.split(r"(?<=[.다])\s+", c["note"])
        c["note"] = " ".join(p for p in parts if not re.search(r"U1[4578]", p))
    assert all(c["D"] for c in clubs.values())
    html = html[:i] + json.dumps(clubs, ensure_ascii=False) + html[end:]

    n = len(clubs)
    desc = f"K리그 {n}개 구단 유스 초등부(U11·U12) 연도별·2026 시즌 성적을 한눈에 비교 · 출처: 넥스트플레이어"
    html = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"',
                  lambda m: m.group(1) + desc + '"', html)
    html = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*"',
                  lambda m: m.group(1) + TITLE + '"', html)
    html = rep(html, 'content="https://kleague-youth.vercel.app/"', 'content="https://kleague-youth.vercel.app/elementary/"')
    # 미리보기 이미지: elementary/og.png (초등부 문구로 만든 별도 이미지, 한 번 만들어 두면 됨)
    html = rep(html, 'content="https://kleague-youth.vercel.app/og.png"', 'content="https://kleague-youth.vercel.app/elementary/og.png"', 2)
    html = rep(html, "<title>K리그 유스 성적 대시보드</title>", f"<title>{TITLE}</title>")
    html = rep(html, '<h1 id="ttl">K리그 유스 성적 대시보드</h1>', f'<h1 id="ttl">{TITLE}</h1>')
    html = rep(html, "document.getElementById('ttl').textContent='K리그 유스 성적 대시보드';",
               f"document.getElementById('ttl').textContent='{TITLE}';")
    html = rep(html, "구단을 선택하면 U11~U18 연령별 상세 성적을 볼 수 있습니다", "구단을 선택하면 U11(초5)·U12(초6) 상세 성적을 볼 수 있습니다")
    html = rep(html, "`U11 · U12 · U14 · U15 · U17 · U18 | 출처", "`초등부 U11 · U12 | 출처")
    html = rep(html, "const ages=['U11','U12','U14','U15','U17','U18'];", "const ages=['U11','U12'];")
    html = rep(html, "'6장 모두 펼치기'", "`${SHEETS.length}장 모두 펼치기`", 2)
    # 연령이 2개뿐이라 비교표 폭 제한을 풀어 휴대폰에서도 가로 스크롤 없이
    css = ("/*elementary*/.cmp table{min-width:0}.cmp td .cum{margin-left:4px}\n"
           "@media (max-width:640px){.cmp table td,.cmp table th{padding:6px 5px}"
           ".cmp td:not(.cn){text-align:center;line-height:1.35}"
           ".cmp td .rec,.cmp td .cum{display:block;margin-left:0}"
           ".cmp td.cn a{font-size:12.5px;gap:5px}.cmp td.cn img.emb{width:18px;height:18px}"
           ".cmp h4 .leg{margin-left:0}}\n")
    html = rep(html, "</style><script>// https://d3js", css + "</style><script>// https://d3js")
    leftover = re.findall(r"U1[4578]", html[:i] + html[i + len(json.dumps(clubs, ensure_ascii=False)):])
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"elementary page: {OUT} ({len(html)//1024}KB), U14~U18 남은 표기 {len(leftover)}개")


if __name__ == "__main__":
    main()
