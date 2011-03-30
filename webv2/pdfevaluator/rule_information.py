from web.pdfevaluator.models import Ruleset, Rule

def save_ruleset(dictionary):
	new_ruleset = Ruleset()	
	new_ruleset.save()

	if dictionary.has_key('Rules'):
		for rule in dictionary['Rules']:
			print rule
			new_rule = Rule(title=rule['title'],
							wcag_id = rule['wcag_id'],
							sect508_id = ['rule.sect508_id'],
							message = ['rule.message'],
							ruleset = new_ruleset)
			new_rule.save()

	return new_ruleset


