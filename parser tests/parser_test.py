from progress_parser import parse_progress_report
import parser_expected
import unittest

chienfeilin_expected = parser_expected.chienfeilin
darryl_expected = parser_expected.darryl
steven_expected = parser_expected.steven
eugene_expected = parser_expected.eugene
ximingwong_expected = parser_expected.ximingwong
yoakim_expected = parser_expected.yoakim


class TestUtil():
    def test_string(self, expected, actual):
        self.assertEqual(expected, actual)

    def test_ids(self, expected, actual):
        # Test if length of ID sets are equal
        self.assertEquals(len(expected), len(actual))
        # Test if each key in actual output is in the expected output
        for courseid in expected:
            self.assertTrue(courseid in actual)

    def test_course_versions(self, expected, actual):
        # Test that each course version is the same
        for id in expected:
            self.assertEqual(expected[id], actual[id])

    def test_unit_versions(self, expected, actual):
        # Test that each unit version is the same
        for unitid in expected:
            # If strict elective, check that theres no version
            if 'ELECTIVE' in unitid:
                self.assertFalse('ver' in actual[unitid])
            # If not strict elective, unit has a version so check it
            else:
                self.assertEqual(expected[unitid]['ver'], actual[unitid]['ver'])

    def test_unit_credits(self, expected, actual):
        # Test that each unit credit is the same
        for unitid in expected:
            self.assertEqual(expected[unitid]['credits'], actual[unitid]['credits'])

    def test_unit_status(self, expected, actual):
        # Test that each unit status is the same
        for unitid in expected:
            self.assertEqual(expected[unitid]['status'], actual[unitid]['status'])

    def test_unit_attempts(self, expected, actual):
        # Test that each unit attempts is the same
        for unitid in expected:
            self.assertEqual(expected[unitid]['attempt'], actual[unitid]['attempt'])


