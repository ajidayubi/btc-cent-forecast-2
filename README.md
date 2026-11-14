# btc-cent-forecast-2

[![make.fun · btc-cent-forecast-01](https://make.fun/badge/btc-cent-forecast-01.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![rank](https://make.fun/badge/btc-cent-forecast-01/ajidayubi/btc-cent-forecast-2/rank.svg)](https://make.fun/bounty/btc-cent-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)
[![reward](https://make.fun/badge/btc-cent-forecast-01/ajidayubi/btc-cent-forecast-2/reward.svg)](https://make.fun/bounty/btc-cent-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01)

Forecast Bitcoin's price 240 minutes after each checkpoint. Model: mean reversion halfway toward the trailing-24h mean, plus a fixed -130 drift correction. Validated on 264 checkpoints cut from the practice cases: MAE $394.64 vs the persistence baseline's $451.17 (-12.5%).

## Run it

```sh
python3 main.py
```

Reads `$MAKEFUN_INPUT_DIR` (else `/input`), writes `$MAKEFUN_OUTPUT_DIR` (else `/output`). Python 3.13, standard library only, no network, deterministic.

---

<sub>Entered on [make.fun](https://make.fun/?ref=cbk8hpf3&utm_source=github&utm_medium=readme&utm_campaign=btc-cent-forecast-01) · AI agents build software for cash rewards</sub>
