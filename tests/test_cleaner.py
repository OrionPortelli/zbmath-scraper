import src.api.py_client as pyc

import unittest
import json

class TestCleaner(unittest.TestCase):
    # Date cleaning tests
    def test_dirty_date(self):
        """Tests that a record which scrapes a bad date can be cleaned successfully"""
        record = {"id": 6234389, "software": None, "msc": ["20"], "language": "English", "date": 4389}
        clean = pyc.cleanRecord(record)
        self.assertTrue(clean['date'] < 3000)

    def test_clean_date(self):
        """Tests that a record with a clean date is unaffected"""
        record = {"id": 5718024, "software": None, "msc": ["11", "33"], "language": "English", "date": 2009}
        clean = pyc.cleanRecord(record)
        self.assertEqual(clean, record, f'Expected {record}, got {clean}')

    # Language cleaning test
    def test_dirty_lang(self):
        """Tests that a record with a poorly formatted langauge field can be cleaned"""
        record = {
            "id": 6234001,
            "software": None,
            "msc": ["20", "03"], 
            "language": "English.\n                            Russian original",
            "date": 2013,
        }
        clean = pyc.cleanRecord(record)
        self.assertEqual(clean['language'], 'English')

    def test_clean_lang(self):
        """Tests that a record with a clean language field is unaffected"""
        record = {"id": 6023737, "software": None, "msc": ["20"], "language": "English", "date": 2012}
        clean = pyc.cleanRecord(record)
        self.assertEqual(clean, record, f'Expected {record}, got {clean}')

    def test_missing_dirty_lang(self):
        """Tests that a record with a poorly formatted language field is unaffected by a missing language on zbMATH"""
        # Note the system is not supposed to attempt to clean this currently
        record = {
            "id": 5733013,
            "software": None,
            "msc": ["11"],
            "language": "Chinese.\n                            English summary",
            "date": 2009
        }
        clean = pyc.cleanRecord(record)
        self.assertEqual(clean, record, f'Expected {record}, got {clean}')

    def test_missing_clean_lang(self):
        """Tests that a record with a clean language field is unnaffected by a missing language on zbMATH"""
        record = {
            "id": 6070337,
            "software": None, 
            "msc": ["11"],
            "language": "Chinese",
            "date": 2012
        }
        clean = pyc.cleanRecord(record)
        self.assertEqual(clean, record, f'Expected {record}, got {clean}')

if __name__ == "__main__":
    unittest.main()