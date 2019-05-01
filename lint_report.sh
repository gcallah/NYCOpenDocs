#!/bin/bash

PYTHON_FILES=$(find ../NYCOpenRecords -name '*.py');

for filename in $PYTHON_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##'../NYCOpenRecords/'} | sed -e 's,/,_,g' | sed -e 's/.py/.py_lint.txt/')
    $(exec flake8 --max-line-length 120 $filename \; | sed -e 's,../NYCOpenRecords/,,g' > $LINT_FILE_NAME)
done