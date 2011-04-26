import os
import simplejson as json

from django.core.files.storage import default_storage

from web.pdfevaluator.models import *
from web.pdfevaluator.file_name_operation import *


def _process(file_path):
    os.system('java -jar /var/www/django/pdfainspector/web/files/PdfAInspector.jar /var/www/django/pdfainspector/web/'+file_path+' >> /var/www/django/pdfainspector/web/files/pdfs/process.txt')

    #getting results file
    path_parts = get_path_parts(file_path)
    result_directory = path_parts[FilePart.directory]
    result_file_name = 'result_'+path_parts[FilePart.file_name]+'.json'
    result_file_path = result_directory + result_file_name

    return result_file_path

def _save_report(file_path, file_name, report_data, user, ruleset):

    report = Report(user=user, 
                    ruleset=ruleset, 
                    file_path = file_path,
                    file_name = file_name,
                    sect = int(report_data['TagCount']['sect']),
                    h1 = int(report_data['TagCount']['h1']),
                    h2 = int(report_data['TagCount']['h2']),
                    h3 = int(report_data['TagCount']['h3']),
                    h4 = int(report_data['TagCount']['h4']),
                    h5 = int(report_data['TagCount']['h5']),
                    h6 = int(report_data['TagCount']['h6']),
                    p = int(report_data['TagCount']['p']),
                    caption = int(report_data['TagCount']['caption']),
                    table = int(report_data['TagCount']['table']),
                    figure = int(report_data['TagCount']['figure']),
                    l = int(report_data['TagCount']['l']),
                    form = int(report_data['TagCount']['form']),
                    bookmark = int(report_data['TagCount']['bookmark'])
                    )
    report.save()

    for rule_result in report_data["Results"]:
        rule = Rule.objects.filter(ruleset=ruleset).get(rule_id=rule_result['rule_id'])

        rule.save()

        for rule_result in rule_result['test_results']:

            passed = 'V'
            if rule_result['passed'] == 'true':
                passed = 'P'

            result = Result(report = report,
                            rule=rule,
                            result=passed,
                            message=rule_result['message']
                            )
            result.save()

    return report


def evaluate_pdf(file_path, file_name, user, ruleset):
    result_file_path = _process(file_path)

    rules_as_json = json.load(default_storage.open(result_file_path))

    report = _save_report(file_path, file_name, rules_as_json, user, ruleset)

    return report 
