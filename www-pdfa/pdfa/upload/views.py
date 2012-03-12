from backends import handle_file_form

def upload (request):
	currentPage = "upload"
	auth = request.user.is_authenticated()
	return handle_file_form(request, auth, currentPage)
