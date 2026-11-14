"""Mean-reversion forecaster for the cbBTC/USDC one-minute close.

Reads one makefun/btc-cent-case/v1 case per *.in file and writes a single
price guess for the close 240 minutes after the checkpoint: the last close,
pulled halfway toward the mean of the trailing 1,440 closes, less a fixed
downward drift of 130 dollars.
"""

import json
import os

WINDOW = 1440
PULL = 0.5
DRIFT = -130.0


def forecast_price(prices):
    if len(prices) < WINDOW:
        raise ValueError("price series shorter than the trailing window")
    last = prices[-1]
    tail = prices[-WINDOW:]
    mean = sum(tail) / len(tail)
    return round(last + PULL * (mean - last) + DRIFT, 5)


def forecast_case(case):
    market = case["markets"][0]
    price = forecast_price(market["prices"])
    return {"forecasts": [{"case": case["case"], "price": price}]}


def main():
    in_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    for name in sorted(os.listdir(in_dir)):
        if not name.endswith(".in"):
            continue
        with open(os.path.join(in_dir, name), "r", encoding="utf-8") as handle:
            case = json.load(handle)
        result = forecast_case(case)
        stem = name[:-3]
        path = os.path.join(out_dir, stem + ".out")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
