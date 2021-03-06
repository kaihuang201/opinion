
"""
RSSReader.py
Author: Zefu Lu (zefulu2)
Description: This module retrieve RSS feeds from various sources, 
             and store them into a database
Creation: 2014-11-3
"""

#===============================================================================
# import references
#===============================================================================
import sys
reload(sys)
import urllib2
import xml.etree.ElementTree as ET
from DatabaseWrapper import DatabaseWrapper
from ConfigParser import SafeConfigParser
from datetime import datetime
from lxml import html
from pprint import pprint as pp
from dateutil.parser import parse

import os
from django.contrib.auth.models import User
from appopinion.models import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE']='portfolio.settings'
users = User.objects.all()

class RSSReader(object):
    
    '''Constructor, taking in a config_file path'''
    def __init__(self, config_file, db_config_file):
        #initialize config file
        self.config = SafeConfigParser()import os
import sys
from django.contrib.auth.models import User
        self.config.read(config_file)
        
        #initialize database wrapper
        self.db = DatabaseWrapper(db_config_file)

    def processRSS(self):
        source_counter = 0
        while(self.config.has_section("source_"+str(source_counter))):
            
            # Access the xml file through web
            try:
                pp(self.config.get("source_"+str(source_counter), "source"))
                rss_url = urllib2.urlopen(self.config.get("source_"+str(source_counter),"source"))
            except Exception:
                pp("Unable to access source " + str(source_counter))
                break
            
            xml_tree = ET.parse(rss_url)
            
            for item in xml_tree.getroot().iter(self.config.get("source_"+str(source_counter), "item_tag")):
                item_dict = {}
                item_dict['source'] = self.config.get("source_"+str(source_counter),"source_name")
                item_dict['title'] = html.fromstring(item.find(self.config.get("source_"+str(source_counter), "title_tag")).text).text
                item_dict['url'] = item.find(self.config.get("source_"+str(source_counter), "link_tag")).text
                item_dict['content'] = html.document_fromstring(item.find(self.config.get("source_"+str(source_counter), "content_tag")).text).text_content()
                item_dict['date'] = parse(item.find(self.config.get("source_"+str(source_counter), "date_tag")).text).strftime("%Y-%m-%d %H:%M:%S")
                
                """
                if len(self.db.SelectFromTable('appopinion_topic', ['title', 'url'], {'title':item_dict['title']})) == 0:
                    self.db.insertToTable('appopinion_topic', item_dict)
                """
                
                if not Topic.objects.filter(title=item_dict['title']):
                    topic = Topic(
                                title=item_dict['title'],
                                date=item_dict['date'],
                                content=item_dict['content'],
                                url=item_dict['url'],
                                source=item_dict['source'],
                            )
                    topic.save()
                
                
                pp(item_dict)
            source_counter += 1

'''The main process'''
def main():
    Reader = RSSReader('./config/rss_config.cfg','./config/db_config.cfg')
    Reader.processRSS()
    print "Done RSS reading at " + str(datetime.now())
    
if __name__ == '__main__':
    main()
