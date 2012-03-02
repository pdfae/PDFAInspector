# Author: Prateek Arora
# including required modules
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from settings import *
from django.contrib.auth.decorators import login_required
import os, re
from forms import userChangeForm

# profile homepage
@login_required
def profile(request):
	auth = 'true'
	currentPTab = "info"
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
	auth = 'true'
	currentPTab = "reports"
	user = request.user
	file_list = os.listdir(user.get_profile().filepath)
	regex = re.compile('json-.*.json')
	json_file_list = []
	for f in file_list:
		if regex.match(f):
			f = f.replace('json-', '')
			f = f.replace('.json', '') + ".pdf"
			json_file_list.append(f)
	return render_to_response("userprofile/reports.html", locals())

# manage rules
@login_required
def managerules(request):
	auth = 'true'
	currentPTab = "rules"
	return render_to_response("userprofile/rules.html", locals())
	
@login_required
def change(request):
	auth = 'true'
	currentPTab = "info"
	if (request.method=="POST"):
		form = userChangeForm(request.POST)
		if form.is_valid():
			request.user.first_name = form.cleaned_data['first_name']
			request.user.last_name = form.cleaned_data['last_name']
			request.user.email = form.cleaned_data['email']
			request.user.save()
			return HttpResponseRedirect('/accounts/profile/')
	else:
		form = userChangeForm()
		return render_to_response("userprofile/change.html", locals(), context_instance=RequestContext(request))
