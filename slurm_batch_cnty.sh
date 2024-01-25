#!/bin/bash

#SBATCH -t 01:00:00
#SBATCH -p normal_q
#SBATCH -N 1
#SBATCH -A ravt
# Job name:
#SBATCH --job-name=mcmc_runner
#SBATCH --output=R-%x.%j.out

module load Python

./venv/bin/python mcmc_runner_cnty.py -c ./data2020/settings_files/$1_cnty.ini -n 1 --start $SLURM_ARRAY_TASK_ID --steps 25000  --accept $2 --prefix $1_cnty_$2

