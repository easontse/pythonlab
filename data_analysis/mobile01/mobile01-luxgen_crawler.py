#!/usr/bin/env python3

import requests, time, csv, os, sys, logging
from bs4 import BeautifulSoup

def httpGet(url):
    time.sleep(2.2)
    logger.info('HTTP GET: ' + url)
    return requests.get(url)

def get_linklist(url):
    logger.info('Generating Linklist on: ' + url)
    
    soup = BeautifulSoup(httpGet(url).text,'lxml')    
    
    linklist = []
    
    for i in soup.findAll('span', {"class":"otherpages"}):
        raw_url = i.contents[-1]['href']
        len_without_pageNum = int(27 + len(raw_url[raw_url.find('&t=')+3:raw_url.find('&p=')]))
        tgt_url = raw_url[:len_without_pageNum-3]
        if tgt_url not in linklist:
            linklist.append(tgt_url)

        tgt_url = raw_url[:len_without_pageNum]
        pageNum = int(raw_url[-(len(raw_url)-len_without_pageNum):])
        while pageNum > 1:
            tgt_url_with_pgNum = tgt_url + str(pageNum)
            if tgt_url_with_pgNum not in linklist:
                linklist.append(tgt_url_with_pgNum)
            pageNum -= 1

    for i in soup.select('.subject'):
        if '主題' not in i and i not in linklist:
            linklist.append(i.a['href'])
    
    logger.info('Links in the list: ' + str(len(linklist)))
    return linklist

def crawl_content(url):
    logger.info('Crawling Content on: ' + url)
    res = httpGet(url)
    
    if url != res.url:
        logger.warning('Requested URL does not match Response URL, return None!')
        return []
    
    soup = BeautifulSoup(res.text,'lxml')
    
    date = []
    for i in soup.find_all('div', {'class':'date'}):
        date.append(i.text[:-4].strip())

    author = []
    for i in soup.find_all('div', {'class':'fn'}):
        author.append(i.text.strip())

    p_content = []
    inchar = '\n\r'
    ourchar = '  '
    transchar = str.maketrans(inchar, ourchar)
    for i in soup.find_all('div', {'class':'single-post-content'}):
        p_content.append(i.text.translate(transchar).strip())
    
    dataset = []
    for a,b,c in zip(date, author, p_content):
        dataset.append([a, b, soup.select('.topic')[0].text, c, url])
    
    return dataset

#--------------------------------------------------------------------------------

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(filename='mobile01-luxgen.log',level=logging.INFO,format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))
 
pageNum = 66
while True:

    url = 'http://www.mobile01.com/topiclist.php?f=444&p=' + str(pageNum)
    logger.info('Start Crawling on: ' + url + '\n')
    
    if url != httpGet(url).url:
        logger.error('Requested URL does not match Response URL, QUIT!')
        break
    
    for i in get_linklist(url):
        with open('mobile01-luxgen.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            for x in crawl_content('http://www.mobile01.com/'+i):
                if len(x) > 0:
                    writer.writerow([x[0],x[1],x[2],x[3],x[4]])
                else:
                    logger.warning('None received, skipped!')
                    
    logger.info('Finished: ' + url + '\n')
    pageNum += 1
