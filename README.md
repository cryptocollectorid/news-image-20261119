# The World Today — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cryptocollectorid/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/cryptocollectorid/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page summing up the world's news of **Thursday
19 November 2026** in a single 1024×1024 image, drawn with PIL
only. Entry for the make.fun competition
[news-image-20261119](https://make.fun/bounty/news-image-20261119).

## The six stories

1. **Trump, Xi and Putin meet in Shenzhen** — first-ever three-way
   summit of the US, Chinese and Russian leaders, on the APEC
   sidelines.
2. **GTA VI rolls out worldwide** — Rockstar's blockbuster unlocks
   at midnight local time, New Zealand first.
3. **Anthropic debuts on Nasdaq** — Claude maker starts trading as
   ANT after pricing its IPO at $83 a share.
4. **Cyclone Akvan nears India's coast** — severe storm, red
   alerts, schools shut ahead of Friday landfall.
5. **Bumrah strikes as the Test opens** — New Zealand 60 for 4 at
   lunch on day one in Wellington.
6. **India and Japan hold 2+2 talks** — foreign and defence
   ministers meet in Tokyo.

Every story happened, or was first reported, on 19 November 2026.

## How to run

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024, under 1 MiB). The program is
deterministic: no network, no randomness, no timestamps — two runs
produce byte-identical output. A built-in `validate_png()` check
verifies the PNG signature, dimensions and file size on every run.

## License

MIT — see [LICENSE](LICENSE).
