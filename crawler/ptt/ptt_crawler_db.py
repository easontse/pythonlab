import requests, psycopg2, time
from bs4 import BeautifulSoup
from datetime import datetime

def ifExist(pageStatus):
    if pageStatus == 200 or pageStatus != 500:
        return True

def full_or_half_width_char(x):
    if '：' in crawlData(x)[1]:
        return crawlData(x)[1].replace('：',':')
    
    
def crawlData(titleNum):
    data = (crawl_another_page(titleNum + 10)[0][-4:] + '/' +
            soup.select('.date')[titleNum].text.strip() + ',' +
            crawl_another_page(titleNum + 10)[0][-13:-5] + ',' +
            soup.select('.author')[titleNum].text.strip() + ',' + 
            soup.select('.title')[titleNum].text.strip() + ',' +
            crawl_another_page(titleNum + 10)[1])
    return data.split(',')
    
def crawl_another_page(x):
    yurl = 'https://www.ptt.cc' + str(soup.select('a')[x]['href'])
    
    while True:
        try:
            yres = requests.get(yurl, verify=False)
            break
        except KeyboardInterrupt:
            print('Interrupted by operator :S')
            break
        except:
            print('Retry after 3 sec...')
            time.sleep(3)        
            yres = requests.get(yurl, verify=False)
    
    ysoup = BeautifulSoup(yres.text,"lxml")
#    if ifExist(yres.status_code):
    try:
        return [ysoup.select('.article-meta-value')[3].text, yres.url]
    except IndexError:
        return ['00:00:00 9000', yres.url]
            
def loadptt():
    conn = psycopg2.connect(host='postgres',
                            user='postgres',
                            password='postgresadminpassword:D',
                            database='web_crawler')
    cur = conn.cursor()
    
    cur.execute("drop table if exists ptt")
    cur.execute('''
                create table ptt (
                                    post_ts timestamp,
                                    author varchar(20),
                                    title varchar(40),
                                    board varchar(20),
                                    url varchar(60)
                                    );
                                    ''')
    cur.execute('''create index on ptt (post_ts)''')
    cur.execute('''create index on ptt (title)''')
    cur.execute('''create index on ptt (url)''')
    
    indexNum=1
    #while indexNum <= 50:
    while True:
        global url, res, soup
        board = 'Yunlin'
        url = 'https://www.ptt.cc/bbs/' + board + '/index' + str(indexNum) + '.html'
        res = requests.get(url, verify=False)
        soup = BeautifulSoup(res.text,"lxml")
        
        if ifExist(res.status_code):
            
            print(res.url)
            
            for i in range(0,len(soup.select('.title'))):
                print('Importing Record No.' + str(i+1) + ' ...', 'Done!')
                cur.execute('''
                            insert into ptt values(
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                            )
                            ''',
                            (
                            # timestamp
                            datetime.strptime(crawlData(i)[0] + ' ' + crawlData(i)[1].replace('：',':'), '%Y/%m/%d %H:%M:%S'),
                            # author
                            crawlData(i)[2],
                            # title
                            crawlData(i)[3],
                            # board name
                            board,
                            # url
                            crawlData(i)[4]
                            )
                )
                conn.commit()
                i += 1
                      
            indexNum+=1
            
        else:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            print(res.url,'並不存在!')
            break
    conn.close()
loadptt()
