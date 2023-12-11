#<!-- This file was created by staff of the U.S. Securities and Exchange Commission. Data and content created by government employees within the scope of their employment are not subject to domestic copyright protection. 17 U.S.C. 105. -->
#!/bin/bash
# Run Multi-Instance ArelleWrapper Interface Tests

ARELLE=${ARELLE_HOME}/arelleCmdLine.py

rm -fr logs
mkdir logs
find . -name Report -type d -exec rm -fr {} \;
find . -name out -type d -exec rm -fr {} \;

for testdir in mi*;
  do
    echo test $testdir
    cd $testdir
    python3 $ARELLE --plugin EdgarRenderer --disclosureSystem efm-pragmatic -v -f '[{"file":"eelo00001gd-20340331.htm","attachmentDocumentType":"10-K"},{"file":"eelo00002gd-20340331.htm","attachmentDocumentType":"EX-26"}]' --logFile ../logs/log_${testdir}.xml
    cd ..
    if [[ $testdir == *gd ]]; then
	# want to fail if any "<entry .* level="error">" is anywhere in log file
	if grep -E -q 'level="error"' logs/log_${testdir}.xml; then
   	  echo "   fail, errors found"
	fi
	# want to fail if '<entry code="EFM.stripExhibit" level="info-result">\n <message exhibitType="EX-26" files="eelo00002gd' in log file 
	if grep -E -q 'EFM.stripExhibit' logs/log_${testdir}.xml; then
  	  echo "   fail, strip exhibit list found"
	fi
    fi
    if [[ $testdir == *strip ]]; then
	# want to fail if no '<entry code="EFM.stripExhibit" level="info-result">\n <message exhibitType="EX-26" files="eelo00002gd' in log file 
	if ! grep -E -q 'EFM.stripExhibit' logs/log_${testdir}.xml; then
  	  echo "   fail, no strip exhibit list found"
	fi
    fi
    if [[ $testdir == *suspend ]]; then
	# want to fail if no 'level="error">\n <message.*eelo00001gd' in log file
	if ! grep -E -q 'level="error"' logs/log_${testdir}.xml; then
   	  echo "   fail, no errors found"
	fi
	# want to fail if '<entry code="EFM.stripExhibit" level="info-result">\n <message exhibitType="EX-26" files="eelo00002gd' in log file 
	if grep -E -q 'EFM.stripExhibit' logs/log_${testdir}.xml; then
  	  echo "   fail, strip exhibit list found"
	fi
    fi
  done
