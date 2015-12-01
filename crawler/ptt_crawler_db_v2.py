import requests, psycopg2, time
from bs4 import BeautifulSoup
from datetime import datetime

def get_indexPage(board, indexNum):
    retry_counter = 1
    while retry_counter <= 3:
        index_url = 'https://www.ptt.cc/bbs/' + board + '/index' + str(indexNum) + '.html'
        try:
            return requests.get(index_url, verify=False)
        except KeyboardInterrupt:
            print('使用者中斷!')
            break
        except:
            print('連線失敗, 2秒後重試 ...')
            time.sleep(2)
            return requests.get(index_url, verify=False)
        retry_counter += 1
    return '1'

def crawl_data(record):
    try:
        return (record.select('.author')[0].text.strip() + '``' +
                record.select('a')[0].text.strip() + '``' + 
                'https://www.ptt.cc' + record.select('a')[0]['href'])
    except:
        return (record.select('.title')[0].text.strip() + '``' 
                + 'None')

def crawl_timestamp(record):
    ts_url = 'https://www.ptt.cc' + record.select('a')[0]['href']
    while True:
        try:
            ts_res = requests.get(ts_url, verify=False)
            break
        except KeyboardInterrupt:
            print('使用者中斷!')
            break
        except:
            print('時間資料載入失敗, 2秒後重試 ...')
            time.sleep(2)
            ts_res = requests.get(ts_url, verify=False)
    ts_soup = BeautifulSoup(ts_res.text, 'lxml')
    return ts_soup.select('.article-meta-value')[3].text[4:].replace('：',':').strip()

#==============================================================================================

conn = psycopg2.connect(host='postgres',
                        user='postgres',
                        password='postgresadminpassword:D',
                        database='web_crawler')
cur = conn.cursor()

cur.execute("drop table if exists ptt2")
cur.execute('''
            create table ptt2 (
                                post_ts  timestamp,
                                author   varchar(20),
                                title    varchar(50),
                                url      varchar(60),
                                board    varchar(20),
                                indexNum varchar(5)
                                );
            ''')
cur.execute('''create index on ptt (post_ts)''')
cur.execute('''create index on ptt (title)''')
cur.execute('''create index on ptt (url)''')

#===================================================================================================

indexNum = 1
#while indexNum <= 1:
while True:
    try:
        board = 'Yunlin'
        soup = BeautifulSoup(get_indexPage(board, indexNum).text, 'lxml')
    except:
        continue

    for record in soup.select('.r-ent'):
        try:
            crawl_timestamp(record)
        except:
            continue
        
        dataset = (crawl_timestamp(record) +'``'+ 
                   crawl_data(record) + '``' +
                   board + '``' +
                   str(indexNum)
                  ).split('``')
        
        cur.execute('''
                    insert into ptt2 values(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                    )
                    ''',
                    (
                    # timestamp
                    datetime.strptime(dataset[0], '%b %d %H:%M:%S %Y'),
                    # author
                    dataset[1],
                    # title
                    dataset[2],
                    # url
                    dataset[3],
                    # board
                    dataset[4],
                    # indexNum
                    dataset[5]
                    )
        )    
        conn.commit()
    print('已匯入 ' + 'https://www.ptt.cc/bbs/' + board + '/index' + str(indexNum) + '.html')
    indexNum += 1
conn.close()   
print('Nothing More...')
    
#datetime.strptime(crawl_timestamp(record), '%b %d %H:%M:%S %Y')