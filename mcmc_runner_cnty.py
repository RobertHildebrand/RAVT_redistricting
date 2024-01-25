print("Loading packages")
import random, math, csv, os, time, json
from datetime import datetime

from functools import partial
from inspect import getmembers, isfunction, getmodule
from collections import OrderedDict
from timeout import timeout, TimeoutError

import networkx as nx

import scipy.stats as stats
print("Loading gerrychain things")
from gerrychain import Graph, Partition, Election, GeographicPartition
from gerrychain.graph.geo import GeometryError
from gerrychain.updaters import Tally, cut_edges, county_splits
from gerrychain.metrics import polsby_popper

from gerrychain.tree import recursive_tree_part, bipartition_tree_random, bipartition_tree
from gerrychain import MarkovChain
from gerrychain.constraints import (single_flip_contiguous, 
            contiguous_bfs, 
            within_percent_of_ideal_population,
            UpperBound, 
            contiguous, 
            no_worse_L_minus_1_polsby_popper, 
            no_worse_L1_reciprocal_polsby_popper)
from gerrychain.accept import always_accept
print("Loading acceptance functions and partitioning functions")
import acceptance_functions
acceptance_methods = [m[0] for m in getmembers(acceptance_functions, isfunction) if m[0][0] != '_' and getmodule(m[1]).__name__ == 'acceptance_functions']
import partitioning_functions
partitioning_methods = [m[0] for m in getmembers(partitioning_functions, isfunction) if m[0][0] != '_' and getmodule(m[1]).__name__ == 'partitioning_functions']
print("Loading helper_methods")
import helper_methods
import map_compression_and_plot


class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if key in self and key=='data':
            if isinstance(value, list):
                self[key].extend(value)
                return
            elif isinstance(value,str):
                return # ignore conversion list to string (line 554)
        super().__setitem__(key, value)

class RatioTally(Tally):
    """A modified version of the gerrychain tally that tracks a ratio of two values"""
    def __init__(self, fields, alias=None):
        self.fields = fields
        if alias==None:
            alias = fields[0]+"_ratio"
        self.alias = alias
        
    def __call__(self, partition):
        return {part:float(partition[self.fields[0]][part])/partition[self.fields[1]][part] for part in partition[self.fields[0]].keys()}

    
# As a reminder, this was the old formula:
# Partisan Gerrymandering and Competitiveness Objectives

# PVI = 2016𝐷𝑒𝑚𝑇𝑤𝑜𝑃𝑎𝑟𝑡𝑦 + 2012𝐷𝑒𝑚𝑇𝑤𝑜𝑃𝑎𝑟𝑡𝑦 ∗ 50 − 51.54 

# This should be the new formula that we us going forward when working with 2020 data:

# PVI= 2020𝐷𝑒𝑚𝑇𝑤𝑜𝑃𝑎𝑟𝑡𝑦 + 2016𝐷𝑒𝑚𝑇𝑤𝑜𝑃𝑎𝑟𝑡𝑦 ∗ 50 − 51.69
    
class PVITally(Tally):
    def __init__(self, fields, bias=51.69, alias=None):
        self.fields = fields
        self.bias = bias
        if alias == None:
            alias = fields[0] + "_PVI"
        self.alias = alias

    def __call__(self, partition):
        partisan_ratio_Y1 = {part: float(partition[self.fields[0]][part] / (partition[self.fields[0]][part] + partition[self.fields[1]][part])) for part in partition[self.fields[0]].keys()}
        
        partisan_ratio_Y2 = {part: float(partition[self.fields[2]][part] / (partition[self.fields[2]][part] + partition[self.fields[3]][part])) for part in partition[self.fields[0]].keys()}

        return {part: ((partisan_ratio_Y1[part] + partisan_ratio_Y2[part]) * 50) - self.bias for part in partition[self.fields[0]].keys()}

def stripsplit(input): return input.strip().split(',')
        
