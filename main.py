#!/usr/bin/env python3
"""Forecast Bitcoin's price 240 minutes after each checkpoint.

Model, from the case's own 72h of 1-minute closes:
  forecast = last + 0.5 * (mean(last 1440 closes) - last) - 130
  * Mean reversion: BTC oscillates around its trailing-24h mean; pulling
    halfway toward it beats persistence.
  * Fixed drift -130: over the 6 practice cases the average 4h change is
    about -$130 (a sustained downtrend, -96 to -195 per case, stable in
    leave-one-case-out validation). The forecast's own bias is positive
    without it, so the correction helps even if the drift flattens.
Validated on 264 checkpoints cut from the practice cases:
  persistence (house baseline) MAE $451.17, this model MAE $394.64 (-12.5%).
Stdlib only, no network, deterministic.
Reads $MAKEFUN_INPUT_DIR (else /input), writes $MAKEFUN_OUTPUT_DIR (else /output).
"""
import glob
import json
import os

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

WINDOW = 1440   # trailing 24h closes for the mean
PULL = 0.5      # mean-reversion pull
DRIFT = -130.0  # fixed 4h drift correction, dollars


def forecast(prices):
    # The trailing-24h mean needs a full WINDOW of closes; a shorter series
    # would silently average over whatever is there and bias the pull.
    if len(prices) < WINDOW:
        raise ValueError(f"need at least {WINDOW} prices, got {len(prices)}")
    last = prices[-1]
    mean24 = sum(prices[-WINDOW:]) / WINDOW
    return last + PULL * (mean24 - last) + DRIFT


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(INPUT_DIR, "*.in"))):
        with open(path) as fh:
            case = json.load(fh)
        prices = case["markets"][0]["prices"]
        price = forecast(prices)
        if not (0 < price < 10_000_000):
            raise SystemExit("forecast out of range")
        out = {"forecasts": [{"case": case["case"], "price": round(price, 2)}]}
        name = os.path.splitext(os.path.basename(path))[0] + ".out"
        with open(os.path.join(OUTPUT_DIR, name), "w") as fh:
            json.dump(out, fh)


if __name__ == "__main__":
    main()
