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
		return (Rules.Violation, "Add tags to the document.", [])

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
				return (Rules.Pass, "Document has a title", [child.text])
		return (Rules.Violation, "Set the document title.", [])

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
			if child.tagName == "Language" and not child.text == "None":
				return (Rules.Pass, "Language set", [child.text])
		return (Rules.Violation, "Set the document's language.", [])

class DocumentsMustHaveAHeadingPerSevenPages(Rules.Rule):
	"""
		A document must have at least one heading tag for every 7 pages it has.
	"""
	title    = "Documents must have a heading per seven pages"
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
	def helper(tag, found):
		for child in tag.content:
			found = found + DocumentsMustHaveAHeadingPerSevenPages.helper(child,found)
		if HeadingsMustContainTextContent.applies(tag):
			found = found + 1
		return found

	@staticmethod
	def validation(tag):
		neededHeadings = 0
		for metadata in tag.parent.content[1].content:
			if metadata.tagName == "Pages":
				neededHeadings = int(metadata.text) / 7
		foundHeadings = DocumentsMustHaveAHeadingPerSevenPages.helper(tag,0)
		if foundHeadings >= neededHeadings:
			return (Rules.Pass, "Document has enough headings", [str(foundHeadings)])
		return (Rules.Violation, "Add more headings to the document.", ["Needs " + str(neededHeadings - foundHeadings) + " more headings."])

class NonFigureTagsMustContainContent(Rules.Rule):
	"""
		A non-figure tag must not be empty. It must contain text content or another tag.
	"""
	title    = "TagsMustContainContent"
	severity = Rules.Warning
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.DocumentLevel

	@staticmethod
	def applies(tag):
		""" Only applies to tags """
		if tag.tagName in Rules.TagTypes.Figure:
			return False
		while not tag.parent == None:
			if tag.parent.tagName == "tags":
				return True
			tag = tag.parent
		return False

	@staticmethod
	def validation(tag):
		if tag.text == "" and not tag.content:
			return (Rules.Warning, "Place either text content or another tag inside this tag. Or, remove this empty tag.", [])
		return (Rules.Pass, "Tag contains content", [tag.text])	

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
			children = tag.content
			for child in children:
				result = LinksMustContainTextContent.validation(child)
				if result[0] == Rules.Pass:
					return result
			return (Rules.Violation, "Add text content to the link.", [])
		return (Rules.Pass, "Link contains text content", [tag.text])

class LinkTextMustDescribeItsTarget(Rules.Rule):
	"""
		A link's text should describe the page/object it links to.
	"""
	title    = "Link Text Must Describe Its Target"
	severity = Rules.ManualInspection
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Links

	@staticmethod
	def applies(tag):
		""" Only applies to links with text content """
		return LinksMustContainTextContent.applies(tag) and LinksMustContainTextContent.validation(tag)[0] == Rules.Pass

	@staticmethod
	def validation(tag):
		return (Rules.ManualInspection, "Ensure that the link's text describes what it is linking to.", LinksMustContainTextContent.validation(tag)[2])

class FiguresMustHaveAltText(Rules.Rule):
	"""
		Figures must contain alternative text.
	"""
	title    = "Figures Must Have Alt-Text"
	severity = Rules.Violation
	wcag_id  = "7.1"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Figures

	@staticmethod
	def applies(tag):
		""" Only applies to figures """
		return (tag.tagName in Rules.TagTypes.Figure and (tag.parent and tag.parent.tagName != 'Figures'))

	@staticmethod
	def validation(tag):
		for attr in tag.attributes:
			if attr.has_key("Alt"):
				return (Rules.Pass, "Has alt-text", [attr["Alt"]])
		return (Rules.Violation, "Add an alternative text attribute to the figure.", [])


class FigureAltTextMustDescribeFigure(Rules.Rule):
	"""
		The alternative text of a figure must describe the figure
	"""
	title    = "Figure Alt-Text Must Describe Figure"
	severity = Rules.ManualInspection
	wcag_id  = "7.1"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Figures

	@staticmethod
	def applies(tag):
		""" Only applies to figures """
		return FiguresMustHaveAltText.applies(tag) and FiguresMustHaveAltText.validation(tag)[0] == Rules.Pass

	@staticmethod
	def validation(tag):
		# This manual-inspection rule always returns "ManualInspection" because it can not "fail".
		return (Rules.ManualInspection, "Ensure that the alternative text describes the figure.", FiguresMustHaveAltText.validation(tag)[2])


class FormControlsMustHaveTooltips(Rules.Rule):
	"""
		The Tooltip property must be set in all form controls
	"""
	title    = "Form Controls Must Have Tooltips"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Forms

	@staticmethod
	def applies(tag):
		""" Only applies to form controls """
		return (tag.parent != None and tag.parent.tagName == "Form")

	@staticmethod
	def validation(tag):
		for child in tag.content:
			if child.tagName == "Tooltip":
				return (Rules.Pass, "Form control has tooltip", [child.text])
		return (Rules.Violation, "Set the tooltip for this form control.", [])

