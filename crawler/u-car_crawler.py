import requests, datetime, time, csv
from bs4 import BeautifulSoup

def get_soup(pageNum):
    url = 'http://forum.u-car.com.tw/index.asp?page=' + str(pageNum) + '&category=19'
    index_res = requests.get(url)
    return BeautifulSoup(index_res.text)

def get_linklist(soup):
    link_list = []
    for i in soup.select('a'):

        if 'thread.asp' in i['href']:
            link_list.append('http://forum.u-car.com.tw/' + i['href'])

        counter = 0
        while counter < len(link_list):
            if len(link_list[counter]) == 51:
                link_list[counter] += '&page=1'
            counter += 1
            
    for i in set(link_list):
        if len(i) == 59:
            a = int(i[-2:])

            while a > 4:
                url = i[:57] + str(a)
                if url not in link_list:
                    link_list.append(url)
                a -= 1

        elif len(i) == 60:
            a = int(i[-3:])

            while a > 4:
                url = i[:57] + str(a)
                if url not in link_list:
                    link_list.append(url)
                a -= 1

        elif len(i) == 58 and int(i[-1]) > 4:
            a = int(i[-1:])

            while a > 4:
                url = i[:57] + str(a)
                if url not in link_list:
                    link_list.append(url)
                a -= 1

    return list(set(link_list))

def crawl_thread(link):
    thread_res = requests.get(link)
    thread_res.encoding = 'utf-8'
    thread_soup = BeautifulSoup(thread_res.text)
    
    
    thread_data = []
    for i in thread_soup.find_all("div", { "class" : "fd_cont" }):
        thread_data.append([
            # date
            i.find_all("div", {"class":"memberinfo_top_l"})[0].text[:19].strip(),
            # author
            i.find_all("li", {'class':'member_id'})[0].select('a')[0].string.strip(),
            # title
            t1_soup.find_all("div", { "class" : "forumhead" })[0].text.strip(),
            # content
            i.find_all('div', {'class':'userwrite'})[0].text.strip()
        ])
    return thread_data

pageNum = 1
while True:
    try:
        for link in sorted(get_linklist(get_soup(pageNum))):
            with open('u-car.csv', 'a', encoding='utf-8') as csvfile:
                for data in crawl_thread(link):
                    print(data[0],data[1],data[2],link)
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([data[0],data[1],data[2],data[3],link])
        pageNum += 1
    except:
        RetryCounter = 1
        while RetryCounter <= 3:
            print('retry after 2 sec...')
            time.sleep(2)
        break