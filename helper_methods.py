import scipy.stats as stats
import math

norm = stats.norm(0,1)


# A.) For rim south states (MD, VA, NC, TN):
# Pr(Black representative) = phi (-4.194 + (BVAP*0.0975) + (HVAP*0.0300)

# B.) For deep south states (AL, GA, LA, MS, SC): 
# Pr(Black representative) = phi (-4.729 + (BVAP*0.1044) + (HVAP*0.0300)

def calculate_black_reps(partition):
    #return sum(norm.cdf(8.26*x-3.271) for x in partition['BVAP_ratio'].values()) # 2010 values
    return sum(norm.cdf(6.826*x-2.827) for x in partition['BVAP_ratio'].values()) # 2020 values
    #return sum(norm.cdf(10.67*x-4.81) for x in partition['BVAP_ratio'].values()) # 2020 Southern states values


def calculate_black_reps_rim_south(partition):
    return sum(norm.cdf(-4.194+bvap*9.75+ hvap*3) for (bvap,hvap) in zip(partition['BVAP_ratio'].values(),partition['HVAP_ratio'].values()) ) # 2020 Southern states values

def calculate_black_reps_deep_south(partition):
    return sum(norm.cdf(-4.729+bvap*10.44+ hvap*3) for (bvap,hvap) in zip(partition['BVAP_ratio'].values(),partition['HVAP_ratio'].values()) ) # 2020 Southern states values



######
def calculate_black_reps_list(partition):
    #return sum(norm.cdf(8.26*x-3.271) for x in partition['BVAP_ratio'].values()) # 2010 values
    #return sum(norm.cdf(6.826*x-2.827) for x in partition['BVAP_ratio'].values()) # 2020 values
    return [norm.cdf(10.67*x-4.81) for x in partition['BVAP_ratio'].values] # 2020 Southern states values


def calculate_black_reps_rim_south_list(partition):
    return [norm.cdf(-4.194+bvap*9.75+ hvap*3) for (bvap,hvap) in zip(partition['BVAP_ratio'].values,partition['HVAP_ratio'].values)] # 2020 Southern states values

def calculate_black_reps_deep_south_list(partition):
    return [norm.cdf(-4.729+bvap*10.44+ hvap*3) for (bvap,hvap) in zip(partition['BVAP_ratio'].values,partition['HVAP_ratio'].values) ] # 2020 Southern states values

def calculate_dem_prob_list(partition):
    return [norm.cdf(pvi / 4.8) for pvi in partition['Dem_PVI'].values]

def calculate_rep_prob_list(partition):
    return [1 - norm.cdf(pvi / 4.8) for pvi in partition['Dem_PVI'].values]

def calculate_competitive_list(partition):
    return [math.exp(-(pvi / 4.8)**2) for pvi in partition['Dem_PVI'].values]


def calculate_num_competitive_list(partition):
    ''' Competitive districts are those with pvi between -5 and 5'''
    return [abs(pvi)<= 5 for pvi in partition['Dem_PVI'].values]

def pvi_list(df, bias = 51.69):
    return 50*df['D20']/(df['D20'] + df['R20']) + 50*df['D16']/(df['D16'] + df['R16']) - bias


#######



def calculate_dem_prob(partition):
    return sum(norm.cdf(pvi / 4.8) for pvi in partition['Dem_PVI'].values())

def calculate_rep_prob(partition):
    return sum(1 - norm.cdf(pvi / 4.8) for pvi in partition['Dem_PVI'].values())

def calculate_competitive(partition):
    return sum(math.exp(-(pvi / 4.8)**2) for pvi in partition['Dem_PVI'].values())

def calculate_competitive(partition):
    return sum(math.exp(-(pvi / 4.8)**2) for pvi in partition['Dem_PVI'].values())

def calculate_num_competitive(partition):
    ''' Competitive districts are those with pvi between -5 and 5'''
    return sum(abs(pvi)<= 5 for pvi in partition['Dem_PVI'].values())
