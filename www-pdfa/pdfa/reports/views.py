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

def display(request):
	request.session['parsed_pdf'] = request.GET['f']
	return HttpResponseRedirect('/accounts/profile/reports/summary/')

# tab to display tree view

def displaytreeview(request):
	currentTab = "tree"
	user = request.user
	if user.is_authenticated():
		auth = 'true'
		filepath =  user.get_profile().filepath
		currentPTab = "reports"
		baset = "userprofile/profile_base.html"
	else:
		auth = 'false'
		filepath =  MEDIA_ROOT + 'public/'
		currentPage = "upload"
		baset = "base.html"
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	result = open(parsefile)
	base = json.loads(result.read())
	nodes = []
	searchNode(base, "tags", 0, nodes)
	
	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
	
	output += "<div class=\"css-treeview\">"
	for node in nodes:
		output += writeNode2(node)
	output += "</div>"
	return render_to_response("reports/treeview.html", locals())

# tab to display information about tables in document

def displaytables(request):
	currentTab = "tbl"
	user = request.user
	if user.is_authenticated():
		auth = 'true'
		filepath =  user.get_profile().filepath
		currentPTab = "reports"
		baset = "userprofile/profile_base.html"
	else:
		auth = 'false'
		currentPage = "upload"
		filepath =  MEDIA_ROOT + 'public/'
		baset = "base.html"
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	result = open(parsefile)
	base = json.loads(result.read())
	nodes = []
	searchNode(base, "Table", 0, nodes)
	output = ""
	i = 0
	for node in nodes:
		i = i + 1
		output += "<b>Table " + unicode(i) + "</b>\n<br>"
		output += writeNode(node)
		output += "<br>"

	content = []#cnode["content"]
	print content
	return render_to_response("reports/tableview.html", locals())
	
# tab to display information about forms in document

def displayforms(request):
	currentTab = "form"
	user = request.user
	if user.is_authenticated():
		auth = 'true'
		filepath =  user.get_profile().filepath
		currentPTab = "reports"
		baset = "userprofile/profile_base.html"
	else:
		auth = 'false'
		currentPage = "upload"
		filepath =  MEDIA_ROOT + 'public/'
		baset = "base.html"
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	#cnode = parsespecific(parsefile, "Form")
	result = open(parsefile)
	base = json.loads(result.read())
	nodes = []
	searchNode(base, "Form", 0, nodes)
	output = ""
	for node in nodes:
		output += writeNode(node)
	return render_to_response("reports/formview.html", locals())

# tab to display information about images in document

def displayimages(request):
	currentTab = "img"
	user = request.user
	if user.is_authenticated():
		auth = 'true'
		filepath =  user.get_profile().filepath
		currentPTab = "reports"
		baset = "userprofile/profile_base.html"
	else:
		auth = 'false'
		currentPage = "upload"
		filepath =  MEDIA_ROOT + 'public/'
		baset = "base.html"
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	cnode = parsespecific(parsefile, "Images")
	content = cnode["content"]
	
	result = open(parsefile)
	base = json.loads(result.read())
	
	nodes = []
	searchNode(base, "Images", 0, nodes)
	output = ""
	for node in nodes:
		output += writeNode(node)
	output = writeNode(node)
	
	print content
	return render_to_response("reports/imageview.html", locals())

# tab to display information about headers in document

def displayheaders(request):
	currentTab = "head"
	auth = 'true'
	filepath =  request.user.get_profile().filepath
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	json_data = open (parsefile)
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

def displaysummary(request):
	user = request.user
	if user.is_authenticated():
		auth = 'true'
		filepath =  request.user.get_profile().filepath
		currentPTab = "reports"
		baset = "userprofile/profile_base.html"
	else:
		auth = 'false'
		currentPage = "upload"
		filepath =  MEDIA_ROOT + 'public/'
		baset = "base.html"
	currentTab = "summary"
	import json
	from pprint import pprint
	
	filename =  request.session['parsed_pdf']
	resultfile = filepath + "result-" + filename.replace('.pdf','') + ".json"
	
	if os.path.isfile(resultfile):
		json_data = open (resultfile) #insert filepath of json result file
		data = json.load(json_data)
		tests = (data["results"])
		json_data.close()
		rtest=0
		rpass=0
		rwarning=0
		rfail=0
		rinspect=0
		
		for test in tests:
			tags = test["tags"]
			for tag in tags:
				rtest=rtest+1
				if (tag["result"]==1):
					rpass=rpass+1
				elif (tag["result"]==3):
					rwarning=rwarning+1
				elif (tag["result"]==2):
					rfail=rfail+1
				elif (tag["result"]==4):
					rinspect=rinspect+1
		
		print tests
		return render_to_response("reports/summaryview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

# tab to display information about bookmarks in document

def displaybookmark(request):
	user = request.user
	if user.is_authenticated():
		auth = 'true'
		filepath =  user.get_profile().filepath
		currentPTab = "reports"
		baset = "userprofile/profile_base.html"
	else:
		auth = 'false'
		currentPage = "upload"
		filepath =  MEDIA_ROOT + 'public/'
		baset = "base.html"
	currentTab = "bm"
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	result = open(parsefile)
	base = json.loads(result.read())
	nodes = []
	searchNode(base, "Bookmarks", 0, nodes)
	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
	output = "<div class=\"css-treeview\">"
	for node in nodes:
		output += writeNode2(node)
	output += "</div>"
	#cnode = parsespecific(parsefile, "Bookmarks")
	#content = cnode["content"]
	content = []
	return render_to_response("reports/bookmarkview.html", locals())
