from app.models import *

class SectionDict():
    def __init__(self, section, reportID, subsections=[]):
        self.title = section.title
        self.url = section.url
        self.subsections = subsections
        
        #list of results for this section
        self.ruleresults = []
        rules = section.rule_set.filter(section=section)
        report = Report.objects.get(id=reportID)
        for rule in rules:
            result = rule.ruleresult_set.get(report = report)
            self.ruleresults.append((rule,result))

    def addSubEntry(self, subdict):
        self.subsections.append(subdict)
        return self

    def __unicode__(self):
        return self.title

