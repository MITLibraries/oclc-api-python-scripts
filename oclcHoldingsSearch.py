import requests
from bs4 import BeautifulSoup
import csv
import secrets
import urllib
import re
import time
import argparse

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileName', help='the file of data to be searched. optional - if not provided, the script will ask for input')
args = parser.parse_args()

if args.fileName:
    fileName = args.fileName
else:
    fileName = input('Enter the file of data to be searched: ')

#run time start, establish variables,
startTime = time.time()

wskey = secrets.wskey
oclcSymbols = secrets.oclcSymbols
fileNameWithoutExtension = fileName[:fileName.index('.')]

baseURL = 'http://www.worldcat.org/webservices/catalog/search/opensearch?q='
baseURL2 = 'http://www.worldcat.org/webservices/catalog/content/'

oclcSymbolsString = ''
for oclcSymbol in oclcSymbols:
    oclcSymbolsString += oclcSymbol + ','

with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    rowCount = len(list(reader))

#script content
f=csv.writer(open(fileNameWithoutExtension+'oclcSearchMatches.csv', 'w'))
f.writerow(['searchOclcNum']+['heldByMIT']+['holdingsCountNonMIT']+['holdingInstitutions'])
f2=csv.writer(open(fileNameWithoutExtension+'oclcSearchNonMatches.csv', 'w'))
f2.writerow(['searchOoclcNum']+['holdingsCount'])
with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rowCount -= 1
        if rowCount % 200 == 0:
            time.sleep(5)
        if rowCount != 0 and rowCount % 3000 == 0:
            print('sleep 5 min')
            time.sleep(300)
        print('Items remaining: ', rowCount)
        if ')' in row['oclc']:
            searchOclcNum = row['oclc'][row['oclc'].index(')')+1:]
        else:
            searchOclcNum = ''
        print(searchOclcNum)
        searchUrl = 'http://www.worldcat.org/webservices/catalog/content/libraries/' + searchOclcNum + '?maximumLibraries=100&oclcsymbol=' + oclcSymbolsString + '&wskey=' + wskey
        response = requests.get(searchUrl)
        print(response)
        response = response.content
        records = BeautifulSoup(response, "lxml")
        heldByMIT = False
        if records.findAll('diagnostics') != []:
            print('No match')
            f2.writerow([searchOclcNum]+['No match'])
        else:
            records = records.findAll('holding')
            recordInstCodes = []
            for record in records:
                instCode = record.find('institutionidentifier').find('value').text
                if instCode == 'MYG':
                    heldByMIT = True
                else:
                    recordInstCodes.append(instCode)
                holdingsCount = len(recordInstCodes)
            print(recordInstCodes)
            f.writerow([searchOclcNum]+[heldByMIT]+[holdingsCount]+[recordInstCodes])

#print script run time
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
