__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "June 2021"

import json
import os
import pprint
import sys
import time
import uuid

import arrow
import jinja2

# Class MarkdownGenerator was used to generate the initial set of documentation
# markdown files.

class MarkdownGenerator(object):    

    def __init__(self):
        pass

    def generate(self):
        structure = self.documentation_structure()

        # Generate the List of Pages for the main README.md file to copy-and-paste
        for page_idx, page in enumerate(structure):
            title = '{} - {}'.format(page['num'], page['name'])
            print('- [{}]({})'.format(title, page['filename']))

        # Generate the individual markdown pages
        for page_idx, page in enumerate(structure):
            print(json.dumps(page, sort_keys=False, indent=2))
            template_data = page
            template_name = 'doc_page.txt'
            outfile = 'tmp/{}'.format(page['filename'])
            self.render_template(template_name, template_data, outfile)

    # https://github.com/cjoakim/azure-iot-cosmosdb-synapse/blob/main/presentation.md

    def documentation_structure(self):
        lines, structure = list(), list()
        lines.append('Cloud')
        lines.append('Azure,IaaS,PaaS,Costs,Innovation,Provisioning,Pets vs Cattle,DevOps,Security,Marketplace')
        lines.append('NoSQL,Know SQL,Definition,Spectrum')

        lines.append('CosmosDB Overview')
        lines.append('CosmosDB APIs,Family of Databases,SQL(Document),Mongo,Cassandra,Gremlin/Graph,Table')
        
        lines.append('CosmosDB Features')
        lines.append('CosmosDB Basics,PaaS Service,JSON,Schemaless')
        lines.append('CosmosDB Non-Features,Joins,Referential Integrity,Identity Columns')
        lines.append('Partitioning,Partition Key,Physical Partitions,Limits')
        lines.append('Request Units,Definition,Provisioned,Autoscale,Serverless')
        lines.append('Multi-Region,Consistency Levels,SDKs')
        lines.append('Server Side Programming,Stored Procedures,UDFs,Triggers')
        lines.append('Change-Feed,Azure Functions,Pipelines')
        lines.append('TTL,Benefits,Redis')
        lines.append('Spatial Support,GeoJson')
        lines.append('Azure Monitor,Kusto')

        lines.append('Design')
        lines.append('Relational-to-Cosmos,iPhone,Retail Examples,Adventureworks')
        lines.append('Design,Containers,Partition Key,Indexing')

        lines.append('Integrations')
        lines.append('Synapse Link,Synapse,Storage/Parquet,PySpark Example')
        lines.append('Azure Stream Analytics')
        lines.append('Azure Search')
        lines.append('Azure Databricks')
        lines.append('PowerBI')
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('')
        lines.append('')
        
        for line_idx, line in enumerate(lines):
            structure.append(self.page(line_idx, line))
        return structure

    def page(self, line_idx, csv_line):
        tokens = csv_line.split(',')
        page_num = '{:02d}'.format(line_idx)
        page_name = tokens[0]
        page = {}
        page['num'] = page_num
        page['name'] = page_name
        page['filename'] = '{}_{}.md'.format(page_num, page_name).lower().replace(' ','_')
        page['sections'] = list()
        for idx, tok in enumerate(tokens):
            if idx > 0:
                page['sections'].append(tok.strip())
        return page

    def timestamp(self):
        return arrow.utcnow().format('YYYY-MM-DD HH:mm:ss UTC')

    def render_template(self, template_name, template_data, outfile):
        t = self.get_template(os.getcwd(), template_name)
        s = t.render(template_data)
        self.write(outfile, s)

    def get_template(self, root_dir, name):
        filename = 'templates/{}'.format(name)
        return self.get_jinja2_env(root_dir).get_template(filename)

    def get_jinja2_env(self, root_dir):
        return jinja2.Environment(
            loader = jinja2.FileSystemLoader(
                root_dir), autoescape=True)

    def write(self, outfile, s, verbose=True):
        with open(outfile, 'w') as f:
            f.write(s)
            if verbose:
                print('file written: {}'.format(outfile))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        if func == 'generate':
            generator = MarkdownGenerator()
            generator.generate()

