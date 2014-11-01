import responses
import json
import re


new_importfile = {
    "_links": {
        "headers": {
            "href": "/api/v1/db/importfiles/14/headers/"
        },
        "self": {
            "href": "/api/v1/db/importfiles/14/"
        }
    },
    "filename": "emdqnjim-import_person.txt",
    "original_filename": "import_person.txt",
    "delimiter": ";"
}


file_headers = {
    "_links": {
        "self": {
            "href":
            "/api/v1/db/importfiles/14/headers/"
        },
        "unique": {
            "first name": {
                "href":
                "/api/v1/db/importfiles/14/uniques/first%20name/"
            },
            "last name": {
                "href":
                "/api/v1/db/importfiles/14/uniques/last%20name/"
            },
        }
    },
    "headers": ["first name", "last name"]
}


new_importconfig = {
    "_links": {
        "self": {
            "href":
            "/api/v1/db/importconfigs/15/"
        },
        "entity": {
            "href":
            "/api/v1/db/metadata/entities/person/"
        },
        "valid": {
            "href":
            "/api/v1/db/importconfigs/15/valid/"
        },
        "importfile": {
            "href":
            "/api/v1/db/importfiles/14/"
        }
    },
    "field_mappings": {},
    "relation_mappings": {},
    "behavior": "create_and_update"
}

person_metadata = {
    "localname": "Person",
    "is_system": False,
    "name": "person",
    "_links": {
        "fields": [
            {"href": "/api/v1/db/metadata/entities/person/fields/phone/"},
            {"href": "/api/v1/db/metadata/entities/person/fields/firstname/"},
            {"href": "/api/v1/db/metadata/entities/person/fields/id/"},
            {"href": "/api/v1/db/metadata/entities/person/fields/company/"},
            {"href": "/api/v1/db/metadata/entities/person/fields/position/"},
            {"href": "/api/v1/db/metadata/entities/person/fields/name/"},
            ],
        "relations": [
            {"href": "/api/v1/db/metadata/entities/person/relations/company/"},
            ],
        "self": {"href": "/api/v1/db/metadata/entities/person/"},
        "data": {"href": "/api/v1/db/person/", "title": "Person"}
    }
}

position_metadata = {
    "_links": {
        "self": {
            "href":
            "/api/v1/db/metadata/entities/person/fields/position/",
            "title": "Befattning"}
    },
    "options": [
        {"id": 101201, "key": "", "localname": ""},
        {"id": 101601, "key": "", "localname": "Ekonomiansvarig"},
        {"id": 101701, "key": "", "localname": "Försäljningsansvarig"},
        ],
    "type": "option",
    "readonly": False,
    "required": False,
    "name": "position",
    "defaultvalue": {"id": 101201, "key": "", "localname": ""},
    "localname": "Befattning",
    "label": "jobtitle",
    "idfield": 19801
}

company_metadata = {
    "_links": {
        "self": {
            "href": "/api/v1/db/metadata/entities/company/"},
        "fields": [
            {"href":
            "/api/v1/db/metadata/entities/company/fields/id/"},
            {"href":
             "/api/v1/db/metadata/entities/company/fields/name/"}],
        "relations": [
            {"href":
             "/api/v1/db/metadata/entities/company/relations/person/"}],
        "data": {
            "href": "/api/v1/db/company/",
            "title": "Företag"}
    },
    "localname": "Företag",
    "is_system": False,
    "name": "company",
}


id_field = {
    "required": False,
    "_links": {
        "self": {
            "href": "/api/v1/db/metadata/entities/company/fields/id/",
            "title": "Post-ID (System)"}
    }, 
    "type": "system",
    "localname": "Post-ID (System)",
    "name": "id",
    "readonly": True
}

field_name = {
    "options": [],
    "defaultvalue": "",
    "type": "string",
    "readonly": False,
    "required": True,
    "_links": {
        "self": {"href": "/api/v1/db/metadata/entities/company/fields/name/", "title": "F\u00f6retagsnamn"}
    },
    "name": "name",
    "idfield": 4901,
    "localname": "Företagsnamn",
    "label": "name",
    "length": 200}


new_import_job = {
    "errors_count": 0,
    "status": "pending",
    "completed_time": None,
    "_links": {
        "importconfig": {
            "href": "/api/v1/lime_basic_v4_1/importconfigs/1/"
        },
        "self": {
            "href": "/api/v1/lime_basic_v4_1/importjobs/1/"}
    },
    "created_time": "2014-11-08T13:35:40.437036",
    "created_count": 0,
    "updated_count": 0,
    "started_time": None,
    "has_row_errors": False
}

def respond_post_importfile():
    responses.add(responses.POST,
                  'http://example.com/api/v1/db/importfiles/',
                  body=json.dumps(new_importfile),
                  status=201,
                  content_type='application/json')

def respond_put_importfile():
    responses.add_callback(
        responses.PUT,
        'http://example.com/api/v1/db/importfiles/14/',
        callback=lambda req: (200, {}, req.body),  # Just return body
        content_type='application/json')

def respond_get_headers():
    responses.add(responses.GET,
                  'http://example.com/api/v1/db/importfiles/14/headers/',
                  body=json.dumps(file_headers),
                  status=200,
                  content_type='application/json')

def respond_post_config():
    responses.add(responses.POST,
                  'http://example.com/api/v1/db/importconfigs/',
                  body=json.dumps(new_importconfig),
                  status=201,
                  content_type='application/json')

def respond_get_company():
    responses.add(responses.GET,
                  'http://example.com/api/v1/db/metadata/entities/company/',
                  body=json.dumps(file_headers),
                  status=200,
                  content_type='application/json')


def respond_get_person():
    match_url = re.compile(
        r'http://example.com/api/v1/db/metadata/entities/person/.*')
    responses.add(responses.GET,
                  match_url,
                  body=json.dumps(person_metadata),
                  status=200,
                  content_type='application/json')
