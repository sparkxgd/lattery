from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from foodball.models import Sfc as Mo
from foodball.models import SfcDetail
from foodball.models import Plurlanalysis
from foodball.analysisThread import analysisPlurlThread
from foodball.dataThread import load_data
from foodball.loadBonusControl import loadControl

import json


# 获取数据
def get_list(request):
    #   获取页面提交的数据
    expect = request.GET.get("expect","21001")
    #   到数据库去查找数据
    values = Mo.objects.filter(expect__contains=expect).values("id", "updatetime", "fsendtime", "expect",
                                                               "sfcdetail__ordernum", "sfcdetail__homestanding",
                                                               "sfcdetail__gueststanding", "sfcdetail__hometeam",
                                                               "sfcdetail__guestteam", "sfcdetail__plurl_3",
                                                               "sfcdetail__plurl_1", "sfcdetail__plurl_0","sfcdetail__result")
    datas = list(values)
    total = len(datas)
    # 构造返回数据
    if total == 0:
        result = {"code": -1, "msg": "暂无数据！！！", "count": total, "data": datas}
    else:
        result = {"code": 0, "msg": "查询成功！！", "count": total, "data": datas}

    return JsonResponse(result)


# 保存信息
def add(request):
    # 0：成功，-1：不成功
    result = {"code": 0, "msg": "操作成功！！"}
    # 获取页面的数据
    no = request.POST.get("no")
    name = request.POST.get("name")
    floorno = request.POST.get("floorno")
    remark = request.POST.get("remark")
    # 判断一下这个楼房是否存在，如果存在，就不能添加
    u = Mo.objects.filter(no=no)
    if u:
        result["code"] = -1
        result["msg"] = "用户已经存在，不能添加！！"
    else:
        # 插到数据库里面
        m = Mo()
        m.no = no
        m.name = name
        m.floorno = floorno
        m.status = 0
        m.remark = remark
        m.updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m.createtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 真正的保存
        m.save()
    return JsonResponse(result)

#   修改、编辑
def edit(request):
    result = {"code": 0, "msg": "修改成功！"}
    #   获取前端的数据
    id = request.POST.get("id")
    name = request.POST.get("name")
    no = request.POST.get("no")
    floorno = request.POST.get("floorno")
    updatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remark = request.POST.get("remark")
    #   更新
    Mo.objects.filter(id=id).update(name=name,no=no,floorno = floorno,remark=remark,updatetime=updatetime)
    return JsonResponse(result)

#   删除
def delete(request):
    result = {"code": 0, "msg": "删除成功！"}
    #   获取前端的数据
    ids = request.POST.get("id")
    Mo.objects.filter(id=ids).delete()
    return JsonResponse(result)


#   批量删除
def batchdel(request):
    result = {"code": 0, "msg": "删除成功！"}
    #   获取前端的数据
    ids = request.POST.get("ids")
    #   转化成json数据
    ids_json = json.loads(ids)
    #   转换成列表
    ids_list = []
    for m in ids_json:
        ids_list.append(m["id"])
    #   删除
    Mo.objects.filter(id__in=ids_list).delete()
    return JsonResponse(result)

#   获取下拉列表的期数
def get_expect_list(request):
    # 获取当前时间
    now_time = datetime.now()
    year = now_time.year
    ex_start = year % 100
    # 从数据库获取今年的所有数据
    values = Mo.objects.filter(expect__startswith=ex_start).order_by('expect')
    expects = []
    for v in values:
        expects.append(v.expect)
    result = {"code": 0, "msg": "查询成功！！", "count": 0, "data": expects}
    return JsonResponse(result)

