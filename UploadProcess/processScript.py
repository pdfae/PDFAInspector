#!/usr/bin/env python2.7
"""
	Script to process PDF files to JSON output and result files

	This script is executed in the background by the Django web frontend but
	can also be used to generate results from a command line.
"""
import sys
import os
import subprocess
import shlex

if (len(sys.argv) > 4):
	# XXX: The jar and Python script paths should be hard coded relative to THIS file
	#      and we should use Pythons' really nice directory management to find them.
	PDF_JAR = sys.argv[1].strip('\"')
	PYTHON_SCRIPT = sys.argv[2].strip('\"')
	filepath = sys.argv[3].strip('\"')
	filename = sys.argv[4].strip('\"')
	pdf_file = "\"" + filepath + filename + "\""

	# Generate file names for the output files
	parse_file = "\"" + filepath + "json-" + filename.rpartition('.pdf')[0] + ".json" + "\""
	result_file = filepath + "result-" + filename.rpartition('.pdf')[0] + ".json"

	# Open the result file (rules processing) for writes
	result_file_object = open(result_file,'w')

	command1 = "java -jar " + PDF_JAR + " " + pdf_file
	command2 = "python2.7 "+ PYTHON_SCRIPT + " " + parse_file

	# Execute the PDF to JSON/XML converter
	p = subprocess.Popen(shlex.split(command1))
	p.wait()
	# XXX: We should set a time out for this for extremely large PDFs...

	# Run the rules processor
	q = subprocess.Popen(shlex.split(command2), stdout = result_file_object)

	# Get rid of the PDF file
	os.remove(pdf_file.strip('\"'))

	# Wait for the rules processor to finish
	q.wait()

	# Close the generated file
	result_file_object.close()
