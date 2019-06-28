#!/usr/bin/env python3
"""Economic Simulation Matrix Generator."""

import csv
import random
from itertools import *

column_names = [
    "unique_id",
    "disabled",
    "country",
    "crop",
    "sim-price",
    "sim-production-c1",
    "sim-production-c2",
    "notes",
]


country = ["South Sudan"]
disabled = ["False"]
crop = ["cassava,groundnuts,maize,sesame,sorghum"]
sim_price = range(-50, 50, 10)
sim_production_c1 = range(-50, 50, 10)
sim_production_c2 = range(-50, 50, 10)
notes = [" "]

rows = list(
    product(
        disabled, country, crop, sim_price, sim_production_c1, sim_production_c2, notes
    )
)

random.seed(1000)

with open("sim-matrix.csv", "w") as f:
    w = csv.writer(f)
    w.writerow(column_names)
    for row in rows:
        l = ["eco-" + str(random.randint(100000000, 999999999))]
        for e in row:
            if e.__class__ is tuple:
                for t in e:
                    l.append(t)
            else:
                l.append(e)
        w.writerow(l)
