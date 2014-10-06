from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^ahrm/', include('ahrm.foo.urls')),

    (r'^', include('ahrm.main.urls')),
    (r'^system/help$', 'main.views.help'),
    #static content path (js, css...)
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root':settings.MEDIA_ROOT}),
                      
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^i18n/', include('django.conf.urls.i18n')),

)
