import responses
import json
import io
from describe_it import describe, it, Fixture, before_each, after_each
from .haldocs import (respond_post_config,
                      respond_post_importfile,
                      respond_put_importfile,
                      respond_get_headers,
                      respond_get_person)
from io import StringIO
from limeclient import (LimeClient,
                        ImportConfigs,
                        ImportConfig,
                        LimeTypes,
                        ImportFiles)
from hamcrest import (assert_that,
                      has_entry,
                      contains_inanyorder,
                      has_properties,
                      equal_to)


@describe
def limeclient():
    f = Fixture()

    @before_each
    def setup():
        responses.start()

    @after_each
    def teardown():
        responses.stop()
        responses.reset()

    @describe
    def importfile():

        @before_each
        def setup():
            respond_post_importfile()
            respond_put_importfile()
            respond_get_headers()

            f.lime_client = LimeClient(host='http://example.com/',
                                       database='db')
        @it
        def can_be_created():
            impfile = create_file()
            assert_that(impfile, has_properties({
                "filename": "emdqnjim-import_person.txt",
                "original_filename": "import_person.txt",
                "delimiter": ";"
            }))

        @it
        def can_retrieve_headers():
            impfile = create_file()
            headers = impfile.headers

            assert_that(headers.headers,
                        contains_inanyorder('first name', 'last name'))

        @it
        def can_be_saved():
            impfile = create_file()
            impfile.delimiter = ','
            impfile.save()

            saved = json.loads(responses.calls[1].request.body)
            assert_that(saved, has_entry('delimiter', ','))

        def create_file():
            return ImportFiles(f.lime_client).create(
                filename='import_person.txt',
                content=io.StringIO('CONTENT'))

    @describe
    def importconfig():

        @before_each
        def setup():
            respond_post_config()
            respond_get_person()
            respond_post_importfile()

            f.lime_client = LimeClient(host='http://example.com/',
                                       database='db')

        @describe
        def newly_created():

            @before_each
            def setup():
                lime_type = LimeTypes(f.lime_client).get_by_name('person')
                importfile = ImportFiles(f.lime_client).create(
                    filename='filename.txt',
                    content=StringIO(''))

                f.cfg = ImportConfigs(f.lime_client).create(
                    lime_type=lime_type,
                    importfile=importfile)

            @it
            def defaults_to_create_and_update():
                assert_that(f.cfg.behavior,
                            equal_to(ImportConfig.CreateAndUpdate))
