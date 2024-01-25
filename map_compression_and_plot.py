import matplotlib.pyplot as plt
import csv
import pandas as pd
import geopandas as gpd
import matplotlib.patches as mpatches
from matplotlib import cm
import scipy.stats as ss
import helper_methods
import os
import matplotlib.colors as mcol
import matplotlib.cm as cm
#from calculate_bvap import calc_bvap



def plot_map_basic(shape_file, csv_file,fig_out_type):
    '''
    Input: shape_file for the region you want to plot
           csv_file - describing the district assignments of the region

    Output: A map with the districts colored.
    '''
 
    fig_out_filename = csv_file[:-4]+"map."+fig_out_type

    #print("Creating a basic map plot")
    # Read generic US county level shapefile for mapping
    gdf = gpd.read_file(shape_file)
    gdf = gdf.set_index('GEOID')
    df = pd.read_csv(csv_file, header = None, names = ['GEOID', 'District'], index_col = 'GEOID')
    # Initialize 'District' field in geodataframe
    gdf['District'] = 0
    for i in gdf.index:
        gdf['District'][i] = int(df['District'][int(i)])
    
    district_list = list(set(gdf['District']))
    district_list.sort()
#     for i,row in gdf.iterrows():
#         if gdf.loc[i,'District'] == 0:
#             gdf.drop(i,inplace=True)

    fig, ax = plt.subplots(1,1, figsize=(8,8))

    n = 0
    col_maps = []
    average_bvap = 0
    sum_cdf = 0
    for districts in district_list:
        col_map = mpatches.Patch(color=(1.0, 1.0, 0.6, 1.0), label=f"{districts}")
        col_maps.append(col_map)
 

    # Plot map based on District Assignment
    #gdf.plot(column='District', edgecolor='black', cmap="Accent", ax=ax)
    gdf.plot(column='District', edgecolor=None, cmap='tab20', ax=ax)
    plt.axis("off")
    plt.savefig(fig_out_filename, transparent=True)
    #plt.show()


def parse_data_desired_columns(data, other_cols = False):    
        #data = pd.read_csv(summary_file)
        # For information on data columns, see
        # https://www2.census.gov/programs-surveys/decennial/2020/technical-documentation/complete-tech-docs/summary-file/2020Census_PL94_171Redistricting_StatesTechDoc_English.pdf
        #
        # BVAP will record only voting age population that identifies as black alone
        # BVAP_tot will record voting age population that identifies at least partly as black
        bvap_total_columns = ['P0030004','P0030004','P0030011','P0030016','P0030017','P0030018','P0030019',
    'P0030027','P0030028','P0030029','P0030030','P0030037','P0030038', 'P0030039', 
    'P0030040', 'P0030041','P0030042']

        cols = ['P0010001','P0010004','P0030001','P0030004','P0040002']
        rename_cols = ['POP','BPOP','VAP','BVAP','BVAP_TOT', 'HVAP' ]
        if other_cols:
            cols = cols + other_cols
            rename_cols = rename_cols + other_cols
        #print(cols)
        master_data = data[cols]
        master_data = master_data.rename(columns={'P0010001':'POP','P0010004':'BPOP',
                                                  'P0030001':'VAP','P0030004':'BVAP', 'P0040002' : 'HVAP'})
        master_data['BVAP_TOT'] = sum(data[col] for col in bvap_total_columns )

        #master_data[rename_cols].to_csv(f'{output_subfolder}/{state}_{level}_demographics_2020.csv',index=False)
        return master_data[rename_cols]
    
def state_str(test_str):
    # initializing substrings
    sub1 = '../data/Southern_States/bg\\'
    sub2 = "\\"

    # getting index of substrings
    idx1 = test_str.index(sub1)
    idx2 = test_str[idx1 + len(sub1):].index(sub2)

    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1), idx1 + len(sub1)+idx2):
        res = res + test_str[idx]
    return res



