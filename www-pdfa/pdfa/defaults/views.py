# Author: Prateek Arora
# including required modules
from django.shortcuts import *
from settings import *

# homepage
def home(request):
	currentPage = "home"
	if request.user.is_authenticated():
		auth = 'true'
	else:
		auth = 'false'
	return render_to_response("defaults/index.html", locals())
	
# about page
def about(request):
	currentPage = "about"
	if request.user.is_authenticated():
		auth = 'true'
	else:
		auth = 'false'
	return render_to_response("defaults/about.html", locals())