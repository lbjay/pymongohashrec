# -*- coding: utf-8 -*-

import hashlib

try:
    import ujson as json
except ImportError:
    pass
   
def record_digest(record, hashtype='sha1'):
    """
    generate a digest hash from a 'docs' dictionary
    """
    # first make a copy
    rec_copy = record.copy()
    
    # remove any 'meta' values
    for k in rec_copy.keys():
        if k.startswith('_'):
            del rec_copy[k]
            
    h = hashlib.new(hashtype)
    
    # AFAIK sort_keys=True should make this deterministic
    rec_str = json.dumps(rec_copy, sort_keys=True)
    h.update(rec_str)
    
    return h.hexdigest()  

def update_if_changed(self, record, collection):
    """
    updates a record in the collection only if it's hashed
    value differs from what's already stored
    """
    
    record["_digest"] = record_digest(record, self.db)
    spec = {'_id': record['_id'] } #, '_digest': digest}
    
    # look for existing doc 
    existing = collection.find_one(spec, manipulate=False)
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
    return collection.update(spec, record, manipulate=True, upsert=True)
