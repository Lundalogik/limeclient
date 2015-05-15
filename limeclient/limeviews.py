from .haldocument import HalDocument
import http.client
import json
from .limeclient import LimeClientError


class Limeviews:
    def __init__(self, lime_client):
        self.lime_client = lime_client
        self.limeview_url = '/limeview/{}/{}/'

    def get_parsed(self, limetype, viewtype):
        url = self.limeview_url.format(limetype, viewtype)
        res = self.lime_client.get(url=url)
        if res.status_code != http.client.OK:
            raise LimeClientError('Failed to get lime view {}'.format(url),
                                  res.status_code, res.text)

        return Limeview(json.loads(res.text), self.lime_client)

    def get(self, limetype, viewtype):
        url = self.limeview_url.format(limetype, viewtype)
        res = self.lime_client.get(url=url, accept='text/plain')
        if res.status_code != http.client.OK:
            raise LimeClientError('Failed to get lime view {}'.format(url),
                                  res.status_code, res.text)

        return res.text

    def delete(self, limetype, viewtype):
        url = self.limeview_url.format(limetype, viewtype)
        #TODO: add error handling...
        self.lime_client.delete(url=url)

    def modify(self, limetype, viewtype, data):
        url = self.limeview_url.format(limetype, viewtype)
        #TODO: add error handling...
        self.lime_client.put(url=url, content_type='text/plain',
                                   data=data)

    def create(self, limetype, viewtype, data):
        url = self.limeview_url.format(limetype, viewtype)
        #TODO: add error handling...
        self.lime_client.post(url=url, content_type='text/plain',
                                   data=data)


class Limeview(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)
