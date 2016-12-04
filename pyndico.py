import os
import hashlib
import hmac
import urllib
import time
import json

class Pyndico:
    '''Simple python wrapper for the CERN Indico API'''
    def __init__(self, *args, **kwargs):
        '''
        must supply a base url, e.g. "indico.cern.ch"
        Optional arguments (but required for non bublic calls):
            api_key = INDICO_APY_TOKEN
            secret_key = INDICO_SECRET_KEY
        '''
        base_url = args[0]
        if not 'http' in base_url:
            self.base_url = 'https://'+base_url
        else:
            self.base_url = base_url

        #some indico services allow call w/o tokens for public events
        self.api_key = kwargs.get('api_key', None)
        self.secret_key = kwargs.get('secret_key', None)

    def build_request(self, path, params, only_public=False, persistent=False):
        #based on example from indico docs
        #https://indico.readthedocs.io/en/latest/http_api/access/#request-signing-for-python
        items = params.items() if hasattr(params, 'items') else list(params)
        if self.api_key:
            items.append(('apikey', self.api_key))
        if only_public:
            items.append(('onlypublic', 'yes'))
        if self.secret_key:
            if not persistent:
                items.append(('timestamp', str(int(time.time()))))
            items = sorted(items, key=lambda x: x[0].lower())
            url = '%s?%s' % (self.base_url+path, urllib.urlencode(items))
            signature = hmac.new(self.secret_key, url, hashlib.sha1).hexdigest()
            items.append(('signature', signature))
        if not items:
            return path
        return '%s?%s' % (self.base_url+path, urllib.urlencode(items))

    def get(self, **kwargs):
        path = ['/export/']
        if 'qtype' not in kwargs:
            raise KeyError('Muse set type of data to export. \
                    e.g qtype = "event", "categ" or "room"')
        else:
            data_type = kwargs.pop('qtype')
        path.append(data_type+'/')    
        qtype_id = kwargs.pop('qtype_id')
        path.append(qtype_id+'.json')    
        #qtype an qtype_id popped from kwargs. Remaining kwargs are url params
        params = kwargs

        if not 'limit' in params:
            params['limit']=123

        request_url = self.build_request(
                ''.join(path),
                params)
        print(request_url)
        response = urllib.urlopen(request_url)
        print(response)

        return json.load(response)

    def get_event(self, **params):
        params.update(dict(qtype = 'event'))
        return self.get(**params)
    
    def get_category(self, **params):
        params.update(dict(qtype = 'categ'))
        return self.get(**params)
    
    def get_room(self, **params):
        params.update(dict(qtype = 'room'))
        return self.get(**params)


