from web.pdfevaluator.models import Ruleset, Rule

def save_ruleset(dictionary, file_name):
	new_ruleset = Ruleset(file_name = file_name)	
	new_ruleset.save()

	if dictionary.has_key("Rules"):
		for rule in dictionary["Rules"]:
			new_rule = Rule(rule_id = rule["id"],
							title = rule["title"],
							wcag_id = rule["wcag_id"],
							sect508_id = rule["sect508_id"],
							message = rule["message"],
							ruleset = new_ruleset)
			new_rule.save()

	return new_ruleset


