# oclc-api
Most of these scripts require a secrets.py file in the same directory that must contain the following text:

    wskey='[Your OCLC WSkey]'

More information about WSKeys is available [here](https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html).

#### [oclcIsbn.py](oclcIsbn.py)
This script retrieves OCLC numbers and titles based on a text file of ISBNs.

#### [oclcTitlePhraseEnhanced.py](oclcTitlePhraseEnhanced.py)
This script retrieves OCLC records based on a text file of titles and extracts the title, URL, author, publisher, encoding level, language, and date.

#### [worldcatIdentities.py](worldcatIdentities.py)
This script retrieves labels and URIs from the WorldCat Identities API based on a text file of names.
