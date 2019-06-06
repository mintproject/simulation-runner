# -*- coding: utf-8 -*-

import configparser
import functools
import importlib
import logging
import os
import time
from contextlib import contextmanager
from csv import DictReader, Sniffer
from pathlib import Path

import wings

log = logging.getLogger()


def init_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def wings_config(wings_config):
    if not Path(wings_config).exists():
        raise ValueError("Invalid wings_config")

    config = configparser.ConfigParser()
    config.read(wings_config)
    return (
        {
            "server": config["default"]["serverWings"].strip("/"),
            "internal_server": config["default"]["exportWingsURL"],
            "userid": config["default"]["userWings"],
            "domain": config["default"]["domainWings"],
        },
        config["default"]["passwordWings"],
    )


def load_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        log.error("Model <%s> not found" % module_name)
        raise


@contextmanager
def cli(cfg, template):
    config, passwd = wings_config(cfg)
    data = wings.ManageData(**config)
    planner = wings.Planner(template=template, **config)
    with login(data, passwd) as data, login(planner, passwd) as planner:
        yield data, planner


@contextmanager
def login(w, password):
    if w.login(password):
        try:
            yield w
        finally:
            log.debug("Logout")
            w.logout()


def upload_files(model, args):
    log.debug("Upload Files")

    cli = model.wings["data"]
    for k, v in args.items():
        if isinstance(v, Path):
            t = model.__IO_TYPES__[k]
            log.info("Upload file <%s> of type <%s>" % (v, t))
            cli.upload_data_for_type(v.resolve(), t)


def run_template(model, args):
    debug = os.getenv("WINGS_DEBUG", False)
    log.debug("Run Template")
    run_args = args.copy()
    for k, v in args.items():
        if isinstance(v, Path):
            run_args[k] = "file:%s" % v.name

    cli = model.wings["planner"]
    ret = cli.get_expansions(run_args)
    if ret and ret["success"]:
        templates = ret["data"]["templates"]
        log.debug(len(templates))
        if debug is False:
            runid = cli.run_workflow(templates[0], ret["data"]["seed"])
            log.info("Started run with id <%s>" % runid)
        else:
            log.info("Debug mode enabled, skipping running template")


def throttle(chunk_size=15, wait=60):
    def wrap(f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            rv = f(*args)
            for i, r in enumerate(rv):
                if i % chunk_size == 0 and i != 0:
                    log.info("Sleep for %d seconds before iteration <%d>" % (wait, i))
                    time.sleep(wait)
                yield r

        return wrapped_f

    return wrap


def simulation_matrix(sim_file):
    if not Path(sim_file).exists():
        raise ValueError("Invalid simulation-matrix")

    with open(sim_file) as csvfile:
        dialect = Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = DictReader(csvfile, dialect=dialect)
        for row in reader:
            yield row
