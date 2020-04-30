import urllib.request
from bs4 import BeautifulSoup
import math
def getTodaysGoldPrice():
    url="http://goldpricez.com/today-gold-rate-in-india-per-gram"
    html=urllib.request.urlopen(url).read()
    bs = BeautifulSoup(html,'lxml')
    span = bs.find_all('span')

    for s in span:
        if '1 Gram Gold Price =' in s.text:
            price=s.text.replace('\n','').split('=')[1].replace(',','')
            print(price)
            return int(float(price))
    