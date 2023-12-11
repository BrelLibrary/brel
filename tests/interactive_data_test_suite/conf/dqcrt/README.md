# DQCRT 2023 Test Cases

## Introduction

This is a XBRL International style test suite to test FASB DQCRT/2023 rules implementations against us-gaap filings published in 2021-2022 for which XBRL.US expects DQC results, to ascertain that the validator produces equivalent results.

The test cases are in the standard XBRL International test case format,  used by the XII OIM suite (and many others).

The test cases are split into 16 files so they can be run on an 8 or 16 core server in parallel (it takes about 2 hours), they can be re-partitioned as applicable to the testing configuration.

The expected results were those which XBRL-US noted at time of filing with the rule set then in effect, the actual results are from testing with current rules expressed by DQCRT-2023, so in some cases there are some differences which can be manually confirmed by comparing DQC ruleset to DQCRT results, due to updates in the rules from submission time to DQCRT-2023 publication time.

Running the suite with us-gaap/2021-2022 filings against DQCRT/2023 requires a non-production mode of the validator (because EDGAR only applies the 2023 rules to current filings).  (Arelle parameters for that are described below.)

## Testcase file format

The testcase file is a declarative representation that organizes the tests in a way that a test harness can run the tests.

The testcase element is the root element for a set of individual variations.

The testcase contains these elements:

* creator
  * name
  * email
* number:  Testcase number (when part of a larger suite)
* description
* variation:  A single specific test to perform and its expected results (for DQCRT/2021 rules testing).
  * name: a brief name for test cases.
  * description: inline primary document, accession number, entry URL, filing zip URL
  * data
      * instance: Specifies public URL of accession zip file which contains the filing.  The validating tool loads the inline document set or traditional instance document contained in that zip file.
  * result: Contains error codes noted by XBRL.US at the time of filing with the rule set then in effect.  The attribute, blockedMessageCodes, specifies a negating regular expression which only allows message codes for DQCRT, in the format used by XBRL-US, so that all other warnings and messages are not matched against expected results.  For example a validator might report warning messages about hidden facts eligible for transformation, these would be filtered out by that regular expression.
      * error: Specifies the code expected (note that in EDGAR production DQCRT severities are warnings).  The Error is a code, in the format DQC.US.rule.ruleElementId, e.g. DQC.US.0048.7482 means a DQC warning, for US-GAAP (vs IFRS), for rule 0048, for rule element ID 7482.  This code format is used for testing and not reported in this format in the EDGAR production system.

### Operation with Arelle

A shell script is available which runs 16 parallel suite portions and a second shell script merges the test case results file.

Parameters unique to this run are:

*  --disclosureSystem efm-preview-dqcrt-testing: to run DQCRT/2021 rules on us-gaap/2020 filings in this non-production test mode
*  --testcaseResultsCaptureWarnings: to capture warnings in the testcase's error log
*  --testcaseResultOptions match-all: to require that all result error elements are matched (whereas the default behavior is to match-any, as in an "or" condition instead of an "and" condition).
