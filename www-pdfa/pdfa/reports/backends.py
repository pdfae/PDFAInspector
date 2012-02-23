from django.shortcuts import *
from settings import *
from django.contrib.auth.decorators import login_required
import os

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

def parsehelper(node, tag_type):
	#print len(node)
	if len(node) == 1:
		print node[0]
		return
	for c in node:
		if (c["tagName"]==tag_type):
			parsehelper(c["content"], tag_type)
			
def writeNode (node, depth=0):
	print depth
	nodetags = node["tagName"]
	print nodetags
	output = "<div class='node n_" + str(depth) + "'><b>"+node["tagName"]+"</b><br />\n<i>\n"
	
	attr = []
	for i in node["attributes"]:
		for j,k in i.iteritems():
			attr.append(unicode(j) + "=" + unicode(k))
	output += ", ".join(attr)
	output += "</i><br />\n"
	for i in node["content"]:
		if not isinstance(i, basestring) and not isinstance(i, int):
			if i.has_key('text'):
				output += str(i['text'])
			else:
				output += writeNode(i,depth+1)
	output += "</div>"
	return output