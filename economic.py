# -*- coding: utf-8 -*-
"""Economic Model."""

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
    return {
        "cycles-data": "file:cyclesdata.csv",
        "land-input": "file:landinput.csv",
        "price": "file:price.csv",
        "production-cost": "file:productioncost.csv",
        "sim-price": "file:simprice.csv",
        "sim-production-cost": "file:simproductioncost.csv",
        "supply-elasticity": "file:supplyelasticity.csv",
    }
