import re

def get_path_parts(path):
    #file_re = re.compile("^(.*/)?(?:S|(.+?)(?:(\.[^.]*S)|S))")
    file_re = re.compile("^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))")
    path_pieces = file_re.match(path)

    print path_pieces

    directory = path_pieces.group(1)
    file_name = path_pieces.group(2)
    extension = path_pieces.group(3)

    return {FilePart.directory : directory,
            FilePart.file_name : file_name,
            FilePart.extension : extension}
	
class FilePart:
	directory = 'directory'
	file_name =	'file_name' 
	extension = 'extension'

