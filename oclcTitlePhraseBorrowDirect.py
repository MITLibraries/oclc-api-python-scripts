import requests
from bs4 import BeautifulSoup
import csv
import secrets
import urllib
import re
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileName', help='the file of Borrow Direct data. optional - if not provided, the script will ask for input')
args = parser.parse_args()

if args.fileName:
    fileName = args.fileName
else:
    fileName = input('Enter the file of Borrow Direct data: ')

startTime = time.time()

fileNameWithoutExtension = fileName[:fileName.index('.')]

baseURL = 'http://www.worldcat.org/webservices/catalog/search/opensearch?q='
baseURL2 = 'http://www.worldcat.org/webservices/catalog/content/'

with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    rowCount = len(list(reader))

wskey = secrets.wskey
f=csv.writer(open(fileNameWithoutExtension+'oclcSearchMatches.csv', 'w'))
f.writerow(['searchOclcNum']+['borrower']+['lender']+['status']+['patronType']+['isbn']+['searchTitle']+['searchAuthor']+['searchDate']+['oclcNum']+['oclcTitle']+['oclcAuthor']+['oclcPublisher']+['callNumLetters']+['callNumFull']+['physDesc']+['oclcDate'])
f2=csv.writer(open(fileNameWithoutExtension+'oclcSearchNonMatches.csv', 'w'))
f2.writerow(['searchOoclcNum']+['borrower']+['lender']+['status']+['patronType']+['isbn']+['searchTitle']+['searchAuthor']+['searchDate'])
with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rowCount -= 1
        print('Items remaining: ', rowCount)
        borrower = row['BORROWER']
        lender = row['LENDER']
        status = row['STATUS']
        patronType = row['PATRON TYPE']
        searchOclcNum = row['OCLC']
        print(searchOclcNum)
        isbn = row['ISBN']
        searchAuthor = row['AUTHOR']
        searchTitle = row['TITLE']
        searchPublisher = row['PUBLISHER']
        searchDate = row['PUBLICATION YEAR']
        try:
            response = requests.get('http://www.worldcat.org/webservices/catalog/content/'+searchOclcNum+'?format=rss&wskey='+wskey)
            response = response.content
            record = BeautifulSoup(response, "lxml").find('record')
            oclcNum = record.find('controlfield', {'tag' : '001'}).text
            print('search oclc #')
        except:
            originalTitle = searchTitle
            search = urllib.quote(searchTitle)
            response = requests.get(baseURL+search.strip()+'&count=1&format=rss&wskey='+wskey)
            print('search title')
            response = response.content
            record = BeautifulSoup(response, "lxml").findAll('item')
            if record != []:
                record = record[0]
                url = record.find('guid').text
                oclcNum = url.replace('http://worldcat.org/oclc/','')
                oclcAuthor = record.find('author').find('name').text

        response2 = requests.get(baseURL2+oclcNum+'?servicelevel=full&classificationScheme=LibraryOfCongress&wskey='+wskey)
        print('search full record')
        response2 = response2.content
        try:
            record2 = BeautifulSoup(response2, "lxml").find('record')
            try:
                titleA = record2.find('datafield', {'tag' : '245'}).find('subfield', {'code' : 'a'}).text
            except:
                titleA = ''
            try:
                titleB = record2.find('datafield', {'tag' : '245'}).find('subfield', {'code' : 'b'}).text
            except:
                titleB = ''
            oclcTitle = titleA + ' ' + titleB
            oclcDate = record2.find('controlfield', {'tag' : '008'}).text[7:11]
            try:
                callNumFullA = record2.find('datafield', {'tag' : '050'}).find('subfield', {'code' : 'a'}).text
                numStart = re.search('\d', callNumFullA)
                callNumLetters = callNumFullA[:numStart.start()]
            except:
                callNumFullA = ''
                callNumLetters = ''
            try:
                callNumFullB = record2.find('datafield', {'tag' : '050'}).find('subfield', {'code' : 'b'}).text
            except:
                callNumFullB = ''
            callNumFull = callNumFullA + ' ' + callNumFullB
            try:
                oclcPublisher = record2.find('datafield', {'tag' : '260'}).find('subfield', {'code' : 'b'}).text
            except:
                try:
                    oclcPublisher = record2.find('datafield', {'tag' : '264'}).find('subfield', {'code' : 'b'}).text
                except:
                    oclcPublisher = ''
            try:
                physDesc =  record2.find('datafield', {'tag' : '300'}).find('subfield', {'code' : 'a'}).text
            except:
                physDesc = ''
            f.writerow([searchOclcNum]+[borrower]+[lender]+[status]+[patronType]+[isbn]+[searchTitle]+[searchAuthor]+[searchDate]+[oclcNum]+[oclcTitle]+[oclcAuthor]+[oclcPublisher]+[callNumLetters]+[callNumFull]+[physDesc]+[oclcDate])
            oclcNum = ''
            oclcTitle = ''
            oclcAuthor = ''
            callNumLetters = ''
            callNumFull = ''
            oclcPublisher = ''
            oclcDate = ''
        except:
            f2.writerow([searchOclcNum]+[borrower]+[lender]+[status]+[patronType]+[isbn]+[searchTitle]+[searchAuthor]+[searchDate])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
