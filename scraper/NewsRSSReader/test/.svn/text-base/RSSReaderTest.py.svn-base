
"""
RSSReaderTest.py
Author: Zefu Lu (zefulu2)
Description: Test for RSSReader.py
Creation: 2014-11-5
"""

#===============================================================================
# import references
#===============================================================================
from RSSReader import RSSReader
import unittest

class RSSReaderTest(unittest.TestCase):
    
    '''Setting up the Database Wrapper'''
    def setUp(self):
        self.reader = RSSReader('./rss_test_config.cfg' ,'./db_test_config.cfg')
    
    '''Test the process'''
    def testProcess(self):
        self.reader.processRSS()
        result = self.db.SelectFromTable('topics_test', ['title'], {'title':'title 1'})
        self.assertEqual(len(result), 1, "Should have 1 entry")
        result = self.db.SelectFromTable('topics_test', ['title'], {'title':'title 2'})
        self.assertEqual(len(result), 1, "Should have 1 entry")
        result = self.db.SelectFromTable('topics_test', ['title'], {'title':'title 3'})
        self.assertEqual(len(result), 1, "Should have 1 entry")