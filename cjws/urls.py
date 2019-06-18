from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from blogapp import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    path('admin/', include('adminapp.urls')),
    path('', include('blogapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.handler404
handler500 = views.handler500
