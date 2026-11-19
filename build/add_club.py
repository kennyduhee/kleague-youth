# -*- coding: utf-8 -*-
"""넥스트플레이어에서 구단의 U11~U18 전 시즌 기록을 수집해 index.html 에 추가한다.

    python build/add_club.py <구단 키> [<구단 키> ...]     # 지정한 구단
    python build/add_club.py --new                         # 아직 대시보드에 없는 구단 전부

구단 설정(팀 ID·학교명·색)은 build/clubs_config.py.
시즌 계산 규칙은 update_data.season() 과 같다 (기존 구단 데이터와 대조해 검증).
같은 키의 구단이 이미 있으면 새로 수집한 기록으로 바꾼다. 구단 하나가 끝날 때마다 저장한다.
"""
import json, sys, pathlib, re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import update_data as U
from clubs_config import CLUBS as CONFIG

PATH = pathlib.Path(__file__).resolve().parent.parent / "index.html"
AGES = ["U11", "U12", "U14", "U15", "U17", "U18"]
LABEL = {"U11": "U11 (초5)", "U12": "U12 (초6)", "U14": "U14 (중2)", "U15": "U15 (중3)", "U17": "U17 (고2)", "U18": "U18 (고3)"}
GRADE = {"U11": "초5", "U12": "초6", "U14": "중2", "U15": "중3", "U17": "고2", "U18": "고3"}
LEVEL = {"U11": "초등부", "U12": "초등부", "U14": "중등부", "U15": "중등부", "U17": "고등부", "U18": "고등부"}
NOTE = ("※ 연도 합계는 넥스트플레이어 집계값, 대회별 행은 경기 결과를 대회 단위로 합산한 값입니다(일부 연도는 두 값이 다를 수 있습니다). "
        "리그 순위는 사이트의 \"리그 순위\" 기준, 대회 성적의 \"n조 m위\"는 조별리그 순위이며 두 개면 1차/2차 조별리그입니다. "
        "승부차기 경기는 무승부로 계산했습니다. 기록이 없는 연도는 표시되지 않습니다. {extra}2026 시즌은 진행 중일 수 있습니다.")


def pairs(school, ages):
    """{'U14':'광성중','U15':'광성중',...} → 'U14 · U15: 광성중 / U17 · U18: 대건고'"""
    out = []
    for s in dict.fromkeys(school[a] for a in ages if a in school):
        out.append((" · ".join(a for a in ages if school.get(a) == s), s))
    return out


def build_meta(cfg):
    ages = [a for a in AGES if a in cfg["teams"]]
    ps = pairs(cfg["school"], ages)
    feeder = " / ".join(f"{a}: {s}" for a, s in ps) if ps else f"{ages[0]}~{ages[-1]}: {cfg['name']} 유스"
    josa = lambda a: "은" if a[-1] in "178" else "는"   # U11·U17·U18 → 은, U12·U14·U15 → 는
    extra = "".join(f"{a.replace(' · ', '·')}{josa(a)} {s}, " for a, s in ps)
    extra = (extra[:-2] + " 기록입니다. ") if extra else ""
    missing = [a for a in AGES if a not in cfg["teams"]]
    if missing:
        extra += f"{'·'.join(missing)}{josa(missing[-1])} 넥스트플레이어에 팀이 없어 표시하지 않습니다. "
    sheets = [[a.lower(), a, f"{GRADE[a]} · {cfg['school'].get(a, LEVEL[a])}", [a]] for a in ages]
    return feeder, NOTE.format(extra=extra), sheets


def collect(tid, ag, this_year):
    graph = U.get("teamInfo", teamId=tid, ageGroup=ag, sYear=this_year).get("teamResultMapGraph") or []
    years = sorted({int(g["year"]) for g in graph if int(g.get("played") or 0) > 0})
    with ThreadPoolExecutor(3) as ex:
        seasons = list(ex.map(lambda y: U.season(tid, ag, y, None), years))
    return [s for s in seasons if s]


def save_club(key, club, accent):
    html = PATH.read_text(encoding="utf-8")
    i = html.index("const CLUBS=") + len("const CLUBS=")
    clubs, end = json.JSONDecoder().raw_decode(html, i)
    clubs[key] = club
    html = html[:i] + json.dumps(clubs, ensure_ascii=False) + html[end:]
    m = re.search(r"const ACC=\{([^}]*)\}", html)
    assert m, "ACC 맵 없음"
    acc = dict(re.findall(r"(\w+):'([^']*)'", m.group(1)))
    acc[key] = accent
    html = html[:m.start()] + "const ACC={" + ",".join(f"{k}:'{v}'" for k, v in acc.items()) + "}" + html[m.end():]
    PATH.write_text(html, encoding="utf-8", newline="\n")


def add(key):
    cfg = CONFIG[key]
    now = datetime.now(U.KST)
    D = {}
    for ag in [a for a in AGES if a in cfg["teams"]]:
        tid = cfg["teams"][ag]
        ys = collect(tid, ag, now.year)
        if ys:
            D[ag] = {"id": tid, "label": LABEL[ag], "years": ys}
        print(f"  {ag} {tid}: {len(ys)}시즌 {ys[0][0] if ys else '-'}~{ys[-1][0] if ys else '-'}, {sum(y[1] for y in ys)}경기", flush=True)
    feeder, note, sheets = build_meta(cfg)
    sheets = [s for s in sheets if s[1] in D]
    club = {"name": cfg["name"], "short": cfg["short"], "asof": now.strftime("%Y-%m-%d"),
            "c1": cfg["c1"], "c2": cfg["c2"], "grad": cfg["grad"], "feeder": feeder,
            "D": D, "sheets": sheets, "note": note}
    save_club(key, club, cfg["accent"])


def main():
    args = sys.argv[1:]
    if args == ["--new"]:
        html = PATH.read_text(encoding="utf-8")
        i = html.index("const CLUBS=") + len("const CLUBS=")
        have = json.JSONDecoder().raw_decode(html, i)[0]
        args = [k for k in CONFIG if k not in have]
    for n, key in enumerate(args, 1):
        print(f"[{n}/{len(args)}] {key} {CONFIG[key]['name']}", flush=True)
        add(key)
    print("done", flush=True)


if __name__ == "__main__":
    main()
