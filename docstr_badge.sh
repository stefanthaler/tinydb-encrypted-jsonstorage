#!/bin/bash
COV=$(docstr-coverage tinydb_encrypted_jsonstorage/ | grep "Total docstring coverage:" | cut -d":" -f 2 | cut -d";" -f1 | cut -d" " -f 2)
python -m pybadges --left-text=docstr-coverage --right-text=$COV --right-color='#4c1' > ./badges/doc_coverage.svg
