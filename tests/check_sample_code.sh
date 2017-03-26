#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: pylint_sample.sh <target>"
fi

tgt=${1}

files=`find ${tgt} -name "*.py"`

# pylint
for file in ${files[@]}; do
    pylint ${file}
    ret=`echo $?`
    if [ ${ret} -ne 0 ]; then
        exit 1
    fi
done

# pep8
for file in ${files[@]}; do
    pep8 ${file}
    ret=`echo $?`
    if [ ${ret} -ne 0 ]; then
        exit 1
    fi
done
