import itertools
import os
import re
from typing import List
import pandas as pd

'''
    This file provides functions to parse the output of MMPBSA.py file which is in .dat format
'''

calc_separator = '\n-------------------------------------------------------------------------------\n-------------------------------------------------------------------------------\n'
method_separators = {
    'gb': 'GENERALIZED BORN:',
    'gbnsr6': 'GENERALIZED BORN (GBNSR6):',
    'pb': 'POISSON BOLTZMANN:'
}

components_output = {
    'gb': {
        'structure_types': ['wildtype', 'mutation'],
        'structure_names': ['Complex', 'Receptor', 'Ligand', 'Differences'],
        'energy_types': ['VDWAALS', 'EEL', 'EGB', 'ESURF', 'G gas', 'G solv', 'total'],
        'calc_results': ['avg', 'std', 'std err']
    },
    'gbnsr6': {
        'structure_types': ['wildtype', 'mutation'],
        'structure_names': ['Complex', 'Receptor', 'Ligand', 'Differences'],
        'energy_types': ['VDWAALS', 'EEL', 'EGB', 'ESURF', 'G gas', 'G solv', 'total'],
        'calc_results': ['avg', 'std', 'std err']
    },
    'pb': {
        'structure_types': ['wildtype', 'mutation'],
        'structure_names': ['Complex', 'Receptor', 'Ligand', 'Differences'],
        'energy_types': ['VDWAALS', 'EEL', 'EPB', 'ENPOLAR', 'EDISPER', 'G gas', 'G solv', 'total'],
        'calc_results': ['avg', 'std', 'std err']
    }
}

def extract_result(args, config_params) -> None:
    output_name = args.output_name
    tmp_dir = config_params['amber']['tmp_path']

    final_arr = []
    working_dirs = os.listdir(tmp_dir)
    for working_dir in working_dirs:
        if not os.path.exists(f"{os.path.abspath(tmp_dir)}/{working_dir}/FINAL_RESULTS.dat"):
            print(f"Error happened in running alanine scanning in {os.path.abspath(tmp_dir)}/{working_dir}")
            continue
        final_arr.append(parse_file(f"{os.path.abspath(tmp_dir)}/{working_dir}/FINAL_RESULTS.dat", working_dir))

    df = pd.DataFrame(final_arr)
    df.to_csv(output_name, index=False)

def parse_file(file, working_dir):
    f = open(file, 'r')
    content = f.read()

    final_dict = {}
    final_dict.update({"working_dir": working_dir})
    for method in ['gb', 'pb', 'gbnsr6']:
        calc_content = content.split(method_separators[method])[1].split(calc_separator)[0] + \
                       content.split(method_separators[method])[2].split('RESULT OF ALANINE SCANNING')[0]
        final_dict.update(extract_components(calc_content, method))

    return final_dict

def extract_components(content: str, method: str) -> dict:
    cols = generate_combinations(method)
    nums = extract_numbers(content)
    return {cols[i]: nums[i] for i in range(len(cols))}


def extract_numbers(text):
    # Use regular expression to find all numbers in the text
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', text)
    return [float(num) for num in numbers]


def generate_combinations(method: str) -> List[str]:
    combinations = []
    for structure_type, structure_name, calc_method, energy_type, calc_result in itertools.product(
            components_output[method]['structure_types'], components_output[method]['structure_names'], [method],
            components_output[method]['energy_types'], components_output[method]['calc_results']):
        combination = f"{structure_name}_{structure_type}_{calc_method}_{energy_type}_{calc_result}"
        combinations.append(combination)
    return combinations
