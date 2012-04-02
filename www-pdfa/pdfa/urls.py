from django.conf.urls.defaults import patterns, include, url

from defaults.views import about, contact

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    #Reports
    (r'^reports/(?P<uid>[\w -]+)/', include('reports.urls')),
    
    #User Profiles
	(r'^accounts/profile/', include('userprofile.urls')),
	
    #Registration
    (r'^accounts/', include('registration.urls')),
    (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/'}),
    (r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
    

    #File Upload
    (r'^upload/', include('upload.urls')),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    
    # Defaults:
    (r'^about', about),
    (r'^contact/', contact),
    #(r'^contact', contact),
    #(r'', home),
    (r'', include('upload.urls')),
    
)
