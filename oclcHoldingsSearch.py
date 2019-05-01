import requests
from bs4 import BeautifulSoup
import csv
import secrets
import time
import datetime
import argparse

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileName', help='the file of data to be searched. \
optional - if not provided, the script will ask for input')
args = parser.parse_args()

if args.fileName:
    fileName = args.fileName
else:
    fileName = input('Enter the file of data to be searched: ')

# run time start, establish variables,
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

# script content
f = csv.writer(open(fileNameWithoutExtension + 'oclcSearchMatches.csv', 'w'))
f.writerow(['bartonId'] + ['searchOclcNum'] + ['heldByMIT']
           + ['holdingsCountNonMIT'] + ['holdingInstitutions'])
f2 = csv.writer(open(fileNameWithoutExtension
                + 'oclcSearchNonMatches.csv', 'w'))
f2.writerow(['searchOoclcNum'] + ['holdingsCount'])
with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rowCount -= 1
        if rowCount != 0 and rowCount % 200 == 0:
            time.sleep(5)
        if rowCount != 0 and rowCount % 3000 == 0:
            print('sleep 5 min')
            time.sleep(300)
        print('Items remaining: ', rowCount)
        bartonId = row['bartonId']
        if ')' in row['oclcNum']:
            searchOclcNum = row['oclcNum'][row['oclcNum'].index(')') + 1:]
        else:
            searchOclcNum = row['oclcNum']
        print(searchOclcNum)
        searchUrl = 'http://www.worldcat.org/'
        searchUrl = searchUrl + 'webservices/catalog/content/libraries/'
        searchUrl = searchUrl + searchOclcNum
        searchUrl = searchUrl + '?maximumLibraries=100&oclcsymbol='
        searchUrl = searchUrl + oclcSymbolsString + '&wskey=' + wskey
        response = requests.get(searchUrl)
        print(response)
        response = response.content
        records = BeautifulSoup(response, "lxml")
        heldByMIT = False
        if records.findAll('diagnostics') != []:
            print('No match')
            f2.writerow([searchOclcNum] + ['No match'])
        else:
            records = records.findAll('holding')
            recordInstCodes = []
            for record in records:
                instCode = record.find('institutionidentifier')
                instCode = instCode.find('value').text
                if instCode == 'MYG':
                    heldByMIT = True
                else:
                    recordInstCodes.append(instCode)
                holdingsCount = len(recordInstCodes)
            print(recordInstCodes)
            f.writerow([bartonId] + [searchOclcNum] + [heldByMIT]
                       + [holdingsCount] + [recordInstCodes])

# print script run time
td = datetime.timedelta(seconds=time.time() - startTime)
print("Elapsed time: {}".format(td))
