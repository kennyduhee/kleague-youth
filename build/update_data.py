# -*- coding: utf-8 -*-
"""넥스트플레이어에서 올해 시즌 기록을 다시 불러와 index.html 의 데이터를 갱신한다.

업데이트를 요청할 때 실행한다:  python build/update_data.py [index.html 경로]
실행하면 헤더의 '최종 업데이트' 표기(NP_UPDATED)도 실행 시각(KST)으로 바뀐다.

규칙 (기존 수집 데이터와 같은 방식, 18팀 대조로 검증):
  · 대회별 기록: teamInfo 의 전체 경기 목록을 리그/대회 id 별로 묶어 계산 (승부차기는 무승부)
  · 연도 합계: 넥스트플레이어 시즌 요약(teamResultMap)
  · 대회명: 이미 있던 대회(같은 구분·같은 시작일)는 다듬어 둔 기존 이름 유지, 새 대회는 API 이름
  · 성적: 대회 = teamInfoCup 결과, 리그 = 순위. 같은 성적이면 기존 표기 순서 유지
  · 지난 시즌 기록은 건드리지 않음. 한 팀이라도 불러오기에 실패하면 그 팀은 기존 기록 유지
"""
import json, re, sys, time, pathlib, functools, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

KST = timezone(timedelta(hours=9))
API = "https://mobile.nextplayer.co.kr/back_front/base_front/api/v1/"
path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "index.html")


def get(ep, **q):
    url = API + ep + "?" + urllib.parse.urlencode(q)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (kleague-youth weekly update)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                j = json.load(r)
            if j.get("state") != "SUCCESS":
                raise RuntimeError(j.get("msg") or "API error")
            return j.get("data") or {}
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


@functools.lru_cache(maxsize=None)
def season_list(ep, ag, yr):
    try:
        return get(ep, sYear=yr, ageGroup=ag)
    except Exception:
        return {}


def np_name(ty, raw):
    m = re.match(r"^\[([^\]]+)\]\s*(.*)$", str(raw))
    br, rest = (m.group(1), m.group(2).strip()) if m else ("", str(raw).strip())
    rest = re.sub(r"^20\d\d\s+", "", rest)
    br = re.sub(r"^U1\d_", "", br)
    return f"{rest}({br.split('/')[-1].strip()})" if ty == "C" else f"{rest} [{br}]"


d8 = lambda s: re.sub(r"\D", "", str(s))[:8] if s else ""
md = lambda s: f"{s[4:6]}.{s[6:8]}" if s else ""
per = lambda a, b: f"{md(a or b)}~{md(b or a)}" if (a or b) else ""


def sort_res(parts):
    key = lambda s: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]
    return "/".join(sorted(parts, key=key))


