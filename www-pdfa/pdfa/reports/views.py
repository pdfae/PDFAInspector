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
	return [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename]

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
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		
		resultFP = open(resultfile)
		result_data = json.load(resultFP)
		resultFP.close()
		
		parseFP = open(parsefile)
		parse_data = json.load(parseFP)
		parseFP.close()
		
		tagged = False
		headed = False
		
		for c in parse_data['content']:
			if c["tagName"] == "Metadata":
				metadata = c["content"]	
		for m in metadata:
			if m["tagName"] == "Title":
				mettitle = m["content"]
				print mettitle
			if m["tagName"] == "Pages":
				numpages = m["content"]
		
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
						tagged = True
					if test["id"] == "core.MultiPageDocumentsMustHaveHeaders":
						headed = True
				elif (tag["result"]==2):
					nfail += 1
				elif (tag["result"]==3):
					nins += 1	
			
			if category == 0:
				continue
			category -= 1	
				
			rnum[category] += 1
			rtitle[category].append([test["title"], npass, nfail, nins])
			rtest[category].append(ntest)
			rpass[category].append(npass)
			rfail[category].append(nfail)
			rinspect[category].append(nins)
				
		content = []
		content.append(["Link"])
		content.append(["Figure"])
		content.append(["Form Control"])
		content.append(["Header"])
		content.append(["Table"])
		
		tot_test = 0
		tot_pass = 0
		tot_fail = 0
		tot_ins = 0
		for i in range(0,5):
			if sum(rtest[i]) > 0:
				content[i].append(sum(rtest[i])/rnum[i])
			else:
				content[i].append(0)
			content[i].append(rtitle[i])
			tot_test += sum(rtest[i])
			tot_pass += sum(rpass[i])
			tot_fail += sum(rfail[i])
			tot_ins += sum(rinspect[i])
		
		if tot_fail == 0:
			message = "<span style = \"color:green\">The document is accessible</span>"	
		form = setup_notes_form(request, uid, notes, fileObj)
		message = content
		return render_to_response("reports/summaryview.html", locals(), context_instance=RequestContext(request))
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displaytreeview(request, uid):
	currentTab = "tree"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	tags = "<div class=\"css-treeview\">"
	tags += writeTag(parsefile, "tags")
	tags += "</div>"
	return render_to_response("reports/treeview.html", locals())

def displaylinks(request, uid):
	currentTab = "links"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	[ruleRows, tableRows] = getData(parsefile, resultfile, uid, 1)
	name = "Link"
	return render_to_response("reports/rowView.html", locals())

def displayfigures(request, uid):
	currentTab = "img"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	[ruleRows, tableRows] = getData(parsefile, resultfile, uid, 2)
	name = "figure"
	return render_to_response("reports/rowView.html", locals())

def displayforms(request, uid):
	currentTab = "form"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	[ruleRows, tableRows] = getData(parsefile, resultfile, uid, 3)
	name = "form control"
	return render_to_response("reports/formview.html", locals())

def displaybookmark(request, uid):
	currentTab = "bm"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	tags = "<div class=\"css-treeview\">"
	tags += writeTag(parsefile, "Bookmarks")
	tags += "</div>"
	return render_to_response("reports/treeview.html", locals())

def displaytables(request, uid):
	currentTab = "tbl"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)	
	[ruleRows, output] = getTable(parsefile, resultfile)
	return render_to_response("reports/tableview.html", locals())
	
def displayformtree(request, uid):
	currentTab = "formtree"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	result = open(parsefile)
	base = json.loads(result.read())
	output = '<a href="javascript:check_all()">Expand All</a>'
	output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
	output += "<div class=\"css-treeview\">"
	output += writeNode2(base, "Form")
	output += "</div>"
	return render_to_response("reports/treeview.html", locals())
