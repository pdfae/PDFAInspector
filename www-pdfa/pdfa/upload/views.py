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
				unid = unicode(uuid.uuid4())
				filename = unid + ".pdf"
				filepath = MEDIA_ROOT + "public/"
				if auth:
					filepath = request.user.get_profile().filepath
				fileObj = UserFile(uid = unid, owner = request.user.username, title = data['title'], notes = data['notes'])
				fileObj.file.save(filename, ContentFile(request.FILES['file'].read()))
				fileObj.save()
				process_file(filename, filepath)
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


def process_file(filename, filepath):
	print filepath + filename
	subprocess.Popen(["python2.7", PROCESS_SCRIPT, filepath + filename])
	#subprocess.Popen(["python2.7", PROCESS_SCRIPT, "\""+PDF_JAR+"\"","\""+PYTHON_SCRIPT+"\"","\""+MEDIA_ROOT+filepath+"/\"","\""+filename+"\""])