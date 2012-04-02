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

def setup_notes_form(request, uid, notes, fileObj):
	if (request.method=="POST"):
			form = notesupdateform(request.POST)
			if form.is_valid():
				fileObj = UserFile.objects.get(uid = uid)
				fileObj.notes = form.cleaned_data['notes']
				fileObj.save()
	else:
		data = {'notes': notes}
		form = notesupdateform(data)
	return form
	
# tab to display tree view

def displaysummary(request, uid):
	currentTab = "summary"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		
		resultFP = open(resultfile)
		result_data = json.load(resultFP)
		resultFP.close()
		
		parseFP = open(parsefile)
		parse_data = json.load(parseFP)
		parseFP.close()
		
		message = "<span color=\"red\">The document is untagged and not accessible</span>"
		
		rnum = {}
		rtitle = {}
		rtest={}
		rpass={}
		rfail={}
		rinspect={}
		for i in range(0,6):
			rnum[i] = 0
			rtitle[i] = []
			rtest[i] = []
			rpass[i] = []
			rfail[i] = []
			rinspect[i] = []
		
		tests = result_data["results"]	
		for test in tests:
			tags = test["tags"]
			category = test["category"]
			ntest = 0
			npass = 0
			nfail = 0
			nins = 0
			for tag in tags:		
				ntest += 1
				if (tag["result"]==1):
					npass += 1
					if test["id"] == "core.DocumentMustBeTagged":
						message = "<span color = \"#FFA500\">The document is partially accessible</span>"
				elif (tag["result"]==2):
					nfail += 1
				elif (tag["result"]==3):
					nins += 1	
			rnum[category] += 1
			rtitle[category].append([test["title"], npass, nfail, nins])
			rtest[category].append(ntest)
			rpass[category].append(npass)
			rfail[category].append(nfail)
			rinspect[category].append(nins)
				
		content = []
		content.append(["Document Level Rules:"])
		content.append(["Links:"])
		content.append(["Figures:"])
		content.append(["Forms:"])
		content.append(["Headers:"])
		content.append(["Tables:"])
		
		tot_test = 0
		tot_pass = 0
		tot_fail = 0
		tot_ins = 0
		for i in range(0,6):
			if sum(rtest[i]) > 0:
				content[i].append(sum(rtest[i])/rnum[i])
				content[i].append(rtitle[i])
			else:
				content[i].append("")
			
			tot_test += sum(rtest[i])
			tot_pass += sum(rpass[i])
			tot_fail += sum(rfail[i])
			tot_ins += sum(rinspect[i])
		
		if tot_fail == 0:
			message = "<span color = \"green\">The document is accessible</span>"	
		form = setup_notes_form(request, uid, notes, fileObj)
		return render_to_response("reports/summaryview.html", locals(), context_instance=RequestContext(request))
	else:
		return render_to_response("reports/summary_notfound.html", locals())


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

def displaylinks(request, uid):
	currentTab = "links"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj] = setup(request.user, uid)
	tableRows = getLink(parsefile, resultfile, uid)
	return render_to_response("reports/rowView.html", locals())

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
		output += "<div><p><b>Table " + unicode(i) + "</b></p>\n"
		output += writeNode(node)
		output += "</div>"

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
