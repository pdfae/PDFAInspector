import json
import os
from web.app.models import *

def extractResults(filename, reportID):
   filename = 'Results.txt'
   j = extractJSON(filename)
   getResults(j, reportID)


def getResults(jobject, reportID):
    #jobject['results'][0]['section'].keys()
    for sectionResult in jobject['results']:
        getResultsFromSection(sectionResult['section'], reportID)

def getResultsFromSection(jobject, reportID):
    report = Report.objects.get(id=reportID)

    print "\n\n"

    section = Section.objects.get(title=jobject['title'])
    rules = Rule.objects.filter(section = section)
    
    for result in jobject['rule']:
        print "result: "
        print result
        rule = rules.get(title = result['name'])
        res = result['result']
        message = result['message']
        ruleresult = RuleResult(rule=rule,report=report,result=res,\
                message=message)
        ruleresult.save()
        print ruleresult.rule.id

    for sectionResult in jobject['subsections']:
        getResultsFromSection(sectionResult['section'], reportID)
    

#Turns the results.json file into a python dictionary object
def extractJSON(filename):
    filepath = os.path.abspath('../web/results/'+filename)
    fp = open(filepath,'r')
    return json.load(fp)

