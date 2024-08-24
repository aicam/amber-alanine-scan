import logging
import os
import subprocess
import time
from argparse import Namespace
from concurrent.futures import as_completed, ProcessPoolExecutor
from typing import List

from parmed.amber import AmberParm

def run_tleap(working_dirs: List[str], args: Namespace, config_params: dict) -> None:
    batch_size = config_params['runner']['tleap_batch_size']
    batches = [working_dirs[i:i + batch_size] for i in range(0, len(working_dirs), batch_size)]

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_batch, batch, args, config_params): batch for batch in batches}

        for future in as_completed(futures):
            batch = futures[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing batch {batch}: {e}")
            else:
                logging.info(f"Batch {batch} processed successfully")

def run_MMPBSA(working_dirs: List[str]) -> None:
    for working_dir in working_dirs:
        origin_dir = os.getcwd()
        os.chdir(working_dir)
        run_slurm_job("mmpbsa_runner.sh")
        os.chdir(origin_dir)


def process_batch(batch: List[str], args: Namespace, config_params: dict) -> None:
    for working_dir in batch:
        origin_dir = os.getcwd()
        os.chdir(working_dir)
        err, num_errs = run_tleap_cli("tleap.in")

        # Topology files to update radii in them
        topologies_list = [
            'mutation_complex.prmtop', 'mutation_ligand.prmtop', 'wildtype_receptor.prmtop',
            'wildtype_ligand.prmtop', 'wildtype_complex.prmtop', 'wildtype_complex_solvated.prmtop'
        ]

        if num_errs > 0:
            logging.error(f"tLEAP failed on parameterizing files with log {err}")
            exit(-1)
        if config_params['scan']['update_atom_radii']:
            for topology_file in topologies_list:
                update_radii(topology_file, config_params['scan']['atom_radii'])
        os.chdir(origin_dir)

        logging.info(f"Parameterization of PDB files in {working_dir} finished")

def run_tleap_cli(tleap_in: str) -> (str, int):
    # Run the command
    result = subprocess.run(f"tleap -s -f {tleap_in}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode()
    num_errors = int(stdout.split("Exiting LEaP: Errors = ")[1].split(";")[0].replace(' ', ''))
    return stdout, num_errors

def update_radii(topology_file: str, radiis: dict):
    '''
        This function is used to update atom radius based on opt standard
        :param topology_file: path to the topology file
        :radiis: list of atom radiis
        :return: replace the topology file with the new one
        '''
    parm = AmberParm(topology_file)
    for i, atom in enumerate(parm.atoms):
        if atom.atomic_number in radiis.keys(): parm.atoms[i].solvent_radius = radiis[atom.atomic_number]

    os.remove(topology_file)
    parm.write_parm(topology_file)


def run_slurm_job(script_path: str):
    # Run the sbatch command
    result = subprocess.run(['sbatch', script_path], capture_output=True, text=True)

    dir_name = '/'.join(script_path.split('/')[:-1])

    # Check if the sbatch command was successful
    if result.returncode == 0:
        # Extract job ID from the sbatch output
        job_id = result.stdout.strip().split()[-1]
        logging.info(f"Job submitted successfully in directory {dir_name} with job id {job_id}.")
    else:
        logging.error(f"Failed to submit job the job for directory {dir_name}: {result.stderr}")
        exit(-1)
