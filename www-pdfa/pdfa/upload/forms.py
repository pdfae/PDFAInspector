from django import forms as forms

class uploadfileform (forms.Form):
	title = forms.CharField(max_length = 130, label = "Report Title", required = False)
	file = forms.FileField()
	notes = forms.CharField(max_length = 2000, widget=forms.Textarea, required = False)

class notesupdateform (forms.Form):
	notes = forms.CharField(max_length = 2000, widget=forms.Textarea, required = False)
	
class ContactForm (forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length = 2000, widget=forms.Textarea, required = True)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)