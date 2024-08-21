#!/bin/bash

#SBATCH --job-name=vasp
#SBATCH --nodes=16
#SBATCH --ntasks-per-nodes=32
#SBATCH --time=12:30:00
#SBATCH --partition=part1
#SBATCH --exclusive
#SBATCH --output=vasp.%j.out
#SBATCH --error=vasp.%j.err

module load vasp mpi
time mpirun vasp_std
