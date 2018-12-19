import requests
import csv
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import urllib

baseURL = 'http://www.worldcat.org/identities/find?fullName='
f=csv.writer(open('worldcatIdentitiesResults.csv', 'w'))
f.writerow(['search']+['result']+['ratio']+['partialRatio']+['tokenSort']+['tokenSet']+['avg']+['uri'])
with open('people.txt') as txt:
    for row in txt:
        rowEdited = urllib.quote(row.replace(' ', '+').strip())
        url = baseURL+rowEdited.strip()
        response = requests.get(url).content
        record = BeautifulSoup(response, "lxml").find('html').find('body').find('nameauthorities').find('match')
        try:
            label = record.find('establishedform').text
            uri = record.find('uri').text
        except:
            label = ''
            uri = ''
        ratio = fuzz.ratio(row, label)
        partialRatio = fuzz.partial_ratio(row, label)
        tokenSort = fuzz.token_sort_ratio(row, label)
        tokenSet = fuzz.token_set_ratio(row, label)
        avg = (ratio+partialRatio+tokenSort+tokenSet)/4
        f=csv.writer(open('worldcatIdentitiesResults.csv', 'a'))
        f.writerow([row.strip()]+[label]+[ratio]+[partialRatio]+[tokenSort]+[tokenSet]+[avg]+[uri])
