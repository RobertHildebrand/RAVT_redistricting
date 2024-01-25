#!/bin/bash

#SBATCH -t 19:30:00
#SBATCH -p normal_q
#SBATCH -N 1
#SBATCH -A ravt

module load Python

./venv/bin/python mcmc_runner_all.py -c ./data2020/settings_files/$1.ini -n 6 --start $SLURM_ARRAY_TASK_ID --steps 25000  --accept $2 --prefix $1_bg_$2
