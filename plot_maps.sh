#!/bin/bash


module load Python

./venv/bin/python plot_maps_from_geojsons.py --file $1
