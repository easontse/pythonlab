import requests
from bs4 import BeautifulSoup

def ifExist(pageStatus):
    if pageStatus == 200 or pageStatus != 500:
        return True

def crawlData():
    for i in range(0,len(soup.select('.title'))):
        data=(crawl_another_page(i+10)[0][-4:] + '/' +
              soup.select('.date')[i].text.strip() + ',' +
              crawl_another_page(i+10)[0][-13:-5] + ',' +
              soup.select('.author')[i].text.strip() + ',' + 
              soup.select('.title')[i].text.strip() + ',' +
              crawl_another_page(i+10)[1])
        print(data.split(',')[::])
    i += 1

def crawl_another_page(x):
    yurl = 'https://www.ptt.cc' + str(soup.select('a')[x]['href'])
    yres = requests.get(yurl)
    ysoup = BeautifulSoup(yres.text,"lxml")
    if ifExist(res.status_code):
        try:
            return [ysoup.select('.article-meta-value')[3].text, yres.url]
        except IndexError:
            return ['00:00:00 0000', yres.url]
            
indexNum=1
while indexNum <= 200:
#while True:
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
    
