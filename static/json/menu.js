{
  "code": 0
  ,"msg": ""
  ,"data": [
    {
    "title": "统计中心"
    ,"icon": "layui-icon-home"
    ,"list": [{
      "name": "basemanage"
      ,"title": "基本信息"
      ,"list":[{
        "name": "sfc"
        ,"title": "胜负彩"
        ,"jump": "baseMange/sfc/list"
        },{
        "name": "plurl"
        ,"title": "赔率分析"
        ,"jump": "baseMange/analysi_plurl/list"
        },{
        "name": "plurl2"
        ,"title": "赔率分析2"
        ,"jump": "baseMange/analysi_plurl_2/list"
        },{
        "name": "plurl3"
        ,"title": "赔率分析3"
        ,"jump": "baseMange/analysi_plurl_3/list"
        }]
    }, {
      "name": "userlist"
      ,"title": "用户管理"
        ,"jump": "user/administrators/list"
    }, {
      "name": "homepage2"
      ,"title": "权限管理"
      ,"jump": "home/homepage2"
    }]
  },
   {
    "name": "set"
    ,"title": "设置"
    ,"icon": "layui-icon-set"
    ,"list": [{
      "name": "system"
      ,"title": "系统设置"
      ,"spread": true
      ,"list": [{
        "name": "website"
        ,"title": "网站设置"
      },{
        "name": "email"
        ,"title": "邮件服务"
      }]
    },{
      "name": "user"
      ,"title": "个人中心"
      ,"spread": true
      ,"list": [{
        "name": "info"
        ,"title": "基本资料"
      },{
        "name": "password"
        ,"title": "修改密码"
      }]
    }]
  }]
}