from django.shortcuts import *
from forms import uploadfileform
from settings import MEDIA_ROOT, PDF_JAR, PYTHON_SCRIPT
from django.contrib.auth.decorators import login_required
import string as string
import os

def handle_file_form(request, template_get, template_post, auth):
	if (request.method=="POST"):
		filename = str(request.FILES['file'])
		if (filename.endswith('.pdf')):
			form = uploadfileform(request.POST, request.FILES)
			if form.is_valid():
				handle_uploaded_file(request.FILES['file'], request.user)
				process_file(request.FILES['file'], request.user)
				if request.user.is_authenticated():
					return HttpResponseRedirect('/accounts/profile/managereports/')
				else:
					file = str(request.FILES['file'])
					return HttpResponseRedirect('/accounts/profile/reports/?f=' + file)
		else:
			message = "Not a PDF file"
			form = uploadfileform()
			return render_to_response(template_get, locals(), context_instance=RequestContext(request))
	else:
		form = uploadfileform()
		return render_to_response(template_get, locals(), context_instance=RequestContext(request))

def handle_uploaded_file(filename, user):
	if user.is_authenticated():
		#print filename
		destination = open(user.get_profile().filepath + str(filename), 'wb+')
	else:
		destination = open(MEDIA_ROOT + 'public/' + str(filename), 'wb+')
	for chunk in filename.chunks():
		destination.write(chunk)
	destination.close()

def process_file(file, user):
	filename = str(file)
	parse_file = "json-" + filename.rpartition('.pdf')[0] + ".json"
	result_file = "result-" + filename.rpartition('.pdf')[0] + ".json"
	if user.is_authenticated():
		filepath = user.get_profile().filepath
	else:
		filepath = MEDIA_ROOT + 'public/'	
	command1 = "java -jar "+ PDF_JAR + " " + filepath + filename
	command2 = "rm " + filepath + filename
	command3 = "python2.7 "+ PYTHON_SCRIPT + " " + filepath + parse_file + " > " + filepath + result_file
	os.system(command1)
	os.system(command2)
	os.system(command3)