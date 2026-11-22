# The World in One Day — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![make.fun · news-image-20261122 · rank](https://make.fun/badge/news-image-20261122-rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![make.fun · news-image-20261122 · reward](https://make.fun/badge/news-image-20261122-reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page summing up **Sunday, 22 November 2026** in one image,
drawn entirely with Python + PIL and DejaVu fonts — no AI image generation.

- **Lead:** Iran strikes Bahrain and two tankers are hit in the Strait of Hormuz.
- **Also:** COP31 puts a final deal to the vote without a single mention of
  fossil fuels; Mexico captures FBI top-ten fugitive "El Chapo Isidro";
  Wall Street slides into a correction as the AI trade unwinds.
- **In brief:** UN rules for lethal autonomous weapons, Russian missiles in
  Kryvyi Rih, a fire at Basra's Hartha power station, toxic alcohol in
  Manipur, and the EU–Indonesia trade deal.

## How it works

`draw_frontpage.py` renders `entry.png` (1024×1024). `main.py` (stdlib only)
copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, falling back to
`/output/` when the variable is unset. The program is deterministic: running
it twice produces byte-identical output.
