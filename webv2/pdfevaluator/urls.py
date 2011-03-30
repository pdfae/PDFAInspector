from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('web.pdfevaluator.views',

	url(r'^upload_ruleinformation/$', direct_to_template,{'template':'pdfevaluator/ruleinformation_upload.html'}),
	url(r'^save_ruleinformation/$', 'save_rule_information'),
	url(r'^(?P<username>\w+)/$', 'profile'),
	url(r'^$', 'index'),
		
)
