"""
	Rule Information
"""

# Rule results
NotSet           = 0
Pass             = 1
Violation        = 2
ManualInspection = 3
Warning          = 4

# Rule Categories
class Categories():
	DocumentLevel    = 0
	Links            = 1
	Figures          = 2
	Forms            = 3
	Headers          = 4
	Tables           = 5
	Bookmarks        = 6

#WCAG Levels
class WCAG():
	NotSet = 0
	A      = 1
	AA     = 2
	AAA    = 3

# Rule tags
class TagTypes():
	Document = ["Document"]
	Part = ["Part"]
	Div = ["Div"]
	Art = ["Art"]
	Sect = ["Sect"]
	H1 = ["H1"]
	H2 = ["H2"]
	H3 = ["H3"]
	H4 = ["H4"]
	H5 = ["H5"]
	H6 = ["H6"]
	Paragraph = ["P"]
	List = ["L"]
	ListItem = ["LI"]
	Label = ["LBL"]
	ListItemBody = ["LBody"]
	Caption = ["Caption"]
	BlockQuote = ["BlockQuote"]
	Index = ["Index"]
	TOC = ["TOC"]
	TOCI = ["TOCI"]
	Table = ["Table"]
	TableRow = ["TR"]
	TableData = ["TD"]
	TableHeader = ["TH"]
	BibEntry = ["BibEntry"]
	Quote = ["Quote"]
	Span = ["Span"]
	Figure = ["Figure"]
	Form = ["Form"]
	Link = ["Link"]
	Code = ["Code"]
	Formula = ["Formula"]
	Note = ["Note"]
	Reference = ["Reference"]

class Rule():
	title = ""
	severity = NotSet
	wcag_id = ""
	wcag_level = WCAG.NotSet
	category = Categories.DocumentLevel
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
