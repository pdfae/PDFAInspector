from django.shortcuts import *
from forms import uploadfileform
from settings import MEDIA_ROOT, PDF_JAR
from django.contrib.auth.decorators import login_required
import os

def handle_file_form(request, template_get, template_post, auth):
	if (request.method=="POST"):
		print "in upload section"
		form = uploadfileform(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'], request.user)
			process_file(request.FILES['file'], request.user)
			return render_to_response(template_post, locals(), context_instance=RequestContext(request))
	else:
		form = uploadfileform()
		return render_to_response(template_get, locals(), context_instance=RequestContext(request))

def handle_uploaded_file(filename, user):
	if user.is_authenticated():
		print filename
		destination = open(user.get_profile().filepath + str(filename), 'wb+')
	else:
		destination = open(MEDIA_ROOT + 'public/' + str(filename), 'wb+')
	for chunk in filename.chunks():
		destination.write(chunk)
	destination.close()

def process_file(file, user):
	if user.is_authenticated():
		command1 = "java -jar "+ PDF_JAR + " " + user.get_profile().filepath + str(file)
		command2 = "rm " + user.get_profile().filepath + str(file)
		# command3 = "python2.7 "+ PYTHON_SCRIPT + user.get_profile().filepath + <json file> + " > " + user.get_profile().filepath + <results file>
		
	else:
		command1 = "java -jar "+ PDF_JAR + " " + MEDIA_ROOT + 'public/' + str(file)
		command2 = "rm " + MEDIA_ROOT + 'public/' + str(file)
		# command3 = "python2.7 "+ PYTHON_SCRIPT + user.get_profile().filepath + <json file> + " > " + user.get_profile().filepath + <results file>
	print command1
	print command2
	os.system(command1)
	os.system(command2)