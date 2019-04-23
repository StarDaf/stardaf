from django.conf.urls import url
from . import views
from paystack import views as v
from django.contrib.auth import views as v

app_name='account'

urlpatterns = [
    url(r'^$', views.market, name='market'),
    url(r'^category/(?P<category>[-\w]+)/$', views.market, name='market_category'),
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
    url(r'^user-follow/$', views.follow, name='follow'),
    url(r'^home/$', views.stream, name='stream'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.market,name='post_list_by_tag'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^terms-and-conditions/$', views.terms, name='term'),
    url(r'^contact-us/$', views.contact, name='contact'),
    url(r'^success/$', views.success, name='success'),
    url(r'^failure/$', views.failure, name='failure'),
    url(r'^(?P<username>[-\w]+)/$', views.profile, name='profile'),
    #url(r'^(?P<business_name>[-\w]+)/', views.profile1, name='profile1'),
    url(r'^filter/(?P<market>[-\w]+)/$', views.filter_shops, name='filter'),
    url(r'^favourites/(?P<user_id>\d+)/$', views.favourites, name='favourites'),
    url(r'^market/(?P<market>[-\w]+)/$', views.filter_shops, name='farmcenter'),
    url(r'(?P<username>[-\w]+)/followers/', views.followers, name='followers'),
    url(r'(?P<username>[-\w]+)/following/', views.following, name='following'),
    url(r'self-delete/(?P<admin_id>\d+)/', views.self_delete, name='delete'),
                                                       
]