class FormControlTooltipMustBeUnique(Rules.Rule):
	"""
		The tooltip of a form control must be unique within the document.
	"""
	title    = "Form Control Tooltip Must Be Unique"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Forms

	@staticmethod
	def applies(tag):
		""" Only applies to form controls with tooltips """
		return FormControlsMustHaveTooltips.applies(tag) and FormControlsMustHaveTooltips.validation(tag)[0] == Rules.Pass

	@staticmethod
	def validation(tag):
		foundOnce = False
		tooltip = ""
		for child in tag.content:
			if child.tagName == "Tooltip":
				tooltip = child.text
		form = tag.parent.content
		for control in form:
			for child in control.content:
				if child.tagName == "Tooltip":
					if child.text == tooltip:
						if foundOnce:
							return (Rules.Violation, "At least one other form control shares this tooltip. Change all but one of them to ensure uniqueness.", FormControlsMustHaveTooltips.validation(tag)[2])
						else:
							foundOnce = True
		return (Rules.Pass, "Tooltip is unique", [])

class FormControlTooltipMustDescribeFormControl(Rules.Rule):
	"""
		The tooltip of a form control must describe the purpose of the control.
	"""
	title    = "Form Control Tooltip Must Describe Form"
	severity = Rules.ManualInspection
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Forms

	@staticmethod
	def applies(tag):
		""" Only applies to form controls with tooltips """
		return FormControlsMustHaveTooltips.applies(tag) and FormControlsMustHaveTooltips.validation(tag)[0] == Rules.Pass

	@staticmethod
	def validation(tag):
		# This manual-inspection rule always returns "ManualInspection" because it can not "fail".
		if tag.tagName == "Radiobutton":
			return (Rules.ManualInspection, "Ensure that the tooltip both the response indicated by the button and the question responds to.", FormControlsMustHaveTooltips.validation(tag)[2])
		return (Rules.ManualInspection, "Ensure that the tooltip describes the purpose of this form control.", FormControlsMustHaveTooltips.validation(tag)[2])

class TablesMustHaveHeadings(Rules.Rule):
	"""
		The first row of any table must be heading cells
	"""
	title    = "Tables Must Have Headings"
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
					if not grandchild.tagName in Rules.TagTypes.TableHeading:
						return (Rules.Violation, "First row contains non-heading element " + grandchild.tagName + ". Consider changing to a TH.", [])
				return (Rules.Pass, "First row of table consists of heading cells", [])
		return (Rules.Violation, "Add a row of table heading (TH) elements to the table.", [])

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
		return (Rules.Violation, "Add data (TD) cells to the table.", [])

class TableCellsMustContainContent(Rules.Rule):
	"""
		Any data or heading cell in a table must contain some content
	"""
	title    = "Table Cells Must Contain Content"
	severity = Rules.Warning
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Tables

	@staticmethod
	def applies(tag):
		""" Only applies to tables """
		return (tag.tagName in Rules.TagTypes.TableData or tag.tagName in Rules.TagTypes.TableHeading)

	@staticmethod
	def validation(tag):
		if len(tag.content) > 0:
			return (Rules.Pass, "Cell contains content", [])
		return (Rules.Warning, "Add content to this table cell.", [])

class HeadingsMustContainTextContent(Rules.Rule):
	"""
		Any heading must contain some non-null text content
	"""
	title    = "Headings Must Contain Text Content"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Headings

	@staticmethod
	def applies(tag):
		""" Only applies to headings """
		if tag.tagName in Rules.TagTypes.H1:
			return True
		if tag.tagName in Rules.TagTypes.H2:
			return True
		if tag.tagName in Rules.TagTypes.H3:
			return True
		if tag.tagName in Rules.TagTypes.H4:
			return True
		if tag.tagName in Rules.TagTypes.H5:
			return True
		if tag.tagName in Rules.TagTypes.H6:
			return True
		return False

	@staticmethod
	def validation(tag):
		if tag.text == "":
			return (Rules.Violation, "Add some text content to this heading.", [])
		return (Rules.Pass, "Heading contains text content", [tag.text])

class HeadingsMustDescribeTheSection(Rules.Rule):
	"""
		A heading must describe the section it precedes.
	"""
	title    = "Headings Must Describe The Section"
	severity = Rules.ManualInspection
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Headings

	@staticmethod
	def applies(tag):
		""" Only applies to headings with text content """
		return HeadingsMustContainTextContent.applies(tag) and HeadingsMustContainTextContent.validation(tag)[0] == Rules.Pass

	@staticmethod
	def validation(tag):
		# This manual-inspection rule always returns "ManualInspection" because it can not "fail".
		return (Rules.ManualInspection, "Ensure that the heading describes the section it precedes.", HeadingsMustContainTextContent.validation(tag)[2])

