from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__)) # find current file place in abs path

# print readme.rst
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name = 'epyb',
    version = '0.1.6',
    description = 'A tool which allows you to download books from certain websites and convert to epub for you automatically.',
    long_description= 'An integration of customer google search + web scraper for book site + epub convert.',
    url = 'https://rioaraki.github.io/epyb',
    author= 'Yue Li',
    author_email='yueee.li@mail.utoronto.ca',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords = 'online book epub converter',
    packages = find_packages(), # TODO: research how it works
    install_requires=['requests',
                      'bs4',
                      'google-api-python-client']
)