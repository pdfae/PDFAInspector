from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
	(r'^treeview/', displaytreeview),
	(r'^figureview/', displayfigures),
	(r'^formview/', displayforms),
	(r'^tableview/', displaytables),
    (r'^linkview/', displaylinks),
    (r'^headview/', displayhead),
    (r'^bookmarkview/', displaybookmark),
    (r'^emptyview/', displayempty),
    (r'^formtreeview/', displayformtree),
    (r'', displaysummary),
)
