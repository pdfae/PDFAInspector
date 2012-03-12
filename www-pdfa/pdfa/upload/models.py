'''
Created on Mar 2, 2012

@author: arora6
'''
from django.db import models
from django.contrib.auth.models import User

def content_file_name(instance, filename):
    if (instance.owner == ""):
        return '/'.join(["public", filename])
    return '/'.join([instance.owner, filename])

# Create your models here.
class UserFile(models.Model):
    uid = models.CharField(max_length = 40, editable = False, unique = True)    
    owner = models.CharField(max_length = 30, editable = False)
    filename = models.FileField(upload_to = content_file_name)
    title = models.CharField(max_length = 130)
    notes = models.CharField(max_length = 2000)
    def __unicode__(self):
        return unicode(self.owner)
