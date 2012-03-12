from django.conf.urls.defaults import patterns, include, url
from upload.views import upload
from views import *

urlpatterns = patterns('',
    (r'^managereports', managereports),
    (r'^managerules', managerules),
    (r'^managerules', managerules),
    (r'^accountinfo', profile),
    (r'^change', change),
	(r'', upload),
    
)
