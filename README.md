# Run Simulations


# Adding a New Model

## Prerequisites

WINGS Component(s) and Template should pre-exist.

```bash
$ ./sim-runner.py -h
usage: sim-runner.py [-h] -w WINGS_CONFIG -m MODEL_NAME [-d] simulation_matrix

Run WINGS template based on simulation matrix.

positional arguments:
  simulation_matrix     Simulation Matrix

optional arguments:
  -h, --help            show this help message and exit
  -w WINGS_CONFIG, --wings-config WINGS_CONFIG
                        WINGS Configuration File
  -m MODEL_NAME, --model-name MODEL_NAME
                        Model to run
  -d, --debug           Debug
```

## Create a <model_name>.py File

1. The file must define a constant `__WINGS_TEMPLATE_NAME__` whose value should be the name of the WINGS template to invoke.

1. The file must define a constant `__IO_TYPES__` whose value should be a dictionary mapping the input to it's corresponding type. Only required for file types.

1. The file must implement one method `process_input`, which takes one dictionary as input, and returs a dictionary as output.

    1. The input dictionary represents the row read from the simulation-matrix csv file.
    1. The output dictionary represents the input for the WINGS template being invoked.

        a. The `key` represents the input variable name of the template.
        a. The `value` represents the value for that input. For input(s) that take a file as input, the value should be a Python `Path` object pointing to the location of the file. The runner will upload the file before starting the run. For files that already exist in WINGS, the `value` should be the WINGS filename as a string prefixed with `file:`.


### Example
```python
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
        "cycles-data": Path("cyclesdata.csv"),
        "land-input": "file:landinput.csv",
        "price": "file:price.csv",
        "production-cost": "file:productioncost.csv",
        "sim-price": "file:simprice.csv",
        "sim-production-cost": "file:simproductioncost.csv",
        "supply-elasticity": "file:supplyelasticity.csv",
    }
```
