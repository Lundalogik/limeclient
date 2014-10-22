import collections
from .haldocument import HalDocument
import http.client
import json
from .limeclient import LimeClientError

class ImportConfigs:
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def create(self, entity, importfile):
        url = '/importconfigs/'
        cfg = ImportConfig.create(self.lime_client, entity, importfile)

        r = self.lime_client.post(url, data=json.dumps(cfg.hal))
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to create import config',
                                  r.status_code, r.text)
        return ImportConfig(json.loads(r.text), self.lime_client)

class ImportConfig(HalDocument):
    CreateAndUpdate = 'create_and_update'
    OnlyUpdate = "only_update"
    OnlyCreate = "only_create"

    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @staticmethod
    def create(lime_client, entity, importfile):
        cfg = ImportConfig.create_empty(lime_client)
        cfg.entity = entity
        cfg.importfile = importfile
        return cfg

    @property
    def entity(self):
        return self.linked_resource('entity', EntityType)

    @entity.setter
    def entity(self, val):
        self.add_linked_resource('entity', val)

    @property
    def importfile(self):
        return self.linked_resource('importfile', ImportFile)

    @importfile.setter
    def importfile(self, val):
        self.add_linked_resource('importfile', val)

    def add_mapping(self, mapping):
        if type(mapping) == RelationMapping:
            self.relation_mappings[mapping.relation_url] = mapping.data
        else:
            self.field_mappings[mapping.field_url] = mapping.data

    def validate(self):
        return self.linked_resource('valid', ImportConfigStatus)

    def save(self):
        if '_embedded' in self.hal:
            del self.hal['_embedded']
        self.lime_client.put(self.self_url, data=json.dumps(self.hal))


class ImportConfigStatus(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

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
    def default(self, option):
        self._set_mapping('!', option.id)

    def map_option(self, column_val, option):
        self._set_mapping(column_val, option.id)

    def _get_mapping(self, key):
        return (self['settings']['mapping'][key]
                if key in self['settings']['mapping']
                else None)

    def _set_mapping(self, column_val, field_val):
        self['settings']['mapping'][column_val] = {'key': field_val}


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

