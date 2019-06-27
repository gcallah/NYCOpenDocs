#!/bin/bash

OPEN_RECORDS_REPO=$1
if [ -z OPEN_RECORDS_REPO ]; then
    OPEN_RECORDS_REPO="."
fi

PYTHON_FILES=$(find ${OPEN_RECORDS_REPO} -name '*.py');
JS_FILES=$(find ${OPEN_RECORDS_REPO} -name '*.js' ! -name '*.min.js')
CSS_FILES=$(find ${OPEN_RECORDS_REPO} -name '*.css' ! -name '*.min.css')
MIN_FILES=$(find ${OPEN_RECORDS_REPO} -name '*.min.js' -o -name '*.min.css')

for filename in $PYTHON_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##$OPEN_RECORDS_REPO'/'} | sed -e 's,/,_,g' | sed -e 's/.py/.py_lint.txt/')
    echo $LINT_FILE_NAME
    REPORT=$(exec flake8 --max-line-length 120 $filename \; | sed -e 's,'$OPEN_RECORDS_REPO'/,,g')
    if [ "$REPORT"  == "" ]; then
        $(echo "No problems to report" > $LINT_FILE_NAME)
    else
        $(echo "$REPORT" > $LINT_FILE_NAME)
    fi
done

for filename in $JS_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##$OPEN_RECORDS_REPO'/'} | sed -e 's,/,_,g' | sed -e 's/.js$/.js_lint.txt/')
    echo $LINT_FILE_NAME
    length=${#PWD}
    fullPath=${PWD:0:$length-11}NYCOpenRecords/${filename##$OPEN_RECORDS_REPO'/'} 
    REPORT=$(npx eslint ${filename} | sed -e "s,$fullPath,,g")
    $(echo "$REPORT" > $LINT_FILE_NAME)
done

for filename in $CSS_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##$OPEN_RECORDS_REPO'/'} | sed -e 's,/,_,g' | sed -e 's/.css$/.css_lint.txt/')
    echo $LINT_FILE_NAME
    length=${#PWD}
    fullPath=${PWD:0:$length-11}NYCOpenRecords/${filename##$OPEN_RECORDS_REPO'/'} 
    REPORT=$(npx csslint ${filename} | sed -e "s,$fullPath,,g")
    $(echo "$REPORT" > $LINT_FILE_NAME)
done

for filename in $MIN_FILES; do
    LINT_FILE_NAME=templates/$(echo ${filename##$OPEN_RECORDS_REPO'/'} | sed -e 's,/,_,g' | sed -e 's/.js$/.js_lint.txt/' |  sed -e 's/.css$/.css_lint.txt/')
    echo $LINT_FILE_NAME
    $(echo "Linting is not performed on minified files." > $LINT_FILE_NAME)
done