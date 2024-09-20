import os
import sys
from argparse import Namespace

import yaml
import logging

from lib.variables import Element

def setup_logging():
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            # Convert the pathname to a relative path
            record.pathname = os.path.relpath(record.pathname)
            return super().format(record)

    # Configure the logging system
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level to DEBUG to capture all types of log messages
        format='%(pathname)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to standard output
            logging.FileHandler('app.log', mode='w')  # Log to a file (app.log)
        ]
    )

    # Replace the default formatter with the custom formatter
    for handler in logging.getLogger().handlers:
        handler.setFormatter(CustomFormatter('%(pathname)s - %(levelname)s - %(message)s'))

def check_compatibility():
    try:
        from parmed.amber import AmberParm
    except Exception as e:
        logging.error(e)
        exit(-1)

    amberhome = os.getenv('AMBERHOME')

    if not amberhome:
        logging.error("Environment variable AMBERHOME is not set.")
        exit(-1)

    logging.info(f"AMBERHOME is set to: {amberhome}")

def parse_config_yml(config_file: str) -> dict:
    # Load the YAML file
    with open(config_file, 'r') as file:
        data = yaml.safe_load(file)

    if 'atom_radii' in data['scan']:
        data['scan']['atom_radii'] = Element.map_atom_radii_dict(data['scan']['atom_radii'])
    if not data['scan']['only_parameterization']:
        data['amber']['trajectory_path'] = os.path.abspath(data['amber']['trajectory_path'])
    return data

def check_exist_data(args: Namespace, config_params: dict):
    base_name = args.wildtype_topology_file
    tleap_in = config_params['amber']['input_tleap_config']
    mmpbsa_in = config_params['amber']['input_mmpbsa_config']
    mmpbsa_runner = config_params['runner']['mmpbsa_script']
    trajectory_path = config_params['amber']['trajectory_path']

    if not os.path.exists(base_name):
        logging.error(f"wildtype topology file not found: '{base_name}'")
        sys.exit(-1)
    if not os.path.exists(tleap_in):
        logging.error(f"tLEAP input file not found: '{tleap_in}'")
        sys.exit(-1)
    if not os.path.exists(mmpbsa_in):
        logging.error(f"MMPBSA input file not found: '{mmpbsa_in}'")
        sys.exit(-1)
    if not os.path.exists(mmpbsa_runner):
        logging.error(f"MMPBSA runner input file not found: '{mmpbsa_in}'")
        sys.exit(-1)
    if not os.path.exists(trajectory_path) or len(os.listdir(trajectory_path)) == 0:
        logging.error(f"trajectory directory is wrong: '{trajectory_path}'")
        if not config_params['scan']['only_parameterization']:
            exit(-1)
