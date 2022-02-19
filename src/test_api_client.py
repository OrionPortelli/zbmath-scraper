import unittest
import api_client as api

class TestAPIClient(unittest.TestCase):
    # getCount: Valid filters
    def test_count_multipage(self):
        """Tests ID count when multiple pages required (>100 ID's)"""
        self.assertTrue(int(api.getIDCount(set='05', start='2020-01', end='2020-02')) > 100)

    def test_count_onepage(self):
        """Tests ID count when only one page returned (<100 ID's)"""
        self.assertTrue(api.getIDCount(set='05', start='2020-01-01', end='2020-01-04'))

    def test_count_none(self):
        """Tests ID count when no results match the filters (0 ID's)"""
        self.assertEqual(api.getIDCount(set='05', start='2020-01-01', end='2020-01-02'), 0)

    def test_count_flipped_dates(self):
        """Tests ID count when the start occurs after the end date (0 ID's)"""
        self.assertEqual(api.getIDCount(set='05', start='2020-01-02', end='2020-01-01'), 0)

    # getCount: Invalid filters
    def test_count_bad_msc(self):
        """Tests ID count when inputting invalid msc code filter"""
        with self.assertRaises(ValueError, msg="Bad argument (invalid filters)"):
            api.getIDCount(set='what', start='2020-01', end='2020-02')

    def test_count_bad_start(self):
        """Tests ID count when inputting invalid start filter"""
        with self.assertRaises(ValueError, msg="Bad argument (invalid filters)"):
            api.getIDCount(set='05', start='what', end='2020-02')

    def test_count_bad_end(self):
        """Tests ID count when inputting invalid end filter"""
        with self.assertRaises(ValueError, msg="Bad argument (invalid filters)"):
            api.getIDCount(set='05', start='2020-01', end='what')

    # getClasses: Returns correct amount (slow test)
    #def test_classes(self):
    #    """Tests getClasses returns the correct number of classes ("""
    #    self.assertEquals(len(api.getClasses()), 64)

    # getRecord: Valid records
    def test_record_valid(self):
        """Tests that the default example record can be scraped without error"""
        api.getRecord(5797851)

    def test_record_no_soft(self):
        """Tests that records with no software can be scraped without error"""
        api.getRecord(7465767)

    # getRecord: Invalid records
    # ...TBD

if __name__ == "__main__":
    unittest.main()