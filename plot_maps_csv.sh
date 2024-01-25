#!/bin/bash


module load Python

./venv/bin/python plot_maps_from_csv.py --file $1
