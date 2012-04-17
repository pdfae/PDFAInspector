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
			if m["tagName"] == "Pages":
				numpages = m["content"]
			if m["tagName"] == "Language":
				language = m["content"]
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
				elif (tag["result"]==2):
					nfail += 1
				elif (tag["result"]==3):
					nins += 1	
				if test["id"] == "core.HeadersMustContainTextContent":
					headed = True
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
		content.append(["Link Tags"])
		content.append(["Figure (Image) Tags"])
		content.append(["Form Controls"])
		content.append(["Header Tags"])
		tables = []
		getNodesByName(parse_data, "Table", tables)
		content.append(["Table Tags"])
		
		tot_test = 0
		tot_pass = 0
		tot_fail = 0
		tot_ins = 0
		for i in range(0,5):
			if sum(rtest[i]) > 0:
				if i!=4:
					content[i].append(sum(rtest[i])/rnum[i])
				else:
					content[i].append(len(tables))
			else:
				content[i].append(0)
			content[i].append(rtitle[i])
			tot_test += sum(rtest[i])
			tot_pass += sum(rpass[i])
			tot_fail += sum(rfail[i])
			tot_ins += sum(rinspect[i])

		form = setup_notes_form(request, uid, notes, fileObj)
		message = content
		return render_to_response("reports/summaryview.html", locals(), context_instance=RequestContext(request))
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displaytreeview(request, uid):
	currentTab = "tree"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		tags = "<div class=\"css-treeview\">"
		tags += writeTag(parsefile, "tags")
		tags += "</div>"
		return render_to_response("reports/treeview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displaylinks(request, uid):
	currentTab = "links"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		name = "Link"
		info = "Text"
		[ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 1, name)
		return render_to_response("reports/rowView.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displayfigures(request, uid):
	currentTab = "img"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		name = "Figure"
		info = "Alt Text"
		[ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 2, name)
		return render_to_response("reports/rowView.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displayforms(request, uid):
	currentTab = "form"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		name = "Form Control"
		info = "Tooltip"
		[ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 3, name)
		return render_to_response("reports/formview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displayhead(request, uid):
	currentTab = "head"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		name = "Header"
		info = "Text"
		[ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 4, name)
		return render_to_response("reports/headerview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displaybookmark(request, uid):
	currentTab = "bm"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		tags = "<div class=\"css-treeview\">"
		tags += writeTag(parsefile, "Bookmarks")
		tags += "</div>"
		return render_to_response("reports/treeview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displaytables(request, uid):
	currentTab = "tbl"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)	
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		[ruleRows, tagged, num, output] = getTable(parsefile, resultfile)
		name = "table"
		return render_to_response("reports/tableview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())

def displayempty(request, uid):
	currentTab = "empty"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)	
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		resultFP = open(resultfile)
		result_data = json.load(resultFP)
		resultFP.close()
		parseFP = open(parsefile)
		parse_data = json.load(parseFP)
		parseFP.close()
		tests = result_data["results"]
		numfail = 0
		empty = []
		tagged = False
		tag_urls = {}
		getNodes(parse_data, 0, tag_urls)
		for test in tests:
			if test["id"] == "core.DocumentMustBeTagged" and test['tags'][0]['result'] == 1:
				tagged = True
			if test["id"] == "core.NonFigureTagsMustContainContent":	
				for tag in test["tags"]:
					if tag['result'] == 2:
						numfail += 1
						actual_tag = tag_urls[tag['tag']]
						tag['tagName'] = actual_tag['tagName']
						attr = []
						if 'attributes' in actual_tag:
							attr = actual_tag['attributes']
						for a in attr:
							if 'Page' in a:
								tag['page'] = a['Page']
						empty.append(tag)
		return render_to_response("reports/emptyview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())
		
def displayformtree(request, uid):
	currentTab = "formtree"
	[auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
	if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):	
		result = open(parsefile)
		base = json.loads(result.read())
		output = '<a href="javascript:check_all()">Expand All</a>'
		output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
		output += "<div class=\"css-treeview\">"
		output += writeNode2(base, "Form")
		output += "</div>"
		return render_to_response("reports/treeview.html", locals())
	else:
		return render_to_response("reports/summary_notfound.html", locals())