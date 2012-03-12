# Author: Prateek Arora
# including required modules
from django.shortcuts import *
from settings import *

# homepage
def home(request):
	currentPage = "home"
	if request.user.is_authenticated():
		auth = 'true'
		base = 'userprofile/profile_base.html'
	else:
		auth = 'false'
		base = 'base.html'
	return render_to_response("uploads/fileupload.html", locals())
	
# about page
def about(request):
	currentPage = "about"
	if request.user.is_authenticated():
		auth = 'true'
		base = 'userprofile/profile_base.html'
	else:
		auth = 'false'
		base = 'base.html'
	return render_to_response("defaults/about.html", locals())

# contact page
def contact(request):
	currentPage = "contact"
	if request.user.is_authenticated():
		auth = 'true'
		base = 'userprofile/profile_base.html'
	else:
		auth = 'false'
		base = 'base.html'
	return render_to_response("defaults/contact.html", locals())
