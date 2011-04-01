import os
import simplejson

from web.pdfevaluator.models import *
from web.pdfevaluator.file_name_operation import *


def _process(file_path):
	processor = '/var/www/django/pdfainspector/web/files/PdfAInspector.jar'
	absolute_file_loc = '/var/www/django/pdfainspector/'+file_path
	b = os.system('java -jar '+processor+' '+'absolute_file_loc >>'+
		'/var/www/django/pdfainspector/web/files/pdfs/process_output.txt')


def evaluate_pdf(file_path, file_name, user):
	_process(file_path)

	#getting results file
	path_parts = get_path_parts(file_path)
	#result_directory = path_parts[FilePart.directory]+'Tempfiles/results/'
	#result_file_name = 'result_'+path_parts[FilePart.file_name]
	#result_file_path = result_directory + result_file_name

	#result_file = open(result_file_path).read()

	return "hi"
