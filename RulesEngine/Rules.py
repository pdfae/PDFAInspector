"""
	Rule Information
"""

# Rule results
NotSet    = 0
Pass      = 1
Violation = 2

# Rule tags
class TagTypes():
	Image = ["image","Image","Figure"]
	Paragraph = ["p"]

class Rule():
	title = ""
	severity = NotSet
	wcag_id = ""
	@staticmethod
	def applies(tag):
		return False
	@staticmethod
	def validation(tag):
		return (Pass, "This is not a real test", [])
	pass

class Tag():
	def __init__(self):
		self.tagName    = ""
		self.content    = []
		self.text       = ""
		self.attributes = []
		self.parent     = None
