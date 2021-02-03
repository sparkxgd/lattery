import requests
import json
import urllib.error
from bs4 import BeautifulSoup


# 下载奖金数据
def loadBonusInfo(expect):
    if expect:
        someurl = "https://zx.500.com/zc/inc/zc_kaijiang.php"
        d = {"gt": "ajax", "lotid": 1, "expect": expect}
        print(someurl+"?"+expect)
        try:
            req = requests.post(someurl,data=d)
            html = str(req.content, encoding='utf-8')
            analysis(expect,html)
        except urllib.error.URLError as e:
            print(someurl)
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)


def analysis(expect,html):
    soup = BeautifulSoup(html, 'html.parser')
    kj_info_r = soup.find('div', attrs={"class": "kj-info-r"})
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
    print(j_9_1)




if __name__ == '__main__':
    loadBonusInfo("21002")
