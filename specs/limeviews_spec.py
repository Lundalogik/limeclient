from describe_it import describe, it, Fixture, before_each, after_each
from limeclient import LimeClient, Limeviews
from hamcrest import assert_that, equal_to
import http.client
import responses


@describe
def limeviews():
    f = Fixture()

    @before_each
    def setup():
        responses.start()
        f.limeclient = LimeClient('http://example.com', database='db')
        f.limeviews = Limeviews(f.limeclient)

    @after_each
    def teardown():
        responses.stop()
        responses.reset()

    @describe
    def get_as_plain_text():
        @before_each
        def setup():
            responses.add(responses.GET,
                          'http://example.com/api/v1/db/limeview/company/card/',
                          body='TEXT FOR VIEW',
                          status=200,
                          content_type='text/plain')

        @it
        def requests_the_view_as_plain_text():
            f.limeviews.get('company', 'card')
            accept = responses.calls[0].request.headers['Accept']
            assert_that(accept, equal_to('text/plain'))

    @describe
    def get_parsed():

        @before_each
        def setup():
            responses.add(responses.GET,
                          'http://example.com/api/v1/db/limeview/company/card/',
                          body='{}',
                          status=200,
                          content_type='application/hal+json')

        @it
        def requests_parsed_views_as_json():
            f.limeviews.get_parsed('company', 'card')
            accept = responses.calls[0].request.headers['Accept']
            assert_that(accept, equal_to('application/hal+json'))

    @describe
    def modify_limeview():

        @before_each
        def setup():
            responses.add(responses.PUT,
                          'http://example.com/api/v1/db/limeview/company/card/',
                          status=http.client.NO_CONTENT)

        @it
        def puts_limeviews_as_plain_text():
            f.limeviews.modify('company', 'card', data='VIEW DEFINITION')
            content_type = responses.calls[0].request.headers['Content-Type']
            assert_that(content_type, equal_to('text/plain'))

    @describe
    def create_limeview():

        @before_each
        def setup():
            responses.add(responses.POST,
                          'http://example.com/api/v1/db/limeview/company/card/',
                          status=http.client.CREATED)

        @it
        def posts_limeviews_as_plain_text():
            f.limeviews.create('company', 'card', data='VIEW DEFINITION')
            content_type = responses.calls[0].request.headers['Content-Type']
            assert_that(content_type, equal_to('text/plain'))

    @describe
    def delete_limeview():

        @before_each
        def setup():
            responses.add(responses.DELETE,
                          'http://example.com/api/v1/db/limeview/company/card/',
                          status=http.client.NO_CONTENT)

        @it
        def posts_limeviews_as_plain_text():
            f.limeviews.delete('company', 'card')
            url = responses.calls[0].request.url
            assert_that(url, equal_to('http://example.com/api/v1/db/limeview/company/card/'))
