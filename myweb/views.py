from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from myweb.models import Users,Types,Goods, District,Orders, Detail

import time
# ===============商城展示=============
#公共信息加载函数
def loadinfo1(s):
    context={}
    context['type0list'] = Types.objects.filter(pid=0)
    return context

#公共信息加载函数
def loadinfo():
    context={}
    context['type0list'] = Types.objects.filter(pid=0)
    return context
# 商城首页
def shopindex(request):
    context = loadinfo()
    mypic=[]
    numpic=0
    list = Goods.objects.extra(select = {'_has':'clicknum'}).order_by('-_has')
    for i  in list:
        if numpic <= 4:
            mypic.append(i)
            numpic += 1 
    print(mypic)
    print(numpic)
    context['mypic']=mypic

    return render(request,"myweb/shopindex.html",context)
# 商品列表
def shoplist(request):
    context = loadinfo()

    list = Goods.objects.filter()
    if Goods.state != 3:
        if request.GET.get('tid','') != '':
            tid = str(request.GET.get('tid',''))
            list = list.filter(typeid__in=Types.objects.only('id').filter(path__contains=','+tid+','))
        context['goodslist'] = list
        return render(request,"myweb/shoplist.html",context)

# 注册会员
def shopregister(request):
    context = loadinfo()
    return render(request,"myweb/shopregister.html")

# 执行注册
def doregister(request):
    try:
        ob = Users()
        ob.phone = request.POST['phone']
        ob.username = request.POST['username']
        # 获取密码并md5
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.psssword = m.hexdigest()
        ob.state = 1
        ob.addtime = time.time()
        ob.save()
        context = {'info':'注册成功,请登录!'}
        return render(request,"myweb/info.html",context)
    except:
        context = {'info':'注册失败!'}
    return render(request,"myweb/info.html",context)

# 会员登录
# 会员登录表单
def shoplogin(request):
    return render(request,"myweb/shoplogin.html")

