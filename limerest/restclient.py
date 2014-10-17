import json
from urllib.parse import urljoin, urlparse
import requests
import http.client


class RestClientError(Exception):
    def __init__(self, message, status_code, details):
        self.message = message
        self.status_code = status_code
        self.details = details

    def __str__(self):
        return "{0} ({1})\r\n{2}".format(
            self.message, self.status_code, self.details
        )

class RestClient:
    def __init__(self, host, database):
        self.host = host
        self.session = None
        self.database = database

    def login(self, user=None, password=None):

        data = {
            'database': self.database,
            'username': user,
            'password': password
        }
        data = json.dumps(data)

        r = self.request('POST', self._sessions_url(), data=data)
        if r.status_code != http.client.CREATED:
            raise RestClientError('Failed to login!', r.status_code, r.text)

        self.session = json.loads(r.text)
        return self

    def logout(self):
        r = self.request('DELETE', self._sessions_url())
        if r.status_code != http.client.NO_CONTENT:
            raise RestClientError('Failed to logout!', r.status_code, r.text)

        self.session = None

    def get(self, url, **kwargs):
        url = self.normalize(url)
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        url = self.normalize(url)
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        url = self.normalize(url)
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        url = self.normalize(url)
        return self.request('DELETE', url, **kwargs)

    def normalize(self, url):
        parsed = urlparse(url)

        path = (parsed.path if parsed.path.startswith('/api/v1/')
                else self.build_path(parsed.path))

        if parsed.query:
            path += '?{}'.format(parsed.query)

        if not parsed.hostname:
            return urljoin(self.host, path)

        return urljoin(parsed.geturl(), path)


    def build_path(self, path):
        return '/api/v1/' + self.database + path

    def request(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})

        if self.session:
            headers['sessionid'] = self.session['id']

        kwargs['headers'] = headers

        if 'data' in kwargs:
            print('===================================')
            print('REQUEST ({} {}):'.format(method, url))
            print(kwargs['data'])

        r = requests.request(method, url, **kwargs)

        print('===================================')
        print('RESPONSE ({} {}):'.format(method, url))
        print(r.text)

        return r

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def _sessions_url(self):
        return urljoin(self.host, '/api/v1/sessions/')
