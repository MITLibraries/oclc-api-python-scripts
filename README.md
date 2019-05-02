# oclc-api

**Note**: Upgraded to Python 3 in 02/2019. The Python 2.x version can be downloaded [here](https://github.com/ehanson8/oclc-api/releases)

Most of these scripts require a secrets.py file in the same directory that must contain the following text (and may include other variables):

    wskey='[Your OCLC WSkey]'

More information about WSKeys is available [here](https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html).

#### [downloadMarcxmlRecords.py](downloadMarcxmlRecords.py)
Based on a list of OCLC numbers, downloads the full MARCXML records. The script is designed to pause for 5 seconds every 200 requests and for 5 minutes at every 3000 requests in order to avoid time out errors from the API.

#### [oclcHoldingsSearch.py](oclcHoldingsSearch.py)
Based on the OCLC symbols specified in secrets.py, uses a CSV of OCLC numbers and produces CSVs of matches and non-matches for record that are held by the specified institutions. For the matches, the CSV includes how many institutions hold that title amongst the institutions specified in secrets.py. The script is designed to pause for 5 seconds every 200 requests and for 5 minutes at every 3000 requests in order to avoid time out errors from the API.

#### [oclcIsbn.py](oclcIsbn.py)
Retrieves OCLC numbers and titles based on a text file of ISBNs.

#### [oclcSearchForNewNum.py](oclcSearchForNewNum.py)
Based on a list of OCLC numbers, searches for records that have been merged and now have new OCLC numbers.

#### [oclcTitleDateSearch.py](oclcTitleDateSearch.py)
Retrieves OCLC records based on a text file of titles and dates and extracts the title, URL, author, publisher, encoding level, language, physical description, and date.

#### [oclcTitlePhraseBorrowDirect.py](oclcTitlePhraseBorrowDirect.py)
Retrieves OCLC data based on a CSV from the BorrowDirect Data Repository (Beta), on the Penn Library Data Farm.

#### [oclcTitlePhrase.py](oclcTitlePhrase.py)
Retrieves OCLC records based on a text file of titles and extracts the title, URL, author, publisher, encoding level, physical description, language, and date.

#### [worldcatIdentities.py](worldcatIdentities.py)
Retrieves labels and URIs from the WorldCat Identities API based on a text file of names.