def dissolve_to_districts(shape_file, csv_file, summarize = False, additional_data = False):
    '''
    Input: shape_file for the region you want to plot
           csv_file - describing the district assignments of the region
           summarize - True  - this will use just the columns that we interested in.
                       False - this will dissolve all columns from the shape file. 
            additional_data - if you want to add data that is not included in the shapefile, then you can provide a separate 
                            csv file with matching indices and new columns that of interest to add to the data.

    Output: A geopandas dataframe that contains information on the districts that was dissolved
            from the shapefile/census data and the assignment file
    '''
 
    
    
    #print("Creating a basic map plot")
    # Read generic US county level shapefile for mapping
    gdf = gpd.read_file(shape_file)
    gdf = gdf.set_index('GEOID')
    df = pd.read_csv(csv_file, header = None, names = ['GEOID', 'District'], index_col = 'GEOID')

    # Initialize 'District' field in geodataframe
    #gdf['District'] = 0
    #for i in gdf.index:
        #gdf['District'][i] = df['District'][i]
    gdf = pd.merge(gdf, df, left_index=True, right_index=True)
    if additional_data:
        additional_cols = ['R16', 'D16', 'L16','R20', 'D20', 'L20'] # should make this more general, but this works for what I need at the moment.
        for file in additional_data:
            df_add = pd.read_csv(file, index_col = 'GEOID')
            gdf = pd.merge(gdf, df_add, left_index=True, right_index=True)
        
    district_list = list(set(gdf['District']))
    district_list.sort()
    gdf_districts = gdf.dissolve(by='District', aggfunc='sum')
    gdf_districts['NAME'] = list(gdf_districts.index)
    
    
    #return [df, gdf, gdf_districts]

#     for i,row in gdf.iterrows():
#         if gdf.loc[i,'District'] == 0:
#             gdf.drop(i,inplace=True)


 

    # Plot map based on District Assignment
    #gdf.plot(column='District', edgecolor='black', cmap="Accent", ax=ax)
    
    points = gdf_districts['geometry'].apply(lambda x: x.representative_point().coords[:])
    gdf_districts['Representative_lat'] = [coords[0][0] for coords in points]
    gdf_districts['Representative_long'] = [coords[0][0] for coords in points]
     
    if summarize:
        other_cols = ['geometry', 'Representative_lat', 'Representative_long', 'NAME']
        if additional_data:
            other_cols += additional_cols
        #print(other_cols)
        gdf_districts = parse_data_desired_columns(gdf_districts, other_cols = other_cols)
        #add BVAP ratio
        gdf_districts['BVAP_ratio'] =gdf_districts['BVAP']/gdf_districts['VAP']
        gdf_districts['HVAP_ratio'] =gdf_districts['HVAP']/gdf_districts['VAP']
        gdf_districts['Black_reps'] =helper_methods.calculate_black_reps_list(gdf_districts)
        gdf_districts['Black_reps_rim'] =helper_methods.calculate_black_reps_rim_south_list(gdf_districts)
        gdf_districts['Black_reps_deep'] =helper_methods.calculate_black_reps_deep_south_list(gdf_districts)
        gdf_districts['Dem_PVI'] = helper_methods.pvi_list(gdf_districts)
        gdf_districts['Dem_prob'] =helper_methods.calculate_dem_prob_list(gdf_districts)
        gdf_districts['Rep_prob'] =helper_methods.calculate_rep_prob_list(gdf_districts)
        gdf_districts['Competitiveness'] =helper_methods.calculate_competitive_list(gdf_districts)
        gdf_districts['Competitive'] =helper_methods.calculate_num_competitive_list(gdf_districts)
        
        gdf = parse_data_desired_columns(gdf, other_cols = ['geometry', 'NAME'])
        #add BVAP ratio
        gdf['BVAP_ratio'] =gdf['BVAP']/gdf['VAP']
        gdf['HVAP_ratio'] =gdf['HVAP']/gdf['VAP']
    return df, gdf, gdf_districts
    
    
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
       
