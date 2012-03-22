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
	severity = Rules.Warning
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
				#print child.content
				return (Rules.Pass, "Document has a title", [])
		return (Rules.Warning, "Document does not have a title", [])

class LinksMustHaveAltText(Rules.Rule):
	"""
		A link must contain alternative text.
	"""
	title    = "Links Must Have Alt-Text"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Links

	@staticmethod
	def applies(tag):
		""" Only applies to images """
		return (tag.tagName in Rules.TagTypes.Link)

	@staticmethod
	def validation(tag):
		for attr in tag.attributes:
			if attr.has_key("Alt"):
				return (Rules.Pass, "Has alt-text", [])
		return (Rules.Violation, "Does not have alt-text", [])

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
				return (Rules.Pass, "Has alt-text", [])
		return (Rules.Violation, "Does not have alt-text", [])

class FormElementsMustHaveNames(Rules.Rule):
	"""
		The Name property must be set in all form elements
	"""
	title    = "Form Elements Must Have Names"
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
			if child.tagName == "Name":
				return (Rules.Pass, "Form element has a name", [])
		return (Rules.Violation, "Form element has no name", [])

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
				return (Rules.Pass, "Form element has a tooltip", [])
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
		return (Rules.Warning, "No table row found", [])

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
			return TablesMustContainDataCells.validation(child)
		return (Rules.Violation, "Table does not contain data cells", [])
