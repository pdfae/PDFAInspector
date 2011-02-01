from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationForm
from app.forms import LoginForm

forms = {
        "registration":RegistrationForm(),
        "login":LoginForm()
}

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    #(r'^admin/(.*)',admin.site.root),
    (r'^accounts/',include('web.registration.urls')),
    (r'^app/', include('web.app.urls')),
    (r'^$', direct_to_template, 
        {'template':'index.html', 'extra_context':forms}),
)
