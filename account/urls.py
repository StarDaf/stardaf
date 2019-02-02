from django.conf.urls import url
from . import views
from django.contrib.auth import views as v

app_name='account'

urlpatterns = [
    url(r'^$', views.stream, name='stream'),
    url(r'^sign-in/', v.login, name='login'),
    url(r'^sign-out/', v.logout, name='logout'),
    url(r'^logout-then-login/$', v.logout_then_login, name='logout_then_login'),
    url(r'^password-change/$', v.password_change, {'post_change_redirect' : 'account:password_change_done'}, name='password_change'),
    url(r'^password-change/done/$', v.password_change_done, name='password_change_done'),
    url(r'^password-reset/$', v.password_reset, {'post_reset_redirect':'account:password_reset_done'}, name='password_reset'),
    url(r'^password-reset/done$', v.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', v.password_reset_confirm, {'post_reset_redirect':'account:login'} ,name='password_reset_confirm'),
    url(r'^password-reset/complete/$', v.password_reset_complete, name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/(?P<user_id>\d+)/(?P<username>[-\w]+)/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^user-follow/$', views.follow, name='follow'),
    url(r'^market/$', views.market, name='market'),
    url(r'^filter/(?P<market>[-\w]+)/$', views.filter_shops, name='filter'),
    url(r'^favourites/(?P<user_id>\d+)/$', views.favourites, name='favourites'),
    url(r'^(?P<market>[-\w]+)/$', views.filter_shops, name='farmcenter'),
    url(r'(?P<username>[-\w]+)/followers/', views.followers, name='followers'),
    url(r'(?P<username>[-\w]+)/following/', views.following, name='following'),
                                                     

]


