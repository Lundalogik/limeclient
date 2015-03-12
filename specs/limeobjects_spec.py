import responses
import json
import io
from describe_it import describe, it, Fixture, before_each, after_each
from .haldocs import (respond_get_limeobject_company,
                      respond_get_metadata_company)
from io import StringIO
from limeclient import (LimeClient,
                        LimeObjects,
                        LimeObject)
from hamcrest import (assert_that,
                      not_none,
                      instance_of,
                      has_key,
                      has_properties,
                      equal_to)


@describe
def limeobjects():
    f = Fixture()

    @before_each
    def setup_limeobjects():
        responses.start()

    @after_each
    def teardown_limeobjects():
        responses.stop()
        responses.reset()

    @describe
    def limeobjects_get():

        @before_each
        def setup_limeobjects_get():
            respond_get_metadata_company()
            respond_get_limeobject_company()

            f.lime_client = LimeClient(host='http://example.com/',
                                       database='db')

        @it
        def get_company():
            lo = LimeObjects(f.lime_client).get_object('company', 1001)
            assert_that(lo, instance_of(LimeObject))

    @describe
    def limeobjects_props():

        @before_each
        def setup_limeobjects_props():
            respond_get_metadata_company()
            respond_get_limeobject_company()

            f.lime_client = LimeClient(host='http://example.com/',
                                       database='db')

        @it
        def props_of_company():
            lo = LimeObjects(f.lime_client).get_object('company', 1001)
            assert_that(lo, has_properties({
                'name': 'company',
                'localname': 'Företag'
            }))

        @it
        def props_of_company_name():
            lo = LimeObjects(f.lime_client).get_object('company', 1001)
            assert_that(lo.fields['name'], has_properties({
                'defaultvalue': '',
                'type': 'string',
                'readonly': False,
                'required': True,
                'name': 'name',
                'localname': 'Företagsnamn',
                'label': 'name',
                'length': 200,
                'value': 'Lundalogik AB'
            }))

        @it
        def props_of_company_buyingstatus():
            lo = LimeObjects(f.lime_client).get_object('company', 1001)
            assert_that(lo.fields['buyingstatus'], has_properties({
                'type': 'option',
                'readonly': False,
                'required': False,
                'name': 'buyingstatus',
                'localname': 'Köpstatus',
                'label': 'none'
            }))

        @it
        def props_of_company_buyingstatus_value():
            lo = LimeObjects(f.lime_client).get_object('company', 1001)
            assert_that(lo.fields['buyingstatus'].value, has_properties({
                'key': 'prospect',
                'id': 108501,
                'localname': 'Prospekt'
            }))
