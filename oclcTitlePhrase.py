import requests
from bs4 import BeautifulSoup
import csv
import secrets
import urllib

baseURL = 'http://www.worldcat.org/webservices/catalog/search/opensearch?q='
baseURL2 = 'http://www.worldcat.org/webservices/catalog/content/'
wskey = secrets.wskey
f=csv.writer(open('oclcTitleSearchMatches.csv', 'wb'))
f.writerow(['bibNumber']+['searchTitle']+['oclcTitle']+['oclcNum']+['url']+['author']+['publisher']+['physDesc']+['encoding']+['date'])
f2=csv.writer(open('oclcTitleSearchNonMatches.csv', 'wb'))
f2.writerow(['bibNumber']+['searchTitle'])
with open('oclcRecordsTitle.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bibNumber = row['bib#']
        print bibNumber
        searchTitle = row['245 - all subfields'][2:]
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
        search = urllib.quote(searchTitle)
        response = requests.get(baseURL+search.strip()+'&format=rss&wskey='+wskey).content
        records = BeautifulSoup(response, "lxml").findAll('item')
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
                    f.writerow([bibNumber]+[searchTitle]+[oclcTitle]+[oclcNum]+[url]+[author]+[publisher]+[physDesc]+[encoding]+[date])
            f.writerow(['']+['']+['']+['']+['']+['']+['']+['']+['']+[''])
        else:
            f2.writerow([bibNumber]+[searchTitle])
