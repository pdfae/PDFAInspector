"""
Standard WCAG rules
"""
import Rules
import sys

class ThisImageIsAnImage(Rules.Rule):
	"""
		If it's an image, it passes!
	"""
	title    = "Images Must Be Images"
	severity = Rules.Violation
	wcag_id  = "n/a"

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


