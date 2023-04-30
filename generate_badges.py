import anybadge
import json

def create_badge(value, label, filename, thresholds):
    badge = anybadge.Badge(label, value, thresholds=thresholds)
    badge.write_badge(filename)

def get_pylint_score(filename):
    with open(filename, 'r') as f:
        pylint_data = json.load(f)
    score = pylint_data[0]['score']
    return score

def get_test_coverage(filename):
    with open(filename, 'r') as f:
        for line in f:
            if 'TOTAL' in line:
                coverage_line = line
                break
    coverage_percentage = float(coverage_line.split()[-1].strip('%'))
    return coverage_percentage

def get_pep8_score(filename):
    with open(filename, 'r') as f:
        total_errors = sum(int(line.split()[0]) for line in f)
    return total_errors

def main():
    pylint_score = get_pylint_score('pylint-report.json')
    test_coverage = get_test_coverage('coverage.xml')
    pep8_compliance = get_pep8_score('flake8-report.txt')

    code_quality_thresholds = {50: 'red', 70: 'orange', 85: 'yellow', 95: 'green'}
    test_coverage_thresholds = {50: 'red', 70: 'orange', 85: 'yellow', 95: 'green'}
    pep8_compliance_thresholds = {2: 'red', 4: 'orange', 6: 'yellow', 8: 'green'}

    create_badge(pylint_score, 'Code Quality', 'code_quality_badge.svg', code_quality_thresholds)
    create_badge(test_coverage, 'Test Coverage', 'test_coverage_badge.svg', test_coverage_thresholds)
    create_badge(pep8_compliance, 'PEP8', 'pep8_badge.svg', pep8_compliance_thresholds)

if __name__ == '__main__':
    main()
