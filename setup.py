import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'aiohttp==0.20.2',
    'dateparser==0.6.0',
    'SQLAlchemy==1.0.12',
    'lxml==4.6.3',
]

setup(
    name='grazyna',
    version='0.6.12',
    download_url='https://github.com/firemark/grazyna/tarball/0.6.12',
    description='Grazyna The irc bot',
    long_description='Grazyna The irc bot',
    classifiers=[],
    author='Firemark',
    author_email='marpiechula@gmail.com',
    url='https://github.com/firemark/grazyna',
    keywords='irc socket bot'.split(),
    packages=['grazyna'] + ['grazyna.' + p for p in find_packages('grazyna')],
    package_data={'': ['default_config.ini']},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="grazyna.firemark.tests",
)
