
"""
CommentGenerator.py
Author: Zefu Lu (zefulu2)
Description: This Module generates comments and add it to the database
Creation: 2014-11-4
"""

#===============================================================================
# import references
#===============================================================================
import sys
reload(sys)
# from DatabaseWrapper import DatabaseWrapper
from datetime import datetime
from dateutil.parser import parse
from pprint import pprint as pp
from random import randrange
import time

import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE']='opinion.settings'

from django.contrib.auth.models import User
from appopinion.models import *

users = User.objects.all()
django.setup()

class CommentGenerator(object):
    '''Constructor'''
    def __init__(self, topic_id):
        self.topic_id = topic_id;
        #initialize database wrapper
        #self.db = DatabaseWrapper(db_config_file)
    
    def generate(self):
        counter= 1
        while(True):
            item_dict = {}
            item_dict['content'] = "Comment " + str(randrange(1000)) + "  @ "+datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            item_dict['date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            item_dict['parent_id'] = self.topic_id
            
            # self.db.insertToTable('newapp_comment', item_dict)
            topic = Topic.objects.get(pk=item_dict['parent_id'])
            comment = Comment(
                        content=item_dict['content'],
                        parent=topic,
                        date=item_dict['date'],
                       )
            comment.save()

            pp(item_dict)
            time.sleep(2)
            counter+=1

def main():
    generator = CommentGenerator(5)
    generator.generate()
    
if __name__ == '__main__':
    main()
