from django.conf.urls import patterns, url, include
from chat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<chat_room_id>\d+)/$', views.chat_room, name='room'),
    url(r'^long-poll/(?P<chat_room_id>\d+)/$', views.longpoll_chat_room, name='logpoll_room'),
)
