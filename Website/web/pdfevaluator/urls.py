from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('web.pdfevaluator.views',

	#url(r'^upload_ruleinformation/$', direct_to_template,{'template':'pdfevaluator/ruleinformation_upload.html'}),
	url(r'^save_rule_information/$', 'save_rule_information'),
	url(r'^evaluate_pdf/$', 'evaluate_pdf'),
	url(r'^evaluate_json/$', 'evaluate_json'),
	url(r'^report/(?P<result_id>\w+)/xml/$', 'get_result_xml'),
	url(r'^report/(?P<result_id>\w+)/$', 'get_result'),
	#url(r'^(?P<username>\w+)/$', 'profile'),
	#url(r'^/$', 'index'),
		
)
