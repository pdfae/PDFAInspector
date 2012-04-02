from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
	(r'^treeview/', displaytreeview),
	(r'^figureview/', displayfigures),
	(r'^formview/', displayforms),
	(r'^tableview/', displaytables),
    (r'^linkview/', displaylinks),
    (r'^bookmarkview/', displaybookmark),
    (r'^formtreeview/', displayformtree),
    (r'', displaysummary),
)
