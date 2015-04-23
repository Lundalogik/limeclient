from .haldocument import HalDocument
import http.client
import json
from .limeclient import LimeClientError


class Limeviews:
    def __init__(self, lime_client):
        self.lime_client = lime_client
        self.limeview_url = '/limeview/{}/{}/'

    def limeview_crud(self, method, limetype, viewtype, **kwargs):
        url = self.limeview_url.format(limetype, viewtype)
        r = getattr(self.lime_client, method)(url=url, **kwargs)

        if r.status_code != http.client.OK \
                and r.status_code != http.client.CREATED \
                and r.status_code != http.client.NO_CONTENT:
            raise LimeClientError('Failed to {} lime view {}'
                                  .format(method, url),
                                  r.status_code, r.text)

        if method == 'get' and 'headers' not in kwargs:
            return Limeview(json.loads(r.text), self.lime_client)
        elif method == 'get' and 'Accept' in kwargs.get('headers', '') \
                and kwargs['headers']['Accept'] == 'text/plain':
            return r.text
        else:
            return r.status_code

    def get_parsed(self, limetype, viewtype):
        return self.limeview_crud('get', limetype, viewtype)

    def get(self, limetype, viewtype):
        return self.limeview_crud('get', limetype, viewtype,
                                  headers={'Accept': 'text/plain'})

    def delete(self, limetype, viewtype):
        return self.limeview_crud('delete', limetype, viewtype)

    def modify(self, limetype, viewtype, data):
        return self.limeview_crud('put', limetype, viewtype, data=data)

    def create(self, limetype, viewtype, data):
        return self.limeview_crud('post', limetype, viewtype, data=data)


class Limeview(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)
