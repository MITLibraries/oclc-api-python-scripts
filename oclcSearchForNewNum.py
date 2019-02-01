import requests
from bs4 import BeautifulSoup
import csv
import secrets
import time

startTime = time.time()

baseURL = 'http://www.worldcat.org/webservices/catalog/content/'
wskey = secrets.wskey
f=csv.writer(open('newOclcNumResults.csv', 'w'))
f.writerow(['bibNum']+['search']+['newOclcNum'])

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
            response = requests.get(baseURL+search.strip()+'?wskey='+wskey).content
            record = BeautifulSoup(response, "lxml").find('record')
            oclcNum = record.find('controlfield', {'tag' : '001'}).text.lstrip('0')
        except:
            fullTitle = ''
            oclcNum = ''
        if search.lstrip('0') != oclcNum:
            print(search, oclcNum)
            f.writerow([bibNum]+[search]+[oclcNum])
        else:
            oclcNum = ''
            f.writerow([bibNum]+[search]+[oclcNum])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
