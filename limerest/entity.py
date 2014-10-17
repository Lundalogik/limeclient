from .haldocument import HalDocument
from urllib.parse import urlparse
import http.client
import json
from .restclient import RestClientError

class Entities:
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def get_by_url(self, url):
        parsed = urlparse(url)
        if not parsed.query:
            url += '?_embed=all'

        r = self.rest_client.get(url)
        if r.status_code != http.client.OK:
            raise RestClientError('Failed to get entity {}'.format(url),
                                  r.status_code, r.text)
        return Entity(json.loads(r.text), self.rest_client)

    def get_by_name(self, name):
        url = '/metadata/entities/{}/?_embed=all'.format(name)
        return self.get_by_url(url)

class Entity(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

    @property
    def fields(self):
        return {f.name: f for f in self.linked_resource('fields',
                                                        create_field)}

    @property
    def relations(self):
        return {r.name: r for r in self.linked_resource('relations', Relation)}


class SimpleField(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

class OptionField(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

    def option_id_for(self, localname):
        return next(o['id'] for o in self.options
                    if o['localname'] == localname)

def create_field(hal, rest_client):
    types = {
        'option': OptionField
    }
    ctor = types.get(hal['type'], SimpleField)
    return ctor(hal, rest_client)


class Relation(HalDocument):
    def __init__(self, hal, rest_client):
        super().__init__(hal, rest_client)

    @property
    def related(self):
        # Should really be stored in '_links'
        return Entities(self.rest_client).get_by_url(self.related_entity)

