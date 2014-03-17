from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dagew.views.home', name='home'),
    # url(r'^dagew/', include('dagew.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$','blog.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$','blog.views.index'),
    url(r'^regist/$','blog.views.regist'),
    url(r'^regist_1/$','blog.views.regist_1'),
    url(r'^login/$','blog.views.user_login'),
    url(r'^logout/$','blog.views.user_logout'),
    url(r'^restaurant/$','blog.views.restaurant'),
    url(r'^dingcan/$','blog.views.dingcan'),
    url(r'^zhinan/$','blog.views.zhinan'),
    url(r'^user/$','blog.views.show_user'),
    url(r'^jifen/$','blog.views.jifen'),
    url(r'^notice/$','blog.views.notice'),
    url(r'^women/$','blog.views.women'),
    url(r'^zhaopin/$','blog.views.zhaopin'),
    url(r'^duihuan/$','blog.views.duihuan'),
    url(r'^guize/$','blog.views.guize'),
    url(r'^update/$','blog.views.update'),
    url(r'^update_mima/$','blog.views.update_mima'),
    url(r'^order/$','blog.views.order'),
    url(r'^order_select/$','blog.views.order_select'),
)
