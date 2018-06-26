from django.conf.urls import url

from . import views


app_name = 'toptran'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    
    url(r'^news$', views.NewsView.as_view(), name='news'),
    url(r'^news/(?P<pk>[0-9]+)/$', views.newsdetail, name='newsdetail'),

    url(r'^knowledge$', views.KnowledgeView.as_view(), name='knowledge'),
    url(r'^knowledge/(?P<pk>[0-9]+)/$', views.knowledgedetail, name='knowledgedetail'),

    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    url(r'^case$', views.CaseView.as_view(), name='case'),
    url(r'^product$', views.product_list, name='product_list'),
    url(r'^product/(?P<category_slug>[-\w]+)/$',views.product_list,name='product_list_by_category'),
    url(r'^product/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.product_detail,name='product_detail'),
    
]

