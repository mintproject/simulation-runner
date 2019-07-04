# -*- coding: utf-8 -*-
"""Cycles Model."""

import os

from pathlib import Path
from string import Template

__WINGS_TEMPLATE_NAME__ = "cycles_v2_standalone_fertilizer_increase"

__IO_TYPES__ = {
    "cycles_crops": "CyclesCrops",
    "cycles_ctrl": "CyclesCtrl",
    "cycles_operation": "CyclesOperation",
    "cycles_ctrl1": "CyclesCtrl",
    "cycles_operation1": "CyclesOperation",
    "cycles_ctrl2": "CyclesCtrl",
    "cycles_operation2": "CyclesOperation",
    "cycles_soil": "CyclesSoil",
    "cycles_weather": "CyclesWeather",
}


def _process_operation_file(kwargs, input_folder_dir, start_year=2000, end_year=2017, baseline=False, fertilizer_increase=False):

    year_count = 1
    operation_contents = ""

    while (year_count <= end_year - start_year + 1):
        with open("cycles/templates/template.operation") as t_op_file:
            src = Template(t_op_file.read())
            op_data = {
                "year_count": year_count,
                "crop_name": kwargs["crop"],
                "fertilization_date": int(kwargs["start_planting_date"]) - 10,
                "fertilization_rate": kwargs["fertilizer_rate"],
                "start_planting_date": kwargs["start_planting_date"],
                "end_planting_date": kwargs["end_planting_date"],
                "tillage_date": int(kwargs["start_planting_date"]) + 20,
            }
            result = src.substitute(op_data)
            operation_contents += result

            # handling weeds
            if float(kwargs["weed_fraction"]) > 0:
                with open("cycles/templates/template-weed.operation") as t_wd_file:
                    wd_src = Template(t_wd_file.read())
                    wd_data = {
                        "year_count": year_count,
                        "weed_planting_date": int(kwargs["start_planting_date"]) + 7,
                        "weed_fraction": kwargs["weed_fraction"]
                    }
                    wd_result = wd_src.substitute(wd_data)
                    operation_contents += wd_result + "\n"

            year_count += 1

    # writing operations file
    f = "baseline_" + kwargs["unique_id"] if baseline else kwargs["unique_id"]
    if fertilizer_increase:
        f = f + "_fertilizer_increase"
        input_folder_dir = input_folder_dir + "_fertilizer_increase"
    op_filename = Path(input_folder_dir + "/" + f + ".operation")
    with op_filename.open("w") as op_file:
        op_file.write(operation_contents)
        return op_filename

    return None


def _process_ctrl_file(kwargs, input_folder_dir, op_filename, baseline=False, fertilizer_increase=False):
    with open("cycles/templates/template.ctrl") as t_ctrl_file:
        src = Template(t_ctrl_file.read())
        ctrl_data = {
            "start_year": 2000,
            "end_year": 2017,
            "rotation_size": 18,
            "crop_file": "crops.crop",
            "operation_file": op_filename,
            "soil_file": kwargs["soil"],
            "weather_file": kwargs["weather"],
            "reinit": 0 if baseline else 1,
        }
        result = src.substitute(ctrl_data)

        f = "baseline_" + kwargs["unique_id"] if baseline else kwargs["unique_id"]
        if fertilizer_increase:
            f = f + "_fertilizer_increase"
            input_folder_dir = input_folder_dir + "_fertilizer_increase"
        ctrl_filename = Path(input_folder_dir + "/" + f + ".ctrl")
        with ctrl_filename.open("w") as ctrl_file:
            ctrl_file.write(result)
            return ctrl_filename


def process_input(kwargs):

    # temporary conditions to limit number of executions
    if kwargs["crop"] != "Maize" \
        or kwargs["forcing"] == "True" \
        or kwargs["weather"] != "met8.88Nx27.12E.weather" \
        or kwargs["planting_date_fixed"] != "True" \
        or kwargs["start_planting_date"] != "100" \
        or kwargs["fertilizer_rate"] != "0.00"        :
        return None
    if kwargs["planting_date_fixed"] == "True":
         kwargs["end_planting_date"] = -999

    # create input folder
    input_folder_dir = "./cycles/inputs/" + kwargs["unique_id"]
    if not os.path.exists(input_folder_dir):
        os.makedirs(input_folder_dir)
    if not os.path.exists(input_folder_dir + "_fertilizer_increase"):
        os.makedirs(input_folder_dir + "_fertilizer_increase")

    # baseline args
    baseline_kwargs = kwargs.copy()
    baseline_kwargs["start_planting_date"] = 100
    baseline_kwargs["fertilizer_rate"] = 156.25
    baseline_op_filename = _process_operation_file(
        baseline_kwargs, input_folder_dir, baseline=True
    )
    baseline_ctrl_filename = _process_ctrl_file(
        baseline_kwargs, input_folder_dir, baseline_op_filename.name, True
    )

    # Main simulation
    op_filename = _process_operation_file(kwargs, input_folder_dir)
    ctrl_filename = _process_ctrl_file(kwargs, input_folder_dir, op_filename.name)

    op_fi_filename = _process_operation_file(kwargs, input_folder_dir, fertilizer_increase=True)
    ctrl_fi_filename = _process_ctrl_file(kwargs, input_folder_dir, op_fi_filename.name, fertilizer_increase=True)

    return {
        "cycles_ctrl": baseline_ctrl_filename,
        "cycles_operation": baseline_op_filename,
        "cycles_crops": "file:crops.crop",
        "cycles_ctrl1": ctrl_filename,
        "cycles_operation1": op_filename,
        "cycles_ctrl2": ctrl_fi_filename,
        "cycles_operation2": op_fi_filename,
        "cycles_soil": "file:pongo.soil",
        "cycles_weather": "file:" + kwargs["weather"],
        "unique_id": kwargs["unique_id"],
        "unique_id1": kwargs["unique_id"] + "_fertilizer_increase",
        "crop_name": kwargs["crop"],
    }
