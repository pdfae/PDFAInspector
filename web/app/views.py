from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from app.forms import UploadFileForm
from app.forms import RulesForm
from app.models import *
from app.rules import saveRuleset
from app.resultProcessing import saveResults
from app.resultProcessing import getReportWithNestedResults
from app.utilities import *

from registration.forms import RegistrationForm

import json
import os
import re

#remove the next three lines and the about_pages stuff
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template

def index(request):
#    form = UploadFileForm()
#    return render_to_response('app/index.html',{'uploadForm':form},
#            context_instance=RequestContext(request))
    loginForm = RegistrationForm()
    uploadForm = UploadFileForm()

    return render_to_response('app/index.html',{'uploadForm':uploadForm,\
            'loginForm':loginForm})

@login_required
def genReport(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            #get information from form
            file = request.FILES['file']
            user = request.user
            rulesetID = int(request.POST['ruleset'])
            ruleset = Ruleset.objects.get(id=rulesetID)

            #generate a random url
            url = genURL()

            #save a new report to database
            report = Report(url=url,user=user,ruleset=ruleset)
            report.save()

            #parse the pdf into a json object
            jresult = parsePDF(file, ruleset, report)

            #save json information to database
            saveResults(jresult, report)

            results = getReportWithNestedResults(report)

            return render_to_response('app/report.html',\
                    {'report':report,'ruleset':results})
    else:
        form = UploadFileForm()
    return render_to_response('index.html',{'uploadForm': form})


def genURL():
    '''
Generates a random key for the report
'''
    #TODO: make this actually work..
    url = "1"
    return url


def parsePDF(file, ruleset, report): 
    '''
Uploads the file and calls the pdf parser function
returns JSON (dictionary) object that represents the accesibility of the pdf
'''

    # save file to temp location
    filename = str(report.id)+str(file.name)
    #location = 'tempfiles/pdf/'+filename
    #filePath = default_storage.save(location, file)

    filePath = save(file, 'tempfiles/pdf/', filename)

    # get location of processor
    startingDir = os.getcwd()
    fileDir = startingDir + '/' + filePath
    processDir = startingDir+'/processor'
    os.chdir(processDir)

    #run processor
    os.system("java -jar PdfAInspector.jar "+fileDir)
    os.chdir(startingDir)
    
    #resultfile = tempfile/result/result_filename.json 
    #get filename
    savedFileName = re.compile("^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))")
    resultFile = savedFileName.match(filePath)
    dir = resultFile.group(1)
    savedfilename = resultFile.group(2)
    resultfile = dir+"result_"+savedfilename+".json"
    fp = open(resultfile, 'r')
    jresult = json.load(fp)

    return jresult

def readRulesetFile (request):
    if request.method == 'POST':
        form = RulesForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            filepath = save(file, 'tempfiles/rules/')

            #convert file to json object
            fp = open(filepath, 'r')
            rulesetDict = json.load(fp)

            #print rulesetDict

            saveRuleset(rulesetDict)

    #add return
    return render_to_response('app/rules_upload_complete.html')
