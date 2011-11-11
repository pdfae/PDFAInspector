from django.db import models

class User (models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	email = models.EmailField()
	def __unicode__(self):
		return self.username

class Upload (models.Model):
	filename = models.CharField(max_length=30)
	file = models.FileField(upload_to='/temp/')
	def __unicode__(self):
		return self.filename

# Create your models here.
