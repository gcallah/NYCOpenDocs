#!/bin/bash

PYTHON_FILES=$(find ../NYCOpenRecords -name '*.py');
JS_FILES=$(find ../NYCOpenRecords -name '*.js' ! -name '*.min.js')

for filename in $PYTHON_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##'../NYCOpenRecords/'} | sed -e 's,/,_,g' | sed -e 's/.py/.py_lint.txt/')
    REPORT=$(exec flake8 --max-line-length 120 $filename \; | sed -e 's,../NYCOpenRecords/,,g')
    if [ "$REPORT"  == "" ]; then
        $(echo "No problems to report" > $LINT_FILE_NAME)
    else
        $(echo "$REPORT" > $LINT_FILE_NAME)
    fi
done

for filename in $JS_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##'../NYCOpenRecords/'} | sed -e 's,/,_,g' | sed -e 's/.js$/.js_lint.txt/')
    echo $LINT_FILE_NAME
    length=${#PWD}
    fullPath=${PWD:0:$length-11}NYCOpenRecords/${filename##'../NYCOpenRecords/'} 
    REPORT=$(npx eslint ${filename} | sed -e "s,$fullPath,,g")
    $(echo "$REPORT" > $LINT_FILE_NAME)
done