#   更新数据
def update_data(request):
    result = {"code": 0, "msg": "更新成功！"}
    # 获取当前时间
    now_time = datetime.now()
    year = now_time.year
    ex_start = year % 100
    # 从数据库获取今年的所有数据
    values = Mo.objects.filter(expect__startswith=ex_start).order_by('expect')
    curr_expects = []  # 大于当前期
    max_expect = 0  # 最大期
    for v in values:
        expect = v.expect
        fsendtime = v.fsendtime
        if int(expect) > max_expect:
            max_expect = int(expect)
            if  fsendtime>now_time:
                curr_expects.append(expect)


        sd_values = SfcDetail.objects.filter(expect=expect)
        if sd_values:
            k_num = 0   # 未开奖场数
            # 如果不是空，说明已经有数据，那么就开始判断是否开奖
            for s in sd_values:
                if s.result == -1:
                    # 未开奖
                    k_num +=1
            if k_num>3:
                # 说明还未完全开奖，还可以更新
                es = []
                es.append(int(expect))
                load_data(es)
        else:
            # 暂时还没有数据，那么下载数据
            es = []
            es.append(int(expect))
            load_data(es)

    update_expects = []  # 需要更新的未来几期
    if len(curr_expects)>0:
        # 说明有数据
        curr_expects.sort()
        curr_expect = curr_expects[0]
        update_expects.append(int(curr_expect))
        update_expects.append(int(curr_expect)+1)
        update_expects.append(int(curr_expect)+2)
    else:
        update_expects.append(int(max_expect) + 1)
        update_expects.append(int(max_expect) + 2)
        update_expects.append(int(max_expect) + 3)
    load_data(update_expects)
    return JsonResponse(result)

#   分析赔率
def analysis_plurl(request):
    #   获取页面提交的数据
    expect = request.POST.get("expect")
    #   到数据库去查找数据
    values = SfcDetail.objects.filter(expect=expect)
    # 分一、二、三赔 的赔率
    p1 = []
    p2 = []
    p3 = []
    # 不分赔 零赔 总的排序分析
    p0 =[]
    for o in values:
        p = [{"plurl":o.plurl_3,"p":3},{"plurl":o.plurl_1,"p":1},{"plurl":o.plurl_0,"p":0}]
        p.sort(key=lambda keys:keys['plurl'])
        # 格式：赔率|场次|胜平负|结果|几赔
        v1 = {"plurl":p[0].get("plurl").__float__(),"ordernum":o.ordernum,"spf":p[0].get("p"),"result":o.result,"pei":1}
        v2 = {"plurl":p[1].get("plurl").__float__(),"ordernum":o.ordernum,"spf":p[1].get("p"),"result":o.result,"pei":2}
        v3 = {"plurl":p[2].get("plurl").__float__(),"ordernum":o.ordernum,"spf":p[2].get("p"),"result":o.result,"pei":3}
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

    result = {"code": 0, "msg": "分析完成！！！", "count": 0, "data": 0}

    return JsonResponse(result)


#   历史数据分析赔率
def analysis_plurl_all(request):
    #   获取页面提交的数据
    values = Mo.objects.all()
    # 创建新线程
    thread = analysisPlurlThread("分析赔率",values)
    # 开启新线程
    thread.start()
    thread.join()

    result = {"code": 0, "msg": "分析完成！！！", "count": 0, "data": 0}

    return JsonResponse(result)


#   排序
def peixue(v1,v2,v3):
    v = [v1,v2,v3]
    v.sort()
    return v

