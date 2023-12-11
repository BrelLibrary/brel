## Multi-Instance SHR Example Tests

This folder contains a series of multi-instance tests for Arelle with the EdgarRenderer plugin.  It's intended to deomonstrate whether Arelle is properly identifying situations where error handling differs between primary document and the independent inline XBRL instance that is an EX-26 exhibit.

There is a shell script for running each through Arelle on a BASH shell (please update any directory references to your system).

The intention of each test case is indicated in the name of its directory.  The two files, a 10-K primary document and a EX-26 exhibit document are from the SEC test suite.

The Arelle calls from the shell script use the json structure file parameter in a manner similar to how EDGAR itself invokes Arelle.

The expected situations are as follows:

Directory name pattern

mi-{seq}-pri-{status}-att-{status}{-disposition}

 * {seq} is a sequence number for the test
 * {status} is the expected validation result result:
     * gd - good (no errors or warnings)
     * {type-of-error}_ng - raises an error, not good
          * efm - EFM error
          * ix - Inline Xbrl 1.1 error
          * xbrl - XBRL 2.1 error
          * xmlval - XML element value error
          * xmlsyn - XML schema syntax error
 * {disposition} 
     * gd - good
     * suspend - the filing is suspended due to primary document error
     * strip - the filing is accepted with the EX-26 exhibit stripped due to exhibit error

