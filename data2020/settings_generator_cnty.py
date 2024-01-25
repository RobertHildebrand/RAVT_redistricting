import os

#state_string = 'AL,GA,LA,MD,MS,NC,SC,TN,IN,IL,PA,OH,MT,MI'
run_count = 25
steps = 25000
ini_path = 'settings_files/'

#state_list = [s.upper() for s in state_string.split(',')]

scope = 'cnty'
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

state_list = states.keys()


os.makedirs(ini_path, exist_ok=True)

for state in state_list:
    out = open(os.path.join(ini_path, f'{state}_cnty.ini'),'w')
    outfile =   ''
    outfile +=  '[Inputs]\n'
    outfile += f'geometry: data2020/spatial_network/{scope}/{state.lower()}_pl2020_{scope}.json\n'

    outfile +=  f'data: data2020/demographics/{scope}/{state.lower()}_{scope}_demographics_2020.csv GEOID VAP VAP\n'
    outfile +=  f'data: data2020/demographics/{scope}/{state.lower()}_{scope}_demographics_2020.csv GEOID BVAP BVAP\n'
    outfile +=  f'data: data2020/demographics/{scope}/{state.lower()}_{scope}_demographics_2020.csv GEOID HVAP HVAP\n'
    outfile +=  f'data: data2020/demographics/{scope}/{state.lower()}_{scope}_demographics_2020.csv GEOID POP POP\n'

    outfile +=  f'data: data2020/partisan_data/{scope}/{state.lower()}_{scope}_census_2020_voter_data_2016_summarized.csv GEOID D16 D1\n'
    outfile +=  f'data: data2020/partisan_data/{scope}/{state.lower()}_{scope}_census_2020_voter_data_2020_summarized.csv GEOID D20 D2\n'
    outfile +=  f'data: data2020/partisan_data/{scope}/{state.lower()}_{scope}_census_2020_voter_data_2016_summarized.csv GEOID R16 R1\n'
    outfile +=  f'data: data2020/partisan_data/{scope}/{state.lower()}_{scope}_census_2020_voter_data_2020_summarized.csv GEOID R20 R2\n'

    outfile +=  '[Iteration]\n'
    outfile += f'#number_of_runs: {run_count}\n'
    outfile += f'#steps: {steps}\n'

    outfile +=  '[Configuration]\n'
    outfile +=  'population_tolerance: 0.1\n'
    outfile +=  '#accept: \n'
    outfile +=  'partition: semi_random_split\n'
    outfile +=  f'districts: {states[state]["reps"]}\n'

    outfile +=  '[Outputs]\n'
    outfile += f'outfolder: outputs/{scope}/{state}/\n'
    outfile += f'prefix: {state}_{scope}_new_\n'
    outfile += f'summary_file: outputs/summaries/{state}_{scope}_2020_summary_new_objectives_cnty.csv\n'
    out.write(outfile)
