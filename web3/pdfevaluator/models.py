from django.contrib.auth.models import User
from django.db import models

class Ruleset (models.Model):
	file_name = models.CharField(max_length=255) #original file name
#	file_path = models.FilePathField(path='/var/www/django/pdfainspector/web/files/rules')

class Report (models.Model):
	datestamp = models.DateField(auto_now_add=True)
	user = models.ForeignKey(User)
	ruleset = models.ForeignKey(Ruleset)
	file_name = models.CharField(max_length=50) #original file name
#	file_path = models.FilePathField(path='/var/www/django/pdfainspector/web/files/pdfs')

class Rule (models.Model):
	ruleset = models.ForeignKey(Ruleset)
	title = models.CharField(max_length=255)
	rule_id = models.CharField(max_length=50)
	wcag_id = models.CharField(max_length=50)
	sect508_id = models.CharField(max_length=50)
	message = models.TextField(blank=True)

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
    message = models.CharField(max_length=255)

    def __unicode__(self):
        return self.message
