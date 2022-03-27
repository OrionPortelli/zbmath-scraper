import unittest
import src.api.py_client as pyc

class TestCleaner(unittest.TestCase):
    # Record cleaning test
    def test_count_multipage(self):
        """Tests that a record which scrapes a bad date can be cleaned successfully"""
        record = {"id": 6234389, "software": None, "msc": ["20"], "language": "English", "date": 4389}
        record = pyc.cleanRecord(record)
        self.assertTrue(record['date'] < 3000)

if __name__ == "__main__":
    unittest.main()