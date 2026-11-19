# -*- coding: utf-8 -*-
"""넥스트플레이어에서 한 구단의 U11~U18 전 시즌 기록을 수집해 index.html 에 추가한다.

    python build/add_club.py <구단 키> [index.html 경로]

구단 설정은 아래 CLUBS_NEW 에 적는다 (팀 ID 는 넥스트플레이어 클럽 페이지 주소
https://mobile.nextplayer.co.kr/club/<팀 ID>?ageGroup=U11 의 숫자).
시즌 계산 규칙은 update_data.season() 과 같다 (기존 구단 데이터와 대조해 검증).
이미 같은 키의 구단이 있으면 새로 수집한 기록으로 바꾼다.
"""
import json, sys, pathlib, re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import update_data as U

LABEL = {"U11": "U11 (초5)", "U12": "U12 (초6)", "U14": "U14 (중2)", "U15": "U15 (중3)", "U17": "U17 (고2)", "U18": "U18 (고3)"}
NOTE = ("※ 연도 합계는 넥스트플레이어 집계값, 대회별 행은 경기 결과를 대회 단위로 합산한 값입니다(일부 연도는 두 값이 다를 수 있습니다). "
        "리그 순위는 사이트의 \"리그 순위\" 기준, 대회 성적의 \"n조 m위\"는 조별리그 순위이며 두 개면 1차/2차 조별리그입니다. "
        "승부차기 경기는 무승부로 계산했습니다. 기록이 없는 연도는 표시되지 않습니다. {extra}2026 시즌은 진행 중일 수 있습니다.")

CLUBS_NEW = {
    "suwon": {
        "name": "수원삼성", "short": "수원", "accent": "#4cc3ff",
        "c1": "#0a2357", "c2": "#1b4ea3", "grad": "linear-gradient(140deg,#071a40 0%,#123c86 55%,#1f5fc4 100%)",
        "feeder": "U14 · U15: 매탄중 / U17 · U18: 매탄고",
        "teams": {"U11": 5865, "U12": 2537, "U14": 7582, "U15": 3151, "U17": 4818, "U18": 3596},
        "sub": {"U11": "초5 · 초등부", "U12": "초6 · 초등부", "U14": "중2 · 매탄중", "U15": "중3 · 매탄중", "U17": "고2 · 매탄고", "U18": "고3 · 매탄고"},
        "extra": "U14·U15는 수원삼성블루윙즈 U15(매탄중), U17·U18은 매탄고 기록입니다. ",
    },
}


def collect(tid, ag, this_year):
    graph = U.get("teamInfo", teamId=tid, ageGroup=ag, sYear=this_year).get("teamResultMapGraph") or []
    years = sorted({int(g["year"]) for g in graph if int(g.get("played") or 0) > 0})
    with ThreadPoolExecutor(4) as ex:
        seasons = list(ex.map(lambda y: U.season(tid, ag, y, None), years))
    return [s for s in seasons if s]


def main():
    key = sys.argv[1]
    path = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(__file__).resolve().parent.parent / "index.html")
    cfg = CLUBS_NEW[key]
    now = datetime.now(U.KST)
    D = {}
    for ag, tid in cfg["teams"].items():
        ys = collect(tid, ag, now.year)
        D[ag] = {"id": tid, "label": LABEL[ag], "years": ys}
        print(f"{ag} {tid}: {len(ys)}시즌 {ys[0][0] if ys else '-'}~{ys[-1][0] if ys else '-'}, {sum(y[1] for y in ys)}경기")
    club = {"name": cfg["name"], "short": cfg["short"], "asof": now.strftime("%Y-%m-%d"),
            "c1": cfg["c1"], "c2": cfg["c2"], "grad": cfg["grad"], "feeder": cfg["feeder"],
            "D": D, "sheets": [[ag.lower(), ag, cfg["sub"][ag], [ag]] for ag in cfg["teams"]],
            "note": NOTE.format(extra=cfg["extra"])}

    html = path.read_text(encoding="utf-8")
    i = html.index("const CLUBS=") + len("const CLUBS=")
    clubs, end = json.JSONDecoder().raw_decode(html, i)
    clubs[key] = club
    html = html[:i] + json.dumps(clubs, ensure_ascii=False) + html[end:]
    # 차트·카드 포인트 색 (ACC 맵)
    m = re.search(r"const ACC=\{([^}]*)\}", html)
    assert m, "ACC 맵 없음"
    acc = dict(re.findall(r"(\w+):'([^']*)'", m.group(1)))
    acc[key] = cfg["accent"]
    html = html[:m.start()] + "const ACC={" + ",".join(f"{k}:'{v}'" for k, v in acc.items()) + "}" + html[m.end():]
    path.write_text(html, encoding="utf-8", newline="\n")
    print("added", key, "->", path)


if __name__ == "__main__":
    main()
