from django.conf.urls.defaults import patterns, include, url
from myapp.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', home),
	(r'^user/$', signup),
	(r'^contact/$', contact),
	(r'^upload/$', upload),
	(r'^about/$', about),
	(r'^view/$', view),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
