from configparser import ConfigParser

parser = ConfigParser({
    'main': {
        'admins': None,
        'channels': None,
        'password': 'hurr-durr',
    },
    'auth': {
        'module': 'grazyna.plugins.NonAuth'
    },
    'plugins': {}
})