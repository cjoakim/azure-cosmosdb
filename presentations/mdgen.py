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
        self.line = line
        self.tokens = tokens.split()

class Section(Base):

    def __init__(self, line):
        Base.__init__(self, line)

    def is_section(self):
        return True

    def is_page(self):
        return False


class Page(Base):

    def __init__(self, line, tokens):
        Base.__init__(self, line)

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

    def is_section(self):
        return False

    def is_page(self):
        return True


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
        lines.append('Section,1,Cloud')
        lines.append('Azure,IaaS,PaaS,Costs,Innovation,Provisioning,Pets vs Cattle,DevOps,Security,Marketplace')
        lines.append('NoSQL,Know SQL,Definition,Spectrum')

        lines.append('Section,2,,CosmosDB Overview')
        lines.append('CosmosDB APIs,Family of Databases,SQL(Document),Mongo,Cassandra,Gremlin/Graph,Table')
        lines.append('Cost Model')

        lines.append('Section,3,CosmosDB Features')
        lines.append('CosmosDB Basics,PaaS Service,JSON,Schemaless,')
        lines.append('CosmosDB Non-Features,Joins,Referential Integrity,Identity Columns')
        lines.append('Partitioning,Partition Key,Physical Partitions,Limits')
        lines.append('Request Units,Definition,Provisioned,Autoscale,Serverless')
        lines.append('Multi-Region,Consistency Levels,SDKs,Uptime SLA,Performance SLA')
        lines.append('SQL,Examples')
        lines.append('Server Side Programming,Stored Procedures,UDFs,Triggers')
        lines.append('Change-Feed,Azure Functions,Pipelines')
        lines.append('TTL,Benefits,Redis')
        lines.append('Spatial Support,GeoJson')
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
        lines.append('Future API1')
        lines.append('Future API2')
        lines.append('Future API3')

        lines.append('Section,8,Summary')
        lines.append('Thank you,Contact Info')

        for line_idx, line in enumerate(lines):
            if line.lower().startswith('section,'):
                structure.append(Section(line))
            else:
                structure.append(Page(line))
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

