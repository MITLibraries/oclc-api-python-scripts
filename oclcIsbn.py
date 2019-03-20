import requests
from bs4 import BeautifulSoup
import csv
import secrets

baseURL = 'http://www.worldcat.org/webservices/catalog/content/isbn/'
wskey = secrets.wskey
f = csv.writer(open('isbnResults.csv', 'w'))
f.writerow(['isbn'] + ['001'] + ['245'])
with open('isbns.txt') as txt:
    for row in txt:
        try:
            wskey = '?wskey=' + wskey
            response = requests.get(baseURL + row.strip() + wskey).content
            record = BeautifulSoup(response, "lxml").find('record')
            oclcNum = record.find('controlfield', {'tag': '001'}).text
            title = record.find('datafield', {'tag': '245'})
            title = title.find('subfield', {'code': 'a'}).text
            try:
                subtitle = record.find('datafield', {'tag': '245'})
                subtitle = subtitle.find('subfield', {'code': 'b'}).text
                fullTitle = title + subtitle
            except ValueError:
                fullTitle = title
        except ValueError:
            fullTitle = ''
            oclcNum = ''
        f.writerow([row.strip()] + [oclcNum] + [fullTitle])
