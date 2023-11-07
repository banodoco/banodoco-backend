import datetime
from django.db import transaction
from pytz import timezone

from ai_project.models import DBLock
from middleware.response import success

def use_lock(function, key):
    with transaction.atomic():
        if function == 'acquire':
            lock, created = DBLock.objects.get_or_create(row_key=key)
            if lock.created_on + datetime.timedelta(minutes=1) < datetime.datetime.now(tz=timezone('UTC')):
                created = True
                
            payload = {
                'data': True if created else False
            }
            return (payload, 'success', True)
        else:
            DBLock.objects.filter(row_key=key).delete()
            return ({'data': True}, 'success', True)