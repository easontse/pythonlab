import requests, time, csv
from bs4 import BeautifulSoup

def get_index_url(pageNum):
    return 'http://www.mobile01.com/forumtopic.php?c=21&p=' + str(pageNum)

def get_res(url):
    time.sleep(2)
    res = requests.get(url)
    print('Received: ' + res.url)
    return res

def gen_linklist(pageNum):
    print('Crawling links from index page: ' + get_index_url(pageNum))
    linklist = []
    soup = BeautifulSoup(get_res(get_index_url(pageNum)).text)
    
    for i in soup.select('.subject'):
        if 'subject-text' in str(i):
            linklist.append('http://www.mobile01.com/' + i.a['href'])
    return list(set(linklist))

def crawl_thread_1(soup, thread_url):
    print('Crawling thread: ' + thread_url)
    thread_data = []
    for i in soup.select('.single-post'):
        thread_data.append([
              # date
              i.find_all('div', {'class':'date'})[0].text[:-4].strip(),
              # author
              i.select('.inner')[0].select('.fn')[0].text.strip(),
              # title
              soup.select('.topic')[0].text.strip(),
              # content
              i.find_all('div', {'class':'single-post-content'})[0].text.strip(),
              # url
              thread_url
        ])
    print('thread_data appended: ' + thread_url)
    return thread_data

def get_reply_linklist(soup):
    print('Generating link list of replies...')
    maxPage = int(soup.select('.numbers')[0].text[6:6+len(soup.select('.numbers')[0].text.strip())-14])
    print('Max Page: ' + str(maxPage))
    
    reply_linklist = []
    if maxPage == 1:
        return reply_linklist
        
    while maxPage > 1:
        url = str(link) + '&p='  + str(maxPage)
        if url not in reply_linklist:
            reply_linklist.append(url)
        maxPage -= 1
        
    print('Link list generated successfully. Length: ' + str(len(list(set(reply_linklist)))))
    return sorted(list(set(reply_linklist)))

def crawl_reply(soup):
    reply_linklist = get_reply_linklist(soup)
    
    if len(reply_linklist) < 1:
        return None
    
    reply_data = []
    
    for link in reply_linklist:
        print('Crawling reply: ' + link)
        reply_res = get_res(link)
        reply_soup = BeautifulSoup(reply_res.text)
        
        for replylink in list(set(reply_soup.select('.single-post'))):
            reply_data.append([
                # date
                replylink.find_all('div', {'class':'date'})[0].text[:-4].strip(),
                # author
                replylink.select('.inner')[0].select('.fn')[0].text.strip(),
                # title
                reply_soup.select('.topic')[0].text.strip(),
                # content
                replylink.find_all('div', {'class':'single-post-content'})[0].text.strip(),
                # url
                reply_res.url
                ])

    print('reply_data length: ' + str(len(reply_data)))
    return reply_data

#---------------------------------------------------------------------------------------------------------------------

counter = 1
while counter <= 20:
    for link in gen_linklist(counter):

        soup = BeautifulSoup(get_res(link).text)

        dataset = crawl_thread_1(soup, link)
        print('Before extend: ' + str(len(dataset)))

        if crawl_reply(soup) != None:
            reply_dataset = crawl_reply(soup)
            print('Reply dataset received successfully!')
            dataset.extend(reply_dataset)
            print('After extend: ' + str(len(dataset)))
            print('Processed: ' + link + '\n')
        else:
            print('There is only one page of thread.')
            print('Processed: ' + link + '\n')

    print('Length of dataset:' + str(len(dataset)))
    
    with open('mobile01.csv', 'a', encoding='utf-8') as csvfile:
        for data in dataset:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([data[0],data[1],data[2],data[3],data[4]])
    
    counter += 1