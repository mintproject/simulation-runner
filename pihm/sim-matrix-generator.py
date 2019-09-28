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
    # Calib File Variations
    "GEOL_KSATH",
    "GEOL_KSATV",
    "GEOL_KMACSATH",
    "GEOL_MACVF",
    "GEOL_THETAS",
    "GEOL_THETAR",
    "GEOL_DMAC",
    "SOIL_KINF",
    "SOIL_KMACSATV",
    "SOIL_DINF",
    "SOIL_ALPHA",
    "SOIL_BETA",
    "SOIL_MACHF",
    "LC_VEGFRAC",
    "LC_ALBEDO",
    "LC_ROUGH",
    "LC_DROOT",
    "LC_ISMAX",
    "LC_IMPAF",
    "LC_SOILDGD",
    "TS_PRCP",
    "TS_LAI",
    "TS_SFCTMP",
    "ET_ETP",
    "ET_IC",
    "ET_TR",
    "ET_SOIL",
    "RIV_ROUGH",
    "RIV_KH",
    "RIV_SINU",
    "RIV_CWR",
    "RIV_BEDTHICK",
    "RIV_BSLOPE",
    "RIV_DPTH",
    "RIV_WDTH",
    "IC_GW",
    "IC_RIV",
    "AQ_DEPTH",
]


disabled = [False]
start_date = ["2017-01-01"]
end_date = ["2017-12-31"]
region = ["pongo"]

GEOL_KSATH = [0.5, 1, 10]
GEOL_KSATV = [0.5, 1, 10]
GEOL_KMACSATH = [0.5, 1, 2]
GEOL_MACVF = [0.5, 1, 2]
GEOL_THETAS = [0.5, 1, 1.2]
GEOL_THETAR = [0.5, 1, 1.2]
SOIL_KINF = [0.5, 1, 2]
SOIL_KMACSATV = [0.5, 1, 2]
SOIL_DINF = [0.5, 1, 1.5]
SOIL_ALPHA = [0.5, 1, 1.5]
SOIL_BETA = [0.5, 1, 1.5]
LC_VEGFRAC = [0.2, 0.5, 1]
LC_ALBEDO = [0.5, 0.75, 1]
LC_ROUGH = [0.5, 1, 1.5]
LC_DROOT = [0.8, 1, 1.5]
LC_ISMAX = [0.5, 1, 1.5]
TS_PRCP = [0.8, 1, 1.2]
TS_LAI = [0.5, 1, 1.5]
TS_SFCTMP = [-1, 0, +2]
ET_ETP = [0.6, 1, 1.2]
RIV_ROUGH = [0.5, 1, 4]
RIV_KH = [0.5, 1, 10]


variations = {
    "GEOL_KSATH": GEOL_KSATH,
    "GEOL_KSATV": GEOL_KSATV,
    "GEOL_KMACSATH": GEOL_KMACSATH,
    "GEOL_MACVF": GEOL_MACVF,
    "GEOL_THETAS": GEOL_THETAS,
    "GEOL_THETAR": GEOL_THETAR,
    "SOIL_KINF": SOIL_KINF,
    "SOIL_KMACSATV": SOIL_KMACSATV,
    "SOIL_DINF": SOIL_DINF,
    "SOIL_ALPHA": SOIL_ALPHA,
    "SOIL_BETA": SOIL_BETA,
    "LC_VEGFRAC": LC_VEGFRAC,
    "LC_ALBEDO": LC_ALBEDO,
    "LC_ROUGH": LC_ROUGH,
    "LC_DROOT": LC_DROOT,
    "LC_ISMAX": LC_ISMAX,
    "TS_PRCP": TS_PRCP,
    "TS_LAI": TS_LAI,
    "TS_SFCTMP": TS_SFCTMP,
    "ET_ETP": ET_ETP,
    "RIV_ROUGH": RIV_ROUGH,
    "RIV_KH": RIV_KH,
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
        "GEOL_KSATH": 1,
        "GEOL_KSATV": 1,
        "GEOL_KMACSATH": 1,
        "GEOL_MACVF": 1,
        "GEOL_THETAS": 1,
        "GEOL_THETAR": 1,
        "GEOL_DMAC": 1,
        "SOIL_KINF": 1,
        "SOIL_KMACSATV": 1,
        "SOIL_DINF": 1,
        "SOIL_ALPHA": 1,
        "SOIL_BETA": 1,
        "SOIL_MACHF": 1,
        "LC_VEGFRAC": 1,
        "LC_ALBEDO": 1,
        "LC_ROUGH": 1,
        "LC_DROOT": 1,
        "LC_ISMAX": 1,
        "LC_IMPAF": 1,
        "LC_SOILDGD": 1,
        "TS_PRCP": 1,
        "TS_LAI": 1,
        "TS_SFCTMP": 0.0,
        "ET_ETP": 1,
        "ET_IC": 1,
        "ET_TR": 1,
        "ET_SOIL": 1,
        "RIV_ROUGH": 1,
        "RIV_KH": 1,
        "RIV_SINU": 1,
        "RIV_CWR": 1,
        "RIV_BEDTHICK": 1,
        "RIV_BSLOPE": 0.0,
        "RIV_DPTH": 0.0,
        "RIV_WDTH": 0.0,
        "IC_GW": 0.0,
        "IC_RIV": 0.0,
        "AQ_DEPTH": 0.0,
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
