# -*- coding: utf-8 -*-
"""Economic Model."""

import os
from pathlib import Path

__WINGS_TEMPLATE_NAME__ = "economic-v5-standalone"


__IO_TYPES__ = {
    "cycles-data": "economic-cycles-data",
    "land-input": "economic-land-input",
    "price": "economic-price",
    "production-cost": "economic-production-cost",
    "sim-price": "economic-sim-price",
    "sim-production-cost": "economic-sim-production-cost",
    "supply-elasticity": "economic-supply-elasticity",
}


def process_input(kwargs):
    # Create input directory
    input_dir = "./economic/inputs/"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    return {
        "cycles-data": _generate_cycles_data(**kwargs),
        "land-input": _generate_land_input(**kwargs),
        "price": _generate_price(**kwargs),
        "production-cost": _generate_production_cost(**kwargs),
        "sim-price": _generate_sim_price(**kwargs),
        "sim-production-cost": _generate_sim_production_cost(**kwargs),
        "supply-elasticity": _generate_supply_elasticity(**kwargs),
    }


def _generate_cycles_data(**kwargs):
    return "file:cyclesdata.csv"


def _generate_land_input(**kwargs):
    return "file:landinput.csv"


def _generate_price(**kwargs):
    return "file:price.csv"


def _generate_production_cost(**kwargs):
    return "file:productioncost.csv"


def _generate_sim_price(**kwargs):
    o = Path("./economic/inputs/%s-sim-price.csv" % kwargs["unique_id"])
    with o.open("w") as f:
        f.write(
            """,p
cassava,0.26064
groundnuts,0.80474
maize,0.30263
sesame,0.74735
sorghum,0.3742
"""
        )
    return o


def _generate_sim_production_cost(**kwargs):
    o = Path("./economic/inputs/%s-sim-production_cost.csv" % kwargs["unique_id"])
    with o.open("w") as f:
        f.write(
            """,c1,c2
cassava,0.26064
groundnuts,0.80474
maize,0.30263
sesame,0.74735
sorghum,0.3742
"""
        )
    return o


def _generate_supply_elasticity(**kwargs):
    return "file:supplyelasticity.csv"
