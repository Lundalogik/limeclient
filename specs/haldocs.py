import responses
import json
import re


session = {
    'id': '91EC44ECF2E64C5CB96DEC6B3A402D96010000',
    'database': 'db'
}

new_importfile = {
    '_links': {
        'headers': {
            'href': '/api/v1/db/importfiles/14/headers/'
        },
        'self': {
            'href': '/api/v1/db/importfiles/14/'
        }
    },
    'filename': 'emdqnjim-import_person.txt',
    'original_filename': 'import_person.txt',
    'delimiter': ';'
}

file_headers = {
    '_links': {
        'self': {
            'href':
            '/api/v1/db/importfiles/14/headers/'
        },
        'unique': {
            'first name': {
                'href':
                '/api/v1/db/importfiles/14/uniques/first%20name/'
            },
            'last name': {
                'href':
                '/api/v1/db/importfiles/14/uniques/last%20name/'
            },
        }
    },
    'headers': ['first name', 'last name']
}

new_importconfig = {
    '_links': {
        'self': {
            'href':
            '/api/v1/db/importconfigs/15/'
        },
        'entity': {
            'href':
            '/api/v1/db/metadata/entities/person/'
        },
        'valid': {
            'href':
            '/api/v1/db/importconfigs/15/valid/'
        },
        'importfile': {
            'href':
            '/api/v1/db/importfiles/14/'
        }
    },
    'field_mappings': {},
    'relation_mappings': {},
    'behavior': 'create_and_update'
}

person_metadata = {
    'localname': 'Person',
    'is_system': False,
    'name': 'person',
    '_links': {
        'fields': [
            {'href': '/api/v1/db/metadata/entities/person/fields/phone/'},
            {'href': '/api/v1/db/metadata/entities/person/fields/firstname/'},
            {'href': '/api/v1/db/metadata/entities/person/fields/id/'},
            {'href': '/api/v1/db/metadata/entities/person/fields/company/'},
            {'href': '/api/v1/db/metadata/entities/person/fields/position/'},
            {'href': '/api/v1/db/metadata/entities/person/fields/name/'},
        ],
        'relations': [
            {'href': '/api/v1/db/metadata/entities/person/relations/company/'},
            ],
        'self': {'href': '/api/v1/db/metadata/entities/person/'},
        'data': {'href': '/api/v1/db/person/', 'title': 'Person'}
    }
}

position_metadata = {
    '_links': {
        'self': {
            'href':
            '/api/v1/db/metadata/entities/person/fields/position/',
            'title': 'Befattning'}
    },
    'options': [
        {'id': 101201, 'key': '', 'localname': ''},
        {'id': 101601, 'key': '', 'localname': 'Ekonomiansvarig'},
        {'id': 101701, 'key': '', 'localname': 'Försäljningsansvarig'},
        ],
    'type': 'option',
    'readonly': False,
    'required': False,
    'name': 'position',
    'defaultvalue': {'id': 101201, 'key': '', 'localname': ''},
    'localname': 'Befattning',
    'label': 'jobtitle',
    'idfield': 19801
}

