[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=C8FBBG2RZ5WYS&currency_code=EUR&source=url)

# tinydb-encrypted-jsonstorage
A TinyDB storage implementation that stores values as encrypted json.

# Requirements
## Python
* [TinyDB](https://tinydb.readthedocs.io/en/latest/getting-started.html)
* [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/)

## OS Dependencies:
* python3, python3-venv, python3-pip

# Get Sources
* git clone git@github.com:stefanthaler/tinydb-encrypted-jsonstorage.git
* cd tinydb-encrypted-jsonstorage
* python3 -m venv .env
* . .env/bin/activate.fish  
* pip install -r requirements.txt

# Build
* follow steps in "Get Sources"
* pip3 install -r requirements-building.txt
* python setup.py bdist_wheel

# Test
* follow steps in "Get Sources"
* pip3 install -r requirements-building.txt
* python setup.py test

# Install

## Pip
* pip install tinydb-encrypted-jsonstorage

## Pip + Git
* pip install git+git://github.com/stefanthaler/tinydb-encrypted-jsonstorag.git#egg=tinydb-encrypted-jsonstorage

## Git + Local Pip
* Follow steps in "Build"
* pip install ./

# Use

TODO add example here 




# Thanks  
* Shields.io, for providing the github paypal button: https://shields.io/
