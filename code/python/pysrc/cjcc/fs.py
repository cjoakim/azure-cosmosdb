__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.05.28"

import csv
import json
import os


class FS(object):
    """

    """

    @classmethod
    def pwd(cls):
        return os.getcwd()

    @classmethod
    def read(cls, infile):
        with open(infile, 'rt') as f:
            return f.read()

    @classmethod
    def read_lines(cls, infile):
        lines = list()
        with open(infile, 'rt') as f:
            for line in f:
                lines.append(line)
        return lines

    @classmethod
    def read_csv(cls, infile, reader='default', delim=',', dialect='excel', skip=0):
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

    @classmethod
    def read_json(cls, infile):
        with open(infile, 'rt') as f:
            return json.loads(f.read())

    @classmethod
    def text_file_iterator(cls, infile):
        # return a line generator that can be iterated with iterate()
        with open(infile, 'rt') as f:
            for line in f:
                yield line.strip()

    @classmethod
    def write(cls, outfile, s, verbose=True):
        with open(outfile, 'w') as f:
            f.write(s)
            if verbose:
                print('file written: {}'.format(outfile))

    @classmethod
    def walk(cls, directory):
        files = list()
        for dir_name, subdirs, base_names in os.walk(directory):
            for base_name in base_names:
                full_name = "{}/{}".format(dir_name, base_name)
                entry = dict()
                entry['base'] = base_name
                entry['dir'] = dir_name
                entry['full'] = full_name
                entry['abspath'] = os.path.abspath(full_name)
                files.append(entry)
        return files

    @classmethod
    def read_csvfile_into_rows(cls, infile, delim=','):
        rows = list()  # return a list of csv rows
        with open(infile, 'rt') as csvfile:
            reader = csv.reader(csvfile, delimiter=delim)
            for row in reader:
                rows.append(row)
        return rows

    @classmethod
    def read_csvfile_into_objects(cls, infile, delim=','):
        objects = list()  # return a list of dicts
        with open(infile) as csvfile:
            reader = csv.reader(csvfile, delimiter=delim)
            headers = None
            for idx, row in enumerate(reader):
                if idx == 0:
                    headers = row
                else:
                    if len(row) == len(headers):
                        obj = dict()
                        for field_idx, field_name in enumerate(headers):
                            key = field_name.strip().lower()
                            obj[key] = row[field_idx].strip()
                        objects.append(obj)
        return objects
