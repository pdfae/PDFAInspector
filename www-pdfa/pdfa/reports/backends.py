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

def writeNodeContent (node, depth=0):
	print "depth =" + unicode(depth)
	nodetag = node["tagName"]
	print nodetag
	output = "<div class='node n_" + unicode(depth) + "'><b>"+nodetag+":</b>\n"
	
	attr = []

	for i in node["content"]:
		if not isinstance(i, basestring) and not isinstance(i, int):
			output += "</i>\n"
			if i.has_key('text'):
				output += unicode(i['text'])
			else:
				output += writeNodeContent(i,depth+1)
		else:
			output += "<i>\n"
			output += unicode(i)
			output += "</i>\n"
	output += "</div>"
	return output

def getFormOutput(parsefile, resultfile):	
	output = ""
	if os.path.isfile(parsefile):
		filePointer = open(parsefile)
		parsedata = json.load(filePointer)
		filePointer.close()
		forms = []
		searchNode(parsedata, "Form", 0, forms)
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
		result_list = []
		count = 0
		for result in resultdata['results']:
			if result['category'] == 3:
				#output += unicode(result) + "<br><br>"
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
							page = 'Unknown'
						[name, tooltip] = getNameTooltip(content)
						url_list.append(tag_url)
						page_list.append(page)
						name_list.append(name)
						tooltip_list.append(tooltip)
					result_list.append([])	
					result_list[tag_count].append(tag)
					tag_count += 1	
				count +=1		
		if len(url_list) > 0:
			output += startTable(["Form URL","Page", "Name", "Tooltip", "Rule", "Result", "Message"])
			for url, page, name, tooltip, result in zip(url_list, page_list, name_list, tooltip_list, result_list):
				output += "<br><br>URL: " + unicode(url)
				output += "<br>Page: " + unicode(page)
				output += "<br>Name: " + unicode(name)
				output += "<br>Tooltip: " + unicode(tooltip)
				output += "<br>Result: " + unicode(result)
		else:
			output += "No form elements found"
	'''
	<table class="fancy">
	<tr>
		<th>
			Rule
		</th>
		<th>
			Tag URL
		</th>
		<th>
			Result
		</th>
		<th>
			Message
		</th>
	</tr>
	
	{% for test in tests %}
	<tr>
		{% if test.tags|length > 0 %}
			<td rowspan = "{{test.tags|length}}">
				{{ test.title }}
			</td>
			
			{% for tag in test.tags %}
				{% if forloop.first %}
				{% else %}
					<tr>
				{% endif %}
					<td>
						{{tag.tag}}
					</td>
					<td>
						{% if tag.result == 1 %}
							<FONT COLOR="006400"><b>
								pass
							</b></FONT>
						{% endif %}
						{% if tag.result == 2 %}
							<FONT COLOR="FF0000"><b>
								fail
							</b></FONT>
						{% endif %}
					</td>
					<td>
						{{tag.message}}
					</td>
				{% if forloop.first %}
				{% else %}
					</tr>
				{% endif %}
			{% endfor %}
		{% else %}
			<td>
				{{ test.title }}
			</td>
			<td>
				Test was not run on any tags
			</td>
			<td>
				N/A
			</td>
			<td>
				N/A
			</td>
		{% endif %}
	</tr>
	{% endfor %}
</table>-->
	'''
	#output += tag_url + ':<br>Page:' + 	unicode(page) + '<br>Name:' + unicode(name) + '<br>Tooltip:' + unicode(tooltip) + '<br>'				
	#output += unicode(url_list) + '<br><br>' + unicode(page_list) + '<br><br>' + unicode(name_list) + '<br><br>' + unicode(tooltip_list) + '<br><br>' + unicode(result_list) + "<br><br>"
	#output += unicode(resultdata['results'])
	return output

def startTable(header_list):
	string = "<table class=\"fancy\">\n<tr>"
	for header in header_list:
		string += "<th>" + header + "</th>\n"
	string += "</tr>\n"
	return string

def endTable():
	return "</table>\n"

def getNameTooltip(content):
	name = "Unknown"
	tooltip = "Unknown"
	for tag in content:
		if (tag['tagName'] == 'Name'):
			name = tag['content'][0]
		if (tag['tagName'] == 'Tooltip'):
			tooltip = tag['content'][0]	
	return [name, tooltip]	