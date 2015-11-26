import requests
from bs4 import BeautifulSoup

def ifExist(pageStatus):
    if pageStatus == 200 or pageStatus != 500:
        return True

def crawlData():
    for i in range(0,len(soup.select('.title'))):
        print(getYear(i+10)[-4:] + '/' +
            soup.select('.date')[i].text.strip() + ',' +
            soup.select('.author')[i].text.strip() + ',' + 
            "'" + soup.select('.title')[i].text.strip() + "'")
    i += 1

def getYear(x):
    try:
        soup.select('a')[x]['href']
    except IndexError:
        return '0001'
    yurl = 'https://www.ptt.cc' + str(soup.select('a')[x]['href'])
    yres = requests.get(yurl)
    ysoup = BeautifulSoup(yres.text,"lxml")
    try:
        return ysoup.select('.article-meta-value')[3].text
    except IndexError:
        return '0000'
    
        
    
indexNum=1175
#while indexNum <= 1180:
while True:
    url = 'https://www.ptt.cc/bbs/Yunlin/index' + str(indexNum) + '.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    if ifExist(res.status_code):
        print(res.url)
        crawlData()
        indexNum+=1
    else:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print(res.url,'並不存在!')
        break
    
