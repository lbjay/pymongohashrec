# -*- coding: utf-8 -*-

import re
import json
import hashlib

from pymongo.collection import Collection
from injectors import DigestInjector
   
class HashrecCollection(Collection):
    
    def __init__(self, *args, **kwargs):

        try:
            self._hashrec_hashtype = kwargs.pop('hashrec_hashtype')
        except KeyError:
            self._hashrec_hashtype = 'sha1'
        
        try:
            self._hashrec_metapattern = re.compile(kwargs.pop('hashrec_metapattern'))
        except KeyError:
            self._hashrec_metapattern = re.compile('^_')

        super(HashrecCollection, self).__init__(*args, **kwargs)
        
        self.database.add_son_manipulator(DigestInjector())

    def record_digest(self, record):
        """
        generate a digest hash from a 'docs' dictionary
        """
        # first make a copy
        rec_copy = record.copy()
        
        # remove any 'meta' values
        for k in rec_copy.keys():
            if self._hashrec_metapattern.match(k):
                del rec_copy[k]
                
        h = hashlib.new(self._hashrec_hashtype)
        
        # AFAIK sort_keys=True should make this deterministic
        rec_str = json.dumps(rec_copy, sort_keys=True)
        h.update(rec_str)
        
        return h.hexdigest()  

    def update_if_changed(self, record):
        """
        updates a record in the collection only if it's hashed
        value differs from what's already stored
        """
        
        record["_digest"] = self.record_digest(record)

        # look for existing doc 
        spec = {'_id': record['_id'] } 
        wanted = {'_id': 1, '_digest': 1} 
        existing = self.find_one(spec, wanted, manipulate=False)

        if existing:
            # do the digest values match?
            if existing.has_key("_digest") and existing["_digest"] == record["_digest"]:
                # no change; do nothing
                return
            elif existing.has_key("_digest"):
                # add existing digest value to spec to avoid race conditions
                spec['_digest'] = existing["_digest"]
        
        # NOTE: even for cases where there was no existing doc we need to do an 
        # upsert to avoid race conditions
        return self.update(spec, record, manipulate=True, upsert=True)
