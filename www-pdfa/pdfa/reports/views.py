'''
5 tabs -> tree view, images, headers, forms, tables
clicking on each, should run json parser for appropriate type and json file
currently, dump json parsed information on screen
'''
# Author: Prateek Arora
# including required modules
from django.shortcuts import *
from settings import *
from django.contrib.auth.decorators import login_required
import os
from backends import *
import json

@login_required
def display(request):
	request.session['parsed_pdf'] = request.GET['f']
	return HttpResponseRedirect('/accounts/profile/reports/summary/')

# tab to display tree view
@login_required
def displaytreeview(request):
	currentPage = "userprofile"
	currentTab = "treeview"
	auth = 'true'
	file = request.user.get_profile().filepath + request.session['parsed_pdf']
	import json
	result = open(file)
	j = json.loads(result.read())
	output = writeNode(j)
	return render_to_response("reports/treeview.html", locals())

# tab to display information about tables in document
@login_required
def displaytables(request):
	currentPage = "userprofile"
	auth = 'true'
	file = request.user.get_profile().filepath + request.session['parsed_pdf']
	cnode = parsespecific(file, "Images")
	content = cnode["content"]
	print content
	return render_to_response("reports/tableview.html", locals())
	
# tab to display information about forms in document
@login_required
def displayforms(request):
	currentPage = "userprofile"
	auth = 'true'
	file = request.user.get_profile().filepath + request.session['parsed_pdf']
	cnode = parsespecific(file, "Form")
	content = cnode["content"]
	print content
	return render_to_response("reports/formview.html", locals())

# tab to display information about images in document
@login_required
def displayimages(request):
	currentPage = "userprofile"
	auth = 'true'
	file = request.user.get_profile().filepath + request.session['parsed_pdf']
	cnode = parsespecific(file, "Images")
	content = cnode["content"]
	
	print content
	return render_to_response("reports/imageview.html", locals())

# tab to display information about headers in document
@login_required
def displayheaders(request):
	currentPage = "userprofile"
	auth = 'true'
	file = request.user.get_profile().filepath + request.session['parsed_pdf']
	json_data = open (file)
	data = json.load(json_data)
	cnode = data["content"]
	for c in cnode:
		if (c["tagName"] == "tags"):
			cnode2 = c["content"]
	
	for c2 in cnode2:
		if (c2["tagName"] == "Sect"):
			content = c2["content"]
		else:
			content = []
	#print cnode		
	#print content
	return render_to_response("reports/headerview.html", locals())

# tab to display information about headers in document
@login_required
def displaysummary(request):
	currentPage = "userprofile"
	auth = 'true'
	import json
	from pprint import pprint	
	#file = request.user.get_profile().filepath + request.session['parsed_pdf']
	file = "/home/pdfae/PDFAInspector/www-pdfa/files/atulgupte/results-json-testdocument-images.json"
	#resultfile = file + "results"
	#if os.path.isfile(resultfile):
	json_data = open (file) #insert filepath of json result file
	data = json.load(json_data)
	tests = (data["results"])
	json_data.close()
	rpass=0
	rwarning=0
	rfail=0
	rinspect=0
	for test in tests:
		#print test
		tags = test["tags"]
		for tag in tags:
			if (tag["result"]=="pass"):
				rpass=rpass+1
			elif (tag["result"]=="warning"):
				rwarning=rwarning+1
			elif (tag["result"]=="fail"):
				rfail=rfail+1
			elif (tag["result"]=="manual inspection"):
				rinspect=rinspect+1
	return render_to_response("reports/summaryview.html", locals())
	#else:
	#	return render_to_response("reports/summary_notfound.html", locals())

