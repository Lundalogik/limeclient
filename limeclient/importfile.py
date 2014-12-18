from .haldocument import HalDocument
import json
import http.client
from .limeclient import LimeClientError


class ImportFileHeaders(HalDocument):
    """
    Contains the headers of a parsed import file.

    :param hal: representation of an import file as returned from LIME.
    :param hal: lime_client :class:`LimeClient` to use for communication
        with LIME
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)


class ImportFiles:
    """
    Handles uploading of import files to LIME

    :param lime_client: a logged in :class:`LimeClient` instance
    """

    def __init__(self, lime_client):
        self.lime_client = lime_client

    def create(self, filename, content):
        """
        Upload an import file to LIME. Returns an :class:`ImportFile`
        instance

        :param filename: name of uploaded file
        :param content: a file object containing the data to import
        """
        files = {'file': (filename, content)}
        r = self.lime_client.post('/importfiles/', files=files)
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to create import file',
                                  r.status_code,
                                  r.text)
        return ImportFile(json.loads(r.text), self.lime_client)


class ImportFile(HalDocument):
    """
    Represents a file to import to LIME.

    :param hal: representation of an import file as returned from LIME.
    :param hal: lime_client :class:`LimeClient` to use for communication with
        LIME
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @property
    def headers(self):
        return self.linked_resource('headers', ImportFileHeaders)

    def save(self):
        self.lime_client.put(self.self_url, data=json.dumps(self.hal))
