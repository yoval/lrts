# 说明

[懒人听书](https://www.lrts.me/) 下载工具gui 版，可下载**登录账号已购买内容**（vip账号可下载vip限免）。

已打包为exe格式：https://fuwenyue.lanzouf.com/ij2bC039n4ej

#### 1、使用方法：

![](https://gitee.com/fuwenyue/tuchuang/raw/master/1650035253716lrts.png)


默认使用 motrix 的端口，不会使用Aira2的直接用 https://motrix.app/zh-CN 即可。

#### 2、安装依赖包

`pip install -r requirements.txt`

#### 3、打包

`Pyinstaller -F -w lrts.py -i favicon.ico -p download.py`
