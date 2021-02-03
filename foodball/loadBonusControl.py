'''
下载、分析及保存奖金数据相关控制
2021年1月11日12:59:24
'''
import threading
from foodball.models import Sfc
import requests
import urllib.error
from bs4 import BeautifulSoup


# 下载奖金数据
def loadBonusInfo(expect):
    if expect:
        someurl = "https://zx.500.com/zc/inc/zc_kaijiang.php"
        d = {"gt": "ajax", "lotid": 1, "expect": expect}
        try:
            req = requests.post(someurl, data=d)
            html = str(req.content, encoding='utf-8')
            analysis(expect,html)
        except urllib.error.URLError as e:
            print(someurl)
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)


#   解析奖金数据
def analysis(expect,html):
    soup = BeautifulSoup(html, 'html.parser')
    kj_info_r = soup.find('div', attrs={"class": "kj-info-r"})
    print(expect)
    # print(kj_info_r)
    if kj_info_r:
        lis = kj_info_r.findAll('li')
        # print(lis)
        #   14场一等奖
        j_14_1 = lis[0].findAll('em')[1].string.replace(",","")
        #   14场二等奖
        j_14_2 = lis[1].findAll('em')[1].string.replace(",","")
        #   14场销售总金额
        j_14_t = lis[2].em.string.replace(",","")
        #   9场一等奖
        j_9_1 = lis[3].findAll('em')[1].string.replace(",","")
        #   9场销售总金额
        j_9_t = lis[4].em.string.replace(",","")
        # print(j_9_t)
        save_data(expect,j_14_1,j_14_2,j_14_t,j_9_1,j_9_t)


def save_data(expect,j_14_1,j_14_2,j_14_t,j_9_1,j_9_t):
    if j_14_1=='--':
        j_14_1=-1
    if j_14_2=='--':
        j_14_2=-1
    if j_14_t=='--':
        j_14_t=-1
    if j_9_1=='--':
        j_9_1=-1
    if j_9_t=='--':
        j_9_t=-1
    o = Sfc.objects.filter(expect=expect).first()
    if o:
        if not o.j91 or o.j91 == -1:
            Sfc.objects.filter(expect=expect).update(j141=j_14_1,j142=j_14_2,j14t=j_14_t,j91=j_9_1,j9t=j_9_t)


# 下载数据线程
class LoadDataThread (threading.Thread):
    def __init__(self,name,expects=[]):
        threading.Thread.__init__(self)
        self.threadID = name
        self.expects = expects

    def run(self):
        print("开始线程：" + self.threadID)
        for exp in self.expects:
            loadBonusInfo(exp)
        print("退出线程：" + self.threadID)


# 下载数据控制
def loadControl(expects=[],num=10):
    if len(expects) <= num:
        # 开启一个线程即可
        x = LoadDataThread("loadkj",expects)
        x.start()
        x.join()

    else:
        xs = []
        for i in range(0,len(expects),num):
            x = LoadDataThread(str(i), expects[i:i+num])
            xs.append(x)

        for x in xs:
            x.start()

        for x in xs:
            x.join()

if __name__ == '__main__':
    loadBonusInfo("21001")