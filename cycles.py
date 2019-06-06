# -*- coding: utf-8 -*-
"""Cycles Model."""

import os

from pathlib import Path
from string import Template

__WINGS_TEMPLATE_NAME__ = "cycles-v3-standalone"

__IO_TYPES__ = {
    "cycles-data": "economic-cycles-data",
    "land-input": "economic-land-input",
    "price": "economic-price",
    "production-cost": "economic-production-cost",
    "sim-price": "economic-sim-price",
    "sim-production-cost": "economic-sim-production-cost",
    "supply-elasticity": "economic-supply-elasticity",
}


def _process_operation_file(kwargs, input_folder_dir):
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
        op_filename = kwargs['unique_id'] + '.operation'
        with open(input_folder_dir + '/' + op_filename, 'w') as op_file:
            op_file.write(result)
            return op_filename
    return None


def _process_ctrl_file(kwargs, input_folder_dir, op_filename):
    with open('cycles/templates/template.ctrl') as t_ctrl_file:
        src = Template(t_ctrl_file.read())
        ctrl_data = {
            'start_year': 2000,
            'end_year': 2017,
            'crop_file': 'crops.crop',
            'operation_file': op_filename,
            'soil_file': kwargs['soil'],
            'weather_file': kwargs['weather']
        }
        result = src.substitute(ctrl_data)

        with open(input_folder_dir + '/' + kwargs['unique_id'] + '.ctrl', 'w') as ctrl_file:
            ctrl_file.write(result)


def process_input(kwargs):
    print(kwargs)

    # create input folder
    input_folder_dir = './cycles/inputs/' + kwargs['unique_id']
    if not os.path.exists(input_folder_dir):
        os.makedirs(input_folder_dir)

    # Cycles operation file
    op_filename = _process_operation_file(kwargs, input_folder_dir)

    # Cycles control file
    _process_ctrl_file(kwargs, input_folder_dir, op_filename)

    return None

    # return {
    #     "cycles-data": "file:cyclesdata.csv",
    #     "land-input": "file:landinput.csv",
    #     "price": "file:price.csv",
    #     "production-cost": "file:productioncost.csv",
    #     "sim-price": "file:simprice.csv",
    #     "sim-production-cost": "file:simproductioncost.csv",
    #     "supply-elasticity": "file:supplyelasticity.csv",
    # }
