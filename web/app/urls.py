from django.conf.urls.defaults import *

urlpatterns = patterns('app.views',
        (r'^upload_file','genReport'),
        (r'^success','success'),
        (r'^report/(?P<reportID>\d+)','renderReport'),
        (r'$','index'),

)
