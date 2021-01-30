"""
Usage:
  python main.py generate_dotnet_code
  python main.py generate_java_code
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.11.14"

import csv
import json
import sys
import time
import os

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)

def generate_dotnet_code():
    print("generate_dotnet_code")
    counties = read_calculate_nc_counties()
    for c in counties:
        t = 'counties.Add(new County() <state="{}", name="{}", population={}, statePct={}, rangeMin={}, rangeMax={}>);'
        l = t.format(c['state'],c['name'],c['population'],c['pct_total'],c['min'],c['max'])
        l = l.replace('<','{').replace('>', '}')
        #print(l)

        print('            counties.Add(new County() {')
        print('                state="{}",'.format(c['state']))
        print('                name="{}",'.format(c['name']))
        print('                population={},'.format(c['population']))
        print('                statePct={},'.format(c['pct_total']))
        print('                rangeMin={},'.format(c['min']))
        print('                rangeMax={}>);'.format(c['max']).replace('>','}'))

        # counties.Add(new County() {
        #         state="NC", 
        #         name="Yancey", 
        #         population=17903, 
        #         statePct=0.0017241578563160053,
        #         rangeMin=0.9982758421436837,
        #         rangeMax=0.9999999999999997});

        # public string state      { get; set; }
        # public string name       { get; set; }
        # public int    population { get; set; }
        # public double statePct   { get; set; }
        # public double rangeMin   { get; set; }
        # public double rangeMax   { get; set; }
        # counties.Add(new County() {state="NC", name="Wake"});

def generate_java_code():
    print("generate_java_code")

def read_calculate_nc_counties():
    counties = list()
    rows = read_csv('nc_counties.txt', skip=1)
    total_pop = 0
    for row in rows:
        pop = int(row[1])
        total_pop = total_pop + pop
        county = dict()
        county['state'] = 'NC'
        county['name']  = row[0]
        county['population']  = int(pop)
        counties.append(county)

    total_popf = float(total_pop)
    sum_pct = 0.0

    for c in counties:
        c['min'] = sum_pct
        pct_total = float(c['population']) / total_popf
        sum_pct = sum_pct + pct_total
        c['max'] = sum_pct
        c['pct_total'] = pct_total
        #print(json.dumps(c, indent=2, sort_keys=False))

    print('num counties: {}'.format(len(counties)))
    print('total_pop:    {}'.format(total_pop))
    print('total_popf:   {}'.format(total_popf))
    return counties


def read_lines(infile):
    lines = list()
    with open(infile, 'rt') as f:
        for line in f:
            lines.append(line)
    return lines

def read_csv(infile, reader='default', delim=',', dialect='excel', skip=0):
    rows = list()
    if reader == 'dict':
        with open(infile, 'rt') as csvfile:
            rdr = csv.DictReader(csvfile, dialect=dialect, delimiter=delim)
            for row in rdr:
                rows.append(row)
    else:
        with open(infile) as csvfile:
            rdr = csv.reader(csvfile, delimiter=delim)
            for idx, row in enumerate(rdr):
                if idx >= skip:
                    rows.append(row)
    return rows

if __name__ == "__main__":
    func = sys.argv[1].lower()

    if func == 'generate_dotnet_code':
        generate_dotnet_code()
    elif func == 'generate_java_code':
        generate_java_code()
    else:
        print_options('Error: invalid function: {}'.format(func))
