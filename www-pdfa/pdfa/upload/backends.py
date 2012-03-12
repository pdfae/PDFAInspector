from django.shortcuts import *
from forms import uploadfileform
from settings import MEDIA_ROOT, PDF_JAR, PYTHON_SCRIPT, PROCESS_SCRIPT
from django.contrib.auth.decorators import login_required
import string as string
import os
import subprocess
from models import UserFile
from django.core.files.base import ContentFile

def handle_file_form(request, auth, currentPage):
	if (request.method=="POST"):
		filename = str(request.FILES['file'])
		if (filename.endswith('.pdf')):
			form = uploadfileform(request.POST, request.FILES)
			if form.is_valid():
				#u = request.user
				'''
				u = UserFile(owner = request.user.username)
				u.filename.save(request.FILES['file'].name, ContentFile(request.FILES['file'].read()))
				u.save()
				'''
				
				handle_uploaded_file(request.FILES['file'], request.user)
				process_file(request.FILES['file'], request.user)
				if request.user.is_authenticated():
					return HttpResponseRedirect('/accounts/profile/managereports/')
				else:
					file = str(request.FILES['file'])
					return render_to_response('upload/processing.html', locals())
		else:
			message = "Not a PDF file"
			form = uploadfileform()
			return render_to_response("upload/fileupload.htm", locals(), context_instance=RequestContext(request))
	else:
		form = uploadfileform()
		return render_to_response("upload/fileupload.htm", locals(), context_instance=RequestContext(request))

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
	if user.is_authenticated():
		filepath = user.get_profile().filepath
	else:
		filepath = MEDIA_ROOT + 'public/'
	subprocess.Popen(["python", PROCESS_SCRIPT, "\""+PDF_JAR+"\"","\""+PYTHON_SCRIPT+"\"","\""+filepath+"\"","\""+filename+"\""])