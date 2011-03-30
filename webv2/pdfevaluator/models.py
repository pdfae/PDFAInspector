from django.contrib.auth.models import User
from django.db import models

class Ruleset (models.Model):
    title = models.CharField(max_length=256, blank=True)
    url = models.URLField(max_length=256, blank=True)

class Report (models.Model):
    datestamp = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    ruleset = models.ForeignKey(Ruleset)
	pdf_file = models.CharField()

class Rule (models.Model):
	ruleset = models.ForeignKey(Ruleset)
	title = models.CharField(max_length=256)
	wcag_id = models.CharField(max_length=256)
	sect508_id = models.CharField(max_length=256)
	message = models.CharField(max_length=256)

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
