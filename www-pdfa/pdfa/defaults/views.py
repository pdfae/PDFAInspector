# Author: Prateek Arora
# including required modules
from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext
from settings import *
from upload.forms import ContactForm
import inspect
import sys, os, pkgutil
from operator import itemgetter

# about page
def about(request):
	currentPage = "about"
	auth = request.user.is_authenticated()
	sys.path.append(DIR)
	enginePath = os.path.join(DIR, 'RulesEngine')
	sys.path.append(enginePath)
	rulesPath = os.path.join(DIR, 'RulesEngine', 'rules')
	sys.path.append(rulesPath)
	rulesFile = os.path.join(rulesPath, 'core.py')
	rules = []
	rules.append(["Document Level Rules"])
	rules.append(["Rules for Link Tags"])
	rules.append(["Rules for Figure (Image) Tags"])
	rules.append(["Rules for Header Tags"])
	rules.append(["Rules for Table Tags"])
	rules.append(["Rules for Form Controls"])
	rules.append(["Rules for Bookmarks"])
	for i in range(7):
		rules[i].append([])
	print rules
	try:
		import core
		for name, clas in inspect.getmembers(core, inspect.isclass):
			dic = {}
			category = -1
			for key, value in clas.__dict__.iteritems():
				if key == "__doc__":
					dic['description'] = value.strip('\n\t')
				elif key == "applies":
					for name, val in inspect.getmembers(value):
						if name == "__func__":
							dic['Condition'] = inspect.getdoc(val)
				else:
					dic[key] = value
				if key == "category":
					category = int(value)	
			rules[category][1].append(dic)	
		#rules = sorted(rules, key=itemgetter('category'))
		
	except ImportError as e:
		message = "Rules file not found"
	
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
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			cc_myself = form.cleaned_data['cc_myself']
			recipients = ['jongund@illinois.edu']
			if cc_myself:
				recipients.append(sender)
		from django.core.mail import send_mail
		send_mail(subject, message, sender, recipients)
		return HttpResponseRedirect('/thanks/') # Redirect after POST
	else:
		form = ContactForm() # An unbound form
	return render_to_response('defaults/contact.html', locals(), context_instance=RequestContext(request))
