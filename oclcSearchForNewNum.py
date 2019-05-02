import requests
from bs4 import BeautifulSoup
import csv
import secrets
import time
import datetime

startTime = time.time()

baseURL = 'http://www.worldcat.org/webservices/catalog/content/'
wskey = secrets.wskey
f = csv.writer(open('newOclcNumResults.csv', 'w'))
f.writerow(['bibNum'] + ['search'] + ['newOclcNum'])

filename = 'noHathiTrustMatch.csv'

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    counter = 0
    for row in reader:
        counter = counter + 1
        print(counter)
        search = row['oclcNum']
        bibNum = row['bibNum']
        try:
            response = requests.get(baseURL + search.strip()
                                    + '?wskey=' + wskey).content
            record = BeautifulSoup(response, "lxml").find('record')
            oclcNum = record.find('controlfield', {'tag': '001'}).text
            oclcNum = oclcNum.lstrip('0')
        except ValueError:
            fullTitle = ''
            oclcNum = ''
        if search.lstrip('0') != oclcNum:
            print(search, oclcNum)
            f.writerow([bibNum] + [search] + [oclcNum])
        else:
            oclcNum = ''
            f.writerow([bibNum] + [search] + [oclcNum])

elapsedTime = time.time() - startTime
td = datetime.timedelta(seconds=time.time() - startTime)
print("Elapsed time: {}".format(td))
