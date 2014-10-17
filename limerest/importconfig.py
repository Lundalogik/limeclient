import collections
from .haldocument import HalDocument
import http.client
import json
from .restclient import RestClientError

class ImportConfigs:
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def create(self):
        url = '/importconfigs/'
        r = self.rest_client.post(url)
        if r.status_code != http.client.CREATED:
            raise RestClientError('Failed to create import config',
                                  r.status_code, r.text)
        return ImportConfig(json.loads(r.text), self.rest_client)

class ImportConfig(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

    @property
    def entity(self):
        return self.linked_resource('entity', Entity)

    @entity.setter
    def entity(self, val):
        self.add_linked_resource('entity', val)

    @property
    def importfile(self):
        return self.linked_resource('importfile', ImportFile)

    @importfile.setter
    def importfile(self, val):
        self.add_linked_resource('importfile', val)

    def add_field_mapping(self, mapping):
        self.field_mappings[mapping.field_url] = mapping.data

    def add_relation_mapping(self, mapping):
        self.relation_mappings[mapping.relation_url] = mapping.data

    def save(self):
        if '_embedded' in self.hal:
            del self.hal['_embedded']
        self.rest_client.put(self.self_url, data=json.dumps(self.hal))


class SimpleFieldMapping(collections.UserDict):
    def __init__(self, column, field, key=False):
        self._field = field
        self.data = {
            'column': column,
            'key': key
        }

    @property
    def field_url(self):
        return self._field.self_url


class OptionFieldMapping(collections.UserDict):
    def __init__(self, column, field):
        self._field = field
        self.data = {
            'column': column,
            'settings': {
                'mapping': {}
            }
        }

    @property
    def field_url(self):
        return self._field.self_url

    @property
    def default(self):
        return self._get_mapping('!')

    @default.setter
    def default(self, val):
        self._set_mapping('!', val)

    def map_value(self, column_val, field_val):
        self._set_mapping(column_val, field_val)

    def _get_mapping(self, key):
        return (self['settings']['mapping'][key]
                if key in self['settings']['mapping']
                else None)

    def _set_mapping(self, column_val, field_val):
        self['settings']['mapping'][column_val] = field_val


class RelationMapping(collections.UserDict):
    def __init__(self, column, relation, key_field):
        self._relation = relation
        self.data = {
            'column': column,
            'key_field': key_field.self_url
        }

    @property
    def relation_url(self):
        return self._relation.self_url

