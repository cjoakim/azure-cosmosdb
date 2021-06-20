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


class Base(object):

    def __init__(self, line):
        self.line   = line
        self.tokens = line.split(',')
        self.url      = 'June_2021.md'
        self.next_url = 'June_2021.md'
        self.prev_url = 'June_2021.md'
        self.toc_url  = 'June_2021.md'

class Section(Base):

    def __init__(self, line):
        Base.__init__(self, line)  # Section,7,Other CosmosDB APIs
        self.number = self.tokens[1]
        self.name   = self.tokens[2]
        self.otype  = 'Section'
        self.url    = 'June_2021.md'

    def is_section(self):
        return True

    def is_page(self):
        return False

    def is_page(self):
        return False

    def number_name(self):
        return '{} - {}'.format(self.number, self.name)

    def __str__(self):
        obj = dict()
        obj['type']   = self.otype
        obj['number'] = self.number
        obj['name']   = self.name
        return json.dumps(obj, indent=2)


class Page(Base):

    def __init__(self, line, section_number, seq_number):
        Base.__init__(self, line)
        self.section_number = int(section_number)
        self.seq_number = int(seq_number)
        self.section_seq = '{:01d}.{:02d}'.format(self.section_number, self.seq_number)
        self.sections = list()
        self.name = None
        self.filename = None
        self.otype = 'Page'

        for idx, tok in enumerate(self.tokens):
            if idx > 0:
                self.sections.append(tok.strip())
            else:
                self.name = tok.strip()

        self.title = '{} {}'.format(self.section_seq, self.name)
        self.filename = '{}_{}.md'.format(
            self.section_seq.replace('.','_'), self.name).lower().replace(' ','_').replace('-','_')
        self.url = self.filename 

    def is_section(self):
        return False

    def is_page(self):
        return True

    def number_name(self):
        return '{} - {}'.format(self.section_seq, self.name)

    def template_data(self):
        data = dict()
        data['type']   = self.otype
        data['section_seq'] = self.section_seq
        data['name'] = self.name
        data['sections'] = self.sections
        data['title']    = self.title
        data['filename'] = self.filename
        data['url']      = self.url
        data['prev_url'] = self.prev_url
        data['next_url'] = self.next_url
        data['toc_url']  = self.toc_url
        return data 

    def __str__(self):
        return json.dumps(self.template_data(), indent=2)


class MarkdownGenerator(object):    

    def __init__(self):
        pass

    def generate(self):
        structure = self.documentation_structure()

        # Iterate to set previous and next urls
        prev_url, last_idx = None, len(structure) - 1

        for obj_idx, obj in enumerate(structure):
            if prev_url != None:
                obj.prev_url = prev_url
            if obj_idx < last_idx:
                obj.next_url = structure[obj_idx + 1].url
            prev_url = obj.url

        for obj in structure:
            print(obj)

        if True:
            # Generate the individual markdown pages
            for obj_idx, obj in enumerate(structure):
                if obj.is_page():
                    template_name = 'doc_page.txt'
                    outfile = 'tmp/{}'.format(obj.filename)
                    self.render_template(template_name, obj.template_data(), outfile)

        if True:
            # Generate the List of Pages for the main README.md file to copy-and-paste
            for obj_idx, obj in enumerate(structure):
                if obj.is_section():
                    print('')
                    print('## {}'.format(obj.number_name()))
                    print('')
                else:
                    # title = '{} - {}'.format(page['num'], page['name'])
                    print('- [{}]({})'.format(obj.title, obj.filename))


    # https://github.com/cjoakim/azure-iot-cosmosdb-synapse/blob/main/presentation.md

    def documentation_structure(self):
        lines, structure = list(), list()
        lines.append('Section,1,Cloud')
        lines.append('Azure,IaaS,PaaS,Costs,Innovation,Provisioning,Pets vs Cattle,DevOps,Security,Marketplace')
        lines.append('NoSQL,Know SQL,Definition,Spectrum')

        lines.append('Section,2,CosmosDB Overview')
        lines.append('CosmosDB APIs,Family of Databases,SQL(Document),Mongo,Cassandra,Gremlin/Graph,Table')
        lines.append('Cost Model')

        lines.append('Section,3,CosmosDB Features')
        lines.append('CosmosDB Basics,PaaS Service,JSON,Schemaless')
        lines.append('CosmosDB Non-Features,Joins,Referential Integrity,Identity Columns')
        lines.append('Partitioning,Partition Key,Physical Partitions,Limits')
        lines.append('Request Units,Definition,Provisioned,Autoscale,Serverless')
        lines.append('Multi-Region,Consistency Levels,SDKs,Uptime SLA,Performance SLA')
        lines.append('SQL,Examples')
        lines.append('Server Side Programming,Stored Procedures,UDFs,Triggers')
        lines.append('Change-Feed,Azure Functions,Pipelines')
        lines.append('TTL,Benefits,Redis')
        lines.append('Spatial Support,GeoJson,Query Examples')
        lines.append('Azure Monitor,Kusto')

        lines.append('Section,4,Design and Development')
        lines.append('Design Process,Query Driven,RU costs,Excel,Kusto,Iterations')
        lines.append('Design Considerations,Containers,Partition Key,Indexing,Composite Indexes')
        lines.append('Relational-to-Cosmos Example,iPhone,Retail Examples,Adventureworks')
        lines.append('Local Development,Windows Emulator,Linux Emulator,Mongo Docker,Serverless')

        lines.append('Section,5,Integrations')
        lines.append('Azure Stream Analytics')
        lines.append('Azure Functions')
        lines.append('Synapse Link,Synapse,Storage/Parquet,PySpark Example')
        lines.append('Azure Search')
        lines.append('Azure Databricks,https://devblogs.microsoft.com/cosmosdb/spark-3-connector-databricks')
        lines.append('Applications,App Service,Azure Kubernetes Service')
        lines.append('Kafka,https://devblogs.microsoft.com/cosmosdb/seamlessly-transfer-kafka-data-with-the-new-azure-cosmos-db-connector-for-confluent/')
        lines.append('PowerBI')

        lines.append('Section,6,New and Preview Features')
        lines.append('New and Preview Features,Point-in-Time Restore,Partial Document Update,Other')
        # lines.append('Point-in-Time Restore,https://docs.microsoft.com/en-us/azure/cosmos-db/continuous-backup-restore-portal')
        # lines.append('Partial Document Update,https://azure.microsoft.com/en-us/updates/partial-document-update-for-azure-cosmos-db-in-private-preview/')

        lines.append('Section,7,Other CosmosDB APIs')
        lines.append('Gremlin-Graph,Apache Tinkerpop,Bill-of-Material Example,Bulk Loader')
        lines.append('MongoDB,Migration')
        lines.append('Cassandra')
        lines.append('Table')

        lines.append('Section,8,Summary')
        lines.append('Summary,Questions,Contact Info')

        curr_section_number, seq_number = 0, 0

        for line_idx, line in enumerate(lines):
            if line.lower().startswith('section,'):
                s = Section(line)
                curr_section_number = s.number
                seq_number = 0
                structure.append(s)
            else:
                seq_number = seq_number + 1
                p = Page(line, curr_section_number, seq_number)
                structure.append(p)
        return structure

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

