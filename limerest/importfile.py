from .haldocument import HalDocument
import json
import http.client

class ImportFileHeaders(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)


class ImportFiles:
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def create(self, filename):
        files = {'file': (filename, open(filename, 'r'))}
        r = self.rest_client.post('/importfiles/', files=files)
        if r.status_code != http.client.CREATED:
            raise RestClientError('Failed to create import file', r.status_code,
                                  r.text)
        return ImportFile(json.loads(r.text), self.rest_client)

class ImportFile(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

    @property
    def headers(self):
        return self.linked_resource('headers', ImportFileHeaders)

    def save(self):
        self.rest_client.put(self.self_url, data=json.dumps(self.hal))

