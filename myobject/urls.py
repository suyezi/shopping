from django.conf.urls import include,url
from django.contrib import admin


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 网站后台
    url(r'^myadmin/', include('myadmin.urls')),
    # 网站前台
    url(r'^', include('myweb.urls')),
]
