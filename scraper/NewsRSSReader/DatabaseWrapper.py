
"""
DatabaseWrapper.py
Author: Zefu Lu (zefulu2)
Description: This module serves as a wrapper of database 
             Provides database operations like insertion
Creation: 2014-11-4
"""

#===============================================================================
# import references
#===============================================================================
import sys
reload(sys)
import MySQLdb
from ConfigParser import SafeConfigParser
from datetime import datetime
from pprint import pprint as pp
import time    

class DatabaseWrapper(object):
    '''Constructor, taking in a config_file path'''
    def __init__(self, config_file):
        #initialize config file
        self.config = SafeConfigParser()
        self.config.read(config_file)
        
        #set up connection to MySQL database
        self.db = MySQLdb.connect(self.config.get('ip', 'ip'), self.config.get('ip', 'username'), self.config.get('ip', 'password'), self.config.get('database', 'database'))
        self.cursor = self.db.cursor()
    
    '''Insert operation, taking a table name and a dictionary of data'''
    def insertToTable(self, table, data_dict):
        columns = self.getColumns(table)
        
        #Automatically Construct the SQL statement
        sql = "INSERT INTO "+self.config.get('database', 'database')+"."+table+"("
        for column in columns:
            sql += column+","
        sql = sql[:-1] + ") VALUES ("
        for column in columns:
            if isinstance(data_dict[column], str):
                sql += "'"+MySQLdb.escape_string(data_dict[column])+"',"
            else:
                sql += str(data_dict[column])+","
        sql = sql[:-1] + ")"
        
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as detail:
            # Rollback in case there is any error
            self.db.rollback()
            print detail
            return False
        
    '''Select operation, taking a table name, a key, and a dictionary of restriction values for query'''
    def SelectFromTable(self, table, keys, query_dict):
        columns = self.getColumns(table)
        
        #Automatically Construct the SQL statement
        " SELECT * FROM EMPLOYEE \WHERE INCOME > '%d'"
        sql = "SELECT "
        for key in keys:
            sql += key+","
        sql = sql[:-1] + " FROM "+self.config.get('database', 'database')+"."+table + " WHERE "
        for key in query_dict.keys():
            sql += key+"='"+MySQLdb.escape_string(query_dict[key])+"' "
        result_list = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                row_dict= {}
                index = 0
                for key in keys:
                    row_dict[key] = row[index]
                    result_list.append(row_dict)
                    index+=1
        except Exception as detail:
            print detail
            return result_list
        return result_list
    
    '''Helper function that outputs a list of columns of a table, given a table name'''
    def getColumns(self, table):
        table_counter = 0
        while(self.config.has_section("table_"+str(table_counter))):
            if (self.config.get("table_"+str(table_counter), "table") == table):
                columns = self.config.get("table_"+str(table_counter), "columns")
                return columns.split(' ')
        return None
            
    
'''The main process'''
def main():
    #db = DatabaseWrapper('./config/db_config.cfg')
    pass
    
if __name__ == '__main__':
    main()