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
	currentTab = "tree"
	auth = 'true'
	filepath =  request.user.get_profile().filepath
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	result = open(parsefile)
	j = json.loads(result.read())
	node = searchNode(j, "tags")
	output = writeNode(node)
	return render_to_response("reports/treeview.html", locals())

# tab to display information about tables in document
@login_required
def displaytables(request):
	auth = 'true'
	currentTab = "tbl"
	#file = request.user.get_profile().filepath + request.session['parsed_pdf']
	#cnode = parsespecific(file, "Images")
	content = []#cnode["content"]
	print content
	return render_to_response("reports/tableview.html", locals())
	
# tab to display information about forms in document
@login_required
def displayforms(request):
	currentTab = "form"
	auth = 'true'
	filepath =  request.user.get_profile().filepath
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	#cnode = parsespecific(parsefile, "Form")
	result = open(parsefile)
	j = json.loads(result.read())
	node = searchNode(j, "Form")
	output = writeNodeContent(node)
	return render_to_response("reports/formview.html", locals())

# tab to display information about images in document
@login_required
def displayimages(request):
	currentTab = "img"
	auth = 'true'
	filepath =  request.user.get_profile().filepath
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	cnode = parsespecific(parsefile, "Images")
	content = cnode["content"]
	
	result = open(parsefile)
	j = json.loads(result.read())
	node = searchNode(j, "Images")
	output = writeNode(node)
	
	print content
	return render_to_response("reports/imageview.html", locals())

# tab to display information about headers in document
@login_required
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
@login_required
def displaysummary(request):
	auth = 'true'
	currentTab = "summary"
	import json
	from pprint import pprint
	filepath =  request.user.get_profile().filepath
	filename =  request.session['parsed_pdf']
	resultfile = filepath + "result-" + filename.replace('.pdf','') + ".json"
	#print resultfile
	if os.path.isfile(resultfile):
		json_data = open (resultfile) #insert filepath of json result file
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
	else:
		return render_to_response("reports/summary_notfound.html", locals())

# tab to display information about bookmarks in document
@login_required
def displaybookmark(request):
	auth = 'true'
	currentTab = "bm"
	filepath =  request.user.get_profile().filepath
	filename =  request.session['parsed_pdf']
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	import json
	result = open(parsefile)
	base = json.loads(result.read())
	node = searchNode(base, "Bookmarks")
	output = writeNode(node)
	return render_to_response("reports/bookmarkview.html", locals())
