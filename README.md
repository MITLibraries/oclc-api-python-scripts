# oclc-api
Most of these scripts require a secrets.py file in the same directory that must contain the following text:

    wskey='[Your OCLC WSkey]'

More information about WSKeys is available [here](https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html).

#### [oclcIsbn.py](oclcIsbn.py)
Retrieves OCLC numbers and titles based on a text file of ISBNs.

#### [oclcSearchForNewNum.py](oclcSearchForNewNum.py)
Based on a list of OCLC numbers, searchs for records that have been merged and now have new OCLC numbers.

#### [oclcTitleDateSearch.py](oclcTitleDateSearch.py)
Retrieves OCLC records based on a text file of titles and dates and extracts the title, URL, author, publisher, encoding level, language, physical description, and date.

#### [oclcTitlePhraseBorrowDirect.py](oclcTitlePhraseBorrowDirect.py)
Retrieves OCLC data based on a CSV from the BorrowDirect Data Repository (Beta), on the Penn Library Data Farm.

#### [oclcTitlePhrase.py](oclcTitlePhrase.py)
Retrieves OCLC records based on a text file of titles and extracts the title, URL, author, publisher, encoding level, physical description, language, and date.

#### [worldcatIdentities.py](worldcatIdentities.py)
Retrieves labels and URIs from the WorldCat Identities API based on a text file of names.
