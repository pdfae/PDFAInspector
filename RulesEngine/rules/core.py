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
			if child.tagName == "Title":
				return (Rules.Pass, "Document has a title", [])
		return (Rules.Violation, "Document does not have a title", [])

class MultiPageDocumentsMustHaveHeaders(Rules.Rule):
	"""
		A document longer than one page must have at least one header.
	"""
	title    = "Multi Page Documents Must Have Headers"
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
					return (int(metadata.text) > 1)
		return False

	@staticmethod
	def validation(tag):
		if tag.tagName in Rules.TagTypes.Heading:
			return (Rules.Pass, "Document contains headers", [])
		for child in tag.content:
			result = MultiPageDocumentsMustHaveHeaders.validation(child)
			if result[0] == Rules.Pass:
				return result
		return (Rules.Violation, "Document does not contain headers", [])

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
		return (Rules.Pass, "Header contains text content", [])
