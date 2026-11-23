# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sehabudien/news-image-23/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sehabudien/news-image-23/reward.svg)](https://make.fun/bounty/news-image-20261123)

A newspaper front page that sums up the world news of **Monday 23 November 2026**
in a single image — an entry for the
[make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).

## The six stories

1. **COP31 collapses — no deal in Antalya.** After a record 44 hours of overtime,
   the UN climate talks ended with no deal; the final pact never named fossil
   fuels, and the EU and island states refused it. The UN chief called it
   "deeply disappointing".
2. **Quake shakes Vanuatu.** A magnitude 6.5 earthquake struck the Vanuatu region
   at 02:40 UTC on Monday, 601 km down. The USGS rated it green; no tsunami threat.
3. **UK to host 2035 Women's World Cup.** FIFA confirms in Zurich on Monday: the
   first World Cup on British soil since 1966 — 48 teams, 104 matches.
4. **AI to read breast scans.** The NHS launches EDITH, the world's largest trial
   of AI in breast screening. Nearly 700,000 women at 30 sites will take part.
5. **Nepal PM meets Modi in Delhi.** Nepal's PM Balen Shah meets Narendra Modi in
   New Delhi on Monday, his first bilateral visit. Energy, trade and a $2bn aid
   deal lead talks.
6. **Wellington Test ends in a draw.** India's record 720 for 9 — the biggest Test
   total ever on New Zealand soil — was not enough. New Zealand held on at
   239 for 5 to draw the first Test.

Sources: Reuters • AP • BBC • USGS • Sky News. Every story happened or was first
reported on Monday 23 November 2026.

## How it is built

`render23.py` draws the front page with Pillow (original illustrations: a cracked
globe, a seismograph, a goal and ball, a screening monitor with a pink ribbon,
the Indian and Nepalese flags, cricket stumps and bat) and writes `entry.png`
(1024×1024, ~149 KB). `main.ts` (Node 22, standard library only) validates the
image — PNG/JPEG magic bytes, ≤ 1,048,576 bytes, ≤ 1024×1024 pixels — and copies
it to `/output/entry.png`.

```sh
python3 render23.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
