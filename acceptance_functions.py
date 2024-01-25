
import helper_methods

def compactness(partition):
    c = float(len(partition))
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return pp_current >= pp_prev
    
def black_representatives(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    return reps_current >= reps_prev

def bvap_rim_south(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    return reps_current >= reps_prev

def bvap_deep_south(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    return reps_current >= reps_prev


def bvap_all(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (reps_current+0.3*pp_current+ 0.7*comp_reps_current) >= (reps_prev+0.3*pp_prev+0.7*comp_reps_current)

def bvap_all_90_10(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (reps_current+0.5*0.1*pp_current+ 0.5*0.9*comp_reps_current) >= (reps_prev+0.5*0.1*pp_prev+0.5*0.9*comp_reps_current)

def bvap_all_cut_edges(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    cut_current = sum(partition['cut_edges'].values())/c
    cut_prev = (sum(partition.parent['cut_edges'].values())/c)
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (reps_current+0.003*cut_current+ 0.7*comp_reps_current) >= (reps_prev+0.003*cut_prev+0.7*comp_reps_current)

def bvap_all_cut_edges_03(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    cut_current = sum(partition['cut_edges'].values())/c
    cut_prev = (sum(partition.parent['cut_edges'].values())/c)
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (reps_current+0.03*cut_current+ 0.7*comp_reps_current) >= (reps_prev+0.03*cut_prev+0.7*comp_reps_current)

def bvap_pp(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current+pp_current) >= (reps_prev+pp_prev)
    
def bvap75_pp25(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.75+pp_current*0.25) >= (reps_prev*0.75+pp_prev*0.25)

def bvap90_pp10(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.9+pp_current*0.1) >= (reps_prev*0.9+pp_prev*0.1)
    
def bvap95_pp5(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.95+pp_current*0.05) >= (reps_prev*0.95+pp_prev*0.05)

def comp50_bvap50(partition):
    c= float(len(partition))
    reps_current = helper_methods.calculate_black_reps(partition)/c
    reps_prev = helper_methods.calculate_black_reps(partition.parent)/c
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (comp_reps_current*0.5+reps_current*0.5) >= (comp_reps_prev*0.5+reps_prev*0.5)

#####
# Bvap Rim South 2020
#####

def bvap_rim(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    return reps_current >= reps_prev

def bvap_rim_pp(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current+pp_current) >= (reps_prev+pp_prev)
    
def bvap_rim75_pp25(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.75+pp_current*0.25) >= (reps_prev*0.75+pp_prev*0.25)

def bvap_rim90_pp10(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.9+pp_current*0.1) >= (reps_prev*0.9+pp_prev*0.1)
    
def bvap_rim95_pp5(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.95+pp_current*0.05) >= (reps_prev*0.95+pp_prev*0.05)

def comp50_bvap_rim50(partition):
    c= float(len(partition))
    reps_current = helper_methods.calculate_black_reps_rim_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_rim_south(partition.parent)/c
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (comp_reps_current*0.5+reps_current*0.5) >= (comp_reps_prev*0.5+reps_prev*0.5)
### 
# Bvap Deep South 2020
###
def bvap_deep(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    return reps_current >= reps_prev

def bvap_deep_pp(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current+pp_current) >= (reps_prev+pp_prev)
    
def bvap_deep75_pp25(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.75+pp_current*0.25) >= (reps_prev*0.75+pp_prev*0.25)

def bvap_deep90_pp10(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.9+pp_current*0.1) >= (reps_prev*0.9+pp_prev*0.1)
    
def bvap_deep95_pp5(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.95+pp_current*0.05) >= (reps_prev*0.95+pp_prev*0.05)

def comp50_bvap_deep50(partition):
    c= float(len(partition))
    reps_current = helper_methods.calculate_black_reps_deep_south(partition)/c
    reps_prev = helper_methods.calculate_black_reps_deep_south(partition.parent)/c
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return (comp_reps_current*0.5+reps_current*0.5) >= (comp_reps_prev*0.5+reps_prev*0.5)

###
# Political Objectives
###

def dem_gerrymander(partition):
    dem_reps_current = helper_methods.calculate_dem_prob(partition)
    dem_reps_prev = helper_methods.calculate_dem_prob(partition.parent)
    return dem_reps_current >= dem_reps_prev

def rep_gerrymander(partition):
    rep_reps_current = helper_methods.calculate_rep_prob(partition)
    rep_reps_prev = helper_methods.calculate_rep_prob(partition.parent)
    return rep_reps_current >= rep_reps_prev

def competitive_reps(partition):
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    return comp_reps_current >= comp_reps_prev
    
def dem90_pp10(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_dem_prob(partition)/c
    reps_prev = helper_methods.calculate_dem_prob(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.9+pp_current*0.1) >= (reps_prev*0.9+pp_prev*0.1)

def rep90_pp10(partition):
    c = float(len(partition))
    reps_current = helper_methods.calculate_rep_prob(partition)/c
    reps_prev = helper_methods.calculate_rep_prob(partition.parent)/c
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (reps_current*0.9+pp_current*0.1) >= (reps_prev*0.9+pp_prev*0.1)
    
def comp75_pp25(partition):
    c= float(len(partition))
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (comp_reps_current*0.75+pp_current*0.25) >= (comp_reps_prev*0.75+pp_prev*0.25)
    
def comp90_pp10(partition):
    c= float(len(partition))
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (comp_reps_current*0.9+pp_current*0.1) >= (comp_reps_prev*0.9+pp_prev*0.1)

def comp50_pp50(partition):
    c= float(len(partition))
    comp_reps_current = helper_methods.calculate_competitive(partition)
    comp_reps_prev = helper_methods.calculate_competitive(partition.parent)
    pp_current = sum(partition['polsby_popper'].values())/c
    pp_prev = (sum(partition.parent['polsby_popper'].values())/c)
    return (comp_reps_current*0.5+pp_current*0.5) >= (comp_reps_prev*0.5+pp_prev*0.5)
    
def prototype_variable_mixer(partition, helpers, ratios):
    accept_list = helpers.split(',')
    ratio_list = ratios.split(',')
    
    return
