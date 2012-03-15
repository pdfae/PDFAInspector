from django.shortcuts import *
from settings import *
import json
from django.contrib.auth.decorators import login_required
import os
import uuid

def tablesummary(data, tests):
	rpass=0
	rwarning=0
	rfail=0
	rinspect=0
	for test in tests:
		print test
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

def parsespecific(file, tag_type):
	import json
	from pprint import pprint
	
	json_data = open (file)
	data = json.load(json_data)
	contentnode = data["content"]

	for c in contentnode:
		if (c["tagName"] == tag_type):
			return c
	return None
			
def writeNode (node, depth=0):
	print "depth =" + unicode(depth)
	nodetag = node["tagName"]
	print nodetag
	output = "<div class='node n_" + unicode(depth) + "'><b>"+nodetag+"</b><br />\n<i>\n"
	
	attr = []
	for i in node["attributes"]:
		for j,k in i.iteritems():
			attr.append(unicode(j) + "=" + unicode(k))
	output += ", ".join(attr)
	output += "</i><br />\n"
	for i in node["content"]:
		if not isinstance(i, basestring) and not isinstance(i, int):
			if i.has_key('text'):
				print ""
				output += unicode(i['text'])
			else:
				output += writeNode(i,depth+1)
		else:
			output += unicode(i)
	output += "</div>"
	return output

def writeNode2 (node, tagName, bool = False, depth=0, count = 0, url = ''):
	#print "depth =" + unicode(depth)
	nodetag = node["tagName"]
	url += unicode(count) + ":" + unicode(nodetag) 
	#print nodetag
	if (nodetag == tagName):
		bool = True
	uid = unicode(uuid.uuid4());
	output = ""
	if bool:
		output += "<table class = \"fancy\"><tr><td><ul><li><input type=checkbox id=\""+uid+"\" checked=\"checked\"/><label for=\""+uid+"\"><b><a name = \"" + url + "\" id = \"" + url + "\">"+nodetag+ "</a></b></label><ul><li>\n<i>\n"
	url += "/"
	attr = []
	for i in node["attributes"]:
		for j,k in i.iteritems():
			attr.append(unicode(j) + "=" + unicode(k))
	if bool:
		output += ", ".join(attr)
		output += "</i></li>\n"
	count = 0
	for i in node["content"]:	
		if not isinstance(i, basestring) and not isinstance(i, int):
			if i.has_key('text'):
				print ""
				if bool:
					output += "<li>" + unicode(i['text']) + "</li>"
			else:
				output += writeNode2(i, tagName, bool, depth+1, count, url)
		else:
			if bool:
				output += "<li>" + unicode(i) + "</li>"
		count += 1	
	if bool:
		output += "</ul></li></ul></td></tr></table>"
	return output

	
	
def searchNode (node, tagName, depth=0, a =[]):
	nodetag = node["tagName"]
	if (nodetag == tagName):
		a.append(node)
	else:
		for i in node["content"]:
			if not isinstance(i, basestring) and not isinstance(i, int):
				searchNode(i,tagName, depth+1, a)		

def getNodes(node, count=0, dict = {}, url='#'):
	nodetag = node["tagName"]
	url += unicode(count) + ":" + unicode(nodetag)
	dict[url] = node
	url += "/"
	count = 0
	for i in node["content"]:
		if not isinstance(i, basestring) and not isinstance(i, int):
			getNodes(i, count, dict, url)
		count += 1
def countNode (node):
	total = 0
	for i in node["content"]:
		if not isinstance(i, basestring) and not isinstance(i, int):
			total += 1 + countNode(i)
	return total

def generateFormData(parsefile, resultfile):
	if os.path.isfile(parsefile):
		filePointer = open(parsefile)
		parsedata = json.load(filePointer)
		filePointer.close()
		tag_urls = {}
		getNodes(parsedata, 0, tag_urls)
	if os.path.isfile(resultfile):
		filePointer = open(resultfile)
		resultdata = json.load(filePointer)
		filePointer.close()
		url_list = []
		page_list = []
		name_list = []
		tooltip_list = []
		rule_list = []
		result_list = []
		count = 0
		for result in resultdata['results']:
			if result['category'] == 3:
				#output += unicode(result) + "<br><br>"
				rule_list.append(result['title'])
				tag_count = 0
				for tag in result['tags']:
					if count == 0:
						tag_url = unicode(tag['tag'])
						parsed_tag = tag_urls[tag_url]
						attr = parsed_tag['attributes']
						content = parsed_tag['content']
						if len(attr) > 0:
							page = attr[0]['Page']
						else:
							page = 'null'
						[name, tooltip] = getNameTooltip(content)
						url_list.append(tag_url)
						page_list.append(page)
						name_list.append(name)
						tooltip_list.append(tooltip)
					result_list.append([])	
					result_list[tag_count].append(tag)
					tag_count += 1	
				count +=1
	return [zip(url_list, page_list, name_list, tooltip_list, result_list), rule_list]			

