import os
import sys
from datetime import datetime
import django


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE']='opinion.settings'

from django.contrib.auth.models import User
from appopinion.models import *

users = User.objects.all()
django.setup()

if __name__ == "__main__":
    """
    topic = Topic(
                title=item_dict['title'],
                date=item_dict['date'],
                content=item_dict['content'],
                url=item_dict['url'],
                source=item_dict['source'],
            )
    """
    

    topic = Topic(
                title='haha',
                date=datetime.now(),
                content='hahaha',
                url='google.com',
                source='K',
            )
    topic.save()

