import argparse
from argparse import Namespace

def parse_main_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description="Tool for calculating EGB and EPB of biomolecules with alanine scanning mutations.")

    parser.add_argument(
        '--extract-result', '-e',
        type=bool,
        required=True,
        help='Indicates whether its time to run or extract the result after all jobs are finished'
    )
    parser.add_argument(
        '--wildtype-topology-file', '-w',
        type=str,
        required=False,
        help='Specify the topology file of the wildtype structure'
    )
    parser.add_argument(
        '--config-file', '-c',
        type=str,
        required=False,
        help='Specify the filename which includes configuration to run mutations'
    )
    parser.add_argument(
        '--output-name', '-o',
        type=str,
        required=False,
        help='Specify the output filename (should be in csv format)'
    )

    return parser.parse_args()

def parse_tleap_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description="Updates atom radiuses based on configuration file for amber-alanine-scan")

    parser.add_argument(
        '--config-file', '-c',
        type=str,
        required=True,
        help='Specify the filename which includes configuration to run mutations'
    )

    parser.add_argument(
        '--directory-prefix', '-w',
        type=str,
        required=True,
        help='MMPBSA directories prefix'
    )

    parser.add_argument(
        '--config-file', '-c',
        type=str,
        required=True,
        help='Specify the filename which includes configuration to run mutations'
    )

    return parser.parse_args()