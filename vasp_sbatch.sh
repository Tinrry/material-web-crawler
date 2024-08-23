#!/bin/bash

#SBATCH --job-name=vasp
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=12:30:00
#SBATCH --partition=part1
#SBATCH --exclusive
#SBATCH --output=vasp.%j.out
#SBATCH --error=vasp.%j.err

module load vasp
time mpirun -n 32 vasp_std