def generateImageData(parsefile, resultfile, c):
	if os.path.isfile(parsefile):
		filePointer = open(parsefile)
		parsedata = json.load(filePointer)
		filePointer.close()
		tag_urls = {}
		getNodes(parsedata, 0, tag_urls)
	if os.path.isfile(resultfile):
		filePointer = open(resultfile)
		resultdata = json.load(filePointer)
		filePointer.close()
		url_list = []
		page_list = []
		alt_list = []
		rule_list = []
		result_list = []
		count = 0
		for result in resultdata['results']:
			if result['category'] == c:
				rule_list.append(result['title'])
				tag_count = 0
				for tag in result['tags']:
					if count == 0:
						tag_url = unicode(tag['tag'])
						parsed_tag = tag_urls[tag_url]
						attr = parsed_tag['attributes']
						alt = 'null'
						page = 'null'
						for a in attr:
							if 'Alt' in a:
								alt = a['Alt']
							if 'Page' in a:
								page = a['Page']	
						url_list.append(tag_url)
						page_list.append(page)
						alt_list.append(alt)
					result_list.append([])	
					result_list[tag_count].append(tag)
					tag_count += 1	
				count +=1
	return [zip(url_list, page_list, alt_list, result_list), rule_list]			

def getFormOutput(parsefile, resultfile, uid):	
	output = ""
	[lists, rule_list] = generateFormData(parsefile, resultfile)
	if len(lists) > 0 and len(lists[0]) > 0:
		output += startTable(["Form","Page", "Name", "Tooltip", "Rule", "Result", "Message"])
		for url, page, name, tooltip, result in lists:
			output += "<tr>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += "<a href = \"/reports/" + uid + "/formtreeview/" + unicode(url) + "\">" + unicode(url.split(':')[-1]) + "</a>"
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(page)
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(name)
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(tooltip)
			output += "</td>\n"
				
			counter = 0
			for rule in result:
				if counter != 0:
					output += "<tr>\n"
				output += "<td>" + unicode(rule_list[counter]) + "</td>\n"
				output += "<td>" + getResultFromInt(rule['result']) + "</td>\n"
				output += "<td>" + unicode(rule['message']) + "</td>\n"
				if counter != 0:
					output += "</tr>\n"
				counter += 1
			output += "</tr>\n"
		output += endTable()	
	else:
		output += "No form elements found"
	return output

def getImageOutput(parsefile, resultfile, uid):
	output = ""
	[lists, rule_list] = generateImageData(parsefile, resultfile, 2)
	
	if len(lists) > 0 and len(lists[0]) > 0:
		output += startTable(["Tag","Page", "Alt text", "Rule", "Result", "Message"])
		for url, page, alt, result in lists:
			output += "<tr>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += "<a href = \"/reports/" + uid + "/treeview/" + unicode(url) + "\">" + unicode(url.split(':')[-1]) + "</a>"
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(page)
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(alt)
			output += "</td>\n"
				
			counter = 0
			for rule in result:
				if counter != 0:
					output += "<tr>\n"
				output += "<td>" + unicode(rule_list[counter]) + "</td>\n"
				output += "<td>" + getResultFromInt(rule['result']) + "</td>\n"
				output += "<td>" + unicode(rule['message']) + "</td>\n"
				if counter != 0:
					output += "</tr>\n"
				counter += 1
			output += "</tr>\n"
		output += endTable()	
	else:
		output += "No image tags found"
	return output

def getLinkOutput(parsefile, resultfile, uid):
	output = ""
	[lists, rule_list] = generateImageData(parsefile, resultfile, 1)
	if len(lists) > 0 and len(lists[0]) > 0:
		output += startTable(["Link","Page", "Alt text", "Rule", "Result", "Message"])
		for url, page, alt, result in lists:
			output += "<tr>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += "<a href = \"/reports/" + uid + "/treeview/" + unicode(url) + "\">" + unicode(url.split(':')[-1]) + "</a>"
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(page)
			output += "</td>\n"
				
			output += "<td rowspan = \"" + unicode(len(result)) + "\">\n"
			output += unicode(alt)
			output += "</td>\n"
				
			counter = 0
			for rule in result:
				if counter != 0:
					output += "<tr>\n"
				output += "<td>" + unicode(rule_list[counter]) + "</td>\n"
				output += "<td>" + getResultFromInt(rule['result']) + "</td>\n"
				output += "<td>" + unicode(rule['message']) + "</td>\n"
				if counter != 0:
					output += "</tr>\n"
				counter += 1
			output += "</tr>\n"
		output += endTable()	
	else:
		output += "No link tags found"
	return output


def startTable(header_list):
	string = "<table class=\"fancy\">\n<tr>"
	for header in header_list:
		string += "<th>" + header + "</th>\n"
	string += "</tr>\n"
	return string

def endTable():
	return "</table>\n"

def getResultFromInt(i):
	if i == 1:
		return "<FONT COLOR=\"006400\"><b>pass</b></FONT>"
	elif i == 2:
		return "<FONT COLOR=\"FF0000\"><b>fail</b></FONT>"
	elif i == 3:
		return "<b>warning</b>"
	elif i == 4:
		return "<b>manual inspection</b>"
	else:
		return ""

def getNameTooltip(content):
	name = "null"
	tooltip = "null"
	for tag in content:
		if (tag['tagName'] == 'Name'):
			name = tag['content'][0]
		if (tag['tagName'] == 'Tooltip'):
			tooltip = tag['content'][0]	
	return [name, tooltip]	