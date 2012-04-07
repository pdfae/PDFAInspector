# Author: Prateek Arora
# including required modules
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from settings import *
from django.contrib.auth.decorators import login_required
import os, re
from forms import userChangeForm
from upload.models import UserFile

# profile homepage
@login_required
def profile(request):
	auth = True
	currentPage = "account"
	username = request.user.username
	first_name = request.user.first_name
	last_name = request.user.last_name
	email = request.user.email
	last_login = request.user.last_login
	date_joined = request.user.date_joined
	return render_to_response("userprofile/profile.html", locals())

# manage reports
@login_required
def managereports(request):
	auth = True
	currentPage = "reports"
	user = request.user
	file_list = UserFile.objects.filter(owner = user.username)
	if (request.method=="POST"):
		x=request.POST
	return render_to_response("userprofile/reports.html", locals(), context_instance=RequestContext(request))

# manage rules
@login_required
def managerules(request):
	auth = True
	currentPTab = "rules"
	return render_to_response("userprofile/rules.html", locals())
	
@login_required
def change(request):
	auth = True
	currentPage = "account"
	if (request.method=="POST"):
		form = userChangeForm(request.POST, initial={'e-mail': request.user.email})
		if form.is_valid():
			request.user.first_name = form.cleaned_data['first_name']
			request.user.last_name = form.cleaned_data['last_name']
			request.user.email = form.cleaned_data['email']
			request.user.save()
			return HttpResponseRedirect('/accounts/profile/accountinfo')
	else:
		data = {'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email}
		form = userChangeForm(data)
		return render_to_response("userprofile/change.html", locals(), context_instance=RequestContext(request))
