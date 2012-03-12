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
	category = Rules.Categories.DocumentLevel

	@staticmethod
	def applies(tag):
		"""Applies to any document"""
		return (tag.tagName == "tags")
	@staticmethod
	def validation(tag):
		if len(tag.content) > 0:
			return (Rules.Pass, "The document has tags", [])
		return (Rules.Violation, "The document has no tags", [])

class ThisImageIsAnImage(Rules.Rule):
	"""
		If it's an image, it passes!
	"""
	title    = "Images Must Be Images"
	severity = Rules.Violation
	wcag_id  = "n/a"
	category = Rules.Categories.Images

	@staticmethod
	def applies(tag):
		""" Only applies to images """
		return (tag.tagName in Rules.TagTypes.Image and (tag.parent and tag.parent.tagName != 'Images'))

	@staticmethod
	def validation(tag):
		# It's an image!
		return (Rules.Pass, "Is an image.", [])

class ImagesMustHaveAltText(Rules.Rule):
	"""
		If it's an image, it must have alt-text.
	"""
	title    = "Images Must Have Alt-Text"
	severity = Rules.Violation
	wcag_id  = "7.1"
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

