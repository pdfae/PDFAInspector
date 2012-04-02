from django.core.files.base import ContentFile
from django.shortcuts import HttpResponseRedirect, render_to_response, RequestContext
import uuid
import subprocess
from settings import MEDIA_ROOT, PDF_JAR, PYTHON_SCRIPT, PROCESS_SCRIPT
from forms import uploadfileform, ContactForm
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

def contact (request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            if form.is_valid():
    		subject = form.cleaned_data['subject']
    		message = form.cleaned_data['message']
    		sender = form.cleaned_data['sender']
    		cc_myself = form.cleaned_data['cc_myself']
    		recipients = ['atul.guptey@gmail.com']
    		if cc_myself:
        		recipients.append(sender)
    	from django.core.mail import send_mail
    	send_mail(subject, message, sender, recipients)
    	return HttpResponseRedirect('/thanks/') # Redirect after POST
    
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })

def process_file(filename):
	[filepath, filename] = filename.rsplit('/', 1)
	subprocess.Popen(["python", PROCESS_SCRIPT, "\""+PDF_JAR+"\"","\""+PYTHON_SCRIPT+"\"","\""+MEDIA_ROOT+filepath+"/\"","\""+filename+"\""])