import requests
from bs4 import BeautifulSoup
import csv
import secrets
import time
import argparse
import os

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
baseURL = 'http://www.worldcat.org/webservices/catalog/content/'

with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    rowCount = len(list(reader))

# script content
dwnldDir = 'oclcRecords/'
if os.path.isdir(dwnldDir) is False:
    os.makedirs(dwnldDir)
with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if rowCount != 0 and rowCount % 200 == 0:
            time.sleep(5)
        if rowCount != 0 and rowCount % 3000 == 0:
            print('sleep 5 min')
            time.sleep(300)
        searchOclcNum = row['oclcNum']
        print(searchOclcNum)
        serviceLevel = '?servicelevel=full'
        classScheme = '&classificationScheme=LibraryOfCongress'
        response = requests.get(baseURL + searchOclcNum + serviceLevel
                                + classScheme + '&wskey=' + wskey)
        print(response)
        response = response.content
        record = BeautifulSoup(response, "lxml")
        f = open(dwnldDir + searchOclcNum + '.xml', 'w')
        f.write(str(record.find('record')))
        rowCount -= 1
        print('Items remaining: ', rowCount)

# print script run time
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
