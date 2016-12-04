import hashlib
import hmac
import urllib
import time
import json

class PyndicoEventResponse:
    def __init__(self, result_json):
        self.response = result_json
        self._set_attributes()
    
    def _set_attributes(self):
        self.room = self.response['roomFullname']
        self.id = self.response['id']
        self.category = self.response['category']
        self.start = self.response['startDate']
        self.start_date = self.start['date']
        self.start_time = self.start['time']
        self.time_zone = self.start['tz']
        self.location = self.response['location']
        self.title = self.response['title']
        self.contributions = self.response['contributions']
        self.catalogue = [
                self._catalogue_contribution(c) 
                for c in self.contributions
                if c['startDate'] != None]
    
    def _catalogue_contribution(self, c):
        start =  c['startDate']
        time = start['time']
        tz = start['tz']

        title = c['title']
        speakers = [n['fullName'] for n in c['speakers']]
        attachments = []
        for f in c['folders']:
            for a in f['attachments']:
                if a['type'] == 'file':
                    attachments.append(
                            dict(
                                filename = a['filename'],
                                title = a['title'],
                                url = a['download_url'],
                                ))
        return dict(
            title = title,
            speakers = speakers,
            attachments = attachments,
            time = time,
            tz = tz
            )
    def __str__(self):
        return '{}, {}, {}-{}-{}'.format(
                self.title, 
                self.id, 
                self.start_date, 
                self.start_time, 
                self.time_zone)

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
            url = '%s?%s' % (path, urllib.urlencode(items))
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
        response = urllib.urlopen(request_url)

        return json.load(response)

    def get_event(self, **params):
        params.update(dict(qtype = 'event'))
        response =  self.get(**params)
        event_results = []
        for result in response['results']:
            try:
                event_results.append(
                        PyndicoEventResponse(result))
            except KeyError as e:
                print('Malformed Response: ', e, result)
        return event_results       
    
    def get_category(self, **params):
        params.update(dict(qtype = 'categ'))
        #TODO category response object
        return self.get(**params)
    
    def get_room(self, **params):
        params.update(dict(qtype = 'room'))
        #TODO room response object
        return self.get(**params)


