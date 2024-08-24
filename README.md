# Amber Alanine Scanning

This library is designed to facilitate high-throughput Alanine scanning on ligand-receptor complexes. It automates several stages of the process, making it more efficient and user-friendly. Before using this tool, ensure you have AmberTools version 22 or later installed. Note that the main script is configured for Slurm. If your supercomputer uses a different job scheduler, you will need to modify the script accordingly.
<br>
## Dataset
This tool has been tested and validated using the SARS-CoV-2 structure to analyze the binding free energy of various mutations in the COVID-19 spike protein. Specifically, we utilized the crystal structure of the SARS-CoV-2 spike receptor-binding domain in complex with the ACE2 receptor, identified by the Protein Data Bank (PDB) ID 6m0j.

# How to run
First clone the repository, create a virtual environment for the Python > 3.8 and install the requirements.
```commandline
git clone
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Next, you need to write a configuration for your Alanine scanning protocol.
config.template.yml is a sample to configure scanning. 

### Configuration Attributes

#### amber:
- **`input_tleap_config`**: Path to the template input file for tLEAP, which parameterize the structures.
- **`input_mmpbsa_config`**: Path to the template input file for MMPBSA, which calculates the binding free energy.
- **`trajectory_path`**: Directory where the simulation trajectory files are stored.
- **`tmp_path`**: Directory for temporary files created during the processing.

#### runner:
- **`memory_size`**: The amount of memory (in MB) allocated for the process.
- **`cpu_cores`**: The number of CPU cores to use for parallel processing.
- **`tleap_batch_size`**: Number of systems to parameterize in one batch using tLEAP.
- **`mmpbsa_script`**: Path to the Slurm job script template for running MMPBSA.

#### scan:
- **`mutations`**: List of mutation positions (residue numbers) to perform Alanine scanning on.
- **`only_parameterization`**: If true, the script will only parameterize the systems and exit, without running MMPBSA.
- **`skip_parameterization`**: If true, the script will skip the parameterization step and directly proceed to MMPBSA output files stored in temporary folder.
- **`update_atom_radii`**: If true, custom atom radii will be applied during parameterization.
- **`atom_radii`**: List of custom atomic radii to be used in the parameterization (element and radius pairs).

You need to run simulation of wildtype complex separately and only use the path to them here.
Make sure to use same parameters for tLEAP as you use here so parameterization of mutation files not get error.
Also, you need to provide PDB file of your wildtype structure because mutations are performed on PDB file first, then the PDB file is parameterized.