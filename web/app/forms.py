from django import forms
from app.models import Ruleset

class UploadFileForm(forms.Form):
    #RULESET_CHOICES = [(rule.id, rule.title) for rule in Ruleset.objects.all()]
    RULESET_CHOICES = [(1,"Ruleset title")]

    file = forms.FileField()
    ruleset = forms.ChoiceField(choices=RULESET_CHOICES)
    #addRuleset = forms.





