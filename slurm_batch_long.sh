#!/bin/bash

#SBATCH -t 10:30:00
#SBATCH -p normal_q
#SBATCH -N 1
#SBATCH -A ravt

module load Python

./venv/bin/python mcmc_runner.py -c ./data2020/settings_files/$1.ini -n 1 --start $SLURM_ARRAY_TASK_ID --steps 100000  --accept $2 --prefix $1_bg_$2
