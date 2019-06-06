# -*- coding: utf-8 -*-
"""Cycles Model."""

import os

from pathlib import Path
from string import Template

__WINGS_TEMPLATE_NAME__ = "cycles_v2_standalone"

__IO_TYPES__ = {
    "cycles_crops": "CyclesCrops",
    "cycles_ctrl": "CyclesCtrl",
    "cycles_operation": "CyclesOperation",
    "cycles_ctrl1": "CyclesCtrl",
    "cycles_operation1": "CyclesOperation",
    "cycles_soil": "CyclesSoil",
    "cycles_weather": "CyclesWeather",
}


def _process_operation_file(kwargs, input_folder_dir, baseline=False):
    with open('cycles/templates/template.operation') as t_op_file:
        src = Template(t_op_file.read())
        op_data = {
            'crop_name': kwargs['crop'],
            'fertilization_date': int(kwargs['start_planting_date']) - 10,
            'fertilization_rate': kwargs['fertilizer_rate'],
            'start_planting_date': kwargs['start_planting_date'],
            'tillage_date':  int(kwargs['start_planting_date']) + 20
        }
        result = src.substitute(op_data)
        f = 'baseline_' + kwargs['unique_id'] if baseline else kwargs['unique_id']
        op_filename = Path(input_folder_dir + '/' + f + '.operation')
        with op_filename.open('w') as op_file:
            op_file.write(result)
            return op_filename
    return None


def _process_ctrl_file(kwargs, input_folder_dir, op_filename, baseline=False):
    with open('cycles/templates/template.ctrl') as t_ctrl_file:
        src = Template(t_ctrl_file.read())
        ctrl_data = {
            'start_year': 2000,
            'end_year': 2017,
            'crop_file': 'crops.crop',
            'operation_file': op_filename,
            'soil_file': kwargs['soil'],
            'weather_file': kwargs['weather'],
            'reinit': 0 if baseline else 1
        }
        result = src.substitute(ctrl_data)

        f = 'baseline_' + kwargs['unique_id'] if baseline else kwargs['unique_id']
        ctrl_filename = Path(input_folder_dir + '/' + f + '.ctrl')
        with ctrl_filename.open('w') as ctrl_file:
            ctrl_file.write(result)
            return ctrl_filename


def process_input(kwargs):
    # create input folder
    input_folder_dir = './cycles/inputs/' + kwargs['unique_id']
    if not os.path.exists(input_folder_dir):
        os.makedirs(input_folder_dir)

    # baseline args
    baseline_kwargs = kwargs.copy()
    baseline_kwargs['start_planting_date'] = 100
    baseline_kwargs['fertilizer_rate'] = 156.25
    baseline_op_filename = _process_operation_file(baseline_kwargs, input_folder_dir, True)
    baseline_ctrl_filename = _process_ctrl_file(baseline_kwargs, input_folder_dir, baseline_op_filename.name, True)

    # Main simulation
    op_filename = _process_operation_file(kwargs, input_folder_dir)
    ctrl_filename = _process_ctrl_file(kwargs, input_folder_dir, op_filename.name)

    if kwargs['crop'] != 'Maize':
        return None

    return {
        "cycles_ctrl": baseline_ctrl_filename,
        "cycles_operation": baseline_op_filename,
        "cycles_crops": "file:crops.crop",
        "cycles_ctrl1": ctrl_filename,
        "cycles_operation1": op_filename,
        "cycles_soil": "file:pongo.soil",
        "cycles_weather": "file:" + kwargs['weather'],
        "unique_id": kwargs['unique_id'],
        "crop_name": kwargs['crop']
    }
