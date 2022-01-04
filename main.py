# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 23:54:24 2022
@author: Mypc
"""
import requests,base64,time,json
#---开始配置---
#页面链接
pageurl = 'https://www.lrts.me/book/41660813'
#帐号信息
account = 'info@fuwenyue.com'
password = '&QaQKgHW6V4&Juo'
#下载方式：(1.调用自定义Aira2,2.调用默认Aria2,3.直接使用Python下载)
DownType = 3
#下载范围（End为0时，范围不限）
#开始集数
Start=310
#结束集数
End=0
#---结束配置---
#pageurl = input('请粘贴页面链接：')
#account = input('请粘贴懒人听书账号:')
#password = input('请粘贴懒人听书密码：')
headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn;  MI2 Build/JRO03L) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 XiaoMi/MiuiBrowser/1.0'}
def Login(account,password):
    print('*'*12)
    global conn
    LoginUrl = 'https://m.lrts.me/ajax/logon'
    conn = requests.session()
    PostData = {"account":account,"pwd":base64.b64encode(bytes(password,'ascii'))}
    rep = conn.post(LoginUrl, data=PostData,headers=headers)
    if rep.json()['phone']:
        print('登录成功！帐号为：%s，可下载免费部分及已订购部分！'%rep.json()['phone'])
    else:
        print('登陆失败！仅下载免费部分。')
    print('*'*12)
#更改文件名便于保存
def ChangeFileName(filename):
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
#调用远程Aria2下载
def QdownLoad(DownloadUrl,Filename):
    JsonRpcUrl = 'http://localhost:2800/jsonrpc'
    Token = 'werqrqrasfatertg'
    PostData = {
    "jsonrpc": "2.0",
    "method": "aria2.addUri",
    "id": "1",
    "params": [
        "token:%s"%Token,
        [DownloadUrl],
        {"out":Filename,
         "split":"32",
         "max-connection-per-server":"5",
         "seed-ratio":"0.1"}
    ]
}
    Send = requests.post(JsonRpcUrl,json.dumps(PostData))
    if Send.status_code==200:
        print('推送成功！')
    else:
        print('推送失败！请打开Aria2并确保正常运行。')
#调用Aria2下载
def Air2DownLoad(DownloadUrl,Filename):
    JsonRpcUrl = 'http://localhost:6800/jsonrpc'
    PostData = {
        "jsonrpc":"2.0",
        "method":"aria2.addUri",
        "id":1,
        "params":[[DownloadUrl],
                  {"out":Filename,
                   "split":"32",
                   "max-connection-per-server":"5",
                   "seed-ratio":"0.1"}]}
    Send = requests.post(JsonRpcUrl,json.dumps(PostData))
    if Send.status_code==200:
        print('推送成功！')
    else:
        print('推送失败！请打开Aria2并确保正常运行。')
#调用Python下载
def PythonDownLoad(DownloadUrl,Filename):
    with open(Filename,'wb') as f :
        print('正在下载:%s'%Filename)
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
    print('---')
    print(AudioName)
    AudioSection = AudioJson['section']
    AudioJsonUrl = 'http://m.lrts.me/ajax/getPlayPath?entityId=%s&entityType=3&opType=1&sections=[%s]&type=0'%(BookID,AudioSection)
    Audiorep = conn.get(AudioJsonUrl,headers=headers)
    if Audiorep.json()['msg']!=None:
        print(Audiorep.json()['msg'])
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
        print(Audiorep.json()['msg'])
    FileUrl = Audiorep.json()['list'][0]['path']
    FileName = AudioName+'.mp3'
    return FileName,FileUrl

if __name__=='__main__':
    Login(account,password)
    if 'book' in pageurl:
        BookID = pageurl.split('/')[-1]
        AudioJsonList = GetBookJsonList(BookID)
        if End==0:
            pass
        else:
            AudioJsonList=AudioJsonList[Start-1:End]
            print('下载范围：%s集~%s集'%(Start,End))
        for AudioJson in AudioJsonList:
            try:
                FileName,FileUrl = GetBookDownInfo(AudioJson,BookID)
                print('抓取成功！')
            except:
                continue
            if DownType==1:
                QdownLoad(FileUrl, FileName)
            elif DownType==2:
                Air2DownLoad(FileUrl,FileName)
            elif DownType ==3:
                PythonDownLoad(FileUrl,FileName)
            else:
                print('下载工具配置错误！')
            time.sleep(5)
    elif 'album' in pageurl:
        AlbumID = pageurl.split('/')[-1]
        AudioJsonList = GetAlbumJsonList(AlbumID)
        if End==0:
            pass
        else:
            AudioJsonList=AudioJsonList[Start-1:End]
            print('下载范围：%s集~%s集'%(Start,End))
        for AudioJson in AudioJsonList:
            try:
                FileName,FileUrl = GetBookDownInfo(AudioJson,BookID)
            except:
                continue
            if DownType==1:
                QdownLoad(FileUrl, FileName)
            elif DownType==2:
                Air2DownLoad(FileUrl,FileName)
            elif DownType ==3:
                PythonDownLoad(FileUrl,FileName)
            else:
                print('下载工具配置错误！')
            time.sleep(5)        
    else :
        print('暂不支持此类型')