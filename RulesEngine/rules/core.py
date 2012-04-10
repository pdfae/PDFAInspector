"""
Standard WCAG rules
"""
import Rules
import sys

class DocumentMustBeTagged(Rules.Rule):
	"""
		Any document should contain tags.
	"""
	title    = "Documents Must Be Tagged"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.DocumentLevel

	@staticmethod
	def applies(tag):
		"""Applies to any document"""
		return (tag.tagName == "tags")
	@staticmethod
	def validation(tag):
		if len(tag.content) > 0:
			return (Rules.Pass, "Document contains tags", [])
		return (Rules.Violation, "Document does not contain tags", [])

class DocumentShouldBeTitled(Rules.Rule):
	"""
		A document should have a title.
	"""
	title    = "Documents Should Be Titled"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.DocumentLevel

	@staticmethod
	def applies(tag):
		"""Applies to any document"""
		return (tag.tagName == "Metadata")

	@staticmethod
	def validation(tag):
		for child in tag.content:
			if child.tagName == "Title" and not child.text == "":
				return (Rules.Pass, "Document has a title", [])
		return (Rules.Violation, "Document does not have a title", [])

class DocumentMustHaveALanguageSet(Rules.Rule):
	"""
		The language should be specified in every document
	"""
	title    = "Documents Must Have A Language Set"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.DocumentLevel

	@staticmethod
	def applies(tag):
		"""Applies to any document"""
		return (tag.tagName == "Metadata")

	@staticmethod
	def validation(tag):
		for child in tag.content:
			if child.tagName == "Language" and not child.text == "":
				return (Rules.Pass, "Language set", [])
		return (Rules.Violation, "Language not set", [])

class DocumentsMustHaveAHeaderPerSevenPages(Rules.Rule):
	"""
		A document must have at least one header tag for every 7 pages it has.
	"""
	title    = "Documents must have a header per seven pages"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.DocumentLevel

	@staticmethod
	def applies(tag):
		"""Applies to any multi-page document"""
		if not tag.parent == None and tag.parent.parent == None and tag.tagName == "tags":
			for metadata in tag.parent.content[1].content:
				if metadata.tagName == "Pages":
					return (int(metadata.text) >= 7)
		return False

	@staticmethod
	def helper(tag, required, found):
		if tag.tagName in Rules.TagTypes.Heading:
			found = found + 1
		if found >= required:
			return True
		for child in tag.content:
			result = DocumentsMustHaveAHeaderPerSevenPages.helper(child,required,found)
			if result == True:
				return result
		return False


	@staticmethod
	def validation(tag):
		numHeaders = 1
		for metadata in tag.parent.content[1].content:
			if metadata.tagName == "Pages":
				numHeaders = int(metadata.text) / 7
		result = DocumentsMustHaveAHeaderPerSevenPages.helper(tag,numHeaders,0)
		if result == True:
			return (Rules.Pass, "Document has enough headers", [])
		return (Rules.Violation, "Document does not have enough headers", [])
		
class LinksMustContainTextContent(Rules.Rule):
	"""
		A link must contain some text content.
	"""
	title    = "Links Must Contain Text Content"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Links

	@staticmethod
	def applies(tag):
		""" Only applies to links """
		return (tag.tagName in Rules.TagTypes.Link)

	@staticmethod
	def validation(tag):
		if tag.text == "":
			return (Rules.Violation, "Link does not contain text content", [])
		return (Rules.ManualInspection, "Link text must describe target of the link", [])

class ImagesMustHaveAltText(Rules.Rule):
	"""
		Images must contain alternative text.
	"""
	title    = "Images Must Have Alt-Text"
	severity = Rules.Violation
	wcag_id  = "7.1"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Images

	@staticmethod
	def applies(tag):
		""" Only applies to images """
		return (tag.tagName in Rules.TagTypes.Image and (tag.parent and tag.parent.tagName != 'Images'))

	@staticmethod
	def validation(tag):
		for attr in tag.attributes:
			if attr.has_key("Alt"):
				return (Rules.ManualInspection, "Figure alt-text must describe the figure", [])
		return (Rules.Violation, "Does not have alt-text", [])

