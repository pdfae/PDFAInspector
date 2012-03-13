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
from upload.models import UserFile

def setup(user, uid):
	auth = user.is_authenticated()
	if auth:
		currentPage = "reports"
	else:
		currentPage = "upload"
	fileObj = UserFile.objects.get(uid = uid)
	title = fileObj.title
	notes = fileObj.notes
	[filepath, filename] = fileObj.file.name.rsplit('/', 1)
	filepath = MEDIA_ROOT + filepath + "/"
	parsefile = filepath + "json-" + filename.replace('.pdf','') + ".json"
	resultfile = filepath + "result-" + filename.replace('.pdf','') + ".json"
	return [auth, currentPage, parsefile, resultfile, title, notes]



# tab to display tree view
def displaytreeview(request, uid):
	currentTab = "tree"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
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

def displaytables(request, uid):
	currentTab = "tbl"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)	
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

def displayforms(request, uid):
	currentTab = "form"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
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

def displayimages(request, uid):
	currentTab = "img"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
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

def displayheaders(request, uid):
	currentTab = "head"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
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
def displaysummary(request, uid):
	currentTab = "summary"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
	output = ""
    	
    	if os.path.isfile(parsefile):
    		
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
					
		for test in tests:
			if (test["category"]==0):
				output += "<b>Document Level Rules:</b><br><table class = \"fancy\"><tr><th>Total tests</th><th>Pass</th></tr>"
				output += "<td></td><td></td>"
			if (test["category"]==1):
				output += "<br><br><b>Links:</b><br><table class = \"fancy\"><tr><th>Total tests</th><th>Pass</th></tr>"
				output += "<td></td><td></td>"
			if (test["category"]==2):
				output += "<br><br><b>Images:</b><br><table class = \"fancy\"><tr><th>Total tests</th><th>Pass</th></tr>"
				output += "<td></td><td></td>"
			if (test["category"]==3):
				output += "<br><br><b>Forms:</b><br><table class = \"fancy\"><tr><th>Total tests</th><th>Pass</th></tr>"
				output += "<td></td><td></td>"
			if (test["category"]==4):
				output += "<br><br><b>Headers:</b><br><table class = \"fancy\"><tr><th>Total tests</th><th>Pass</th></tr>"
				output += "<td></td><td></td>"
			if (test["category"]==5):
				output += "<br><br><b>Tables:</b><br><table class = \"fancy\"><tr><th>Total tests</th><th>Pass</th></tr>"
				output += "<td></td><td></td>"
    		
    		filePointer = open(parsefile)
        	data = json.load(filePointer)
        	filePointer.close()
        	tags = []
        	searchNode(data, "tags", 0, tags)
        	links = []
        	searchNode(tags[0], "Link", 0, links)
        	images = []
        	searchNode(tags[0], "Figure", 0, images)
        	forms = []
        	tables = []
        	searchNode(tags[0], "Table", 0, links)
        	searchNode(data, "Form", 0, forms)
        	numTags = countNode(tags[0])
        	numForms = countNode(forms[0])
        	numLinks = len(links)
        	numImages = len(images)
        	numTables = len(tables)
        	
        	return render_to_response("reports/summaryview.html", locals())
    	else:
        	return render_to_response("reports/summary_notfound.html", locals())

'''
def displaysummary(request, uid):
	currentTab = "summary"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
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
'''
# tab to display information about bookmarks in document

def displaybookmark(request, uid):
	currentTab = "bm"
	[auth, currentPage, parsefile, resultfile, title, notes] = setup(request.user, uid)
	result = open(parsefile)
	base = json.loads(result.read())
	nodes = []
	searchNode(base, "Bookmarks", 0, nodes)
	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
	output += "<div class=\"css-treeview\">"
	for node in nodes:
		output += writeNode2(node)
	output += "</div>"
	#cnode = parsespecific(parsefile, "Bookmarks")
	#content = cnode["content"]
	content = []
	return render_to_response("reports/bookmarkview.html", locals())
