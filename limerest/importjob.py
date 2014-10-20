from .haldocument import HalDocument
import json
import http.client
from .limeclient import LimeClientError

EMPTY_HAL = {"_links": {}}
class ImportJobs:
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def create(self, import_config):
        url = '/importjobs/'
        job = ImportJob.create(import_config, self.lime_client)

        r = self.lime_client.post(url, data=json.dumps(job.hal))
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to create import job',
                                  r.status_code, r.text)
        return ImportJob(json.loads(r.text), self.lime_client)

    def get(self, url):
        r = self.lime_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to fetch import job',
                                  r.status_code, r.text)
        return ImportJob(json.loads(r.text), self.lime_client)


class ImportJob(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @staticmethod
    def create(config, lime_client):
        job = ImportJob(EMPTY_HAL, lime_client)
        job.add_linked_resource('importconfig', config)
        return job

    def refresh(self):
        return ImportJobs(self.lime_client).get(self.self_url)

    @property
    def errors(self):
        return self.linked_resource('errors', ImportJobErrors)

    @property
    def has_errors(self):
        return self.has_link('errors')

class ImportJobErrors(HalDocument):
    def __init__(self, hal, lime_client):
        # Fix: /importjobs/x/errors/ returns a naked array instead of HAL
        hal = {"errors": hal}
        super().__init__(hal, lime_client)

