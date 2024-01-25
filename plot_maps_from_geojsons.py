import os
import argparse
import math
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import cm
import matplotlib.colors as mcol



def plot_districts(gdf_districts,file,fig_out_type, new_edgecolor, data_col, new_cmap, legend_on, num_color = 'r', vmin = None, vmax = None):    
    fig_out_filename = file[:-8]+"_"+data_col+"."+fig_out_type
    print(f"Output filename: {fig_out_filename}")
    
    fig, ax = plt.subplots(1,1, figsize=(16,16))

    n = 0
    col_maps = []
    average_bvap = 0
    sum_cdf = 0
    district_list = list(gdf_districts.index)
    for districts in district_list:
        col_map = mpatches.Patch(color=(1.0, 1.0, 0.6, 1.0), label=f"{districts}")
        col_maps.append(col_map)
    # Set plotting options
    colormap = 'tab20'
    if new_cmap:
        colormap = new_cmap
    data_choice = 'Representative_lat'
    if data_col:
        data_choice = data_col
    edgecolor = 'None'
    if new_edgecolor:
        edgecolor = new_edgecolor
    
#     # create the colorbar
#     norm = colors.Normalize(vmin=0, vmax=1)
#     cbar = plt.cm.ScalarMappable(norm=norm, cmap='gist_earth_r')

#     # plot
#     fig, ax = plt.subplots(figsize=(15, 7))
#     gdf.plot(column='Index_power', cmap='gist_earth_r', legend=False, norm=norm, ax=ax) 

#     # add colorbar
#     ax_cbar = fig.colorbar(cbar, ax=ax)
    cbax = fig.add_axes([0.95, 0.3, 0.03, 0.39])   
    cbax.set_title(data_choice)
    
    if not vmin:
        vmin=min(gdf_districts[data_choice])
    if not vmax:
        vmax=max(gdf_districts[data_choice])
        
    sm = plt.cm.ScalarMappable(cmap=colormap, \
                norm=plt.Normalize(vmin=vmin, vmax=vmax))
    
    sm._A = []
    
    fig.colorbar(sm, cax=cbax)#, format="%d")
    # Plot
    gdf_districts.plot(column = data_choice, edgecolor=edgecolor, cmap=colormap, ax=ax, legend=False, 
                       vmin=vmin, vmax=vmax)  
    
#     colormap = "copper_r"   # add _r to reverse the colormap
#     ax = world.plot(column='pop_est', cmap=colormap, \
#                 figsize=[12,9], \
#                 vmin=min(world.pop_est), vmax=max(world.pop_est))
    
    #ax.set_title('World Population')
    #ax.grid() 
    
    #fig = ax.get_figure()
    # add colorbar axes to the figure
    # here, need trial-and-error to get [l,b,w,h] right
    # l:left, b:bottom, w:width, h:height; in normalized unit (0-1)


    # dont use: plt.tight_layout()
    #plt.show()
    
    #plt.legend(title="legend")
    # Annotate plot with numbering
    gdf_districts.apply(lambda x: 
             ax.annotate(text=x.NAME, xy=(x.Representative_lat, x.Representative_long), ha='center', color = num_color,  weight='bold', size = 14), axis=1);
    ax.axis("off")
    head, tail = os.path.split(file)
    #plt.title(data_choice)
    plt.savefig(fig_out_filename, transparent=True)
    print(f"Figure saved: {fig_out_filename}")
    # save the dissolved data
    plt.show() 
    # dissolve the data from the demographics file as well and add that to this data
    
def adjust_lightness(color, amount=1.2):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])





if __name__ == "__main__":    
    
    
    parser = argparse.ArgumentParser(description='Program to plot from geojson file.')

    parser.add_argument("--file", help="file with geojson to plot")

    args = parser.parse_args()

    
    
    filename = args.file
    
    if filename[-3:]=='txt':
        with open(filename) as file:
            lines = file.readlines()
            files = [line.rstrip() for line in lines]
        
    if filename[-7:]=='geojson':
        files = [filename]
    
    
    for file in files:
        gdf = gpd.read_file(file)

        # Make first plot for BVAP Ratio
        new_edgecolor = 'Black'
        new_cmap ='BuPu' 
        data_col = 'BVAP_ratio'
        legend_on = True
        fig_out_type = 'png'

        plot_districts(gdf,file,fig_out_type, new_edgecolor, data_col, new_cmap, legend_on, vmin = 0, vmax = 0.7)


        # plot Political map


        # Make a user-defined colormap.
        cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",[adjust_lightness("r"),adjust_lightness("b")])
        cm2 = mcol.LinearSegmentedColormap.from_list("MyCmapName",[adjust_lightness("b"),adjust_lightness("r")])

        new_edgecolor = 'Black'
        new_cmap =cm1# 'BuPu' 
        data_col = 'Dem_prob'
        legend_on = True
        fig_out_type = 'png'

        plot_districts(gdf,file,fig_out_type, new_edgecolor, data_col, new_cmap, legend_on, num_color = 'white', vmin = 0, vmax = 1)



