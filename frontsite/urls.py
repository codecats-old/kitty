from django.conf.urls import patterns, url, include
from frontsite import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   url(r'^$', views.Index.as_view(), name='index'),
   url(r'^avatar/$', views.avatar, name='avatar'),
   url(r'^show-avatar/(?P<path>.+)$', views.show_avatar, name='show-avatar'),
   url(r'^vote/(?P<profile_id>\d+)$', views.vote, name='vote'),
   url(r'^category$', views.Category.as_view(), name='category'),
   url(r'^category/(?P<id>\d+)/(?P<delete>\w+)?$', views.Category.as_view(), name='category_detail'),
   url(r'^user/(?P<id>\d+)$', views.User.as_view(), name='user'),
   url(r'^users/$', views.get_all_users, name='all_users'),
   url(r'^token$', views.token, name='token'),
   url(r'^locale/(?P<lang>[a-zA-Z_]+)', views.Locale.as_view(), name='locale'),
   url(r'^login$', views.Login.as_view(), name='login'),
   url(r'^registration$', views.Registration.as_view(), name='registration'),
   url(r'^logout$', views.Logout.as_view(), name='logout'),
)