company_metadata = {
    '/api/v1/db/metadata/entities/company/': {
        '_links': {
            'self': {
                'href': '/api/v1/db/metadata/entities/company/'},
            'fields': [
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/id/'},
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/name/'},
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/buyingstatus/'},
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/created_by/'},
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/created_time/'},
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/modified_by/'},
                {'href':
                 '/api/v1/db/metadata/entities/company/fields/modified_time/'}
            ],
            'relations': [
                {'href':
                 '/api/v1/db/metadata/entities/company/relations/person/'}],
            'data': {
                'href': '/api/v1/db/company/',
                'title': 'Företag'}
        },
        'localname': 'Företag',
        'is_system': False,
        'name': 'company'
    },
    '/api/v1/db/metadata/entities/company/fields/created_by/': {
        'name': 'created_by',
        'readonly': True,
        'localname': 'Skapad av (System)',
        'required': False,
        'type': 'system'
    },
    '/api/v1/db/metadata/entities/company/fields/created_time/': {
        'name': 'created_time',
        'readonly': True,
        'localname': 'Skapad (System)',
        'required': False,
        'type': 'system'
    },
    '/api/v1/db/metadata/entities/company/fields/modified_by/': {
        'name': 'modified_by',
        'readonly': True,
        'localname': 'Senast uppdaterad av (System)',
        'required': False,
        'type': 'system'
    },
    '/api/v1/db/metadata/entities/company/fields/modified_time/': {
        'name': 'modified_time',
        'readonly': True,
        'localname': 'Senast uppdaterad (System)',
        'required': False,
        'type': 'system'
    },
    '/api/v1/db/metadata/entities/company/fields/id/': {
        'required': False,
        '_links': {
            'self': {
                'href': '/api/v1/db/metadata/entities/company/fields/id/',
                'title': 'Post-ID (System)'}
        },
        'type': 'system',
        'localname': 'Post-ID (System)',
        'name': 'id',
        'readonly': True
    },
    '/api/v1/db/metadata/entities/company/fields/name/': {
        'options': [],
        'defaultvalue': '',
        'type': 'string',
        'readonly': False,
        'required': True,
        '_links': {
            'self': {
                'href': '/api/v1/db/metadata/entities/company/fields/name/',
                'title': 'F\u00f6retagsnamn'}
        },
        'name': 'name',
        'idfield': 4901,
        'localname': 'Företagsnamn',
        'label': 'name',
        'length': 200
    },
    '/api/v1/db/metadata/entities/company/fields/buyingstatus/': {
        '_links': {
            'self': {
                'href':
                '/api/v1/db/metadata/entities/company/fields/buyingstatus/'}
        },
        'idfield': 25001,
        'type': 'option',
        'readonly': False,
        'required': False,
        'name': 'buyingstatus',
        'label': 'none',
        'localname': 'Köpstatus',
        'defaultvalue': {'key': 'none', 'localname': '', 'id': 108001},
        'options': [
            {'key': 'none', 'localname': '', 'id': 108001},
            {'key': 'notinterested', 'localname': 'Ej intressant', 'id': 108401},
            {'key': 'prospect', 'localname': 'Prospekt', 'id': 108501},
            {'key': 'active', 'localname': 'Aktiv kund', 'id': 108601},
            {'key': 'excustomer', 'localname': 'Före detta kund', 'id': 108701}
        ]
    }
}

new_import_job = {
    'errors_count': 0,
    'status': 'pending',
    'completed_time': None,
    '_links': {
        'importconfig': {
            'href': '/api/v1/lime_basic_v4_1/importconfigs/1/'
        },
        'self': {
            'href': '/api/v1/lime_basic_v4_1/importjobs/1/'}
    },
    'created_time': '2014-11-08T13:35:40.437036',
    'created_count': 0,
    'updated_count': 0,
    'started_time': None,
    'has_row_errors': False
}

lime_object_company = {
    '_links': {
        'self': {
            'href': '/api/v1/db/entities/invoice/1001',
        },
        'metadata': {
            'href': '/api/v1/db/metadata/entities/company/'
        },
    },
    'id': 1001,
    'created_time': '2012-11-13T00:00:00',
    'created_by': 201,
    'modified_time': '2012-11-13T00:00:00',
    'modified_by': 201,
    'name': 'Lundalogik AB',
    'buyingstatus': 'prospect'
}


def respond_post_session():
    responses.add(responses.POST,
                  'http://example.com/api/v1/sessions/',
                  body=json.dumps(session),
                  status=201,
                  content_type='application/json')


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


def respond_get_metadata_company():
    _respond_get_metadata(company_metadata)


def respond_get_person():
    match_url = re.compile(
        r'http://example.com/api/v1/db/metadata/entities/person/.*')
    responses.add(responses.GET,
                  match_url,
                  body=json.dumps(person_metadata),
                  status=200,
                  content_type='application/json')


def respond_get_limeobject_company():
    responses.add(responses.GET,
                  'http://example.com/api/v1/db/entities/company/1001',
                  body=json.dumps(lime_object_company),
                  status=200,
                  content_type='application/json')


def _respond_get_metadata(data):
    for url, metadata in data.items():
        responses.add(responses.GET,
                      'http://example.com{}'.format(url),
                      body=json.dumps(metadata),
                      status=200,
                      content_type='application/json')
