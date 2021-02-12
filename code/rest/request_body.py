__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2021.02.11"

import json
import os
import time

import jinja2


class RequestBody(object):

    @classmethod
    def create_db(cls, dbname):
        values = dict()
        values['dbname'] = dbname
        template = cls.get_template('create_db.txt')
        return json.loads(cls.render(template, values))

    @classmethod
    def create_container(cls, cname, pk, indexing_type='default'):
        values = dict()
        values['cname'] = cname
        values['pk'] = pk
        tname = 'create_container_{}_indexing.txt'.format(indexing_type)
        template = cls.get_template(tname)
        return json.loads(cls.render(template, values))

    @classmethod
    def replace_database_autopilot_offer(cls, ru, resource, offerResourceId, id, rid):
        values = dict()
        values['offerThroughput'] = ru
        values['resource'] = resource
        values['offerResourceId'] = offerResourceId
        values['id'] = id
        values['rid'] = rid
        tname = 'replace_db_autopilot_offer.txt'
        template = cls.get_template(tname)
        return json.loads(cls.render(template, values))

    @classmethod
    def replace_container_offer(cls, ru, resource, offerResourceId, id, rid):
        values = dict()
        values['offerThroughput'] = ru
        values['resource'] = resource
        values['offerResourceId'] = offerResourceId
        values['id'] = id
        values['rid'] = rid
        tname = 'replace_container_offer.txt'
        template = cls.get_template(tname)
        return json.loads(cls.render(template, values))

    # class private methods 

    @classmethod
    def get_template(cls, name):
        root_dir = os.getcwd()
        filename = 'templates/{}'.format(name)
        return cls.get_jinja2_env(root_dir).get_template(filename)

    @classmethod
    def render(cls, template, values):
        return template.render(values)

    @classmethod
    def get_jinja2_env(cls, root_dir):
        print('get_jinja2_env root_dir: {}'.format(root_dir))
        return jinja2.Environment(
            loader = jinja2.FileSystemLoader(
                root_dir), autoescape=True)
