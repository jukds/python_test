from django.conf.urls import url
from . import views

app_name = 'fristwebapp'
urlpatterns = [
    #index
    url(r'^$', views.index,name ='index'),
    #all topic
    url(r'^topics/$',views.topics,name = 'topics'),
    #special page
    url(r'^topics/(?P<topic_id>\d+)/$',views.topic, name = 'topic'),
    #add new topic page
    url(r'^new_topic/$',views.new_topic,name = 'new_topic'),
    #add new entry page 
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry,name = 'new_entry'),
    #edit entry page
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,name = 'edit_entry'),
    #测试内容2019.3.7
    url(r'^fristwebapp/ajax/$',views.ajax_page),
    url(r'^fristwebapp/ajax_update/$',views.ajax_test),
    url(r'^fristwebapp/ajax_update2$',views.ajax_test2),
]