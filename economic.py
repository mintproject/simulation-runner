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
    "sim-price": "economic-sim-price",
    "sim-production-cost": "economic-sim-production-cost",
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
        "unique-id": kwargs["unique_id"],
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
    return "file:pongo-landinput.csv"


def _generate_price(**kwargs):
    return "file:pongo-price.csv"


def _generate_production_cost(**kwargs):
    return "file:pongo-productioncost.csv"


def _generate_sim_price(unique_id, crop, price, sim_price, **kwargs):
    o = Path("./economic/inputs/%s/%s-simprice.csv" % (unique_id, unique_id))

    with o.open("w") as f:
        w = csv.writer(f)

        crop = crop.split(",")
        price = price.split(",")
        sim_price = float(sim_price) / 100

        w.writerow(["", "p"])
        for c, p in zip(crop, price):
            p = float(p)
            w.writerow((c, p + (p * sim_price)))

    return o


def _generate_sim_production_cost(
    unique_id,
    crop,
    production_cost_c1,
    production_cost_c2,
    sim_production_c1,
    sim_production_c2,
    **kwargs
):
    o = Path("./economic/inputs/%s/%s-simproductioncost.csv" % (unique_id, unique_id))
    with o.open("w") as f:
        w = csv.writer(f)

        crop = crop.split(",")
        production_cost_c1 = production_cost_c1.split(",")
        production_cost_c2 = production_cost_c2.split(",")
        sim_production_c1 = float(sim_production_c1) / 100
        sim_production_c2 = float(sim_production_c2) / 100

        w.writerow(["", "c1", "c2"])
        for c, c1, c2 in zip(crop, production_cost_c1, production_cost_c2):
            c1 = float(c1)
            c2 = float(c2)

            w.writerow(
                (c, c1 + (c1 * sim_production_c1), c2 + (c2 * sim_production_c2))
            )
    return o


def _generate_supply_elasticity(**kwargs):
    return "file:supplyelasticity.csv"
