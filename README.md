# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Andia86/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Andia86/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One page that sums up Wednesday 25 November 2026 in world news, drawn by a
Python program (Pillow): 12 lead cards, a markets panel, a UTC timeline of the
day, a dotted world map with a pin for every story region, and 40 one-line
briefs. Every story on the page happened, or was first reported, on Wednesday
25 November 2026 in some time zone, and each one was checked against dated
wire copy from that day before it was allowed on the page. NEWS_SOURCES.md
lists the dated source behind every story, and names the big earlier-day
stories that were deliberately left out.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png` (1024 x 1024). Running it twice gives the same
bytes: the page is drawn from fixed data with no clock, no network and no
randomness.

---

<sub>Entered on [make.fun](https://make.fun/?ref=chengzhi-jiang&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
