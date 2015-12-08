import requests, datetime, time, re
import pandas as pd
from bs4 import BeautifulSoup

t1_url = 'http://forum.u-car.com.tw/thread.asp?forumid=285933&page=1'
t1_res = requests.get(t1_url)
t1_soup = BeautifulSoup(t1_res.text)

for i in t1_soup.find_all("div", { "class" : "fd_cont" }):
    print(
        # date
        i.find_all("div", {"class":"memberinfo_top_l"})[0].text[:19],
        # author
        i.find_all("li", {'class':'member_id'})[0].select('a')[0].string,
        # content
        i.find_all('div', {'class':'userwrite'})[0].text
    )