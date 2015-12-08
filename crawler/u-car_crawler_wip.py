import requests, datetime, time
import pandas as pd
from bs4 import BeautifulSoup

pageNum = 12
url = 'http://forum.u-car.com.tw/index.asp?page=' + str(pageNum) + '&category=19'

index_res = requests.get(url)
index_soup = BeautifulSoup(index_res.text)

def get_linklist(soup):
    link_list = []
    for i in soup.select('a'):

        if 'thread.asp' in i['href']:
            link_list.append('http://forum.u-car.com.tw/' + i['href'])

        counter = 0
        while counter < len(link_list):
            if len(link_list[counter]) == 51:
                link_list[counter] += '&page=1'
            counter += 1
            
    for i in set(link_list):
        if len(i) == 59:
            a = int(i[-2:])

            while a > 4:
                url = i[:57] + str(a)
                if url not in link_list:
                    link_list.append(url)
                a -= 1

        elif len(i) == 60:
            a = int(i[-3:])

            while a > 4:
                url = i[:57] + str(a)
                if url not in link_list:
                    link_list.append(url)
                a -= 1

        elif len(i) == 58 and int(i[-1]) > 4:
            a = int(i[-1:])

            while a > 4:
                url = i[:57] + str(a)
                if url not in link_list:
                    link_list.append(url)
                a -= 1

    return list(set(link_list))

for i in sorted(get_linklist(index_soup)):
    print(i)