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

import os
import argparse
import math
        

with open('cnty_runs.sh', 'w') as f:
    f.seek(0)

    f.write('#!/bin/bash\n')
    for state in states.keys():
        f.write(f'sbatch --array=15-15 --job-name {state}_cnty slurm_batch_cnty.sh {state} dem_gerrymander'+'\n')

    f.write('mv *.out outfiles\n')
    f.write('mv *.*.out outfiles\n')
    f.write('squeue -A ravt')

    f.truncate()