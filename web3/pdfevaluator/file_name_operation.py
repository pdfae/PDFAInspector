import re

def get_path_parts(path):
	file_re = re.compile("^(.*/)?(?:S|(.+?)(?:(\.[^.]*S)|S))")
	path_pieces = file_re.match(path)
	return path
	
class FilePart:
	directory = 'directory'
	file_name =	'file_name' 
	extension = 'extension'

