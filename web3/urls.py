from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    #url(r'^accounts/', include('registration.urls')),
    url(r'^pdf/', include('web.pdfevaluator.urls')),
    url(r'^', include('web.pdfevaluator.urls')),
	#url(r'',
	#	auth_views.login, {'template_name': 'index.html'},
	#	name='auth_login'),
)
