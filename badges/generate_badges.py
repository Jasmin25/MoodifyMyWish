import anybadge
import json
import xml.etree.ElementTree as ET
from pylint.lint import Run


def create_badge(value, label, filename, thresholds):
    badge = anybadge.Badge(label, value, thresholds=thresholds)
    badge.write_badge(filename)


def get_pylint_score(pylint_target_file):
    results = Run([pylint_target_file], do_exit=False)
    return results.linter.stats.global_note


def get_test_coverage(coverage_file):
    tree = ET.parse(coverage_file)
    root = tree.getroot()
    coverage_percentage = 0

    try:
        lines_total = int(root.get('lines-valid'))
        lines_covered = int(root.get('lines-covered'))
        coverage_percentage = (lines_covered / lines_total) * 100
    except (ValueError, TypeError):
        print("Error: coverage.xml is empty or has an unexpected format.")
        return 0

    return round(coverage_percentage,2)


def get_pep8_score(flake8_report_file):
    with open(flake8_report_file, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
        total_errors = int(last_line.strip())
    return total_errors


def main():

    pylint_score = get_pylint_score('app.py')
    test_coverage = get_test_coverage('coverage.xml')
    pep8_compliance = get_pep8_score('flake8-report.txt')

    print(f"Code Quality: {pylint_score}")
    print(f"Test Coverage: {test_coverage}")
    print(f"PEP8 Compliance: {pep8_compliance}")

    badge_values = {
        'code_quality': pylint_score,
        'test_coverage': test_coverage,
        'pep8_compliance': pep8_compliance
    }

    with open('badges/badge_values.json', 'w') as file:
        json.dump(badge_values, file)

if __name__ == '__main__':
    main()
