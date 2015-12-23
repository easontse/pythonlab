import requests
import datetime
import time
from bs4 import BeautifulSoup

def get_indexPage(board, indexNum):
    retry_counter = 1
    while retry_counter <= 3:
        index_url = 'https://www.ptt.cc/bbs/' + board + '/index' + str(indexNum) + '.html'
        try:
            return requests.get(index_url, verify=False)
        except KeyboardInterrupt:
            print('Interupted by operator.')
            break
        except:
            print('Retry after 2 sec ...')
            time.sleep(2)
            return requests.get(index_url, verify=False)
        retry_counter += 1
    return '1'

def crawl_data(record):
    try:
        return (record.select('.author')[0].text.strip() + '``' +
                record.select('a')[0].text.strip() + '``' +
                'https://www.ptt.cc' + record.select('a')[0]['href'])
    except IndexError:
        return (record.select('.title')[0].text.strip() + '``'
                + 'None')

def crawl_timestamp(record):
    ts_url = 'https://www.ptt.cc' + record.select('a')[0]['href']
    try:
        ts_res = requests.get(ts_url, verify=False)
    except IndexError:
        print('Retry after 2 sec ...')
        time.sleep(2)
        ts_res = requests.get(ts_url, verify=False)
    ts_soup = BeautifulSoup(ts_res.text, 'lxml')
    return ts_soup.select('.article-meta-value')[3].text[4:].replace('：',':').strip()



indexNum = 1
while indexNum <= 1:
#while True:
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
        print((crawl_timestamp(record) +'``'+
               crawl_data(record) + '``' +
               board + '``' +
               str(indexNum)
              ).split('``'))

    indexNum += 1

print('Nothing More...')

#datetime.strptime(crawl_timestamp(record), '%b %d %H:%M:%S %Y')
