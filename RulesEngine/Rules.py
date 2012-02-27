"""
	Rule Information
"""

# Rule results
NotSet    = 0
Pass      = 1
Violation = 2

# Rule tags
class TagTypes():
	Container = ["Document","Part","Div","Art","Sect"]
	Heading = ["H1","H2","H3","H4","H5","H6"]
	Paragraph = ["P"]
	List = ["L"]
	ListItem = ["LI"]
	Label = ["LBL"]
	ListItemBody = ["LBody"]
	Caption = ["Caption"]
	SpecialText = ["BlockQuote","Index","TOC","TOCI"]
	Table = ["Table"]
	TableRow = ["TR"]
	TableData = ["TD"]
	TableHeader = ["TH"]
	Inline = ["BibEntry","Quote","Span"]
	Image = ["Figure"]
	Form = ["Form"]
	SpecialInline = ["Code","Formula","Link","Note","Reference"]


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
