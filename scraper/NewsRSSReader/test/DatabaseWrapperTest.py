
"""
DatabaseWrapperTest.py
Author: Zefu Lu (zefulu2)
Description: Test for DatabaseWrapper.py
Creation: 2014-11-5
"""

#===============================================================================
# import references
#===============================================================================
from DatabaseWrapper import DatabaseWrapper
import unittest
from dateutil.parser import parse

class DatabaseWrapperTest(unittest.TestCase):
    
    '''Setting up the Database Wrapper'''
    def setUp(self):
        self.db = DatabaseWrapper('./db_test_config.cfg')
        
    '''Test getColumns'''
    def testGetColumns(self):
        columns = self.db.getColumns('topics_test')
        self.assertEqual(len(columns), 5, "Should have 5 columns")
        self.assertEqual(columns[0], 'title', "First column is title")
        self.assertEqual(columns[4], 'source', "Last column is source")

    '''Test insert'''
    def testInsert(self):
        date = 'Thu, 14 Mar 2013 13:33:07 -0400'
        date = parse(date).strftime("%Y-%m-%d %H:%M:%S")
        dict_1 = {'title': 'title_1', 'date': date,'content': 'content_1', 'url':'url_1', 'source': 'source_1'}
        self.assertEqual(self.db.insertToTable('topics_test', dict_1), True, "Should have no errors")
        
    '''Test Select'''
    def testSelect(self):
        result = self.db.SelectFromTable('topics_test', ['title'], {'title':'title_1'})
        self.assertEqual(len(result), 1, "Should have 1 entry")
        