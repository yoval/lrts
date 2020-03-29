# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 21:07:11 2018
@author: fuwen
"""
from subprocess import call
import requests, base64, json, time, os, re

BookID = 40689

account = 'info@fuwenyue.com'
password = '&QaQKgHW6V4&Juod'

FilePath = r'C:\Users\Administrator\Desktop\有声小说'
#使用IDM下载
IdmPath = 'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n'])
    
def ChangeFileName(filename):
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('”','')
    filename = filename.replace('<','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    filename = filename.replace('（','(')
    filename = filename.replace(chr(65279),'') # UTF-8+BOM
#    print(ord(filename[0]))
    filename = filename.split('(')[0]
    return filename

Mp3ListJsonUrl = 'http://m.lrts.me/ajax/getBookMenu?bookId=%d&pageNum=1&pageSize=5000&sortType=0'%(BookID)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
ba_password = base64.b64encode(bytes(password,'ascii'))
LoginUrl = 'https://m.lrts.me/ajax/logon'
conn = requests.session()
PostData = {"account":account,"pwd":ba_password}
rep = conn.post(LoginUrl, data=PostData)
repJson = json.loads(rep.text)
msg = repJson['msg']
if msg =='账号或密码错误':
    print('帐号或密码错误，仅下载免费部分')
else:
    print('登录成功，下载该帐号免费部分及购买部分')
Mp3ListJson = conn.get(Mp3ListJsonUrl, headers = headers)
Mp3ListJson = json.loads(Mp3ListJson.text)
Mp3List = Mp3ListJson['list']
Mp3NameList = [Mp3dict['name'] for Mp3dict in Mp3List]
Mp3NameList = [ChangeFileName(i) for i in Mp3NameList]

AlreadyDown = [FileName.replace('.mp3','') for FileName in os.listdir(FilePath)]
Count = 0
for Mp3Name in Mp3NameList :
    Count+=1
    if Mp3Name in AlreadyDown :
        continue
    Mp3JsonUrl = 'http://m.lrts.me/ajax/getPlayPath?entityId=%d&entityType=3&opType=1&sections=[%d]&type=0'%(BookID,Count)
    Mp3Url = conn.get(Mp3JsonUrl, headers = headers)
    try :
        Mp3Url = json.loads(Mp3Url.text)['list'][0]['path']
        print('正在下载%s……'%Mp3Name)
        IdmDownLoad(Mp3Url,Mp3Name+'.mp3')
        time.sleep(2)
    except :
        print('%s，未购买，跳过……'%Mp3Name)
