from configparser import ConfigParser
from importlib import import_module
import re


class MyConfigParser(ConfigParser):

    def getlist(self, section, key, seperator=','):
        return re.split(' *%s *' % seperator, self[section][key])

    def getmodule(self, section, key):
        module_fullpath = self[section][key]
        module_path, _, cls_path = module_fullpath.rpartition('.') 
        module = import_module(module_path) 
        return getattr(module, cls_path)


def create_empty_config():
    return MyConfigParser(
        comment_prefixes=[';', '//'],
        dict_type=dict,
    )


def create_config(stream):
    config = create_empty_config()
    config.read_file(stream)

    return config
