#!/bin/bash

module load Python

./venv/bin/python mcmc_runner_cnty.py -c ./data2020/settings_files/$3_cnty.ini -n 1 --steps $2  --accept $1 --prefix $3_cnty_$1

