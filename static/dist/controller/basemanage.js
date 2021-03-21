/** layuiAdmin.pro-v1.2.1 LPPL License By http://www.layui.com/admin/ */
;layui.define(["table", "form"], function (e) {
    var i = (layui.$, layui.admin), t = layui.view, l = layui.table, r = layui.form;
    //楼房信息管理
    l.render({//楼房信息管理的表格
        elem: "#LAY-floor-back-manage",
        url: "/floors/",
        cols: [[{type: "checkbox", fixed: "left"}, {field: "id", width: 80, title: "ID", sort: !0}, {
            field: "no",
            title: "楼房编号"
        }, {
            field: "name",
            title: "楼房名称"
        }, {
            field: "floorno",
            title: "楼层"
        }
            , {field: "updatetime", title: "更新时间", sort: !0}
            , {
                field: "status",
                title: "状态",
                templet: "#buttonTpl",
                minWidth: 80,
                align: "center"
            }, {title: "操作", width: 150, align: "center", fixed: "right", toolbar: "#table-floor-admin"}]],
        page: !0,
        limit: 30,
        height: "full-320",
        text: "对不起，加载出现异常！"
    }), l.on("tool(LAY-floor-back-manage)", function (e) {
        var l = e.data;
        "del" === e.event ?  layer.confirm("确定删除此楼房？", function (i) {
                   //提交 Ajax 成功后，关闭当前弹层并重载表格
               layui.admin.req({
                  type:"POST",
                  url:"/floor_del/",
                  data:{"id":l.id},
                  dataType:"json",
                  success:function (r) {
                      layer.alert(r.msg);
                      layui.table.reload("LAY-floor-back-manage");
                  }
              })
                    , e.del()
                    , layer.close(i)
        }) : "edit" === e.event && i.popup({
            title: "编辑楼房",
            area: ["420px", "450px"],
            id: "LAY-popup-floor-add",
            success: function (e, i) {
                t(this.id).render("baseMange/floor/addform", l).done(function () {
                    r.render(null, "layuiadmin-form-floor"), r.on("submit(LAY-floor-back-submit)", function (e) {
                         layui.admin.req({
                                            type:"post",
                                            url:"/floor_edit/",
                                            data:e.field,
                                            dataType:"json",
                                            success:function (r) {
                                                layer.alert(r.msg);
                                                layui.table.reload("LAY-floor-back-manage");
                                            }
                                         }), layer.close(i)
                    })
                })
            }
        })
    }),

        //房间类型新管理
    l.render({//房间类型管理的表格
        elem: "#LAY-roomtype-back-manage",
        url: "/roomtypes/",
        cols: [[{type: "checkbox", fixed: "left"}, {field: "id", width: 80, title: "ID", sort: !0}, {
            field: "typename",
            title: "类型名称"
        }, {
            field: "price",
            title: "普通价"
        }, {
            field: "vip_price",
            title: "会员价"
        }
            , {field: "updatetime", title: "更新时间", sort: !0}
            ,  {title: "操作", width: 150, align: "center", fixed: "right", toolbar: "#table-roomtype-admin"}]],
        page: !0,
        limit: 30,
        height: "full-320",
        text: "对不起，加载出现异常！"
    }), l.on("tool(LAY-roomtype-back-manage)", function (e) {
        var l = e.data;
        "del" === e.event ?  layer.confirm("确定删除？", function (i) {
                   //提交 Ajax 成功后，关闭当前弹层并重载表格
               layui.admin.req({
                  type:"POST",
                  url:"/roomtype_del/",
                  data:{"id":l.id},
                  dataType:"json",
                  success:function (r) {
                      layer.alert(r.msg);
                      layui.table.reload("LAY-roomtype-back-manage");
                  }
              })
                    , e.del()
                    , layer.close(i)
        }) : "edit" === e.event && i.popup({
            title: "编辑房间类型",
            area: ["420px", "450px"],
            id: "LAY-popup-roomtype-add",
            success: function (e, i) {
                t(this.id).render("baseMange/roomtype/addform", l).done(function () {
                    r.render(null, "layuiadmin-form-roomtype"), r.on("submit(LAY-roomtype-back-submit)", function (e) {
                         layui.admin.req({
                                            type:"post",
                                            url:"/roomtype_edit/",
                                            data:e.field,
                                            dataType:"json",
                                            success:function (r) {
                                                layer.alert(r.msg);
                                                layui.table.reload("LAY-roomtype-back-manage");
                                            }
                                         }), layer.close(i)
                    })
                })
            }
        })
    }),


            //胜负彩信息管理
    l.render({//胜负彩信息管理的表格
        elem: "#LAY-sfc-back-manage",
        url: "/sfcs/",
        cols: [[{
            field: "expect",
            title: "期号"
        },{
            field: "sfcdetail__ordernum",
            title: "序号",
            templet: '#titleTpl'
        },{
            field: "sfcdetail__hometeam",
            title: "主队"
        }, {
            field: "sfcdetail__guestteam",
            title: "客队"
        },{
            field: "sfcdetail__homestanding",
            title: "主队排名"
        }, {
            field: "sfcdetail__gueststanding",
            title: "客队排名"
        }, {
            field: "sfcdetail__plurl_3",
            title: "胜赔率"
        }, {
            field: "sfcdetail__plurl_1",
            title: "平赔率"
        },{
            field: "sfcdetail__plurl_0",
            title: "负赔率"
        },{
            field: "sfcdetail__result",
            title: "结果<span class='layui-badge layui-bg-blue'>一赔</span><span class='layui-badge layui-bg-orange'>二赔</span><span class='layui-badge layui-bg-danger'>三赔</span>",
             width: 200
            ,toolbar: "#table-sfc-result"
        }
        , {title: "操作", width: 400, align: "center", fixed: "right", toolbar: "#table-sfc-admin"}]],
        text: "对不起，加载出现异常！"
    }), l.on("tool(LAY-floor-back-manage)", function (e) {
        var l = e.data;
        "del" === e.event ?  layer.confirm("确定删除此楼房？", function (i) {
                   //提交 Ajax 成功后，关闭当前弹层并重载表格
               layui.admin.req({
                  type:"POST",
                  url:"/sfc_del/",
                  data:{"id":l.id},
                  dataType:"json",
                  success:function (r) {
                      layer.alert(r.msg);
                      layui.table.reload("LAY-sfc-back-manage");
                  }
              })
                    , e.del()
                    , layer.close(i)
        }) : "edit" === e.event && i.popup({
            title: "编辑楼房",
            area: ["420px", "450px"],
            id: "LAY-popup-floor-add",
            success: function (e, i) {
                t(this.id).render("baseMange/sfc/addform", l).done(function () {
                    r.render(null, "layuiadmin-form-fsfc"), r.on("submit(LAY-sfc-back-submit)", function (e) {
                         layui.admin.req({
                                            type:"post",
                                            url:"/sfc_edit/",
                                            data:e.field,
                                            dataType:"json",
                                            success:function (r) {
                                                layer.alert(r.msg);
                                                layui.table.reload("LAY-sfc-back-manage");
                                            }
                                         }), layer.close(i)
                    })
                })
            }
        })
    }),

l.render({//胜负彩赔率分析管理的表格
        elem: "#LAY-plurl-back-manage",
        url: "/plurls/",
        cols: [[{
            field: "expect_id",
            title: "期号",
            width: 80
        },{
            field: "peiname",
            title: "赔名称",
            width: 80
        }, {
            field: "peivalue",
            title: "赔率分析",
            toolbar: "#table-plurl-peivalue_1",
             width: 150

        }, {
            field: "peivalue",
            title: "赔率",
            toolbar: "#table-plurl-peivalue_2"

        }

        ]],
        page: !0,
        limit: 32,
        height: "full-320",
        text: "对不起，加载出现异常！"
    }), l.on("tool(LAY-floor-back-manage)", function (e) {
        var l = e.data;
        "del" === e.event ?  layer.confirm("确定删除此楼房？", function (i) {
                   //提交 Ajax 成功后，关闭当前弹层并重载表格
               layui.admin.req({
                  type:"POST",
                  url:"/plurl_del/",
                  data:{"id":l.id},
                  dataType:"json",
                  success:function (r) {
                      layer.alert(r.msg);

                      layui.table.reload("LAY-plurl-back-manage");
                  }
              })
                    , e.del()
                    , layer.close(i)
        }) : "edit" === e.event && i.popup({
            title: "编辑楼房",
            area: ["420px", "450px"],
            id: "LAY-popup-floor-add",
            success: function (e, i) {
                t(this.id).render("baseMange/plurl/addform", l).done(function () {
                    r.render(null, "layuiadmin-form-plurl"), r.on("submit(LAY-plurl-back-submit)", function (e) {
                         layui.admin.req({
                                            type:"post",
                                            url:"/plurl_edit/",
                                            data:e.field,
                                            dataType:"json",
                                            success:function (r) {
                                                layer.alert(r.msg);
                                                layui.table.reload("LAY-plurl-back-manage");
                                            }
                                         }), layer.close(i)
                    })
                })
            }
        })
    }),
        l.render({//胜负彩赔率分析管理的表格
        elem: "#LAY-plurl2-back-manage",
        url: "/plurls_2/",
        cols: [[{
            field: "expect_id",
            title: "期号",
            width: 80,
            rowspan: 2
        },{
            field: "peiname",
            title: "赔名称",
            width: 80,
            rowspan: 2

        } ,{align: 'center', title: '场次', colspan: 14}], //colspan即横跨的单元格数，这种情况下不用设置field和width
            [{
            field: "c_1",
            title: "1场",
            width: 75,
            templet: function(obj){
                var d = obj.c_1;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_2",
            title: "2场",
            templet: function(obj){
                var d = obj.c_2;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }
        }
        , {
            field: "c_3",
            title: "3场",
            templet: function(obj){
                var d = obj.c_3;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }
        }, {
            field: "c_4",
            title: "4场",
            templet: function(obj){
                var d = obj.c_4;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_5",
            title: "5场",
            templet: function(obj){
                var d = obj.c_5;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_6",
            title: "6场",
            templet: function(obj){
                var d = obj.c_6;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_7",
            title: "7场",
            templet: function(obj){
                var d = obj.c_7;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_8",
            title: "8场",
            templet: function(obj){
                var d = obj.c_8;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_9",
            title: "9场",
            templet: function(obj){
                var d = obj.c_9;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_10",
            title: "10场",
            templet: function(obj){
                var d = obj.c_10;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_11",
            title: "11场",
            templet: function(obj){
                var d = obj.c_11;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_12",
            title: "12场",
            templet: function(obj){
                var d = obj.c_12;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_13",
            title: "13场",
            templet: function(obj){
                var d = obj.c_13;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }

        }, {
            field: "c_14",
            title: "14场",
            templet: function(obj){
                var d = obj.c_14;
                var arr = new Array();
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    return arr.join("");
            }
        }
        ]], even: true //开启隔行背景
        ,size: 'sm', //小尺寸的表格
        page: !0,
        limit: 33,
        height: "full-320",
        text: "对不起，加载出现异常！"
    }), l.on("tool(LAY-floor-back-manage)", function (e) {
        var l = e.data;
        "del" === e.event ?  layer.confirm("确定删除此楼房？", function (i) {
                   //提交 Ajax 成功后，关闭当前弹层并重载表格
               layui.admin.req({
                  type:"POST",
                  url:"/plurl_del/",
                  data:{"id":l.id},
                  dataType:"json",
                  success:function (r) {
                      layer.alert(r.msg);

                      layui.table.reload("LAY-plurl2-back-manage");
                  }
              })
                    , e.del()
                    , layer.close(i)
        }) : "edit" === e.event && i.popup({
            title: "编辑楼房",
            area: ["420px", "450px"],
            id: "LAY-popup-floor-add",
            success: function (e, i) {
                t(this.id).render("baseMange/plurl2/addform", l).done(function () {
                    r.render(null, "layuiadmin-form-plurl2"), r.on("submit(LAY-plurl2-back-submit)", function (e) {
                         layui.admin.req({
                                            type:"post",
                                            url:"/plurl_edit/",
                                            data:e.field,
                                            dataType:"json",
                                            success:function (r) {
                                                layer.alert(r.msg);
                                                layui.table.reload("LAY-plurl2-back-manage");
                                            }
                                         }), layer.close(i)
                    })
                })
            }
        })
    }),
 l.render({//胜负彩赔率分析管理的表格3
        elem: "#LAY-plurl3-back-manage",
        url: "/plurls_3/",
        cols: [[{
            field: "expect_id",
            title: "期号",
            width: 80,
        },{
            field: "peivalue",
            title: "分析",
            width: 130,
            templet: function(d){
                let kj9 = d.kj[0].j91;
                let objs = eval(d.peivalue);
                let arr = new Array();
                let num = 0;
                let z_plurl_total = 0;
                let z_plurl = 0;
                for(var i=0;i < objs.length;i++){
                    z_plurl +=parseFloat(objs[i].plurl);
                    if(objs[i].spf==objs[i].result){
                        num +=1;
                        z_plurl_total +=parseFloat(objs[i].plurl);
                    }
                }
                arr.push("<p>任九：");
                arr.push(kj9);
                arr.push("元</p>");

                arr.push("<p>总计：");
                let z_plurl_r = Math.round(z_plurl*100)/100;
                arr.push(z_plurl_r);
                arr.push("</p>");

                arr.push("<p>中总计：");
                let z_plurl_total_r = Math.round(z_plurl_total*100)/100;
                arr.push(z_plurl_total_r);
                arr.push("</p>");

                arr.push("<p>中平均：");
                let x=z_plurl_total/num;
                let z_plurl_avg = Math.round(x*100)/100;
                arr.push(z_plurl_avg);
                arr.push("</p>");
                return arr.join("");
             }
        },{
            field: "pei_1",
            title: "信息<span class='layui-badge layui-bg-black'>0</span><span class='layui-badge layui-bg-blue'>1</span><span class='layui-badge'>3</span>",
            templet: function(obj){
                var pei_1 = obj.pei_1;
                var pei_2 = obj.pei_2;
                var pei_3 = obj.pei_3;
                var objs= obj.peivalueall;
                var arr = new Array();

                for(var i=0;i < objs.length;i++){
                        var tip = "场次："+objs[i].ordernum+" 胜平负："+objs[i].spf;
                        if(objs[i].spf==objs[i].result){
                            arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                        }else{
                            arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                        }
                        arr.push(objs[i].plurl);
                        arr.push(" </span> ");
                    }
                arr.push(" </br> ");
                //分析，获取后面的数据
                var pervobjs=objs.slice(24,objs.length-1);
                //定义14场都是310
                var p_14 = ["310","310","310","310","310","310","310","310","310","310","310","310","310","310"];
                //出去分析后面的20个，剩下的
                for(var j=0;j<p_14.length;j++){
                     for(var i=0;i < pervobjs.length;i++){
                         if(pervobjs[i].ordernum===j+1){
                            var spf=pervobjs[i].spf;
                            var a = p_14[j].replace(spf,'');
                            p_14[j]=a;
                         }
                    }
                }
                arr.push("去除20后：");
                for(var j=0;j<p_14.length;j++){
                    for(var k in pei_1){
                        var d = pei_1[k];
                        if(d.ordernum===(j+1)){
                            var tip = "场次："+d.ordernum+" 胜平负："+d.spf+" 开奖："+d.result;
                            if(p_14[j].indexOf(d.result) != -1){
                                arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                            }else{
                                arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                            }
                        }
                    }
                    arr.push(" <span class='layui-badge layui-bg-blue'> ");
                     arr.push(j+1);
                     arr.push("</span> ");
                     arr.push(p_14[j]);
                     arr.push("</span> ");
                }
                arr.push("预测：");
                var ag=1;
                var arr_mr = [];
                while (ag<10){
                    var mr = Math.floor(Math.random() * 14)+1;
                    var f = true;
                    for(k = 0;k < arr_mr.length;k++){
                        if (mr == arr_mr[k]) {
                            f = false;
                             break;
                         }
                    }
                    if(f){
                         arr_mr[ag]=mr;
                         ag +=1;
                    }
                }
                arr.push(arr_mr.sort(function(a, b){return a - b}));
                arr.push(" </br> ");

                arr.push("<table border='1'>");
                arr.push("<tr>");

                arr.push("<td>");
                arr.push("一赔");
                arr.push("</td>");
                for(var k in pei_1){

                    arr.push("<td>");
                    var d = pei_1[k];
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;

                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    if(d.spf==0){
                        arr.push(" <span class='layui-badge-dot layui-bg-black'></span>");
                    }else if(d.spf==1){
                        arr.push(" <span class='layui-badge-dot layui-bg-blue'></span>");
                    }else{
                        arr.push(" <span class='layui-badge-dot'></span>");
                    }
                    arr.push(d.ordernum);
                    arr.push("</td>");
                }
                arr.push("</tr>");

                arr.push("<tr>");

                arr.push("<td>");
                arr.push("二赔");
                arr.push("</td>");
                for(var k in pei_2){
                    arr.push("<td>");
                    var d = pei_2[k];
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    arr.push("</td>");
                }
                arr.push("</tr>");

                arr.push("<tr>");
                arr.push("<td>");
                arr.push("三赔");
                arr.push("</td>");
                for(var k in pei_3){
                    arr.push("<td>");
                    var d = pei_3[k];
                    var tip = "场次："+d.ordernum+" 胜平负："+d.spf;
                    if(d.spf==d.result){
                        arr.push(" <span class='layui-badge' title='"+tip+"'> ");
                    }else{
                        arr.push(" <span class='layui-badge layui-bg-gray' title='"+tip+"'> ");
                    }
                    arr.push(d.plurl);
                    arr.push(" </span> ");
                    arr.push("</td>");
                }
                arr.push("</tr>");

                arr.push("</table>");

                return arr.join("");
            }

        }

        ]],
        even: true, //开启隔行背景
        page: !0,
        limit: 33,
        height: "full-320",
        text: "对不起，加载出现异常！"
    }), l.on("tool(LAY-floor-back-manage)", function (e) {
        var l = e.data;
        "del" === e.event ?  layer.confirm("确定删除此楼房？", function (i) {
                   //提交 Ajax 成功后，关闭当前弹层并重载表格
               layui.admin.req({
                  type:"POST",
                  url:"/plurl_del/",
                  data:{"id":l.id},
                  dataType:"json",
                  success:function (r) {
                      layer.alert(r.msg);

                      layui.table.reload("LAY-plurl2-back-manage");
                  }
              })
                    , e.del()
                    , layer.close(i)
        }) : "edit" === e.event && i.popup({
            title: "编辑楼房",
            area: ["420px", "450px"],
            id: "LAY-popup-floor-add",
            success: function (e, i) {
                t(this.id).render("baseMange/plurl2/addform", l).done(function () {
                    r.render(null, "layuiadmin-form-plurl2"), r.on("submit(LAY-plurl2-back-submit)", function (e) {
                         layui.admin.req({
                                            type:"post",
                                            url:"/plurl_edit/",
                                            data:e.field,
                                            dataType:"json",
                                            success:function (r) {
                                                layer.alert(r.msg);
                                                layui.table.reload("LAY-plurl2-back-manage");
                                            }
                                         }), layer.close(i)
                    })
                })
            }
        })
    }),

        e("basemanage", {})
});