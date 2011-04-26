from django import forms

class UploadPdfForm(forms.Form):
    file = forms.FileField()
    private = forms.BooleanField(default=False,required=False)
