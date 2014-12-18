import json
from describe_it import describe, it, Fixture, before_each, after_each
from hamcrest import (assert_that,
                      has_entry,
                      contains_inanyorder,
                      has_properties,
                      equal_to)
import limeclient as lc
import requests
from unittest.mock import MagicMock, patch


@describe
def hosting_login():
    f = Fixture()

    @before_each
    def setup():
        f.lime_client = lc.LimeClient(host='https://hosting.example.com')


    @it
    def starts_with_the_hosting_server_set_as_host():
        assert_that(f.lime_client.host,
                    equal_to('https://hosting.example.com'))

    @it
    def updates_the_host_when_redirected():
        mock_request = _build_redirecting_fake_request()

        with patch('requests.request', mock_request):
            f.lime_client.login(user='kalle', password='pass')
            assert_that(f.lime_client.host,
                        equal_to('https://myapp.example.com'))

    def _build_redirecting_fake_request():
        class Response:
            pass

        # First, let hosting redirect our request to create a new session
        hosting_response = Response()
        hosting_response.status_code = 307
        hosting_response.headers = {
            'location': 'https://myapp.example.com/api/v1/db/sessions/'
        }

        # Second, let the app server respond with info about the redirection
        app_response = Response()
        app_response.status_code = 201
        app_response.history = [hosting_response]
        app_response.url =  'https://myapp.example.com/api/v1/db/sessions/'
        app_response.text = json.dumps({'id': '<SESSION_ID>'})

        return MagicMock(return_value=app_response)

