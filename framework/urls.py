from django.conf import settings
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^$', include('core.urls')),
                       url(r'', include('contact.urls')),
                       url(r'^forum/', include('forum.urls')),
                       url(r'^profil/', include('profil.urls')),
                       url(r'^issue/', include('issues.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^i18n/', include('django.conf.urls.i18n')),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
