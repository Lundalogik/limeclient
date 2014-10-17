from .haldocument import HalDocument
import json
import http.client
from .restclient import RestClientError

EMPTY_HAL = {"_links": {}}
class ImportJobs:
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def create(self, import_config):
        url = '/importjobs/'
        job = ImportJob.create(import_config, self.rest_client)

        r = self.rest_client.post(url, data=json.dumps(job.hal))
        if r.status_code != http.client.CREATED:
            raise RestClientError('Failed to create import job',
                                  r.status_code, r.text)
        return ImportJob(json.loads(r.text), self.rest_client)

    def get(self, url):
        r = self.rest_client.get(url)
        if r.status_code != http.client.OK:
            raise RestClientError('Failed to fetch import job',
                                  r.status_code, r.text)
        return ImportJob(json.loads(r.text), self.rest_client)


class ImportJob(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

    @staticmethod
    def create(config, rest_client):
        job = ImportJob(EMPTY_HAL, rest_client)
        job.add_linked_resource('importconfig', config)
        return job

    def refresh(self):
        return ImportJobs(self.rest_client).get(self.self_url)

    @property
    def errors(self):
        return self.linked_resource('errors', ImportJobErrors)

class ImportJobErrors(HalDocument):
    def __init__(self, hal, rest_client):
        # Fix: /importjobs/x/errors/ returns a naked array instead of HAL
        hal = {"errors": hal}
        super().__init__(hal, rest_client)

