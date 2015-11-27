import requests, psycopg2, time
from bs4 import BeautifulSoup
from datetime import datetime

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
        print(datetime.strptime(data.split(',')[0] + ' ' + data.split(',')[1], '%Y/%m/%d %H:%M:%S'),
             data.split(',')[3], data.split(',')[4], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
    i += 1

def crawl_another_page(x):
    yurl = 'https://www.ptt.cc' + str(soup.select('a')[x]['href'])
    yres = requests.get(yurl)
    ysoup = BeautifulSoup(yres.text,"lxml")
    if ifExist(res.status_code):
        try:
            return [ysoup.select('.article-meta-value')[3].text, yres.url]
        except IndexError:
            return ['00:00:00 9000', yres.url]

def connectdb():
    conn = psycopg2.connect(user='lab')
    cur = conn.cursor()

    cur.execute('''drop table if exists ptt_crawler''')

    cur.execute('''
        create table ubike (
            when_ts       timestamp,
            where_pt      point,
            code          varchar(8),
            name          varchar(32),
            area_name     varchar(32),
            space_num     int,
            avg_bike_num  real,
            max_bike_num  int,
            min_bike_num  int,
            bike_num_std  real,
            avg_space_num real,
            max_space_num int,
            min_space_num int,
            space_num_std real
        )
    ''')
    cur.execute('''create index on ubike (when_ts)''')
    cur.execute('''create index on ubike (code)''')
    cur.execute('''create index on ubike (name)''')
    cur.execute('''create index on ubike using gist (where_pt)''')

indexNum=1
while indexNum <= 1:
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