def load_geometry(geometry, no_json=False):
    if geometry is None:
        print("Error: You must include a geometry file (either shapefile or pre-processed json) to run on")
        exit()
        
    # If there are multiple geometries from the settings file, grab the last one that isn't blank
    if isinstance(args.geometry, list): 
        args.geometry = [i for i in args.geometry if i != ''][-1]
    
    
    # Load in the geometry file
    if geometry[-4:] == '.shp':
        graph = parse_shapefile(geometry, no_json)
    elif geometry[-5:] == '.json':
        graph = Graph.from_json(geometry)
    else:
        print(f"Error: Unsupported geometry file type for '{args.geometry}'.  Please supply either a Shapefile (.shp) or a JSON (.json) as input.")
        exit()
    return graph

def parse_shapefile(filename, no_json=True):
    try:
        graph = Graph.from_file(filename)#, ignore_errors=True)
    except GeometryError as e:
        print(f"Hit a geometry error '{e}', ignoring")
        graph = Graph.from_file(filename, ignore_errors=True)
    
    nodelist = list(graph.nodes().keys())
    
    if 'block_grp' in graph.nodes()[nodelist[0]]:
        nodemap = {n:graph.nodes()[n]['block_grp'] for n in nodelist}
    else:
        nodemap = {n:graph.nodes()[n]['GEOID'] for n in nodelist}
    graph = nx.relabel_nodes(graph,nodemap)
    
    if not no_json:
        graph.to_json(f'{filename.split(".")[0]}.json')
        
    return graph
    
@timeout(600)
def _timeout_wrapper(*args, **kwargs):
    #print(f'Random nuumber: {random.randint(1,100000)}')
    return recursive_tree_part(*args, **kwargs)
    
def partition_with_timeout(graph, districts, target=None, population_field=None, epsilon=0.02):
    #If districts is an int, make it a list
    if isinstance(districts, int):
        districts = range(1,districts+1)
    d_list = districts
    pop_field = population_field if population_field else "POP"
    
    p = None
    print("Creating initial partition")
    while p is None:
        try:
            random.seed()
            s = time.time()
            p = _timeout_wrapper(graph, d_list, target, pop_field, epsilon, node_repeats=5, method=bipartition_tree_random)
            print(f'Partitioning took {time.time()-s} seconds')
        except TimeoutError as e:
            print("Timed out, re-trying initial partition")
            p = None
        except KeyboardInterrupt as e:
            print("Caught kill command")
            time.sleep(1)
            return None
    return p

    
def run_markov_chain(proposal, constraints, acceptance, initial_state, total_steps):
    count = [0,[]]
    prop = partial(proposal, count=count)
    
    chain = MarkovChain(
        proposal=prop, 
        constraints=constraints,
        accept=acceptance,
        initial_state=initial_state,
        total_steps=total_steps)
        
    for i,partition in enumerate(chain):
        print(f'{"".join(count[1])}: {i}')
        #print(f'Track: {i}, {helper_methods.calculate_black_reps_deep_south(partition)}')
        if i>0: 
            if count[1][-1] == '&': break
        count[0] = i
        count[1] = []
        
        
    return chain.state
        



