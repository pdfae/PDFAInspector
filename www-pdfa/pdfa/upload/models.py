# Author: Prateek Arora

from django.db import models
from django.contrib.auth.models import User

# Function: content_file_name
#
# This funciton is called when a user account is activated.
# Returns the complete filepath where an uploaded file is to be stored.
# 

def content_file_name(instance, filename):
    if (instance.owner == ""):
        return '/'.join(["public", filename])
    return '/'.join([instance.owner, filename])

# UserFile model
#
# Model that stores the unique ID (uid), file owner (user name), file,
# report title (title), notes and creation date in the database associated
# with this tool.
#

class UserFile(models.Model):
    uid = models.CharField(max_length = 40, editable = False, unique = True)    
    owner = models.CharField(max_length = 30, editable = False)
    file = models.FileField(upload_to = content_file_name)
    title = models.CharField(max_length = 130)
    notes = models.CharField(max_length = 2000)
    date = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return "Id: " + self.uid + " Owner: " + self.owner + " Title: " + self.title + " Notes: " + self.notes
