#!/usr/bin/env python3
"""Economic Simulation Matrix Generator."""

import csv
import random
from itertools import product

column_names = [
    "unique_id",
    "disabled",
    "country",
    "crop",
    "price",
    "production_cost_c1",
    "production_cost_c2",
    "sim_price",
    "sim_production_c1",
    "sim_production_c2",
    "notes",
]


country = ["South Sudan"]
disabled = ["False"]
crop = ["cassava", "groundnuts", "maize", "sesame", "sorghum"]

price = [0.26064, 0.80474, 0.30263, 0.74735, 0.3742]
sim_price = range(-50, 50, 10)

production_cost_c1 = [383, 383, 175, 383, 350]
sim_production_c1 = range(-50, 50, 10)

production_cost_c2 = [2.5, 2.5, 1, 2.5, 2.7]
sim_production_c2 = range(-50, 50, 10)
notes = [" "]

rows = list(
    product(
        disabled,
        country,
        [",".join(crop)],
        [",".join([str(x) for x in price])],
        [",".join([str(x) for x in production_cost_c1])],
        [",".join([str(x) for x in production_cost_c2])],
        sim_price,
        sim_production_c1,
        sim_production_c2,
        notes,
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
