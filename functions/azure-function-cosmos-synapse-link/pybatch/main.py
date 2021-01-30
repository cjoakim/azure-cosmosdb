"""
Usage:
    python main.py initialize_plants_list
    python main.py post_to_azure_function local
    python main.py post_to_azure_function azure
    python main.py random_plant_changes 6
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.10.10"

import json
import os
import pprint
import random
import requests
import sys
import time
import uuid

from docopt import docopt

from faker import Faker

def initialize_plants_list():
    random.seed()
    data = dict()
    updated_at = epoch()

    nc_rows = read_csv_file('data/postal_codes_nc.csv')
    sc_rows = read_csv_file('data/postal_codes_sc.csv')
    ga_rows = read_csv_file('data/postal_codes_ga.csv')
    print('{} rows read for nc'.format(len(nc_rows)))
    print('{} rows read for sc'.format(len(sc_rows)))
    print('{} rows read for ga'.format(len(ga_rows)))

    nc_rnd = select_random_rows(nc_rows, 33)
    sc_rnd = select_random_rows(sc_rows, 34)
    ga_rnd = select_random_rows(ga_rows, 34)
    plants = list()
    for row in nc_rnd:
        plants.append(row)
    for row in sc_rnd:
        plants.append(row)
    for row in nc_rnd:
        plants.append(row)
    print('{} merged/selected plants'.format(len(plants)))

    for plant in plants:
        add_randomized_values(plant)

    for plant in plants:
        if 'longitude' in plant.keys():
            del plant['longitude']
        if 'latitude' in plant.keys():
            del plant['latitude']
        plant['updated_at'] = updated_at

    data['updated_at'] = updated_at
    data['plants'] = plants
    write_obj_as_json_file('data/plants_initial.json', data)
    write_obj_as_json_file(plants_filename(), data)

def select_random_rows(rows, count):
    random_rows = list()
    for i in random_indices(rows):
        if len(random_rows) < count:
            random_rows.append(rows[i])
    return random_rows

def random_indices(array):
    indices = list()
    for i in range(0, len(array)):
        indices.append(i)
    random.shuffle(indices)
    return indices

def add_randomized_values(plant):
    location = dict()
    location['type'] = 'Point'
    location['coordinates'] = [float(plant['longitude']), float(plant['latitude'])] 
    plant['location'] = location

    faker = Faker()
    plant_mgr = '{} {}'.format(faker.first_name(), faker.last_name())
    city = plant['city_name']

    plant['doctype'] = 'plant'
    plant['products'] = random_products_list(5)
    plant['active_ind'] = random_active_indicator()
    plant['plant_name'] = '{}'.format(city).replace(' ', '_')
    plant['plant_address'] = '{} {} {}'.format(
        random_street_number(), faker.street_name(), faker.street_suffix())
    plant['plant_manager'] = plant_mgr
    plant['pk'] = plant['plant_name']

def random_products_list(count):
    manufactured_items = manufactured_products_and_components()
    items = list()
    for i in random_indices(manufactured_items):
        if len(items) < count:
            items.append(manufactured_items[i])
    return items

def manufactured_products_and_components():
    mfg_list = list()
    for i in range(1, 100):
       mfg_list.append('Component_{}'.format(i)) 
    for i in range(1, 100):
       mfg_list.append('Product_{}'.format(i)) 
    return mfg_list

def random_street_number():
    return random.randint(1, 1000)

def random_active_indicator():
    if random.random() < 0.05:
        return 'closed'
    else:
        return 'active'

def random_plant_changes(count):
    updated_at = epoch()
    print('creating {} random_plant_changes at {}'.format(count, updated_at))
    data = read_json(plants_filename())
    plants = data['plants']

    for enum_idx, plant_idx in enumerate(random_indices(plants)):
        if enum_idx < count:
            modify_plant(plants[plant_idx], updated_at)

    data['updated_at'] = updated_at
    write_obj_as_json_file(plants_filename(), data)

def modify_plant(plant, updated_at):
    r = random.random()
    # 10% of the random changes are active_ind toggling
    # 90% are product list changes
    if r < 0.1:
        if plant['active_ind'] == 'closed':
            plant['active_ind'] = 'active'
        else:
            plant['active_ind'] = 'closed'
    else:
        plant['products'] = random_products_list(6)

    plant['updated_at'] = updated_at
    return plant

def post_to_azure_function(target):
    print('post_to_azure_function: {}'.format(target))
    body = read_json(plants_filename())
    print(json.dumps(body, sort_keys=True, indent=2))
    url = azure_function_url(target)

    function = 'update_plants_{}'.format(epoch())
    invoke(function, 'post', url, {}, body)

def azure_function_url(target):
    if target == 'azure':
        return os.environ['AZURE_FUNCTION_PLANTS_AZURE']
    else:
        return 'http://localhost:7071/api/CosmosPlantsUpdate'
        #return os.environ['AZURE_FUNCTION_PLANTS_LOCAL']

def invoke(function_name, method, url, headers={}, json_body={}):
    # This is a generic method which invokes all HTTP Requests to the Azure Search Service
    print('===')
    print("invoke: {} {} {}\nheaders: {}\nbody: {}".format(function_name, method.upper(), url, headers, json_body))
    print('---')
    if method == 'get':
        r = requests.get(url=url, headers=headers)
    elif method == 'post':
        r = requests.post(url=url, headers=headers, json=json_body)
    elif method == 'put':
        r = requests.put(url=url, headers=headers, json=json_body)
    elif method == 'delete':
        r = requests.delete(url=url, headers=headers)
    else:
        print('error; unexpected method value passed to invoke: {}'.format(method))

    print('response: {}'.format(r))
    if r.status_code < 300:
        try:
            resp_obj = json.loads(r.text)
            outfile = 'tmp/{}.json'.format(function_name)
            print(outfile)
            write_obj_as_json_file(outfile, resp_obj)
        except Exception as e:
            print("exception processing http response".format(e))
            print(r.text)
    else:
        print(r.text)
    return r

# IO functions below

def epoch():
    return int(time.time())

def plants_filename():
    return 'data/plants.json'

def read_csv_file(infile):
    lines = read_text_file(infile)
    fields, rows = list(), list()

    for idx, line in enumerate(lines):
        if idx == 0:
            fields = line.split(',') 
        else:
            row = dict()
            values = line.split(',')
            for vidx, value in enumerate(values):
                fname = fields[vidx]
                row[fname] = value
            rows.append(row)
    return rows

def read_text_file(infile):
    lines = list()
    with open(infile, 'rt') as f:
        for idx, line in enumerate(f):
            lines.append(line.strip())
    return lines   

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

def write_obj_as_json_file(outfile, obj):
    txt = json.dumps(obj, sort_keys=True, indent=2)
    with open(outfile, 'wt') as f:
        f.write(txt)
    print("file written: " + outfile)

def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()

        if func == 'initialize_plants_list':
            initialize_plants_list()

        elif func == 'post_to_azure_function':
            target = sys.argv[2]
            post_to_azure_function(target)

        elif func == 'random_plant_changes':
            count = int(sys.argv[2])
            random_plant_changes(count)

        elif func == 'truncate_container_per_criteria':
            dbname = sys.argv[2]
            cname  = sys.argv[3]
            crit   = sys.argv[4]
            truncate_container_per_criteria(dbname, cname, crit)

        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
            print_options('Error: no command-line args entered')
