# 说明

很久之前的项目，最近频繁收到`issues` 。图省事把gui等删了重写……

#### 配置说明：

仅修改`config.ini`即可，需配合Air2作为下载工具。如果用的是[Motrix](https://motrix.app/zh-CN/) ，则无需修改Air2→JsonRpcUrl。通常`.py`文件无需修改。

```
#书籍信息
[BookUrl]
#书籍链接，自动识别album与book
BookUrl = https://www.lrts.me/book/6953

#登录信息
[LoginData]
account = info@fuwenyue.com
password = &QaQKgHW6V4&JuoO

#下载范围
[DownLoadRange]
#开始集数
Start = 1020
#结束集数
Stop = 1024

#Air2 配置（默认Motrix）
[Air2]
#Air2 RPC
JsonRpcUrl = http://localhost:16800/jsonrpc
#下载至目录
Outfloder = E:\下载目录
#下载间隔
Delay = 10

```



![](images\lanrentingshu.png)



![](images\spyder.png)



![motrix](images\motrix.png)

