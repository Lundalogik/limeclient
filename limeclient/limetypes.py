from .haldocument import HalDocument
from urllib.parse import urlparse
import http.client
import json
from .limeclient import LimeClientError


class LimeTypes:
    """
    Retrieve type information about entities in LIME Pro.

    :param lime_client: a logged in :class:`LimeClient` instance
    """
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def get_by_url(self, url):
        """
        Retrieve a :class:`LimeType` given its url.

        :param url: this is the url that uniquely identifies an lime type.
        """
        parsed = urlparse(url)
        if not parsed.query:
            url += '?_embed=all'

        r = self.lime_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to get lime type {}'.format(url),
                                  r.status_code, r.text)
        return LimeType(json.loads(r.text), self.lime_client)

    def get_by_name(self, name):
        """
        Retrieve a :class:`LimeType` given its name in LIME Pro.

        :param name: name in LIME Pro (e.g. 'company')
        """
        url = '/metadata/entities/{}/?_embed=all'.format(name)
        return self.get_by_url(url)


class LimeType(HalDocument):
    """
    Represents a type of object in LIME Pro.
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @property
    def fields(self):
        """
        Retrieve all fields for this lime type.
        """
        return {f.name: f for f in self.linked_resource('fields',
                                                        create_field)}

    @property
    def relations(self):
        """
        Retrieve all relations (:class:`Relation`) for this lime type.
        """
        return {r.name: r for r in self.linked_resource('relations', Relation)}


class SimpleField(HalDocument):
    """
    Represents a simple field type.
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)


class OptionField(HalDocument):
    """
    Represents an option field type.
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    def option_by_localname(self, localname):
        """
        Retrieve an :class:`Option` value given its local name.
        """
        return next(o for o in self.options if o.localname == localname)

    def option_by_key(self, key):
        """
        Retrieve an :class:`Option` value given its key.
        """
        return next(o for o in self.options if o.key == key)

    def option_by_id(self, id):
        """
        Retrieve an :class:`Option` value given its id.
        """
        return next(o for o in self.options if o.id == id)

    @property
    def options(self):
        """
        All possible :class:`Option` values for this field.
        """
        return [Option(o) for o in self.hal['options']]


class Option:
    """
    Represents a possible value for an :class:`OptionField`.
    """
    def __init__(self, raw):
        self.raw = raw

    @property
    def id(self):
        """Id of the option value"""
        return self.raw['id']

    @property
    def key(self):
        """Key of the option value"""
        return self.raw['key']

    @property
    def localname(self):
        """Local name of the option value"""
        return self.raw['localname']


def create_field(hal, lime_client):
    types = {
        'option': OptionField
    }
    ctor = types.get(hal['type'], SimpleField)
    return ctor(hal, lime_client)


class Relation(HalDocument):
    """
    Represents a relation to another lime type in LIME Pro.
    """

    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @property
    def related(self):
        """The related :class:`LimeType`"""
        return self.linked_resource('related_entity', LimeType)
