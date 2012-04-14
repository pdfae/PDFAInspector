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

PDF_JAR = "../PdfInspector/lib/pdfainspector.jar"
RULES_SCRIPT = "../RulesEngine/RulesEngine.py"

if (len(sys.argv) > 1):
	# XXX: The jar and Python script paths should be hard coded relative to THIS file
	#      and we should use Pythons' really nice directory management to find them.
	dir = os.path.dirname(sys.argv[0])
	PDF_JAR = os.path.join(dir, PDF_JAR)
	RULES_SCRIPT = os.path.join(dir, RULES_SCRIPT)
	
	# Generate file names for the output files
	pdf_file = sys.argv[1]
	(fp,fname) = os.path.split(pdf_file)
	parse_file = os.path.join(fp, "json-" + fname.rsplit(".pdf")[0] + ".json")
	result_file = os.path.join(fp, "result-" + fname.rsplit(".pdf")[0] + ".json")

	command1 = "java -jar " + PDF_JAR + " " + pdf_file
	command2 = "python2.7 "+ RULES_SCRIPT + " " + parse_file
	
	# Execute the PDF to JSON/XML converter
	p = subprocess.Popen(shlex.split(command1))
	p.wait()
	# XXX: We should set a time out for this for extremely large PDFs...
	
	# Open the result file (rules processing) for writes
	result_file_object = open(result_file,'w')
	# Run the rules processor
	q = subprocess.Popen(shlex.split(command2), stdout = result_file_object)

	# Get rid of the PDF file
	os.remove(pdf_file.strip('\"'))

	# Wait for the rules processor to finish
	q.wait()

	# Close the generated file
	result_file_object.close()
