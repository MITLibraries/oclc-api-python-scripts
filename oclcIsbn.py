import requests
from bs4 import BeautifulSoup
import csv
import secrets

baseURL = 'http://www.worldcat.org/webservices/catalog/content/isbn/'
wskey = secrets.wskey
f=csv.writer(open('isbnResults.csv', 'w'))
f.writerow(['isbn']+['001']+['245'])
with open('isbns.txt') as txt:
    for row in txt:
        try:
            response = requests.get(baseURL+row.strip()+'?wskey='+wskey).content
            record = BeautifulSoup(response, "lxml").find('record')
            oclcNum = record.find('controlfield', {'tag' : '001'}).text
            title = record.find('datafield', {'tag' : '245'}).find('subfield', {'code' : 'a'}).text
            try:
                subtitle = record.find('datafield', {'tag' : '245'}).find('subfield', {'code' : 'b'}).text
                fullTitle = title + subtitle
            except:
                fullTitle = title
        except:
            fullTitle = ''
            oclcNum = ''
        f.writerow([row.strip()]+[oclcNum]+[fullTitle])
