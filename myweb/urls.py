from django.conf.urls import url
from . import views

urlpatterns = [
    # =============商品展示
    # # 商城首页
    url(r'^shopindex$', views.shopindex,name="shopindex"),
    url(r'^shoplist$', views.shoplist,name="shoplist"),
    url(r'^shopmeilanx/(?P<gid>[0-9]+)$', views.shopmeilanx,name="shopmeilanx"),
   
    url(r'^shopregister$', views.shopregister,name="shopregister"),
    url(r'^shoplogin$', views.shoplogin,name="shoplogin"),
   
    # ========会员模块=============
    url(r'^dologin$', views.dologin, name="dologin"),
    url(r'^doregister$', views.doregister, name="doregister"),
    url(r'^loginout$', views.loginout, name="loginout"),
    # =========购物车==============
    url(r'^shopcart$', views.shopcart,name="shopcart"),
    url(r'^cartadd/(?P<sid>[0-9]+)$', views.cartadd, name="cartadd"),
    url(r'^cartempty$', views.cartempty, name="cartempty"),
    url(r'^cartdel/(?P<sid>[0-9]+)$', views.cartdel, name="cartdel"),
    url(r'^cartchange$', views.cartchange, name="cartchange"),
    url(r'^district/([0-9]+)$', views.district, name='district'),  #Ajax加载城市信息
    # =========订单=================
   
    url(r'^ordersform$',views.ordersform,name = 'ordersform'),#浏览订单
    url(r'^ordersconfirm$',views.ordersconfirm,name = 'ordersconfirm'),#确认订单
    url(r'^ordersinsert$',views.ordersinsert,name = 'ordersinsert'),#执行订单

    url(r'^ordersinfo$',views.ordersinfo,name = 'ordersinfo'),#订单信息
    # 订单处理
    url(r'^orderstatus$',views.orderstatus,name = 'orderstatus'),
    # 订单详情
    url(r'^shoporder$', views.shoporder,name="shoporder"), 


     #个人中心
    url(r'^shopmember$', views.shopmember,name="shopmember"), 
]
