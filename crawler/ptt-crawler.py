import requests
from bs4 import BeautifulSoup

def ifExist(pageStatus):
    if pageStatus == 200 or pageStatus != 500:
        return True

def crawlData(i):
    data = (crawl_another_page(i+10)[0][-4:] + '/' +
            soup.select('.date')[i].text.strip() + ',' +
            crawl_another_page(i+10)[0][-13:-5] + ',' +
            soup.select('.author')[i].text.strip() + ',' + 
            soup.select('.title')[i].text.strip() + ',' +
            crawl_another_page(i+10)[1])
    return data.split(',')
    
def crawl_another_page(x):
    yurl = 'https://www.ptt.cc' + str(soup.select('a')[x]['href'])
    yres = requests.get(yurl)
    ysoup = BeautifulSoup(yres.text,"lxml")
    
    if ifExist(res.status_code):
        try:
            return [ysoup.select('.article-meta-value')[3].text, yres.url]
        except IndexError:
            return ['00:00:00 0000', yres.url]
            
def loadptt():
    indexNum=1
    
    while indexNum <= 1:
    #while True:
        url = 'https://www.ptt.cc/bbs/Yunlin/index' + str(indexNum) + '.html'
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"lxml")
        
        if ifExist(res.status_code):
            
            print(res.url)
            
            for i in range(0,len(soup.select('.title'))):
                print(crawlData(i)[0])
                i += 1
                
            indexNum+=1
            
        else:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            print(res.url,'並不存在!')
            break

loadptt()
