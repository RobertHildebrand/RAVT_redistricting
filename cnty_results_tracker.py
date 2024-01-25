import os
from tabulate import tabulate
import argparse
import math


states = {
    'AL': {'reps': 7, 'fips': 1, 'name': 'ALABAMA'},
    'AK': {'reps': 1, 'fips': 2, 'name': 'ALASKA'},
    'AZ': {'reps': 9, 'fips': 4, 'name': 'ARIZONA'},
    'AR': {'reps': 4, 'fips': 5, 'name': 'ARKANSAS'},
    'CA': {'reps': 52, 'fips': 6, 'name': 'CALIFORNIA'},
    'CO': {'reps': 8, 'fips': 8, 'name': 'COLORADO'},
    'CT': {'reps': 5, 'fips': 9, 'name': 'CONNECTICUT'},
    'DC': {'reps': 1, 'fips': 11, 'name': 'DC'},
    'DE': {'reps': 1, 'fips': 10, 'name': 'DELAWARE'},
    'FL': {'reps': 28, 'fips': 12, 'name': 'FLORIDA'},
    'GA': {'reps': 14, 'fips': 13, 'name': 'GEORGIA'},
    'HI': {'reps': 2, 'fips': 15, 'name': 'HAWAII'},
    'ID': {'reps': 2, 'fips': 16, 'name': 'IDAHO'},
    'IL': {'reps': 17, 'fips': 17, 'name': 'ILLINOIS'},
    'IN': {'reps': 9, 'fips': 18, 'name': 'INDIANA'},
    'IA': {'reps': 4, 'fips': 19, 'name': 'IOWA'},
    'KS': {'reps': 4, 'fips': 20, 'name': 'KANSAS'},
    'KY': {'reps': 6, 'fips': 21, 'name': 'KENTUCKY'},
    'LA': {'reps': 6, 'fips': 22, 'name': 'LOUISIANA'},
    'ME': {'reps': 2, 'fips': 23, 'name': 'MAINE'},
    'MD': {'reps': 8, 'fips': 24, 'name': 'MARYLAND'},
    'MA': {'reps': 9, 'fips': 25, 'name': 'MASSACHUSETTS'},
    'MI': {'reps': 13, 'fips': 26, 'name': 'MICHIGAN'},
    'MN': {'reps': 8, 'fips': 27, 'name': 'MINNESOTA'},
    'MS': {'reps': 4, 'fips': 28, 'name': 'MISSISSIPPI'},
    'MO': {'reps': 8, 'fips': 29, 'name': 'MISSOURI'},
    'MT': {'reps': 2, 'fips': 30, 'name': 'MONTANA'},
    'NE': {'reps': 3, 'fips': 31, 'name': 'NEBRASKA'},
    'NV': {'reps': 4, 'fips': 32, 'name': 'NEVADA'},
    'NH': {'reps': 2, 'fips': 33, 'name': 'NEW HAMPSHIRE'},
    'NJ': {'reps': 12, 'fips': 34, 'name': 'NEW JERSEY'},
    'NM': {'reps': 3, 'fips': 35, 'name': 'NEW MEXICO'},
    'NY': {'reps': 26, 'fips': 36, 'name': 'NEW YORK'},
    'NC': {'reps': 14, 'fips': 37, 'name': 'NORTH CAROLINA'},
    'ND': {'reps': 1, 'fips': 38, 'name': 'NORTH DAKOTA'},
    'OH': {'reps': 15, 'fips': 39, 'name': 'OHIO'},
    'OK': {'reps': 5, 'fips': 40, 'name': 'OKLAHOMA'},
    'OR': {'reps': 6, 'fips': 41, 'name': 'OREGON'},
    'PA': {'reps': 17, 'fips': 42, 'name': 'PENNSYLVANIA'},
    'RI': {'reps': 2, 'fips': 44, 'name': 'RHODE ISLAND'},
    'SC': {'reps': 7, 'fips': 45, 'name': 'SOUTH CAROLINA'},
    'SD': {'reps': 1, 'fips': 46, 'name': 'SOUTH DAKOTA'},
    'TN': {'reps': 9, 'fips': 47, 'name': 'TENNESSEE'},
    'TX': {'reps': 38, 'fips': 48, 'name': 'TEXAS'},
    'UT': {'reps': 4, 'fips': 49, 'name': 'UTAH'},
    'VT': {'reps': 1, 'fips': 50, 'name': 'VERMONT'},
    'VA': {'reps': 11, 'fips': 51, 'name': 'VIRGINIA'},
    'WA': {'reps': 10, 'fips': 53, 'name': 'WASHINGTON'},
    'WV': {'reps': 2, 'fips': 54, 'name': 'WEST VIRGINIA'},
    'WI': {'reps': 8, 'fips': 55, 'name': 'WISCONSIN'},
    'WY': {'reps': 1, 'fips': 56, 'name': 'WYOMING'}
    }

