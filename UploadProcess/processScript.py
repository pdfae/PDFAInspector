
import sys
import os
import subprocess
import shlex

if (len(sys.argv) > 4):
	PDF_JAR = sys.argv[1].strip('\"')
	PYTHON_SCRIPT = sys.argv[2].strip('\"')
	filepath = sys.argv[3].strip('\"')
	filename = sys.argv[4].strip('\"')
	
	pdf_file = "\"" + filepath + filename + "\""
	parse_file = "\"" + filepath + "json-" + filename.rpartition('.pdf')[0] + ".json" + "\""
	result_file = filepath + "result-" + filename.rpartition('.pdf')[0] + ".json"
	result_file_object = open(result_file,'w')
	
	command1 = "java -jar " + PDF_JAR + " " + pdf_file
	command2 = "python2.7 "+ PYTHON_SCRIPT + " " + parse_file
	
	p = subprocess.Popen(shlex.split(command1))
	
	p.wait()
	q = subprocess.Popen(shlex.split(command2), stdout = result_file_object)
	
	os.remove(pdf_file.strip('\"'))
	
	q.wait()
	result_file_object.close()