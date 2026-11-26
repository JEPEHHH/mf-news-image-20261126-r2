# mf-news-image-20261126-r2

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/JEPEHHH/mf-news-image-20261126-r2/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/JEPEHHH/mf-news-image-20261126-r2/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

news-image-20261126

## Run it

```sh
bash run.sh
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>


---

# 26 November 2026 — one-day world news poster

A deterministic, offline entry for the make.fun one-image news contest.

`main.py` draws a 960x960 RGB poster from scratch using only the Python 3.13
standard library. It paints the canvas, rasterises a small built-in bitmap
font, encodes a PNG with `zlib` and `struct`, then writes `entry.png` to the
output directory. No API keys, no packages, no network, no clock reads.

## Run locally

    mkdir -p out
    MAKEFUN_OUTPUT_DIR=out python3 main.py

In the grader the program writes `/output/entry.png` instead.

## Coverage

The poster names Thursday 26 November 2026 and shows the day's lead stories:
the Gulf war escalation (Houthi strike on Saudi oil infrastructure, drone
attack in Kuwait), Russia's missile and drone barrage on Ukraine, Ebola
passing 12,000 cases in eastern Congo, the US storm that postponed the
Thanksgiving parade, plus a news wire on Gaza, Bangkok, Paris and AI.

## License

MIT — see LICENSE.