#states = states.keys()

states = ['AL', 'AR','CO', 'IA', 'ID', 'KS', 'LA', 'ME', 'MS','NE', 'NH', 'NM', 'OK', 'OR', 'SC', 'WV']
print(states)

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("--objectives", help="determines which objectives to tabulate")
parser.add_argument("--states", help="determines which states to look at")
parser.add_argument("--south", help="determines which states to look at")
parser.add_argument("--todo", help="determines which states to look at")

args = parser.parse_args()

if args.states:
    states = args.states.split(',')
elif args.south == 'rim':
    states = ['MD', 'VA', 'NC', 'TN']
elif args.south == 'deep':
    states = ['AL', 'GA', 'LA', 'MS', 'SC']  
elif args.south == 'south':
    states = ['MD', 'VA', 'NC', 'TN','AL', 'GA', 'LA', 'MS', 'SC']  
else:
    # Open a file
    path = "outputs/cnty/"
    states_dir = os.scandir(path)
    #states = [state.name for state in states_dir]
    states.sort()

# Open a file
objectives = ['black_representatives', 'dem_gerrymander', 'rep_gerrymander', 'compactness']
#['compactness','comp50_pp50','competitive_reps','dem90_pp10',
                 # 'dem_gerrymander','rep90_pp10','rep_gerrymander']


if args.objectives:
    objectives =  args.objectives.split(',')

short_names = {
'bvap_rim':'bvap', 
'bvap_rim_pp':'50_50', 
'bvap_rim75_pp25':'75_25',
'bvap_rim90_pp10':'90_10',
'bvap_rim95_pp5'  : '95_5',
'bvap_deep':'bvap', 
'bvap_deep_pp':'50_50', 
'bvap_deep75_pp25':'75_25',
'bvap_deep90_pp10':'90_10',
'bvap_deep95_pp5'  : '95_5',
'compactness':'pp'  
}

def job_name(obj):
    if obj in short_names.keys():
        return short_names[obj]
    return ''
 
    
print(" ".join(objectives))
print("\n")
counts = []
todo = []

for state in states:
    path = f"outputs/cnty/{state}/"
    state_dir = os.scandir(path)
    runs = [run.name[6:-4] for run in state_dir if run.name[-1]=='n' if '25.0k' in run.name]

    

    objective_counts = [len([run for run in runs if objective+'_25.0k' in run]) for objective in objectives] #objective_counts = [len([run for run in runs if 'new_'+objective+'_25.0k' in run]) for objective in objectives]
    if state not in ['not sure why this was here...']:
        #print(f"{state} :  {min(objective_counts)>= 25}  counts: {objective_counts}")
        counts += [[state,min(objective_counts)>= 15] + objective_counts]
    for i,obj in zip(objective_counts, objectives):
        if i < 15:
            j = (math.ceil(i/2))*2
            if j < 5 and obj == 'dem_gerrymander':
                todo += [f'sbatch --array={max(j+1,i)}-{min(j+2,3)} --job-name {state}_cnty_{job_name(obj)} slurm_batch_cnty.sh {state} {obj}']
            

print(tabulate(counts, headers=['State', 'Done'] + [obj[:16] for obj in objectives]))

print('\n')

if args.todo:
    for t in todo:
        print(t)
    print('squeue -A ravt')
        
        
if args.todo == 'write_next' or args.to == 'run_next':
    with open('next_runs.sh', 'w') as f:
        f.seek(0)
 
        f.write('#!/bin/bash\n')
        if todo:
            for i in range(min(6,len(todo))):
                f.write(todo[i]+'\n')
        
        f.write('mv *.out outfiles\n')
        f.write('mv *.*.out outfiles\n')
        f.write('squeue -A ravt')
        
        f.truncate()
        
if args.todo == 'run_next':
    import subprocess
    rc = subprocess.call("next_cnty_runs.sh")
    
# print("\nMatt files that we're fixing")
# for state in ['IA','KS','IL']:
#     path = f"outputs/bg/{state}/"
#     state_dir = os.scandir(path)
#     runs = [run.name[6:-4] for run in state_dir if run.name[-1]=='v' if '25.0k' in run.name]
#     set(runs)
    
#     objective_counts = [len([run for run in runs if objective in run]) for objective in objectives]
#     if state not in ['MT', 'ME', 'WY', 'HI', 'AK','ID']:
#         print(f"{state} :  {min(objective_counts)>= 25}  counts: {objective_counts}")
# print("Ignored states that have too few districts")