class TestCampbell(unittest.TestCase):
    expected = parser_expected.campbell
    actual = parse_progress_report(open('test_inputs/Campbell-pr.pdf', 'rb'))

    def test_name(self):
        TestUtil.test_string(self, self.expected['name'], self.actual['name'])

    def test_id(self):
        TestUtil.test_string(self, self.expected['id'], self.actual['id'])

    def test_date(self):
        TestUtil.test_string(self, self.expected['date'], self.actual['date'])

    def test_course_ids(self):
        TestUtil.test_ids(self, self.expected['course'], self.actual['course'])

    def test_course_versions(self):
        TestUtil.test_course_versions(self, self.expected['course'], self.actual['course'])

    def test_auto_ids(self):
        TestUtil.test_ids(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_versions(self):
        TestUtil.test_unit_versions(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_credits(self):
        TestUtil.test_unit_credits(self, self.expected['automatic'], self.actual['automatic'])

    def test_planned_ids(self):
        TestUtil.test_ids(self, self.expected['planned'], self.actual['planned'])

    def test_planned_versions(self):
        TestUtil.test_unit_versions(self, self.expected['planned'], self.actual['planned'])

    def test_planned_credits(self):
        TestUtil.test_unit_credits(self, self.expected['planned'], self.actual['planned'])

    def test_planned_status(self):
        TestUtil.test_unit_status(self, self.expected['planned'], self.actual['planned'])

    def test_units_ids(self):
        TestUtil.test_ids(self, self.expected['units'], self.actual['units'])

    def test_units_versions(self):
        TestUtil.test_unit_versions(self, self.expected['units'], self.actual['units'])

    def test_units_credits(self):
        TestUtil.test_unit_credits(self, self.expected['units'], self.actual['units'])

    def test_units_status(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

    def test_units_attempts(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

class TestChienFeiLin(unittest.TestCase):
    expected = parser_expected.chienfeilin
    actual = parse_progress_report(open('test_inputs/ChienFeiLin-pr.pdf', 'rb'))

    def test_name(self):
        TestUtil.test_string(self, self.expected['name'], self.actual['name'])

    def test_id(self):
        TestUtil.test_string(self, self.expected['id'], self.actual['id'])

    def test_date(self):
        TestUtil.test_string(self, self.expected['date'], self.actual['date'])

    def test_course_ids(self):
        TestUtil.test_ids(self, self.expected['course'], self.actual['course'])

    def test_course_versions(self):
        TestUtil.test_course_versions(self, self.expected['course'], self.actual['course'])

    def test_auto_ids(self):
        TestUtil.test_ids(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_versions(self):
        TestUtil.test_unit_versions(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_credits(self):
        TestUtil.test_unit_credits(self, self.expected['automatic'], self.actual['automatic'])

    def test_planned_ids(self):
        TestUtil.test_ids(self, self.expected['planned'], self.actual['planned'])

    def test_planned_versions(self):
        TestUtil.test_unit_versions(self, self.expected['planned'], self.actual['planned'])

    def test_planned_credits(self):
        TestUtil.test_unit_credits(self, self.expected['planned'], self.actual['planned'])

    def test_planned_status(self):
        TestUtil.test_unit_status(self, self.expected['planned'], self.actual['planned'])

    def test_units_ids(self):
        TestUtil.test_ids(self, self.expected['units'], self.actual['units'])

    def test_units_versions(self):
        TestUtil.test_unit_versions(self, self.expected['units'], self.actual['units'])

    def test_units_credits(self):
        TestUtil.test_unit_credits(self, self.expected['units'], self.actual['units'])

    def test_units_status(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

    def test_units_attempts(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

class TestDarryl(unittest.TestCase):
    expected = parser_expected.darryl
    actual = parse_progress_report(open('test_inputs/Darryl-pr.pdf', 'rb'))

    def test_name(self):
        TestUtil.test_string(self, self.expected['name'], self.actual['name'])

    def test_id(self):
        TestUtil.test_string(self, self.expected['id'], self.actual['id'])

    def test_date(self):
        TestUtil.test_string(self, self.expected['date'], self.actual['date'])

    def test_course_ids(self):
        TestUtil.test_ids(self, self.expected['course'], self.actual['course'])

    def test_course_versions(self):
        TestUtil.test_course_versions(self, self.expected['course'], self.actual['course'])

    def test_auto_ids(self):
        TestUtil.test_ids(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_versions(self):
        TestUtil.test_unit_versions(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_credits(self):
        TestUtil.test_unit_credits(self, self.expected['automatic'], self.actual['automatic'])

    def test_planned_ids(self):
        TestUtil.test_ids(self, self.expected['planned'], self.actual['planned'])

    def test_planned_versions(self):
        TestUtil.test_unit_versions(self, self.expected['planned'], self.actual['planned'])

    def test_planned_credits(self):
        TestUtil.test_unit_credits(self, self.expected['planned'], self.actual['planned'])

    def test_planned_status(self):
        TestUtil.test_unit_status(self, self.expected['planned'], self.actual['planned'])

    def test_units_ids(self):
        TestUtil.test_ids(self, self.expected['units'], self.actual['units'])

    def test_units_versions(self):
        TestUtil.test_unit_versions(self, self.expected['units'], self.actual['units'])

    def test_units_credits(self):
        TestUtil.test_unit_credits(self, self.expected['units'], self.actual['units'])

    def test_units_status(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

    def test_units_attempts(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

class TestSteven(unittest.TestCase):
    expected = parser_expected.steven
    actual = parse_progress_report(open('test_inputs/Steven-pr.pdf', 'rb'))

    def test_name(self):
        TestUtil.test_string(self, self.expected['name'], self.actual['name'])

    def test_id(self):
        TestUtil.test_string(self, self.expected['id'], self.actual['id'])

    def test_date(self):
        TestUtil.test_string(self, self.expected['date'], self.actual['date'])

    def test_course_ids(self):
        TestUtil.test_ids(self, self.expected['course'], self.actual['course'])

    def test_course_versions(self):
        TestUtil.test_course_versions(self, self.expected['course'], self.actual['course'])

    def test_auto_ids(self):
        TestUtil.test_ids(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_versions(self):
        TestUtil.test_unit_versions(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_credits(self):
        TestUtil.test_unit_credits(self, self.expected['automatic'], self.actual['automatic'])

    def test_planned_ids(self):
        TestUtil.test_ids(self, self.expected['planned'], self.actual['planned'])

    def test_planned_versions(self):
        TestUtil.test_unit_versions(self, self.expected['planned'], self.actual['planned'])

    def test_planned_credits(self):
        TestUtil.test_unit_credits(self, self.expected['planned'], self.actual['planned'])

    def test_planned_status(self):
        TestUtil.test_unit_status(self, self.expected['planned'], self.actual['planned'])

    def test_units_ids(self):
        TestUtil.test_ids(self, self.expected['units'], self.actual['units'])

    def test_units_versions(self):
        TestUtil.test_unit_versions(self, self.expected['units'], self.actual['units'])

    def test_units_credits(self):
        TestUtil.test_unit_credits(self, self.expected['units'], self.actual['units'])

    def test_units_status(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

    def test_units_attempts(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

class TestXiMingWong(unittest.TestCase):
    expected = parser_expected.ximingwong
    actual = parse_progress_report(open('test_inputs/XiMingWong-pr.pdf', 'rb'))

    def test_name(self):
        TestUtil.test_string(self, self.expected['name'], self.actual['name'])

    def test_id(self):
        TestUtil.test_string(self, self.expected['id'], self.actual['id'])

    def test_date(self):
        TestUtil.test_string(self, self.expected['date'], self.actual['date'])

    def test_course_ids(self):
        TestUtil.test_ids(self, self.expected['course'], self.actual['course'])

    def test_course_versions(self):
        TestUtil.test_course_versions(self, self.expected['course'], self.actual['course'])

    def test_auto_ids(self):
        TestUtil.test_ids(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_versions(self):
        TestUtil.test_unit_versions(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_credits(self):
        TestUtil.test_unit_credits(self, self.expected['automatic'], self.actual['automatic'])

    def test_planned_ids(self):
        TestUtil.test_ids(self, self.expected['planned'], self.actual['planned'])

    def test_planned_versions(self):
        TestUtil.test_unit_versions(self, self.expected['planned'], self.actual['planned'])

    def test_planned_credits(self):
        TestUtil.test_unit_credits(self, self.expected['planned'], self.actual['planned'])

    def test_planned_status(self):
        TestUtil.test_unit_status(self, self.expected['planned'], self.actual['planned'])

    def test_units_ids(self):
        TestUtil.test_ids(self, self.expected['units'], self.actual['units'])

    def test_units_versions(self):
        TestUtil.test_unit_versions(self, self.expected['units'], self.actual['units'])

    def test_units_credits(self):
        TestUtil.test_unit_credits(self, self.expected['units'], self.actual['units'])

    def test_units_status(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

    def test_units_attempts(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

class TestYoakim(unittest.TestCase):
    expected = parser_expected.yoakim
    actual = parse_progress_report(open('test_inputs/Yoakim-pr.pdf', 'rb'))

    def test_name(self):
        TestUtil.test_string(self, self.expected['name'], self.actual['name'])

    def test_id(self):
        TestUtil.test_string(self, self.expected['id'], self.actual['id'])

    def test_date(self):
        TestUtil.test_string(self, self.expected['date'], self.actual['date'])

    def test_course_ids(self):
        TestUtil.test_ids(self, self.expected['course'], self.actual['course'])

    def test_course_versions(self):
        TestUtil.test_course_versions(self, self.expected['course'], self.actual['course'])

    def test_auto_ids(self):
        TestUtil.test_ids(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_versions(self):
        TestUtil.test_unit_versions(self, self.expected['automatic'], self.actual['automatic'])

    def test_auto_credits(self):
        TestUtil.test_unit_credits(self, self.expected['automatic'], self.actual['automatic'])

    def test_planned_ids(self):
        TestUtil.test_ids(self, self.expected['planned'], self.actual['planned'])

    def test_planned_versions(self):
        TestUtil.test_unit_versions(self, self.expected['planned'], self.actual['planned'])

    def test_planned_credits(self):
        TestUtil.test_unit_credits(self, self.expected['planned'], self.actual['planned'])

    def test_planned_status(self):
        TestUtil.test_unit_status(self, self.expected['planned'], self.actual['planned'])

    def test_units_ids(self):
        TestUtil.test_ids(self, self.expected['units'], self.actual['units'])

    def test_units_versions(self):
        TestUtil.test_unit_versions(self, self.expected['units'], self.actual['units'])

    def test_units_credits(self):
        TestUtil.test_unit_credits(self, self.expected['units'], self.actual['units'])

    def test_units_status(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

    def test_units_attempts(self):
        TestUtil.test_unit_status(self, self.expected['units'], self.actual['units'])

if __name__ == '__main__':
    unittest.main()
