__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com,christopher.joakim@gmail.com"
__license__ = "MIT"
__version__ = "2020.05.28"

import os
import time

import jinja2


class Template(object):

    @classmethod
    def get_template(cls, root_dir, name):
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
