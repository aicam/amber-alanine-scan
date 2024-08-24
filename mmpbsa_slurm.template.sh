#!/bin/bash

echo "done 123"
exit 0

#SBATCH --job-name={job_name}
#SBATCH --partition=cpu
#SBATCH --mem={memory_size}
#SBATCH --cpus-per-task={cpu_cores}
#SBATCH --output=output.log
#SBATCH --error=error.log
#SBATCH --time=72:00:00

module load amber

$AMBERHOME/bin/MMPBSA.py \
  -i mmpbsa.in \
  -o FINAL_RESULTS.dat \
 -sp wildtype_complex_solvated.prmtop \
 -cp wildtype_complex.prmtop \
 -rp wildtype_receptor.prmtop \
 -lp wildtype_ligand.prmtop \
 -y {trajectory_path}/*.mdcrd \
 -mc mutation_complex.prmtop \
 -ml mutation_ligand.prmtop