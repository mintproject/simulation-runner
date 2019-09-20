#!/usr/bin/env python3
"""Economic Simulation Matrix Generator."""

import csv
import sys
import hashlib


column_names = [
    "unique_id",
    "disabled",
    "region",
    "start_date",
    "end_date",
    "TS_PRCP",
    "TS_SFCTMP",
    "ET_ETP",
    "SOIL_KINF",
    "SOIL_KMACSATV",
    "SOIL_ALPHA",
    "SOIL_BETA",
    "GEOL_KMACSATH",
    "GEOL_DMAC",
    "GEOL_THETAS",
    "LC_VEGFRAC",
    "LC_DROOT",
]


disabled = [False]
start_date = ["2017-01-01"]
end_date = ["2017-12-31"]
region = ["pongo"]
TS_PRCP = [1.2, 1, 0.8]
TS_SFCTMP = [+2.0, 0.0, -2.0]
ET_ETP = [1.2, 1, 0.6]
SOIL_KINF = [1.5, 1, 0.5]
SOIL_KMACSATV = [10, 1, 0.5]
SOIL_ALPHA = [1.5, 1, 0.5]
SOIL_BETA = [1.5, 1, 0.5]
GEOL_KMACSATH = [10, 1, 0.5]
GEOL_DMAC = [1.5, 1, 0.5]
GEOL_THETAS = [2.0, 1, 0.5]
LC_VEGFRAC = [1, 0.5, 0.2]
LC_DROOT = [1.5, 1, 0.5]

variations = {
    "TS_PRCP": TS_PRCP,
    "TS_SFCTMP": TS_SFCTMP,
    "ET_ETP": ET_ETP,
    "SOIL_KINF": SOIL_KINF,
    "SOIL_KMACSATV": SOIL_KMACSATV,
    "SOIL_ALPHA": SOIL_ALPHA,
    "SOIL_BETA": SOIL_BETA,
    "GEOL_KMACSATH": GEOL_KMACSATH,
    "GEOL_DMAC": GEOL_DMAC,
    "GEOL_THETAS": GEOL_THETAS,
    "LC_VEGFRAC": LC_VEGFRAC,
    "LC_DROOT": LC_DROOT,
}


def _hash(_d):
    combined = ""
    for _k, _v in _d.items():
        combined += f"_{_k}_{_v}"
    else:
        _d["unique_id"] = hashlib.md5(combined.strip("_").encode()).hexdigest()
        _d["disabled"] = False

    return _d


f = sys.argv[1] if len(sys.argv) > 1 else "sim-matrix.csv"
with open(f, "w") as f:
    w = csv.DictWriter(f, fieldnames=column_names)
    w.writeheader()
    d = {
        "start_date": start_date[0],
        "end_date": end_date[0],
        "region": "pongo",
        "TS_PRCP": 1,
        "TS_SFCTMP": 0.0,
        "ET_ETP": 1,
        "SOIL_KINF": 1,
        "SOIL_KMACSATV": 1,
        "SOIL_ALPHA": 1,
        "SOIL_BETA": 1,
        "GEOL_KMACSATH": 1,
        "GEOL_DMAC": 1,
        "GEOL_THETAS": 1,
        "LC_VEGFRAC": 1,
        "LC_DROOT": 1,
    }
    for k, values in variations.items():
        for v in values:
            _d = d.copy()
            if _d[k] == v:
                continue
            _d[k] = v
            _d = _hash(_d)
            w.writerow(_d)
    else:
        _d = d.copy()
        _d = _hash(_d)
        w.writerow(_d)
