import requests
from bs4 import BeautifulSoup

def ifExist(pageStatus):
    if pageStatus == 200 or pageStatus != 500:
        return True

def crawlData():
    for i in range(1,len(soup.select('.title'))):
            print(soup.select('.date')[i].text.strip() + ',' +
                  soup.select('.author')[i].text.strip() + ',' + 
                  "'" + soup.select('.title')[i].text.strip() + "'")
            i += 1

indexNum=1184
#while indexNum <= 150:
while True:
    url = 'https://www.ptt.cc/bbs/Yunlin/index' + str(indexNum) + '.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text)
    if ifExist(res.status_code):
        print(res.url)
        crawlData()
    else:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print(res.url,'並不存在!')
        break
    indexNum+=1