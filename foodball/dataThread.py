import threading
from urllib.request import Request, urlopen
import urllib.error
from xml.etree import ElementTree
from foodball.models import Sfc,SfcDetail


qihao =[
{"year":"2006","num":77},
{"year":"2007","num":105},
{"year":"2008","num":102},
{"year":"2009","num":109},
{"year":"2010","num":128},
{"year":"2011","num":141},
{"year":"2012","num":178},
{"year":"2013","num":185},
{"year":"2014","num":189},
{"year":"2015","num":199},
{"year":"2016","num":199},
{"year":"2017","num":195},
{"year":"2018","num":176},
{"year":"2019","num":181},
{"year":"2020","num":83},
{"year":"2021","num":3},
]


class getDataThread (threading.Thread):
    def __init__(self,year):
        threading.Thread.__init__(self)
        self.threadID = year
        self.name = year

    def run(self):
        print("开始线程：" + self.name)
        for exp in qihao:
            for k, v in exp.items():
                if v == self.name:
                    get_page(self.name,exp.get("num"))
        print("退出线程：" + self.name)


def get_page(year, num):
    expects = get_expect(year,num)
    for expect in expects:
        o = Sfc.objects.filter(expect=expect)
        if not o:
            print(expect)
            someurl = "https://www.500.com/static/public/sfc/daigou/xml/"+expect+".xml"
            try:
                req = Request(someurl)
                with urlopen(req) as res:
                    html = res.read().decode()
                analysis_xml(html)
            except urllib.error.URLError as e:
                print(someurl)
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)

def get_expect(year, num):
    expects = []
    y = str(year)[2:]
    for i in range(1, num+1):
        n = get_expect_num(i)
        expect = y+str(n)
        expects.append(expect)
    return expects


def get_expect_num(no):
    if no < 10:
        return "00"+str(no)
    elif no < 100:
        return "0" + str(no)
    else:
        return no


def analysis_xml(d):
    tree = ElementTree.XML(d)
    head = analysis_head(tree)
    rows = analysis_row(tree,head)
    save_data(rows,head)


def analysis_head(tree):

    for node in tree.iter('head'):
        expect = node.attrib.get('expect')
        updatetime = node.attrib.get('updatetime')
        fsendtime = node.attrib.get('fsendtime')
        h = Sfc()
        h.expect = expect
        h.fsendtime = fsendtime
        h.updatetime = updatetime
    return h


def analysis_row(tree,head):
    rows = []
    for node in tree.iter('row'):
        ordernum = node.attrib.get('ordernum')
        hometeam = node.attrib.get('hometeam')
        guestteam = node.attrib.get('guestteam')
        homescore = node.attrib.get('homescore')
        guestscore = node.attrib.get('guestscore')
        result = node.attrib.get('result')

        homestanding = node.attrib.get('homestanding')
        gueststanding = node.attrib.get('gueststanding')

        if homestanding.__eq__(""):
            homestanding = -1
        if gueststanding.__eq__(""):
            gueststanding = -1

        p = node.attrib.get('plurl')
        if p.__eq__(""):
            plurl_3 = 0
            plurl_1 = 0
            plurl_0 = 0
        else:
            plurl = p.split("&nbsp;")
            plurl_3 = plurl[0]
            plurl_1 = plurl[1]
            plurl_0 = plurl[2]

        if result.__eq__("") or result.__eq__("*"):
            h = int(homescore)
            g = int(guestscore)
            if h > g:
                result = 3
            elif h < g:
                result = 0
            else:
                result = 1

            if h == -1 and g == -1:
                result = -1



        sfcd = SfcDetail()
        sfcd.expect = head
        sfcd.ordernum = ordernum
        sfcd.hometeam = hometeam
        sfcd.guestteam = guestteam
        sfcd.homescore = homescore
        sfcd.guestscore = guestscore
        sfcd.result = result
        sfcd.plurl_3 = plurl_3
        sfcd.plurl_1 = plurl_1
        sfcd.plurl_0 = plurl_0
        sfcd.homestanding = homestanding
        sfcd.gueststanding = gueststanding
        rows.append(sfcd)

    return rows


def save_data(rows,head):
    o = Sfc.objects.filter(expect=head.expect)
    if not o:
        head.save()
    else:
        Sfc.objects.filter(expect=head.expect).update(fsendtime=head.fsendtime, updatetime=head.updatetime)

    need_save = []
    for r in rows:
        sd = SfcDetail.objects.filter(expect=head.expect,ordernum=r.ordernum)
        if sd:
            sd.update(homescore=r.homescore, guestscore=r.guestscore, result=r.result, plurl_3=r.plurl_3,
                      plurl_1=r.plurl_1, plurl_0=r.plurl_0)
        else:
            need_save.append(r)
    SfcDetail.objects.bulk_create(need_save)


# 根据期号下载数据
class LoadDataThread (threading.Thread):
    def __init__(self,name,expect):
        threading.Thread.__init__(self)
        self.threadID = name
        self.name = name
        self.vs = expect

    def run(self):
        print("开始线程：" + self.name)
        for p in self.vs:
            load_page(p)
        print("退出线程：" + self.name)


def load_page(expect_int):
    expect = str(expect_int)
    print(expect)
    someurl = "https://www.500.com/static/public/sfc/daigou/xml/" + expect + ".xml"
    try:
        req = Request(someurl)
        with urlopen(req) as res:
            html = res.read().decode()
        analysis_xml(html)
    except urllib.error.URLError as e:
        print(someurl)
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


#   根据期号下载数据
def load_data(expect):
    # 创建新线程
    thread = LoadDataThread("更新数据线程",expect)
    # 开启新线程
    thread.start()
    thread.join()