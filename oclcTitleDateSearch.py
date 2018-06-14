import requests
from bs4 import BeautifulSoup
import csv
import secrets
import urllib
import re

baseURL = 'http://www.worldcat.org/webservices/catalog/search/opensearch?q='
baseURL2 = 'http://www.worldcat.org/webservices/catalog/content/'
wskey = secrets.wskey
f=csv.writer(open('oclcTitleDateSearchMatches.csv', 'wb'))
f.writerow(['bibNumber']+['searchTitle']+['searchDate']+['searchType']+['oclcTitle']+['date']+['oclcNum']+['url']+['author']+['publisher']+['physDesc']+['encoding'])
f2=csv.writer(open('oclcTitleDateSearchNonMatches.csv', 'wb'))
f2.writerow(['bibNumber']+['searchTitle']+['searchDate'])
with open('oclcRecordsTitle.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bibNumber = row['bib#']
        print bibNumber
        searchType = 'date & title'
        searchTitle = row['245 - all subfields'][2:]
        if row['260 - all subfields'] != '':
            if 'c' in row['260 - all subfields']:
                searchDate = row['260 - all subfields']
                searchDate = searchDate[searchDate.index('c')+2:].strip()
                searchDate = re.sub('[^\d-]+', '', searchDate)
                query = 'srw.yr+%3D+"'+searchDate+'"+and+'
            else:
                query = ''
        elif row['260 - all subfields'] != '':
            if 'c' in row['264 - all subfields']:
                searchDate = row['264 - all subfields']
                searchDate = searchDate[searchDate.index('c')+2:].strip()
                searchDate = re.sub('[^\d-]+', '', searchDate)
                query = 'srw.yr+%3D+"'+searchDate+'"+and+'
            else:
                query = ''
        else:
            query = ''
        originalTitle = searchTitle
        if 'b' in searchTitle:
            searchTitle = searchTitle[:searchTitle.index('b')] + ' ' + searchTitle[searchTitle.index('b')+2:]
            if 'c' in searchTitle:
                searchTitle = searchTitle[:searchTitle.index('c')]
            else:
                pass
        elif 'c' in searchTitle:
            searchTitle = searchTitle[:searchTitle.index('c')]
        else:
            pass
        searchTitleURL = urllib.quote(searchTitle).strip()
        query = baseURL + query + 'srw.ti+%3D+"'+ searchTitleURL + '"&format=rss&wskey='+wskey
        print query
        response = requests.get(query).content
        records = BeautifulSoup(response, 'lxml').findAll('item')
        if records != []:
            for record in records:
                oclcTitle = record.find('title').text.encode('utf-8')
                url = record.find('guid').text.encode('utf-8')
                oclcNum = url.replace('http://worldcat.org/oclc/','')
                author = record.find('author').find('name').text.encode('utf-8')
                response2 = requests.get(baseURL2+oclcNum+'?servicelevel=full&classificationScheme=LibraryOfCongress&wskey='+wskey).content
                record2 = BeautifulSoup(response2, "lxml").find('record')
                encoding = record2.find('leader').text[17].encode('utf-8')
                type = record2.find('controlfield', {'tag' : '008'}).text[23:24]
                date = record2.find('controlfield', {'tag' : '008'}).text[7:11].encode('utf-8')
                try:
                    publisher = record2.find('datafield', {'tag' : '260'}).find('subfield', {'code' : 'b'}).text.encode('utf-8')
                except:
                    try:
                        publisher = record2.find('datafield', {'tag' : '264'}).find('subfield', {'code' : 'b'}).text.encode('utf-8')
                    except:
                        publisher = ''
                try:
                    catLang =  record2.find('datafield', {'tag' : '040'}).find('subfield', {'code' : 'b'}).text.encode('utf-8')
                except:
                    catLang = ''
                try:
                    physDesc =  record2.find('datafield', {'tag' : '300'}).find('subfield', {'code' : 'a'}).text.encode('utf-8')
                except:
                    physDesc = ''
                if type == ' ' and (catLang == 'eng' or catLang == ''):
                    f.writerow([bibNumber]+[searchTitle]+[searchDate]+[searchType]+[oclcTitle]+[date]+[oclcNum]+[url]+[author]+[publisher]+[physDesc]+[encoding])
            f.writerow(['']+['']+['']+['']+['']+['']+['']+['']+['']+[''])
        else:
            f2.writerow([bibNumber]+[searchTitle]+[searchDate])
