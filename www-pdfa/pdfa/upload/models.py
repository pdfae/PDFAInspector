'''
Created on Mar 2, 2012

@author: arora6
'''
from django.db import models
from django.contrib.auth.models import User

def content_file_name(instance, filename):
    return '/'.join([instance.owner.username, filename])

# Create your models here.
class UserFile(models.Model):    
    owner = models.ForeignKey(User)
    name = models.FileField(upload_to = content_file_name)
    def __unicode__(self):
        return unicode(self.owner.username)