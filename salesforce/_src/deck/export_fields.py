# -*- coding: utf-8 -*-
"""Dump camps.py to JSON so the deck generator can build the field appendix.

camps.py stays the single source of truth: the HTML, the CSV and the deck all
read from it. Run this before build_deck.cjs whenever camps.py changes:

    python3 export_fields.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import camps  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields.json")


def rows(arr):
    return [{"sec": s, "name": n, "type": t, "values": v, "req": r}
            for s, n, t, v, r in (x[:5] for x in arr)]


data = {"rfq": rows(camps.RFQ), "quote": rows(camps.QUOTE), "line": rows(camps.LINE)}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print("%s — RFQ %d · Quote %d · Line %d"
      % (OUT, len(data["rfq"]), len(data["quote"]), len(data["line"])))
