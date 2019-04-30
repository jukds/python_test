from django.conf.urls import url
#已修改,
#卧槽，国内网站是真的垃圾，stackoverflow是真的牛逼，服了
#书上的源码已经过时了版本库在不断变化
#template的构建方式也不同了
from django.contrib.auth.views import LoginView

from . import views

app_name = 'users'
urlpatterns = [
   url(r'^login/$',LoginView.as_view(),name='login'), 
   url(r'^logout/$', views.logout_view, name='logout'), 
   url(r'^register$',views.register,name='register'),
]