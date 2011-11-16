# Create your views here.
from django.shortcuts import *
from forms import *
from models import *
import json
import os

def signup(request):
	return render_to_response("user.html", locals())

def home(request):
	currentPage = "home"
	return render_to_response("index.html", locals())

def about(request):
	currentPage = "about"
	return render_to_response("about.html", locals())

def contact(request):
	currentPage = "contact"
	if (request.method=="POST"):
		f = signupform(request.POST)
		if f.is_valid():
			name = f.cleaned_data['username']
			pword = f.cleaned_data['password']
			eml = f.cleaned_data.get('email', 'noreply@uiuc.edu')
			newuser = User(username = name, password = pword, email=eml)
			newuser.save()
			return HttpResponseRedirect('/user/')		
	else:
		f = signupform()
	return render_to_response("form.html", locals(), context_instance=RequestContext(request))

def upload (request):
	currentPage = "upload"
	if (request.method=="POST"):
		print "in upload section"
		f = uploadfileform(request.POST, request.FILES)
		if f.is_valid():
			fname = f.cleaned_data['filename']
			handle_uploaded_file(request.FILES['file'], fname)
			os.system("java -jar /opt/PDFAInspector/PdfInspector/PdfAInspector.jar /var/www-pdfa/files/" + fname + " &")
			return render_to_response("processing.html",locals())
	else:
		f = uploadfileform()
	return render_to_response("fileupload.htm", locals(), context_instance=RequestContext(request))

def writeNode (node, depth=0):
	output = "<div class='node n_" + str(depth) + "'><b>"+node["tagName"]+"</b><br />\n<i>\n"
	attr = []
	for i in node["attributes"]:
		for j,k in i.iteritems():
			attr.append(j + "=" + k)
	output += ", ".join(attr)
	output += "</i><br />\n"
	for i in node["content"]:
		if len(i) > 1:
			output += writeNode(i,depth+1)
		else:
			output += str(i["text"])
	output += "</div>"
	return output


def view (request):
	currentPage = "upload"
	fname = request.GET['f']
	output = ""
	r_path = '/var/www-pdfa/files/json-' + fname[:fname.find('.')] + ".json"
	if os.path.isfile(r_path):
		result = open(r_path)
		j = json.loads(result.read())
		output = writeNode(j)
		result.close()
	else:
		output = "File not done processing."
	return render_to_response("viewfile.html",locals())


def handle_uploaded_file(f, fname):
	destination = open('/var/www-pdfa/files/'+fname, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

