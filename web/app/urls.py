from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from app.forms import RulesForm

forms = {
        "rules":RulesForm(),
        }

urlpatterns = patterns('app.views',
        (r'^upload_file','genReport'),
        (r'^success','success'),
        (r'^report/(?P<reportID>\d+)','renderReport'),
        (r'^upload_rule',direct_to_template,
            {'template':'app/upload_rules.html','extra_context':forms}),
        (r'^save_rules','readRulesetFile'),
        (r'$','index'),

)
