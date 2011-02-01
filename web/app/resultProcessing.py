from app.models import *

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
