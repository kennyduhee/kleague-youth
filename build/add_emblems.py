# -*- coding: utf-8 -*-
"""구단 엠블럼(팀 마크)을 넥스트플레이어에서 받아 emblems/ 에 저장하고 대시보드에 표시한다.

  · 구단별로 소속 팀(U11~U18)들이 가장 많이 쓰는 엠블럼 하나를 고른다 (옛 엠블럼 등 예외 제외)
  · 이미지는 저장소의 emblems/<구단 키>.png 로 저장 (넥스트플레이어 서버에 직접 링크하지 않음)
  · CLUBS 데이터에 emblem 경로를 넣고, 비교표 구단명·구단 카드·상세 제목 앞에 표시
  · 엠블럼이 없는 구단은 기존처럼 글자 원형 표시

구단을 추가한 뒤 다시 실행하면 새 구단 엠블럼만 받아 온다:  python build/add_emblems.py
"""
import json, sys, pathlib, hashlib, collections, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import update_data as U

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATH = ROOT / "index.html"
OUT = ROOT / "emblems"
IMG = "https://mobile.nextplayer.co.kr/NP/"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kleague-youth dashboard)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def pick(key, club):
    """소속 팀 엠블럼 중 가장 많이 쓰이는 이미지 → (bytes, 확장자)"""
    def team_emblem(item):
        ag, T = item
        m = U.get("teamInfo", teamId=T["id"], ageGroup=ag, sYear=U.datetime.now(U.KST).year).get("teamInfoMap") or {}
        return m.get("emblem")
    with ThreadPoolExecutor(3) as ex:
        paths = [p for p in ex.map(team_emblem, club["D"].items()) if p]
    imgs = {p: fetch(IMG + p.lstrip("/")) for p in dict.fromkeys(paths)}
    count = collections.Counter(hashlib.sha1(imgs[p]).hexdigest() for p in paths)
    best = count.most_common(1)[0][0]
    p = next(p for p in paths if hashlib.sha1(imgs[p]).hexdigest() == best)
    ext = ".jpg" if p.lower().endswith((".jpg", ".jpeg")) else ".png"
    return imgs[p], ext


MARK = "/*club-emblems*/"
CSS = MARK + r"""
.crest.img{background:#fff;padding:3px;overflow:hidden}
.crest.img img{width:100%;height:100%;object-fit:contain;display:block}
.cmp td.cn a{display:inline-flex;align-items:center;gap:7px}
.cmp td.cn img.emb{width:20px;height:20px;object-fit:contain;flex:none;background:#fff;border-radius:50%;padding:1px}
#ttl{display:flex;align-items:center;gap:10px}
#ttl img.emb{width:34px;height:34px;object-fit:contain;background:#fff;border-radius:50%;padding:3px;flex:none}
@media (max-width:640px){#ttl img.emb{width:28px;height:28px}}
"""
JS = [
    # 구단 카드: 글자 원형 → 엠블럼
    ("const cr=$('div','crest',C.short.slice(0,3));",
     "const cr=$('div','crest',C.emblem?'':C.short.slice(0,3));if(C.emblem){cr.classList.add('img');const im=$('img');im.src=C.emblem;im.alt=C.name;im.loading='lazy';cr.appendChild(im)}"),
    # 비교표 구단명 앞
    ("const ln=$('a',null,CLUBS[k].name);ln.href='#'+k;",
     "const ln=$('a',null,CLUBS[k].name);ln.href='#'+k;if(CLUBS[k].emblem){const im=$('img','emb');im.src=CLUBS[k].emblem;im.alt='';im.loading='lazy';ln.prepend(im)}"),
    # 상세 화면 제목 앞
    ("document.getElementById('ttl').textContent=`${C.name} 유스 연도별 성적`;",
     "document.getElementById('ttl').textContent=`${C.name} 유스 연도별 성적`;if(C.emblem){const im=$('img','emb');im.src=C.emblem;im.alt='';document.getElementById('ttl').prepend(im)}"),
]


def main():
    html = PATH.read_text(encoding="utf-8")
    i = html.index("const CLUBS=") + len("const CLUBS=")
    clubs, end = json.JSONDecoder().raw_decode(html, i)
    OUT.mkdir(exist_ok=True)
    for key, club in clubs.items():
        if club.get("emblem") and (ROOT / club["emblem"]).exists():
            continue
        data, ext = pick(key, club)
        (OUT / f"{key}{ext}").write_bytes(data)
        club["emblem"] = f"emblems/{key}{ext}"
        print(f"{key}: {club['emblem']} ({len(data)} bytes)", flush=True)
    html = html[:i] + json.dumps(clubs, ensure_ascii=False) + html[end:]
    if MARK not in html:
        anchor = "</style><script>// https://d3js"
        assert html.count(anchor) == 1
        html = html.replace(anchor, CSS + anchor, 1)
    for old, new in JS:
        if new in html:
            continue
        assert html.count(old) == 1, "패치 대상 없음: " + old[:50]
        html = html.replace(old, new, 1)
    PATH.write_text(html, encoding="utf-8", newline="\n")
    print("emblems ok")


if __name__ == "__main__":
    main()
