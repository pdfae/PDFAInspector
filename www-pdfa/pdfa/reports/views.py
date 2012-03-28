'''
5 tabs -> tree view, images, headers, forms, tables
clicking on each, should run json parser for appropriate type and json file
currently, dump json parsed information on screen
'''
# Author: Prateek Arora, Atul Gupte
# including required modules
from django.shortcuts import *
from settings import *
from django.contrib.auth.decorators import login_required
import os
from backends import *
import json
from upload.models import UserFile
from upload.forms import notesupdateform

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
	return [auth, currentPage, parsefile, resultfile, title, notes, fileObj]



# tab to display tree view
def displaytreeview(request, uid):
	currentTab = "tree"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	result = open(parsefile)
	base = json.loads(result.read())
	output = '<a href="javascript:check_all()" style="padding-right: 30px;">Expand All</a>'
	output += '<a href="javascript:uncheck_all()">Collapse All</a>'
	output += "<div class=\"css-treeview\">"
	output += writeNode2(base, "tags")
	output += "</div>"
	return render_to_response("reports/treeview.html", locals())

# tab to display information about tables in document

def displaytables(request, uid):
	currentTab = "tbl"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)	
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
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	output = getFormOutput(parsefile, resultfile, uid)
	return render_to_response("reports/formview.html", locals())

# tab to display information about images in document

def displayimages(request, uid):
	currentTab = "img"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	output = getImageOutput(parsefile, resultfile, uid)
	return render_to_response("reports/formview.html", locals())

# tab to display information about headers in document

def displayheaders(request, uid):
	currentTab = "head"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
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
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)

	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
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
		searchNode(tags[0], "Table", 0, tables)
		searchNode(data, "Form", 0, forms)
		numTags = countNode(tags[0])
		numForms = len(forms[0]['content'])
		numLinks = len(links)
		numImages = len(images)
		numTables = len(tables)
		numHeaders = 0 #ask how this is to be done
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
		
		rules = {}
		for test in tests:
			rules[test["category"]] = True
		
		output = []
		output.append("<b>Document Level Rules:</b><br>\n")
		output.append("<b>Links:</b><br>\n")
		output.append("<b>Images:</b><br>\n")
		output.append("<b>Forms:</b><br>\n")
		output.append("<b>Headers:</b><br>\n")
		output.append("<b>Tables:</b><br>\n")
		if numLinks == 0:
			output[1] += "<b>No link tags found</b><br>\n"
			rules[1] = False
		else:
			output[1] += "<b>Number of links: " + unicode(numLinks) + "</b><br>\n"	
		if numImages == 0:
			output[2] += "<b>No image tags found</b><br>\n"
			rules[2] = False
		else:
			output[2] += "<b>Number of images: " + unicode(numImages) + "</b><br>\n"
		if numForms == 0:
			output[3] += "<b>No form elements found</b><br>\n"
			rules[3] = False
		else:
			output[3] += "<b>Number of forms: " + unicode(numForms) + "</b><br>\n"
		output[4] += "<b>Not yet implemented</b><br>\n"
		rules[4] = False	
		if numTables == 0:
			output[5] += "<b>No table tags found</b><br>\n"
			rules[5] = False
		else:
			output[5] += "<b>Number of tables: " + unicode(numTables) + "</b><br>\n"
		
		count = [1] * len(rules)
		for r in rules:
			if rules[r]:
				output[r] += "<table class = \"fancy\">\n<tr>\n"
				output[r] += "<th>Title</th>\n"
				output[r] += "<th>Pass</th>\n"
				output[r] += "<th>Fail</th>\n"
				output[r] += "<th>Warning</th>\n"
				output[r] += "<th>Manual Inspection</th>\n</tr>\n"
		
		for test in tests:
			i = test["category"]
			if (len(test["tags"])) >= 1:
				
				numPass=0
				numFail=0
				numWarn=0
				numInsp=0
				for tag in test["tags"]:
					if (tag["result"]==1):
						numPass+=1
					elif (tag["result"])==2:
						numFail+=1
					elif (tag["result"])==3:
						numWarn+=1
					elif (tag["result"])==4:
						numInsp+=1
				if count[i] %2 == 0:
					output[i] += "<tr class = \"even\">"
				else:
					output[i] += "<tr>"
				output[i] += "<td>" + unicode(test["title"]) + "</td><td>" + unicode(numPass) + "</td><td>" + unicode(numFail) + "</td><td>" + unicode(numWarn) + "</td><td>" + unicode(numInsp) + "</td></tr>"
				count[i] += 1
				
		output[0] += "</table>"
		output[1] += "</table>"
		output[2] += "</table>"
		output[3] += "</table>"
		output[4] += "</table>"
		output[5] += "</table>"
		
			
		if (request.method=="POST"):
			form = notesupdateform(request.POST)
			if form.is_valid():
				fileObj = UserFile.objects.get(uid = uid)
				fileObj.notes = form.cleaned_data['notes']
				fileObj.save()
		else:
			data = {'notes': notes}
			form = notesupdateform(data)

		return render_to_response("reports/summaryview.html", locals(), context_instance=RequestContext(request))
	else:
		return render_to_response("reports/summary_notfound.html", locals())

# tab to display information about bookmarks in document

def displaybookmark(request, uid):
	currentTab = "bm"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	result = open(parsefile)
	base = json.loads(result.read())
	nodes = []
	searchNode(base, "tags", 0, nodes)

	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
	output += "<div class=\"css-treeview\">"
	for node in nodes:
		output += writeNode2(base, "Bookmarks")
	output += "</div>"
	return render_to_response("reports/treeview.html", locals())

def displaylinks(request, uid):
	currentTab = "links"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	output = getLinkOutput(parsefile, resultfile, uid)
	return render_to_response("reports/formview.html", locals())

def displayformtree(request, uid):
	currentTab = "formtree"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	result = open(parsefile)
	base = json.loads(result.read())
	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
	output += "<div class=\"css-treeview\">"
	output += writeNode2(base, "Form")
	output += "</div>"
	return render_to_response("reports/treeview.html", locals())
