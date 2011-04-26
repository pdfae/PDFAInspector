from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('web.registration.urls')),
    url(r'^pdf/', include('web.pdfevaluator.urls')),
	url(r'^about/$', direct_to_template,{'template':'pdfevaluator/about.html',
        'extra_context':{'currpage_is_about':True,}}),
	url(r'^run_inspector/$', direct_to_template,{'template':'pdfevaluator/run_inspector.html',
        'extra_context':{'currpage_is_run_inspector':True,}}),
	url(r'^(?P<username>\w+)/reports/$', 'web.pdfevaluator.views.profile'),
	url(r'^(?P<username>\w+)/$', 'web.pdfevaluator.views.profile'),
    #url(r'^', include('web.pdfevaluator.urls')),
	url(r'^$', direct_to_template,{'template':'index.html', 
        'extra_context':{'currpage_is_home':True,}}),
	#url(r'',
	#	auth_views.login, {'template_name': 'index.html'},
	#	name='auth_login'),
)
