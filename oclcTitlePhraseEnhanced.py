import requests
from bs4 import BeautifulSoup
import csv
import secrets

baseURL = 'http://www.worldcat.org/webservices/catalog/search/opensearch?q='
baseURL2 = 'http://www.worldcat.org/webservices/catalog/content/'
wskey = secrets.wskey
f=csv.writer(open('resultsTitle.csv', 'wb'))
f.writerow(['bibNumber']+['horizonTitle']+['oclcTitle']+['url']+['author']+['publisher']+['encoding']+['lang']+['date'])
with open('oclcRecordsTitle.txt') as txt:
    for row in txt:
        bibNumber = row[:row.index('|')]
        horizonTitle = row[row.index('|')+1:]
        search = horizonTitle.replace(' ','%20')
        response = requests.get(baseURL+search.strip()+'&format=rss&wskey='+wskey).content
        records = BeautifulSoup(response, "lxml").findAll('item')
        for record in records:
            try:
                title = record.find('title').text.encode('utf-8')
                url = record.find('guid').text.encode('utf-8')
                author = record.find('author').find('name').text.encode('utf-8')
            except:
                title = ''
                url = ''
                author = ''
            recordNumber = url.replace('http://worldcat.org/oclc/','')
            response2 = requests.get(baseURL2+recordNumber+'?classificationScheme=LibraryOfCongress&wskey='+wskey).content
            record2 = BeautifulSoup(response2, "lxml").find('record')
            try:
                encoding = record2.find('leader').text[17].encode('utf-8')
                date = record2.find('controlfield', {'tag' : '008'}).text[7:11].encode('utf-8')
                lang = record2.find('controlfield', {'tag' : '008'}).text[35:38].encode('utf-8')
            except:
                date = ''
                lang = ''
                encoding = ''
            try:
                publisher = record2.find('datafield', {'tag' : '260'}).find('subfield', {'code' : 'b'}).text.encode('utf-8')
            except:
                try:
                    publisher = record2.find('datafield', {'tag' : '264'}).find('subfield', {'code' : 'b'}).text.encode('utf-8')
                except:
                    publisher = ''
            f.writerow([bibNumber]+[horizonTitle]+[title]+[url]+[author]+[publisher]+[encoding]+[lang]+[date])
