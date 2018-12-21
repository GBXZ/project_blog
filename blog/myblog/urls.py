from django.contrib import admin
from django.urls import path, include,re_path
from myblog import views


# 设置命名空间需要加上 app_name
app_name = 'myblog'
urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    re_path('detail/(?P<pk>\d*)', views.Detail.as_view(), name='detail'),
    path('oauth_weibo_login', views.weibo_login, name='wb_login'),   # 微博登陆页面
    path('weibo/connect/callback.php', views.weibo_get_code),  # 微博回调页面
    path('myself/', views.Formyself.as_view(), name='myself'),  # 介绍
    path('contact/', views.Contact.as_view(), name='contact'),  # 联系
    path('fully/', views.Full_width.as_view(), name='fully'),
]
