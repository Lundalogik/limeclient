from .haldocument import HalDocument
import json
import http.client
from .limeclient import LimeClientError

class ImportFileHeaders(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)


class ImportFiles:
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def create(self, filename, content):
        files = {'file': (filename, content)}
        r = self.lime_client.post('/importfiles/', files=files)
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to create import file', r.status_code,
                                  r.text)
        return ImportFile(json.loads(r.text), self.lime_client)

class ImportFile(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @property
    def headers(self):
        return self.linked_resource('headers', ImportFileHeaders)

    def save(self):
        self.lime_client.put(self.self_url, data=json.dumps(self.hal))

