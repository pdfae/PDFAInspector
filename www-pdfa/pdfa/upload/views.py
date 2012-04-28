# Author: Prateek Arora

from django.core.files.base import ContentFile
from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
import uuid
import subprocess
from settings import MEDIA_ROOT, PDF_JAR, PYTHON_SCRIPT, PROCESS_SCRIPT
from forms import uploadfileform
from models import UserFile

# Function: upload
#
# This function is called when the user wants to upload a file for evaluation.
#

def upload (request):
	currentPage = "upload"
	auth = request.user.is_authenticated()
	if (request.method=="POST"):	# If the form has been submitted...
		filename = request.FILES['file'].name
		if (filename.endswith('.pdf')):	# allow users to only upload pdf files
			form = uploadfileform(request.POST, request.FILES) # A form bound to the POST data
			if form.is_valid():	# All validation rules pass
				data = form.cleaned_data
				# generate default report title if not specified by user
				if (data['title'] == ''):
					data['title'] = "Report for " + filename
				unid = unicode(uuid.uuid4())
				filename = unid + ".pdf"
				filepath = MEDIA_ROOT + "public/"
				# if user has logged in, save uploaded file to user's folder
				if auth:
					filepath = request.user.get_profile().filepath
				fileObj = UserFile(uid = unid, owner = request.user.username, title = data['title'], notes = data['notes'])
				fileObj.file.save(filename, ContentFile(request.FILES['file'].read()))
				fileObj.save()
				process_file(filename, filepath) #	call function to run evaluator on uploaded file
				if auth:
					user = request.user.get_profile()
					user.filecount = user.filecount + 1
					user.save()
					return HttpResponseRedirect('/accounts/profile/managereports/')
				else:
					return render_to_response("upload/processing.html", {"uid": fileObj.uid})
		else:
			message = "Not a PDF file"
	form = uploadfileform()
	return render_to_response("upload/fileupload.htm", locals(), context_instance=RequestContext(request))

# Function: process_file
#
# This function is called once the file upload is complete. It runs the evaluation script on the uploaded file.
#

def process_file(filename, filepath):
	print filepath + filename
	subprocess.Popen(["python2.7", PROCESS_SCRIPT, filepath + filename])