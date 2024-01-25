import os
 
# Open a file
path = "outputs/bg/"
states_dir = os.scandir(path)
states = [state.name for state in states_dir]
states.sort()

# Open a file
objectives = ['compactness','comp50_pp50','competitive_reps','dem90_pp10',
                  'dem_gerrymander','rep90_pp10','rep_gerrymander']
objectives = 
print(objectives)
print("\n")
for state in states:
    path = f"outputs/bg/{state}/"
    state_dir = os.scandir(path)
    runs = [run.name[6:-4] for run in state_dir if run.name[-1]=='v' if '25.0k' in run.name]

    

    objective_counts = [len([run for run in runs if objective in run]) for objective in objectives]
    if state not in ['MT', 'ME', 'WY', 'HI', 'AK','ID','IA','KS','IL', 'TN']:
        print(f"{state} :  {min(objective_counts)>= 25}  counts: {objective_counts}")

print("\nMatt files that we're fixing")
for state in ['IA','KS','IL']:
    path = f"outputs/bg/{state}/"
    state_dir = os.scandir(path)
    runs = [run.name[6:-4] for run in state_dir if run.name[-1]=='v' if '25.0k' in run.name]
    set(runs)
    
    objective_counts = [len([run for run in runs if objective in run]) for objective in objectives]
    if state not in ['MT', 'ME', 'WY', 'HI', 'AK','ID']:
        print(f"{state} :  {min(objective_counts)>= 25}  counts: {objective_counts}")
print("Ignored states that have too few districts")
