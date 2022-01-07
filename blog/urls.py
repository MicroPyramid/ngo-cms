from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.post_list),
    path('events/', views.event_list),
    path('contact-us/', views.contact_us),
    path('rss.xml', views.rss),
    path('sitemap/', views.sitemap),
    path('donations/', views.donations),
    path('employment/', views.employment),
    path('financial_information/', views.financial_information),
    re_path('events/(?P<slug>[a-zA-Z0-9._+-]+)/',
            views.event_detail, name='event_detail'),
    re_path('news/(?P<slug>[a-zA-Z0-9._+-]+)/details/',
            views.post_detail, name='post_detail'),
    re_path('news/category/(?P<slug>[a-zA-Z0-9._+-]+)/', views.category_posts),
    re_path('news/archives/(?P<year>[0-9_-]+)/(?P<month>[0-9_-]+)',
            views.archive_posts),
    re_path('page/(?P<slug>[a-zA-Z0-9._+-]+)/display/', views.page_display),
]
