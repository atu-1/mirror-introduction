#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: pylint_sample.sh <target>"
fi

tgt=${1}

files=`find ${tgt} -name ".py"`

for file in ${files[@]}; do
    pylint ${file}
done
