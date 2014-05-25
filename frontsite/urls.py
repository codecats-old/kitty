from django.conf.urls import patterns, url, include
from frontsite import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^$', views.Index.as_view(), name='index'),
   url(r'^login$', views.Login.as_view(), name='login'),
   url(r'^registration$', views.Registration.as_view(), name='registration'),
   url(r'^logout$', views.Logout.as_view(), name='logout'),
)
