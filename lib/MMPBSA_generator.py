import logging
import os
import shutil
import sys
from argparse import Namespace
from typing import List

def generate_directories(args: Namespace, config_params: dict) -> List[str]:
    '''
    Generates all directories each with all materials needed for the MMPBSA.py
    :param config_params: configuration parameters coming from YAML file
    :param args: command line arguments
    '''

    base_name = args.wildtype_topology_file
    mut_args = config_params['scan']['mutations']
    base_dir = config_params['amber']['tmp_path']
    tleap_in = config_params['amber']['input_tleap_config']
    mmpbsa_in = config_params['amber']['input_mmpbsa_config']
    mmpbsa_runner = config_params['runner']['mmpbsa_script']
    trajectory_path = config_params['amber']['trajectory_path']
    memory_size = config_params['runner']['memory_size']
    cpu_cores = config_params['runner']['cpu_cores']

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    wildtype_name = base_name.split('/')[-1].split('.')[0]

    wildtype_complex_lines, wildtype_receptor_lines, wildtype_ligand_lines = split_pdb_structures(base_name)
    logging.info(f"Generated {len(wildtype_receptor_lines)} atoms for receptor and {len(wildtype_ligand_lines)} atoms for ligand")

    if len(wildtype_receptor_lines) <= len(wildtype_ligand_lines):
        logging.warning("Receptor has fewer atoms than ligand, make sure to put receptor on top of PDB (before TER) and ligand after that")

    working_dirs = []
    for mut_arg in mut_args:
        working_dir = f"{base_dir}/{wildtype_name}-{mut_arg}"
        working_dirs.append(working_dir)
        os.makedirs(working_dir, exist_ok=True)

        mutated_ligand_lines = mutate(wildtype_ligand_lines, str(mut_arg))
        mutated_complex_lines = wildtype_receptor_lines + ["TER\n"] + mutated_ligand_lines

        with open(f"{working_dir}/wildtype_complex.pdb", 'w') as f:
            f.writelines(wildtype_complex_lines)
        with open(f"{working_dir}/wildtype_ligand.pdb", 'w') as f:
            f.writelines(wildtype_ligand_lines)
        with open(f"{working_dir}/wildtype_receptor.pdb", 'w') as f:
            f.writelines(wildtype_receptor_lines)
        with open(f"{working_dir}/mutation_ligand.pdb", 'w') as f:
            f.writelines(mutated_ligand_lines)
        with open(f"{working_dir}/mutation_complex.pdb", 'w') as f:
            f.writelines(mutated_complex_lines)
        shutil.copy(tleap_in, f"{working_dir}/tleap.in")
        shutil.copy(mmpbsa_in, f"{working_dir}/mmpbsa.in")
        with open(mmpbsa_runner, 'r') as runner:
            content = ''.join(runner.readlines())
            content = content.replace("{job_name}", f"alanine-scanning-{mut_arg}")
            content = content.replace("{trajectory_path}", trajectory_path)
            content = content.replace("{memory_size}", str(memory_size))
            content = content.replace("{cpu_cores}", str(cpu_cores))
            with open(f"{working_dir}/mmpbsa_runner.sh", 'w') as local:
                local.write(content)

    logging.info(f"{len(mut_args)} directories for running generated")

    return working_dirs



def split_pdb_structures(pdb: str):
    '''
    Split receptor and ligand
    :param pdb: path to complex PDB file
    :return: receptor and ligand lines (from complex PDB file)
    '''
    pdb_lines = open(pdb, 'r').readlines()
    complex = []
    receptor = []
    ligand = []
    mode = 'receptor'

    for line in pdb_lines:
        if mode == 'receptor' and line.startswith('TER'):
            complex.append(line)
            mode = 'ligand'
            continue
        if mode == 'ligand' and line.startswith('TER'):
            logging.error("Found 2 TER in PDB file, remove extra one and run again")
            exit(1)

        if not line.startswith('ATOM') and not line.startswith('HETATM'):
            continue
        if line.startswith("HETATM"):
            logging.warning("Found HETATM in structure file. These types of atoms typically cause error on running tLEAP.")

        if mode == 'receptor':
            receptor.append(line)
        else:
            ligand.append(line)

        complex.append(line)
    return complex, receptor, ligand


def mutate(lines: List[str], idx: str) -> List[str]:
    '''
    Mutate a set of lines of a PDB
    Caution: a single structure with unique residue number (idx) should be passed to this function only
    :param lines: lines of PDB file
    :param idx: residue number
    :return: mutated lines of PDB file
    '''
    counter = 0
    records = ('ATOM', 'HETATM')
    mutated = []

    for line in lines:
        if line.startswith(records):

            if line[22:26].strip() == idx:
                if (counter <= 4) and (line[16] == "A" or line[16] == " "):  # count for ALA
                    new_line = line[:16] + "ALA".rjust(4) + line[20:]
                    mutated.append(new_line)
                    counter = counter + 1
                    continue
                else:
                    continue
        mutated.append(line)

    return mutated
