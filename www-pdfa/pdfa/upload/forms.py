from django import forms as forms

class uploadfileform (forms.Form):
	file = forms.FileField()