class HeadingsSharingParentsMustHaveUniqueContent(Rules.Rule):
	"""
		A pair of headings which have the same parent heading must have different content.
	"""
	title    = "Headings Sharing Parents Must Have Unique Content"
	severity = Rules.Violation
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Headings

	@staticmethod
	def applies(tag):
		""" Only applies to headings """
		if tag.tagName in Rules.TagTypes.H1:
			return True
		if tag.tagName in Rules.TagTypes.H2:
			return True
		if tag.tagName in Rules.TagTypes.H3:
			return True
		if tag.tagName in Rules.TagTypes.H4:
			return True
		if tag.tagName in Rules.TagTypes.H5:
			return True
		if tag.tagName in Rules.TagTypes.H6:
			return True
		return False

	@staticmethod
	def getHeadingLevel(tag):
		if tag.tagName in Rules.TagTypes.H1:
			return 1
		if tag.tagName in Rules.TagTypes.H2:
			return 2
		if tag.tagName in Rules.TagTypes.H3:
			return 3
		if tag.tagName in Rules.TagTypes.H4:
			return 4
		if tag.tagName in Rules.TagTypes.H5:
			return 5
		if tag.tagName in Rules.TagTypes.H6:
			return 6
		return 7

	@staticmethod
	def validation(tag):
		siblings = tag.parent.content
		index = siblings.index(tag)
		level = HeadingsSharingParentsMustHaveUniqueContent.getHeadingLevel(tag)
		i = index - 1
		while i > 0:
			if HeadingsSharingParentsMustHaveUniqueContent.getHeadingLevel(siblings[i]) < level:
				break
			i = i - 1
		i = i + 1
		while i < len(siblings):
			level2 = HeadingsSharingParentsMustHaveUniqueContent.getHeadingLevel(siblings[i])
			if level2 < level:
				break
			elif level2 == level and not i == index:
				if siblings[i].text == tag.text:
					return (Rules.Violation, "At least one heading under the same parent has the same text as this one. Change the text of at least one of these headings to make them unique.", [tag.text])
			i = i + 1
		return (Rules.Pass, "Heading text is unique.", [tag.text])
		
class HeadingsShouldBeProperlyNested(Rules.Rule):
	"""
		Headings should be nested in the order H1, H2, H3, etc. They can go back in any order.
	"""
	title    = "Headings Should Be Properly Nested"
	severity = Rules.Warning
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Headings

	@staticmethod
	def applies(tag):
		""" Only applies to headings """
		if tag.tagName in Rules.TagTypes.H1:
			return True
		if tag.tagName in Rules.TagTypes.H2:
			return True
		if tag.tagName in Rules.TagTypes.H3:
			return True
		if tag.tagName in Rules.TagTypes.H4:
			return True
		if tag.tagName in Rules.TagTypes.H5:
			return True
		if tag.tagName in Rules.TagTypes.H6:
			return True
		return False

	@staticmethod
	def getHeadingLevel(tag):
		if tag.tagName in Rules.TagTypes.H1:
			return 1
		if tag.tagName in Rules.TagTypes.H2:
			return 2
		if tag.tagName in Rules.TagTypes.H3:
			return 3
		if tag.tagName in Rules.TagTypes.H4:
			return 4
		if tag.tagName in Rules.TagTypes.H5:
			return 5
		if tag.tagName in Rules.TagTypes.H6:
			return 6
		return 7

	@staticmethod
	def validation(tag):
		siblings = tag.parent.content
		index = siblings.index(tag)
		level = HeadingsShouldBeProperlyNested.getHeadingLevel(tag)
		if index == 0:
			if level == 1:
				return (Rules.Pass, "Heading is properly nested.", [])
			else:
				return (Rules.Warning, "Ensure this tag is only one level below its parent (H1->H2, etc.)", [])
		i = index - 1
		while i > 0:
			if HeadingsShouldBeProperlyNested.getHeadingLevel(siblings[i]) < level:
				break
			i = i - 1
		parent = siblings[i]
		if HeadingsShouldBeProperlyNested.getHeadingLevel(parent) == level - 1:
			return (Rules.Pass, "Heading is properly nested.", [])
		return (Rules.Warning, "Ensure this tag is only one level below its parent (H1->H2, etc.)", [])

class BookmarksMustDescribeTheRelevantPartOfTheDocument(Rules.Rule):
	"""
		Bookmarks must describe the section of the document to which they link.
	"""
	title    = "Bookmarks Must Describe The Relevant Part Of The Document"
	severity = Rules.ManualInspection
	wcag_id  = "n/a"
	wcag_level = Rules.WCAG.NotSet
	category = Rules.Categories.Bookmarks

	@staticmethod
	def applies(tag):
		""" Only applies to bookmarks with text """
		if tag.text == "":
			return False
		while not tag.parent == None:
			if tag.parent.tagName == "Bookmarks":
				return True
			tag = tag.parent
		return False

	@staticmethod
	def validation(tag):
		return (Rules.ManualInspection, "Ensure that the bookmark describes the bookmarked content.", [tag.text])