def season(tid, ag, yr, old):
    sid = str(tid)
    inf = get("teamInfo", teamId=tid, ageGroup=ag, sYear=yr)
    cup = get("teamInfoCup", teamId=tid, ageGroup=ag, sYear=yr)
    lg = get("teamInfoLeague", teamId=tid, ageGroup=ag, sYear=yr)
    LL, CL = season_list("league", ag, yr), season_list("cup", ag, yr)
    LN, CN, CR, LR = {}, {}, {}, {}
    for x in LL.get("totalleagueList") or []:
        LN[str(x["league_id"])] = x["league_name"]
    for x in CL.get("totalCupList") or []:
        CN[str(x["cup_id"])] = x["cup_name"]
    for x in (cup.get("teamCupMatchList") or []) + (cup.get("teamCupResultList") or []):
        if x.get("cup_id") is not None and x.get("cup_name"):
            CN.setdefault(str(x["cup_id"]), x["cup_name"])
    for x in cup.get("teamCupResultList") or []:
        if x.get("result"):
            a = CR.setdefault(str(x["cup_id"]), [])
            if x["result"] not in a:
                a.append(x["result"])
    for x in lg.get("teamLeagueEnterList") or []:
        if str(x.get("team_id")) == sid:
            LN.setdefault(str(x["league_id"]), x["league_name"])
            if x.get("rank"):
                LR[str(x["league_id"])] = f"{x['rank']}위"
    rank_by_name = {x["league_name"]: f"{x['rank']}위" for x in lg.get("teamLeagueRankList") or []
                    if str(x.get("play_year")) == str(yr) and x.get("rank")}

    groups = {}
    for m in inf.get("teamTotalMatchList") or []:
        home = str(m.get("home_id")) == sid
        if not home and str(m.get("away_id")) != sid:
            continue
        if m.get("home_score") is None or m.get("away_score") is None:
            continue
        ty = "L" if int(m.get("total_type") or 0) == 1 else "C"
        g = groups.setdefault(ty + str(m["league_id"]), {"ty": ty, "id": str(m["league_id"]), "m": []})
        hs, as_ = int(m["home_score"]), int(m["away_score"])
        g["m"].append((hs if home else as_, as_ if home else hs, d8(m.get("pdate"))))

    oc = old[7] if old else []
    comps = []
    for g in groups.values():
        ms, ty = g["m"], g["ty"]
        ds = sorted(d for *_, d in ms if d)
        w = sum(a > b for a, b, _ in ms)
        dr = sum(a == b for a, b, _ in ms)
        raw = (LN if ty == "L" else CN).get(g["id"])
        res = (LR.get(g["id"]) or rank_by_name.get(raw)) if ty == "L" else (sort_res(CR[g["id"]]) if g["id"] in CR else None)
        start = md(ds[0]) if ds else ""
        prev = next((o for o in oc if o[0] == ty and o[9].split("~")[0] == start), None)
        name = prev[1] if prev else (np_name(ty, raw) if raw else f"{'리그' if ty == 'L' else '대회'} #{g['id']}")
        if prev and res and sort_res(prev[2].split("/")) == sort_res(res.split("/")):
            res = prev[2]
        comps.append((ds[0] if ds else "", [ty, name, res or (prev[2] if prev else "-"), len(ms), w, dr, len(ms) - w - dr,
                                          sum(a for a, _, _ in ms), sum(b for _, b, _ in ms), per(ds[0] if ds else "", ds[-1] if ds else "")]))
    if not comps:
        return None
    comps.sort(key=lambda x: x[0])
    cs = [c for _, c in comps]
    R = inf.get("teamResultMap") or {}
    if R and int(R.get("played") or 0) > 0:
        tot = [int(R[k]) for k in ("played", "won", "draw", "lost", "gf", "ga")]
    else:
        tot = [sum(c[i] for c in cs) for i in range(3, 9)]
    return [yr, *tot, cs]


def main():
    html = path.read_text(encoding="utf-8")
    i = html.index("const CLUBS=") + len("const CLUBS=")
    clubs, end = json.JSONDecoder().raw_decode(html, i)
    now = datetime.now(KST)
    yr = now.year
    jobs = [(ck, ag, T) for ck, C in clubs.items() for ag, T in C["D"].items()]

    def run(job):
        ck, ag, T = job
        old = next((y for y in T["years"] if y[0] == yr), None)
        try:
            return job, season(T["id"], ag, yr, old), None
        except Exception as e:
            return job, None, e

    with ThreadPoolExecutor(4) as ex:
        results = list(ex.map(run, jobs))

    changed, failed, ok_clubs = [], [], set()
    for (ck, ag, T), y, err in results:
        if err is not None:
            failed.append(f"{ck} {ag}: {err}")
            continue
        ok_clubs.add(ck)
        if y is None:
            continue
        idx = next((k for k, v in enumerate(T["years"]) if v[0] == yr), None)
        if idx is None:
            T["years"].append(y)
            T["years"].sort(key=lambda v: v[0])
            changed.append(f"{ck} {ag} (새 시즌)")
        elif T["years"][idx] != y:
            T["years"][idx] = y
            changed.append(f"{ck} {ag}")

    if len(failed) == len(jobs):
        print("모든 팀 불러오기 실패 — 변경하지 않음", *failed, sep="\n  ")
        sys.exit(1)
    for ck in ok_clubs:
        clubs[ck]["asof"] = now.strftime("%Y-%m-%d")

    html = html[:i] + json.dumps(clubs, ensure_ascii=False) + html[end:]
    stamp = now.strftime("%Y-%m-%d %H:%M")
    html, n = re.subn(r"const NP_UPDATED='[^']*';", f"const NP_UPDATED='{stamp}';", html)
    path.write_text(html, encoding="utf-8", newline="\n")
    print(f"{stamp} KST · {len(jobs) - len(failed)}/{len(jobs)}팀 확인 · 변경 {len(changed)}팀")
    for c in changed:
        print("  변경:", c)
    for f in failed:
        print("  실패:", f)


if __name__ == "__main__":
    main()
