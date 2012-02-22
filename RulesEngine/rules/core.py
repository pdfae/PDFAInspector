"""
Standard WCAG rules
"""
import Rules

class ImagesMustHaveAltTags(Rules.Rule):
	"""
		All images must have alt tags describing
		their content in text.
	"""
	title    = "Images Must Have Alt Tags"
	severity = Rules.Violation
	wcag_id  = "1.1.1"

	@staticmethod
	def applies(tag):
		""" Only applies to images """
		return (tag.tagName in Rules.TagTypes.Image)

	@staticmethod
	def validation(tag):
		# ...
		return (Rules.Pass, "Image has an alt tag.", [])

