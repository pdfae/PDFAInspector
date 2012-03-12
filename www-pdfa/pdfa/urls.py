from django.conf.urls.defaults import patterns, include, url

from defaults.views import about, contact

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    #Reports
    (r'^accounts/profile/reports/', include('reports.urls')),
    
    #User Profiles
	(r'^accounts/profile/', include('userprofile.urls')),
	
    #Registration
    (r'^accounts/', include('registration.urls')),

    #File Upload
    (r'^upload/', include('upload.urls')),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Defaults:
    (r'^about', about),
    (r'^contact', contact),
    #(r'', home),
    (r'', include('upload.urls')),
    
)
