from .haldocument import HalDocument
from urllib.parse import urlparse
import http.client
import json
from .limeclient import LimeClientError


class EntityTypes:
    """
    Retrieve type information about entities in LIME Pro.

    :param lime_client: a logged in :class:`LimeClient` instance
    """
    def __init__(self, lime_client):
        self.lime_client = lime_client

    def get_by_url(self, url):
        """
        Retrieve a :class:`EntityType` given its url.

        :param url: this is the url that uniquely identifies an entity type.
        """
        parsed = urlparse(url)
        if not parsed.query:
            url += '?_embed=all'

        r = self.lime_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to get entity type {}'.format(url),
                                  r.status_code, r.text)
        return EntityType(json.loads(r.text), self.lime_client)

    def get_by_name(self, name):
        """
        Retrieve a :class:`EntityType` given its name in LIME Pro.

        :param name: name in LIME Pro (e.g. 'company')
        """
        url = '/metadata/entities/{}/?_embed=all'.format(name)
        return self.get_by_url(url)


class EntityType(HalDocument):
    """
    Represents a type of object in LIME Pro.
    """
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @property
    def fields(self):
        """
        Retrieve all fields for this entity type.
        """
        return {f.name: f for f in self.linked_resource('fields',
                                                        create_field)}

    @property
    def relations(self):
        """
        Retrieve all relations (:class:`Relation`) for this entity type.
        """
        return {r.name: r for r in self.linked_resource('relations', Relation)}


class SimpleField(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)


class OptionField(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    def option_by_localname(self, localname):
        return next(o for o in self.options if o.localname == localname)

    def option_by_key(self, key):
        return next(o for o in self.options if o.key == key)

    def option_by_id(self, id):
        return next(o for o in self.options if o.id == id)

    @property
    def options(self):
        return [Option(o) for o in self.hal['options']]


class Option:
    def __init__(self, raw):
        self.raw = raw

    @property
    def id(self):
        return self.raw['id']

    @property
    def key(self):
        return self.raw['key']

    @property
    def localname(self):
        return self.raw['localname']


def create_field(hal, lime_client):
    types = {
        'option': OptionField
    }
    ctor = types.get(hal['type'], SimpleField)
    return ctor(hal, lime_client)


class Relation(HalDocument):
    def __init__(self, hal, lime_client):
        super().__init__(hal, lime_client)

    @property
    def related(self):
        return self.linked_resource('related_entity', EntityType)
