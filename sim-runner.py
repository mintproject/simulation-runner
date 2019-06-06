#!/usr/bin/env python3
"""Simulation RUnner."""

import argparse
import logging
import os

import _utils

log = logging.getLogger()


def run_simulations(wings_config, model_name, simulation_matrix, **kwargs):
    if kwargs["debug"]:
        os.environ["WINGS_DEBUG"] = "1"

    model = _utils.load_module(model_name)
    with _utils.cli(wings_config, model.__WINGS_TEMPLATE_NAME__) as (data, planner):
        model.wings = {"data": data, "planner": planner}
        _throttled_func = _utils.throttle(
            kwargs.get("chunk_size", 15), kwargs.get("chunk_size", 60)
        )(model.process_input)
        for row in _utils.simulation_matrix(simulation_matrix):
            log.debug("Simulation Matrix Row: %s" % row)
            args = _throttled_func(row)
            if args is not None:
                _utils.upload_files(model, args)
                _utils.run_template(model, args)


def _main():
    parser = argparse.ArgumentParser(
        description="Run WINGS template based on simulation matrix."
    )
    parser.add_argument(
        "-c",
        "--wings-config",
        dest="wings_config",
        required=True,
        help="WINGS Configuration File",
    )
    parser.add_argument(
        "-m", "--model-name", dest="model_name", required=True, help="Model to run"
    )
    parser.add_argument(
        "-c",
        "--throttle-chunk",
        dest="chunk_size",
        type=int,
        default=15,
        help="Chunk size",
    )
    parser.add_argument(
        "-w", "--throttle-wait", dest="wait", type=int, default=60, help="Wait time"
    )
    parser.add_argument(
        "-d", "--debug", dest="debug", default=False, action="store_true", help="Debug"
    )
    parser.add_argument("simulation_matrix", help="Simulation Matrix")
    args = parser.parse_args()
    run_simulations(**vars(args))


if __name__ == "__main__":
    _utils.init_logger()
    try:
        _main()
        log.info("Done")
    except Exception as e:
        log.exception(e)
