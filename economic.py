# -*- coding: utf-8 -*-
"""Economic Model."""

import os
import csv
from pathlib import Path

__WINGS_TEMPLATE_NAME__ = "economic-v5-standalone"


__IO_TYPES__ = {
    "cycles-data": "economic-cycles-data",
    "land-input": "economic-land-input",
    "price": "economic-price",
    "production-cost": "economic-production-cost",
    "supply-elasticity": "economic-supply-elasticity",
}


def process_input(kwargs):
    if kwargs["disabled"] != "False":
        return None

    # Create input directory
    input_dir = "./economic/inputs/%s" % kwargs["unique_id"]
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    return {
        "cycles-data": _generate_cycles_data(**kwargs),
        "land-input": _generate_land_input(**kwargs),
        "price": _generate_price(**kwargs),
        "production-cost": _generate_production_cost(**kwargs),
        "crop-price-adjustment": "%r" % kwargs["sim_price"],
        "land-cost-adjustment": "%r" % kwargs["sim_production_c1"],
        "fertilizer-cost-adjustment": "%r" % kwargs["sim_production_c2"],
        "supply-elasticity": _generate_supply_elasticity(**kwargs),
    }


def _generate_cycles_data(**kwargs):
    return "file:cyclesdata.csv"


def _generate_land_input(**kwargs):
    return "file:pongo-landinput.csv"


def _generate_price(**kwargs):
    return "file:pongo-price.csv"


def _generate_production_cost(**kwargs):
    return "file:pongo-productioncost.csv"


def _generate_supply_elasticity(**kwargs):
    return "file:supplyelasticity.csv"
