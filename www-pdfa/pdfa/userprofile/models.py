from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.signals import request_finished
from settings import MEDIA_ROOT
import os

class UserProfile(models.Model):
	# This field is required.
	user = models.OneToOneField(User)
	# Other fields here
	filepath = models.FilePathField(default = '')

def create_user_profile(sender, instance, created, **kwargs):
	# when created
	if created:
		UserProfile.objects.create(user=instance)
	#when activated	
	if (not created and instance.is_active):
		user = instance
		username = user.username
		user.get_profile().filepath = MEDIA_ROOT + username + '/'
		user.get_profile().save()
		os.system("mkdir " + user.get_profile().filepath)
		
post_save.connect(create_user_profile, sender=User)