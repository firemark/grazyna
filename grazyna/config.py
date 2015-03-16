from configparser import ConfigParser
import re


class MyConfigParser(ConfigParser):

    def getlist(self, section, key, seperator=','):
        return re.split(' *%s *' % seperator, self[section][key])

    def getmodule(self, section, key):
        path, clsname = self[section][key].rsplit(".", 1)
        module = __import__(path, globals(), locals(), [clsname])
        return getattr(module, clsname)


def create_config(stream):
    config = MyConfigParser(
        comment_prefixes=[';', '//'],
        dict_type=dict
    )
    config.read_file(stream)

    return config