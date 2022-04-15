import requests,re,time
from threading import Thread
from queue import Queue


q = Queue(100000)

class FastRequests:
    def __init__(
            self,infos,threads=20,headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/99.0.4844.74',
            'Cookie':''
        }
    ):
        self.threads = threads # 线程数 20
        for info in infos:
            q.put(info)
        self.headres = headers

    def run(self):
        for i in range(self.threads):
            t = Consumer(self.headres)
            t.start()

class Consumer(Thread):
    def __init__(self,headers):
        Thread.__init__(self)
        self.headers = headers
        self.size = 0
        self.time = 0

    def run(self):
        while True:
            if q.qsize() == 0:
                break
            self.download(q.get())

    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def sizeFormat(self,size, is_disk=False, precision=2):

        formats = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        unit = 1000.0 if is_disk else 1024.0
        if not (isinstance(size, float) or isinstance(size, int)):
            raise TypeError('a float number or an integer number is required!')
        if size < 0:
            raise ValueError('number must be non-negative')
        for i in formats:
            size /= unit
            if size < unit:
                return f'{round(size, precision)}{i}'
        return f'{round(size, precision)}{i}'

    def download(self,info):
        title = info['title']
        link = info['link']
        if title == '':
            title = self.validateTitle(link.split('/')[-1])
        start_time = time.time()
        response = requests.get(url=link, headers=self.headers, stream=True).content
        end_time = time.time()
        self.time = end_time - start_time
        self.size += response.__sizeof__()

        with open(title,'wb') as f:
            f.write(response)
            f.close()
        title = title.split('/')[-1]
        print(f'{title} {self.sizeFormat(self.size)} 耗时：{round(self.time,3)}s')

if __name__ == '__main__':
    info1 = {
        'title':'1.ts',
        'link':'https://1252524126.vod2.myqcloud.com/9764a7a5vodtransgzp1252524126/215eee7e5285890804441012426/drm/v.f230.ts?start=0&end=2920399&type=mpegts'
    }
    info2 = {
        'title':'2.ts',
        'link':'https://1252524126.vod2.myqcloud.com/9764a7a5vodtransgzp1252524126/215eee7e5285890804441012426/drm/v.f230.ts?start=2920400&end=4720703&type=mpegts'
    }
    fr = FastRequests(infos=[info1,info2])
    fr.run()