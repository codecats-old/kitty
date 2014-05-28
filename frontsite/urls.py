from django.conf.urls import patterns, url, include
from frontsite import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^$', views.Index.as_view(), name='index'),
   url(r'^category$', views.Category.as_view(), name='category'),
   url(r'^category/(?P<id>\d+)/(?P<delete>\w+)?$', views.Category.as_view(), name='category_detail'),
   # url(r'^category/(?P<id>\d+)/(?P<delete>delete)$', views.Category.as_view(), name='category_detail_confirm'),
   url(r'^user$', views.User.as_view(), name='user'),
   url(r'^token$', views.token, name='token'),
   url(r'^locale/(?P<lang>[a-zA-Z_]+)', views.Locale.as_view(), name='locale'),
   url(r'^login$', views.Login.as_view(), name='login'),
   url(r'^registration$', views.Registration.as_view(), name='registration'),
   url(r'^logout$', views.Logout.as_view(), name='logout'),
)
