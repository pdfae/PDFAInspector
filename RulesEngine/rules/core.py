"""
Standard WCAG rules
"""
import Rules

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

