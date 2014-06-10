# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from pymongo.son_manipulator import SONManipulator

from utils import record_digest

class DatetimeInjector(SONManipulator):
    """
    Used for injecting/removing the datetime values of records
    """
    def __init__(self, collections=[]):
        self.collections = collections
        
    def transform_incoming(self, son, collection):
        if collection.name in self.collections:
            son['_dt'] = datetime.utcnow().replace(tzinfo=pytz.utc)
        return son
    
    def transform_outgoing(self, son, collection):
        if collection.name in self.collections:
            if son.has_key('_dt'):
                del son['_dt']
        return son
    
class DigestInjector(SONManipulator):
    """
    Inserts a digest hash of the contents of the doc being inserted
    """
    def __init__(self, collections=[]):
        self.collections = collections
        
    def transform_incoming(self, son, collection):
        if collection.name in self.collections:
            if not son.has_key('_digest'):
                son['_digest'] = record_digest(son, collection.database)
        return son
    
    def transform_outgoing(self, son, collection):
        if collection.name in self.collections:
            if son.has_key('_digest'):
                del son['_digest']
        return son 