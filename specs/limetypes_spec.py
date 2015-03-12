import responses
from describe_it import describe, it, Fixture, before_each, after_each
from .haldocs import (respond_post_session,
                      respond_get_metadata_company)
from limeclient import (LimeClient,
                        LimeTypes)
from hamcrest import (assert_that,
                      not_none,
                      same_instance,
                      has_properties)


@describe
def limetypes():
    f = Fixture()

    @before_each
    def setup_limetypes():
        responses.start()

    @after_each
    def teardown_limetypes():
        responses.stop()
        responses.reset()

    @describe
    def limetypes_get():

        @before_each
        def setup_limetypes_get():
            respond_post_session()
            respond_get_metadata_company()

            f.lime_client = LimeClient(host='http://example.com/',
                                       database='db')
            f.lime_client.login('admin', '')

        @it
        def can_get_company():
            lime_type = LimeTypes(f.lime_client).get_by_name('company')
            assert_that(lime_type, not_none())

        @it
        def can_get_company_from_cache():
            type_a = LimeTypes(f.lime_client).get_by_name('company')
            type_b = LimeTypes(f.lime_client).get_by_url(type_a.self_url)
            assert_that(type_a, same_instance(type_b))

    @describe
    def limetypes_props():
        @before_each
        def setup_limetypes_props():
            respond_post_session()
            respond_get_metadata_company()

        @it
        def props_of_company():
            lime_type = LimeTypes(f.lime_client).get_by_name('company')
            assert_that(lime_type, has_properties({
                'name': 'company',
                'localname': 'Företag'
            }))

        @it
        def props_of_company_name():
            lime_type = LimeTypes(f.lime_client).get_by_name('company')
            assert_that(lime_type.fields['name'], has_properties({
                'defaultvalue': '',
                'type': 'string',
                'readonly': False,
                'required': True,
                'name': 'name',
                'localname': 'Företagsnamn',
                'label': 'name',
                'length': 200
            }))

        def props_of_company_buyingstatus():
            lime_type = LimeTypes(f.lime_client).get_by_name('company')
            assert_that(lime_type.fields['buyingstatus'], has_properties({
                'type': 'option',
                'readonly': False,
                'required': False,
                'name': 'buyingstatus',
                'localname': 'Köpstatus',
                'label': 'none'
            }))

        def props_of_company_buyingstatus_defaultvalue():
            lime_type = LimeTypes(f.lime_client).get_by_name('company')
            assert_that(
                lime_type.fields['buyingstatus'].defaultvalue, has_properties({
                    'key': 'none',
                    'id': 108001,
                    'localname': ''
                }))