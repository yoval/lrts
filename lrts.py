# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 10:49:36 2018

@author: fuwen
"""
import requests
import re
import time
import json
from bs4 import BeautifulSoup
import os


BookID = 6953  #BookID
Lenth = 1262  #章节数量

def Get_Co_ID(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'lxml')
    columns = soup.find_all('li',class_ = 'clearfix')
    for column in columns:
        title = column.get_text()
        title = title.split()[1]
        sectionid = re.findall('section(\d+)',str(column))[1]
        Mp3_url = 'http://www.lrts.me/ajax/path/4/%s/%s' %(BookID,sectionid)   
        html_doc = requests.get(Mp3_url).text
        data = json.loads(html_doc)['data']
        with open('videos/lrts.txt','a',encoding='utf-8') as f:
            f.writelines([data,',',title,'\n'])

def rename():
    urls = open('videos/lrts.txt','r+',encoding='UTF-8')
    urls = urls.readlines()
    for url in urls :
        url = url.split(',')
        name_1 = url[1]
        name_1 = name_1.strip()
        Url = url[0]
        name_2 = Url.split('/')
        name_2 = name_2[len(name_2) - 1]
        with open('videos/rename.bat','a',encoding='UTF-8') as videos:
            videos.writelines(['REN "',name_2,'" "',name_1,'.mp3\n'])
        with open('videos/url.txt','a',encoding='UTF-8') as url_txt:
            url_txt.writelines([Url,'\n'])


if not os.path.exists('videos'):
    os.mkdir('videos')
with open('videos/rename.bat','a',encoding='UTF-8') as videos:
    videos.writelines(['CHCP 65001','\n\n'])
for lenth in range(1,Lenth,10) :
    url = 'http://www.lrts.me/ajax/playlist/2/%d/%d/next' %(BookID,lenth)
    Get_Co_ID(url)
    time.sleep(1)
rename()