# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:45:33 2022

@author: fuwen
"""
import requests,base64,download,json
import PySimpleGUI as sg,time

import os
import sys
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')

def GetLoginMessage():
    login = [
        [sg.Text('账号：'),sg.Input(key = '-username-')],
        [sg.Text('密码：'),sg.Input(key = '-password-')],
        [sg.Button('登录',key = 'yes'),sg.Button('取消',key = 'Cancel')]
        ]
    
    window = sg.Window('懒人听书登录', login)
    event, values = window.Read()
    if event in (None, 'Cancel'):
        window.Close()
    username = values['-username-']
    password = values['-password-']
    event, values = window.Read()
    window.Close()
    return event,username,password

def Login(account,password):
    global conn
    LoginUrl = 'https://m.lrts.me/ajax/logon'
    conn = requests.session()
    PostData = {"account":account,"pwd":base64.b64encode(bytes(password,'ascii'))}
    rep = conn.post(LoginUrl, data=PostData,headers=headers)
    if rep.json()['phone']:
        print('登录成功！帐号为：%s，可下载免费部分及已订购部分！'%rep.json()['phone'])
        s = '已登录 '
        phone = rep.json()['phone']
    else:
        print('登陆失败！仅下载免费部分。')
        s = '未登录'
        phone = ''
    return s,phone

def ChangeFileName(filename):
    filename = filename.strip()
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('”','')
    filename = filename.replace('<','')
    filename = filename.replace('-','')
    filename = filename.replace('.mp3','')
    filename = filename.replace('.m4a','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    filename = filename.replace('（','(')
    filename = filename.replace(chr(65279),'') # UTF-8+BOM
    filename = filename.split('(')[0]
    return filename

#调用Python下载
def PythonDownLoad(DownloadUrl,Filename):
    with open(outfloder+'/'+Filename,'wb') as f :
        r = requests.get(DownloadUrl, stream=True)
        f.write(r.content)

#通过BookID获得BookJson列表
def GetBookJsonList(BookID):
    AudioListJsonUrl = 'http://m.lrts.me/ajax/getBookMenu?bookId=%s&pageNum=1&pageSize=5000&sortType=0'%(BookID)
    AudioListJsonRep = conn.get(AudioListJsonUrl,headers=headers)
    AudioList = AudioListJsonRep.json()['list']
    return AudioList

#通过BookJson提取文件名、下载链接
def GetBookDownInfo(AudioJson,BookID):
    AudioName = AudioJson['name']
    AudioName = ChangeFileName(AudioName)
    AudioSection = AudioJson['section']
    AudioJsonUrl = 'http://m.lrts.me/ajax/getPlayPath?entityId=%s&entityType=3&opType=1&sections=[%s]&type=0'%(BookID,AudioSection)
    Audiorep = conn.get(AudioJsonUrl,headers=headers)
    if Audiorep.json()['msg']!=None:
        pass
    FileUrl = Audiorep.json()['list'][0]['path']
    Fileformat = FileUrl.split('.')[-1]
    Fileformat = Fileformat.split('?')[0]
    FileName = AudioName+'.'+Fileformat
    return FileName,FileUrl

#通过AlbumId获得播放列表
def GetAlbumJsonList(AlbumID):
    AlbumListJsonUrl = 'https://m.lrts.me/ajax/getAlbumAudios?ablumnId=%s&sortType=0'%AlbumID
    AlbumListJsonRep = conn.get(AlbumListJsonUrl,headers=headers)
    AlbumList = AlbumListJsonRep.json()['list']
    return AlbumList

#通过AlbumJson提取文件名、下载链接
def GetAlbumDownInfo(AlbumJson,AlbumID):
    global Audiorep
    AudioName = AlbumJson['name']
    AudioName = ChangeFileName(AudioName)
    AudioSection = AlbumJson['section']
    AudioJsonUrl = 'https://m.lrts.me/ajax/getPlayPath?entityId=%s&entityType=2&opType=1&sections=[%s]&type=0'%(AlbumID,AudioSection)
    Audiorep = conn.get(AudioJsonUrl,headers=headers)
    if Audiorep.json()['msg']!=None:
        pass
    FileUrl = Audiorep.json()['list'][0]['path']
    FileName = AudioName+'.mp3'
    return FileName,FileUrl

# 调用Air2下载
def Air2DownLoad(JsonRpcUrl,DownloadUrl,Mp3Name):
    PostData = {
        "jsonrpc":"2.0",
        "method":"aria2.addUri",
        "id":1,
        "params":[[DownloadUrl],
                  {"out":Mp3Name,
                   "dir":outfloder,
                   "split":"32",
                   "max-connection-per-server":"5",
                   "seed-ratio":"0.1"}]}
    Send = requests.post(JsonRpcUrl,json.dumps(PostData))
    if Send.status_code==200:
        print('%s 推送成功！'%Mp3Name)
    else:
        print('推送失败！请打开Aria2并确保正常运行。')


headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn;  MI2 Build/JRO03L) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 XiaoMi/MiuiBrowser/1.0'}
loginEvent,username,password = GetLoginMessage()
s,phone = Login(username,password)

sg.theme('GreenTan')
frame1 = [sg.Radio('Book', "RADIO1", default=True, key = '-book-',size=(10, 1)),sg.Radio('Album', "RADIO1",key = '-album-',  size=(10, 1))],
frame2 = [[sg.Radio('内置下载器', "RADIO2", key = '-python-',size=(10, 1)),sg.Radio('Aria2', "RADIO2",key = '-aria2-',  size=(10, 1) ,default=True)],[sg.Text('RPC：'),sg.Input('http://localhost:16800/jsonrpc',key = '-RPC-',size=(25,1))]]
frame3 = [sg.Text('Book&Album ID：'),sg.Input('33857',key = '-bookid-',size=(8, 1)),sg.Text('开始集数：'),sg.Input('1',key = '-start-',size=(5, 1)),sg.Text('结束集数：'),sg.Input('10',key = '-end-',size=(5, 1))],

layout = [
    [sg.Text('登录状态:%s'%s+phone)],
    [sg.Column([[sg.Frame('书籍类型:', frame1,size=(200,80))]]),sg.Column([[sg.Frame('下载工具:', frame2,size=(250,80))]])],
    [sg.Column([[sg.Frame('下载选项:', frame3,size=(470,50))]])],
    [sg.Text('下载至目录：'),sg.Input(),sg.FolderBrowse('浏览',key = '-outfloder-')],
    [sg.Button('确认',key = 'ok')],
    [sg.Text('输出日志：')],
    [sg.Output(size=(70, 6))],
    ]
window = sg.Window('懒人听书下载工具 v1.1', layout)

count=0
while True:
    count+=1
    if loginEvent == None:
        break
    if count ==1:    
        sg.popup_timed(s)
    event, values = window.Read()
    print('正在启动程序……')
    if event in (None, 'Cancel'):
        break
    start = int(values['-start-'])
    end = int(values['-end-'])
    bookid = values['-bookid-']
    outfloder = values['-outfloder-']
    JsonRpcUrl = values['-RPC-']
    Aria2Choose = values['-aria2-']
    b = values['-book-']
    if b==True:
        AudioJsonList = GetBookJsonList(bookid)
        AudioJsonList=AudioJsonList[start-1:end]
        for AudioJson in AudioJsonList:
            time.sleep(5)
            try:
                FileName,FileUrl = GetBookDownInfo(AudioJson,bookid)
            except :
                path = AudioJson['path']
                payType = AudioJson['payType']
                name = AudioJson['name']
                if path == None and payType ==2:
                    print('%s 未购买'%name)
                continue
            if outfloder == '':
                title= FileName
            else:
                title= outfloder+'/'+FileName    
            if Aria2Choose == True:
                Air2DownLoad(JsonRpcUrl,FileUrl,FileName)
            else:
                fr = download.FastRequests(infos=[{'title':title,'link':FileUrl}])
                fr.run()
    else:
        AudioJsonList = GetAlbumJsonList(bookid)
        AudioJsonList=AudioJsonList[start-1:end]
        for AudioJson in AudioJsonList:
            time.sleep(5)
            try:
                FileName,FileUrl = GetBookDownInfo(AudioJson,bookid)
            except :
                path = AudioJson['path']
                payType = AudioJson['payType']
                name = AudioJson['name']
                if path == None and payType ==2:
                    print('%s 未购买'%name)
                continue
            if outfloder == '':
                title= FileName
            else:
                title= outfloder+'/'+FileName
            if Aria2Choose == True:
                Air2DownLoad(JsonRpcUrl,FileUrl,FileName)
            else:
                fr = download.FastRequests(infos=[{'title':outfloder+'/'+FileName,'link':FileUrl}])
                fr.run()
window.Close()
