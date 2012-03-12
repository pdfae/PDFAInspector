from django.core.files.base import ContentFile
from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
import uuid
import subprocess
from settings import MEDIA_ROOT, PDF_JAR, PYTHON_SCRIPT, PROCESS_SCRIPT
from forms import uploadfileform
from models import UserFile

def upload (request):
	currentPage = "upload"
	auth = request.user.is_authenticated()
	if (request.method=="POST"):
		filename = request.FILES['file'].name
		if (filename.endswith('.pdf')):
			form = uploadfileform(request.POST, request.FILES)
			if form.is_valid():
				data = form.cleaned_data
				if (data['title'] == ''):
					data['title'] = "Report for " + filename
				fileObj = UserFile(uid = unicode(uuid.uuid4()), owner = request.user.username, title = data['title'], notes = data['notes'])
				fileObj.file.save(request.FILES['file'].name, ContentFile(request.FILES['file'].read()))
				fileObj.save()
				process_file(fileObj.file.name)
				return HttpResponseRedirect('/accounts/profile/managereports/')
		else:
			message = "Not a PDF file"
	form = uploadfileform()
	return render_to_response("upload/fileupload.htm", locals(), context_instance=RequestContext(request))

def process_file(filename):
	[filepath, filename] = filename.rsplit('/', 1)
	subprocess.Popen(["python", PROCESS_SCRIPT, "\""+PDF_JAR+"\"","\""+PYTHON_SCRIPT+"\"","\""+MEDIA_ROOT+filepath+"/\"","\""+filename+"\""])