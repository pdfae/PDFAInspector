from django.db import models
from django.contrib.auth.models import User

class Ruleset (models.Model):
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

class Report (models.Model):
    datestamp = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=256)
    ruleset = models.ForeignKey(Ruleset)

class Section (models.Model):
    ruleset = models.ForeignKey(Ruleset)
    parentSection = models.ForeignKey('self',null=True,blank=True)
    num = models.IntegerField()
    title = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

class Requirement (models.Model):
    section = models.ForeignKey(Section)
    num = models.IntegerField()
    title = models.CharField(max_length=256)
    level = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

class Rule (models.Model):
    requirement = models.ForeignKey(Requirement)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

class Result (models.Model):
    RESULT_TYPES = (
            (u'P', u'Pass'),
            (u'PR', u'Potential Recommendation'),
            (u'R', u'Recommendation'),
            (u'PV', u'Potential Violation'),
            (u'V', u'Violation'),
    )
    report = models.ForeignKey(Report)
    rule = models.ForeignKey(Rule)
    result = models.CharField(max_length=2,choices=RESULT_TYPES)
    message = models.CharField(max_length=256)

    def __unicode__(self):
        return self.message
