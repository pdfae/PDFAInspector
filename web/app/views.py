from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from app.forms import UploadFileForm
from app.models import *

import json

def index(request):
    form = UploadFileForm()
    return render_to_response('app/index.html',{'uploadForm':form},
            context_instance=RequestContext(request))

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
    filename = str(report.id)+str(file.name)
    location = 'tempfiles/pdf/'+filename
    default_storage.save(location, file)

    #TODO: call karen's functions
    #resultfile = tempfile/results/filename.json 

    resultfile = 'results/Results.txt'
    fp = open(resultfile, 'r')
    jresult = json.load(fp)

    return jresult


def saveResults(jresult, report):
    '''
    saves results to database
    '''
    #TODO: i dont think we need the ruleset info, just need the id
    ruleset = report.ruleset
    results = jresult['results']

    #put results in database
    for result in results:
        ruleID = result['rule_id']
        rule = Rule.objects.get(id=ruleID)

        rresult = result['result']
        message = result['message']
        
        Result(rule=rule,result=rresult,message=message, report=report).save()

def getReportWithNestedResults(report):
    '''
    returns a dictionary object with results nested
    '''
    ruleset = report.ruleset
    sections = ruleset.section_set.filter(parentSection=None)

    sectionList = []

    for section in sections:
        print section
        #if it has requirements instead of sections
        if section.requirement_set.all():
            sectionList.append({'section':section, \
                    'requirements':getRequirements(section, report)})
        else:
            for subsection in section.section_set.all():
                sectionList.append({'section':section, \
                        'subsections':getSubsection(subsection, report)})

    return sectionList


def getSubsection(section, report):
    '''
    returns a list of dictionaries
    section: given section
    requirements: list of requirment dictionaries OR subsections: list of section dicts
    '''

    sectionList = []

    if section.requirement_set.all():
        sectionList.append({'section':section, \
            'requirements':getRequirements(section, report)})


    else:
        for subsection in section.section_set.all():
            sectionList.append({'section':subsection, \
                 'subsections':getSubsection(subsection, report)})

    return sectionList


def getRequirements(section, report):
    '''
    Returns a list of dictionaries:
    requirement: requirement object
    rules: list of rules that fall under the requirement
    '''

    requirementList = []
    for requirement in section.requirement_set.all():
        ruleList = getRules(requirement,report)
        requirementList.append({'requirement':requirement,'rules':ruleList})
    
    return requirementList


def getRules(requirement, report):
    '''
    Returns a list of dictionaries:
    rule: rule object
    results: list of results that fall under the requirement given the report
    '''
    ruleList = []
    for rule in requirement.rule_set.all():
       resultList = rule.result_set.filter(report=report) 
       ruleList.append({'rule':rule,'results':resultList})

    return ruleList
