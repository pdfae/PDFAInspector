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
	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
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
        	searchNode(tags[0], "Table", 0, links)
        	searchNode(data, "Form", 0, forms)
        	numTags = countNode(tags[0])
        	numForms = countNode(forms[0])
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
					
		output = []
		output.append("<b>Document Level Rules:</b><br><table class = \"fancy\"><tr><th>Title</th><th>Pass</th><th>Fail</th><th>Warning</th><th>Manual Inspection</th></tr>")
		output.append("<b>Links:</b><br><table class = \"fancy\"><tr><th>Title</th><th>Pass</th><th>Fail</th><th>Warning</th><th>Manual Inspection</th></tr><tr><td><center>Number of Links</center></td><td colspan=\"4\"><center>" + unicode(numLinks) + "</center></td></tr>")
		output.append("<b>Images:</b><br><table class = \"fancy\"><tr><th>Title</th><th>Pass</th><th>Fail</th><th>Warning</th><th>Manual Inspection</th></tr><tr><td><center>Number of Image Tags</center></td><td colspan=\"4\"><center>" + unicode(numImages) + "</center></td></tr>")
		output.append("<b>Forms:</b><br><table class = \"fancy\"><tr><th>Title</th><th>Pass</th><th>Fail</th><th>Warning</th><th>Manual Inspection</th></tr><tr><td><center>Number of Form Elements</center></td><td colspan=\"4\"><center>" + unicode(numForms) + "</center></td></tr>")
		output.append("<b>Headers:</b><br><table class = \"fancy\"><tr><th>Title</th><th>Pass</th><th>Fail</th><th>Warning</th><th>Manual Inspection</th></tr><tr><td><center>Number of Header Elements</center></td><td colspan=\"4\"><center>Not Implemented</center></td></tr>")
		output.append("<b>Tables:</b><br><table class = \"fancy\"><tr><th>Title</th><th>Pass</th><th>Fail</th><th>Warning</th><th>Manual Inspection</th></tr><tr><td><center>Number of Table Elements</center></td><td colspan=\"4\"><center>" + unicode(numTables) + "</center></td></tr>")
		
		
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
				output[i] += "<tr><td><center>" + unicode(test["title"]) + "</center></td>" + "<td><center>" + unicode(numPass) + "</center></td>"+ "<td><center>" + unicode(numFail) + "</center></td>"+ "<td><center>" + unicode(numWarn) + "</center></td>"+ "<td><center>" + unicode(numInsp) + "</center></td></tr>"
			elif (len(test["tags"])) == 0:
				output[i] += "<tr><td><center>" + unicode(test["title"]) + "</center></td>" + "<td colspan=\"4\"><center>" + "Not Run On Any Tags" + "</center></td></tr>"
			
		output[0] += "</table><br><br>"
		output[1] += "</table><br><br>"
		output[2] += "</table><br><br>"
		output[3] += "</table><br><br>"
		output[4] += "</table><br><br>"
		output[5] += "</table><br><br>"
        
        	if (request.method=="POST"):
			form = notesupdateform(request.POST)
			if form.is_valid():
				request.fileObj.file.notes = notes
				request.fileObj.file.save()

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