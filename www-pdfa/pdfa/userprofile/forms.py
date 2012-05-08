# Author: Prateek Arora, Atul Gupte

from django.forms import ModelForm

from django.contrib.auth.models import User

# Class: userChangeForm
#
# This is the form that gets displayed when the user updates his account settings.
# It allows users to update their first/last names and e-mail. 
#

class userChangeForm (ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')