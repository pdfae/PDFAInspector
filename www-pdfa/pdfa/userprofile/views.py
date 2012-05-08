# Author: Prateek Arora, Atul Gupte

# including required modules
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from settings import *
from django.contrib.auth.decorators import login_required
import os, re
from forms import userChangeForm
from upload.models import UserFile
from django.core.files import File

# Function: profile
#
# This function, when called, renders the user-profile.
#


@login_required		# This ensures that only authenticated users can access this function
def profile(request):
	auth = True
	currentPage = "account"
	user = request.user
	return render_to_response("userprofile/profile.html", locals())

# Function: managereports
#
# This function lists all of the user's available reports, and allows users 
# to delete selected reports.
#

@login_required
def managereports(request):
	auth = True
	currentPage = "reports"
	user = request.user
	file_list = UserFile.objects.filter(owner = user.username).order_by('-date')
	if (request.method=="POST"): # if checkboxes have been selected and 'delete' has been hit
		formdata=request.POST
		for f in file_list:
			if len(formdata.getlist(f.uid))>0:
				# obtain filepaths of all related files (json/xml)
				fname = (unicode(f.file.name).split('/')[1]).rstrip('.pdf')
				fp = request.user.get_profile().filepath
				xml_file = fp+"xml-"+fname+".xml"
				json_file = fp+"json-"+fname+".json"
				result_file = fp+"result-"+fname+".json"
				if os.path.isfile(xml_file):
					os.remove(xml_file)	
				if os.path.isfile(json_file):
					os.remove(json_file)
				if os.path.isfile(result_file):
					os.remove(result_file)
				f.delete() # delete all associated files when user selects a report to delete
	file_list = UserFile.objects.filter(owner = user.username).order_by('-date')
	return render_to_response("userprofile/reports.html", locals(), context_instance=RequestContext(request))

# manage rules
@login_required
def managerules(request):
	auth = True
	currentPTab = "rules"
	return render_to_response("userprofile/rules.html", locals())
	
# Function: change
#
# This function, when called, allows a user to change account settings.
#

@login_required
def change(request):
	auth = True
	currentPage = "account"
	if (request.method=="POST"): # if the user action is 'submit'
		form = userChangeForm(request.POST, initial={'e-mail': request.user.email})
		if form.is_valid():
			request.user.first_name = form.cleaned_data['first_name']
			request.user.last_name = form.cleaned_data['last_name']
			request.user.email = form.cleaned_data['email']
			request.user.save()
			return HttpResponseRedirect('/accounts/profile/accountinfo')
	else:
		# display form with pre-filled data
		data = {'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email}
		form = userChangeForm(data)
		return render_to_response("userprofile/change.html", locals(), context_instance=RequestContext(request))
