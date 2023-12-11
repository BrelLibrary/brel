#!/bin/bash
set -ex

# re-generate arelle's formula-assertion-style testcase file from test.xml authoritative testcase file
java -jar saxon9.jar tests.xml extractTestcase.xsl  > testcase.xml

# to run from source
ARELLE="C:/Python/Python38/python.exe W:/git-group2/sec-arelle/arelle-src/arelleCmdLine.py"

# remove old log files
rm -f out/ixt-sec*

# run test cases
$ARELLE --plugins transforms/SEC -f testcase.xml -v --logFile out/ixt-sec-arelle.log --csvTestReport out/ixt-sec-arelle.csv

