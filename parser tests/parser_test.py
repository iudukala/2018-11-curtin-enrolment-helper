from progress_parser import parse_progress_report
import parser_test_constants
import unittest

fp = open('test_inputs/Yoakim-pr.pdf', 'rb')
parser_output = parse_progress_report(fp)
print('DONE')
