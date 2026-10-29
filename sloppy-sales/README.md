# sloppy-sales

A small sales-report script for the multi-agent review panel to look at. It runs,
but it was written in a hurry: the logic is slow and the code is hard to read.

## Run it

```bash
python report.py
```

It prints a per-order report and the top customer by total spend.

## Your panel's job

Point your review panel at `report.py`. The performance reviewer should flag the
slow patterns; the readability reviewer should flag the messy ones. This file has
plenty of both.
