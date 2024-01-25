import os
from tabulate import tabulate
import argparse
import math

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("--objectives", help="determines which objectives to tabulate")
parser.add_argument("--states", help="determines which states to look at")
parser.add_argument("--south", help="predetermined settings for rim or deep")
parser.add_argument("--todo", help="prints next commands to run")

args = parser.parse_args()


if args.states:
    states = args.states.split(',')
elif args.south == 'rim':
    states = ['MD', 'VA', 'NC', 'TN']
elif args.south == 'deep':
    states = ['AL', 'GA', 'LA', 'MS', 'SC']  
else:
    # Open a file
    path = "outputs/bg/"
    states_dir = os.scandir(path)
    states = [state.name for state in states_dir]
    states.sort()

# Open a file
objectives = ['compactness','comp50_pp50','competitive_reps','dem90_pp10',
                  'dem_gerrymander','rep90_pp10','rep_gerrymander']
if args.south == 'rim':
    objectives = ['bvap_rim', 'bvap_rim_pp', 'bvap_rim75_pp25','bvap_rim90_pp10','bvap_rim95_pp5', 'compactness']
    
if args.south == 'deep':
    objectives = ['bvap_deep', 'bvap_deep_pp', 'bvap_deep75_pp25','bvap_deep90_pp10','bvap_deep95_pp5','compactness']

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
    path = f"outputs/bg/{state}/"
    state_dir = os.scandir(path)
    runs = [run.name[6:-4] for run in state_dir if run.name[-1]=='n' if '25.0k' in run.name]

    

    objective_counts = [len([run for run in runs if 'new_'+ objective+'_25.0k' in run]) for objective in objectives] #objective_counts = [len([run for run in runs if 'new_'+objective+'_25.0k' in run]) for objective in objectives]
    if state not in ['not sure why this was here...']:
        #print(f"{state} :  {min(objective_counts)>= 25}  counts: {objective_counts}")
        counts += [[state,min(objective_counts)>= 100] + objective_counts]
    for i,obj in zip(objective_counts, objectives):
        if i < 100:
            j = (math.ceil(i/25))*25
            if j < 100:
                todo += [f'sbatch --array={max(j+1,i)}-{min(j+25,100)} --job-name {state}_{job_name(obj)} slurm_batch.sh {state} {obj}']
            

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
    rc = subprocess.call("next_runs.sh")
    
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
