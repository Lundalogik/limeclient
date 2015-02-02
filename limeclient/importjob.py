from .haldocument import HalDocument
import json
import http.client
from .limeclient import LimeClientError

EMPTY_HAL = {"_links": {}}


class ImportJobs:
    """
    Handles the creation of a new import job.

    :param lime_client: a logged in :class:`LimeClient` instance
    """

    def __init__(self, lime_client):
        self.lime_client = lime_client

    def create(self, import_config):
        """
        Create a new :class:`ImportJob`. This indicates to the server that it
        can start executing the job as soon as possible.

        :param import_config: a ready :class:`ImportConfig` instance.
        """

        url = '/importjobs/'
        job = ImportJob.create(import_config, self.lime_client)

        r = self.lime_client.post(url, data=json.dumps(job.hal))
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to create import job',
                                  r.status_code, r.text)
        return ImportJob(json.loads(r.text), self.lime_client)

    def get(self, url):
        """
        Retrieve an existing :class:`ImportJob` from the server.

        :param url: the url that identifies the job on the server.
        """
        r = self.lime_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to fetch import job',
                                  r.status_code, r.text)
        return ImportJob(json.loads(r.text), self.lime_client)


class ImportJob(HalDocument):
    """
    Represents an import job on the server.

    :param lime_client: a logged in :class:`LimeClient` instance
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @staticmethod
    def create(config, lime_client):
        job = ImportJob.create_empty(lime_client)
        job.add_linked_resource('importconfig', config)
        return job

    def refresh(self):
        """
        Retrieve a fresh version of the import job from the server.
        """
        return ImportJobs(self.lime_client).get(self.self_url)

    @property
    def errors(self):
        """
        Retrieve a :class:`ImportJobErrors` that contains all errors for this
        job
        """
        return self.linked_resource('errors', ImportJobErrors)

    @property
    def has_errors(self):
        """
        Determine if this job has encountered any errors.
        """
        return self.has_link('errors')


class ImportJobErrors(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)
