from backends import handle_file_form

def upload (request):
	currentPage = "upload"
	if request.user.is_authenticated():
		auth = 'true'
		base = 'userprofile/profile_base.html'
	else:
		auth = 'false'
		base = 'base.html'
	return handle_file_form(request, base, auth, currentPage)
