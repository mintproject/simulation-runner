# -*- coding: utf-8 -*-
"""Economic Model."""

import csv
import hashlib
import os
from pathlib import Path

__WINGS_TEMPLATE_NAME__ = "PIHM-4.1.0-standalone"


__IO_TYPES__ = {"pihm-input": "targz"}


def process_input(
    start_date="2017-01-01",
    end_date="2017-12-31",
    region="pongo",
    TS_PRCP=1,
    TS_SFCTMP=0.0,
    ET_ETP=1,
    SOIL_KINF=1,
    SOIL_KMACSATV=1,
    SOIL_ALPHA=1,
    SOIL_BETA=1,
    GEOL_KMACSATH=1,
    GEOL_DMAC=1,
    GEOL_THETAS=1,
    LC_VEGFRAC=1,
    LC_DROOT=1,
    disabled="False",
    **kwargs,
):
    if disabled == "True":
        return None

    return {
        "pihm-input": _generate_pihm_input(start_date, end_date, region),
        "start_date": start_date,
        "end_date": end_date,
        "region": region,
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


def _generate_pihm_input(start_date, end_date, region):
    combined = f"start_date_{start_date}_end_date_{end_date}_region_{region}"
    checksum = hashlib.md5(combined.encode()).hexdigest()
    return f"file:pihm-input-{region}-{checksum}.tgz"
