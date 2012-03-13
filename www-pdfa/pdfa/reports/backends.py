from django.shortcuts import *
from settings import *
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

def writeNode2 (node, depth=0):
	print "depth =" + unicode(depth)
	nodetag = node["tagName"]
	print nodetag
	uid = unicode(uuid.uuid4());
	output = "<table class = \"fancy\"><tr><td><ul><li><input type=checkbox id=\""+uid+"\"/><label for=\""+uid+"\"><b>"+nodetag+"</b></label><ul><li>\n<i>\n"
	
	attr = []
	for i in node["attributes"]:
		for j,k in i.iteritems():
			attr.append(unicode(j) + "=" + unicode(k))
	output += ", ".join(attr)
	output += "</i></li>\n"
	for i in node["content"]:
		if not isinstance(i, basestring) and not isinstance(i, int):
			if i.has_key('text'):
				print ""
				output += "<li>" + unicode(i['text']) + "</li>"
			else:
				output += writeNode2(i,depth+1)
		else:
			output += "<li>" + unicode(i) + "</li>"
			
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