def get_analysis_plurl_list_3(request):
    #   获取页面提交的数据
    page = int(request.GET.get("page"))
    limit = int(request.GET.get("limit"))
    expect = request.GET.get("expect")
    if expect:
        #   到数据库去查找数据
        values = Plurlanalysis.objects.filter(expect=expect,peiname="零赔").order_by('-expect')[(page-1)*limit:limit*page].values()
        datas = list(values)
        total =Plurlanalysis.objects.filter(expect=expect,peiname="零赔").count()
    else:
        #   到数据库去查找数据
        values = Plurlanalysis.objects.filter(peiname="零赔").order_by('-expect')[(page-1)*limit:limit*page].values()
        datas = list(values)
        total =Plurlanalysis.objects.filter(peiname="零赔").count()


    # 重构造一下，使用于前端页面显示
    for v in range(len(datas)):
        # 将奖金信息查出来
        j_v = list(Mo.objects.filter(expect=datas[v].get("expect_id")).values())

        peivalue = eval(datas[v].get("peivalue"))
        peivalue_list = sorted(peivalue,key=lambda i:i["pei"])
        pei_1 = peivalue_list[:14]
        pei_2 = peivalue_list[14:28]
        pei_3 = peivalue_list[28:42]


        pei_1_ord = sorted(pei_1,key=lambda i:i["plurl"])
        pei_2_ord = []
        pei_3_ord = []
        for o in pei_1_ord:
            for o2 in pei_2:
                if o["ordernum"] == o2["ordernum"]:
                    pei_2_ord.append(o2)
            for o3 in pei_3:
                if o["ordernum"] == o3["ordernum"]:
                    pei_3_ord.append(o3)

        datas[v]["pei_1"] = pei_1_ord
        datas[v]["pei_2"] = pei_2_ord
        datas[v]["pei_3"] = pei_3_ord
        datas[v]["kj"] = j_v
    # 构造返回数据
    if total == 0:
        result = {"code": -1, "msg": "暂无数据！！！", "count": total, "data": datas}
    else:
        result = {"code": 0, "msg": "查询成功！！", "count": total, "data": datas}

    return JsonResponse(result)



def get_analysis_plurl_list_2(request):
    #   获取页面提交的数据
    page = int(request.GET.get("page"))
    limit = int(request.GET.get("limit"))
    expect = request.GET.get("expect")
    if expect:
        #   到数据库去查找数据
        values = Plurlanalysis.objects.filter(expect=expect,peiname__in=("一赔","二赔","三赔")).order_by('-expect')[(page-1)*limit:limit*page].values()
        datas = list(values)
        total =Plurlanalysis.objects.filter(expect=expect,peiname__in=("一赔","二赔","三赔")).count()
    else:
        #   到数据库去查找数据
        values = Plurlanalysis.objects.filter(peiname__in=("一赔","二赔","三赔")).order_by('-expect')[(page-1)*limit:limit*page].values()
        datas = list(values)
        total =Plurlanalysis.objects.filter(peiname__in=("一赔","二赔","三赔")).count()

    # 重构造一下，使用于前端页面显示
    for v in range(len(datas)):
        peivalue = eval(datas[v].get("peivalue"))
        peivalue_list = sorted(peivalue,key=lambda i:i["ordernum"])
        for i in range(len(peivalue_list)):
            k = "c_"+str(1+i)
            datas[v][k] = peivalue_list[i]

    # 构造返回数据
    if total == 0:
        result = {"code": -1, "msg": "暂无数据！！！", "count": total, "data": datas}
    else:
        result = {"code": 0, "msg": "查询成功！！", "count": total, "data": datas}

    return JsonResponse(result)


def get_analysis_plurl_list(request):
    #   获取页面提交的数据
    page = int(request.GET.get("page"))
    limit = int(request.GET.get("limit"))
    peiname = request.GET.get("peiname")
    if peiname:
        #   到数据库去查找数据
        values = Plurlanalysis.objects.filter(peiname=peiname).order_by('-expect')[(page-1)*limit:limit*page].values()
        datas = list(values)
        total =Plurlanalysis.objects.filter(peiname=peiname).count()
    else:
        #   到数据库去查找数据
        values = Plurlanalysis.objects.all().order_by('-expect')[(page-1)*limit:limit*page].values()
        datas = list(values)
        total =Plurlanalysis.objects.all().count()
    # 构造返回数据
    if total == 0:
        result = {"code": -1, "msg": "暂无数据！！！", "count": total, "data": datas}
    else:
        result = {"code": 0, "msg": "查询成功！！", "count": total, "data": datas}

    return JsonResponse(result)


# 下载奖金数据
def load_kj_data(request):
    expects = []
    values = Mo.objects.filter(Q(j91=-1)|Q(j91=None))
    for v in values:
        expects.append(v.expect)
    loadControl(expects,100)
    # 构造返回数据
    result = {"code": 0, "msg": "更新成功！！", "count": 0, "data": ""}

    return JsonResponse(result)