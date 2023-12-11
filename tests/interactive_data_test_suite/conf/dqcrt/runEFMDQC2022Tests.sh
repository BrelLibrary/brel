#<!-- This file was created by staff of the U.S. Securities and Exchange Commission. Data and content created by government employees within the scope of their employment are not subject to domestic copyright protection. 17 U.S.C. 105. -->
#!/bin/bash

# Run FASB DQCRT taxonomy tests 
#
# Tests DQCRT/2022 against 12,790 us-gaap/2021 filings
#
# Assumes 16 core cpu to run in 2.5 hrs
#
# Results have been verified by XBRL-US against their databasee of results
#
# Requires arelle disclosure system efm-preview-dqcrt-testing
#
# Result report files merged by script mergeEFMDQC2021TestsOut.sh

ARELLECMDLINESRC=/home/arelle/edgr231/arelleCmdLine.py
PYTHON=python3.9
PLUGINS='validate/EFM|inlineXbrlDocumentSet'
EFM_VAL=efm-preview-dqcrt-testing

rm -f out/EFM-DQC-2022-*

for f in $(seq 1 `ls DQC-2022-test-*.xml|wc -l`)
do
	TESTCASESROOT=DQC-2022-test-${f}.xml
	f2dig=$(printf "%02d" ${f})
	OUTPUTLOGFILE=out/EFM-DQC-2022-log-${f2dig}.log
	OUTPUTERRFILE=out/EFM-DQC-2022-err-${f2dig}.txt
	OUTPUTCSVFILE=out/EFM-DQC-2022-report-${f2dig}.csv
	TESTCASESINDEXFILE=$TESTCASESROOT

	$PYTHON $ARELLECMDLINESRC --file "$TESTCASESINDEXFILE" --noCertificateCheck --plugins $PLUGINS --disclosureSystem $EFM_VAL --validate --testcaseResultOptions match-all --csvTestReport "$OUTPUTCSVFILE" --testcaseResultsCaptureWarnings --logFile "$OUTPUTLOGFILE" 2>  "$OUTPUTERRFILE" &
	echo "$! " >> out/EFM-DQC-2022-PIDs
done
