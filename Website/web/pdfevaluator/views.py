import simplejson as json

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext

from web.pdfevaluator.rule_information import save_ruleset
from web.pdfevaluator.pdf import evaluate_pdf as evaluate
from web.pdfevaluator.models import *

from django.contrib.auth.models import User
from web.pdfevaluator.models import Report, Rule

from web.pdfevaluator.pdf import _save_report as get_json_result
from web.pdfevaluator.file_name_operation import *

@login_required
def index(request):
	return redirect(test+'/')
	#return redirect(request.user.username+'/')

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    reports = Report.objects.filter(user=user)
    return render_to_response('pdfevaluator/profile.html',{'user':user, 'reports':reports, 'currpage_is_profile':True})

@login_required
def save_rule_information(request):
    if request.method == 'POST':
        file = request.FILES['file']
        saved_filepath = default_storage.save('files/rules/'+file.name, file)
        rules_as_json = json.load(default_storage.open(saved_filepath))
        ruleset = save_ruleset(rules_as_json, file.name)
        rules = Rule.objects.select_related()
        
        return render_to_response('pdfevaluator/ruleinformation_upload_complete.html', {'rules': rules})
    else:
        return redirect('/')

@login_required
def evaluate_pdf(request):
    if request.method == 'POST':
        file = request.FILES['file']
        public_form  = request.POST.get('public','True')
        private_report = False
        if public_form is 'False':
            private_report = True
        saved_filepath = default_storage.save('files/pdfs/'+file.name, file)
        ruleset = Ruleset.objects.get(id=1)
        report = evaluate(saved_filepath, file.name, request.user, ruleset)
        report.private = private_report
        report.save()
		
        return redirect('report/'+str(report.id)+'/')
                    #length = int(report_data['TagCount']['length'])
    else:
        return render_to_response('index.html')

@login_required
def evaluate_json(request):
    if request.method == 'POST':
        file = request.FILES['file']
        saved_filepath = default_storage.save('files/json/'+file.name, file)
        rules_as_json = json.load(default_storage.open(saved_filepath))

        ruleset = Ruleset.objects.get(id=1)
        report = get_json_result(file.name,rules_as_json,request.user,ruleset)

        rules_and_results = []
        for rule in Rule.objects.filter(ruleset=ruleset):
            rules_and_results.append(rule)
            rules_and_results.append(Result.objects.filter(rule=rule))

        return render_to_response('pdfevaluator/report.html', {'report':report,'rules_and_results': rules_and_results})
    else:
        return redirect('/')

def get_result(request, result_id):
    report = Report.objects.get(id = result_id)
    ruleset = report.ruleset
    rules_and_results = []
    for rule in Rule.objects.filter(ruleset=ruleset):
        total_pass = Result.objects.filter(rule=rule,report=report,result='P').count()
        total = Result.objects.filter(rule=rule, report=report).count() 
        pass_str = str(total_pass)+'/'+str(total)
        if total == 0:
		    pass_str = 'N/A'

        elif total_pass == total:
            pass_str = '[Pass] '+pass_str
            for result in Result.objects.filter(rule=rule, result='P'):
                pass_str = pass_str+' : '+result.message
                break

        else:
            pass_str = '[Fail] '+pass_str
            for result in Result.objects.filter(rule=rule,report=report,result='V'):
                pass_str = pass_str+' : '+result.message
                break

        rules_and_results.append((rule, pass_str))

    return render_to_response('pdfevaluator/report.html', {'report':report,'rules_and_results': rules_and_results}, context_instance=RequestContext(request))

def get_result_xml(request, result_id):
    report = Report.objects.get(id = result_id)
    path_parts = get_path_parts(report.file_path)
    file = open('/var/www/django/pdfainspector/web/files/pdfs/final-'+path_parts[FilePart.file_name]+'.xml')
    xmlfile = File(file)
    return HttpResponse(file, mimetype='application/xhtml+xml')
