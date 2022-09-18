# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:45:33 2022

@author: fuwen
"""
import requests,base64,configparser,re,json,time

conf = configparser.ConfigParser()
conf.read('config.ini', encoding="utf-8-sig")
headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn;  MI2 Build/JRO03L) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 XiaoMi/MiuiBrowser/1.0'}
# 登录
def login(account,password):
    global conn
    global rep
    LoginUrl = 'https://m.lrts.me/ajax/logon'
    conn = requests.session()
    PostData = {"account":account,"pwd":base64.b64encode(bytes(password,'ascii'))}
    rep = conn.post(LoginUrl, data=PostData,headers=headers)
    phone = rep.json()['phone']
    if phone =='':
        print(rep.json()['msg'])
    print('当前登录账号：%s'%phone)

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
    time.sleep(int(delay))
# 通过链接判断下载文件类型
def GetExtension(DownloadUrl):
    Extension = DownloadUrl.split('?')[0]
    Extension = Extension[-4:]
    return Extension
# 更改文件名
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

account = conf.get('LoginData','account')
password = conf.get('LoginData','password')
start = conf.get('DownLoadRange','Start')
stop = conf.get('DownLoadRange','Stop')
BookUrl = conf.get('BookUrl','BookUrl')
JsonRpcUrl = conf.get('Air2','JsonRpcUrl')
outfloder = conf.get('Air2','Outfloder')
delay = conf.get('Air2','Delay')
login(account,password)
# 解析下载链接
if 'book' in BookUrl:
    BookID = re.findall('book/(\d+)',BookUrl)[0]
    BookDetailUrl = 'https://m.lrts.me/ajax/getBookInfo?id=%s'%BookID
    BookDetail = conn.get(BookDetailUrl,headers=headers).json()
    print('当前解析书籍：',BookDetail['name'],'---',BookDetail['author'])
    ListUrl = 'https://m.lrts.me/ajax/getBookMenu?bookId=%s&pageNum=1&pageSize=5000&sortType=0'%BookID
    LenDetail = conn.get(ListUrl,headers=headers).json()
    AudioList = LenDetail['list']
    if len(AudioList)==1000:
        time.sleep(5)
        ListUrl = 'https://m.lrts.me/ajax/getBookMenu?bookId=%s&pageNum=2&pageSize=5000&sortType=0'%BookID
        LenDetail = conn.get(ListUrl,headers=headers).json()
        AudioList = AudioList + LenDetail['list']
    Len = len(AudioList)        
    print('本书总共集数：%s'%Len)
    print('配置下载范围:',start,'~',stop)
    for OneAudio in AudioList[int(start)-1:int(stop)]:
        AudioName = OneAudio['name']
        AudioName = ChangeFileName(AudioName)
        sections = OneAudio['section']
        SectionsUrl = 'https://m.lrts.me/ajax/getPlayPath?entityId=%s&entityType=3&opType=1&sections=[%s]&type=0'%(BookID,sections)
        SectionsJson = conn.get(SectionsUrl,headers=headers).json()
        try:
            DownloadUrl = SectionsJson['list'][0]['path']
            Air2DownLoad(JsonRpcUrl,DownloadUrl,AudioName+GetExtension(DownloadUrl))
        except:
            print(AudioName,SectionsJson['msg'])
elif 'album' in BookUrl:
    AlbumID = re.findall('album/(\d+)',BookUrl)[0]
    AlbumDetailUrl = 'https://m.lrts.me/ajax/getAlbumInfo?id=%s'%AlbumID
    AlbumDetail = conn.get(AlbumDetailUrl,headers=headers).json()
    print('当前解析专辑：',AlbumDetail['ablumn']['name'],'---',AlbumDetail['ablumn']['author'])
    ListUrl = 'https://m.lrts.me/ajax/getAlbumAudios?ablumnId=%s&sortType=0'%AlbumID
    LenDetail = conn.get(ListUrl,headers=headers).json()
    Len = LenDetail['count']
    print('本专辑共集数：%s'%Len)
    print('配置下载范围:',start,'~',stop)
    for OneAudio in LenDetail['list'][int(start)-1:int(stop)]:
        AudioName = OneAudio['name']
        AudioName = ChangeFileName(AudioName)
        sections = OneAudio['section']
        SectionsUrl = 'https://m.lrts.me/ajax/getPlayPath?entityId=%s&entityType=2&opType=1&sections=[%s]&type=0'%(AlbumID,sections)
        DownloadUrl = conn.get(SectionsUrl,headers=headers).json()['list'][0]['path']
        Air2DownLoad(JsonRpcUrl,DownloadUrl,AudioName+GetExtension(DownloadUrl))
else:
    print('暂不支持类型')