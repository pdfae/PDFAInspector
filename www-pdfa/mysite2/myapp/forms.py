from django import forms as forms

RULES_CHOICES = (
	('general', 'General Rules'),
	('useroption1', 'WCAG'),
)

class signupform (forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(widget=forms.PasswordInput, label="Password")
	email = forms.EmailField()

class uploadfileform (forms.Form):
	filename = forms.CharField(label="Filename")
	file = forms.FileField()