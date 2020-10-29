# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:45:30 2020

@author: fuwen
"""
from subprocess import call
import os,requests, base64, json, time

AlbumId = 87982
#帐号信息
account = 'info@fuwenyue.com'
password = '&QaQKgHW6V4&Juo'
#文件下载路径
FilePath = r'D:\有声小说'
#IDM路径
IdmPath = 'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
#登陆帐号
LoginUrl = 'https://m.lrts.me/ajax/logon'
conn = requests.session()
PostData = {"account":account,"pwd":base64.b64encode(bytes(password,'ascii'))}
rep = conn.post(LoginUrl, data=PostData)
repJson = json.loads(rep.text)
msg = repJson['msg']
if msg =='账号或密码错误':
    print('帐号或密码错误，仅下载免费部分')
else:
    print('登录成功，下载该帐号免费部分及购买部分')
#使用IDM下载
def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n','a'])
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

# 文件名格式化
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
    filename = filename.replace(' ','(')
    filename = filename.replace(chr(65279),'') # UTF-8+BOM
    #filename = filename.split('(')[0]
    return filename
AlreadyDown = [FileName.replace('.mp3','',1) for FileName in os.listdir(FilePath)]
AlbumUrl = 'https://m.lrts.me/ajax/getAlbumAudios?ablumnId=%d&sortType=0'%AlbumId
AlbumJson = conn.get(AlbumUrl)
AlbumJson = AlbumJson.json()
AudioList = AlbumJson['list']
for SingalDict in AudioList:
    AudioName = SingalDict['name']
    AudioName = ChangeFileName(AudioName)
    print('正在尝试下载 %s ……'%AudioName)
    if AudioName in AlreadyDown:
        print('目录已有该文件，跳过下载。')
        continue
    SectionID = SingalDict['section']
    SingalAudioUrl = 'https://m.lrts.me/ajax/getPlayPath?entityId=%d&entityType=2&opType=1&sections=[%d]&type=0'%(AlbumId,SectionID)
    SingalAudioJson = conn.get(SingalAudioUrl,headers = headers)
    SingalAudioJson = SingalAudioJson.json()
    AudioDownUrl = SingalAudioJson['list'][0]['path']
    IdmDownLoad(AudioDownUrl,AudioName+'.mp3')
    time.sleep(30)
    
