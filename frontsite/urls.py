from django.conf.urls import patterns, url, include
from frontsite import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^$', views.IndexView.as_view(), name='index'),
   url(r'^login$', views.login, name='login'),
   url(r'^registration$', views.registration, name='registration'),
   url(r'^logout$', logout, name='logout'),
)
