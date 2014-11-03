import collections
from .haldocument import HalDocument
import http.client
import json
from .limeclient import LimeClientError

class ImportConfigs:
    """
    Manages creation of :class:`ImportConfig` instances in LIME

    :param lime_client: a logged in :class:`LimeClient` instance
    """
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def create(self, lime_type, importfile):
        """
        Create a new :class:`ImportConfig` instance in LIME.

        :param lime_type: :class:`LimeType` instance that references what type
            of data to import
        :param importfile: :class:`ImportFile` instance to import
        """

        url = '/importconfigs/'
        cfg = ImportConfig.create(self.lime_client, lime_type, importfile)

        r = self.lime_client.post(url, data=json.dumps(cfg.hal))
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to create import config',
                                  r.status_code, r.text)
        return ImportConfig(json.loads(r.text), self.lime_client)

class ImportConfig(HalDocument):
    """
    Used for configuring an import.

    :param hal: representation of an import file as returned from LIME.
    :param hal: lime_client :class:`LimeClient` to use for communication
        with LIME
    """
    CreateAndUpdate = 'create_and_update'
    OnlyUpdate = "only_update"
    OnlyCreate = "only_create"

    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @staticmethod
    def create(lime_client, lime_type, importfile):
        """
        Create a new instance of :class:`ImportConfig`

        :param lime_client: a logged in :class:`LimeClient` instance
        :param lime_type: :class:`LimeType` instance that references what type
            of data to import
        :param importfile: :class:`ImportFile` instance to import
        """
        cfg = ImportConfig.create_empty(lime_client)
        cfg.lime_type = lime_type
        cfg.importfile = importfile
        return cfg

    @property
    def lime_type(self):
        return self.linked_resource('entity', LimeType)

    @lime_type.setter
    def lime_type(self, val):
        self.add_linked_resource('entity', val)

    @property
    def importfile(self):
        return self.linked_resource('importfile', ImportFile)

    @importfile.setter
    def importfile(self, val):
        self.add_linked_resource('importfile', val)

    def add_mapping(self, mapping):
        """
        Add information about how to map a column in the import file to data
        in LIME.

        :param mapping: One of :class:`SimpleFieldMapping`,
            :class:`OptionFieldMapping`, or :class:`RelationMapping`.
        """
        if type(mapping) == RelationMapping:
            self.relation_mappings[mapping.relation_url] = mapping.data
        else:
            self.field_mappings[mapping.field_url] = mapping.data

    def validate(self):
        """
        Ask LIME to validate the import configuration. Returns an
            :class:`ImportConfigStatus` instance.
        """
        return self.linked_resource('valid', ImportConfigStatus)

    def save(self):
        """
        Save the import configuration in LIME.
        """
        if '_embedded' in self.hal:
            del self.hal['_embedded']
        self.lime_client.put(self.self_url, data=json.dumps(self.hal))


class ImportConfigStatus(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

class SimpleFieldMapping(collections.UserDict):
    """
    Maps a column to a simple field on the object we want to import to.

    :param column: Name of column in import file
    :param field: the field we want to map to
    :param key: if `True`, the value of this column will be used to find
        existing objects in LIME Pro.
    """
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
    """
    Maps a column to a simple field on the object we want to import to.

    :param column: Name of column in import file
    :param field: the field we want to map to
    """

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
        """
        The value to give the field if none of the mappings apply for the
        value in the column.
        """
        return self._get_mapping('!')

    @default.setter
    def default(self, option):
        self._set_mapping('!', option.id)

    def map_option(self, column_val, option):
        """
        Map a value for a column to an option for a field.

        :param column_val: a value of the column in the import file
        :param option: a :class:`Option` instance. The option value to map to.
        """
        self._set_mapping(column_val, option.id)

    def _get_mapping(self, key):
        return (self['settings']['mapping'][key]
                if key in self['settings']['mapping']
                else None)

    def _set_mapping(self, column_val, field_val):
        self['settings']['mapping'][column_val] = {'key': field_val}


class RelationMapping(collections.UserDict):
    """
    Use the value in a column to find a related object in LIME Pro.

    :param column: column that we want to map
    :param relation: the :class:`Relation` that we want to map.
    :param key_field: the field of the related type that we will match
        against to find related objects.
    """
    def __init__(self, column, relation, key_field):
        self._relation = relation
        self.data = {
            'column': column,
            'key_field': key_field.self_url
        }

    @property
    def relation_url(self):
        return self._relation.self_url

