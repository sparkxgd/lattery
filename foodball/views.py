from django.shortcuts import render
from foodball.dataThread import getDataThread


years = [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

# 打开首页
def index(request):

    return render(request, "index.html")


def up(request):
    xiancs = []
    for y in years:
        # 创建新线程
        thread = getDataThread(y)
        # 开启新线程
        thread.start()
        xiancs.append(thread)

    for x in xiancs:
        x.join()



