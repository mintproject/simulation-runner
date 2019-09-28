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
    GEOL_KSATH=1,
    GEOL_KSATV=1,
    GEOL_KMACSATH=1,
    GEOL_MACVF=1,
    GEOL_THETAS=1,
    GEOL_THETAR=1,
    GEOL_DMAC=1,
    SOIL_KINF=1,
    SOIL_KMACSATV=1,
    SOIL_DINF=1,
    SOIL_ALPHA=1,
    SOIL_BETA=1,
    SOIL_MACHF=1,
    LC_VEGFRAC=1,
    LC_ALBEDO=1,
    LC_ROUGH=1,
    LC_DROOT=1,
    LC_ISMAX=1,
    LC_IMPAF=1,
    LC_SOILDGD=1,
    TS_PRCP=1,
    TS_LAI=1,
    TS_SFCTMP=0.0,
    ET_ETP=1,
    ET_IC=1,
    ET_TR=1,
    ET_SOIL=1,
    RIV_ROUGH=1,
    RIV_KH=1,
    RIV_SINU=1,
    RIV_CWR=1,
    RIV_BEDTHICK=1,
    RIV_BSLOPE=0.0,
    RIV_DPTH=0.0,
    RIV_WDTH=0.0,
    IC_GW=0.0,
    IC_RIV=0.0,
    AQ_DEPTH=0.0,
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
        "GEOL_KSATH": GEOL_KSATH,
        "GEOL_KSATV": GEOL_KSATV,
        "GEOL_KMACSATH": GEOL_KMACSATH,
        "GEOL_MACVF": GEOL_MACVF,
        "GEOL_THETAS": GEOL_THETAS,
        "GEOL_THETAR": GEOL_THETAR,
        "GEOL_DMAC": GEOL_DMAC,
        "SOIL_KINF": SOIL_KINF,
        "SOIL_KMACSATV": SOIL_KMACSATV,
        "SOIL_DINF": SOIL_DINF,
        "SOIL_ALPHA": SOIL_ALPHA,
        "SOIL_BETA": SOIL_BETA,
        "SOIL_MACHF": SOIL_MACHF,
        "LC_VEGFRAC": LC_VEGFRAC,
        "LC_ALBEDO": LC_ALBEDO,
        "LC_ROUGH": LC_ROUGH,
        "LC_DROOT": LC_DROOT,
        "LC_ISMAX": LC_ISMAX,
        "LC_IMPAF": LC_IMPAF,
        "LC_SOILDGD": LC_SOILDGD,
        "TS_PRCP": TS_PRCP,
        "TS_LAI": TS_LAI,
        "TS_SFCTMP": TS_SFCTMP,
        "ET_ETP": ET_ETP,
        "ET_IC": ET_IC,
        "ET_TR": ET_TR,
        "ET_SOIL": ET_SOIL,
        "RIV_ROUGH": RIV_ROUGH,
        "RIV_KH": RIV_KH,
        "RIV_SINU": RIV_SINU,
        "RIV_CWR": RIV_CWR,
        "RIV_BEDTHICK": RIV_BEDTHICK,
        "RIV_BSLOPE": RIV_BSLOPE,
        "RIV_DPTH": RIV_DPTH,
        "RIV_WDTH": RIV_WDTH,
        "IC_GW": IC_GW,
        "IC_RIV": IC_RIV,
        "AQ_DEPTH": AQ_DEPTH,
    }


def _generate_pihm_input(start_date, end_date, region):
    combined = f"start_date_{start_date}_end_date_{end_date}_region_{region}"
    checksum = hashlib.md5(combined.encode()).hexdigest()
    return f"file:pihm-input-{region}-{checksum}.tgz"
