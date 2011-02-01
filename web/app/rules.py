from app.models import *

def saveRuleset(dictionary):
    title = dictionary['title']
    url = dictionary['url']

    newRuleset = Ruleset(title=title,url=url)
    newRuleset.save()

    if dictionary.has_key('sections'):
        for section in dictionary['sections']:
            saveSection(section, newRuleset, None)

def saveSection(dictionary, ruleset, parentSection):

    num = dictionary['num']
    title = dictionary['title']
    
    newSection = Section(ruleset=ruleset,parentSection=parentSection,\
            num=num,title=title)
    newSection.save()

    if dictionary.has_key('sections'):
        for section in dictionary['sections']:
            saveSection(section, ruleset, newSection)

    if dictionary.has_key('requirements'):
        for requirement in dictionary['requirements']:
            saveRequirement(requirement, newSection)


def saveRequirement(dictionary, section):
    num = dictionary['num']
    title = dictionary['title']
    level = dictionary['level']

    newRequirement=Requirement(section=section,num=num,title=title,level=level)

    newRequirement.save()

    if dictionary.has_key('rules'):
        for rule in dictionary['rules']:
            saveRule(rule, newRequirement)


def saveRule(dictionary, requirement):
    title = dictionary['title']
    url = dictionary['url']

    newRule = Rule(requirement=requirement,title=title,url=url)

    newRule.save()
    
