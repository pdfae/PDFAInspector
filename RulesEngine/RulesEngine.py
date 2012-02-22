#!/usr/bin/env python
"""
	PDF Accessibility Inspector

	Core Rules Engine
"""

import os, sys, inspect, re, json
import Rules

packages = []
rules = []

def plural(n,pstr="s",sstr=""):
	"""
	Pluralize a string if n is > 1
	"""
	if n == 1:
		return sstr
	else:
		return _str

def readable(docstring):
	return re.sub(r'\s\s*', ' ', docstring).strip()

def load():
	"""
	Load/reload all rule packages and their contents.
	"""
	global rules, packages
	packages = []
	rules    = []
	for package in [x.replace(".py","") for x in os.listdir(os.path.join(sys.path[0], "rules")) if x.endswith(".py") and not x.startswith("__")]:
		print >> sys.stderr, "Loading package '%s'..." % (package),
		# Construct the true package name
		name = 'rules.' + package
		# Import it into scope
		__import__(name, globals(), locals(), [], -1)
		# And grab a reference to it
		_package = sys.modules[name]
		# Update its internal name for reference later
		_package._name = package
		# And add it to the available packages
		packages.append(_package)
		print >> sys.stderr, "[%s]" % _package.__doc__.strip()
		# Now load up all of its rules...
		for ruleName in [x for x in dir(_package) if inspect.isclass(_package.__dict__[x]) and (Rules.Rule in _package.__dict__[x].__bases__)]:
			# And initializethem appropriately.
			rule = _package.__dict__[ruleName]
			rule._name = "%s.%s" % (package, ruleName)
			rules.append(rule)
	print >> sys.stderr, "Loaded %d rule%s from %d package%s. Ready to process." % (len(rules), plural(len(rules)), len(packages), plural(len(packages)))

def recName(lst):
	return " > ".join([x.tagName for x in lst])

def generateTree(tag, parent=None):
	node = Rules.Tag()
	node.parent = parent
	node.tagName    = tag['tagName']
	if tag.has_key('text'):
		node.text       = tag['text']
	else:
		node.text = ""
	node.attributes = tag['attributes']
	node.content    = []
	for i in tag['content']:
		if not isinstance(i, basestring) and not isinstance(i, int):
			node.content.append(generateTree(i, node))
	return node

def runRecursive(outputTreeNode, rule, tag, parents=[]):
	path = parents[:]
	path.append(tag)
	if rule.applies(tag):
		print >> sys.stderr, "Running rule %s on %s" % (rule.title, recName(path))
		resultCode, message, args = rule.validation(tag)
		result = {}
		result['tag']     = recName(path)
		result['result']  = resultCode
		result['message'] = message
		result['args']    = args
		outputTreeNode['tags'].append(result)
	for i in tag.content:
		runRecursive(outputTreeNode, rule, i, path)

def process(json_object):
	"""
	Process a JSON object.
	"""
	inputTree  = generateTree(o)
	outputTree = {}
	outputTree['results'] = []
	for rule in rules:
		outNode = {}
		outNode['id'] = rule._name
		outNode['title'] = rule.title
		outNode['description'] = readable(rule.__doc__)
		outNode['tags'] = []
		print >> sys.stderr, "Running rule `%s` with description `%s`..." % (rule._name, readable(rule.__doc__))
		runRecursive(outNode, rule, inputTree)
		outputTree['results'].append(outNode)
	return json.dumps(outputTree)

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		# Need a file to work on...
		print >> sys.stderr, "%s: expected argument" % (sys.argv[0])
		sys.exit(1)
	print >> sys.stderr, "Processing file %s" % (sys.argv[1])
	load()
	f = open(sys.argv[1])
	o = json.load(f)
	f.close()
	print process(o)


