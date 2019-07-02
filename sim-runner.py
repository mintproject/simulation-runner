#!/usr/bin/env python3
"""Simulation RUnner."""

import argparse
import logging
import os

import _utils

log = logging.getLogger()


def run_simulations(
    wings_config, model_name, simulation_matrix, debug=False, dry_run=False, **kwargs
):
    model = _utils.load_module(model_name)
    with _utils.cli(wings_config, model.__WINGS_TEMPLATE_NAME__) as (data, planner):
        model.wings = {"data": data, "planner": planner}
        _throttled_func = _utils.throttle(
            kwargs.get("chunk_size", 15), kwargs.get("sleep", 60)
        )(model.process_input)
        for row in _utils.simulation_matrix(simulation_matrix):
            log.debug("Simulation Matrix Row: %s" % row)
            args = _throttled_func(row)
            if args is not None and dry_run is False:
                _utils.upload_files(model, args)
                _utils.run_template(model, args)

            if args is None:
                log.info("process_input returned None, skipping")

            if args is not None and dry_run:
                log.info("dry-run mode, skipping")


def _main():
    parser = argparse.ArgumentParser(
        description="Run WINGS template based on simulation matrix."
    )
    parser.add_argument(
        "-w",
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
        "-s", "--throttle-sleep", dest="sleep", type=int, default=60, help="Sleep time"
    )
    parser.add_argument(
        "-d", "--debug", dest="debug", default=False, action="store_true", help="Debug"
    )
    parser.add_argument(
        "--dry-run", dest="dry_run", default=False, action="store_true", help="Dry run"
    )
    parser.add_argument("simulation_matrix", help="Simulation Matrix")
    args = parser.parse_args()
    if args.debug:
        os.environ["WINGS_DEBUG"] = "1"
    _utils.init_logger()

    run_simulations(**vars(args))


if __name__ == "__main__":
    try:
        _main()
        log.info("Done")
    except Exception as e:
        log.exception(e)
