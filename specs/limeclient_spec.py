from describe_it import describe, it, Fixture, before_each, after_each
from hamcrest import assert_that, equal_to
from limeclient import LimeClient
from unittest.mock import MagicMock

@describe
def limeclient():
    f = Fixture()

    @before_each
    def setup():
        f.client = LimeClient('http://example.org/', database='database')
        f.client._request = MagicMock()

    @it
    def uses_the_correct_method_for_get():
        f.client.get('/limeview/company/card/')
        args, _ = f.client._request.call_args
        method, url = args

        assert_that(method, equal_to('GET'))

    @it
    def gets_data_from_server_with_json_as_default_accepted_mimetype():
        f.client.get('/limeview/company/card/')
        assert_that(requested_header('Accept'),
                    equal_to('application/hal+json'))

    @it
    def gets_data_with_specified_mimetype_as_accepted():
        f.client.get('/limeview/company/card/', accept='text/plain')
        assert_that(requested_header('Accept'), equal_to('text/plain'))

    @it
    def posts_data_with_json_as_default_content_type():
        f.client.post('/limeview/company/card/')
        assert_that(requested_header('Content-Type'), equal_to('application/json'))

    @it
    def posts_data_with_specified_content_type():
        f.client.post('/limeview/company/card/', content_type='text/plain')
        assert_that(requested_header('Content-Type'), equal_to('text/plain'))

    @it
    def puts_data_with_json_as_default_content_type():
        f.client.put('/limeview/company/card/')
        assert_that(requested_header('Content-Type'),
                    equal_to('application/json'))

    @it
    def puts_data_with_specified_content_type():
        f.client.put('/limeview/company/card/', content_type='text/plain')
        assert_that(requested_header('Content-Type'), equal_to('text/plain'))

    def requested_header(header):
        _, kwargs = f.client._request.call_args
        headers = kwargs['headers']
        return headers[header]

