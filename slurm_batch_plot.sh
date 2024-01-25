#!/bin/bash

#SBATCH -t 05:30:00
#SBATCH -p normal_q
#SBATCH -N 1
#SBATCH -A ravt
# Job name:
#SBATCH --job-name=plot

module load Python

./venv/bin/python plot_maps_helper.py --states $1