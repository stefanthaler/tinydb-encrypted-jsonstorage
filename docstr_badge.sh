#!/bin/bash
COV=$(docstr-coverage tinydb_encrypted_jsonstorage/ | grep "Total docstring coverage:" | cut -d":" -f 2 | cut -d";" -f1 | cut -d" " -f 2)
CMP=$(echo $COV | cut -d"." -f 1)
if [ $CMP -lt 50 ] 
then
	COLOR=#EF5350
elif [ $COV -lt 90 ]
then
	COLOR=#FFCA28
else 
	COLOR=#66BB6A	
fi


python -m pybadges --left-text=docstr-coverage --right-text=$COV --right-color=$COLOR > ./badges/doc_coverage.svg
