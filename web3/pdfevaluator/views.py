import simplejson as json

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,redirect

from web.pdfevaluator.rule_information import save_ruleset
from web.pdfevaluator.pdf import evaluate_pdf as evaluate

from django.contrib.auth.models import User
from web.pdfevaluator.models import Report, Rule

#@login_required
def index(request):
	return redirect(test+'/')
	#return redirect(request.user.username+'/')

#@login_required
def profile(request, username):
	user = User.objects.get(username=username)
	user = request.user
	return render_to_response('pdfevaluator/profile.html',{'user':user})

#@login_required
def save_rule_information(request):
	if request.method == 'POST':
		file = request.FILES['file']
		saved_filepath = default_storage.save('web/files/rules/'+file.name, file)

		rules_as_json = json.load(default_storage.open(saved_filepath))
		ruleset = save_ruleset(rules_as_json, file.name)

		rules = Rule.objects.select_related()

		return render_to_response('pdfevaluator/ruleinformation_upload_complete.html', {'rules': rules})
	else:
		return redirect('/')

#@login_required
def evaluate_pdf(request):
	if request.method == 'POST':
		file = request.FILES['file']
		saved_filepath = default_storage.save('web/files/pdfs/'+file.name, file)
		report = evaluate(saved_filepath, file.name, request.user)
		
	#	redirect_location = 'report/'+report.id+'/'
		#return render_to_response('pdfevaluator/results.html', {'report':report})
		return redirect('hi/'+report)

	else:
		return render_to_response('index.html')

#@login_required
def get_result(request, result_id):
	return render_to_response('pdfevaluator/results.html', {'report':result_id})