class FormElementsMustHaveTooltips(Rules.Rule):
	"""
		The Tooltip property must be set in all form elements
	"""
	title    = "Form Elements Must Have Tooltips"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Forms

	@staticmethod
	def applies(tag):
		""" Only applies to form elements """
		return (tag.parent != None and tag.parent.tagName == "Form")

	@staticmethod
	def validation(tag):
		for child in tag.content:
			if child.tagName == "Tooltip":
				if tag.tagName == "Radiobutton":
					return (Rules.ManualInspection, "Tooltip must describe both the response indicated by the button and the question responds to", [])
				return (Rules.ManualInspection, "Tooltip must describe the purpose of the control", [])
		return (Rules.Violation, "Form element has no tooltip", [])

class TablesMustHaveHeaders(Rules.Rule):
	"""
		The first row of any table must be header cells
	"""
	title    = "Tables Must Have Headers"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Tables

	@staticmethod
	def applies(tag):
		""" Only applies to tables """
		return (tag.tagName in Rules.TagTypes.Table)

	@staticmethod
	def validation(tag):
		for child in tag.content:
			if child.tagName in Rules.TagTypes.TableRow:
				for grandchild in child.content:
					if not grandchild.tagName in Rules.TagTypes.TableHeader:
						return (Rules.Violation, "First row contains non-header element " + grandchild.tagName, [])
				return (Rules.Pass, "First row of table consists of header cells", [])
		return (Rules.Violation, "No table row found", [])

class TablesMustContainDataCells(Rules.Rule):
	"""
		Any table must contain at least one data cell
	"""
	title    = "Tables Must Contain Data Cells"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Tables

	@staticmethod
	def applies(tag):
		""" Only applies to tables """
		return (tag.tagName in Rules.TagTypes.Table)

	@staticmethod
	def validation(tag):
		if tag.tagName in Rules.TagTypes.TableData:
			return (Rules.Pass, "Table contains data cells", [])
		for child in tag.content:
			result = TablesMustContainDataCells.validation(child)
			if result[0] == Rules.Pass:
				return result
		return (Rules.Violation, "Table does not contain data cells", [])

class TableCellsMustContainContent(Rules.Rule):
	"""
		Any data or header cell in a table must contain some content
	"""
	title    = "Table Cells Must Contain Content"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Tables

	@staticmethod
	def applies(tag):
		""" Only applies to tables """
		return (tag.tagName in Rules.TagTypes.TableData or tag.tagName in Rules.TagTypes.TableHeader)

	@staticmethod
	def validation(tag):
		if len(tag.content) > 0:
			return (Rules.Pass, "Cell contains content", [])
		return (Rules.Violation, "Cell does not contain content", [])

class HeadersMustContainTextContent(Rules.Rule):
	"""
		Any header must contain some non-null text content
	"""
	title    = "Headers Must Contain Text Content"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Headers

	@staticmethod
	def applies(tag):
		""" Only applies to headers """
		return (tag.tagName in Rules.TagTypes.Heading)

	@staticmethod
	def validation(tag):
		if tag.text == "":
			return (Rules.Violation, "Header does not contain text content", [])
		return (Rules.ManualInspection, "Header text should describe the corresponding section", [])

class BookmarksMustDescribeTheRelevantPartOfTheDocument(Rules.Rule):
	"""
		Bookmarks must describe the section of the document to which they link
	"""
	title    = "Bookmarks Must Describe The Relevant Part Of The Document"
	severity = Rules.ManualInspection
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Bookmarks

	@staticmethod
	def applies(tag):
		""" Only applies to bookmarks """
		while not tag.parent == None:
			if tag.parent.tagName == "Bookmarks":
				return True
			tag = tag.parent
		return False

	@staticmethod
	def validation(tag):
		return (Rules.ManualInspection, "Bookmarks should describe the corresponding section", [])
