import http.client
import json
from .limeclient import LimeClientError


class HalDocument:
    def __init__(self, hal, lime_client):
        self.hal = hal
        self.lime_client = lime_client
        self._setup_properties()

    @classmethod
    def create_empty(Klass, lime_client):
        EMPTY_HAL = {"_links": {}}
        return Klass(EMPTY_HAL, lime_client)

    @property
    def self_url(self):
        return self._resource_link('self')['href']

    def _get_properties(self):
        return {k: v for k, v in self.hal.items() if not k.startswith('_')}

    def _linked_resource(self, link_name, resource_type):
        link = self._resource_link(link_name)

        if isinstance(link, list):
            return (self._get_resource(l, resource_type) for l in link)

        return self._get_resource(link, resource_type)

    def _add_linked_resource(self, link_name, resource):
        self.hal['_links'][link_name] = resource._resource_link('self')
        self._embed(resource)

    def _embed(self, resource):
        self.hal['_embedded'] = self.hal.get('_embedded') or {}
        self.hal['_embedded'][resource.self_url] = resource.hal

    def _has_embedded(self, url):
        return '_embedded' in self.hal and url in self.hal['_embedded']

    def _has_link(self, linkname):
        return '_links' in self.hal and linkname in self.hal['_links']

    def _get_resource_link_href(self, link_name):
        return self._resource_link(link_name)['href']

    def _resource_link(self, link_name):
        return self.hal['_links'][link_name]

    def _get_resource(self, link, resource_type):
        url = link['href']
        if self._has_embedded(url):
            return resource_type(self.hal['_embedded'][url], self.lime_client)

        return self._load_resource(url, resource_type)

    def _load_resource(self, url, resource_type):
        r = self.lime_client.get(url)
        if r.status_code != http.client.OK:
            raise LimeClientError('Failed to get linked resource',
                                  r.status_code,
                                  r.text)

        res = json.loads(r.text)

        return resource_type(res, self.lime_client)

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
            if not hasattr(type(self), prop):
                setattr(type(self), prop, property(getter(prop), setter(prop)))
