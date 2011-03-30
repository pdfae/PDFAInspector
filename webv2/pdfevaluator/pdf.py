import os

from web.pdfevaluator.models import *

def evaluate_pdf(file, user):
	parse_and_get_evaluation(file)

def parse_and_get_evaluation(file):
	#send through evaluation engine
	#read json file
	#return as dict
