import json

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,redirect

from web.pdfevaluator.rule_information import save_ruleset
from web.pdfevaluator.pdfe import evaluate_pdf

from django.contrib.auth.models import User
from web.pdfevaluator.models import Report, Rule

@login_required
def index(request):
	print "Index?"
	return redirect(request.user.username+'/')

@login_required
def profile(request, username):
	print "profile?"

	#user = User.objects.get(username=username)
	user = request.user
	return render_to_response('pdfevaluator/profile.html',{'user':user})

@login_required
def save_rule_information(request):
	if request.method == 'POST':
		file = request.FILES['file']
		saved_filepath = default_storage.save('files/rules/'+file.name, file)
		print "in here!"
		rules_as_json = json.load(default_storage.open(saved_filepath))
		ruleset = save_ruleset(rules_as_json)

		rules = Rule.objects.select_related()
		#default_storage.delete(saved_filepath)

		return render_to_response('pdfevaluator/ruleinformation_upload_complete.html', {'rules': rules})
	else:
		return redirect(request.user.username+'/')

@login_required
def evaluate_pdf(request):
	if request.method == 'POST':
		pdf = request.FILES['pdf_file']
		pdf_path = default_stroage.save('files/rules/'+pdf.name, pdf)
		report = evaluate_pdf(pdf_path, request.user)
		
		redirect_location = 'report/'+report.id+'/'
		return redirect(redirect_location, request.user)
