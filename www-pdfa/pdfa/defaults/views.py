# Author: Prateek Arora
# including required modules
from django.shortcuts import render_to_response
from settings import *
	
# about page
def about(request):
	currentPage = "about"
	auth = request.user.is_authenticated()
	print auth
	return render_to_response("defaults/about.html", locals())

# contact page
def contact(request):
	currentPage = "contact"
	auth = request.user.is_authenticated()
	return render_to_response("defaults/contact.html", locals())
