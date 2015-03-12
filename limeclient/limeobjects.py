from .limeclient import LimeClientError
from .limetypes import (LimeTypes,
                        SimpleField,
                        OptionField)
from urllib.parse import urlparse
import http.client
import json


class LimeObjects:
    """
    Get, update or delete one or multiple lime objects.

    :param lime_client: a logged in :class:`LimeClient` instance
    """
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def get_object_by_url(self, url):
        """
        Retrieve a :class:`LimeType` given its url.

        :param url: a url that uniquely identifies an lime object.
        """
        parsed = urlparse(url)
        if not parsed.query:
            url += '?_embed=all'

        r = self.lime_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to get lime type {}'.format(url),
                                  r.status_code, r.text)
        return LimeObject(json.loads(r.text), self.lime_client)

    def get_object(self, lime_type, lime_id):
        """
        Retrieve a :class:`LimeType` given its url.

        :param lime_type: name of the lime type to retrieve
        :param lime_id: id of the lime object to retrieve
        """
        url = '/entities/{}/{}'.format(lime_type, lime_id)
        return self.get_object_by_url(url)


class LimeObject:
    def __init__(self, hal, lime_client):
        self.lime_client = lime_client
        self.hal = hal
        self._fields = None
        self._lime_type = None

    @property
    def fields(self):
        """
        Retrieve all fields for this lime object
        """

        if not self._fields:
            self._fields = {
                f.name: self._create_value(f) for f
                in self.lime_type.fields.values()
                if f.name in self.hal
            }

        return self._fields

    @property
    def lime_type(self):
        if not self._lime_type:
            self._lime_type = LimeTypes(self.lime_client).get_by_url(
                self.hal['_links']['metadata']['href'])

        return self._lime_type

    @property
    def localname(self):
        return self.lime_type.localname

    @property
    def name(self):
        return self.lime_type.name

    def _create_value(self, field):
        types = {
            'option': OptionValue
        }

        ctor = types.get(field.type, SimpleValue)
        return ctor(self.hal[field.name], field.hal, self.lime_client)


class SimpleValue(SimpleField):
    def __init__(self, value, hal, lime_client):
        super().__init__(hal, lime_client)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class OptionValue(OptionField):
    def __init__(self, value, hal, lime_client):
        super().__init__(hal, lime_client)
        self._value = self.option_by_key(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