if __name__ == "__main__":
    import argparse, configparser
    print("Starting new run")    
    settings = {
        'no_json': False,
        'data': [],
        'number_of_runs': 1,
        'steps': 1000,
        'start': 0,
        'population_tolerance': 0.02,
        }
    
    print("Load and parse the config file, if there is one, as default settings")
    conf_parser = argparse.ArgumentParser(description="Basic description text", add_help=False)
    conf_parser.add_argument('-c', "--config", dest="config_file", default="", type=str, help="A config file to read settings from")
    args,ignore = conf_parser.parse_known_args()
    if args.config_file:
        iniparse = configparser.RawConfigParser(dict_type=MultiOrderedDict, strict=False)
        iniparse.read(args.config_file)
        for group in iniparse.sections():
            settings.update(iniparse.items(group))
    
    print(settings)


    
    parser = argparse.ArgumentParser(parents=[conf_parser])
    parser.set_defaults(**settings)
    
    inputs = parser.add_argument_group('Inputs')
    inputs.add_argument('-g', '--geometry', help="The input geometry to run on, in shapefile or network graph json format (required)")
    inputs.add_argument('--no-json', action="store_true", help="Don't save a json export of the network graph (only relevant if the geometry is a shapefile)")
    inputs.add_argument('--only-json', action="store_true", help="Exit immediately after loading the shapefile and creating a json, before attempting to run anything else.")
    inputs.add_argument('--input_districts', help="An input district assignment to use as the initial seed")
    inputs.add_argument('-d', '--data', action="append", nargs=4, metavar=('FILE','KEY_COL','VALUE_COL','NAME'), help="Load CSV data files with additional values, where FILE is the filename, KEY_COL is the unique ids to match against, VALUE_COL is the values to add, and NAME is the name to use within the system.  Columns are either names (from the first row of the file) or a zero-indexed integer; they should both be one or the other.")
    
    iteration = parser.add_argument_group('Iteration')
    iteration.add_argument('-n', '--number_of_runs', type=int, help='The number of simulation runs to execute')
    iteration.add_argument('-s', '--steps', type=int, help='The number of iteration steps to take per run')
    iteration.add_argument('--start', type=int, help='The index to start counting from when labling the output of multiple runs')
    #iteration.add_argument('--seed', type=str, default=None, help='The starting seed to seed the pRNG with.')
    
    params = parser.add_argument_group('Configuration')
    params.add_argument('-t', '--population_tolerance', type=float, help='The population tolerance in floating-point format (default 0.02)')
    params.add_argument('-a', '--accept', choices=acceptance_methods, metavar='METHOD', help='An acceptence criteria from: %(choices)s')
    params.add_argument('-p', '--partition', choices=partitioning_methods, metavar='METHOD', help='An acceptence criteria from: %(choices)s')
    params.add_argument('--districts', type=int, help="The number of districts to divide the area into (required)")
    
    outinfo = parser.add_argument_group('Output')
    outinfo.add_argument('-o', '--outfolder', help="The folder to store outputs in")
    outinfo.add_argument('-P', '--prefix', help="A prefix for output file names")
    outinfo.add_argument('--summary_file', help="A file to write summary statistics to")
    
    args = parser.parse_args()
    print("Loading geometry" + args.geometry)
    graph = load_geometry(args.geometry, args.no_json)
    if args.only_json:
        exit()
    
    #if not args.seed:
    #    args.seed = hex(random.randint(0,2**32-1))[2:]
    #random.seed(args.seed)
    
    
    data_keys = []
    # Load in all the specified data files
    print("Loading data:")
    print(args.data)
    for dataset in args.data:
        if isinstance(dataset, str):
            dataset = dataset.split(' ')
        f_name, k_col, v_col, name = dataset
        if k_col.isdigit() and v_col.isdigit():
            csv_object = csv.Reader(open(f_name,'r'))
        else: 
            csv_object = csv.DictReader(open(f_name,'r'))
        values = {str(row[k_col]):float(row[v_col]) for row in csv_object}
        nx.set_node_attributes(graph, values, name)
        data_keys.append(name)
        
    population_total = sum(nx.get_node_attributes(graph,'POP').values())
    
    # pick off the county numbers and add to a dictionary
    values = { key : key[2:5]  for key in nx.get_node_attributes(graph,'POP').keys()}
    nx.set_node_attributes(graph, values, 'counties')
    args.districts = int(args.districts)
    args.population_tolerance = float(args.population_tolerance)
    district_count = args.districts
    
    
    print(f'population_total: {population_total}, district_count: {district_count}')
    partition_settings = {
        'pop_col':'POP',
        'pop_target':max(1,population_total//district_count),
        'epsilon':args.population_tolerance,
        'runs':args.steps}
    acceptance = getattr(acceptance_functions, args.accept)
    print(f'Acceptance function: {args.accept}')
    proposal = partial(getattr(partitioning_functions, args.partition), settings=partition_settings)
    updaters = {
        'cut_edges':cut_edges, 
        'population': Tally('POP', alias='population'),
        'polsby_popper': polsby_popper,
        'areas':Tally('area'),
        'county_splits': county_splits('','counties'),
    }
    if 'VAP' in data_keys: updaters['VAP'] = Tally('VAP')
    if 'BVAP' in data_keys: updaters['BVAP'] = Tally('BVAP')
    if 'HVAP' in data_keys: updaters['HVAP'] = Tally('HVAP')
    if 'VAP' in data_keys and 'BVAP' in data_keys:
        updaters['BVAP_ratio'] = RatioTally(['BVAP','VAP'], 'BVAP_ratio')
    if 'VAP' in data_keys and 'HVAP' in data_keys:
        updaters['HVAP_ratio'] = RatioTally(['HVAP','VAP'], 'HVAP_ratio')
        
    if 'D1' in data_keys: updaters['D1'] = Tally('D1')
    if 'R1' in data_keys: updaters['R1'] = Tally('R1')
    if 'D2' in data_keys: updaters['D2'] = Tally('D2')
    if 'R2' in data_keys: updaters['R2'] = Tally('R2')
    if all(partisan_year in data_keys for partisan_year in ['D1','D2','R1','R2']):
        updaters['Dem_PVI'] = PVITally(['D1','R1','D2','R2'], 51.54, 'Dem_PVI')

    skipped_runs = []
    for run in range(args.start,args.start+args.number_of_runs):
        start = datetime.now()
    
        print(f"Starting run {run:0>3}")
        if args.input_districts == None:
            initial_assignment = partition_with_timeout(graph, args.districts, target=population_total/district_count, population_field = 'POP', epsilon=args.population_tolerance-0.001)
        else:
            initial_assignment = dict(map(stripsplit, open(args.input_districts,'r')))
        
        if initial_assignment == None:
            print("Skipping to next run")
            skipped_runs.append(run)
            continue
        
        initial_partition = GeographicPartition(
            graph,
            assignment=initial_assignment,
            updaters=updaters)
        pop_constraint = within_percent_of_ideal_population(initial_partition, args.population_tolerance)
        
        constraints = [
            contiguous,
            pop_constraint,
            #no_worse_L1_reciprocal_polsby_popper  
            ]

        result = run_markov_chain(proposal, constraints, acceptance, initial_partition, total_steps=args.steps)
        print(f"Mean PP: {sum(result['polsby_popper'].values())/float(len(result['polsby_popper']))}")
        
        #Save the output to file
        os.makedirs(args.outfolder, exist_ok=True)
        outname = f"{args.prefix}_{args.steps/1000}k_{run:0>2}.csv"
        print(outname)
        #outname = f"{args.prefix}_{args.seed}_{args.steps/1000}k_{run:0>2}.csv"
        outfile_path = os.path.join(args.outfolder, outname)
        outfile = open(outfile_path, 'w')
        for block,district in result.assignment.items():
            outfile.write("{},{}\n".format(block,district))
        outfile.close()
        print("csv file successfully written")
        
        
        
        state = args.prefix[0:2]
        objective = args.prefix[2:]
        
        
        csv_file = outfile_path
        
        shape_file = f'data2020/shapefiles/cnty/{state.lower()}_pl2020_cnty_shp/{state.lower()}_pl2020_cnty.shp'

        additional_data = [f'data2020/partisan_data/cnty/{state.lower()}_cnty_census_2020_voter_data_2020.csv', 
                       f'data2020/partisan_data/cnty/{state.lower()}_cnty_census_2020_voter_data_2016.csv']


        map_compression_and_plot.compress_and_plot(state,  csv_file, shape_file, additional_data)
        
        
        
        
        
        
        
        
        print(args.summary_file)
        #Summary file output
        if args.summary_file:
            os.makedirs(os.path.dirname(args.summary_file), exist_ok=True)
            if os.path.exists(args.summary_file):
                sumfile = open(args.summary_file,'a')
            else:
                sumfile = open(args.summary_file,'w')
                sumfile.write("start_time,end_time,outfile_name,acceptance,number_of_districts,pop_tolerance,polsby_popper,mean_BVAP_ratio,black_reps,mean_HVAP_ratio, black_reps_rim, black_reps_south, mean_CPVI,Dem_Prob,Rep_Prob,competitiveness, avg_competitiveness, competitive_districts, cut_edges\n")
                #sumfile.write("start_time,end_time,seed,outfile_name,acceptance,number_of_districts,pop_tolerance,polsby_popper,mean_BVAP_ratio,black_reps,mean_CPVI,Dem_Prob,Rep_Prob\n")
            sumline = f"{start.isoformat()},{datetime.now().isoformat()},{outname},{args.accept},{district_count},{args.population_tolerance},{sum(result['polsby_popper'].values())/district_count:.3f}"
            #sumline = f"{start.isoformat()},{datetime.now().isoformat()},{args.seed},{outname},{args.accept},{district_count},{args.population_tolerance},{sum(result['polsby_popper'].values())/district_count:.3f}"
                        #{},\
                        #{},\
                        #"
            
            if 'BVAP_ratio' in result.updaters.keys():
                black_reps = helper_methods.calculate_black_reps(result)
                sumline += f",{sum(result['BVAP_ratio'].values())/district_count:.3f},{black_reps:.2f}"
                #','.join([sumline, sum(result['BVAP_ratio'])/district_count, black_reps])
            else: sumline += ',,'
            
            if 'HVAP_ratio' in result.updaters.keys():
                sumline += f",{sum(result['HVAP_ratio'].values())/district_count:.3f}"
                black_reps = helper_methods.calculate_black_reps_rim_south(result)
                sumline += f",{black_reps:.2f}"
                black_reps = helper_methods.calculate_black_reps_deep_south(result)
                sumline += f",{black_reps:.2f}"
            else: sumline += ', , ,'
            

            if 'Dem_PVI' in result.updaters.keys():
                CPVI = sum(result['Dem_PVI'].values())/district_count
                dem_prob = helper_methods.calculate_dem_prob(result)
                rep_prob = helper_methods.calculate_rep_prob(result)
                competitiveness = helper_methods.calculate_competitive(result)
                avg_competitiveness = competitiveness/len(result)
                num_competitive = helper_methods.calculate_num_competitive(result)
                sumline += f',{CPVI:.3f},{dem_prob:.2f},{rep_prob:.2f},{competitiveness:.2f}, {avg_competitiveness:.2f},{num_competitive:.2f}'
            else: sumline += ',,,,'
            cut_edges = len(result['cut_edges'])
            sumline+=f',{cut_edges}'
            
            sumfile.write(sumline+'\n')
            sumfile.close()
            
            print("Summary file successfully written")
            #Save a json with lots of information

            outfile_path = os.path.join(args.outfolder, outname)
            outfile = open(outfile_path, 'w')
            for block,district in result.assignment.items():
                outfile.write("{},{}\n".format(block,district))
            outfile.close()

            #Save various data about output to file
            outnamejson = f"{args.prefix}_{args.steps/1000}k_{run:0>2}.json"
            outfile_path = os.path.join(args.outfolder, outnamejson)
            output_metadata = {}
            output_metadata['settings'] = vars(args)
            output_metadata['date_created'] = str(start)
            output_data = {}
            data_keys = ['perimeter', 'exterior_boundaries', 'interior_boundaries', 
                          'area',  'population', 'polsby_popper', 
                          'areas', 'VAP', 'BVAP', 'BVAP_ratio', 'HVAP', 'HVAP_ratio',
                          'D1', 'R1', 'D2', 'R2', 'Dem_PVI',  'cut_edges', 'cut_edges_by_part','boundary_nodes']
            for key in data_keys:
                output_data[key] = result[key]
            output_data['cut_edges']= list(output_data['cut_edges'])
            output_data['cut_edges_by_part']= list(output_data['cut_edges_by_part'])
            output_data['boundary_nodes']= list(output_data['boundary_nodes'])
            output_metadata['data'] = output_data
            #output_metadata['Host computer'] = str(socket.gethostname())
        
            with open(outfile_path, 'w') as outfile:
                json.dump(output_metadata, outfile,indent=4)
            
    print(f'Skipped runs: {", ".join(map(str,skipped_runs))}')
    
    #print(args)
    #print(population_total)
    
    
    #print(args)
    #print(args.geometry)
    
    
    
    
    