# 会员执行登录
def dologin(request):
    try:
        #根据账号获取登录者信息
        user = Users.objects.get(phone=request.POST['phone'])
        #判断当前用户是否是后台管理员用户
        if user.state != 2:
            # 验证密码
            import hashlib
            m = hashlib.md5() 
            m.update(bytes(request.POST['password'],encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['vipuser'] = user.toDirct()
                
                return redirect(reverse('shopindex'))
            else:
                context = {'info':'登录密码错误！'}
                return render(request,"myweb/info.html",context)
        else:
            context = {'info':'此用禁止登录！'}
            return render(request,"myweb/info.html",context)
    except:
        context = {'info':'登录账号错误！'}
    return render(request,"myweb/info.html",context)


# 会员退出
def loginout(request):
    # 清楚登录的session信息
    del request.session['vipuser']
    # 跳转登录页面  地址改变
    return redirect(reverse('shoplogin'))
# 详情页
def shopmeilanx(request,gid):
    context = loadinfo()
    ob = Goods.objects.get(id=gid)
    # 累加点击量
    ob.clicknum += 1
    ob.save()
    context['goods'] = ob
    return render(request,"myweb/shopmeilanx.html",context)

# =============购物车===================
# 浏览购物车
def shopcart(request):
    context = loadinfo1(request)
    if 'shoplists' not in request.session:
        request.session['shoplists'] = {}
    return render(request,"myweb/shopcart.html",context)
# 添加购物车
def cartadd(request,sid):
    # context = loadinfo1(request)
    goods = Goods.objects.get(id = sid)
    shop = goods.toDirct();
    shop['nums'] = int(request.GET.get('nums'))

    if 'shoplists' in request.session:
        shoplists = request.session['shoplists']
    else:
        shoplists = {}
    if sid in shoplists:
        shoplists[sid]['nums'] += shop['nums']
    else:
        shoplists[sid] = shop
    request.session['shoplists'] = shoplists
    # return render(request,"myweb/shopcart.html")
    return redirect(reverse('shopcart'))
# 删除购物车
def cartdel(request,sid):
    shoplists = request.session['shoplists']
    del shoplists[sid]
    request.session['shoplists'] = shoplists
    return redirect(reverse('shopcart'))
# 清空购物车
def cartempty(request):
    context = loadinfo1(request)
    request.session['shoplists'] = {}
    return render(request,"myweb/shopcart.html",context)

# 改变购物车中商品的数量
def cartchange(request):
    context = loadinfo1(request) 
    shoplists = request.session['shoplists']
    # 获取信息
    shopid = request.GET['sid']
    num1 = int(request.GET.get('nums'))
    if num1 < 1:
        num1 = 1
    shoplists[shopid]['nums'] = num1 
    request.session['shoplists'] = shoplists
    return render(request,"myweb/shopcart.html",context)

# 城市级联

def district(request,upid):
    dlist = District.objects.filter(upid=upid)
    list = []
    for ob in dlist:
        list.append({'id':ob.id,'name':ob.name})
    return JsonResponse({'data':list})

# =========订单====================
def ordersform(request):
    # 获取要结账的商品id信息
    ids = request.GET.get('gids','')
    if ids == '':
        return HttpResponse('请选择要结账的商品')
    gids = ids.split(',')

    #获取购物车中的商品信息
    shoplists = request.session['shoplists']
    # 封装要结账的商品信息,以及累积的金额
    orderlist = {}
    total = 0
    for sid in gids:
        orderlist[sid] = shoplists[sid]
        total += shoplists[sid]['price']*shoplists[sid]['nums']#累计金额
    request.session['orderlist'] = orderlist
    request.session['total'] = total
    return render(request,"myweb/ordersform.html")
    

def ordersconfirm(request):
    print(request.POST['linkman'])
    print(request.POST['address'])
    print(request.POST['code'])
    print(request.POST['phone'])
    request.session['linkman'] = request.POST['linkman']
    request.session['address'] = request.POST['address']
    request.session['code'] = request.POST['code']
    request.session['phone'] = request.POST['phone']
    return render(request,"myweb/ordersconfirm.html")

def ordersinsert(request):
    # 封装订单信息,并执行添加
    orders = Orders()
    orders.uid = request.session['vipuser']['id']
    orders.linkman = request.session['linkman']
    orders.address = request.session['address']
    orders.code = request.session['code']
    orders.phone = request.session['phone']
    orders.addtime = time.time()
    orders.total = request.session['total']
    orders.status = 0
    orders.save()
    # 获取订单详情
    orderlist = request.session['orderlist']
    shoplists = request.session['shoplists']
    # 遍历购物信息,并添加订单详情
    for shop in orderlist.values():
        del shoplists[str(shop['id'])]
        detail = Detail()
        detail.orderid = orders.id
        detail.goodsid = shop['id']
        detail.name = shop['goods']
        detail.price = shop['price']
        detail.num = shop['nums']
        detail.save()
    del request.session['orderlist']
    del request.session['total']
    request.session['shoplists'] = shoplists
    del request.session['shoplists']
    context = {'info':'订单成功: 订单id号:'+str(orders.id)}
    return render(request,"myweb/info.html",context)
    # return HttpResponse('订单成功: 订单id号:'+str(orders.id))
# 提示信息
def ordersinfo(request):
   pass

def shoporder(request):
    context = loadinfo()
    # 从session中获取登录信息
    orders = Orders.objects.filter(uid = request.session['vipuser']['id'])
    # 遍历当前用户的所有订单信息,并获取每个订单所对应的订单详情信息,并以detaillist属性放置
    for order in orders:
        dlist = Detail.objects.filter(orderid=order.id)#获取当前订单中的详情
        order.detaillist = dlist #将订单详情以detaillist属性放置到订单对象中
        # 遍历当前订单信息,并追加每个商品的图片
        for detail in dlist:
            goods = Goods.objects.get(id = detail.goodsid)
            detail.picname = goods.picname
            print(detail.picname)
    context['orders'] = orders
    return render(request,"myweb/shoporder.html",context)

def orderstatus(request):
    ody = Orders.objects.get(id = request.GET.get('cd'))
    print(ody.status)
    if ody.status==0:
        ody.status = 3
    if ody.status==1:
        oty.status = 2  
    ody.save()
    return redirect(reverse('shoporder'))


# 个人中心
def shopmember(request):
    context = loadinfo()
    # 从session中获取登录信息
    users = Users.objects.filter(id = request.session['vipuser']['id'])
   
    dorder = Orders.objects.filter(uid =request.session['vipuser']['id'])

    mydorder = dorder.filter(status = 0)
    mynum = 0
    for i in mydorder:
        mynum += 1 
    print(mynum)

    mydorder1 = dorder.filter(status = 1)
    mynum1 = 0
    for j in mydorder:
        mynum1 += 1 
    print(mynum1)
    mydorder2 = dorder.filter(status = 2)
    mynum2 = 0
    for k in mydorder:
        mynum2 += 1 
    print(mynum2)
    context = {'ulist':users}
    return render(request,"myweb/shopmember.html",context)






