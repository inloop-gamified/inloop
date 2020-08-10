from defusedxml import ElementTree

from inloop.medics.models import Violation, Rule
from inloop.solutions.models import Solution, get_upload_path_solution

from pathlib import PurePath

from typing import List

class CheckstyleParser:
    def __init__(self, xmlString: str):
        self.xmlString = xmlString

    def priority_from_severity(self, severity: str) -> str:
        if severity == 'info':
            return 'information'
        return severity

    def parse(self, solution: Solution) -> List[Violation]:
        root = ElementTree.fromstring(self.xmlString)
        violations = []
        for file in root.findall('.//file'):
            file_path = file.attrib.get('name')
            solution_file_name = PurePath(file_path).name
            solution_file_upload_path = get_upload_path_solution(solution, solution_file_name)
            solution_file = solution.solutionfile_set.get(file=solution_file_upload_path)
            for error in file.findall('error'):
                priority = self.priority_from_severity(error.attrib.get('severity'))
                check_uri = error.attrib.get('source')
                check_name = check_uri.split('.')[-1]
                rule_name = check_name.replace('Check', '')
                try:
                    rule = Rule.objects.get(identifier=rule_name)
                except Rule.DoesNotExist:
                    continue
                violations.append(Violation(
                    message=error.attrib.get('message'),
                    priority=priority,
                    start_line = error.attrib.get('line'),
                    end_line = error.attrib.get('line'),
                    start_column=error.attrib.get('column'),
                    end_column=error.attrib.get('column'),
                    rule=rule,
                    solution=solution,
                    solution_file=solution_file
                ))
        return violations
