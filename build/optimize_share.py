# -*- coding: utf-8 -*-
"""단톡방 대량 공유 대비 최적화 (여러 번 실행해도 결과가 같다).

  1) 엠블럼 경량화: emblems/<구단>.png → 96px WebP data URI 로 index.html 안에 포함
     (방문당 이미지 요청 27건 → 0건, 용량 약 600KB → 약 80KB)
  2) 카톡·SNS 미리보기 태그(og:*, twitter:*) 추가 + og.png(1200x630) 생성
  3) 캐시 설정은 저장소 루트 vercel.json 에서 관리 (이 스크립트는 건드리지 않음)
  4) Vercel Web Analytics 스크립트 추가
     (Vercel 대시보드 → 프로젝트 → Analytics → Enable 을 눌러야 집계가 시작됨)

구단 추가(add_club.py) · 엠블럼 추가(add_emblems.py) 뒤에 마지막으로 실행:
    python build/optimize_share.py            # index.html 갱신
    python build/optimize_share.py --og       # og.png 도 다시 생성 (playwright 필요)
"""
import base64, io, json, pathlib, re, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATH = ROOT / "index.html"
SITE = "https://kleague-youth.vercel.app"
SIZE = 96  # 화면 최대 52px × 레티나 2배


def webp_uri(png: pathlib.Path) -> str:
    im = Image.open(png).convert("RGBA")
    im.thumbnail((SIZE, SIZE), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=82, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def inline_emblems(html: str) -> tuple[str, int]:
    n = 0
    def rep(m):
        nonlocal n
        p = ROOT / m.group(1)
        if not p.exists():
            return m.group(0)
        n += 1
        return '"emblem": "' + webp_uri(p) + '"'
    html = re.sub(r'"emblem":\s*"(emblems/[^"]+)"', rep, html)
    return html, n


def club_count(html: str) -> int:
    m = re.search(r"const CLUBS=(\{.*?\});\s*(?:let|const|var)\s", html, re.S)
    if not m:
        return 0
    try:
        return len(json.loads(m.group(1)))
    except Exception:
        return len(re.findall(r'"asof":', m.group(1)))


def meta_block(n: int) -> str:
    title = "K리그 유스 성적 대시보드"
    desc = f"K리그 {n}개 구단 유스(U11~U18) 연도별·2026 시즌 성적을 한눈에 비교 · 출처: 넥스트플레이어"
    img = f"{SITE}/og.png"
    tags = [
        f'<meta name="description" content="{desc}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{title}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{SITE}/">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{img}">',
    ]
    return "<!--share-meta-->" + "".join(tags) + "<!--/share-meta-->"


ANALYTICS = ('<!--va--><script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)};</script>'
             '<script defer src="/_vercel/insights/script.js"></script><!--/va-->')


def patch(html: str) -> str:
    html, n = inline_emblems(html)
    html = re.sub(r"<!--share-meta-->.*?<!--/share-meta-->", "", html, flags=re.S)
    html = re.sub(r"<!--va-->.*?<!--/va-->", "", html, flags=re.S)
    cnt = club_count(html)
    html = html.replace('<meta name="viewport" content="width=device-width,initial-scale=1">',
                        '<meta name="viewport" content="width=device-width,initial-scale=1">' + meta_block(cnt), 1)
    i = html.rindex("</head>")
    html = html[:i] + ANALYTICS + html[i:]
    print(f"emblems inlined: {n}, clubs: {cnt}")
    return html


def make_og(html: str):
    from playwright.sync_api import sync_playwright
    clubs = re.search(r"const CLUBS=(\{.*?\});\s*(?:let|const|var)\s", html, re.S)
    data = json.loads(clubs.group(1)) if clubs else {}
    logos = [c.get("emblem") for c in data.values() if c.get("emblem")]
    n = len(data)
    imgs = "".join(f'<img src="{u}">' for u in logos[:24])
    page = f"""<html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>body{{margin:0;width:1200px;height:630px;font-family:'Pretendard Variable',Pretendard,sans-serif;
background:radial-gradient(1200px 600px at 80% -10%,#1f3a7a 0%,#0b1430 55%,#070b18 100%);color:#fff;overflow:hidden;position:relative}}
.wrap{{padding:64px 72px}}.tag{{display:inline-block;background:#f5c451;color:#0b1430;font-weight:900;font-size:26px;padding:8px 18px;border-radius:10px}}
h1{{font-size:76px;line-height:1.08;margin:26px 0 14px;font-weight:900;letter-spacing:-1.5px}}
p{{font-size:30px;color:#c9d3ea;margin:0}}.logos{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;flex-wrap:wrap;gap:12px}}
.logos img{{width:58px;height:58px;background:#fff;border-radius:50%;padding:5px;object-fit:contain;box-sizing:border-box}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:14px;background:#f5c451}}</style></head><body><div class="bar"></div><div class="wrap">
<span class="tag">U11 · U12 · U14 · U15 · U17 · U18</span><h1>K리그 유스<br>성적 대시보드</h1>
<p>{n}개 구단 · 연도별 성적과 2026 시즌을 한눈에 비교</p></div><div class="logos">{imgs}</div></body></html>"""
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.set_content(page, wait_until="networkidle")
        pg.wait_for_timeout(500)
        pg.screenshot(path=str(ROOT / "og.png"))
        b.close()
    Image.open(ROOT / "og.png").convert("RGB").save(ROOT / "og.png", optimize=True)
    print("og.png written")


if __name__ == "__main__":
    html = PATH.read_text(encoding="utf-8")
    html = patch(html)
    PATH.write_text(html, encoding="utf-8")
    if "--og" in sys.argv:
        make_og(html)
