from django.shortcuts import *
from forms import uploadfileform
from settings import MEDIA_ROOT
from backends import handle_file_form

def upload (request):
	currentPage = "upload"
	if request.user.is_authenticated():
		auth = 'true'
		template_get = "upload/user_fileupload.html"
		template_post = "userprofile/reports.html"
	else:
		auth = 'false'
		template_get = "upload/fileupload.htm"
		template_post = "upload/processing.html"
	return handle_file_form(request, template_get, template_post, auth)
