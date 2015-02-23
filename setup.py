import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'requests==2.5.1'
]

setup(
    name='grazyna',
    version='0.5',
    description='Grazyna The irc bot',
    long_description='Grazyna The irc bot',
    classifiers=[],
    author='Firemark',
    author_email='marpiechula@gmail.com',
    url='https://github.com/firemark/grazyna',
    keywords='irc socket bot',
    packages=['grazyna'] + ['grazyna.' + p for p in find_packages('grazyna')],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="grazyna.firemark.tests",
)
