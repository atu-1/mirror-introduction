#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: pylint_sample.sh <target>"
fi

tgt=${1}

files=`find ${tgt} -name "*.py"`

# pylint
for file in ${files[@]}; do
    echo "======= pylint test "${file}" ======="
    pylint ${file}
    ret=`echo $?`
    if [ ${ret} -ne 0 ]; then
        echo "Test failed (error code: "${ret}")"
        exit 1
    fi
done

# pep8
for file in ${files[@]}; do
    echo "======= pep8 test "${file}" ======="
    pep8 ${file}
    ret=`echo $?`
    if [ ${ret} -ne 0 ]; then
        exit 1
    fi
done
