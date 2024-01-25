import zipfile, struct, csv, io

from collections import defaultdict


scope_geoid = {
    '050': '{state}{county}',
    '140': '{state}{county}{tract}',
    '150': '{state}{county}{tract}{block_group}',
    '101': '{state}{county}{tract}{block}',
    }
    
# SUMLEV LOGRECNO STATECOUNTY TRACT BLKGRP BLOCK

class SummaryArchive(object):
    def __init__(self, filename):
        self.archive = zipfile.ZipFile(filename,'r')
        self.state = filename[:2]
        self.year = filename[2:6]
        
        self.colname_lookup = {
            'p1': (f'{self.state}00001{self.year}.sf1',5),
            'p2': (f'{self.state}00002{self.year}.sf1',5),
            'p3': (f'{self.state}00003{self.year}.sf1',5),
            'p4': (f'{self.state}00003{self.year}.sf1',13),

            'p10': (f'{self.state}00004{self.year}.sf1',5),
            }
        
    
    #https://stackoverflow.com/questions/4914008/how-to-efficiently-parse-fixed-width-files
    def get_logrecnos(self, target_sumlev):
        geofile = self.archive.open(f"{self.state}geo{self.year}.sf1",'r')
        structfmt = "8x 3s 7x 7s 2x 2s 3s 22x 6s 1s 4s 335x"
        fieldstruct = struct.Struct(structfmt)
        records = {}
        record_list = ['sumlev','logrecno','state','county','tract','block_group','block']
        for row in geofile:
            fields = dict(zip(record_list, map(lambda x: x.decode(), fieldstruct.unpack_from(row))))
            if fields['sumlev'] == target_sumlev:
                geoid = scope_geoid[target_sumlev].format(**fields)
                records[fields['logrecno']] = geoid
        return records
        # block-level: sumlev = 101
        # bg-level: sumlev = 150
        # tract-level: sumlev = 140
        # county-level: sumlev = 050
        # state level: sumlev = 0
    
    def lookup_colname(self, colname: str):
        group = colname[:-3].replace('0','').lower()
        if colname[3]=='0': group+='0'
        index = int(colname[-3:])
        
        return (self.colname_lookup[group][0], self.colname_lookup[group][1]+index-1)
            
    def parse_colnames(self):
        line_format = "([a-z]*)([0-9]{1,3})([a-z]?)\|([0-9]{1,2}):([0-9]{1,2})\|"
        
        
        next_column = defaultdict(5)
        group_starts = {}
        
        for item in regex_lines:
            group, fileno, count = item.parse
            group_starts[group] = (fileno_to_filename, next_column[group])
            next_column[group] += count
        
        self.colname_lookup = group_starts
            
    
    def collect_column(self, logrecnos: set, colname: str):
        filename, col = self.lookup_colname(colname)
        
        outdata = {}
        
        with io.TextIOWrapper(self.archive.open(filename,'r'), encoding='ascii') as csvfile:
            data = csv.reader(csvfile)
            for row in data:
                if row[4] in logrecnos:
                    outdata[row[4]] = row[col]
        return outdata



def merge_dicts(master: dict):
    out = defaultdict(dict)
    for col in master.keys():
        for item in master[col].keys():
            out[item][col] = master[col][item]
    return dict(out)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A script for extracting columns from census summary files")
    
    parser.add_argument('-s','--scope', help="The scope at which to return results.  050 for county, 140 for tract, 150 for block group, and 101 for block.", default='101')
    
    parser.add_argument('summary_file', help="The summary file to parse")
    
    
    args = parser.parse_args()

    mainobj = SummaryArchive(args.summary_file)
    master_data = {}
    master_data['GEOID'] = mainobj.get_logrecnos(args.scope)
    master_data['POP'] = mainobj.collect_column(master_data['GEOID'],'P0010001')
    
    master_data['BPOP'] = mainobj.collect_column(master_data['GEOID'],'P0030003')
    master_data['VAP'] = mainobj.collect_column(master_data['GEOID'],'P0100001')
    master_data['BVAP'] = mainobj.collect_column(master_data['GEOID'],'P0100004')
    resized = merge_dicts(master_data)
    
    outfile = open(f'{mainobj.state}_block_demographics.csv', 'w')
    
    outfile.write("GEOID,POP,BPOP,VAP,BVAP\n")
    for row in sorted(list(resized.keys())):
        #print(f"{resized[row]['GEOID']},{resized[row]['POP']}")
        outfile.write('{GEOID},{POP},{BPOP},{VAP},{BVAP}\n'.format(**resized[row]))
    #print(resized)
    