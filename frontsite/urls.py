from django.conf.urls import patterns, url, include
from frontsite import views
from django.contrib.auth.views import logout

urlpatterns = patterns('',
   #url(r'^$', views.Index.as_view(), name='index'),
   url(r'^$', views.Rhyme.as_view(), name='index'),
   url(r'^most-popular/$', views.most_popular, name='popular'),
   url(r'^random/$', views.random, name='random'),
   url(r'^stored/$', views.stored, name='stored'),
   url(r'^rhyme-store/(?P<id>\d+)$', views.rhyme_store, name='rhyme-store'),
   url(r'^rhyme-unstore/(?P<id>\d+)$', views.rhyme_unstore, name='rhyme-unstore'),
   url(r'^rhyme/(?P<id>\d+)/(?P<delete>\w+)?$', views.Rhyme.as_view(), name='rhyme_detail'),
   url(r'^vote-rhyme/(?P<rhyme_id>\d+)$', views.vote_rhyme, name='vote-rhyme'),
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
