import scipy.stats as stats
import math

norm = stats.norm(0,1)


def calculate_black_reps(partition):
    #return sum(norm.cdf(8.26*x-3.271) for x in partition['BVAP_ratio'].values()) # 2010 values
    return sum(norm.cdf(6.826*x-2.827) for x in partition['BVAP_ratio'].values()) # 2020 values
  
  
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
