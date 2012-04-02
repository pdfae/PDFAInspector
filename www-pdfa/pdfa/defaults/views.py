# Author: Prateek Arora
# including required modules
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from settings import *
from upload.forms import ContactForm
	
# about page
def about(request):
	currentPage = "about"
	auth = request.user.is_authenticated()
	print auth
	return render_to_response("defaults/about.html", locals())

# contact page
#def contact(request):
#	currentPage = "contact"
#	auth = request.user.is_authenticated()
#	return render_to_response("defaults/contact.html", locals())
	
def contact (request):
    currentPage = "contact"
    auth = request.user.is_authenticated()
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

    return render_to_response('defaults/contact.html', locals(), context_instance=RequestContext(request))
