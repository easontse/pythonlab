import requests, datetime, time, csv
from bs4 import BeautifulSoup

def get_soup(indexNum):
    index_url = 'http://club.autohome.com.cn/bbs/allforums-dateline-9-' +str(indexNum)+ '.html'
    index_res = requests.get(index_url)
    index_res.encoding = 'gbk'
    return BeautifulSoup(index_res.text)

def get_linklist(soup):
    print('generating link list...')
    linklist = []
    for link in soup.select('.list_dl'):
        if 'href' in str(link.select('a')[0]):
            linklist.append('http://club.autohome.com.cn' + link.select('a')[0]['href'])
    print('list generated!')
    print(len(list(set(linklist))))
    return sorted(list(set(linklist)))

def crawl_thread(thread_url):
    
    thread_res = requests.get(thread_url)
    thread_res.encoding = 'gbk'
    thread_soup = BeautifulSoup(thread_res.text)
    
    print('crawling data... ' + thread_res.url)
    
    thread_data = []
    for i in thread_soup.find_all('div', {'class':'clearfix'}):
        try:
            thread_data.append([
                  # timestamp
                  i['data-time'].strip(),
                  # author
                  i.a.string.strip(),
                  # title
                  thread_soup.select('.maxtitle')[0].text.strip(),
                  # content
                  i.find_all('div', {'class':'w740'})[0].text.strip(),
                  #url
                  thread_res.url
            ])
            
        except:
            continue
    print(len(thread_data))
    
    if len(thread_soup.select('.fs')[1].text) == 6:
        maxPage = int(thread_soup.select('.fs')[1].text[-3])
    elif len(thread_soup.select('.fs')[1].text) == 7:
        maxPage = int(thread_soup.select('.fs')[1].text[-4:-2])
    elif len(thread_soup.select('.fs')[1].text) == 8:
        maxPage = int(thread_soup.select('.fs')[1].text[-5:-2])
    
    sub_linklist = []
    while maxPage > 1:
        url = str(thread_url[:-6]) + str(maxPage) + '.html'
        if url not in sub_linklist:
            sub_linklist.append(url)
        maxPage -= 1
    
    
    for i in sub_linklist:
        
        sthread_res = requests.get(i)
        sthread_res.encoding = 'gbk'
        sthread_soup = BeautifulSoup(sthread_res.text)
        
        print('crawling thread: ' + sthread_res.url)
        
        
        for x in sthread_soup.find_all('div', {'class':'clearfix'}):
            try:
                thread_data.append([
                      # timestamp
                      x['data-time'].strip(),
                      # author
                      x.a.string.strip(),
                      # title
                      thread_soup.select('.maxtitle')[0].text.strip(),
                      # content
                      x.find_all('div', {'class':'w740'})[0].text.strip(),
                      #url
                      sthread_res.url
                ])
            except:
                continue
    
    return sorted(thread_data)
    
pageNum = 1    
while True:
    try:
        with open('autohome.csv', 'a', encoding='utf-8') as csvfile:
            datalinklist = get_linklist(get_soup(pageNum))
            counter = 0
            while counter < len(datalinklist):
                for data in crawl_thread(datalinklist[counter]):
                    
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([data[0],data[1],data[2],data[3],data[4]])
                    #print(data[0],data[1],data[2],data[3],i)
                    counter += 1
                    
        pageNum += 1
    except:
        RetryCounter = 1
        while RetryCounter <= 3:
            print('retry after 2 sec...')
            time.sleep(2)
            RetryCounter += 1
        break