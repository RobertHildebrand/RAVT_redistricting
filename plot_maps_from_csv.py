import os
import argparse
import math
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
import matplotlib.colors as mcol
import map_compression_and_plot
if __name__ == "__main__":   
    parser = argparse.ArgumentParser(description='Program to plot from geojson file.')

    parser.add_argument("--file", help="file with geojson to plot")

    args = parser.parse_args()

    
    
    filename = args.file
    
    if filename[-3:]=='txt':
        with open(filename) as file:
            lines = file.readlines()
            files = [line.rstrip() for line in lines]
    state = files[0]             
    shape_file = f'data2020/shapefiles/{state.lower()}_pl2020_bg_shp/{state.lower()}_pl2020_bg.shp'
    additional_data = [f'data2020/partisan_data/bg/{state.lower()}_bg_census_2020_voter_data_2020.csv', 
                       f'data2020/partisan_data/bg/{state.lower()}_bg_census_2020_voter_data_2016.csv']
    
    for file in files[1:]:
        csv_file = file
        map_compression_and_plot.compress_and_plot(state,  csv_file, shape_file, additional_data)
