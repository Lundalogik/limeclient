import json
from urllib.parse import urljoin, urlparse
import requests
import http.client
import urllib.parse as up


class LimeClientError(Exception):
    def __init__(self, message, status_code, details):
        self.message = message
        self.status_code = status_code
        self.details = details

    def __str__(self):
        return "{0} ({1})\r\n{2}".format(
            self.message, self.status_code, self.details
        )


class LimeClient:
    """Handles all communication with LIME's API

        :param host: name of host to connect to
        :param database: name of database to logon to
        :param debug: if `True`, print traffic to stdout. Defaults to `False`
        :param verify_ssl_cert: if `False`, ignore SSL certificate
            verification. Defaults to `True`.
    """
    def __init__(self, host, database=None, debug=False, verify_ssl_cert=True):
        self.host = host
        self.session = None
        self.database = database
        self.debug = debug
        self.verify_ssl_cert = verify_ssl_cert

    def login(self, user=None, password=None):
        """
        Log in to LIME.

        :class:`LimeClient` should be used as a context manager. That
        way logging out and closing a session will be done automatically,
        even if an error is encountered.

        .. code-block:: python

            client = LimeClient('localhost', 'mydatabase')
            with client.login('user', 'pass') as c:
                # do stuff
        """

        data = {
            'database': self.database,
            'username': user,
            'password': password
        }
        data = json.dumps(data)

        r = self.request('POST', self._sessions_url(), data=data)
        if r.status_code != http.client.CREATED:
            raise LimeClientError('Failed to login!', r.status_code, r.text)

        self._update_host_if_redirected(r)

        self.session = json.loads(r.text)
        return self

    def logout(self):
        r = self.request('DELETE', self._sessions_url())
        if r.status_code != http.client.NO_CONTENT:
            raise LimeClientError('Failed to logout!', r.status_code, r.text)

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

        kwargs['verify'] = self.verify_ssl_cert

        if self.debug and 'data' in kwargs:
            print('===================================')
            print('REQUEST ({} {}):'.format(method, url))
            print(kwargs['data'])

        r = requests.request(method, url, **kwargs)

        if self.debug:
            print('===================================')
            print('RESPONSE ({} {}) (status: {}):'.format(method, url,
                                                          r.status_code))
            print(r.text)

        return r

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def _sessions_url(self):
        return urljoin(self.host, '/api/v1/sessions/')

    def _update_host_if_redirected(self, response):
        """
        If response contains info about a redirect, we'll use the new host
        for subsequent requests.
        """

        if not len(response.history):
            return

        parsed = up.urlsplit(response.url)
        self.host = up.urlunparse((parsed.scheme, parsed.netloc,
                                   '', '', '', ''))
