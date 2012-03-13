from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
	(r'^treeview/', displaytreeview),
	(r'^imageview/', displayimages),
	(r'^headview/', displayheaders),
	(r'^formview/', displayforms),
	(r'^tableview/', displaytables),
    (r'^linkview/', displaylinks),
    (r'^bookmarkview/', displaybookmark),
    (r'', displaysummary),
)
