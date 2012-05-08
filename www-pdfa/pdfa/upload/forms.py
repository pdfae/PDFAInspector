from django import forms as forms

# Uploadfileform
#
# Creates a form that allows users to upload a file, add a report title and add notes.
# This form is displayed on the 'home/upload' page of the website.
# 

class uploadfileform (forms.Form):
	title = forms.CharField(max_length = 130, label = "Report Title", required = False)
	file = forms.FileField()
	notes = forms.CharField(max_length = 2000, widget=forms.Textarea, required = False)

# Notesupdateform
#
# Creates a textarea that allows users to enter notes.
# This form is displayed on the 'summary' page associated with each report.
# 

class notesupdateform (forms.Form):
	notes = forms.CharField(max_length = 2000, widget=forms.Textarea, required = False)
	
# Contactform
#
# Creates a form that allows users to send a message with a subject and reply-to email address.
# This form is displayed on the 'contact' page of the website.
# 

class ContactForm (forms.Form):
    subject = forms.CharField(max_length=100, label = "Subject")
    message = forms.CharField(widget=forms.Textarea, required = True, label = "Message")
    sender = forms.EmailField(required = True, label = "E-mail")
    cc_myself = forms.BooleanField(required=False)