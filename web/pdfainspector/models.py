from django.db import models
from django.contrib.auth.models import User
    
class UserProfile (models.Model):
    user = models.ForeignKey(User, unique = True)

class Pdf (models.Model):
    timestamp = models.DateTimeField()
    userid = models.ForeignKey(UserProfile)
    id = models.IntegerField(primary_key = True)

class Rule (models.Model):
    userid = models.ForeignKey(UserProfile)
    code = models.TextField()
    id = models.IntegerField(primary_key = True)

class RuleSet (models.Model):
    setName = models.CharField(max_length = 20)
    id = models.IntegerField(primary_key = True)

class RulesRulesets (models.Model):
    ruleid = models.ForeignKey(Rule)
    rulesetid = models.ForeignKey(RuleSet)

class PdfsRulesets (models.Model):
    pdfid = models.ForeignKey(Pdf)
    rulesetid = models.ForeignKey(RuleSet)

class Result (models.Model):
    pdfid = models.ForeignKey(Pdf)
    id = models.IntegerField(primary_key = True)
    passed = models.BooleanField()

class ResultsRules (models.Model):
    resultid = models.ForeignKey(Result)
    ruleid = models.ForeignKey(Rule)

class ResultsRuleSets (models.Model):
    resultid = models.ForeignKey(Result)
    rulesetid = models.ForeignKey(RuleSet)







