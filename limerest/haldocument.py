import http.client
import json
from .limeclient import LimeClientError


class HalDocument:
    def __init__(self, hal, rest_client):
        self.hal = hal
        self.rest_client = rest_client
        self._setup_properties()

    @property
    def self_url(self):
        return self.resource_link('self')['href']

    def linked_resource(self, link_name, resource_type):
        link = self.resource_link(link_name)

        if isinstance(link, list):
            return (self._get_resource(l, resource_type) for l in link)

        return self._get_resource(link, resource_type)

    def add_linked_resource(self, link_name, resource):
        self.hal['_links'][link_name] = resource.resource_link('self')
        self.embed(resource)

    def embed(self, resource):
        self.hal['_embedded'] = self.hal.get('_embedded') or {}
        self.hal['_embedded'][resource.self_url] = resource.hal

    def has_embedded(self, url):
        return '_embedded' in self.hal and url in self.hal['_embedded']

    def has_link(self, linkname):
        return '_links' in self.hal and linkname in self.hal['_links']

    def resource_link(self, link_name):
        return self.hal['_links'][link_name]

    def _get_resource(self, link, resource_type):
        url = link['href']
        if self.has_embedded(url):
            return resource_type(self.hal['_embedded'][url], self.rest_client)

        return self._load_resource(url, resource_type)

    def _load_resource(self, url, resource_type):
        r = self.rest_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to get linked resource',
                                  r.status_code,
                                  r.text)

        res = json.loads(r.text)

        return resource_type(res, self.rest_client)

    def _setup_properties(self):
        def getter(name):
            def get_property(self):
                return self.hal[name]
            return get_property

        def setter(name):
            def set_property(self, val):
                self.hal[name] = val
            return set_property

        for prop in self.hal:
            setattr(type(self), prop, property(getter(prop), setter(prop)))
