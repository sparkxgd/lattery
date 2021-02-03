import threading

from datetime import datetime
from foodball.models import Sfc,SfcDetail,Plurlanalysis



class analysisPlurlThread (threading.Thread):
    def __init__(self,name,values):
        threading.Thread.__init__(self)
        self.threadID = name
        self.values = values

    def run(self):
        print("开始线程：" + self.name)
        for v in self.values:
            analysis_plurl(v.expect)
        print("退出线程：" + self.name)


#   历史数据分析赔率
def analysis_plurl(expect):
        #   到数据库去查找数据
        values = SfcDetail.objects.filter(expect=expect)
        # 分一、二、三赔 的赔率
        p1 = []
        p2 = []
        p3 = []
        # 不分赔 零赔 总的排序分析
        p0 = []
        for o in values:
            p = [{"plurl": o.plurl_3, "p": 3}, {"plurl": o.plurl_1, "p": 1}, {"plurl": o.plurl_0, "p": 0}]
            p.sort(key=lambda keys: keys['plurl'])
            # 格式：赔率|场次|胜平负|结果|几赔
            v1 = {"plurl": p[0].get("plurl").__float__(), "ordernum": o.ordernum, "spf": p[0].get("p"), "result": o.result,
                  "pei": 1}
            v2 = {"plurl": p[1].get("plurl").__float__(), "ordernum": o.ordernum, "spf": p[1].get("p"), "result": o.result,
                  "pei": 2}
            v3 = {"plurl": p[2].get("plurl").__float__(), "ordernum": o.ordernum, "spf": p[2].get("p"), "result": o.result,
                  "pei": 3}
            p1.append(v1)
            p2.append(v2)
            p3.append(v3)

            p0.append(v1)
            p0.append(v2)
            p0.append(v3)

            # 排序
        p1.sort(key=lambda keys: keys['plurl'])
        p2.sort(key=lambda keys: keys['plurl'])
        p3.sort(key=lambda keys: keys['plurl'])
        p0.sort(key=lambda keys: keys['plurl'])
        # 保存数据
        an1 = Plurlanalysis()
        an1.expect_id = expect
        an1.peiname = "一赔"
        an1.peivalue = p1
        an1.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        an2 = Plurlanalysis()
        an2.expect_id = expect
        an2.peiname = "二赔"
        an2.peivalue = p2
        an2.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        an3 = Plurlanalysis()
        an3.expect_id = expect
        an3.peiname = "三赔"
        an3.peivalue = p3
        an3.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        an0 = Plurlanalysis()
        an0.expect_id = expect
        an0.peiname = "零赔"
        an0.peivalue = p0
        an0.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        obj = Plurlanalysis.objects.filter(expect=expect)
        if obj:
            Plurlanalysis.objects.filter(expect=expect).delete()
        an1.save()
        an2.save()
        an3.save()
        an0.save()