def compress_and_plot(state, csv_file, shape_file, additional_data):
    
    df, gdf, gdf_districts = dissolve_to_districts(shape_file, csv_file, summarize = True, additional_data = additional_data)

    gdf_districts.drop(columns = ['geometry']).to_csv(csv_file[:-4] + '_districts.csv')
    print(f"File saved: {csv_file[:-4] + '_districts.csv'}" )
    gdf_districts.to_file(csv_file[:-4] + '_districts.geojson', driver='GeoJSON')
    print(f"File saved: {csv_file[:-4] + '_districts.geojson'}" )
    

    # plot Political map


    # Make a user-defined colormap.
    cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",[adjust_lightness("r"),adjust_lightness("b")])
    cm2 = mcol.LinearSegmentedColormap.from_list("MyCmapName",[adjust_lightness("b"),adjust_lightness("r")])

    new_edgecolor = 'Black'
    new_cmap =cm1# 'BuPu' 
    data_col = 'Dem_prob'
    legend_on = True
    fig_out_type = 'png'

    plot_districts(gdf_districts,csv_file,fig_out_type, new_edgecolor, data_col, new_cmap, legend_on, num_color = 'white', vmin = 0, vmax = 1)


    # plot bvap map

    plot_districts(gdf_districts,csv_file,fig_out_type, new_edgecolor, 'BVAP_ratio', 'BuPu', legend_on, num_color = 'orange', vmin = 0, vmax = 0.7)

    # plot bvap overlay
    fig, ax = plt.subplots(1,1, figsize=(16,16))
    gdf.plot(column = 'BVAP_ratio', edgecolor=None, cmap='BuPu',ax = ax) 
    gdf_districts.geometry.boundary.plot(edgecolor = 'Black', linewidth = 2, ax = ax)
    gdf_districts.apply(lambda x: 
                 ax.annotate(text=x.NAME, xy=(x.Representative_lat, x.Representative_long), ha='center', color = 'orange',  weight='bold', size = 14), axis=1);
    ax.axis("off")


    fig_out_filename = csv_file[:-4]+'BVAP_ratio'+"_overlay."+fig_out_type
    plt.savefig(fig_out_filename, transparent=True)
    plt.close()
    print(f"Figure saved: {fig_out_filename}")


def plot_bvap(state, shape_file):
    
    gdf = gpd.read_file(shape_file)
    gdf = gdf.set_index('GEOID')

    

    # plot Political map


    # Make a user-defined colormap.
    #cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",[adjust_lightness("r"),adjust_lightness("b")])
    #cm2 = mcol.LinearSegmentedColormap.from_list("MyCmapName",[adjust_lightness("b"),adjust_lightness("r")])

    #new_edgecolor = 'Black'
    #new_cmap =cm1# 'BuPu' 
    #data_col = 'Dem_prob'
    legend_on = True
    fig_out_type = 'png'

    #plot_districts(gdf_districts,csv_file,fig_out_type, new_edgecolor, data_col, new_cmap, legend_on, num_color = 'white', vmin = 0, vmax = 1)


    # plot bvap overlay
    fig, ax = plt.subplots(1,1, figsize=(16,16))
    gdf = parse_data_desired_columns(gdf, other_cols = ['geometry', 'NAME'])
        #add BVAP ratio
    gdf['BVAP_ratio'] =gdf['BVAP']/gdf['VAP']
    gdf.plot(column = 'BVAP_ratio', edgecolor=None, cmap='BuPu',ax = ax) 
    gdf_state = gdf.dissolve()
    gdf_state.geometry.boundary.plot(edgecolor = 'Black', linewidth = 2, ax = ax)
    #gdf_districts.apply(lambda x: 
    #             ax.annotate(text=x.NAME, xy=(x.Representative_lat, x.Representative_long), ha='center', color = 'orange',  weight='bold', size = 14), axis=1);
    ax.axis("off")


    fig_out_filename = state+"."+fig_out_type
    plt.savefig(fig_out_filename, transparent=True)
    plt.close()
    print(f"Figure saved: {fig_out_filename}")
    
if __name__ == "__main__":    

    state = 'GA'
    for state in ['LA', 'GA', 'VA', 'SC', 'NC', 'AL', 'MS', 'MD', 'TN']:
    #objective = 'bvap_deep95_pp5'
    #csv_file = f'outputs/bg/{state.upper()}/GA_bg_bvap_deep75_pp25_25.0k_01.csv'
         shape_file = f'data2020/shapefiles/{state.lower()}_pl2020_bg_shp/{state.lower()}_pl2020_bg.shp'

    #additional_data = [f'data2020/partisan_data/bg/{state.lower()}_bg_census_2020_voter_data_2020.csv', 
    #                   f'data2020/partisan_data/bg/{state.lower()}_bg_census_2020_voter_data_2016.csv']


    #compress_and_plot(state, csv_file, shape_file, additional_data)
         plot_bvap(state, shape_file)



