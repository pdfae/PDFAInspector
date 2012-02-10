from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
    (r'^managereports/', managereports),
    (r'^managerules/', managerules),
    (r'^change/', change),
	(r'', profile),
    
)
