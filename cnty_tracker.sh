#!/bin/bash

squeue -A ravt

module load Python

./venv/bin/python cnty_results_tracker.py --south $1 --todo write_next
