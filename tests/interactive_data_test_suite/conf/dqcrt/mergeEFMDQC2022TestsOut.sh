#<!-- This file was created by staff of the U.S. Securities and Exchange Commission. Data and content created by government employees within the scope of their employment are not subject to domestic copyright protection. 17 U.S.C. 105. -->
# merge out results

rm -f out/EFM-DQC-report.csv
awk 'FNR==1 && NR!=1{next;}{print}' out/EFM-DQC-2022-report-*.csv > out/EFM-DQC-2022-report.csv
